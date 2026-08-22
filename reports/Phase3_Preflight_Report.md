# Phase 3 — Preflight Inspection Report

**Generated:** 2026-08-12 from live inspection of local project artifacts.  
**Method:** Every `.pkl` model and scaler loaded, queried, and verified against a fresh re-split of the dataset.  
**Script:** [`phase3_preflight.py`](../phase3_preflight.py)

---

## 1. Project Structure (Verified)

```
EngineFaultDB-main/
├── EngineFaultDB_Final.csv          5,334,236 B   ← primary dataset
├── LICENSE                             35,149 B   ← GPLv3
├── README.md                            5,786 B
├── audit_analysis.py                   15,279 B   ← Phase 1 script
├── baseline_benchmark.py               27,948 B   ← Phase 2 script
├── phase3_preflight.py                           ← this inspection script
├── Dataset_Audit_Report.md              5,395 B   ← Phase 1 output
├── correlation_heatmap.png            243,065 B
├── class_distribution.png              61,425 B
│
├── models/
│   ├── scaler.pkl                       1,223 B
│   ├── scaler_reduced.pkl               1,143 B
│   ├── logistic_regression.pkl          1,351 B
│   ├── logistic_regression_reduced.pkl  1,287 B
│   ├── decision_tree.pkl                5,609 B
│   ├── decision_tree_reduced.pkl        5,609 B
│   ├── mlp.pkl                         20,592 B
│   └── mlp_reduced.pkl                 22,336 B
│
├── results/
│   ├── baseline_metrics.csv               850 B
│   ├── confusion_matrix_logistic_regression.png
│   ├── confusion_matrix_logistic_regression_reduced.png
│   ├── confusion_matrix_decision_tree.png
│   ├── confusion_matrix_decision_tree_reduced.png
│   ├── confusion_matrix_mlp.png
│   └── confusion_matrix_mlp_reduced.png
│
└── reports/
    └── Baseline_Model_Report.md         7,666 B
```

---

## 2. Model Inventory (Loaded & Verified)

### 2.1 Logistic Regression — Full (14 features)

| Property | Value |
| --- | --- |
| File | `models/logistic_regression.pkl` |
| Class | `LogisticRegression` |
| Size | 1,351 B |
| n_features_in_ | 14 |
| classes_ | [0, 1, 2, 3] |
| coef_ shape | (4, 14) |
| intercept_ length | 4 |
| Total params | 60 |
| solver | lbfgs |
| max_iter | 2000 |
| random_state | 42 |
| Convergence iters | 157 |
| predict_proba() | **Yes — verified, returns (1, 4)** |
| Scaler | `scaler.pkl` |
| Reproduced test accuracy | **0.580000** ✓ |

### 2.2 Logistic Regression — Reduced (12 features)

| Property | Value |
| --- | --- |
| File | `models/logistic_regression_reduced.pkl` |
| Class | `LogisticRegression` |
| Size | 1,287 B |
| n_features_in_ | 12 |
| classes_ | [0, 1, 2, 3] |
| coef_ shape | (4, 12) |
| Total params | 52 |
| Convergence iters | 111 |
| predict_proba() | **Yes — verified** |
| Scaler | `scaler.pkl` → column-slice (indices for 12 features) |
| Reproduced test accuracy | **0.580536** ✓ |

### 2.3 Decision Tree — Full (14 features)

| Property | Value |
| --- | --- |
| File | `models/decision_tree.pkl` |
| Class | `DecisionTreeClassifier` |
| Size | 5,609 B |
| n_features_in_ | 14 |
| classes_ | [0, 1, 2, 3] |
| max_depth (config) | 5 |
| actual depth | 5 |
| node_count | 45 |
| n_leaves | 23 |
| criterion | gini |
| random_state | 42 |
| predict_proba() | **Yes — verified, returns (1, 4)** |
| Scaler | `scaler.pkl` |
| Reproduced test accuracy | **0.691607** ✓ |

### 2.4 Decision Tree — Reduced (12 features)

| Property | Value |
| --- | --- |
| File | `models/decision_tree_reduced.pkl` |
| Class | `DecisionTreeClassifier` |
| Size | 5,609 B |
| n_features_in_ | 12 |
| node_count | 45 |
| n_leaves | 23 |
| predict_proba() | **Yes — verified** |
| Scaler | `scaler.pkl` → column-slice |
| Reproduced test accuracy | **0.691696** ✓ |

