# Phase 5K: ESP32 TinyML Deployment Interface Specification

> **Document Status:** `STATUS = PENDING_PHYSICAL_ESP32`  
> **Target Platform:** Espressif ESP32 / ESP32-S3 (Xtensa Dual-Core 32-bit LX7 @ 240 MHz, 512 KB SRAM, 4 MB–8 MB SPI Flash)  
> **Firmware Framework:** ESP-IDF / Arduino-ESP32 / PlatformIO with TensorFlow Lite for Microcontrollers (TFLM)  
> **Dataset Source:** `EngineFaultDB_Final.csv` (14 engine operational features, 4 target fault classes)  
> **Authoritative Baseline Reference:** `results/tinyml_model_profile_verified.csv` & `models/scaler.pkl`

---

## 1. Executive Overview & Scope

This document specifies the deployment interface, tensor memory layout, quantization arithmetic, model registry, hardware timing instrumentation, UART communication protocol, and benchmark verification requirements for running quantized TinyML engine fault classification models on the **Espressif ESP32 / ESP32-S3 microcontroller family**.

```
+---------------------------------------------------------------------------------------------------+
|                                  ESP32 TinyML Diagnostic Pipeline                                 |
|                                                                                                   |
|  [Raw Sensors]               [MinMaxScaler]             [INT8 Quantizer]          [TFLite Micro]  |
|  14 Float32 Features  --->  x_norm = (x - min) * scale  --->  q_in = round(x/S)+Z  --->  [Interpreter]  |
|  (MAP, TPS, RPM, ...)       (models/scaler.pkl)         (S=0.00389, Z=-128)       (Student B / A) |
|                                                                                          |        |
|  [JSON-L UART Report] <---  [Statistics Reducer]   <--- [Microsecond Timer]        <-----+        |
|  115,200 Baud (8N1)         (Mean, P95, P99, Acc)       esp_timer_get_time()        [INT8 Output] |
+---------------------------------------------------------------------------------------------------+
```

> **Specification Notice:** All specifications, data schemas, memory footprints, and expected latencies in this document are design contracts for future physical ESP32 on-device deployment. No physical MCU executions are conducted during specification authoring. All benchmark columns and records are strictly flagged with `STATUS = PENDING_PHYSICAL_ESP32`.

---

## 2. Expected Model Format & Storage

### 2.1 FlatBuffer Storage Architecture
All deployable models are compiled as TensorFlow Lite FlatBuffer binaries (`.tflite`) and converted to 16-byte aligned C byte arrays stored in flash memory (`.rodata` segment), preventing runtime filesystem overhead.

