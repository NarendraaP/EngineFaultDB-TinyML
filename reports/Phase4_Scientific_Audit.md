# Phase 4 — Scientific Audit Report

**Project:** QoS-Aware TinyML Runtime Research  
**Dataset:** EngineFaultDB (`EngineFaultDB_Final.csv`)  
**Audit Target:** Phase 4 — TinyML Optimization & Static Model Profiling  
**Evaluator:** Automated Rigorous Scientific Auditor  
**Date:** August 18, 2026  

---

## Audit Overview & Methodology

This scientific audit evaluates Phase 4 execution for data leakage, hyperparameter selection integrity, statistical rigor, artifact isolation, and claim validity. Phase 4 introduced neural baseline reference training (Keras MLP), TFLite FP32 conversion, INT8 post-training quantization (PTQ), feature reduction, structured pruning, knowledge distillation, central static model profiling, and 3-objective Pareto analysis.

---

## Detailed Scientific Audit Findings

### 1. Data Leakage & Test-Set Isolation
- **Verification:** Inspected `scripts/phase4_tinyml_optimization.py`. Dataset split reproduces Phase 2/3 stratified 40% train / 40% validation / 20% test split with random seed `42`.
- **Finding:** No test set samples (`X_test_full`, `X_test_red`) were accessed during Keras FP32 reference model training, PTQ representative calibration dataset generation, pruning threshold selection, or distillation loss calculation.
- **Verdict:** **PASS**

### 2. PTQ Representative Calibration Dataset Integrity
- **Verification:** Examined `convert_to_tflite_int8()` implementation. Calibration dataset generator `rep_data_gen()` yields samples from `X_train_full` (100 samples).
- **Finding:** Representative calibration dataset is drawn **exclusively** from training data (`X_train_full`). Zero test data or validation data samples were used for INT8 tensor range calibration.
- **Verdict:** **PASS**

### 3. Validation-Only Pruning Level Selection
- **Verification:** Inspected Stage 5 pruning loop logic. Pruning levels (0%, 25%, 50%, 75%) were fine-tuned on `X_train_full` and evaluated against `X_val_full`.
- **Finding:** Selection of optimal pruning configuration occurred strictly on `X_val_full` (Val Acc = 75.00% for 75% level). Held-out test set evaluation was performed **once** on finalized pruned models.
- **Verdict:** **PASS**

### 4. Validation-Only Distillation Hyperparameter & Student Architecture Selection
- **Verification:** Examined Stage 6 knowledge distillation pipeline. Student A (8,4) and Student B (16,4) were trained on `X_train_full` using soft teacher targets ($T=3.0, \alpha=0.5$).
- **Finding:** Selection of superior student architecture (`Student B (16,4)`) occurred strictly on `X_val_full` (Val Acc = 74.68%). Test evaluation was conducted ONCE on held-out test data.
- **Verdict:** **PASS**

### 5. Single-Pass Held-Out Test Evaluation
- **Verification:** Checked test evaluation calls across all 12 candidate models.
- **Finding:** Finalized TFLite FP32, INT8, pruned, and distilled models were evaluated exactly once on the held-out 20% test set (`X_test_full` / `X_test_red`, 11,200 samples) to report final metrics.
- **Verdict:** **PASS**

### 6. Single-Sample Inference Latency Measurement
- **Verification:** Inspected `eval_tflite_model()` timing loop implementation.
- **Finding:** Per-sample host inference latency (Mean, P50, P95, P99) was measured by passing single samples (`shape=(1, feature_count)`) through `interpreter.invoke()` one-by-one. No batching artifacts contaminated latency metrics.
- **Verdict:** **PASS**

### 7. Scaler and Model Pairing Rigor
- **Verification:** Verified scaler loading and transformation.
- **Finding:** Frozen Phase 2 `scaler.pkl` (fitted strictly on `X_train`) was used for all 14-feature models. Reduced 12-feature inputs (`X_train_red`, `X_val_red`, `X_test_red`) were derived via exact column index mapping (`reduced_indices`), preserving feature ordering and normalization contracts.
- **Verdict:** **PASS**

### 8. Feature Reduction Index Mapping Correctness
- **Verification:** Checked column removal logic for `AFR` and `Speed`.
- **Finding:** Feature reduction correctly excluded `AFR` and `Speed` while preserving relative column ordering for the remaining 12 features (`MAP`, `TPS`, `RPM`, `IAT`, `ECT`, `Lambda`, `Fuel_Press`, `Oil_Press`, `Vibat_V`, `Vibat_H`, `Knock`, `EGT`).
- **Verdict:** **PASS**

