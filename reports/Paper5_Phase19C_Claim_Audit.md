# Paper 5 — Phase 19C Comprehensive Claim & Language Audit Report

> **Manuscript:** Paper 5 — On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers  
> **Evaluation Mode:** Fine-Grained Linguistic and Epistemological Claim Audit  
> **Audit Status:** `MINOR_WORDING_CORRECTIONS_IDENTIFIED`  

---

## 1. Sensitive Terminology Scan & Disposition Matrix

A full-text regular-expression scan of `submission/paper.tex` yielded the following findings:

```
+---------------------------------------------------------------------------------------------------------+
| SEARCHED TERM     | OCCURRENCES | LOCATION IN MANUSCRIPT        | ACTION REQUIRED | DISPOSITION RATIONALE   |
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "first"           | 1           | Section VII (Related Work)    | ⚠️ REWRITE       | Replace "first" with    |
|                   |             |                               |                 | "an empirical" to avoid |
|                   |             |                               |                 | temporal priority hype. |
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "proving"         | 1           | Section X (Conclusion)        | ⚠️ REWRITE       | Replace with "demonstrat|
|                   |             |                               |                 | -ing" (inductive logic).|
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "safety headroom" | 1           | Section VI-A (Memory Subsys.) | ⚠️ REWRITE       | Replace with "unallocat-|
|                   |             |                               |                 | ed arena headroom".     |
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "WCET"            | 3           | Section IV-C, Section VIII    | ✅ RETAINED     | Explicitly disclaims    |
|                   |             |                               |                 | formal static WCET.     |
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "throughput"      | 1           | Section IV-C                  | ✅ RETAINED     | Explicitly qualified as |
|                   |             |                               |                 | single-sample compute   |
|                   |             |                               |                 | equivalent capacity.    |
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "real-time"       | 3           | Abstract, Intro, Sec IV-C     | ✅ RETAINED     | Used in application     |
|                   |             |                               |                 | context & deadlines.    |
+-------------------+-------------+-------------------------------+-----------------+-------------------------+
| "SOTA" / "best"   | 0           | None                          | ✅ CLEAN        | Zero occurrences.       |
| "pioneering"      | 0           | None                          | ✅ CLEAN        | Zero occurrences.       |
| "universal"       | 0           | None                          | ✅ CLEAN        | Zero occurrences.       |
| "guarantees"      | 0           | None                          | ✅ CLEAN        | Zero occurrences.       |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Epistemological Claim Hierarchy Mapping

Every major conclusion in Paper 5 is mapped to its authoritative epistemological classification:

```
+---------------------------------------------------------------------------------------------------------+
| MANUSCRIPT CONCLUSION / CLAIM                         | AUTHORITATIVE EVIDENCE TIER | VERIFICATION BASIS        |
+-------------------------------------------------------+-----------------------------+---------------------------+
| Single-sample on-device latency is 64.55 - 89.90 us   | DIRECT_PHYSICAL_MEASUREMENT | esp_timer_get_time() logs |
| Distillation reduces on-chip latency by 28.20%        | DERIVED_FROM_MEASUREMENT    | (89.90 - 64.55) / 89.90   |
| Parameter count vs. latency follows linear R^2 = 0.963| STATISTICAL_DESCRIPTION     | Linear OLS fit on 4 points|
| Host-to-ESP32 slowdown ratio is 62.87x to 76.77x      | DERIVED_FROM_MEASUREMENT    | Physical Mean / Host Mean |
| Host sub-microsecond profiling exhibits rank inversion| INTERPRETATION              | Host noise floor unmasking|
| TFLite Micro commits 916 Bytes of tensor arena memory | DIRECT_PHYSICAL_MEASUREMENT | arena_used_bytes() query  |
| Runtime executes with 0 Bytes dynamic heap allocation | DIRECT_PHYSICAL_MEASUREMENT | esp_get_free_heap_size()  |
| Max latency of 102 us satisfies 5 ms edge deadline    | DERIVED_FROM_MEASUREMENT    | 102 us / 5,000 us = 2.04% |
| Cross-microcontroller transferability (ARM / RISC-V)  | FUTURE_WORK                 | Explicitly in Limitations |
| Physical energy consumption profiling in Joules       | FUTURE_WORK                 | Explicitly in Limitations |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Claim Audit Verdict

- **Verdict:** `MINOR_CORRECTIONS_REQUIRED`
- **Required Edit Summary:**
  1. In Section VII, line 282: Change `"the first empirical, publication-grade characterization"` to `"an empirical, publication-grade characterization"`.
  2. In Section X, line 297: Change `"and proving that structural knowledge distillation"` to `"and demonstrating that structural knowledge distillation"`.
  3. In Section VI-A, line 273: Change `"provides 88.82% safety headroom"` to `"provides 88.82% unallocated headroom"`.
