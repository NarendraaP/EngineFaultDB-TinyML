# Paper 5: On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers

## Overview
This repository contains the complete reproducible manuscript source, physical firmware, model byte headers, and empirical benchmark datasets for **Paper 5** (*IEEE Embedded Systems Letters / ACM TECS*).

---

## 1. Physical Hardware Target Specification
- **Microcontroller:** Espressif ESP32-D0WD-V3 (Revision v3.1)
- **Core Architecture:** Dual-Core 32-bit Xtensa LX6 @ 240 MHz (Crystal: 40 MHz)
- **On-Chip SRAM:** 320 KB Internal SRAM (0 PSRAM)
- **Non-Volatile Flash:** 4 MB Quad-SPI Flash (80 MHz QIO mode @ 3.3V)
- **USB-UART Bridge:** WCH CH9102 (VID: `0x1A86`, PID: `0x55D4`) on `COM7` @ 115,200 baud

---

## 2. Evaluated `FULL_INT8` TinyML Models
All models evaluated in this research are verified disk-serialized TensorFlow Lite FlatBuffers with 0 float32 tensors:
1. `student_a_8_4_int8` (14 features, 176 params, 3,208 Bytes) — Distilled compact student
2. `student_b_16_4_int8` (14 features, 328 params, 3,576 Bytes) — Distilled balanced student
3. `mlp_12f_int8` (12 features, 380 params, 3,712 Bytes) — Feature-pruned baseline
4. `mlp_14f_int8` (14 features, 412 params, 3,728 Bytes) — Full baseline model

---

## 3. Benchmarking Protocol & Methodology
- **Execution Scope:** Pure `interpreter->Invoke()` isolated single-sample kernel inference (excluding preprocessing and UART).
- **Measurement Sample Size:** $N=24,000$ measured inferences (4 models $\times$ 3 rounds $\times$ 2,000 iterations/round).
- **Warmup Protocol:** 100 un-timed inferences preceding every round ($1,200$ warmup inferences total = $25,200$ executions).
- **Hardware Monotonic Timer:** `esp_timer_get_time()` with microsecond-level resolution.
- **Timing Buffer:** In-RAM latency accumulation (`uint32_t latencies[2000]`) with post-hoc on-chip sorting to eliminate UART I/O interference.

---

## 4. Key Empirical Findings
- **Physical Latencies:**
  - `student_a_8_4_int8`: Mean = **64.55 $\mu$s**, P95 = 69.00 $\mu$s, P99 = 76.00 $\mu$s, Max = 77 $\mu$s
  - `student_b_16_4_int8`: Mean = **72.96 $\mu$s**, P95 = 83.00 $\mu$s, P99 = 83.00 $\mu$s, Max = 84 $\mu$s
  - `mlp_12f_int8`: Mean = **76.77 $\mu$s**, P95 = 83.00 $\mu$s, P99 = 90.00 $\mu$s, Max = 90 $\mu$s
  - `mlp_14f_int8`: Mean = **89.90 $\mu$s**, P95 = 95.00 $\mu$s, P99 = 101.00 $\mu$s, Max = 102 $\mu$s
- **Distillation Speedup:** $28.20\%$ physical latency reduction (`student_a` vs `mlp_14f`).
- **Host-to-MCU Slowdown:** $62.87\times\text{--}76.77\times$ slowdown from x86_64 host simulation to 240 MHz silicon.
- **Memory Footprint:** 330 KB Flash (25.19% partition), 61.9 KB Static SRAM, **916 Bytes allocator-committed arena usage** (within 8 KB static arena, 88.82% headroom), **0 Bytes dynamic heap allocated** during inference (0 Bytes memory leak across 25,200 runs).

---

## 5. Reproduction & Build Instructions
1. **Compile LaTeX Manuscript with Tectonic:**
   ```bash
   tectonic papers/Paper5_ESP32_Deployment/submission/paper.tex
   ```
2. **Build and Flash ESP32 Firmware:**
   ```bash
   cd phase5/firmware
   pio run -t upload --environment esp32_devkit
   pio device monitor --port COM7 --baud 115200
   ```
3. **Inspect Output Datasets:**
   - Summary CSV: `phase5/measurements/esp32_model_benchmark.csv`
   - Complete JSON: `phase5/measurements/esp32_full_benchmark.json`
   - Raw Serial Log: `phase5/measurements/esp32_raw_serial_benchmark.txt`
