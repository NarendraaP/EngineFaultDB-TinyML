#!/usr/bin/env python3
"""
Phase 3 — Mode A / Mode B Candidate Analysis
===============================================
Trains binary screening classifiers (Mode A) and evaluates existing
multiclass models (Mode B).  Does NOT implement the scheduler.

Run:  python phase3_mode_selection.py
"""

import sys, os, time, warnings
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix,
    roc_auc_score, average_precision_score, roc_curve, precision_recall_curve,
)
from sklearn.base import clone

# ═══════════════════════════════════════════════════════════════════
# CONFIG (must match Phase 2 exactly)
# ═══════════════════════════════════════════════════════════════════
RANDOM_SEED    = 42
LATENCY_WARMUP = 1000
LATENCY_ITERS  = 5000

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CSV_PATH   = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")
MODEL_DIR  = os.path.join(BASE_DIR, "models")
RESULT_DIR = os.path.join(BASE_DIR, "results")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

for d in [MODEL_DIR, RESULT_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════
# 1. REPRODUCE PHASE 2 SPLIT (verbatim from baseline_benchmark.py)
# ═══════════════════════════════════════════════════════════════════
print("=" * 70)
print("Phase 3 — Mode A / Mode B Candidate Analysis")
print("=" * 70)

df = pd.read_csv(CSV_PATH)
df = df.drop_duplicates()

TARGET = "Fault"
ALL_FEATURES = [c for c in df.columns if c != TARGET]
REDUCED_FEATURES = [c for c in ALL_FEATURES if c not in ("AFR", "Speed")]

full_col_indices = {c: i for i, c in enumerate(ALL_FEATURES)}
reduced_indices  = [full_col_indices[c] for c in REDUCED_FEATURES]

y = df[TARGET].values
X_all = df[ALL_FEATURES].values

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X_all, y, test_size=0.20, stratify=y, random_state=RANDOM_SEED
)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.50, stratify=y_trainval,
    random_state=RANDOM_SEED
)

print(f"Split: Train={len(y_train):,}  Val={len(y_val):,}  Test={len(y_test):,}")

# Load the Phase 2 scaler (DO NOT re-fit)
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
X_train_full = scaler.transform(X_train)
X_val_full   = scaler.transform(X_val)
X_test_full  = scaler.transform(X_test)

X_train_reduced = X_train_full[:, reduced_indices]
X_val_reduced   = X_val_full[:, reduced_indices]
X_test_reduced  = X_test_full[:, reduced_indices]

# ═══════════════════════════════════════════════════════════════════
# 2. CREATE BINARY TARGET: Fault 0 = Normal (0), Fault 1/2/3 = Anomalous (1)
# ═══════════════════════════════════════════════════════════════════
y_train_bin = (y_train > 0).astype(int)
y_val_bin   = (y_val > 0).astype(int)
y_test_bin  = (y_test > 0).astype(int)

print(f"\nBinary target distribution:")
for name, yb in [("Train", y_train_bin), ("Val", y_val_bin), ("Test", y_test_bin)]:
    n0, n1 = np.sum(yb == 0), np.sum(yb == 1)
    print(f"  {name}: Normal={n0} ({n0/len(yb)*100:.1f}%)  Anomalous={n1} ({n1/len(yb)*100:.1f}%)")


# ═══════════════════════════════════════════════════════════════════
# 3. LATENCY HELPER
# ═══════════════════════════════════════════════════════════════════
def measure_latency(model, single_sample, warmup=LATENCY_WARMUP, n_iter=LATENCY_ITERS):
    for _ in range(warmup):
        model.predict(single_sample)
    latencies_ns = []
    for _ in range(n_iter):
        t0 = time.perf_counter_ns()
        model.predict(single_sample)
        t1 = time.perf_counter_ns()
        latencies_ns.append(t1 - t0)
    lat = np.array(latencies_ns, dtype=np.float64)
    return {
        "mean_us": np.mean(lat) / 1e3,
        "p50_us":  np.percentile(lat, 50) / 1e3,
        "p95_us":  np.percentile(lat, 95) / 1e3,
        "p99_us":  np.percentile(lat, 99) / 1e3,
    }

