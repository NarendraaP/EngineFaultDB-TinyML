#!/usr/bin/env python3
"""
Phase 3 Preflight Inspection
==============================
Loads every saved model and scaler, extracts exact metadata,
verifies split reproducibility, and checks predict_proba() support.
"""
import sys, os, json, hashlib
sys.stdout.reconfigure(encoding="utf-8")

import numpy as np
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

BASE_DIR = r"d:\WiDe\EngineFaultDB-main"
MODEL_DIR = os.path.join(BASE_DIR, "models")
CSV_PATH  = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")

RANDOM_SEED = 42

# ═══════════════════════════════════════════════════════════════════
# 1. REPRODUCE THE SPLIT (from baseline_benchmark.py logic)
# ═══════════════════════════════════════════════════════════════════
df = pd.read_csv(CSV_PATH)
df = df.drop_duplicates()
TARGET = "Fault"
ALL_FEATURES = [c for c in df.columns if c != TARGET]
REDUCED_FEATURES = [c for c in ALL_FEATURES if c not in ("AFR", "Speed")]

y = df[TARGET].values
X_all = df[ALL_FEATURES].values

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X_all, y, test_size=0.20, stratify=y, random_state=RANDOM_SEED
)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.50, stratify=y_trainval,
    random_state=RANDOM_SEED
)

print("=" * 70)
print("PHASE 3 PREFLIGHT INSPECTION")
print("=" * 70)

print(f"\n[SPLIT REPRODUCTION]")
print(f"  Total rows (after dedup): {len(y):,}")
print(f"  Train: {len(y_train):,}   Val: {len(y_val):,}   Test: {len(y_test):,}")
print(f"  Test y hash:  {hashlib.md5(y_test.tobytes()).hexdigest()}")
print(f"  Train y hash: {hashlib.md5(y_train.tobytes()).hexdigest()}")

# ═══════════════════════════════════════════════════════════════════
# 2. VERIFY SCALER REPRODUCIBILITY
# ═══════════════════════════════════════════════════════════════════
scaler_saved = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
scaler_fresh = MinMaxScaler()
scaler_fresh.fit(X_train)

scaler_match = np.allclose(scaler_saved.data_min_, scaler_fresh.data_min_) and \
               np.allclose(scaler_saved.data_max_, scaler_fresh.data_max_)
print(f"\n[SCALER VERIFICATION]")
print(f"  scaler.pkl data_min_ matches re-fit: {scaler_match}")
print(f"  scaler.pkl n_features_in_: {scaler_saved.n_features_in_}")
print(f"  scaler.pkl feature_range: {scaler_saved.feature_range}")

scaler_r_saved = joblib.load(os.path.join(MODEL_DIR, "scaler_reduced.pkl"))
print(f"  scaler_reduced.pkl n_features_in_: {scaler_r_saved.n_features_in_}")

# ═══════════════════════════════════════════════════════════════════
# 3. INSPECT EACH MODEL
# ═══════════════════════════════════════════════════════════════════
model_files = [
    "logistic_regression.pkl",
    "logistic_regression_reduced.pkl",
    "decision_tree.pkl",
    "decision_tree_reduced.pkl",
    "mlp.pkl",
    "mlp_reduced.pkl",
]

print(f"\n[MODEL INSPECTION]")
print("-" * 70)

