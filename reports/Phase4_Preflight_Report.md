# Phase 4 — Project Pre-Flight Verification Report

**Project:** QoS-Aware TinyML Runtime Research  
**Phase:** Phase 4 — TinyML Optimization & Static Model Profiling  
**Date:** 2026-08-18  

---

## 1. Executive Summary & Freeze Declaration

Phase 1, Phase 2, and Phase 3 of the QoS-Aware TinyML Runtime research project have been successfully completed and audited. 

> [!IMPORTANT]
> **PHASE 3 IS FROZEN.**  
> None of the Phase 3 models, scalers, preflight scripts, mode selection reports, simulator scripts, or audit reports will be modified, deleted, or overwritten during Phase 4. All Phase 4 experiments build strictly on top of these frozen artifacts as a new experimental layer.

---

## 2. Inventory & Verification of Existing Artifacts

### 2.1 Primary Dataset
- **`EngineFaultDB_Final.csv`** — 55,998 rows, 15 columns (14 features + 1 target `Fault`), 5,334,236 bytes. Verified intact.

### 2.2 Model & Scaler Artifacts (`models/`)

| Artifact Name | Path | File Size | Class / Type | Input Features | Hyperparameters / Structure |
| --- | --- | --- | --- | --- | --- |
| `scaler.pkl` | `models/scaler.pkl` | 1,223 B | `MinMaxScaler` | 14 | Scale range $[0, 1]$, fit on Train set |
| `scaler_reduced.pkl` | `models/scaler_reduced.pkl` | 1,143 B | `MinMaxScaler` | 12 | Scale range $[0, 1]$, fit on Train set (no AFR/Speed) |
| `mlp.pkl` | `models/mlp.pkl` | 20,592 B | `MLPClassifier` | 14 | (16, 8) hidden layers, ReLU, Adam, max_iter=500 |
| `mlp_reduced.pkl` | `models/mlp_reduced.pkl` | 22,336 B | `MLPClassifier` | 12 | (16, 8) hidden layers, ReLU, Adam, max_iter=500 |
| `decision_tree.pkl` | `models/decision_tree.pkl` | 5,609 B | `DecisionTreeClassifier` | 14 | `max_depth=5`, random_state=42 |
| `decision_tree_reduced.pkl` | `models/decision_tree_reduced.pkl` | 5,609 B | `DecisionTreeClassifier` | 12 | `max_depth=5`, random_state=42 |
| `logistic_regression.pkl` | `models/logistic_regression.pkl` | 1,351 B | `LogisticRegression` | 14 | `max_iter=2000`, solver=`lbfgs`, random_state=42 |
| `logistic_regression_reduced.pkl` | `models/logistic_regression_reduced.pkl` | 1,287 B | `LogisticRegression` | 12 | `max_iter=2000`, solver=`lbfgs`, random_state=42 |
| `mode_a_dt5_binary_reduced.pkl` | `models/mode_a_dt5_binary_reduced.pkl` | 4,393 B | `DecisionTreeClassifier` | 12 | `max_depth=5`, binary screening (Normal vs Anomaly) |
| `mode_a_dt5_binary_full.pkl` | `models/mode_a_dt5_binary_full.pkl` | 4,393 B | `DecisionTreeClassifier` | 14 | `max_depth=5`, binary screening |
| `mode_a_dt3_binary_reduced.pkl` | `models/mode_a_dt3_binary_reduced.pkl` | 2,473 B | `DecisionTreeClassifier` | 12 | `max_depth=3`, binary screening |
| `mode_a_dt3_binary_full.pkl` | `models/mode_a_dt3_binary_full.pkl` | 2,473 B | `DecisionTreeClassifier` | 14 | `max_depth=3`, binary screening |
| `mode_a_lr_binary_reduced.pkl` | `models/mode_a_lr_binary_reduced.pkl` | 959 B | `LogisticRegression` | 12 | Binary screening |
| `mode_a_lr_binary_full.pkl` | `models/mode_a_lr_binary_full.pkl` | 975 B | `LogisticRegression` | 14 | Binary screening |

### 2.3 Result Files (`results/`)
- `baseline_metrics.csv` (850 B) — Phase 2 baseline model metrics.
- `mode_selection_metrics.csv` (1,511 B) — Phase 3 Mode A/B candidate metrics.
- `qos_sample_trace.csv` (577,780 B) — Phase 3 11,200-sample test trace at $\theta=0.50$.
- `qos_threshold_sweep.csv` (2,344 B) — Phase 3 test-set threshold sweep.
- `qos_threshold_sweep_val.csv` (2,463 B) — Phase 3 validation-set threshold sweep.
- `qos_threshold_sweep_test.csv` (2,344 B) — Phase 3 held-out test-set threshold sweep.
- `qos_deadline_sweep.csv` (6,566 B) — Phase 3 deadline compliance sweep.
- `qos_policy_sensitivity.csv` (9,246 B) — Phase 3 policy sensitivity data.

### 2.4 Report Files (`reports/`)
- `Dataset_Audit_Report.md` — Phase 1 complete dataset audit.
- `Baseline_Model_Report.md` — Phase 2 baseline benchmarking report.
- `Phase3_Preflight_Report.md` — Phase 3 preflight verification report.
- `Phase3_Mode_Selection_Report.md` — Phase 3 Mode A/B selection report.
- `Phase3_QoS_Runtime_Report.md` — Phase 3 simulator v1 report.
- `Phase3_QoS_Policy_Analysis.md` — Phase 3 policy sensitivity report.
- `Phase3_Scientific_Audit.md` — Phase 3 scientific audit report (PASS on all 6 categories).

---

## 3. Environment & Package Versions

- **Python Version:** 3.13.4 (`64-bit AMD64`)
- **scikit-learn:** 1.9.0
- **joblib:** 1.5.3
- **pandas:** 3.0.5
- **numpy:** 2.3.1
- **Operating System:** Windows

---

## 4. Reproducibility Configuration

- **Random Seed:** 42 (fixed across all splits, initializations, and model training).
- **Split Ratio:** Stratified 40% Train (22,399) / 40% Val (22,399) / 20% Test (11,200).
- **Feature Sets:**
  - Full: 14 features (`Speed`, `RPM`, `AFR`, `TPS`, `MAP`, `IAT`, `ECT`, `Lambda`, `OilPress`, `FuelPress`, `Knock`, `Vibration`, `EGT`, `EGR`).
  - Reduced: 12 features (excluding `AFR` and `Speed`).

---

## 5. Pre-Flight Verification Verdict

**VERDICT: ALL PHASE 2 & 3 ARTIFACTS PRESENT AND VERIFIED INTACT (100% PASS).**  
Phase 4 experimental execution is cleared to proceed.
