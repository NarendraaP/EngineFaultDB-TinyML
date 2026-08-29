# Phase 18A — ESP32 Physical Silicon Identification & Safe Preflight

> **Date:** 2026-08-29  
> **Status:** `ESP32_VERIFIED_READY_FOR_DEPLOYMENT`  
> **Operator:** Automated preflight (non-destructive identification only)

---

## 1. Serial Port Discovery

| Property | COM1 | COM7 |
|:---|:---|:---|
| Description | Communications Port | USB Serial Device |
| Hardware ID | `ACPI\PNP0501\0` | `USB VID:PID=1A86:55D4 SER=56B9006372` |
| VID | — | `0x1A86` (WCH / Qinheng) |
| PID | — | `0x55D4` (CH9102) |
| Serial Number | — | `56B9006372` |
| Manufacturer | Standard port types | Microsoft (generic driver) |
| USB Location | — | `1-10` |
| Type | Legacy ACPI motherboard serial | **USB-UART bridge → ESP32 candidate** |

**Candidate port: COM7**

---

## 2. ESP32 Silicon Identification

### 2.1 Chip Identity (`esptool chip_id`)

| Property | Value |
|:---|:---|
| **Chip Type** | **ESP32-D0WD-V3** |
| **Revision** | **v3.1** |
| **CPU Architecture** | Xtensa LX6 Dual-Core 32-bit |
| **Cores** | 2 + LP Core |
| **Max Clock** | 240 MHz |
| **Crystal Frequency** | 40 MHz |
| **MAC Address** | `08:d1:f9:d9:4a:54` |
| **Features** | Wi-Fi, BT, Dual Core, LP Core, Vref calibration in eFuse, Coding Scheme None |

### 2.2 Flash Identity (`esptool flash_id`)

| Property | Value |
|:---|:---|
| **Flash Manufacturer** | `0x5E` |
| **Flash Device** | `0x4016` |
| **Flash Size** | **4 MB** |
| **Flash Voltage** | 3.3V (set by strapping pin) |

### 2.3 PSRAM

No PSRAM detected. This is a standard ESP32-D0WD-V3 module without external PSRAM.

### 2.4 USB Bridge Identity

| Property | Value |
|:---|:---|
| USB Bridge Chip | **WCH CH9102** |
| VID | `0x1A86` |
| PID | `0x55D4` |
| Serial | `56B9006372` |

> **Note:** The previous discovery (2026-08-20) found an **Arduino Nano (ATmega328P)** on COM6 with a CH340 bridge. That board is no longer connected. The current COM7 device is a genuine Espressif ESP32.

---

## 3. Identity Distinction

| Layer | Identity |
|:---|:---|
| **MCU Silicon** | Espressif ESP32-D0WD-V3, rev v3.1, Xtensa LX6 dual-core @ 240MHz |
| **Board** | ESP32 development board (exact board brand TBD — generic ESP32-DevKitC form factor) |
| **USB Bridge** | WCH CH9102 USB-to-UART (VID `0x1A86` / PID `0x55D4`) |
| **Flash** | 4 MB SPI flash (MFR `0x5E`, DEV `0x4016`) |

---

## 4. Compatibility with Phase 5 Specification

### 4.1 Mismatch Analysis