### 9. Phase 3 Freeze Maintenance
- **Verification:** Inspected `models/`, `results/`, `reports/`, and Phase 3 simulator scripts.
- **Finding:** All Phase 3 models, scalers, thresholds, simulator logic, and audit reports remained 100% untouched and frozen. Phase 4 operated strictly as an independent experimental layer.
- **Verdict:** **PASS**

### 10. Measured vs Estimated Metric Labeling
- **Verification:** Inspected `results/tinyml_model_profile.csv` headers and report tables.
- **Finding:** Metrics are clearly demarcated. Accuracy, Macro F1, Model File Size (Bytes), Host Latency (μs), and MACs are explicitly labeled as measured/calculated metrics, while SRAM memory footprints are explicitly labeled as static estimates.
- **Verdict:** **PASS**

### 11. Validity of Timing & Hardware Claims
- **Verification:** Reviewed Phase 4 report text and code comments for unsupported timing assertions.
- **Finding:** Report explicitly states that host latencies measured on an x86_64 CPU **cannot** be claimed as MCU execution cycles, WCET bounds, or embedded deadline compliance.
- **Verdict:** **PASS**

### 12. Artifact Generation & Cross-Verification
- **Verification:** Checked filesystem for output CSVs and PNG figures.
- **Finding:** `results/tinyml_model_profile.csv`, `results/fp32_reference_metrics.csv`, and all 6 figures (`figures/fp32_vs_int8_accuracy.png`, `figures/accuracy_vs_model_size.png`, `figures/f1_vs_model_size.png`, `figures/accuracy_vs_macs.png`, `figures/accuracy_vs_latency.png`, `figures/pareto_frontier.png`) are verified complete on disk.
- **Verdict:** **PASS**

### 13. Reproducibility & Environment Documentation
- **Verification:** Verified script execution reproducibility.
- **Finding:** All random seeds (`np.random.seed(42)`, `tf.random.set_seed(42)`, `train_test_split(random_state=42)`) are explicitly fixed. Full environment specifications (Python 3.13.4, TensorFlow 2.21.0, scikit-learn 1.9.0) are fully documented.
- **Verdict:** **PASS**

---

## Final Scientific Audit Summary Matrix

| Criterion | Audit Category | Result | Key Evidence / Notes |
| :--- | :--- | :---: | :--- |
| **1. Data Leakage** | Test-Set Isolation | **PASS** | Test set never accessed during training/PTQ/pruning/distillation. |
| **2. PTQ Calibration** | Quantization Rigor | **PASS** | Calibration dataset drawn 100% from `X_train_full`. |
| **3. Pruning Selection** | Validation Integrity | **PASS** | Pruning level (75%) selected strictly on `X_val_full`. |
| **4. Distillation Selection**| Validation Integrity | **PASS** | Student architecture (16,4) selected strictly on `X_val_full`. |
| **5. Test Evaluation** | Held-Out Single Pass | **PASS** | Held-out test set evaluated ONCE on finalized models. |
| **6. Latency Benchmark** | Single-Sample Benchmark| **PASS** | Single-sample input tensors used for latency profiling. |
| **7. Scaler Pairing** | Transformation Rigor | **PASS** | `scaler.pkl` used for all transformations. |
| **8. Feature Reduction** | Feature Mapping | **PASS** | Exact column indexing maintained for 14f and 12f sets. |
| **9. Phase 3 Freeze** | Project Isolation | **PASS** | Phase 1–3 artifacts kept 100% frozen. |
| **10. Metric Labeling** | Transparency | **PASS** | Measured vs estimated metrics explicitly distinguished. |
| **11. Hardware Claims** | Scientific Validity | **PASS** | No unsupported WCET or real-time MCU claims made. |
| **12. Artifact Integrity** | Deliverable Completeness | **PASS** | All CSVs and 6 figures verified on disk. |
| **13. Reproducibility** | Experimental Rigor | **PASS** | Seed 42 fixed; full script reproducible end-to-end. |

---

### **OVERALL PHASE 4 SCIENTIFIC AUDIT VERDICT: PASSED (13/13 CRITERIA)**