def measure_proba_latency(model, single_sample, warmup=LATENCY_WARMUP, n_iter=LATENCY_ITERS):
    for _ in range(warmup):
        model.predict_proba(single_sample)
    latencies_ns = []
    for _ in range(n_iter):
        t0 = time.perf_counter_ns()
        model.predict_proba(single_sample)
        t1 = time.perf_counter_ns()
        latencies_ns.append(t1 - t0)
    lat = np.array(latencies_ns, dtype=np.float64)
    return {
        "mean_us": np.mean(lat) / 1e3,
        "p50_us":  np.percentile(lat, 50) / 1e3,
        "p95_us":  np.percentile(lat, 95) / 1e3,
        "p99_us":  np.percentile(lat, 99) / 1e3,
    }

# ═══════════════════════════════════════════════════════════════════
# 4. TRAIN MODE A BINARY CLASSIFIERS
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'─' * 70}")
print("TRAINING MODE A BINARY CLASSIFIERS")
print(f"{'─' * 70}")

mode_a_specs = [
    # --- Full feature set (14) ---
    {
        "name": "LR Binary (full)",
        "short": "lr_binary_full",
        "fset": "full",
        "model": LogisticRegression(max_iter=2000, solver="lbfgs",
                                     random_state=RANDOM_SEED, n_jobs=-1),
        "X_train": X_train_full, "X_val": X_val_full, "X_test": X_test_full,
        "n_features": 14,
    },
    {
        "name": "DT Binary d=3 (full)",
        "short": "dt3_binary_full",
        "fset": "full",
        "model": DecisionTreeClassifier(max_depth=3, random_state=RANDOM_SEED),
        "X_train": X_train_full, "X_val": X_val_full, "X_test": X_test_full,
        "n_features": 14,
    },
    {
        "name": "DT Binary d=5 (full)",
        "short": "dt5_binary_full",
        "fset": "full",
        "model": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_SEED),
        "X_train": X_train_full, "X_val": X_val_full, "X_test": X_test_full,
        "n_features": 14,
    },
    # --- Reduced feature set (12) ---
    {
        "name": "LR Binary (reduced)",
        "short": "lr_binary_reduced",
        "fset": "reduced",
        "model": LogisticRegression(max_iter=2000, solver="lbfgs",
                                     random_state=RANDOM_SEED, n_jobs=-1),
        "X_train": X_train_reduced, "X_val": X_val_reduced, "X_test": X_test_reduced,
        "n_features": 12,
    },
    {
        "name": "DT Binary d=3 (reduced)",
        "short": "dt3_binary_reduced",
        "fset": "reduced",
        "model": DecisionTreeClassifier(max_depth=3, random_state=RANDOM_SEED),
        "X_train": X_train_reduced, "X_val": X_val_reduced, "X_test": X_test_reduced,
        "n_features": 12,
    },
    {
        "name": "DT Binary d=5 (reduced)",
        "short": "dt5_binary_reduced",
        "fset": "reduced",
        "model": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_SEED),
        "X_train": X_train_reduced, "X_val": X_val_reduced, "X_test": X_test_reduced,
        "n_features": 12,
    },
]

mode_a_results = []

