# Paper 5 — Phase 19A Revision, Experiment Decision & Readiness Plan

> **Manuscript Identifier:** Paper 5 — On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers  
> **Final Readiness Status:** `PAPER_5_READY_TO_DRAFT`  
> **Audited Physical Baseline:** ESP32-D0WD-V3 rev v3.1 (240 MHz, 4 MB Flash, 320 KB SRAM, COM7)  

---

## 1. Evaluation of Potential Experimental Additions (Options A–H)

We audited eight potential experimental additions to determine whether any genuine evidence gap blocks publication:

```
+---------------------------------------------------------------------------------------------------------+
| EXPERIMENTAL ADDITION            | CLASSIFICATION | AUDIT RATIONALE & SCIENTIFIC JUSTIFICATION          |
+----------------------------------+----------------+-----------------------------------------------------+
| A. Additional Benchmark Rounds   | NOT_NEEDED     | 3 rounds x 2,000 runs (N=6,000 pooled per model)    |
|    (e.g., Round 4-5)             |                | yields 95% CI < +/-0.22 us and SD variation <0.03 us|
|                                  |                | Further rounds would yield zero new variance data.  |
+----------------------------------+----------------+-----------------------------------------------------+
| B. Different Core Affinity       | FUTURE_WORK /  | Dedicated Core 1 execution isolates kernel timing   |
|    (Core 0 vs Core 1)            | OPTIONAL       | cleanly from Wi-Fi/BT OS interrupts on Core 0.      |
|                                  |                | Dual-core contention can be explored in future work.|
+----------------------------------+----------------+-----------------------------------------------------+
| C. RTOS Background-Load Benchmark| FUTURE_WORK /  | Synthetic contention is already modeled in Paper 1; |
|    (FreeRTOS task preemption)    | OPTIONAL       | Paper 5's role is isolated kernel characterization. |
+----------------------------------+----------------+-----------------------------------------------------+
| D. ESP-NN Assembly Kernels       | FUTURE_WORK    | Benchmarking portable reference kernels provides an |
|    (Xtensa SIMD extensions)      |                | architecture-independent baseline without lock-in.  |
+----------------------------------+----------------+-----------------------------------------------------+
| E. Hardware Power/Energy Shunt   | FUTURE_WORK    | While valuable, latency + memory characterization is|
|    (Joules / mW profiling)       |                | fully publication-sufficient for IEEE ESL / ACM TECS|
+----------------------------------+----------------+-----------------------------------------------------+
| F. Additional Model Topologies   | NOT_NEEDED     | The 4 INT8 models span 176 to 412 parameters,       |
|    (More than 4 models)          |                | covering uncompressed, distilled, and feature-pruned|
+----------------------------------+----------------+-----------------------------------------------------+
| G. Additional MCU Targets        | FUTURE_WORK    | Multi-chip comparisons belong in a follow-on survey |
|    (e.g., STM32, RP2040, ESP32-S3|                | Paper 5 establishes the definitive ESP32-D0WD-V3 ref.|
+----------------------------------+----------------+-----------------------------------------------------+
| H. End-to-End Sensor Pipeline    | FUTURE_WORK    | Adding ADC/I2C sensor delays would obscure pure     |
|    (Physical ADC / CAN-bus)      |                | neural network execution kernel characteristics.    |
+----------------------------------+----------------+-----------------------------------------------------+
```

---

## 2. Content Sufficiency Assessment

Paper 5 contains comprehensive, high-density experimental material covering all standard sections of an IEEE/ACM embedded systems article:
1. **Physical Silicon Identification & Hardware Setup:** Complete registers, clock tree ($240\,\text{MHz}$), Flash SPI bus ($80\,\text{MHz}$ QIO), and SRAM banks.
2. **Firmware & Portable Kernel Architecture:** Complete C++ implementation in PlatformIO bypassing CMSIS-NN dependencies.
3. **Statistical Latency Suite:** $24,000$ physical data points with Mean, Median, P95, P99, Max, IQR, CV%, and 95% Confidence Intervals.
4. **Host-to-Silicon Divergence:** Rigorous quantification of the $62.9\times\text{--}76.8\times$ slowdown and demonstration of host rank inversion vs. microcontroller monotonic scaling.
5. **Memory Subsystems:** Complete accounting of Flash partition, static SRAM, TFLM tensor arena ($916\,\text{B}$ committed), and heap invariance ($0\,\text{B}$ leak).
6. **Real-Time Deadlines & Feasibility:** Headroom calculations ($>97.96\%$) against $5\text{--}100\,\text{ms}$ edge control loops.

**Format Recommendation:** **SHORT PAPER / LETTER (4–6 pages)** for *IEEE Embedded Systems Letters* or **FOCUSED ARTICLE (8–10 pages)** for *ACM TECS*.

---

## 3. Final Readiness Verdict

### `PAPER_5_READY_TO_DRAFT`

- **Central Research Question:**  
  *How do ultra-low-resource INT8 TinyML models execute on physical 32-bit Xtensa microcontroller silicon, how does measured on-device latency diverge from host simulation, and how is static vs. working memory partitioned under bare-metal runtime constraints?*

- **Central Contribution:**  
  A rigorous empirical on-device characterization of four `FULL_INT8` TinyML models on ESP32-D0WD-V3 silicon across $24,000$ physical inferences, providing the first exact quantification of host-to-silicon latency divergence ($62.9\times\text{--}76.8\times$), physical knowledge distillation acceleration ($28.2\%$), and static tensor arena commitment ($916\,\text{Bytes}$) in the sub-4 KB embedded diagnostic regime.

- **Novelty Classification:** `NOVEL_EMPIRICAL_CHARACTERIZATION`
- **SOTA Status:** `STRONG_HARDWARE_CHARACTERIZATION`
- **Required New Experiments:** `NONE` (Existing empirical evidence is publication-complete and fully verified).
- **Recommended Venue:** *IEEE Embedded Systems Letters (ESL)* (Primary) / *ACM Transactions on Embedded Computing Systems (TECS)* (Alternative).
