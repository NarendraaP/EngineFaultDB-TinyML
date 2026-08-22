# Paper 4 Evidence Map & Verification Traceability

**Paper Title:** *An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims*  
**Paper Directory:** [`papers/Paper4_TinyML_Verification/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/)  
**Primary Evidence Sources:** [`reports/Phase4_5_Independent_Verification.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase4_5_Independent_Verification.md), [`scripts/phase4_5_verification.py`](file:///d:/WiDe/EngineFaultDB-main/scripts/phase4_5_verification.py), [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv), [`reports/Phase3_Scientific_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase3_Scientific_Audit.md), [`reports/Phase5_Software_Runtime_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase5_Software_Runtime_Audit.md)  
**Date:** August 20, 2026  

---

## 1. Traceability Matrix of Verification Findings

| Verification Dimension | Specific Empirical Finding | Authoritative Source Artifact | Exact Location in Source | Evidence Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Data Isolation: Split Ratio** | Stratified $40\%$ train ($22,399$), $40\%$ val ($22,399$), $20\%$ test ($11,200$), `seed=42`. | `baseline_benchmark.py` | Lines 81–95 | **DIRECTLY VERIFIED** |
| **Data Isolation: Scaler Leakage** | `scaler.pkl` fitted strictly on train partition; transformed onto val and test. | `baseline_benchmark.py` | Line 114 | **DIRECTLY VERIFIED** |
| **Data Isolation: Threshold Leakage** | Threshold selected on validation (`qos_threshold_sweep_val.csv`) vs test set optimization bias ($+1.8\%$). | `reports/Phase3_Scientific_Audit.md` | Section 4 & 5 | **AUDIT OBSERVATION** |
| **Data Isolation: PTQ Calibration** | 100 representative samples sampled strictly from `X_train_full`. | `Phase4_5_Independent_Verification.md` | Section 8 | **DIRECTLY VERIFIED** |
| **Artifact Integrity: 20 Discrepancies** | 20 numerical discrepancies between in-memory training tables and verified disk binaries. | `Phase4_5_Independent_Verification.md` | Section 11 (Table of 20 items) | **DIRECTLY VERIFIED** |
| **Quantization: Tensor Inspection** | All 4 INT8 models verified as `FULL_INT8` ($0$ float32 tensors, $8$ int8 tensors). | `Phase4_5_Independent_Verification.md` | Section 4 & 5 | **DIRECTLY VERIFIED** |
| **Quantization: Operator Types** | Execution graph executes pure integer `FULLY_CONNECTED` and `SOFTMAX`. | `Phase4_5_Independent_Verification.md` | Section 4 | **DIRECTLY VERIFIED** |
| **Pruning: Zero Weights Count** | $0\%$ ($0$), $25\%$ ($95$), $50\%$ ($195$), $75\%$ ($298$ zeroes = $73.34\%$). | `Phase4_5_Independent_Verification.md` | Section 6 | **DIRECTLY VERIFIED** |
| **Pruning: Storage Decoupling** | $75\%$ pruning reduces MACs from $384$ to $96$, but FlatBuffer size remains $3,920$\,B (dense array). | `Phase4_5_Independent_Verification.md` | Section 6 | **DIRECTLY VERIFIED** |
| **Pruning: Terminology Fix** | Classified as *"computational sparsity without demonstrated storage compression"*. | `Phase4_5_Independent_Verification.md` | Section 6 & 12 | **AUDIT OBSERVATION** |
| **Computation: Active MACs** | $96, 160, 192, 288, 304, 352, 384$ classified as *"theoretical active MACs"*. | `Phase4_5_Independent_Verification.md` | Section 7 & 12 | **DERIVED** |
| **Timing: Host Benchmarking** | $100$ warmup iterations, $500$ measured single-sample iterations via `time.perf_counter_ns()`. | `Phase4_5_Independent_Verification.md` | Section 9 | **DIRECTLY VERIFIED** |
| **Timing: Terminology Fix** | Host timings ($0.82\,\mu\text{s}$ to $1.69\,\mu\text{s}$) classified as *"empirical host inference latency"*, not WCET. | `Phase4_5_Independent_Verification.md` | Section 9 & 12 | **LIMITATION / BOUNDARY** |
| **Runtime: Zero Ground-Truth Leakage** | `QoSScheduler.select_model()` takes `(deadline, workload, latency)` with zero access to label $y$. | `phase5/runtime/qos_runtime.py` | Lines 83–153 | **DIRECTLY VERIFIED** |
| **Hardware Claims: Evidence Taxonomy** | Strict separation of `[A] Host Empirical`, `[B] Simulation`, `[E] Auxiliary AVR`, `[F] Physical MCU`. | `reports/Phase5_Software_Runtime_Readiness.md` | Section 2 | **AUDIT OBSERVATION** |

---

## 2. Evidence Categorization Summary

- **DIRECTLY VERIFIED (Artifact-level re-computation):** 9 items (splits, scaler fitting, calibration data, 20 discrepancies, tensor graph types, operator types, zero weight counts, FlatBuffer file sizes, runtime routing inputs).
- **DERIVED (Mathematical deductions from verified artifacts):** 1 item (theoretical active MAC derivations).
- **AUDIT OBSERVATION (Methodological findings from empirical auditing):** 3 items (threshold leakage bias, pruning terminology correction, evidence separation taxonomy).
- **LIMITATION / BOUNDARY (Physical scope restrictions):** 2 items (host latency vs WCET, physical MCU absence).
