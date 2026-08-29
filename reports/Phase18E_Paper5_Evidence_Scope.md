# Phase 18E — Paper 5 Evidence Scope & Research Contribution Blueprint

> **Manuscript Title:** Paper 5 — On-Device Deployment and Hardware Validation of QoS-Aware TinyML on ESP32 Microcontrollers  
> **Target Venue:** Specialized Embedded Systems / Edge AI / TinyML Journal (e.g., *IEEE Embedded Systems Letters*, *ACM Transactions on Embedded Computing Systems*, or *MDPI Sensors*)  
> **Status:** `NEW_HARDWARE_CLAIM_UNLOCKED` (Empirical dataset fully verified and archived)  

---

## 1. Paper 5 Unique Research Contribution

To prevent overlap or redundancy with Papers 1–4, Paper 5 is dedicated to the **systems-level implementation, deployment architecture, and comprehensive on-device characterization of TinyML models on resource-constrained 32-bit microcontrollers**.

```
+---------------------------------------------------------------------------------------------------------+
| PAPERS 1–4 FOCUS (Theoretical & Algorithmic) | PAPER 5 FOCUS (Physical Systems & Hardware Characterization) |
+----------------------------------------------+----------------------------------------------------------+
| Paper 1: QoS scheduler state machine logic   | Real-time on-chip timer instrumentation & FreeRTOS state |
| Paper 2: Mathematical 3D Pareto frontier     | Silicon latency distributions & empirical trade-offs     |
| Paper 3: Diagnostic fault domain features    | Single-sample MCU execution & SRAM memory budgeting      |
| Paper 4: Independent verification taxonomy   | Concrete physical firmware build & UART telemetry setup  |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Complete Experimental Evidence Inventory for Paper 5

Paper 5 possesses a fully validated, un-synthesized experimental dataset produced across Phases 18A–18D:

### 1. Interrogated Physical Silicon Baseline:
- **Silicon Target:** Espressif ESP32-D0WD-V3 (revision v3.1, Xtensa LX6 dual-core @ 240 MHz, Crystal: 40 MHz).
- **Storage Subsystems:** 4 MB physical SPI Flash @ 3.3V, 320 KB internal SRAM, 0 PSRAM.
- **Hardware Communications:** WCH CH9102 USB-to-UART bridge on `COM7` @ 115200 / 460800 baud.

### 2. Comprehensive Latency Distributions ($N=24,000$ Measured Single-Sample Inferences):
- **Full Percentile Breakdown:** Mean, Median (P50), P25, P75, P95, P99, IQR, Minimum, and Maximum reported per round ($N=2,000$) and pooled ($N=6,000$) per model.
- **Parametric Latency Progression:**
  - `student_a_8_4_int8` (176 params): Mean = **$64.55\,\mu\text{s}$**, P95 = **$69.00\,\mu\text{s}$**, P99 = **$76.00\,\mu\text{s}$**
  - `student_b_16_4_int8` (328 params): Mean = **$72.96\,\mu\text{s}$**, P95 = **$83.00\,\mu\text{s}$**, P99 = **$83.00\,\mu\text{s}$**
  - `mlp_12f_int8` (380 params): Mean = **$76.77\,\mu\text{s}$**, P95 = **$83.00\,\mu\text{s}$**, P99 = **$90.00\,\mu\text{s}$**
  - `mlp_14f_int8` (412 params): Mean = **$89.90\,\mu\text{s}$**, P95 = **$95.00\,\mu\text{s}$**, P99 = **$101.00\,\mu\text{s}$**

### 3. Multi-Round Repeatability & Stability Evidence:
- 3 independent execution rounds per model showing inter-round standard deviation $<0.03\,\mu\text{s}$ on deterministic runs.
- 95% Confidence Interval half-widths $<\pm 0.22\,\mu\text{s}$ across all models.

### 4. Memory Architecture & Resource Budgeting:
- **Flash Memory Accounting:** 330,153 Bytes program image (25.19% of 1.25 MB partition, 7.88% of 4MB Flash chip).
- **Static SRAM Accounting:** 61,944 Bytes (18.90% of 320 KB internal SRAM).
- **Tensor Arena Sizing:** 8,192 Bytes statically allocated buffer; **916 Bytes** committed allocator usage ($88.82\%$ safety headroom).
- **Dynamic Heap Determinism:** **0 Bytes** heap allocated during inference; **0 Bytes** memory leak over 25,200 total executions.

### 5. Implementation & Portability Findings:
- Detailed documentation of the portable reference `FullyConnected` operator implementation that bypasses ARM-specific CMSIS-NN assumptions on Xtensa LX6 architectures.

---

## 3. Paper 5 Outline & Structural Plan

1. **Introduction:** Microcontroller-based TinyML challenges, memory boundaries, and real-time execution constraints in industrial edge monitoring.
2. **Embedded Deployment Architecture:** ESP32 hardware platform, PlatformIO toolchain, TensorFlow Lite for Microcontrollers runtime, and portable kernel implementation.
3. **Benchmarking Methodology:** Hardware timer instrumentation (`esp_timer_get_time()`), in-RAM latency buffering, zero-I/O measurement loops, and multi-round statistical protocols.
4. **Empirical Performance Evaluation:**
   - Single-sample latency distributions and parameter scaling trends.
   - Host x86_64 vs ESP32 execution slowdown analysis ($62.9\times\text{--}76.8\times$).
   - Multi-round stability and execution repeatability.
5. **Memory Footprint & Resource Utilization:** Deconstruction of Flash, Static RAM, Tensor Arena allocator commitment, and dynamic heap stability.
6. **Real-Time Feasibility & Deadline Margin Analysis:** Evaluation against 5–100 ms industrial diagnostic deadlines.
7. **Threats to Validity & Embedded Limitations:** Discussion of reference vs DSP kernels, ambient operating conditions, and lack of hardware floating-point acceleration.
8. **Conclusion & Future Directions:** On-chip multi-task scheduling, dynamic power profiling, and hardware-in-the-loop validation.