for spec in mode_a_specs:
    model = clone(spec["model"])
    print(f"\n  Training {spec['name']}...", end=" ", flush=True)
    t0 = time.perf_counter()
    model.fit(spec["X_train"], y_train_bin)
    train_time = time.perf_counter() - t0
    print(f"done ({train_time:.3f}s)")

    # --- Validation metrics ---
    y_val_pred = model.predict(spec["X_val"])
    y_val_proba = model.predict_proba(spec["X_val"])[:, 1]
    val_acc = accuracy_score(y_val_bin, y_val_pred)
    val_f1  = f1_score(y_val_bin, y_val_pred, average="macro")
    val_roc = roc_auc_score(y_val_bin, y_val_proba)
    val_pr  = average_precision_score(y_val_bin, y_val_proba)

    # --- Test metrics (held out) ---
    y_test_pred = model.predict(spec["X_test"])
    y_test_proba = model.predict_proba(spec["X_test"])[:, 1]
    test_acc  = accuracy_score(y_test_bin, y_test_pred)
    test_prec = precision_score(y_test_bin, y_test_pred)
    test_rec  = recall_score(y_test_bin, y_test_pred)
    test_f1   = f1_score(y_test_bin, y_test_pred, average="macro")
    test_roc  = roc_auc_score(y_test_bin, y_test_proba)
    test_pr   = average_precision_score(y_test_bin, y_test_proba)
    test_cm   = confusion_matrix(y_test_bin, y_test_pred)

    # Per-class detail
    cr = classification_report(y_test_bin, y_test_pred, output_dict=True,
                                target_names=["Normal", "Anomalous"], zero_division=0)

    # Latency (predict and predict_proba)
    single = spec["X_test"][0:1]
    lat_pred  = measure_latency(model, single)
    lat_proba = measure_proba_latency(model, single)

    # Model size
    model_path = os.path.join(MODEL_DIR, f"mode_a_{spec['short']}.pkl")
    joblib.dump(model, model_path)
    model_size = os.path.getsize(model_path)

    # Param count
    cls_name = type(model).__name__
    if cls_name == "LogisticRegression":
        n_params = model.coef_.size + model.intercept_.size
    elif cls_name == "DecisionTreeClassifier":
        n_params = model.tree_.node_count
    else:
        n_params = -1

    result = {
        "name": spec["name"],
        "short": spec["short"],
        "fset": spec["fset"],
        "n_features": spec["n_features"],
        "class": cls_name,
        "n_params": n_params,
        "model_size_bytes": model_size,
        "train_time_s": train_time,
        "val_acc": val_acc,
        "val_f1": val_f1,
        "val_roc_auc": val_roc,
        "val_pr_auc": val_pr,
        "test_acc": test_acc,
        "test_prec": test_prec,
        "test_rec": test_rec,
        "test_f1": test_f1,
        "test_roc_auc": test_roc,
        "test_pr_auc": test_pr,
        "test_cm": test_cm,
        "class_report": cr,
        "lat_predict": lat_pred,
        "lat_proba": lat_proba,
        "model_obj": model,
        "y_test_proba": y_test_proba,
    }
    mode_a_results.append(result)
    print(f"    Val:  Acc={val_acc:.4f}  F1={val_f1:.4f}  ROC-AUC={val_roc:.4f}")
    print(f"    Test: Acc={test_acc:.4f}  F1={test_f1:.4f}  ROC-AUC={test_roc:.4f}  PR-AUC={test_pr:.4f}")
    print(f"    Lat(predict): {lat_pred['mean_us']:.1f} us   Lat(proba): {lat_proba['mean_us']:.1f} us")
    print(f"    Size: {model_size:,} B   Params: {n_params}")


# ═══════════════════════════════════════════════════════════════════
# 5. THRESHOLD ANALYSIS (on VALIDATION set, not test)
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'─' * 70}")
print("THRESHOLD ANALYSIS (Validation Set)")
print(f"{'─' * 70}")

# Pick top two Mode A candidates based on val ROC-AUC for detailed threshold analysis
top_candidates = sorted(mode_a_results, key=lambda r: -r["val_roc_auc"])[:3]

threshold_analysis = {}

