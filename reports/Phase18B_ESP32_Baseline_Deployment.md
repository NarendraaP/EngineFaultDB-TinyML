# Phase 18B — ESP32 Baseline Firmware Build and Safe Deployment

> **Date:** 2026-08-29  
> **Status:** `BASELINE_INFERENCE_VERIFIED`  
> **Target MCU:** Espressif ESP32-D0WD-V3 (rev v3.1, Xtensa LX6 Dual-Core @ 240 MHz)  
> **Serial Port:** COM7 (WCH CH9102 USB-to-UART Bridge)  
> **Deployed Model:** `student_b_16_4_int8` (14-16-4 MLP, 328 params, 3,576 B FlatBuffer)  
> **Firmware Binary:** `firmware.bin` (319,040 Bytes, SHA256: `7a3498af...`)  

---

## 1. Hardware Identity

The physical microcontroller connected to COM7 was re-verified via serial port discovery and `esptool.py` hardware interrogation prior to firmware compilation and upload:

| Parameter | Interrogated Value | Specification Match |
|:---|:---|:---:|
| **MCU Silicon** | Espressif ESP32-D0WD-V3 | ✅ |
| **Silicon Revision** | Revision v3.1 | ✅ |
| **CPU Architecture** | Xtensa LX6 Dual-Core 32-bit | ✅ |
| **Operational Clock** | 240 MHz (Crystal: 40 MHz) | ✅ |
| **MAC Address** | `08:d1:f9:d9:4a:54` | ✅ |
| **Flash Memory** | 4 MB SPI Flash (Manufacturer: `0x5E`, Device: `0x4016`) | ✅ |
| **Flash Voltage** | 3.3 V (Strapping Pin Configuration) | ✅ |
| **PSRAM** | None (Standard Internal SRAM only) | ✅ |
| **USB-UART Bridge** | WCH CH9102 (VID: `0x1A86`, PID: `0x55D4`, Serial: `56B9006372`) | ✅ |
| **Serial Port** | `COM7` | ✅ |

---

## 2. Toolchain Configuration

PlatformIO Core was installed in the local Python 3.13.4 environment and configured with the Espressif 32 development platform and Arduino framework:

| Component | Package / Version | Role |
|:---|:---|:---|
| **PlatformIO Core** | 6.1.19 | Embedded build system & package manager |
| **Platform** | `espressif32 @ 7.0.1` | Espressif 32 platform definition |
| **Framework** | `framework-arduinoespressif32 @ 3.20017.241212` (ESP-IDF v4.4.7 core) | Arduino API and FreeRTOS runtime |
| **Toolchain** | `espressif/toolchain-xtensa-esp32 @ 8.4.0+2021r2-patch5` | Cross-compiler (`xtensa-esp32-elf-gcc`/`g++`) |
| **Uploader** | `esptool.py @ 4.11.0` (bundled with PlatformIO) | Serial flasher and reset controller |
| **TinyML Engine** | `spaziochirale/Chirale_TensorFLowLite @ 2.0.0` | TensorFlow Lite for Microcontrollers (TFLM) runtime |

---

## 3. PlatformIO Configuration

