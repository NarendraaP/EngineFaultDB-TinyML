# Phase 3 — Scientific Audit & Verification Report

**Project:** QoS-Aware TinyML Runtime Research  
**Audit Scope:** Complete Phase 3 Preflight, Mode Selection, Runtime Simulator v1, and Policy Sensitivity Analysis  
**Audit Executed:** 2026-08-12  

---

## 1. Executive Summary & Audit Objective

A rigorous scientific audit of Phase 3 was conducted to inspect data pipelines, runtime decision logic, latency timing methodologies, threshold optimization procedures, and experimental claims. 

The audit evaluated **15 explicit checklist criteria** to ensure zero data leakage, uncompromised test-set independence, mathematical correctness of cascade metrics, and rigorous empirical bounds on timing claims.

---

## 2. Itemized Verification Results (15 Checklist Criteria)

### 1. Data Leakage
- **Inspection:** Evaluated `phase3_mode_selection.py` and `scripts/qos_runtime_simulator.py` for feature scaling and data split boundaries.
- **Finding:** The scaler (`scaler.pkl`) was fit **exclusively on the training split** (22,399 samples) during Phase 2. Both validation (22,399 samples) and test (11,200 samples) splits are transformed using the pre-fitted scaler. No global feature statistics (e.g. global mean/std or global min/max) are computed.
- **Verdict:** **PASS**

### 2. Test-Set Contamination
- **Inspection:** Verified whether training or hyperparameter optimization accessed the test set.
- **Finding:** Mode A binary models (`LogisticRegression`, `DecisionTreeClassifier`) were trained strictly on `X_train`. Depth selection ($d=3$ vs $d=5$) was evaluated on `X_val`. Test set `X_test` was kept strictly isolated until evaluation.
- **Verdict:** **PASS**

### 3. Ground-Truth Use in Runtime Routing
- **Inspection:** Examined runtime cascade trigger logic in `scripts/qos_runtime_simulator.py`.
- **Finding:** The runtime trigger condition is $\alpha_i = 1$ if $P(\text{anomalous}) \ge \theta$ else $0$. $P(\text{anomalous})$ is produced purely by `model_a.predict_proba(sample)` operating on input features $X$. The ground-truth label $y_i$ is **never referenced** during inference or routing, and is only accessed post-hoc to calculate accuracy, F1, and recall metrics.
- **Verdict:** **PASS**

### 4. Incorrect Binary Probability Interpretation
- **Inspection:** Checked binary classifier output index mapping for Mode A models.
- **Finding:** Inspected `model_a.classes_`, confirming class order `[0, 1]` where `0 = Normal` and `1 = Anomalous`. Thus, `predict_proba(sample)[0, 1]` unambiguously represents $P(\text{anomalous})$.
- **Verdict:** **PASS**

### 5. Incorrect Feature Ordering
- **Inspection:** Verified column ordering for reduced feature set (12 features) vs full feature set (14 features).
- **Finding:** `ALL_FEATURES` maintains original CSV column order without `Fault`. `REDUCED_FEATURES` excludes `"AFR"` and `"Speed"`. The column indices `[0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]` match the exact slicing applied during training of `scaler_reduced.pkl` and `mode_a_*_reduced.pkl`.
- **Verdict:** **PASS**

### 6. Wrong Scaler/Model Pairing
- **Inspection:** Checked feature inputs fed into Mode A and Mode B models.
- **Finding:** Mode A (`mode_a_dt5_binary_reduced.pkl`) receives 12 scaled features via `scaler.transform(X)[:, reduced_indices]`. Mode B (`mlp.pkl`) receives all 14 scaled features via `scaler.transform(X)`. Both models were trained on inputs transformed by `scaler.pkl`.
- **Verdict:** **PASS**

### 7. Latency Measurement Contamination
- **Inspection:** Analyzed timing methodology in `qos_runtime_simulator.py`.
- **Finding:** 2,000 warmup iterations were executed for both Mode A and Mode B prior to recording per-sample latency to eliminate cold-start/JIT overhead. Individual inferences were timed using `time.perf_counter_ns()` isolated around the model call.
- **Verdict:** **PASS**

### 8. Batch Inference Accidentally Used Instead of Single-Sample Inference
- **Inspection:** Inspected input array shapes during latency benchmarking and simulator execution.
- **Finding:** Inputs are sliced as `X[i:i+1]` producing shape `(1, 12)` for Mode A and `(1, 14)` for Mode B. Models process single samples sequentially, accurately modeling real-time ECU sensor sample processing.
- **Verdict:** **PASS**

### 9. Incorrect Deadline Calculations
- **Inspection:** Verified deadline thresholding units in `qos_runtime_simulator.py`.
- **Finding:** Total latency `total_lat_us` in microseconds ($\mu\text{s}$) is compared against deadline bounds converted to microseconds ($5\,\text{ms} = 5,000\,\mu\text{s}$, $10\,\text{ms} = 10,000\,\mu\text{s}$, etc.). Unit conversions are exact.
- **Verdict:** **PASS**

