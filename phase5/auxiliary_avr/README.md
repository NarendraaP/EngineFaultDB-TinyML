# Phase 5L: Auxiliary AVR Experimental Boundary Specification

> **Classification Tag:** `AUXILIARY_AVR_EXPERIMENT`  
> **Storage Location:** `phase5/auxiliary_avr/`  
> **Hardware Architectures:** Atmel / Microchip 8-bit AVR RISC  
> **Target Boards:** Arduino Mega 2560 (ATmega2560), Arduino Uno / Nano (ATmega328P)

---

## 1. Purpose & Scope of Auxiliary AVR Experiments

The experimental scripts and firmware under `phase5/auxiliary_avr/` serve strictly isolated auxiliary benchmarking and hardware transport validation roles. They are designed to probe low-level embedded mechanics without executing full neural network models.

Specifically, the auxiliary AVR suite is restricted to:
1. **Timer Resolution & Jitter Testing:** Evaluating standard 16 MHz 8-bit timer prescalers (`micros()`, `millis()`, and 16-bit Timer1/Timer3 input capture registers) to establish baseline timing jitter and quantization noise in low-cost microcontrollers.
2. **Serial Transport & Telemetry Validation:** Stress-testing UART serial communications (STK500v1 protocol, JSON-line streaming at 57,600 and 115,200 baud, buffer overflow characteristics) to validate telemetry parsers on the host runner.
3. **Discrete State Machine Timing:** Measuring the cycle overhead and latency variance of pure discrete logic state machines (e.g., fallback lookup tables, threshold-based trigger logic) isolated from neural tensor engines.

---

## 2. Target Hardware Specifications

| Parameter | Arduino Uno / Nano | Arduino Mega 2560 | Primary Target: ESP32-S3 *(For Contrast)* |
| :--- | :--- | :--- | :--- |
| **Microcontroller (MCU)** | ATmega328P | ATmega2560 | ESP32-S3 (Xtensa LX7 Dual-Core) |
| **CPU Architecture** | 8-bit AVR RISC | 8-bit AVR RISC | 32-bit Xtensa Dual-Core + Vector SIMD |
| **Clock Frequency** | 16 MHz (1 clock/instruction) | 16 MHz (1 clock/instruction) | 240 MHz (Dual-Issue Superscalar) |
| **SRAM (RAM)** | **2 KB** (2,048 Bytes) | **8 KB** (8,192 Bytes) | **512 KB** internal SRAM |
| **Program Flash Memory** | 32 KB (0.5 KB bootloader) | 256 KB (8 KB bootloader) | 4 MB – 8 MB Quad SPI Flash |
| **Hardware FPU** | None (Software float emulation) | None (Software float emulation) | Hardware Single-Precision FPU |
| **TensorFlow Lite Micro** | **Unsupported** (Insufficient RAM) | **Unsupported** (Insufficient RAM) | **Fully Supported** (Accelerated) |

---

## 3. Fundamental Architecture Limitations

1. **8-bit Architecture & Math Emulation:**
   The AVR core operates with 8-bit registers and an 8-bit ALU. All 32-bit integer arithmetic (required by TFLite quantized INT8 accumulators) and 32-bit IEEE-754 floating-point operations require dozens of clock cycles per operation via software emulation libraries (`libgcc`).
2. **Strict SRAM Incompatibility:**
   TensorFlow Lite for Microcontrollers (TFLM) requires a contiguous tensor arena of at least 2 KB to 8 KB just for interpreter book-keeping, runtime tensor structs, and intermediate activation buffers. The ATmega328P (2 KB SRAM) cannot allocate the tensor arena and stack simultaneously. The ATmega2560 (8 KB SRAM) exhausts virtually all memory on the interpreter skeleton alone.
3. **Absence of SIMD / DSP Instructions:**
   AVR microcontrollers have no vector or SIMD extensions (unlike the ESP32-S3's PIE instructions or ARM Cortex-M CMSIS-NN), rendering matrix-vector multiply-accumulate (MAC) loops extraordinarily slow.
4. **Clock Disparity:**
   Running at 16 MHz, AVR executes 15× fewer clock cycles per second than an ESP32 at 240 MHz, completely misrepresenting real-time powertrain deadline compliance.

---

## 4. Strict Methodological Rules & Guardrails

To prevent scientific misrepresentation, invalid benchmarking claims, and faulty cross-platform generalizations, the following four rules are strictly enforced across the codebase:

```
+---------------------------------------------------------------------------------------------------+
|                                  STRICT METHODOLOGICAL GUARDRAILS                                 |
|                                                                                                   |
|  [Rule 1]  NEVER claim ESP32 compatibility or equivalence from AVR results.                      |
|  [Rule 2]  NEVER claim automotive ECU compatibility or ISO 26262 automotive compliance.           |
|  [Rule 3]  NEVER claim TensorFlow Lite for Microcontrollers (TFLM) performance from AVR tests.    |
|  [Rule 4]  NEVER claim realistic TinyML MCU inference latency or QoS compliance from AVR.         |
+---------------------------------------------------------------------------------------------------+
```

### Detailed Invariant Definitions:
- **Rule 1 — No ESP32 Equivalence:** AVR timing, memory usage, or serial throughput figures must never be extrapolated or projected as proxy measurements for 32-bit ESP32 / ESP32-S3 silicon.
- **Rule 2 — No Automotive ECU Claims:** 8-bit hobbyist development boards (ATmega328P / ATmega2560) do not conform to AEC-Q100 automotive grade specifications, CAN FD bus timing, or ISO 26262 functional safety constraints.
- **Rule 3 — No TFLM Performance Claims:** Because TFLite Micro is not running on AVR, no timing captured on AVR can be attributed to TensorFlow Lite Micro kernel execution.
- **Rule 4 — No Realistic TinyML Performance Claims:** Any latency measured on AVR reflects only rudimentary test stubs or scalar routines, not optimized TinyML execution pipelines.

---

## 5. Result Tagging & Output Requirements

- **Mandatory Result Tag:** Every output JSON packet, CSV record, stdout banner, and summary report generated within this directory must prominently include:
  ```
  STATUS: AUXILIARY_AVR_EXPERIMENT
  ```
- **Directory Isolation:** All firmware source code, platform configurations, test sketches, serial capture logs, and timing measurements must remain strictly inside `phase5/auxiliary_avr/`.

---

## 6. Directory Structure

```
phase5/auxiliary_avr/
├── README.md                          <- This boundary specification document
├── firmware/                          <- AVR test sketches (e.g., timer prescaler, UART loopback)
├── measurements/                      <- Isolated AVR test logs (tagged AUXILIARY_AVR_EXPERIMENT)
└── scripts/                           <- Host Python serial probe and STK500 sync validation scripts
```