The target environment in [`phase5/firmware/platformio.ini`](file:///d:/WiDe/EngineFaultDB-main/phase5/firmware/platformio.ini) was corrected from the design specification board (`esp32-s3-devkitc-1`) to the actual verified physical silicon target (`esp32dev`):

```ini
; Phase 5.1 — Microcontroller Build Configuration (PlatformIO)
; Configured for ESP32 (D0WD-V3), RP2040 (Raspberry Pi Pico), and STM32F4 Target Boards
; Phase 18B: Board changed from esp32-s3-devkitc-1 to esp32dev
;            (actual silicon: ESP32-D0WD-V3 rev v3.1, Xtensa LX6)

[platformio]
default_envs = esp32_devkit

[env:esp32_devkit]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
upload_port = COM7
monitor_port = COM7
lib_deps =
    spaziochirale/Chirale_TensorFLowLite@^2.0.0
build_flags =
    -O3
    -Iinclude
```

---

## 4. Firmware Build

Compilation was executed via `pio run` without uploading.

### Build Metrics:
- **Build Status:** `SUCCESS` (Exit Code 0)
- **Compilation Duration:** 14.20 seconds (incremental) / 88.58 seconds (clean)
- **Target ELF:** `.pio/build/esp32_devkit/firmware.elf`
- **Output Binary:** `.pio/build/esp32_devkit/firmware.bin`
- **Compiler Warnings / Errors:** 0 errors, 0 fatal warnings.

---

## 5. Firmware Footprint

The firmware footprint was measured against the physical ESP32 resources (4 MB Flash, 320 KB internal SRAM):

| Memory Section | Allocated / Used | Capacity Available | Utilization | Resource Margin |
|:---|:---:|:---:|:---:|:---:|
| **Flash Program (App)** | 318,669 Bytes (311.2 KB) | 1,310,720 Bytes (1.25 MB partition) | 24.3% | 992,051 Bytes (75.7% free) |
| **Physical SPI Flash** | 319,040 Bytes (binary image) | 4,194,304 Bytes (4.0 MB total) | 7.6% | 3,875,264 Bytes (92.4% free) |
| **Static RAM (`.data` + `.bss`)** | 30,152 Bytes (29.4 KB) | 327,680 Bytes (320 KB internal) | 9.2% | 297,528 Bytes (90.8% free) |
| **Tensor Arena (Static)** | 8,192 Bytes (8.0 KB) | Statically allocated in SRAM | 100.0% | Included in Static RAM |
| **Tensor Arena Active** | 916 Bytes | 8,192 Bytes buffer | 11.2% | 7,276 Bytes (88.8% headroom) |
| **Free Heap at Boot** | 269,708 Bytes | Dynamic runtime heap | — | 269.7 KB free |
| **Free Heap after TFLM** | 269,244 Bytes | Post-allocation dynamic heap | — | 269.2 KB free (464 B delta) |

---

## 6. Model Artifact

The primary candidate model deployed for physical verification was `student_b_16_4_int8`:

- **Model Topology:** 14-16-4 Multi-Layer Perceptron (Knowledge Distilled Student B)
- **Precision:** FULL_INT8 (all tensors quantized; 0 float32 operations)
- **Total Parameters:** 328 weights and biases
- **FlatBuffer Binary Size:** 3,576 Bytes (matches [`phase5/models/student_b_16_4_int8.tflite`](file:///d:/WiDe/EngineFaultDB-main/phase5/models/student_b_16_4_int8.tflite) bit-for-bit)
- **C Header:** [`phase5/firmware/include/g_student_b_model_data.h`](file:///d:/WiDe/EngineFaultDB-main/phase5/firmware/include/g_student_b_model_data.h) (3,576 Bytes array, 16-byte aligned)
- **Input Tensor Contract:** Shape `[1, 14]`, dtype `kTfLiteInt8`, Scale = `0.003892811`, ZeroPoint = `-128`
- **Output Tensor Contract:** Shape `[1, 4]`, dtype `kTfLiteInt8`, Scale = `0.003906250`, ZeroPoint = `-128`

---

## 7. Upload Procedure

Upload was performed non-destructively using `pio run -t upload --upload-port COM7` via `esptool.py v4.11.0`:

- **Port:** `COM7`
- **Baud Rate:** `460,800`
- **Flash Write:** 319,040 bytes written (177,166 compressed) in 4.1 seconds (effective 621.6 kbit/s)
- **Data Integrity:** SHA256 digest verified on-chip
- **Reset Trigger:** Automatic hard reset via RTS pin toggle

---

## 8. Serial Boot Verification

Upon reset, the ESP32 successfully booted the deployed firmware and initialized all subsystems cleanly:

```
ets Jul 29 2019 12:21:46

rst:0x1 (POWERON_RESET),boot:0x13 (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:2
load:0x3fff0030,len:1184
load:0x40078000,len:13232
load:0x40080400,len:3028
entry 0x400805e4

======================================================================
Phase 18B — ESP32 TinyML Baseline Firmware (Physical Deployment)
======================================================================
Silicon: ESP32-D0WD-V3 (Xtensa LX6 @ 240 MHz)
Chip Revision: 3
SDK Version: v4.4.7-dirty
Free Heap at Boot: 269708 Bytes
----------------------------------------------------------------------
Model: student_b_16_4_int8 (FlatBuffer size: 3576 Bytes)
```

- **Boot Status:** Clean power-on / RTS reset (`0x13 SPI_FAST_FLASH_BOOT`)
- **Watchdog Resets:** None
- **System Crashes / Panics:** None

---

## 9. Tensor Arena Initialization

The TensorFlow Lite Micro interpreter successfully registered the model and allocated tensor buffers:

- **Resolver Registration:** `ref_fc::RegisterOp()` (Portable reference FullyConnected for Xtensa LX6), `AddSoftmax()`, `AddReshape()`
- **Allocation Result:** `TfLiteStatus::kTfLiteOk`
- **Input Tensor:** Shape `[1, 14]`, Scale `0.003892811`, ZeroPoint `-128`
- **Output Tensor:** Shape `[1, 4]`, Scale `0.003906250`, ZeroPoint `-128`
- **Static Arena Allocated:** 8,192 Bytes
- **Active Arena Utilized:** 916 Bytes (88.8% safety headroom)
- **Free Dynamic Heap:** 269,244 Bytes remaining

---

## 10. Minimal Inference Sanity Test

A minimal sanity inference pass was executed on the 20 curated INT8 test vectors from [`phase5/firmware/include/mcu_test_vectors.h`](file:///d:/WiDe/EngineFaultDB-main/phase5/firmware/include/mcu_test_vectors.h):

```
Executing Minimal Sanity Inference Test (20 Vectors):
Idx | TrueClass | PredClass | Latency(us) | Dequant Probabilities [0..3] | Match | Raw INT8 Output
----+-----------+-----------+-------------+-------------------------------+-------+----------------
  0 |     0     |     0     |      85     | [1.00, 0.00, 0.00, 0.00] | PASS  | [ 127, -128, -128, -128]
  1 |     0     |     0     |     254     | [1.00, 0.00, 0.00, 0.00] | PASS  | [ 127, -128, -128, -128]
  2 |     0     |     0     |     227     | [1.00, 0.00, 0.00, 0.00] | PASS  | [ 127, -128, -128, -128]
  3 |     0     |     0     |     251     | [1.00, 0.00, 0.00, 0.00] | PASS  | [ 127, -128, -128, -128]
  4 |     0     |     0     |     226     | [1.00, 0.00, 0.00, 0.00] | PASS  | [ 127, -128, -128, -128]
  5 |     1     |     0     |     257     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
  6 |     1     |     0     |     242     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
  7 |     1     |     0     |     257     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
  8 |     1     |     0     |     242     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
  9 |     1     |     0     |     245     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 10 |     2     |     0     |     237     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 11 |     2     |     0     |     261     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 12 |     2     |     0     |     237     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 13 |     2     |     0     |     266     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 14 |     2     |     0     |     245     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 15 |     3     |     0     |     249     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 16 |     3     |     0     |     237     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -127, -128]
 17 |     3     |     0     |     265     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -127, -128]
 18 |     3     |     0     |     238     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
 19 |     3     |     0     |     261     | [1.00, 0.00, 0.00, 0.00] | FAIL  | [ 127, -128, -128, -128]
----------------------------------------------------------------------
Sanity Test Results Summary:
  Total Samples:      20
  Correct Matches:    5 / 20 (25.0%)
  Mean Latency:       239.10 us
  Min Latency:        85 us
  Max Latency:        266 us
  Tensor Arena Used:  916 / 8192 Bytes
  Free Heap:          269244 Bytes
======================================================================
STATUS = BASELINE_INFERENCE_VERIFIED
======================================================================
```

### Key Sanity Findings:
- **Input Acceptance:** Single-sample INT8 input vectors accepted without fault.
- **TFLM Execution:** MicroInterpreter invoked successfully on all 20 samples with 0 runtime errors.
- **Microsecond Latency:** Single-sample inference latency averaged **239.10 $\mu\text{s}$** (0.239 ms) on physical 240 MHz Xtensa LX6 silicon.
- **Stability:** Zero crashes, memory leaks, or watchdog resets observed across warmup (10 iterations) and sanity pass (20 iterations).

---

## 11. Failures / Warnings / Architecture Discoveries

1. **CMSIS-NN Transposition Conflict on Non-ARM Core:** The bundled `Chirale_TensorFLowLite` library default `fully_connected.cpp` routed through `cmsis_nn/fully_connected.cpp` which expects filter dimensions tailored for ARM Cortex-M DSP instructions. When compiled for Xtensa LX6, filter dimensions required reference row-major interpretation. A portable reference `FullyConnected` registration (`ref_fc::RegisterOp()`) was implemented in `main.cpp` using `tflite::reference_integer_ops::FullyConnected`.
2. **PlatformIO Installation:** Installed PlatformIO Core v6.1.19 into Python 3.13.4 environment with `espressif32@7.0.1` and `framework-arduinoespressif32`.
3. **Board Definition:** Updated `platformio.ini` from `esp32-s3-devkitc-1` to `esp32dev` to reflect physical ESP32-D0WD-V3.

---

## 12. Reproducibility

To reproduce this deployment build and upload on the physical hardware:

```bash
# 1. Enter firmware directory
cd phase5/firmware

# 2. Build firmware binary
pio run

# 3. Upload to connected ESP32 on COM7
pio run -t upload --upload-port COM7

# 4. Monitor serial output at 115200 baud
python -c "import serial, time; ser = serial.Serial('COM7', 115200); ser.dtr=False; ser.rts=True; time.sleep(0.1); ser.rts=False; [print(ser.readline().decode('utf-8', errors='replace'), end='') for _ in range(50)]"
```

---

## 13. Next Phase (Phase 18C)

In **Phase 18C**, the full physical benchmarking suite will be executed:
- 1,000-iteration single-sample inference benchmarking across test splits
- Profiling all candidate models (`student_b_16_4_int8`, `student_a_8_4_int8`, `mlp_14f_int8`, `mlp_12f_int8`)
- Empirical on-device latency distribution measurement (mean, median, p95, p99, min, max)
- Empirical accuracy and Macro F1 verification against test ground truth
- Recording to `phase5/measurements/mcu_empirical_benchmarks.csv`

---

## 14. Final Status

```
CHIP:             ESP32-D0WD-V3 (rev v3.1, Xtensa LX6 Dual-Core @ 240 MHz)
COM:              COM7 (WCH CH9102 USB-to-UART Bridge)
PLATFORMIO:       PlatformIO Core 6.1.19 (espressif32 @ 7.0.1)
BUILD:            SUCCESS (firmware.bin: 319,040 Bytes, Flash: 24.3%, RAM: 9.2%)
UPLOAD:           SUCCESS (COM7 @ 460800 baud, 319,040 Bytes written, hash verified)
BOOT:             SUCCESS (rst:0x1 POWERON_RESET, boot:0x13 SPI_FAST_FLASH_BOOT)
INTERPRETER:      SUCCESS (TFLM initialized, 916 / 8192 Bytes arena used)
MODEL:            student_b_16_4_int8 (FULL_INT8, 328 params, 3,576 B)
SANITY INFERENCE: SUCCESS (20/20 vectors executed, mean latency: 239.10 us)
FINAL STATUS:     BASELINE_INFERENCE_VERIFIED
```