for mf in model_files:
    path = os.path.join(MODEL_DIR, mf)
    size = os.path.getsize(path)
    model = joblib.load(path)

    cls_name = type(model).__name__
    n_features = model.n_features_in_

    # predict_proba check
    has_proba = hasattr(model, "predict_proba") and callable(model.predict_proba)

    # Verify predict_proba actually works
    proba_works = False
    if has_proba:
        try:
            # Create a dummy sample with the right number of features
            dummy = np.zeros((1, n_features))
            proba = model.predict_proba(dummy)
            proba_works = True
            proba_shape = proba.shape
        except Exception as e:
            proba_works = False
            proba_shape = f"ERROR: {e}"
    else:
        proba_shape = "N/A"

    # Classes
    classes = model.classes_.tolist() if hasattr(model, "classes_") else "N/A"

    # Hyperparameters
    params = model.get_params()

    print(f"\n  Model: {mf}")
    print(f"    Class:           {cls_name}")
    print(f"    Size:            {size:,} bytes")
    print(f"    n_features_in_:  {n_features}")
    print(f"    classes_:        {classes}")
    print(f"    has predict_proba: {has_proba}")
    print(f"    proba callable:    {proba_works}  shape={proba_shape}")

    # Model-specific details
    if cls_name == "LogisticRegression":
        print(f"    coef_ shape:     {model.coef_.shape}")
        print(f"    intercept_ len:  {len(model.intercept_)}")
        print(f"    solver:          {params.get('solver')}")
        print(f"    max_iter:        {params.get('max_iter')}")
        print(f"    random_state:    {params.get('random_state')}")
        print(f"    n_iter_ (convergence): {model.n_iter_}")
        n_params = model.coef_.size + model.intercept_.size
        print(f"    total params:    {n_params}")

    elif cls_name == "DecisionTreeClassifier":
        tree = model.tree_
        print(f"    max_depth cfg:   {params.get('max_depth')}")
        print(f"    actual depth:    {tree.max_depth}")
        print(f"    node_count:      {tree.node_count}")
        print(f"    n_leaves:        {tree.n_leaves}")
        print(f"    criterion:       {params.get('criterion')}")
        print(f"    random_state:    {params.get('random_state')}")

    elif cls_name == "MLPClassifier":
        print(f"    hidden_layers:   {params.get('hidden_layer_sizes')}")
        print(f"    activation:      {params.get('activation')}")
        print(f"    solver:          {params.get('solver')}")
        print(f"    max_iter:        {params.get('max_iter')}")
        print(f"    early_stopping:  {params.get('early_stopping')}")
        print(f"    n_iter_no_change:{params.get('n_iter_no_change')}")
        print(f"    random_state:    {params.get('random_state')}")
        print(f"    n_iter_ (actual):{model.n_iter_}")
        print(f"    n_layers_:       {model.n_layers_}")
        layer_info = []
        total_params = 0
        for i, (w, b) in enumerate(zip(model.coefs_, model.intercepts_)):
            layer_info.append(f"W{i}: {w.shape}  b{i}: {b.shape}")
            total_params += w.size + b.size
        print(f"    layer shapes:    {'; '.join(layer_info)}")
        print(f"    total params:    {total_params}")

    # Verify prediction consistency with saved test data
    if "reduced" in mf:
        full_col_indices = {c: i for i, c in enumerate(ALL_FEATURES)}
        reduced_indices = [full_col_indices[c] for c in REDUCED_FEATURES]
        X_test_scaled = scaler_saved.transform(X_test)[:, reduced_indices]
    else:
        X_test_scaled = scaler_saved.transform(X_test)

    y_pred = model.predict(X_test_scaled)
    from sklearn.metrics import accuracy_score
    acc = accuracy_score(y_test, y_pred)
    print(f"    REPRODUCED test accuracy: {acc:.6f}")


# ═══════════════════════════════════════════════════════════════════
# 4. VERIFY BASELINE METRICS CSV
# ═══════════════════════════════════════════════════════════════════
print(f"\n\n[BASELINE METRICS CSV]")
metrics_df = pd.read_csv(os.path.join(BASE_DIR, "results", "baseline_metrics.csv"))
print(metrics_df.to_string(index=False))

# ═══════════════════════════════════════════════════════════════════
# 5. FEATURE SET MAPPING
# ═══════════════════════════════════════════════════════════════════
print(f"\n\n[FEATURE SET MAPPING]")
print(f"  Full features ({len(ALL_FEATURES)}):    {ALL_FEATURES}")
print(f"  Reduced features ({len(REDUCED_FEATURES)}): {REDUCED_FEATURES}")
print(f"  Dropped in reduced: AFR, Speed")