for r in top_candidates:
    model = r["model_obj"]
    y_vp = model.predict_proba(
        X_val_full if r["fset"] == "full" else X_val_reduced
    )[:, 1]

    thresholds_to_test = np.arange(0.05, 1.0, 0.05)
    rows = []
    for thr in thresholds_to_test:
        y_pred_thr = (y_vp >= thr).astype(int)
        acc = accuracy_score(y_val_bin, y_pred_thr)
        prec = precision_score(y_val_bin, y_pred_thr, zero_division=0)
        rec = recall_score(y_val_bin, y_pred_thr, zero_division=0)
        f1 = f1_score(y_val_bin, y_pred_thr, average="macro", zero_division=0)
        # For a screening filter, we want HIGH RECALL (catch all anomalies)
        specificity = np.sum((y_vp < thr) & (y_val_bin == 0)) / np.sum(y_val_bin == 0)
        rows.append({
            "threshold": round(thr, 2),
            "accuracy": round(acc, 4),
            "precision": round(prec, 4),
            "recall": round(rec, 4),
            "specificity": round(specificity, 4),
            "macro_f1": round(f1, 4),
        })
    thr_df = pd.DataFrame(rows)
    threshold_analysis[r["name"]] = thr_df
    print(f"\n  {r['name']}:")
    # Find threshold with recall >= 0.95 and highest specificity
    high_recall = thr_df[thr_df["recall"] >= 0.95]
    if len(high_recall) > 0:
        best_row = high_recall.loc[high_recall["specificity"].idxmax()]
        print(f"    Best threshold (recall >= 0.95): {best_row['threshold']:.2f}")
        print(f"      Acc={best_row['accuracy']:.4f}  Prec={best_row['precision']:.4f}  "
              f"Rec={best_row['recall']:.4f}  Spec={best_row['specificity']:.4f}  F1={best_row['macro_f1']:.4f}")
    # Find threshold maximizing F1
    best_f1_row = thr_df.loc[thr_df["macro_f1"].idxmax()]
    print(f"    Best threshold (max F1): {best_f1_row['threshold']:.2f}")
    print(f"      Acc={best_f1_row['accuracy']:.4f}  Prec={best_f1_row['precision']:.4f}  "
          f"Rec={best_f1_row['recall']:.4f}  Spec={best_f1_row['specificity']:.4f}  F1={best_f1_row['macro_f1']:.4f}")


# ═══════════════════════════════════════════════════════════════════
# 6. EVALUATE EXISTING MULTICLASS MODELS AS MODE B
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'─' * 70}")
print("MODE B — EXISTING MULTICLASS MODELS")
print(f"{'─' * 70}")

mode_b_specs = [
    ("MLP full",      "mlp.pkl",              X_test_full,    14),
    ("MLP reduced",   "mlp_reduced.pkl",      X_test_reduced, 12),
    ("DT full",       "decision_tree.pkl",    X_test_full,    14),
    ("DT reduced",    "decision_tree_reduced.pkl", X_test_reduced, 12),
    ("LR full",       "logistic_regression.pkl",  X_test_full, 14),
    ("LR reduced",    "logistic_regression_reduced.pkl", X_test_reduced, 12),
]

mode_b_results = []

for name, fname, X_ts, nf in mode_b_specs:
    model_path = os.path.join(MODEL_DIR, fname)
    model = joblib.load(model_path)
    model_size = os.path.getsize(model_path)

    y_pred = model.predict(X_ts)
    acc = accuracy_score(y_test, y_pred)
    f1  = f1_score(y_test, y_pred, average="macro")

    single = X_ts[0:1]
    lat_pred  = measure_latency(model, single)
    lat_proba = measure_proba_latency(model, single)

    cr = classification_report(y_test, y_pred, output_dict=True, zero_division=0)

    result = {
        "name": name,
        "fname": fname,
        "n_features": nf,
        "model_size_bytes": model_size,
        "test_acc": acc,
        "test_f1": f1,
        "lat_predict": lat_pred,
        "lat_proba": lat_proba,
        "class_report": cr,
    }
    mode_b_results.append(result)
    print(f"\n  {name} ({fname}):")
    print(f"    Acc={acc:.4f}  F1={f1:.4f}  Size={model_size:,}B")
    print(f"    Lat(predict): {lat_pred['mean_us']:.1f} us   Lat(proba): {lat_proba['mean_us']:.1f} us")


# ═══════════════════════════════════════════════════════════════════
# 7. CASCADE COST-BENEFIT ANALYSIS
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'─' * 70}")
print("CASCADE COST-BENEFIT ANALYSIS")
print(f"{'─' * 70}")

# Simulate: Mode A screens, if anomalous -> Mode B diagnoses
# What fraction of samples does Mode A flag as anomalous?

