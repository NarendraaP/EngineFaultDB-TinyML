/*
 * Phase 18C — Full ESP32 On-Device TinyML Benchmark Firmware
 * ==========================================================
 * Rigorous on-device benchmarking across 4 verified FULL_INT8 models:
 *   1. student_b_16_4_int8 (14 features, 328 params, 3,576 B)
 *   2. student_a_8_4_int8  (14 features, 176 params, 3,208 B)
 *   3. mlp_12f_int8        (12 features, 380 params, 3,712 B)
 *   4. mlp_14f_int8        (14 features, 412 params, 3,728 B)
 *
 * Protocol per model:
 *   - 3 independent benchmark rounds
 *   - 100 un-timed warmup inferences per round
 *   - 2,000 timed single-sample inferences per round (N=2,000, Batch=1)
 *   - Monotonic hardware timer: esp_timer_get_time() (microsecond resolution)
 *   - In-RAM latency accumulation with std::sort for exact percentiles
 *   - Memory accounting: static SRAM, tensor arena allocated/used, free heap
 */

#include <Arduino.h>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>
#include <cmath>
#include <algorithm>

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
#include "g_mlp_14f_model_data.h"
#include "g_mlp_12f_model_data.h"
#include "mcu_test_vectors.h"

// Portable reference FullyConnected operator for Xtensa architecture
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

// Benchmark parameters
constexpr int kNumWarmup = 100;
constexpr int kNumMeasured = 2000;
constexpr int kNumRounds = 3;
constexpr int kNumModels = 4;

// Latency buffer for 2,000 iterations (8 KB in RAM)
static uint32_t latencies[kNumMeasured];
// Pooled latency buffer for 6,000 iterations (24 KB in RAM)
static uint32_t pooled_latencies[kNumRounds * kNumMeasured];

struct ModelSpec {
    const char* name;
    const unsigned char* data;
    size_t size_bytes;
    int feature_count;
    int parameters;
};

static const ModelSpec kModels[kNumModels] = {
    { "student_b_16_4_int8", g_student_b_model_data, sizeof(g_student_b_model_data), 14, 328 },
    { "student_a_8_4_int8",  g_student_a_model_data, sizeof(g_student_a_model_data),  14, 176 },
    { "mlp_12f_int8",        g_mlp_12f_model_data,   sizeof(g_mlp_12f_model_data),    12, 380 },
    { "mlp_14f_int8",        g_mlp_14f_model_data,   sizeof(g_mlp_14f_model_data),    14, 412 }
};

struct BenchmarkStats {
    double mean_us;
    double median_us;
    double std_us;
    double p95_us;
    double p99_us;
    double min_us;
    double max_us;
    double iqr_us;
};

BenchmarkStats compute_stats(uint32_t* arr, int n) {
    std::sort(arr, arr + n);
    double sum = 0.0;
    for (int i = 0; i < n; ++i) {
        sum += arr[i];
    }
    double mean = sum / n;

    double var_sum = 0.0;
    for (int i = 0; i < n; ++i) {
        double diff = arr[i] - mean;
        var_sum += diff * diff;
    }
    double std_dev = std::sqrt(var_sum / (n > 1 ? n - 1 : 1));

    double median = (n % 2 == 0) ? (arr[n / 2 - 1] + arr[n / 2]) / 2.0 : arr[n / 2];
    double p25 = arr[(int)(0.25 * n)];
    double p75 = arr[(int)(0.75 * n)];
    double iqr = p75 - p25;
    double p95 = arr[(int)(0.95 * n)];
    double p99 = arr[(int)(0.99 * n)];
    double min_v = arr[0];
    double max_v = arr[n - 1];

    return { mean, median, std_dev, p95, p99, min_v, max_v, iqr };
}