- **Storage Alignment:** `alignas(16) const unsigned char <model_variable_name>[]`
- **Compiler Placement:** Statically linked in program Flash (`PROGMEM` / `.rodata`).
- **Generator Script:** [`convert_model_to_c_header.py`](file:///d:/WiDe/EngineFaultDB-main/phase5/benchmarks/convert_model_to_c_header.py)

### 2.2 Model Inventory & Flash Footprint

| Model Identifier | Architecture | Precision | Parameters | Flash Size (Bytes) | Flash Size (KB) | C Header Name | Variable Identifier |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `student_b_16_4_int8` | 14-16-4 MLP (KD) | Fully Quantized INT8 | 328 | 3,576 | 3.49 KB | `g_student_b_model_data.h` | `g_student_b_model_data` |
| `student_a_8_4_int8` | 14-8-4 MLP (KD) | Fully Quantized INT8 | 176 | 3,208 | 3.13 KB | `g_student_a_model_data.h` | `g_student_a_model_data` |
| `mlp_14f_int8` | 14-16-8-4 MLP (Baseline) | Fully Quantized INT8 | 412 | 3,728 | 3.64 KB | `g_mlp_14f_model_data.h` | `g_mlp_14f_model_data` |
| `mlp_12f_int8` | 12-16-8-4 MLP (Reduced) | Fully Quantized INT8 | 380 | 3,712 | 3.62 KB | `g_mlp_12f_model_data.h` | `g_mlp_12f_model_data` |

### 2.3 Required TFLM Op Resolver
The deployed inference engine registers only the exact operators required by the MLP topologies:
```cpp
#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"

// Minimum op resolver covering all EngineFaultDB MLP topologies
tflite::MicroMutableOpResolver<3> resolver;
resolver.AddFullyConnected();
resolver.AddSoftmax();
resolver.AddReshape();
```

---

## 3. Expected Input Format & Tensor Ordering

### 3.1 Input Tensor Contract
- **Tensor Shape:** Single-sample inference strictly `[1, 14]` (Batch Size = 1).
- **Inference Mode:** Single-sample on-demand / periodic diagnostic invocation (No batching on MCU).
- **Physical Datatype:** `int8_t` (signed 8-bit integer, range `[-128, 127]`).
- **Feature Count:** 14 features matching Phase 2 [`baseline_benchmark.py`](file:///d:/WiDe/EngineFaultDB-main/baseline_benchmark.py) and `ALL_FEATURES`.

### 3.2 Canonical Feature Sequence (14 Dimensions)
Microcontroller firmware buffers must map sensor inputs into the input tensor in the exact indexed order below:

| Index | Feature Name | Description | Physical Unit | Expected Raw Range (Min – Max) |
| :---: | :--- | :--- | :---: | :---: |
| `0` | `MAP` | Manifold Absolute Pressure | bar | 0.4530 – 4.5470 |
| `1` | `TPS` | Throttle Position Sensor | % | 0.3820 – 4.0480 |
| `2` | `Force` | Engine Dynamic Load / Force | N | 2.5800 – 1537.1180 |
| `3` | `Power` | Calculated Engine Brake Power | kW | 0.4650 – 33.9460 |
| `4` | `RPM` | Engine Rotational Speed | rev/min | 1066.4520 – 5013.4020 |
| `5` | `Consumption L/H` | Hourly Volumetric Fuel Rate | L/h | 1.9170 – 14.8100 |
| `6` | `Consumption L/100KM` | Distance-Specific Fuel Consumption | L/100km | 5.1870 – 20.0430 |
| `7` | `Speed` | Vehicle Longitudinal Velocity | km/h | 22.7570 – 107.5390 |
| `8` | `CO` | Carbon Monoxide Tailpipe Emission | % vol | 0.4210 – 10.1320 |
| `9` | `HC` | Unburnt Hydrocarbons | ppm | 1.7870 – 975.6570 |
| `10` | `CO2` | Carbon Dioxide Emission | % vol | 8.6490 – 15.1290 |
| `11` | `O2` | Residual Exhaust Oxygen Concentration | % vol | 0.2030 – 1.1510 |
| `12` | `Lambda` | Excess Air Ratio ($\lambda$) | dimensionless | 0.6950 – 1.1490 |
| `13` | `AFR` | Air-Fuel Ratio | :1 mass ratio | 10.2100 – 16.8930 |

---

## 4. Feature Scaling Interface

### 4.1 Normalization Mathematical Formula
All sensor inputs must be normalized to $[0.0, 1.0]$ using the Phase 2 frozen `models/scaler.pkl` parameters before INT8 quantization:

$$x_{\text{norm}, i} = (x_{\text{raw}, i} - x_{\text{min}, i}) \cdot \text{scale}_i = x_{\text{raw}, i} \cdot \text{scale}_i + \text{min\_}_i$$

where $\text{scale}_i = \frac{1}{x_{\text{max}, i} - x_{\text{min}, i}}$ and $\text{min\_}_i = -\frac{x_{\text{min}, i}}{x_{\text{max}, i} - x_{\text{min}, i}}$.

### 4.2 C Implementation Header Parameters
```c
/* Scaler parameters derived from models/scaler.pkl (Train split N=22,399) */
typedef struct {
    float scale;
    float min_val;
    float max_val;
} feature_scaler_t;

static const feature_scaler_t G_FEATURE_SCALERS[14] = {
    { 0.244260f, 0.4530f, 4.5470f },     /* 0: MAP */
    { 0.272777f, 0.3820f, 4.0480f },     /* 1: TPS */
    { 0.000652f, 2.5800f, 1537.1180f },  /* 2: Force */
    { 0.029868f, 0.4650f, 33.9460f },    /* 3: Power */
    { 0.000253f, 1066.4520f, 5013.4020f},/* 4: RPM */
    { 0.077561f, 1.9170f, 14.8100f },    /* 5: Consumption L/H */
    { 0.067313f, 5.1870f, 20.0430f },    /* 6: Consumption L/100KM */
    { 0.011795f, 22.7570f, 107.5390f },  /* 7: Speed */
    { 0.102976f, 0.4210f, 10.1320f },    /* 8: CO */
    { 0.001027f, 1.7870f, 975.6570f },   /* 9: HC */
    { 0.154321f, 8.6490f, 15.1290f },    /* 10: CO2 */
    { 1.054852f, 0.2030f, 1.1510f },     /* 11: O2 */
    { 2.202643f, 0.6950f, 1.1490f },     /* 12: Lambda */
    { 0.149633f, 10.2100f, 16.8930f }    /* 13: AFR */
};

inline float normalize_feature(float raw_value, int feature_index) {
    const feature_scaler_t* s = &G_FEATURE_SCALERS[feature_index];
    float norm = (raw_value - s->min_val) * s->scale;
    if (norm < 0.0f) norm = 0.0f;
    if (norm > 1.0f) norm = 1.0f;
    return norm;
}
```

---

## 5. Quantization Parameters (INT8 Math)

### 5.1 Authoritative TFLite Quantization Parameters
Derived from the quantized FlatBuffers in `models/tinyml/`:

- **Input Tensor (TfLiteType: `kTfLiteInt8`):**
  - Scale ($S_{\text{in}}$): `0.0038928112480789423f` ($\approx 1 / 256.88$)
  - Zero Point ($Z_{\text{in}}$): `-128`
  - Quantization Formula:
    $$q_{\text{in}} = \text{clamp}\left(\left\lfloor \frac{x_{\text{norm}}}{S_{\text{in}}} + 0.5 \right\rfloor + Z_{\text{in}}, -128, 127\right)$$

- **Output Tensor (TfLiteType: `kTfLiteInt8`):**
  - Scale ($S_{\text{out}}$): `0.00390625f` ($= 1 / 256$)
  - Zero Point ($Z_{\text{out}}$): `-128`
  - Dequantization Formula (Class Probabilities):
    $$p_k = (q_{\text{out}, k} - Z_{\text{out}}) \cdot S_{\text{out}} = (q_{\text{out}, k} + 128) \cdot 0.00390625$$

### 5.2 Target Fault Class Mapping

| Class ID | Enumeration | Diagnostic Description | Corrective Action / Severity |
| :---: | :--- | :--- | :--- |
| `0` | `FAULT_NONE` | Normal Engine Operation | Baseline nominal running |
| `1` | `FAULT_RICH_MIXTURE` | Rich Air-Fuel Mixture (Excess Fuel) | Oxygen sensor / injector calibration check |
| `2` | `FAULT_LEAN_MIXTURE` | Lean Air-Fuel Mixture (Excess Air) | Vacuum leak / fuel pressure inspection |
| `3` | `FAULT_MISFIRE` | Cylinder Combustion Misfire | Ignition coil / spark plug urgent service |

---

## 6. Model Registry C Interface

```c
#ifndef TINYML_MODEL_REGISTRY_H_
#define TINYML_MODEL_REGISTRY_H_

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

typedef enum {
    MODEL_ID_STUDENT_B_16_4_INT8 = 0,
    MODEL_ID_STUDENT_A_8_4_INT8  = 1,
    MODEL_ID_MLP_14F_INT8        = 2,
    MODEL_ID_MLP_12F_INT8        = 3,
    MODEL_ID_COUNT               = 4
} tinyml_model_id_t;

typedef struct {
    tinyml_model_id_t id;
    const char* name;
    const unsigned char* flatbuffer_data;
    unsigned int flatbuffer_size_bytes;
    uint8_t num_features;
    uint8_t num_classes;
    size_t tensor_arena_required_bytes;
    float input_scale;
    int32_t input_zero_point;
    float output_scale;
    int32_t output_zero_point;
    uint32_t theoretical_macs;
    uint32_t active_macs;
    float verified_accuracy;
    float verified_macro_f1;
    const char* pareto_status;
    const char* deployment_status;
} tinyml_model_metadata_t;

/* Registry API Functions */
void tinyml_registry_init(void);
const tinyml_model_metadata_t* tinyml_get_model_metadata(tinyml_model_id_t model_id);
bool tinyml_select_model(tinyml_model_id_t model_id);
tinyml_model_id_t tinyml_get_active_model_id(void);

#ifdef __cplusplus
}
#endif

#endif // TINYML_MODEL_REGISTRY_H_
```

---

## 7. Hardware Timer & Measurement Protocol

### 7.1 ESP32 Microsecond Timer API
The ESP32 architecture provides a 64-bit hardware timer peripheral accessible via `esp_timer_get_time()` with $1\,\mu\text{s}$ resolution.

```c
#include "esp_timer.h"

// Microsecond timing primitive
#define GET_MICROS() esp_timer_get_time()
```

### 7.2 Timer Overhead Calibration
Prior to running inference loops, the measurement harness must calculate the average register read overhead:

```c
static int64_t calibrate_timer_overhead(void) {
    int64_t sum = 0;
    const int CALIB_ITERS = 1000;
    for (int i = 0; i < CALIB_ITERS; ++i) {
        int64_t t0 = esp_timer_get_time();
        int64_t t1 = esp_timer_get_time();
        sum += (t1 - t0);
    }
    return sum / CALIB_ITERS; // Typically 0 to 1 us
}
```

---

## 8. Memory Interface (Tensor Arena & SRAM Management)

### 8.1 Static SRAM Tensor Arena Allocation
To prevent heap fragmentation and non-deterministic dynamic allocation during vehicle operations, the TFLM Tensor Arena must be statically allocated in the `.bss` section:

```cpp
// 8 KB static tensor arena in internal SRAM
constexpr size_t kTensorArenaSize = 8192;
alignas(16) static uint8_t g_tensor_arena[kTensorArenaSize];
```

### 8.2 Memory Sizing per Model Architecture

| Model Name | Parameters | Arena Used (Bytes) | Recommended Arena Buffer | Free Internal SRAM (Typical ESP32) | Dynamic Allocations in Steady-State |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `student_a_8_4_int8` | 176 | 1,840 B | 4,096 B (4 KB) | > 300 KB | 0 Bytes |
| `student_b_16_4_int8` | 328 | 2,120 B | 4,096 B (4 KB) | > 300 KB | 0 Bytes |
| `mlp_14f_int8` | 412 | 2,360 B | 8,192 B (8 KB) | > 300 KB | 0 Bytes |
| `mlp_12f_int8` | 380 | 2,320 B | 8,192 B (8 KB) | > 300 KB | 0 Bytes |

---

## 9. Serial Logging Format (UART @ 115200 Baud)

Benchmark logs and runtime telemetry are transmitted over the primary UART channel (`115200 8N1`) formatted as single-line JSON objects (`ndjson`).

### 9.1 Per-Sample Inference Event Schema
```json
{
  "type": "INFERENCE_SAMPLE",
  "sample_id": 142,
  "model": "student_b_16_4_int8",
  "pred_class": 3,
  "confidence": 0.984375,
  "latency_us": 1.25,
  "status": "PENDING_PHYSICAL_ESP32"
}
```

### 9.2 Benchmark Summary Packet Schema
```json
{
  "type": "BENCHMARK_SUMMARY",
  "timestamp_ms": 15420,
  "board": "ESP32-S3-DevKitC-1",
  "clock_mhz": 240,
  "model": "student_b_16_4_int8",
  "precision": "FULL_INT8",
  "warmup_iters": 100,
  "measure_iters": 1000,
  "mean_latency_us": 0.00,
  "median_latency_us": 0.00,
  "p95_latency_us": 0.00,
  "p99_latency_us": 0.00,
  "min_latency_us": 0.00,
  "max_latency_us": 0.00,
  "tensor_arena_allocated_bytes": 8192,
  "tensor_arena_used_bytes": 2120,
  "free_heap_bytes": 321456,
  "test_accuracy": 0.0000,
  "test_macro_f1": 0.0000,
  "status": "PENDING_PHYSICAL_ESP32"
}
```

---

## 10. Benchmark Execution Protocol

When physical hardware testing commences, test runners must strictly adhere to the following 5-stage benchmark protocol:

1. **System Initialization:**
   - Initialize UART at 115,200 baud.
   - Configure CPU core frequency to 240 MHz.
   - Calibrate hardware timer read overhead.
2. **Model Instantiation:**
   - Instantiate `tflite::MicroInterpreter` with `g_tensor_arena`.
   - Call `interpreter.AllocateTensors()` and verify `kTfLiteOk`.
   - Log `arena_used_bytes()` and available free heap.
3. **Warmup Phase ($N = 100$ Iterations):**
   - Execute 100 un-timed single-sample inferences on representative test vectors to warm instruction caches and branch predictor tables.
4. **Measurement Phase ($M = 1000$ Iterations):**
   - Sequentially iterate through test vectors from `mcu_test_vectors.h`.
   - Record start timestamp $t_{\text{start}} = \text{GET\_MICROS}()$.
   - Invoke `interpreter.Invoke()`.
   - Record end timestamp $t_{\text{end}} = \text{GET\_MICROS}()$.
   - Store latency $L_i = (t_{\text{end}} - t_{\text{start}}) - t_{\text{overhead}}$.
   - Record predicted class $\arg\max(q_{\text{out}, k})$.
5. **Statistical Reduction & Reporting:**
   - Sort latencies to compute Mean, Median ($P_{50}$), $P_{95}$, $P_{99}$, Min, Max.
   - Compare predictions with reference labels to calculate Empirical On-Device Accuracy and Macro F1.
   - Emit the UART JSON summary packet and write structured CSV row.

---

## 11. Expected Physical MCU Result CSV Schema

MCU benchmark results must be recorded to `phase5/measurements/mcu_empirical_benchmarks.csv` matching the schema below:

### 11.1 Column Definitions
1. `model` (string): Model identifier matching registry (e.g., `student_b_16_4_int8`).
2. `board` (string): Physical MCU target board (e.g., `ESP32-S3-DevKitC-1`).
3. `clock_mhz` (integer): CPU operational clock frequency in MHz (e.g., `240`).
4. `features` (integer): Input feature dimension (`14` or `12`).
5. `precision` (string): Tensor arithmetic format (`FULL_INT8`).
6. `parameters` (integer): Total trainable weights and biases.
7. `flash_bytes` (integer): Model FlatBuffer byte size stored in Flash.
8. `tensor_arena_bytes` (integer): Allocated static tensor arena buffer size.
9. `arena_used_bytes` (integer): Exact tensor arena bytes utilized by TFLM runtime.
10. `free_heap_bytes` (integer): Available dynamic heap space during execution.
11. `warmup_iters` (integer): Number of warmup iterations completed (`100`).
12. `measure_iters` (integer): Number of timed benchmark iterations (`1000`).
13. `mcu_mean_latency_us` (float): Empirical mean single-sample inference time in $\mu\text{s}$.
14. `mcu_median_latency_us` (float): Empirical median single-sample inference time in $\mu\text{s}$.
15. `mcu_p95_latency_us` (float): Empirical 95th percentile latency in $\mu\text{s}$.
16. `mcu_p99_latency_us` (float): Empirical 99th percentile latency in $\mu\text{s}$.
17. `mcu_min_latency_us` (float): Minimum recorded latency in $\mu\text{s}$.
18. `mcu_max_latency_us` (float): Maximum recorded latency in $\mu\text{s}$.
19. `mcu_test_accuracy` (float): Empirical classification accuracy measured on MCU test vectors.
20. `mcu_macro_f1` (float): Empirical unweighted macro-averaged F1 score.
21. `status` (string): Verification status tag (`STATUS = PENDING_PHYSICAL_ESP32`).

### 11.2 Initial Expected Records (Pre-Execution Template)
```csv
model,board,clock_mhz,features,precision,parameters,flash_bytes,tensor_arena_bytes,arena_used_bytes,free_heap_bytes,warmup_iters,measure_iters,mcu_mean_latency_us,mcu_median_latency_us,mcu_p95_latency_us,mcu_p99_latency_us,mcu_min_latency_us,mcu_max_latency_us,mcu_test_accuracy,mcu_macro_f1,status
student_b_16_4_int8,ESP32-S3-DevKitC-1,240,14,FULL_INT8,328,3576,8192,2120,321456,100,1000,0.00,0.00,0.00,0.00,0.00,0.00,0.0000,0.0000,PENDING_PHYSICAL_ESP32
student_a_8_4_int8,ESP32-S3-DevKitC-1,240,14,FULL_INT8,176,3208,8192,1840,321456,100,1000,0.00,0.00,0.00,0.00,0.00,0.00,0.0000,0.0000,PENDING_PHYSICAL_ESP32
mlp_14f_int8,ESP32-S3-DevKitC-1,240,14,FULL_INT8,412,3728,8192,2360,321456,100,1000,0.00,0.00,0.00,0.00,0.00,0.00,0.0000,0.0000,PENDING_PHYSICAL_ESP32
mlp_12f_int8,ESP32-S3-DevKitC-1,240,12,FULL_INT8,380,3712,8192,2320,321456,100,1000,0.00,0.00,0.00,0.00,0.00,0.00,0.0000,0.0000,PENDING_PHYSICAL_ESP32
```

---

## 12. Verification & Compliance Checklist

- [x] Canonical 14-feature input ordering matches Phase 2 `baseline_benchmark.py`.
- [x] Feature scaling values match `models/scaler.pkl`.
- [x] Quantization scale and zero-point parameters match TFLite FlatBuffer metadata.
- [x] Single-sample execution strictly enforced (`shape = (1, 14)`).
- [x] No ground-truth labels accessed in online MCU inference paths.
- [x] Hardware timer using microsecond precision (`esp_timer_get_time()`).
- [x] Static SRAM allocation specified without dynamic heap calls in inference loop.
- [x] All specifications and output schemas marked `STATUS = PENDING_PHYSICAL_ESP32`.