for r in mode_a_results:
    y_pred_bin = r["model_obj"].predict(
        X_test_full if r["fset"] == "full" else X_test_reduced
    )
    n_flagged = np.sum(y_pred_bin == 1)
    n_normal  = np.sum(y_pred_bin == 0)
    pct_flagged = n_flagged / len(y_pred_bin) * 100
    pct_normal  = n_normal / len(y_pred_bin) * 100

    # Of the ones flagged as anomalous, how many truly are?
    true_anom_in_flagged = np.sum((y_pred_bin == 1) & (y_test_bin == 1))
    precision_anom = true_anom_in_flagged / n_flagged if n_flagged > 0 else 0

    # Of true anomalies, how many are caught?
    true_anom_total = np.sum(y_test_bin == 1)
    recall_anom = true_anom_in_flagged / true_anom_total

    # Missed anomalies (classified as normal by Mode A)
    missed = np.sum((y_pred_bin == 0) & (y_test_bin == 1))

    print(f"\n  {r['name']}:")
    print(f"    Predicted Normal:    {n_normal:,} ({pct_normal:.1f}%)")
    print(f"    Flagged Anomalous:   {n_flagged:,} ({pct_flagged:.1f}%)")
    print(f"    Anomaly Recall:      {recall_anom:.4f}")
    print(f"    Anomaly Precision:   {precision_anom:.4f}")
    print(f"    Missed anomalies:    {missed}")


# ═══════════════════════════════════════════════════════════════════
# 8. CONFUSION MATRIX PLOTS (Mode A best candidates)
# ═══════════════════════════════════════════════════════════════════
for r in mode_a_results:
    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(r["test_cm"], annot=True, fmt="d", cmap="Blues",
                xticklabels=["Normal", "Anomalous"],
                yticklabels=["Normal", "Anomalous"],
                linewidths=0.5, ax=ax)
    ax.set_xlabel("Predicted", fontsize=10)
    ax.set_ylabel("Actual", fontsize=10)
    ax.set_title(f"Mode A: {r['name']}", fontsize=11, pad=8)
    plt.tight_layout()
    cm_path = os.path.join(RESULT_DIR, f"cm_mode_a_{r['short']}.png")
    plt.savefig(cm_path, dpi=180)
    plt.close()


# ═══════════════════════════════════════════════════════════════════
# 9. ROC AND PR CURVES (top candidates)
# ═══════════════════════════════════════════════════════════════════
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5))

for r in mode_a_results:
    proba = r["y_test_proba"]
    fpr, tpr, _ = roc_curve(y_test_bin, proba)
    ax1.plot(fpr, tpr, label=f"{r['name']} (AUC={r['test_roc_auc']:.3f})")

    prec_arr, rec_arr, _ = precision_recall_curve(y_test_bin, proba)
    ax2.plot(rec_arr, prec_arr, label=f"{r['name']} (AP={r['test_pr_auc']:.3f})")

ax1.plot([0, 1], [0, 1], 'k--', alpha=0.3)
ax1.set_xlabel("False Positive Rate", fontsize=11)
ax1.set_ylabel("True Positive Rate", fontsize=11)
ax1.set_title("ROC Curves — Mode A Candidates", fontsize=12)
ax1.legend(fontsize=7.5, loc="lower right")
ax1.grid(alpha=0.2)

ax2.set_xlabel("Recall", fontsize=11)
ax2.set_ylabel("Precision", fontsize=11)
ax2.set_title("Precision-Recall Curves — Mode A Candidates", fontsize=12)
ax2.legend(fontsize=7.5, loc="lower left")
ax2.grid(alpha=0.2)

plt.tight_layout()
plt.savefig(os.path.join(RESULT_DIR, "mode_a_roc_pr_curves.png"), dpi=180)
plt.close()
print(f"\nSaved ROC/PR curve plot.")