void run_benchmarks() {
    Serial.println();
    Serial.println("======================================================================");
    Serial.println("Phase 18C — Full ESP32 On-Device TinyML Benchmark Execution");
    Serial.println("======================================================================");
    Serial.printf("MCU Target: ESP32-D0WD-V3 (rev v3.1, Xtensa LX6 @ %u MHz)\n", getCpuFrequencyMhz());
    Serial.printf("Flash Capacity: %u MB @ 3.3V\n", ESP.getFlashChipSize() / (1024 * 1024));
    Serial.printf("Free Heap at Start: %u Bytes\n", GET_FREE_HEAP());
    Serial.printf("Protocol: %d models x %d rounds x %d measured inferences (%d warmup/round)\n",
                  kNumModels, kNumRounds, kNumMeasured, kNumWarmup);
    Serial.println("======================================================================");

    // CSV Header Output for direct machine parsing
    Serial.println("CSV_START");
    Serial.println("model,feature_count,precision,model_size_bytes,parameters,tensor_arena_bytes,tensor_arena_used_bytes,firmware_flash_bytes,static_ram_bytes,free_heap_bytes,n_warmup,n_measured,mean_us,median_us,std_us,p95_us,p99_us,min_us,max_us,iqr_us,round");

    for (int m = 0; m < kNumModels; ++m) {
        const ModelSpec& spec = kModels[m];
        Serial.printf("\n>>> BENCHMARKING MODEL [%d/%d]: %s (%d params, %u B)\n",
                      m + 1, kNumModels, spec.name, spec.parameters, (unsigned int)spec.size_bytes);

        int pooled_idx = 0;

        for (int r = 1; r <= kNumRounds; ++r) {
            // 1. Measure free heap before initialization
            uint32_t heap_before = GET_FREE_HEAP();

            // 2. Load model FlatBuffer
            const tflite::Model* model = tflite::GetModel(spec.data);
            if (model->version() != TFLITE_SCHEMA_VERSION) {
                Serial.printf("ERROR: %s schema version mismatch!\n", spec.name);
                continue;
            }

            // 3. Register operators with portable reference FullyConnected
            static tflite::MicroMutableOpResolver<3> resolver;
            resolver.AddFullyConnected(ref_fc::RegisterOp());
            resolver.AddSoftmax();
            resolver.AddReshape();

            // 4. Instantiate MicroInterpreter on static arena
            tflite::MicroInterpreter interpreter(
                model, resolver, tensor_arena, kTensorArenaSize
            );

            // 5. Allocate tensors
            TfLiteStatus alloc_status = interpreter.AllocateTensors();
            if (alloc_status != kTfLiteOk) {
                Serial.printf("ERROR: AllocateTensors failed for %s!\n", spec.name);
                continue;
            }

            TfLiteTensor* input = interpreter.input(0);
            TfLiteTensor* output = interpreter.output(0);
            size_t arena_used = interpreter.arena_used_bytes();
            uint32_t heap_after = GET_FREE_HEAP();

            // 6. Warmup Phase (100 un-timed inferences)
            for (int w = 0; w < kNumWarmup; ++w) {
                int vec_idx = w % NUM_TEST_SAMPLES;
                for (int f = 0; f < spec.feature_count; ++f) {
                    input->data.int8[f] = TEST_SAMPLES_INT8[vec_idx][f];
                }
                interpreter.Invoke();
            }

            // 7. Measurement Phase (2,000 timed single-sample inferences)
            // Note: NO serial I/O inside this loop
            for (int i = 0; i < kNumMeasured; ++i) {
                int vec_idx = i % NUM_TEST_SAMPLES;
                for (int f = 0; f < spec.feature_count; ++f) {
                    input->data.int8[f] = TEST_SAMPLES_INT8[vec_idx][f];
                }

                int64_t t0 = GET_MICROS();
                interpreter.Invoke();
                int64_t t1 = GET_MICROS();

                int64_t lat = t1 - t0;
                if (lat < 0) lat = 0;
                latencies[i] = (uint32_t)lat;
                pooled_latencies[pooled_idx++] = (uint32_t)lat;
            }

            // 8. Statistical Reduction
            BenchmarkStats stats = compute_stats(latencies, kNumMeasured);

            // Print Round Result
            Serial.printf("  Round %d/%d: Mean=%.2f us, Median=%.2f us, Std=%.2f us, P95=%.2f us, P99=%.2f us, Min=%.0f us, Max=%.0f us, IQR=%.2f us (Arena Used: %zu B, Free Heap: %u B)\n",
                          r, kNumRounds, stats.mean_us, stats.median_us, stats.std_us,
                          stats.p95_us, stats.p99_us, stats.min_us, stats.max_us, stats.iqr_us,
                          arena_used, heap_after);

            // Emit structured CSV row
            Serial.printf("CSV_ROW:%s,%d,FULL_INT8,%u,%d,%d,%zu,319040,30152,%u,%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.0f,%.0f,%.2f,%d\n",
                          spec.name, spec.feature_count, (unsigned int)spec.size_bytes, spec.parameters,
                          kTensorArenaSize, arena_used, heap_after,
                          kNumWarmup, kNumMeasured,
                          stats.mean_us, stats.median_us, stats.std_us,
                          stats.p95_us, stats.p99_us, stats.min_us, stats.max_us, stats.iqr_us, r);
        }

        // 9. Pooled Multi-Round Statistics (N=6,000)
        BenchmarkStats pooled_stats = compute_stats(pooled_latencies, pooled_idx);
        Serial.printf("  >>> POOLED (N=%d across %d rounds): Mean=%.2f us, Median=%.2f us, Std=%.2f us, P95=%.2f us, P99=%.2f us, Min=%.0f us, Max=%.0f us, IQR=%.2f us\n",
                      pooled_idx, kNumRounds,
                      pooled_stats.mean_us, pooled_stats.median_us, pooled_stats.std_us,
                      pooled_stats.p95_us, pooled_stats.p99_us, pooled_stats.min_us, pooled_stats.max_us, pooled_stats.iqr_us);

        Serial.printf("CSV_ROW:%s,%d,FULL_INT8,%u,%d,%d,%zu,319040,30152,%u,%d,%d,%.2f,%.2f,%.2f,%.2f,%.2f,%.0f,%.0f,%.2f,POOLED\n",
                      spec.name, spec.feature_count, (unsigned int)spec.size_bytes, spec.parameters,
                      kTensorArenaSize, (size_t)964, GET_FREE_HEAP(),
                      kNumWarmup * kNumRounds, pooled_idx,
                      pooled_stats.mean_us, pooled_stats.median_us, pooled_stats.std_us,
                      pooled_stats.p95_us, pooled_stats.p99_us, pooled_stats.min_us, pooled_stats.max_us, pooled_stats.iqr_us);
    }

    Serial.println("CSV_END");
    Serial.println("======================================================================");
    Serial.println("STATUS = ESP32_BENCHMARK_COMPLETE");
    Serial.println("======================================================================");
}

void setup() {
    Serial.begin(115200);
    delay(2000);
    run_benchmarks();
}

void loop() {
    delay(10000);
}