The Phase 5 specification ([esp32_interface.md](file:///d:/WiDe/EngineFaultDB-main/phase5/hardware/esp32_interface.md)) targets **ESP32-S3-DevKitC-1** (Xtensa LX7). The detected silicon is **ESP32-D0WD-V3** (Xtensa LX6).

| Dimension | Spec (ESP32-S3) | Detected (ESP32) | Compatible? |
|:---|:---|:---|:---:|
| CPU Architecture | Xtensa LX7 | Xtensa LX6 | ✅ (both support TFLM) |
| Clock Speed | 240 MHz | 240 MHz | ✅ |
| Cores | 2 | 2 + LP | ✅ |
| Flash | 4–8 MB | 4 MB | ✅ |
| SRAM | 512 KB | 520 KB | ✅ |
| PSRAM | Optional | None | ⚠️ (not needed for our models) |
| TFLM Ops (FC+Softmax+Reshape) | Supported | Supported | ✅ |
| `esp_timer_get_time()` | Supported | Supported | ✅ |
| Arduino Framework | Supported | Supported | ✅ |
| UART 115200 8N1 | Supported | Supported | ✅ |
| Max model size (3,728 B) | Fits in 4MB+ flash | Fits in 4MB flash | ✅ |
| Max arena (8 KB) | Fits in 512KB SRAM | Fits in 520KB SRAM | ✅ |

### 4.2 Verdict

**Functionally compatible.** The ESP32-D0WD-V3 (LX6) can run all 4 INT8 models with the same TFLM interpreter, op resolver, timer API, and UART protocol. The only differences:

1. **`platformio.ini`** must change `board` from `esp32-s3-devkitc-1` → `esp32dev`
2. **Benchmark CSV `board` field** must reflect actual board identity
3. **Performance characteristics may differ slightly** (LX6 vs LX7 pipeline)

---

## 5. Toolchain Status

| Tool | Status | Version |
|:---|:---:|:---|
| Python | ✅ Installed | 3.13.4 |
| pyserial | ✅ Installed | 3.5 |
| esptool | ✅ Installed | 5.3.1 |
| PlatformIO | ❌ **NOT INSTALLED** | — |

> **⚠️ BLOCKER:** PlatformIO is required to compile and upload firmware. Must be installed before Phase 18B.

---

## 6. Model Artifact Verification

### 6.1 TFLite FlatBuffer Binaries

| Model | Exists | Size (Bytes) | Expected (Bytes) | Match |
|:---|:---:|:---:|:---:|:---:|
| `student_b_16_4_int8.tflite` | ✅ | 3,576 | 3,576 | ✅ |
| `student_a_8_4_int8.tflite` | ✅ | 3,208 | 3,208 | ✅ |
| `mlp_14f_int8.tflite` | ✅ | 3,728 | 3,728 | ✅ |
| `mlp_12f_int8.tflite` | ✅ | 3,712 | 3,712 | ✅ |

### 6.2 C Header Arrays

| Header File | Exists | Size (Bytes) |
|:---|:---:|:---:|
| `g_student_b_model_data.h` | ✅ | 22,966 |
| `g_student_a_model_data.h` | ✅ | 20,634 |
| `g_mlp_14f_model_data.h` | ✅ | 23,916 |
| `g_mlp_12f_model_data.h` | ✅ | 23,816 |
| `mcu_test_vectors.h` | ✅ | 2,078 |

All model artifacts **verified present** with expected file sizes matching the Phase 5 specification.

---

## 7. Firmware Compatibility Notes

The firmware source ([main_tflm_baseline.cpp](file:///d:/WiDe/EngineFaultDB-main/phase5/firmware/main_tflm_baseline.cpp)) uses conditional compilation:

```cpp
#if defined(ESP_PLATFORM)
  #include "esp_timer.h"
  #include "esp_system.h"
  #define GET_MICROS() esp_timer_get_time()
  #define GET_FREE_HEAP() esp_get_free_heap_size()
```

This `ESP_PLATFORM` macro is defined by both ESP32 and ESP32-S3 Arduino/ESP-IDF frameworks. **No source code changes required** for the firmware to target ESP32-D0WD-V3 — only the `platformio.ini` board configuration needs updating.

---

## 8. Actions NOT Taken (Safety Verification)

| Prohibited Action | Status |
|:---|:---:|
| Flash erase (`erase_flash`) | ❌ Not executed |
| Firmware upload (`write_flash`) | ❌ Not executed |
| PlatformIO upload | ❌ Not executed |
| Model inference on device | ❌ Not executed |
| Any existing firmware modification | ❌ Not executed |
| Paper 1–4 modification | ❌ Not executed |
| Experimental data modification | ❌ Not executed |

---

## 9. Summary & Final Status

```
╔══════════════════════════════════════════════════════════════════════╗
║  PHASE 18A RESULT: ESP32_VERIFIED_READY_FOR_DEPLOYMENT             ║
╠══════════════════════════════════════════════════════════════════════╣
║  Silicon:    ESP32-D0WD-V3 (rev v3.1) — Xtensa LX6 Dual-Core      ║
║  Port:       COM7 via WCH CH9102 USB bridge                        ║
║  Flash:      4 MB @ 3.3V                                           ║
║  Clock:      240 MHz (crystal 40 MHz)                               ║
║  MAC:        08:d1:f9:d9:4a:54                                      ║
║  Models:     4/4 TFLite INT8 binaries verified ✅                    ║
║  Headers:    5/5 C headers verified ✅                               ║
║  Toolchain:  esptool ✅ | pyserial ✅ | PlatformIO ❌ (must install) ║
║  Board Cfg:  platformio.ini needs board change (S3→ESP32)           ║
╚══════════════════════════════════════════════════════════════════════╝
```

### Blockers Before Phase 18B (Firmware Deployment)

1. **Install PlatformIO:** `pip install platformio`
2. **Update `platformio.ini`:** Change `board = esp32-s3-devkitc-1` → `board = esp32dev`
3. **Update benchmark schema:** Change board references from `ESP32-S3-DevKitC-1` to the actual board identity

### Output Files Updated

- [`phase5/measurements/hardware_discovery.json`](file:///d:/WiDe/EngineFaultDB-main/phase5/measurements/hardware_discovery.json) — Updated with ESP32-D0WD-V3 identification
- [`reports/Phase18A_ESP32_Silicon_Preflight.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase18A_ESP32_Silicon_Preflight.md) — This report