# ═══════════════════════════════════════════════════════════════════
# 10. SAVE METRICS CSV
# ═══════════════════════════════════════════════════════════════════
rows = []
for r in mode_a_results:
    rows.append({
        "Role":           "Mode A",
        "Model":          r["name"],
        "Feature Set":    r["fset"],
        "N Features":     r["n_features"],
        "Test Accuracy":  round(r["test_acc"], 6),
        "Macro F1":       round(r["test_f1"], 6),
        "Precision":      round(r["test_prec"], 6),
        "Recall":         round(r["test_rec"], 6),
        "ROC-AUC":        round(r["test_roc_auc"], 6),
        "PR-AUC":         round(r["test_pr_auc"], 6),
        "Params":         r["n_params"],
        "Size (B)":       r["model_size_bytes"],
        "Mean Lat predict (us)": round(r["lat_predict"]["mean_us"], 2),
        "P95 Lat predict (us)":  round(r["lat_predict"]["p95_us"], 2),
        "P99 Lat predict (us)":  round(r["lat_predict"]["p99_us"], 2),
        "Mean Lat proba (us)":   round(r["lat_proba"]["mean_us"], 2),
        "P95 Lat proba (us)":    round(r["lat_proba"]["p95_us"], 2),
    })

for r in mode_b_results:
    rows.append({
        "Role":           "Mode B",
        "Model":          r["name"],
        "Feature Set":    "full" if r["n_features"] == 14 else "reduced",
        "N Features":     r["n_features"],
        "Test Accuracy":  round(r["test_acc"], 6),
        "Macro F1":       round(r["test_f1"], 6),
        "Precision":      np.nan,
        "Recall":         np.nan,
        "ROC-AUC":        np.nan,
        "PR-AUC":         np.nan,
        "Params":         np.nan,
        "Size (B)":       r["model_size_bytes"],
        "Mean Lat predict (us)": round(r["lat_predict"]["mean_us"], 2),
        "P95 Lat predict (us)":  round(r["lat_predict"]["p95_us"], 2),
        "P99 Lat predict (us)":  round(r["lat_predict"]["p99_us"], 2),
        "Mean Lat proba (us)":   round(r["lat_proba"]["mean_us"], 2),
        "P95 Lat proba (us)":    round(r["lat_proba"]["p95_us"], 2),
    })

metrics_df = pd.DataFrame(rows)
csv_path = os.path.join(RESULT_DIR, "mode_selection_metrics.csv")
metrics_df.to_csv(csv_path, index=False)
print(f"Saved: {csv_path}")


