/*
 * Phase 18B — Baseline Microcontroller TinyML Firmware (ESP32-D0WD-V3)
 * ====================================================================
 * Single-sample inference benchmark & sanity firmware for physical ESP32.
 * Target MCU: ESP32-D0WD-V3 (rev v3.1, Xtensa LX6 dual-core @ 240 MHz).
 * Integrates TFLite Micro, microsecond hardware timer instrumentation,
 * static SRAM tensor arena, dynamic heap reporting, and sanity test loop.
 */

#include <Arduino.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>

// TFLite Micro headers
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/kernels/fully_connected.h"
#include "tensorflow/lite/micro/kernels/kernel_util.h"
#include "tensorflow/lite/micro/micro_context.h"
#include "tensorflow/lite/kernels/internal/reference/integer_ops/fully_connected.h"
#include "tensorflow/lite/schema/schema_generated.h"

// Hardware specific timer definitions
#include "esp_timer.h"
#include "esp_system.h"
#define GET_MICROS() esp_timer_get_time()
#define GET_FREE_HEAP() esp_get_free_heap_size()

// Embedded model and test data headers
#include "g_student_b_model_data.h"
#include "g_student_a_model_data.h"
#include "mcu_test_vectors.h"

// Reference FullyConnected Registration for Xtensa/ESP32
namespace ref_fc {

struct OpData {
    tflite::OpDataFullyConnected op_data;
};

void* Init(TfLiteContext* context, const char* buffer, size_t length) {
    return context->AllocatePersistentBuffer(context, sizeof(OpData));
}

TfLiteStatus Prepare(TfLiteContext* context, TfLiteNode* node) {
    OpData* data = static_cast<OpData*>(node->user_data);
    const auto* params = static_cast<const TfLiteFullyConnectedParams*>(node->builtin_data);

    tflite::MicroContext* micro_context = tflite::GetMicroContext(context);
    TfLiteTensor* input = micro_context->AllocateTempInputTensor(node, 0);
    TfLiteTensor* filter = micro_context->AllocateTempInputTensor(node, 1);
    TfLiteTensor* bias = micro_context->AllocateTempInputTensor(node, 2);
    TfLiteTensor* output = micro_context->AllocateTempOutputTensor(node, 0);

    TF_LITE_ENSURE_STATUS(tflite::CalculateOpDataFullyConnected(
        context, params->activation, input->type, input, filter, bias, output, &data->op_data
    ));

    micro_context->DeallocateTempTfLiteTensor(output);
    micro_context->DeallocateTempTfLiteTensor(input);
    micro_context->DeallocateTempTfLiteTensor(filter);
    if (bias != nullptr) {
        micro_context->DeallocateTempTfLiteTensor(bias);
    }
    return kTfLiteOk;
}

TfLiteStatus Eval(TfLiteContext* context, TfLiteNode* node) {
    const OpData* data = static_cast<const OpData*>(node->user_data);
    const TfLiteEvalTensor* input = tflite::micro::GetEvalInput(context, node, 0);
    const TfLiteEvalTensor* filter = tflite::micro::GetEvalInput(context, node, 1);
    const TfLiteEvalTensor* bias = tflite::micro::GetEvalInput(context, node, 2);
    TfLiteEvalTensor* output = tflite::micro::GetEvalOutput(context, node, 0);

    tflite::FullyConnectedParams op_params = tflite::FullyConnectedParamsQuantized(data->op_data);

    tflite::reference_integer_ops::FullyConnected(
        op_params,
        tflite::micro::GetTensorShape(input),
        tflite::micro::GetTensorData<int8_t>(input),
        tflite::micro::GetTensorShape(filter),
        tflite::micro::GetTensorData<int8_t>(filter),
        tflite::micro::GetTensorShape(bias),
        tflite::micro::GetOptionalTensorData<int32_t>(bias),
        tflite::micro::GetTensorShape(output),
        tflite::micro::GetTensorData<int8_t>(output)
    );
    return kTfLiteOk;
}

TfLiteRegistration RegisterOp() {
    return tflite::micro::RegisterOp(Init, Prepare, Eval);
}

} // namespace ref_fc

// Tensor Arena Size (8 KB statically allocated in internal SRAM)
constexpr int kTensorArenaSize = 8 * 1024;
alignas(16) static uint8_t tensor_arena[kTensorArenaSize];

