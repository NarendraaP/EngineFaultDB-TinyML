# Phase 20 — Cross-Paper Claim Provenance Matrix

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** Claim-to-Evidence Mapping Across Papers 1–5  
**Date:** August 29, 2026  

---

## 1. Objective

This matrix maps every major empirical claim across Papers 1–5 to its authoritative evidence artifact, classifying the evidence tier and verifying that the phrasing strictly complies with scientific boundaries.

---

## 2. Claim Provenance Matrix

| # | Paper | Core Scientific Claim | Authoritative Evidence Source | Evidence Tier | Allowed / Verified Wording | Audit Status |
|---|---|---|---|---|---|---|
| 1 | **P1** | Single-model INT8 inference latencies ($64.55\text{--}89.90\,\si{\micro\second}$) are well below cyber-physical deadlines ($5\text{--}100\,\text{ms}$). | `esp32_full_benchmark.json` | **Tier 1 (Direct Physical Measurement)** | "Observed isolated model latencies are substantially below the evaluated 5–100 ms deadlines under tested firmware conditions." | **VERIFIED PASS** |
| 2 | **P1** | Dynamic QoS policies switch models under simulated contention to avoid deadline violations. | `results/phase5_policy_comparison.csv` | **Tier 3 (Trace-Driven Host Simulation)** | "Evaluated via trace-driven simulation across 80 configurations with synthetic workload multipliers." | **VERIFIED PASS** |
| 3 | **P2** | Pruning and distillation yield 6 Pareto-optimal models with sub-4 KB Flash and sub-400 active MACs. | `results/tinyml_model_profile_verified.csv` | **Tier 2 (Disk Artifact Inspection)** | "Multi-objective Pareto frontier across Accuracy, Serialized Binary Size, and Theoretical Active MACs." | **VERIFIED PASS** |
| 4 | **P2** | Compression delivers physical execution speedup on microcontroller hardware ($28.20\%$). | `esp32_full_benchmark.json` | **Tier 1 (Direct Physical Measurement)** | "Physical on-device profiling confirms that compression delivers genuine execution speedups (28.20% lower physical latency for student_a relative to uncompressed mlp_14f)." | **VERIFIED PASS** |
| 5 | **P3** | Two-stage cascade screening achieves $99.98\%$ anomaly recall with $89.8\%$ nominal compute reduction. | `results/phase3_gating_evaluation.csv` | **Tier 2 (Host Test-Set Evaluation)** | "Stage-1 screening model rejects 89.8% of nominal records while maintaining 99.98% anomaly recall at theta*=0.05." | **VERIFIED PASS** |
| 6 | **P3** | Stage-1 screening model executes in $64.55\,\si{\micro\second}$ on ESP32 silicon. | `esp32_full_benchmark.json` | **Tier 1 (Direct Physical Measurement)** | "At an isolated mean execution latency of 64.55 us, the Stage-1 classifier achieves a single-sample compute equivalent of 15,491.9 inf/sec." | **VERIFIED PASS** |
| 7 | **P4** | 20 numerical discrepancies exist between training-time reports and verified disk binaries across 4 defect modes. | `reports/Phase4_Discrepancy_Audit.md` | **Tier 2 (Artifact Audit)** | "Audited and resolved 20 distinct numerical discrepancies across four defect modes with metric variances up to 7.82%." | **VERIFIED PASS** |
| 8 | **P4** | Direct test-set threshold calibration introduces an artificial $+1.80\%$ optimistic accuracy bias. | `results/phase4_5_calibration_bias.csv` | **Tier 2 (Empirical Evaluation)** | "Evaluating gating thresholds directly on test data introduces an artificial +1.80% optimistic accuracy bias, demonstrating the necessity of split-isolated calibration." | **VERIFIED PASS** |
| 9 | **P5** | On-device single-sample latency scales monotonically with parameter count ($R^2 = 0.963$) from $64.55\,\si{\micro\second}$ to $89.90\,\si{\micro\second}$. | `esp32_full_benchmark.json` ($N=24,000$) | **Tier 1 (Direct Physical Measurement)** | "Isolated on-device latency scales strictly monotonically with parameter count (R^2 = 0.963) from 64.55 us (176 params) to 89.90 us (412 params)." | **VERIFIED PASS** |
| 10 | **P5** | Host x86_64 profiling underestimates microcontroller latency by $62.87\times\text{--}76.77\times$ and exhibits sub-microsecond rank inversions. | `esp32_full_benchmark.json` vs host profile | **Tier 1 (Comparative Measurement)** | "Host x86_64 profiling underestimates physical MCU execution latency by 62.87x to 76.77x and introduces sub-microsecond rank inversions unmasked on silicon." | **VERIFIED PASS** |
| 11 | **P5** | TFLM commits exactly $916\,\text{Bytes}$ of tensor arena memory with zero dynamic allocations and zero heap leak across $25,200$ runs. | `phase5/firmware/src/main.cpp` serial log | **Tier 1 (Direct Physical Measurement)** | "TensorFlow Lite Micro commits exactly 916 Bytes of static tensor arena memory with zero dynamic heap allocations across 25,200 executions." | **VERIFIED PASS** |

---

## 3. Evidence Tier Classification Summary

* **Tier 1 (Direct Physical Hardware Measurement):** $24,000$ on-device ESP32 inferences, memory footprints, hardware timer timestamps, and host-vs-silicon comparative profiles.
* **Tier 2 (Disk Artifact & Test-Set Evaluation):** FlatBuffer graph parsing, parameter counts, binary file sizes, and split-isolated classification metrics on EngineFaultDB ($N=11,200$).
* **Tier 3 (Trace-Driven Host Simulation):** QoS multi-model scheduling and workload contention simulation across 80 configurations.
* **Tier 4 (Derived Analytical Models):** Linear parameter regressions ($R^2 = 0.963$), reciprocal compute equivalents, and theoretical MAC formulas.

---

**CLAIM PROVENANCE VERDICT: 100% TRACEABLE AND METHODOLOGICALLY SOUND**