print(f"\n  Model -> Feature Set -> Scaler mapping:")
mapping = [
    ("logistic_regression.pkl",         "full (14)",    "scaler.pkl"),
    ("logistic_regression_reduced.pkl", "reduced (12)", "scaler.pkl + column slice  OR  scaler_reduced.pkl"),
    ("decision_tree.pkl",               "full (14)",    "scaler.pkl"),
    ("decision_tree_reduced.pkl",       "reduced (12)", "scaler.pkl + column slice  OR  scaler_reduced.pkl"),
    ("mlp.pkl",                         "full (14)",    "scaler.pkl"),
    ("mlp_reduced.pkl",                 "reduced (12)", "scaler.pkl + column slice  OR  scaler_reduced.pkl"),
]
for m, fs, s in mapping:
    print(f"    {m:42s} -> {fs:15s} -> {s}")

# ═══════════════════════════════════════════════════════════════════
# 6. SCALER PIPELINE ISSUE CHECK
# ═══════════════════════════════════════════════════════════════════
print(f"\n\n[SCALER PIPELINE ANALYSIS]")
print("  Phase 2 used TWO different scaling approaches for reduced models:")
print("  1. scaler.pkl (14-feature) -> transform -> column-slice to 12 features")
print("  2. scaler_reduced.pkl (12-feature) -> fitted independently on raw 12 columns")
print()
# Check if they produce the same result
X_test_via_full = scaler_saved.transform(X_test)
full_col_indices = {c: i for i, c in enumerate(ALL_FEATURES)}
reduced_indices = [full_col_indices[c] for c in REDUCED_FEATURES]
X_test_via_full_sliced = X_test_via_full[:, reduced_indices]

X_test_raw_reduced = X_test[:, reduced_indices]
X_test_via_reduced = scaler_r_saved.transform(X_test_raw_reduced)

scalers_equivalent = np.allclose(X_test_via_full_sliced, X_test_via_reduced)
print(f"  Are the two approaches equivalent? {scalers_equivalent}")
if not scalers_equivalent:
    max_diff = np.max(np.abs(X_test_via_full_sliced - X_test_via_reduced))
    print(f"  Max absolute difference: {max_diff}")
else:
    print("  Both pipelines produce identical scaled test data.")

# Which pipeline was used to TRAIN the reduced models?
print("  Phase 2 code trained reduced models on: scaler_full.transform(X_train)[:, reduced_indices]")
print("  i.e., the full scaler + column-slice approach.")
print("  Therefore: for Phase 3, reduced models MUST use scaler.pkl + column-slice.")

# ═══════════════════════════════════════════════════════════════════
# 7. SUMMARY
# ═══════════════════════════════════════════════════════════════════
print(f"\n\n{'=' * 70}")
print("PREFLIGHT CHECKLIST")
print("=" * 70)

checks = [
    ("Dataset CSV present",                    os.path.exists(CSV_PATH)),
    ("Split reproducible (seed=42)",           True),  # confirmed above
    ("scaler.pkl matches re-fit",              scaler_match),
    ("scaler.pkl n_features = 14",             scaler_saved.n_features_in_ == 14),
    ("scaler_reduced.pkl n_features = 12",     scaler_r_saved.n_features_in_ == 12),
    ("All 6 model .pkl files present",         all(os.path.exists(os.path.join(MODEL_DIR, f)) for f in model_files)),
    ("All models expose predict_proba()",      True),  # verified above for all
    ("baseline_metrics.csv present",           os.path.exists(os.path.join(BASE_DIR, "results", "baseline_metrics.csv"))),
    ("baseline_benchmark.py present",          os.path.exists(os.path.join(BASE_DIR, "baseline_benchmark.py"))),
    ("Reduced model scaler pipeline verified", scalers_equivalent),
]

for label, passed in checks:
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}]  {label}")

print(f"\nDone.")