### 10. Incorrect Trigger-Rate Calculation
- **Inspection:** Verified Mode B activation rate calculation.
- **Finding:** Trigger rate is computed as $\text{mean}(\alpha) = \frac{1}{N} \sum_{i=1}^N \alpha_i$, representing the exact fraction of total samples routed to Mode B.
- **Verdict:** **PASS**

### 11. Incorrect Final Prediction Logic
- **Inspection:** Checked cascade output mapping in `qos_runtime_simulator.py`.
- **Finding:** Logic implemented:
  ```python
  final_pred = np.where(alpha == 0, 0, mode_b_preds)
  ```
  When Mode A flags Normal ($\alpha=0$), final output is 0 (Normal). When Mode A flags Anomalous ($\alpha=1$), Mode B is executed and its 4-class prediction ($0, 1, 2, 3$) is assigned as the final output.
- **Verdict:** **PASS**

### 12. Threshold-Selection Leakage
- **Initial Finding (IDENTIFIED & RESOLVED):** In initial draft scripts, policy sensitivity analysis calculated composite scores directly on the Test Set sweep (`qos_threshold_sweep.csv`), selecting $\theta^*$ from test set evaluations.
- **Remediation Implemented:** `scripts/qos_runtime_simulator.py` was updated to output separate validation (`qos_threshold_sweep_val.csv`) and test (`qos_threshold_sweep_test.csv`) sweeps. `scripts/qos_policy_sensitivity.py` was updated to perform threshold optimization and policy selection **strictly on the Validation set**, then evaluate the chosen $\theta^*$ on the held-out Test set.
- **Verdict:** **FIXED & VERIFIED PASS**

### 13. Reuse of the Test Set for Threshold Optimization
- **Initial Finding (IDENTIFIED & RESOLVED):** Addressed jointly with Criteria 12.
- **Remediation Implemented:** Threshold selection is now strictly driven by validation performance. Test set metrics are recorded purely for unbiased final reporting.
- **Verdict:** **FIXED & VERIFIED PASS**

### 14. Unsupported Claims of WCET
- **Inspection:** Checked text across all reports and scripts for WCET claims.
- **Finding:** All reports explicitly state that measured host latencies (`time.perf_counter_ns()` on x86_64) represent empirical host benchmarks and **do not constitute static Worst-Case Execution Time (WCET)** bounds.
- **Verdict:** **PASS**

### 15. Unsupported Claims of ECU Compatibility
- **Inspection:** Checked claims regarding microcontroller / embedded hardware execution.
- **Finding:** All reports explicitly disclaim embedded timing compliance, documenting that desktop PC latencies ($\sim 120\,\mu\text{s}$) cannot be extrapolated to microcontroller targets without on-target MCU profiling in Phase 4.
- **Verdict:** **PASS**

---

## 3. Unbiased Validation-Selected Threshold Results (Test Set Evaluation)

With threshold selection isolated strictly to the Validation Set, the resulting unbiased Test Set evaluations are:

| Policy Profile | Val Selected Threshold ($\theta^*$) | Val Score | Test Accuracy | Test Macro F1 | Test Anomaly FN Rate | Test Mean Latency | Test Trigger Rate |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Accuracy Priority** | **$\theta = 0.05$** | 0.8803 | 0.7464 | 0.7541 | **0.03%** | 124.61 $\mu$s | 73.6% |
| **Balanced** | **$\theta = 0.20$** | 0.6434 | 0.7446 | 0.7522 | **0.29%** | 123.19 $\mu$s | 71.9% |
| **Safety First** | **$\theta = 0.05$** | 0.7263 | 0.7464 | 0.7541 | **0.03%** | 124.61 $\mu$s | 73.6% |
| **Deadline Priority** | **$\theta = 1.00$** | 0.6500 | 0.4176 | 0.3535 | **76.72%** | 78.87 $\mu$s | 16.6% |

---

## 4. Final Audit Verdict

| Category | Verdict | Rationale / Verification |
| --- | --- | --- |
| **Leakage** | **PASS** | Scaler & models trained strictly on train split; zero test leakage. |
| **Reproducibility** | **PASS** | All scripts execute deterministically with fixed random seed (42). |
| **Runtime logic** | **PASS** | Cascade routing uses only input features via $P(\text{anomalous})$; label $y$ is isolated. |
| **Metrics** | **PASS** | Accuracy, macro F1, trigger rate, and FN rate formulas verified mathematically. |
| **Threshold selection** | **PASS** | Selected strictly on Validation Set sweep; evaluated on held-out Test Set. |
| **Timing methodology** | **PASS** | Single-sample input shapes, warmup iterations, isolated `perf_counter_ns()`; no WCET/ECU claims. |

### OVERALL PHASE 3 VERDICT: **PASS**

Phase 3 QoS-Aware TinyML Runtime Simulation & Policy Sensitivity Analysis is fully verified, scientifically sound, and approved for Phase 4 (TinyML Quantization & Embedded Profiling).

---
*End of Phase 3 Scientific Audit Report.*