### 2.5 MLP — Full (14 features)

| Property | Value |
| --- | --- |
| File | `models/mlp.pkl` |
| Class | `MLPClassifier` |
| Size | 20,592 B |
| n_features_in_ | 14 |
| classes_ | [0, 1, 2, 3] |
| hidden_layer_sizes | (16, 8) |
| activation | relu |
| solver | adam |
| max_iter | 500 |
| early_stopping | True (patience=20, val_frac=0.1) |
| Actual training iters | 100 (early-stopped) |
| n_layers_ | 4 (input → 16 → 8 → 4 output) |
| Layer shapes | W0:(14,16) b0:(16,) → W1:(16,8) b1:(8,) → W2:(8,4) b2:(4,) |
| Total params | 412 |
| predict_proba() | **Yes — verified, returns (1, 4)** |
| Scaler | `scaler.pkl` |
| Reproduced test accuracy | **0.746607** ✓ |

### 2.6 MLP — Reduced (12 features)

| Property | Value |
| --- | --- |
| File | `models/mlp_reduced.pkl` |
| Class | `MLPClassifier` |
| Size | 22,336 B |
| n_features_in_ | 12 |
| hidden_layer_sizes | (16, 8) |
| Actual training iters | 190 (early-stopped) |
| Layer shapes | W0:(12,16) b0:(16,) → W1:(16,8) b1:(8,) → W2:(8,4) b2:(4,) |
| Total params | 380 |
| predict_proba() | **Yes — verified** |
| Scaler | `scaler.pkl` → column-slice |
| Reproduced test accuracy | **0.739911** ✓ |

---

## 3. Scaler Verification

| Scaler File | n_features_in_ | feature_range | Matches Re-Fit |
| --- | --- | --- | --- |
| `scaler.pkl` | 14 | (0, 1) | **Yes** ✓ |
| `scaler_reduced.pkl` | 12 | (0, 1) | N/A (secondary) |

### Scaler Pipeline Finding

Phase 2 used **two different** approaches to create reduced-feature data:
1. `scaler.pkl` (14-feature) → transform → column-slice to 12 features ← **this is what trained the reduced models**
2. `scaler_reduced.pkl` (12-feature) → fitted independently on raw 12-column subset

**Both approaches produce identical output** (verified: `np.allclose` = True).  
This is mathematically guaranteed because MinMaxScaler operates column-independently.

**For Phase 3:** Either pipeline is valid, but `scaler.pkl` + column-slice is the canonical path since it matches training.

---

## 4. Feature Set Definitions

### Full Feature Set (14 features)

```
MAP, TPS, Force, Power, RPM, Consumption L/H, Consumption L/100KM,
Speed, CO, HC, CO2, O2, Lambda, AFR
```

### Reduced Feature Set (12 features)

```
MAP, TPS, Force, Power, RPM, Consumption L/H, Consumption L/100KM,
CO, HC, CO2, O2, Lambda
```

Removed: `AFR` (r=1.00 with Lambda), `Speed` (r=0.997 with RPM).

### Column Index Mapping (for programmatic slicing)

| Reduced Idx | Full Idx | Feature Name |
| --- | --- | --- |
| 0 | 0 | MAP |
| 1 | 1 | TPS |
| 2 | 2 | Force |
| 3 | 3 | Power |
| 4 | 4 | RPM |
| 5 | 5 | Consumption L/H |
| 6 | 6 | Consumption L/100KM |
| 7 | 8 | CO |
| 8 | 9 | HC |
| 9 | 10 | CO2 |
| 10 | 11 | O2 |
| 11 | 12 | Lambda |

Skipped full indices: 7 (Speed), 13 (AFR).

---

## 5. Split Reproducibility

| Property | Value |
| --- | --- |
| Random seed | 42 |
| Method | `train_test_split` × 2 (80/20 then 50/50) |
| Stratified | Yes (on `Fault`) |
| Total rows (after dedup) | 55,998 |
| Train | 22,399 (40.0%) |
| Val | 22,399 (40.0%) |
| Test | 11,200 (20.0%) |
| Test y hash (MD5) | `fb6086e48294b09da0a6b786f79562f0` |
| Train y hash (MD5) | `acada40b987b52229cf6a8f1f2036497` |

