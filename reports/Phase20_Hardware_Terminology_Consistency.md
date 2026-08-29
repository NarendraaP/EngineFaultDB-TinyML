# Phase 20 — Cross-Paper Hardware Terminology Consistency Audit

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** Terminology, Memory Subsystem Scoping, and Hardware Naming Across Papers 1–5  
**Date:** August 29, 2026  

---

## 1. Objectives

This audit verifies that all hardware descriptions, memory definitions, and execution terms are mathematically and architecturally consistent across Papers 1–5, ensuring that no manuscript introduces conflicting silicon properties or misleading hardware abstractions.

---

## 2. Terminology Evaluation Across Core Concepts

### A. Microcontroller Silicon Identification
* **Authoritative Identification:** Espressif ESP32-D0WD-V3, silicon revision v3.1, dual-core 32-bit Xtensa LX6 microprocessor @ $240\,\text{MHz}$, $40\,\text{MHz}$ crystal oscillator.
* **Paper 1:** ESP32-D0WD-V3, Xtensa LX6 @ $240\,\text{MHz}$, $320\,\text{KB}$ SRAM $\rightarrow$ **CONSISTENT**.
* **Paper 2:** ESP32-D0WD-V3, Xtensa LX6 @ $240\,\text{MHz}$, $320\,\text{KB}$ SRAM $\rightarrow$ **CONSISTENT**.
* **Paper 3:** ESP32-D0WD-V3, Xtensa LX6 @ $240\,\text{MHz}$, $320\,\text{KB}$ SRAM $\rightarrow$ **CONSISTENT**.
* **Paper 4:** ESP32-D0WD-V3, Xtensa LX6 @ $240\,\text{MHz}$, $320\,\text{KB}$ SRAM $\rightarrow$ **CONSISTENT**.
* **Paper 5:** ESP32-D0WD-V3 (rev v3.1), dual-core Xtensa LX6 @ $240\,\text{MHz}$, $4\,\text{MB}$ Flash, $320\,\text{KB}$ SRAM, 0 PSRAM $\rightarrow$ **CONSISTENT (Most Detailed)**.

---

### B. Memory Subsystem Terminology
The audit audited every memory classification term used across the portfolio:

| Term / Memory Subsystem | Allowed Definition | Usage in Manuscripts | Audit Classification |
|---|---|---|---|
| **$916\,\text{Bytes}$ Usage** | *Allocator-committed tensor usage* or *committed tensor arena buffer allocation* | Correctly defined in P1, P2, P3, P4, and P5 as TFLM runtime buffer allocation for model tensors | **PASS** |
| **$8,192\,\text{Bytes}$ Arena** | *Pre-allocated static tensor arena buffer* | Stated as pre-allocated static arena in internal SRAM | **PASS** |
| **$61,944\,\text{Bytes}$ SRAM** | *Internal static SRAM footprint* | Stated as global data structures, system stacks, and runtime descriptors | **PASS** |
| **$330,153\,\text{Bytes}$ Flash** | *Compiled firmware image footprint* | Stated as $25.19\%$ of the $1.25\,\text{MB}$ app partition | **PASS** |
| **$237,452\,\text{Bytes}$ Free Heap** | *Constant free dynamic heap* | Verified as remaining free heap with zero dynamic allocation | **PASS** |
| **"Zero Dynamic Allocation"** | Scoped strictly to *tested firmware / benchmark inference loop* | Explicitly qualified as zero `malloc`/`new` calls during inference execution | **PASS** |

---

### C. Latency and Timing Terminology
* **Timing Scope:** All papers explicitly define measured latency as the isolated execution of `interpreter.Invoke()`, timed with the microsecond-resolution hardware timer (`esp_timer_get_time()`).
* **Excluded Operations:** Sensor acquisition, normalization/scaling, UART logging, and memory setup are explicitly excluded from isolated kernel timing.
* **Empirical Maximum vs. WCET:** Every manuscript explicitly distinguishes empirical maximum latency ($102\,\si{\micro\second}$) from formal static Worst-Case Execution Time (WCET).
* **Single-Sample Compute Equivalent:** All reciprocal throughput conversions ($15,491.9\,\text{inferences/sec}$) are explicitly scoped as single-sample compute equivalents on a single core, not end-to-end sensor-to-actuator throughput.

---

### D. Model Monotonicity and Distillation Scaling
* **Monotonicity Scope:** Described strictly as a *monotonic trend within the evaluated four-model set on bare-metal Xtensa LX6 silicon* ($R^2 = 0.963$).
* **Distillation Speedup:** Formally described as: *The evaluated `student_a_8_4_int8` model exhibited a $28.20\%$ lower isolated ESP32 inference latency than the evaluated `mlp_14f_int8` baseline.*

---

## 3. Discrepancy Classification & Verdict

* **Critical Contradictions:** **NONE (0)**
* **Material Discrepancies:** **NONE (0)**
* **Minor Terminology Inconsistencies:** **NONE (0)**

**HARDWARE TERMINOLOGY VERDICT: FULLY CONSISTENT AND SCIENTIFICALLY DEFENSIBLE**