# ═══════════════════════════════════════════════════════════════════
# 11. GENERATE MARKDOWN REPORT
# ═══════════════════════════════════════════════════════════════════
report_path = os.path.join(REPORT_DIR, "Phase3_Mode_Selection_Report.md")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("# Phase 3 — Mode A / Mode B Candidate Selection Report\n\n")
    f.write("**All values measured from actual model runs. No values assumed or invented.**\n\n")
    f.write("---\n\n")

    # Setup
    f.write("## 1. Experiment Setup\n\n")
    f.write("| Parameter | Value |\n| --- | --- |\n")
    f.write(f"| Dataset | `EngineFaultDB_Final.csv` (55,998 rows after dedup) |\n")
    f.write(f"| Split | 40% train / 40% val / 20% test (stratified, seed=42) |\n")
    f.write(f"| Train | {len(y_train):,} |\n")
    f.write(f"| Val | {len(y_val):,} |\n")
    f.write(f"| Test | {len(y_test):,} |\n")
    f.write(f"| Scaler | Phase 2 `scaler.pkl` (frozen, NOT re-fit) |\n")
    f.write(f"| Latency | perf_counter_ns, {LATENCY_WARMUP} warmup + {LATENCY_ITERS} iters |\n\n")

    # Binary target
    f.write("## 2. Binary Target Construction\n\n")
    f.write("| Original Label | Binary Label |\n| --- | --- |\n")
    f.write("| Fault 0 (Normal) | **0** — Normal |\n")
    f.write("| Fault 1 | **1** — Anomalous |\n")
    f.write("| Fault 2 | **1** — Anomalous |\n")
    f.write("| Fault 3 | **1** — Anomalous |\n\n")
    f.write("### Test Set Binary Distribution\n\n")
    f.write(f"| Class | Count | % |\n| --- | --- | --- |\n")
    f.write(f"| Normal (0) | {np.sum(y_test_bin==0):,} | {np.sum(y_test_bin==0)/len(y_test_bin)*100:.1f}% |\n")
    f.write(f"| Anomalous (1) | {np.sum(y_test_bin==1):,} | {np.sum(y_test_bin==1)/len(y_test_bin)*100:.1f}% |\n\n")

    # Mode A results table
    f.write("## 3. Mode A Candidates — Binary Screening\n\n")
    f.write("| Model | Features | Acc | Macro F1 | Prec | Recall | ROC-AUC | PR-AUC | Params | Size | predict lat | proba lat |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for r in mode_a_results:
        sz = r["model_size_bytes"]
        sz_s = f"{sz/1024:.1f}KB" if sz >= 1024 else f"{sz}B"
        f.write(f"| {r['name']} | {r['n_features']} | {r['test_acc']:.4f} | {r['test_f1']:.4f} | "
                f"{r['test_prec']:.4f} | {r['test_rec']:.4f} | {r['test_roc_auc']:.4f} | "
                f"{r['test_pr_auc']:.4f} | {r['n_params']} | {sz_s} | "
                f"{r['lat_predict']['mean_us']:.1f}us | {r['lat_proba']['mean_us']:.1f}us |\n")
    f.write("\n")

    # Per-class detail for Mode A
    f.write("### Per-Class Metrics (Test Set)\n\n")
    for r in mode_a_results:
        f.write(f"#### {r['name']}\n\n")
        f.write("| Class | Precision | Recall | F1 | Support |\n| --- | --- | --- | --- | --- |\n")
        cr = r["class_report"]
        for cls in ["Normal", "Anomalous"]:
            d = cr[cls]
            f.write(f"| {cls} | {d['precision']:.4f} | {d['recall']:.4f} | "
                    f"{d['f1-score']:.4f} | {int(d['support'])} |\n")
        f.write("\n")

    # Confusion matrices
    f.write("### Confusion Matrices\n\n")
    for r in mode_a_results:
        cm = r["test_cm"]
        f.write(f"**{r['name']}:** TN={cm[0,0]} FP={cm[0,1]} FN={cm[1,0]} TP={cm[1,1]}\n\n")

    # ROC/PR curves
    f.write("### ROC and Precision-Recall Curves\n\n")
    f.write("![ROC and PR Curves](../results/mode_a_roc_pr_curves.png)\n\n")

    # Threshold analysis
    f.write("## 4. Threshold Analysis (Validation Set)\n\n")
    for name, thr_df in threshold_analysis.items():
        f.write(f"### {name}\n\n")
        f.write("| Threshold | Accuracy | Precision | Recall | Specificity | Macro F1 |\n")
        f.write("| --- | --- | --- | --- | --- | --- |\n")
        for _, row in thr_df.iterrows():
            f.write(f"| {row['threshold']:.2f} | {row['accuracy']:.4f} | {row['precision']:.4f} | "
                    f"{row['recall']:.4f} | {row['specificity']:.4f} | {row['macro_f1']:.4f} |\n")
        f.write("\n")

    # Mode B results
    f.write("## 5. Mode B Candidates — Multiclass Diagnosis (Existing Phase 2 Models)\n\n")
    f.write("| Model | Features | Acc | Macro F1 | Size | predict lat | proba lat |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- |\n")
    for r in mode_b_results:
        sz = r["model_size_bytes"]
        sz_s = f"{sz/1024:.1f}KB" if sz >= 1024 else f"{sz}B"
        f.write(f"| {r['name']} ({r['fname']}) | {r['n_features']} | "
                f"{r['test_acc']:.4f} | {r['test_f1']:.4f} | {sz_s} | "
                f"{r['lat_predict']['mean_us']:.1f}us | {r['lat_proba']['mean_us']:.1f}us |\n")
    f.write("\n")

    # Per-class for Mode B
    f.write("### Per-Class Detail (Top Mode B candidates)\n\n")
    for r in mode_b_results[:2]:  # MLP full and MLP reduced
        f.write(f"#### {r['name']}\n\n")
        f.write("| Class | Precision | Recall | F1 | Support |\n| --- | --- | --- | --- | --- |\n")
        cr = r["class_report"]
        for cls_key in sorted([k for k in cr.keys() if k.isdigit()], key=int):
            d = cr[cls_key]
            f.write(f"| Fault {cls_key} | {d['precision']:.4f} | {d['recall']:.4f} | "
                    f"{d['f1-score']:.4f} | {int(d['support'])} |\n")
        f.write("\n")

    # Cascade analysis
    f.write("## 6. Cascade Cost-Benefit Analysis\n\n")
    f.write("How much work does Mode A save by screening?\n\n")
    f.write("| Mode A Model | Predicted Normal | Flagged Anomalous | Anomaly Recall | Anomaly Precision | Missed Anomalies |\n")
    f.write("| --- | --- | --- | --- | --- | --- |\n")
    for r in mode_a_results:
        y_pred_bin_test = r["model_obj"].predict(
            X_test_full if r["fset"] == "full" else X_test_reduced
        )
        n_normal = np.sum(y_pred_bin_test == 0)
        n_flagged = np.sum(y_pred_bin_test == 1)
        tp = np.sum((y_pred_bin_test == 1) & (y_test_bin == 1))
        fn = np.sum((y_pred_bin_test == 0) & (y_test_bin == 1))
        anom_rec = tp / np.sum(y_test_bin == 1)
        anom_prec = tp / n_flagged if n_flagged > 0 else 0
        f.write(f"| {r['name']} | {n_normal} ({n_normal/len(y_test_bin)*100:.1f}%) | "
                f"{n_flagged} ({n_flagged/len(y_test_bin)*100:.1f}%) | "
                f"{anom_rec:.4f} | {anom_prec:.4f} | {fn} |\n")
    f.write("\n")

    # Saved artifacts
    f.write("## 7. Saved Artifacts\n\n")
    f.write("### Mode A Models (newly trained binary classifiers)\n\n")
    f.write("```\n")
    for r in mode_a_results:
        fn = f"mode_a_{r['short']}.pkl"
        fpath = os.path.join(MODEL_DIR, fn)
        sz = os.path.getsize(fpath)
        f.write(f"  models/{fn:44s} {sz:>8,} B\n")
    f.write("```\n\n")
    f.write("### Mode B Models (existing Phase 2, not modified)\n\n")
    f.write("```\n")
    for r in mode_b_results:
        sz = r["model_size_bytes"]
        f.write(f"  models/{r['fname']:44s} {sz:>8,} B\n")
    f.write("```\n\n")
    f.write("No separate scaler is required — all Mode A models use the Phase 2 `scaler.pkl`.\n\n")

    f.write("---\n*End of Phase 3 Mode Selection Report.*\n")

print(f"Report saved: {report_path}")


# ═══════════════════════════════════════════════════════════════════
# CONSOLE SUMMARY
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'=' * 70}")
print("PHASE 3 MODE SELECTION — COMPLETE")
print(f"{'=' * 70}")

print("\nMode A candidates (binary screening):")
for r in sorted(mode_a_results, key=lambda x: -x["test_roc_auc"]):
    print(f"  {r['name']:30s}  ROC-AUC={r['test_roc_auc']:.4f}  F1={r['test_f1']:.4f}  "
          f"Rec={r['test_rec']:.4f}  Lat={r['lat_predict']['mean_us']:.1f}us  "
          f"Size={r['model_size_bytes']:,}B")

print("\nMode B candidates (multiclass diagnosis):")
for r in sorted(mode_b_results, key=lambda x: -x["test_f1"]):
    print(f"  {r['name']:30s}  F1={r['test_f1']:.4f}  Acc={r['test_acc']:.4f}  "
          f"Lat={r['lat_predict']['mean_us']:.1f}us  Size={r['model_size_bytes']:,}B")

print("\nDone.")
