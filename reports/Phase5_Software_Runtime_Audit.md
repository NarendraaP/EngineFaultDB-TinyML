# Phase 5 Software Runtime Scientific Audit

**Date:** 2026-08-20
**Component:** Phase 5 QoS-Aware TinyML Runtime (Software Experiments)

This audit verifies the scientific integrity of the Phase 5 experimental code, ensuring correct methodology, proper data separation, and explicit distinction between host simulations and physical MCU measurements.

## Audit Checks

**1. No ground-truth routing**
*   **Check:** The `QoSScheduler.select_model()` must NOT access `y_test` or true labels. Ground truth is used ONLY in post-hoc `TraceFrame` evaluation.
*   **Verification:** `phase5/runtime/qos_runtime.py`, lines 83-154. The `select_model` function signature is `(self, deadline_ms: float, workload: WorkloadLevel, current_latency_us: float) -> Tuple[ExecutionMode, str]`. It does not accept or access true labels. In `phase5/simulator/trace_simulator.py`, lines 172-173, the ground truth is strictly used for post-hoc correctness evaluation: `true_label = int(y_test[i]); correct = (prediction == true_label)`.
*   **Status: PASS**

**2. No test-set selection leakage**
*   **Check:** The test set must use the same split as Phase 2/3.
*   **Verification:** `phase5/runtime/model_adapter.py`, line 131. The splitting logic precisely matches the requirements: `train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)`.
*   **Status: PASS**

**3. Correct model/scaler pairing**
*   **Check:** All models use `models/scaler.pkl` (MinMaxScaler, 14 features).
*   **Verification:** `phase5/runtime/model_adapter.py`, line 119. `DataPreprocessor` defaults to `scaler_path = 'models/scaler.pkl'` and applies it to testing samples (line 134) and single inferences (line 139).
*   **Status: PASS**

**4. Correct feature ordering**
*   **Check:** Features are `[c for c in df.columns if c != 'Fault']` matching Phase 2.
*   **Verification:** `phase5/runtime/model_adapter.py`, line 126. The extraction code is explicitly `feature_cols = [c for c in df.columns if c != 'Fault']`.
*   **Status: PASS**

**5. Correct model registry usage**
*   **Check:** Registry loads from `results/tinyml_model_profile_verified.csv`, Pareto models are correctly identified.
*   **Verification:** `phase5/run_phase5_pipeline.py`, line 62. The runtime correctly initializes the registry with `os.path.join(RESULT_DIR, "tinyml_model_profile_verified.csv")`. `phase5/runtime/model_registry.py` (line 89) properly filters by `pareto_status == 'PARETO_OPTIMAL'`.
*   **Status: PASS**

**6. No fabricated MCU measurements**
*   **Check:** All values labeled as HOST EMPIRICAL or TRACE-DRIVEN HOST SIMULATION, no claims of MCU/WCET/ECU.
*   **Verification:** `phase5/run_phase5_pipeline.py` lines 8-10 explicitly declare `All latency values are HOST EMPIRICAL — not MCU measurements. All ESP32-dependent measurements: STATUS = PENDING_PHYSICAL_ESP32`. The output CSVs hardcode `evidence_category` to `TRACE-DRIVEN HOST SIMULATION`.
*   **Status: PASS**

**7. Correct distinction between host and simulated timing**
*   **Check:** Evidence categories are explicitly separated.
*   **Verification:** `phase5/simulator/trace_simulator.py` (lines 8-9 and 108) heavily documents this. Generated files like `phase5_policy_comparison.csv` include column names like `avg_host_latency_us`, safely differentiating from MCU hardware latency.
*   **Status: PASS**

**8. Correct Pareto selection**
*   **Check:** The 6 Pareto-optimal models match the verified CSV.
*   **Verification:** `results/tinyml_model_profile_verified.csv` verifies exactly 6 models marked as `PARETO_OPTIMAL` (`pruned_mlp_14f_25pct`, `pruned_mlp_14f_50pct`, `pruned_mlp_14f_75pct`, `student_a_8_4_fp32`, `student_b_16_4_fp32`, `student_b_16_4_int8`). 
*   **Status: PASS**

**9. Reproducible workload generation**
*   **Check:** Workload uses `np.random.RandomState(seed)` for determinism.
*   **Verification:** `phase5/simulator/trace_simulator.py`, line 78 uses `rng = np.random.RandomState(seed)` in `generate_workload_sequence`.
*   **Status: PASS**

**10. Deterministic random seeds**
*   **Check:** `RANDOM_SEED=42` used throughout.
*   **Verification:** Used at the top of `phase5/simulator/trace_simulator.py` (line 28) and `phase5/run_phase5_pipeline.py` (line 38), and explicitly injected into dataset splits and workload generation.
*   **Status: PASS**

**11. Reproducible outputs**
*   **Check:** CSV files are generated deterministically.
*   **Verification:** `phase5/run_phase5_pipeline.py` outputs all `policy_comparison`, `traces`, and `ablation` CSVs using the fixed seeds without unpredictable iterations.
*   **Status: PASS**

## FINAL AUDIT VERDICT

*   **Count of PASS items:** 11
*   **Count of FAIL items:** 0
*   **Overall verdict: AUDIT_PASS**

The Phase 5 QoS-Aware Runtime software evaluation strictly adheres to the established scientific methodology. There is no label leakage to the routing logic, physical MCU numbers are properly deferred, and reproducible seeds and splits are perfectly maintained.
