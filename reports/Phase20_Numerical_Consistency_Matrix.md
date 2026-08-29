# Phase 20 — Cross-Paper Numerical Consistency Matrix

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** Numerical Verification Across Papers 1–5 Against Authoritative Sources  
**Date:** August 29, 2026  

---

## 1. Authoritative Physical Measurements Baseline

All physical microcontroller evidence originates from `phase5/measurements/esp32_full_benchmark.json` and `phase5/measurements/esp32_model_benchmark.csv`:
* Target Silicon: ESP32-D0WD-V3 rev v3.1 @ $240\,\text{MHz}$, $4\,\text{MB}$ Flash, $320\,\text{KB}$ SRAM, 0 PSRAM
* Total Inferences: $24,000$ timed single-sample measurements ($6,000$ per model across 3 independent rounds) + $1,200$ warmups ($25,200$ total physical invocations).

---

## 2. Complete Numerical Consistency Matrix

| Metric / Parameter | Authoritative Value | Paper 1 | Paper 2 | Paper 3 | Paper 4 | Paper 5 | Cross-Paper Match |
|---|---|---|---|---|---|---|---|
| **`student_a` Parameters** | 176 | 176 | 176 | 176 | 176 | 176 | **EXACT (PASS)** |
| **`student_a` Flash ROM** | $3,208\,\text{Bytes}$ | $3,208\,\text{B}$ | $3,208\,\text{B}$ | $3,208\,\text{B}$ | $3,208\,\text{B}$ | $3,208\,\text{B}$ | **EXACT (PASS)** |
| **`student_a` ESP32 Mean Latency** | $64.55\,\si{\micro\second}$ | $64.55\,\si{\micro\second}$ | $64.55\,\si{\micro\second}$ | $64.55\,\si{\micro\second}$ | $64.55\,\si{\micro\second}$ | $64.55\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_a` ESP32 P95 Latency** | $69.00\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_a` ESP32 P99 Latency** | $76.00\,\si{\micro\second}$ | N/A | N/A | N/A | N/A | $76.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_a` Host x86 Latency** | $1.02\,\si{\micro\second}$ | N/A | $1.02\,\si{\micro\second}$ | N/A | $1.02\,\si{\micro\second}$ | $1.02\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_a` Slowdown Ratio** | $63.28\times$ | N/A | N/A | N/A | N/A | $63.28\times$ | **EXACT (PASS)** |
| **`student_b` Parameters** | 328 | 328 | 328 | N/A | 328 | 328 | **EXACT (PASS)** |
| **`student_b` Flash ROM** | $3,576\,\text{Bytes}$ | $3,576\,\text{B}$ | $3,576\,\text{B}$ | N/A | $3,576\,\text{B}$ | $3,576\,\text{B}$ | **EXACT (PASS)** |
| **`student_b` ESP32 Mean Latency** | $72.96\,\si{\micro\second}$ | $72.96\,\si{\micro\second}$ | $72.96\,\si{\micro\second}$ | N/A | $72.96\,\si{\micro\second}$ | $72.96\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_b` ESP32 P95 Latency** | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | N/A | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_b` ESP32 P99 Latency** | $83.00\,\si{\micro\second}$ | N/A | N/A | N/A | N/A | $83.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_b` Host x86 Latency** | $0.98\,\si{\micro\second}$ | N/A | $0.98\,\si{\micro\second}$ | N/A | $0.98\,\si{\micro\second}$ | $0.98\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`student_b` Slowdown Ratio** | $74.45\times$ | N/A | N/A | N/A | N/A | $74.45\times$ | **EXACT (PASS)** |
| **`mlp_12f` Parameters** | 380 | 380 | 380 | N/A | 380 | 380 | **EXACT (PASS)** |
| **`mlp_12f` Flash ROM** | $3,712\,\text{Bytes}$ | $3,712\,\text{B}$ | $3,712\,\text{B}$ | N/A | $3,712\,\text{B}$ | $3,712\,\text{B}$ | **EXACT (PASS)** |
| **`mlp_12f` ESP32 Mean Latency** | $76.77\,\si{\micro\second}$ | $76.77\,\si{\micro\second}$ | $76.77\,\si{\micro\second}$ | N/A | $76.77\,\si{\micro\second}$ | $76.77\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_12f` ESP32 P95 Latency** | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | N/A | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_12f` ESP32 P99 Latency** | $90.00\,\si{\micro\second}$ | N/A | N/A | N/A | N/A | $90.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_12f` Host x86 Latency** | $1.00\,\si{\micro\second}$ | N/A | $1.00\,\si{\micro\second}$ | N/A | $1.00\,\si{\micro\second}$ | $1.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_12f` Slowdown Ratio** | $76.77\times$ | N/A | N/A | N/A | N/A | $76.77\times$ | **EXACT (PASS)** |
| **`mlp_14f` Parameters** | 412 | 412 | 412 | 412 | 412 | 412 | **EXACT (PASS)** |
| **`mlp_14f` Flash ROM** | $3,728\,\text{Bytes}$ | $3,728\,\text{B}$ | $3,728\,\text{B}$ | $3,728\,\text{B}$ | $3,728\,\text{B}$ | $3,728\,\text{B}$ | **EXACT (PASS)** |
| **`mlp_14f` ESP32 Mean Latency** | $89.90\,\si{\micro\second}$ | $89.90\,\si{\micro\second}$ | $89.90\,\si{\micro\second}$ | $89.90\,\si{\micro\second}$ | $89.90\,\si{\micro\second}$ | $89.90\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_14f` ESP32 P95 Latency** | $95.00\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_14f` ESP32 P99 Latency** | $101.00\,\si{\micro\second}$ | N/A | N/A | N/A | N/A | $101.00\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_14f` Host x86 Latency** | $1.43\,\si{\micro\second}$ | N/A | $1.43\,\si{\micro\second}$ | N/A | $1.43\,\si{\micro\second}$ | $1.43\,\si{\micro\second}$ | **EXACT (PASS)** |
| **`mlp_14f` Slowdown Ratio** | $62.87\times$ | N/A | N/A | N/A | N/A | $62.87\times$ | **EXACT (PASS)** |
| **Empirical Maximum Latency** | $102\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | **EXACT (PASS)** |
| **Distillation Speedup** | $28.20\%$ | N/A | $28.2\%$ | N/A | N/A | $28.20\%$ | **EXACT (PASS)** |
| **Tensor Arena Allocated** | $8,192\,\text{Bytes}$ | $8,192\,\text{B}$ | $8,192\,\text{B}$ | $8,192\,\text{B}$ | $8,192\,\text{B}$ | $8,192\,\text{B}$ | **EXACT (PASS)** |
| **Committed Arena Usage** | $916\,\text{Bytes}$ | $916\,\text{B}$ | $916\,\text{B}$ | $916\,\text{B}$ | $916\,\text{B}$ | $916\,\text{B}$ | **EXACT (PASS)** |
| **Static SRAM Footprint** | $61,944\,\text{Bytes}$ | N/A | N/A | N/A | N/A | $61,944\,\text{B}$ | **EXACT (PASS)** |
| **Compiled Flash Binary** | $330,153\,\text{Bytes}$ | N/A | N/A | N/A | N/A | $330,153\,\text{B}$ | **EXACT (PASS)** |
| **Constant Free Heap** | $237,452\,\text{Bytes}$ | N/A | N/A | N/A | N/A | $237,452\,\text{B}$ | **EXACT (PASS)** |
| **Dynamic Allocations** | $0\,\text{Bytes}$ | $0\,\text{B}$ | $0\,\text{B}$ | $0\,\text{B}$ | $0\,\text{B}$ | $0\,\text{B}$ | **EXACT (PASS)** |
| **Reciprocal Throughput Eq.** | $15,491.9\,\text{inf/sec}$ | N/A | N/A | $15,491.9$ | N/A | $15,491.9$ | **EXACT (PASS)** |

---

## 3. Historical Baseline Consistency Verification

In addition to physical hardware measurements, all historical algorithmic metrics from Phases 1–4 were verified:
* **Dataset Records:** $55,998$ total records ($40\%$ train, $40\%$ validation, $20\%$ test $= 11,200$ test records).
* **Paper 3 Cascaded Anomaly Screening:** $\theta^* = 0.05$, $99.98\%$ anomaly recall (only 2 false negatives out of 8,000 nominal test samples), $89.8\%$ nominal compute reduction, $26.36\%$ overall inference reduction.
* **Paper 4 Discrepancy Resolution:** 20 verified discrepancies across 4 defect modes, $+1.80\%$ optimistic test calibration bias.
* **Paper 2 Pareto Frontier:** 6 Pareto-optimal models out of 12 candidate architectures (sub-4 KB, sub-400 active MACs).

---

**NUMERICAL CONSISTENCY VERDICT: 100% PERFECT CONVERGENCE (ZERO DRIFT)**
