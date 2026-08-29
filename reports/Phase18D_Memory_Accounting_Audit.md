# Phase 18D — Memory Accounting & Tensor Arena Audit Report

> **Date:** 2026-08-29  
> **Auditor Role:** Embedded Systems Memory Architecture & Footprint Auditor  
> **Target Silicon:** Espressif ESP32-D0WD-V3 (320 KB SRAM, 4 MB Flash)  
> **Audited Phase:** Phase 18C Physical On-Device Benchmark  

---

## 1. Separation of Memory Domains

The audit strictly separated and categorized all memory regions to ensure that Flash, Static SRAM, Tensor Arena, and Dynamic Heap are never conflated or double-counted:

```
+---------------------------------------------------------------------------------------+
|                                PHYSICAL SPI FLASH (4,194,304 Bytes)                  |
|  [ Bootloader: ~32KB ] [ App Partition: 1,310,720 B ] [ SPIFFS/Data Partition: ~2.6MB]|
|                        |                                                              |
|                        +--> Compiled Program: 330,153 Bytes (25.2% of App Partition)  |
|                             Embedded Models:  14,224 Bytes (Total 4 Model Arrays)    |
+---------------------------------------------------------------------------------------+

+---------------------------------------------------------------------------------------+
|                                INTERNAL SRAM (327,680 Bytes)                          |
|  [ Static RAM (.data + .bss): 61,944 B (18.9%) ] [ Free Dynamic Heap: 237,452 Bytes ] |
|  |                                                                                    |
|  +--> Statically Allocated Tensor Arena Buffer: 8,192 Bytes (8.0 KB)                  |
|       |                                                                               |
|       +--> Committed Working Buffers (TFLM used_bytes): 916 Bytes (11.2% of Arena)    |
|       +--> Unused Arena Safety Headroom:                7,276 Bytes (88.8% of Arena)  |
+---------------------------------------------------------------------------------------+
```

---

## 2. Memory Region Accounting Table

| Memory Domain | Interrogated Value | Available Capacity | Utilization % | Safety Headroom | Audit Status |
|:---|:---:|:---:|:---:|:---:|:---:|
| **Physical SPI Flash** | 330,512 Bytes (Binary) | 4,194,304 Bytes | **7.88%** | 3,863,792 Bytes (92.1%) | ✅ VERIFIED |
| **Application Partition** | 330,153 Bytes (Program) | 1,310,720 Bytes | **25.19%** | 980,567 Bytes (74.8%) | ✅ VERIFIED |
| **Model Flash Footprints** | 3,208 B (`student_a`)<br>3,576 B (`student_b`)<br>3,712 B (`mlp_12f`)<br>3,728 B (`mlp_14f`) | Flash Read-Only (`.rodata`) | — | Stored in Flash, mapped to DROM | ✅ VERIFIED |
| **Static SRAM (`.data` + `.bss`)** | 61,944 Bytes | 327,680 Bytes | **18.90%** | 265,736 Bytes (81.1%) | ✅ VERIFIED |
| **Static Tensor Arena** | 8,192 Bytes | 8,192 Bytes | **100.0%** | Included inside Static SRAM | ✅ VERIFIED |
| **TFLM Arena Working Usage** | 916 Bytes | 8,192 Bytes | **11.18%** | 7,276 Bytes (88.82%) | ✅ VERIFIED |
| **Free Dynamic Heap (Boot)** | 269,708 Bytes | Dynamic Heap Pool | — | 269.7 KB Available | ✅ VERIFIED |
| **Free Dynamic Heap (Post-Init)**| 237,452 Bytes | Dynamic Heap Pool | — | 237.4 KB Available | ✅ VERIFIED |
| **Dynamic Allocations in `Invoke()`**| **0 Bytes** | — | — | **Zero Runtime Heap Usage** | ✅ VERIFIED |

---

## 3. Tensor Arena Deconstruction & Audit

A critical question investigated during this audit was: **"Why do all four candidate models report an identical tensor arena utilization of exactly 916 Bytes?"**

### TFLite Micro Allocator Mechanism:
In TensorFlow Lite Micro (`tensorflow/lite/micro/micro_allocator.cpp`), memory within the static arena buffer is split into two growing regions:
1. **Head Allocations (Non-persistent / Persistent Structs):** Allocated downward from the top of the arena for `NodeAndRegistration` structs, `OpData` structs, and `TfLiteTensor` metadata wrappers. All allocations are 16-byte aligned.
2. **Tail Allocations (Tensor Buffers):** Planned by `MicroMemoryPlanner` (Greedy Memory Planner) for intermediate activation buffers.

### Allocator Breakdown for the Four MLPs:
Because all four candidate models share a similar 2-layer or 3-layer architecture:
- 1 Input Tensor (`[1, 14]` or `[1, 12]` INT8 $\rightarrow 16$ bytes aligned)
- 1 Hidden Layer Tensor (`[1, 16]` or `[1, 8]` INT8 $\rightarrow 16$ bytes aligned)
- 1 Output Tensor (`[1, 4]` INT8 $\rightarrow 16$ bytes aligned)
- 3 Op Registrations (`FullyConnected`, `Softmax`, `Reshape`)

The `MicroAllocator` rounds each chunk to 16-byte alignment boundaries. Consequently, the combined head structs and tail planned buffers yield an identical allocator commitment of **916 Bytes** across these models.

### Tensor Arena Classification Verdict:
- **Audit Classification:** **`VERIFIED_ALLOCATOR_USAGE`**
- **Mandatory Reporting Correction:** The 916 Byte figure must NOT be described as a "dynamic execution peak" (which implies variable run-time stack/heap watermarks). It must be cited as **"TFLM Static Allocator Committed Memory (`used_bytes()`)"**.

---

## 4. Zero Dynamic Leak Verification

Throughout the execution of all 25,200 physical inferences:
- Heap at start of benchmark: `237,452 Bytes`
- Heap at completion of benchmark: `237,452 Bytes`
- **Dynamic Heap Delta ($\Delta H$):** **`0 Bytes`**
- **Memory Leak Status:** **`ZERO LEAKS DETECTED`**

This confirms that the firmware achieves complete memory determinism required for high-reliability embedded and industrial deployments.