**The split is fully deterministic** and can be reproduced by re-running lines 59–93 of `baseline_benchmark.py`.

---

## 6. Reusable Code for Phase 3

| Component | Source | Reusable? | Notes |
| --- | --- | --- | --- |
| Data loading + dedup | `baseline_benchmark.py` L59–66 | ✓ Yes | Copy verbatim |
| Feature set definitions | `baseline_benchmark.py` L68–73 | ✓ Yes | `ALL_FEATURES`, `REDUCED_FEATURES` |
| Stratified split | `baseline_benchmark.py` L85–93 | ✓ Yes | Same seed = same split |
| Scaler loading | `joblib.load("models/scaler.pkl")` | ✓ Yes | Do NOT re-fit |
| Model loading | `joblib.load("models/<name>.pkl")` | ✓ Yes | Frozen artifacts |
| `predict_proba()` | All 6 models | ✓ Yes | Returns (n, 4) probability arrays |
| Latency measurement | `baseline_benchmark.py` L158–180 | ✓ Yes | `perf_counter_ns()` based |
| `evaluate_model()` | `baseline_benchmark.py` L183–221 | ✓ Yes | Full eval function |
| Confusion matrix plot | `baseline_benchmark.py` L224–235 | ✓ Yes | Seaborn heatmap |

---

## 7. predict_proba() Verification

| Model | predict_proba() | Output Shape | Output Type |
| --- | --- | --- | --- |
| logistic_regression.pkl | ✓ Works | (1, 4) | float64 |
| logistic_regression_reduced.pkl | ✓ Works | (1, 4) | float64 |
| decision_tree.pkl | ✓ Works | (1, 4) | float64 |
| decision_tree_reduced.pkl | ✓ Works | (1, 4) | float64 |
| mlp.pkl | ✓ Works | (1, 4) | float64 |
| mlp_reduced.pkl | ✓ Works | (1, 4) | float64 |

All models return calibrated (or at least consistent) class probability vectors that sum to 1.0. This enables confidence-based scheduling in Phase 3.

---

## 8. Preflight Checklist

| # | Prerequisite | Status |
| --- | --- | --- |
| 1 | Dataset CSV present | **PASS** ✓ |
| 2 | Split reproducible (seed=42) | **PASS** ✓ |
| 3 | `scaler.pkl` matches fresh re-fit | **PASS** ✓ |
| 4 | `scaler.pkl` n_features = 14 | **PASS** ✓ |
| 5 | `scaler_reduced.pkl` n_features = 12 | **PASS** ✓ |
| 6 | All 6 model `.pkl` files present | **PASS** ✓ |
| 7 | All models expose `predict_proba()` | **PASS** ✓ |
| 8 | `baseline_metrics.csv` present | **PASS** ✓ |
| 9 | `baseline_benchmark.py` present | **PASS** ✓ |
| 10 | Reduced-model scaler pipeline verified | **PASS** ✓ |

**Result: 10/10 PASS — all prerequisites satisfied for Phase 3.**

---

## 9. Issues Discovered

**None.** No implementation errors found. All saved models reproduce their Phase 2 accuracies exactly:

| Model | Phase 2 Reported | Preflight Reproduced | Match |
| --- | --- | --- | --- |
| LR full | 0.580000 | 0.580000 | ✓ |
| LR reduced | 0.580536 | 0.580536 | ✓ |
| DT full | 0.691607 | 0.691607 | ✓ |
| DT reduced | 0.691696 | 0.691696 | ✓ |
| MLP full | 0.746607 | 0.746607 | ✓ |
| MLP reduced | 0.739911 | 0.739911 | ✓ |

---

## 10. Next Step

The next command to execute is the Phase 3 QoS scheduler implementation script. Based on the verified artifacts:

```bash
python phase3_qos_scheduler.py
```

This script (to be created) should:
1. Load the frozen models from `models/*.pkl` (DO NOT retrain)
2. Load the frozen scaler from `models/scaler.pkl` (DO NOT re-fit)
3. Reproduce the test split using the same seed=42 logic
4. Use `predict_proba()` (confirmed available on all 6 models) for confidence-based routing
5. Implement the QoS scheduler with Mode A (MLP, accuracy priority) and Mode B (DT, latency priority)
6. Evaluate the scheduler on the untouched test set
7. Save results to `results/` and report to `reports/`

---

*End of preflight report.*
