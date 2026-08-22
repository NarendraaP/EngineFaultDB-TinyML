/*
 * Phase 5.1 — Baseline Microcontroller TinyML Firmware (TFLite Micro)
 * ====================================================================
 * Single-sample inference benchmark firmware for ESP32-S3 / RP2040 / STM32F4.
 * Integrates TFLite Micro, microsecond hardware timer instrumentation,
 * static SRAM & dynamic heap reporting, and single-sample execution loops.
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cstdint>

// TFLite Micro headers
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_error_reporter.h"
#include "tensorflow/lite/schema/schema_generated.h"

// Embedded headers
#include "include/g_student_b_model_data.h"
#include "include/g_student_a_model_data.h"
#include "include/mcu_test_vectors.h"

// Hardware specific timer definitions
#if defined(ESP_PLATFORM)
  #include "esp_timer.h"
  #include "esp_system.h"
  #define GET_MICROS() esp_timer_get_time()
  #define GET_FREE_HEAP() esp_get_free_heap_size()
#elif defined(ARDUINO)
  #include "Arduino.h"
  #define GET_MICROS() micros()
  #define GET_FREE_HEAP() 0
#else
  // Native fallback timer for host verification
  #include <chrono>
  inline int64_t GET_MICROS() {
      using namespace std::chrono;
      return duration_cast<microseconds>(steady_clock::now().time_since_epoch()).count();
  }
  inline uint32_t GET_FREE_HEAP() { return 0; }
#endif

// Tensor Arena Size (statically allocated SRAM buffer)
constexpr int kTensorArenaSize = 8 * 1024; // 8 KB SRAM
alignas(16) uint8_t tensor_arena[kTensorArenaSize];

int main() {
    printf("======================================================================\n");
    printf("Phase 5.1 — TFLite Micro Baseline MCU Firmware Benchmark\n");
    printf("======================================================================\n");

    // 1. Initialize Error Reporter
    tflite::MicroErrorReporter micro_error_reporter;
    tflite::ErrorReporter* error_reporter = &micro_error_reporter;

    // 2. Load Model FlatBuffer
    const tflite::Model* model = tflite::GetModel(g_student_b_model_data);
    if (model->version() != TFLITE_SCHEMA_VERSION) {
        TF_LITE_REPORT_ERROR(error_reporter, "Model schema version mismatch!");
        return -1;
    }

    // 3. Register required INT8 Operators
    tflite::MicroMutableOpResolver<3> resolver;
    resolver.AddFullyConnected();
    resolver.AddSoftmax();
    resolver.AddReshape();

    // 4. Instantiate MicroInterpreter
    tflite::MicroInterpreter interpreter(
        model, resolver, tensor_arena, kTensorArenaSize, error_reporter
    );

    // 5. Allocate Tensors in Tensor Arena
    TfLiteStatus allocate_status = interpreter.AllocateTensors();
    if (allocate_status != kTfLiteOk) {
        TF_LITE_REPORT_ERROR(error_reporter, "AllocateTensors() failed!");
        return -1;
    }

    TfLiteTensor* input = interpreter.input(0);
    TfLiteTensor* output = interpreter.output(0);

    printf("Model loaded successfully.\n");
    printf("  Input Dtype: %d, Quant Scale: %f, ZeroPoint: %d\n",
           input->type, input->params.scale, input->params.zero_point);
    printf("  Output Dtype: %d, Quant Scale: %f, ZeroPoint: %d\n",
           output->type, output->params.scale, output->params.zero_point);
    printf("  Tensor Arena Used: %zu / %d Bytes\n", interpreter.arena_used_bytes(), kTensorArenaSize);
    printf("  Free Heap: %u Bytes\n\n", GET_FREE_HEAP());

    // 6. Timer Overhead Calibration
    int64_t timer_t0 = GET_MICROS();
    int64_t timer_t1 = GET_MICROS();
    int64_t timer_overhead_us = timer_t1 - timer_t0;
    printf("Timer Read Overhead: %lld us\n\n", (long long)timer_overhead_us);

    // 7. Warmup Inferences (100 runs)
    for (int i = 0; i < 100; ++i) {
        memcpy(input->data.int8, TEST_SAMPLES_INT8[0], FEATURE_DIM);
        interpreter.Invoke();
    }

    // 8. Benchmark Inferences (1,000 runs single-sample)
    constexpr int kBenchmarkRuns = 1000;
    int64_t latencies[kBenchmarkRuns];

    for (int i = 0; i < kBenchmarkRuns; ++i) {
        int sample_idx = i % NUM_TEST_SAMPLES;
        memcpy(input->data.int8, TEST_SAMPLES_INT8[sample_idx], FEATURE_DIM);

        int64_t start_us = GET_MICROS();
        TfLiteStatus invoke_status = interpreter.Invoke();
        int64_t end_us = GET_MICROS();

        if (invoke_status != kTfLiteOk) {
            TF_LITE_REPORT_ERROR(error_reporter, "Invoke failed on run %d", i);
            return -1;
        }

        latencies[i] = (end_us - start_us) - timer_overhead_us;
    }

    // 9. Compute Latency Statistics
    int64_t sum_us = 0;
    int64_t min_us = latencies[0];
    int64_t max_us = latencies[0];

    for (int i = 0; i < kBenchmarkRuns; ++i) {
        sum_us += latencies[i];
        if (latencies[i] < min_us) min_us = latencies[i];
        if (latencies[i] > max_us) max_us = latencies[i];
    }

    double mean_us = (double)sum_us / kBenchmarkRuns;

    printf("======================================================================\n");
    printf("Empirical MCU Inference Latency Results (1,000 Runs):\n");
    printf("======================================================================\n");
    printf("  Mean Latency:   %.2f us\n", mean_us);
    printf("  Min Latency:    %lld us\n", (long long)min_us);
    printf("  Max Latency:    %lld us\n", (long long)max_us);
    printf("======================================================================\n");

    return 0;
}