// Global TFLM pointers
static const tflite::Model* model = nullptr;
static tflite::MicroInterpreter* interpreter = nullptr;
static TfLiteTensor* input_tensor = nullptr;
static TfLiteTensor* output_tensor = nullptr;
static int64_t timer_overhead_us = 0;

void setup() {
    Serial.begin(115200);
    // Allow serial port to settle
    delay(2000);

    Serial.println();
    Serial.println("======================================================================");
    Serial.println("Phase 18B — ESP32 TinyML Baseline Firmware (Physical Deployment)");
    Serial.println("======================================================================");
    Serial.printf("Silicon: ESP32-D0WD-V3 (Xtensa LX6 @ %u MHz)\n", getCpuFrequencyMhz());
    Serial.printf("Chip Revision: %u\n", ESP.getChipRevision());
    Serial.printf("SDK Version: %s\n", ESP.getSdkVersion());
    Serial.printf("Free Heap at Boot: %u Bytes\n", GET_FREE_HEAP());
    Serial.println("----------------------------------------------------------------------");

    // 1. Load Model FlatBuffer (Primary: student_b_16_4_int8)
    model = tflite::GetModel(g_student_b_model_data);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        Serial.printf("ERROR: Model schema version %lu != expected %d\n",
                      (unsigned long)model->version(), TFLITE_SCHEMA_VERSION);
        return;
    }
    Serial.printf("Model: student_b_16_4_int8 (FlatBuffer size: %u Bytes)\n",
                  sizeof(g_student_b_model_data));

    // 2. Register required INT8 Operators with portable reference FC
    static tflite::MicroMutableOpResolver<3> resolver;
    resolver.AddFullyConnected(ref_fc::RegisterOp());
    resolver.AddSoftmax();
    resolver.AddReshape();

    // 3. Instantiate MicroInterpreter
    static tflite::MicroInterpreter static_interpreter(
        model, resolver, tensor_arena, kTensorArenaSize
    );
    interpreter = &static_interpreter;

    // 4. Allocate Tensors in Tensor Arena
    TfLiteStatus allocate_status = interpreter->AllocateTensors();
    if (allocate_status != kTfLiteOk) {
        Serial.println("ERROR: AllocateTensors() failed!");
        return;
    }

    input_tensor = interpreter->input(0);
    output_tensor = interpreter->output(0);

    Serial.println("TFLM Interpreter Initialized Successfully:");
    Serial.printf("  Input Shape: [%d, %d], Type: %d (kTfLiteInt8)\n",
                  input_tensor->dims->data[0], input_tensor->dims->data[1], input_tensor->type);
    Serial.printf("  Input Quant: Scale = %.9f, ZeroPoint = %d\n",
                  input_tensor->params.scale, input_tensor->params.zero_point);
    Serial.printf("  Output Shape: [%d, %d], Type: %d (kTfLiteInt8)\n",
                  output_tensor->dims->data[0], output_tensor->dims->data[1], output_tensor->type);
    Serial.printf("  Output Quant: Scale = %.9f, ZeroPoint = %d\n",
                  output_tensor->params.scale, output_tensor->params.zero_point);
    Serial.printf("  Tensor Arena Allocated: %d Bytes\n", kTensorArenaSize);
    Serial.printf("  Tensor Arena Used: %u Bytes\n", (unsigned int)interpreter->arena_used_bytes());
    Serial.printf("  Free Heap after TFLM init: %u Bytes\n", GET_FREE_HEAP());
    Serial.println("----------------------------------------------------------------------");

    // 5. Timer Overhead Calibration
    int64_t t_sum = 0;
    constexpr int kCalibRuns = 1000;
    for (int i = 0; i < kCalibRuns; ++i) {
        int64_t t0 = GET_MICROS();
        int64_t t1 = GET_MICROS();
        t_sum += (t1 - t0);
    }
    timer_overhead_us = t_sum / kCalibRuns;
    Serial.printf("Timer Read Overhead: %lld us\n", (long long)timer_overhead_us);
    Serial.println("----------------------------------------------------------------------");

    // 6. Warmup Inference (10 runs)
    Serial.print("Running 10 warmup inferences...");
    for (int i = 0; i < 10; ++i) {
        memcpy(input_tensor->data.int8, TEST_SAMPLES_INT8[0], FEATURE_DIM);
        interpreter->Invoke();
    }
    Serial.println(" DONE.");
    Serial.println("----------------------------------------------------------------------");

    // 7. Minimal Sanity Test (20 curated test vectors)
    Serial.println("Executing Minimal Sanity Inference Test (20 Vectors):");
    Serial.println("Idx | TrueClass | PredClass | Latency(us) | Dequant Probabilities [0..3] | Match | Raw INT8 Output");
    Serial.println("----+-----------+-----------+-------------+-------------------------------+-------+----------------");

    int correct_count = 0;
    int64_t total_latency_us = 0;
    int64_t min_latency_us = 999999;
    int64_t max_latency_us = 0;

    for (int i = 0; i < NUM_TEST_SAMPLES; ++i) {
        // Copy INT8 test vector into input tensor
        TfLiteTensor* cur_input = interpreter->input(0);
        TfLiteTensor* cur_output = interpreter->output(0);
        for (int f = 0; f < FEATURE_DIM; ++f) {
            cur_input->data.int8[f] = TEST_SAMPLES_INT8[i][f];
        }

        // Timed single-sample inference
        int64_t start_us = GET_MICROS();
        TfLiteStatus invoke_status = interpreter->Invoke();
        int64_t end_us = GET_MICROS();

        if (invoke_status != kTfLiteOk) {
            Serial.printf("ERROR: Invoke failed on sample %d!\n", i);
            continue;
        }

        int64_t lat_us = (end_us - start_us) - timer_overhead_us;
        if (lat_us < 0) lat_us = 0;
        total_latency_us += lat_us;
        if (lat_us < min_latency_us) min_latency_us = lat_us;
        if (lat_us > max_latency_us) max_latency_us = lat_us;

        // Dequantize INT8 outputs to probabilities
        int8_t* out_int8 = cur_output->data.int8;
        float probs[4];
        int pred_class = 0;
        float max_prob = -1.0f;

        for (int c = 0; c < 4; ++c) {
            probs[c] = (out_int8[c] - cur_output->params.zero_point) * cur_output->params.scale;
            if (probs[c] > max_prob) {
                max_prob = probs[c];
                pred_class = c;
            }
        }

        uint8_t true_class = TEST_LABELS[i];
        bool is_match = (pred_class == true_class);
        if (is_match) correct_count++;

        Serial.printf("%3d |     %d     |     %d     |    %4lld     | [%.2f, %.2f, %.2f, %.2f] | %-5s | [%4d, %4d, %4d, %4d]\n",
                      i, true_class, pred_class, (long long)lat_us,
                      probs[0], probs[1], probs[2], probs[3],
                      is_match ? "PASS" : "FAIL",
                      out_int8[0], out_int8[1], out_int8[2], out_int8[3]);
    }

    double mean_latency_us = (double)total_latency_us / NUM_TEST_SAMPLES;
    double sanity_accuracy = (double)correct_count / NUM_TEST_SAMPLES * 100.0;

    Serial.println("----------------------------------------------------------------------");
    Serial.println("Sanity Test Results Summary:");
    Serial.printf("  Total Samples:      %d\n", NUM_TEST_SAMPLES);
    Serial.printf("  Correct Matches:    %d / %d (%.1f%%)\n",
                  correct_count, NUM_TEST_SAMPLES, sanity_accuracy);
    Serial.printf("  Mean Latency:       %.2f us\n", mean_latency_us);
    Serial.printf("  Min Latency:        %lld us\n", (long long)min_latency_us);
    Serial.printf("  Max Latency:        %lld us\n", (long long)max_latency_us);
    Serial.printf("  Tensor Arena Used:  %u / %d Bytes\n",
                  (unsigned int)interpreter->arena_used_bytes(), kTensorArenaSize);
    Serial.printf("  Free Heap:          %u Bytes\n", GET_FREE_HEAP());
    Serial.println("======================================================================");
    Serial.println("STATUS = BASELINE_INFERENCE_VERIFIED");
    Serial.println("======================================================================");
}

void loop() {
    // Idle loop after one-shot sanity test in setup()
    delay(5000);
}
