#!/usr/bin/env python3
"""
EngineFaultDB — Phase 2: Baseline Model Benchmark
===================================================
Trains & evaluates three classifiers on two feature sets (full / reduced).
Saves models, metrics, confusion matrices, and a markdown report.

Run:  python baseline_benchmark.py
"""

import sys, os, time, json, warnings
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
)

# ═══════════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════════
RANDOM_SEED   = 42
LATENCY_WARMUP = 1000
LATENCY_ITERS  = 5000
DT_MAX_DEPTH   = 5        # edge-friendly depth constraint
MLP_HIDDEN     = (16, 8)
MLP_MAX_ITER   = 500

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CSV_PATH   = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")
MODEL_DIR  = os.path.join(BASE_DIR, "models")
RESULT_DIR = os.path.join(BASE_DIR, "results")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

for d in [MODEL_DIR, RESULT_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════════
# 1. LOAD & PREPARE
# ═══════════════════════════════════════════════════════════════════════
print("=" * 70)
print("Phase 2 — Baseline Model Benchmark")
print("=" * 70)

df = pd.read_csv(CSV_PATH)
print(f"\nLoaded: {df.shape[0]:,} rows x {df.shape[1]} columns")

# Remove the single exact duplicate found in audit
before = len(df)
df = df.drop_duplicates()
after = len(df)
print(f"Removed {before - after} duplicate row(s). Remaining: {after:,}")

# Define feature sets
TARGET = "Fault"
ALL_FEATURES = [c for c in df.columns if c != TARGET]

# Reduced set: drop AFR (redundant with Lambda), drop Speed (redundant with RPM)
REDUCED_FEATURES = [c for c in ALL_FEATURES if c not in ("AFR", "Speed")]

print(f"Full feature set:    {len(ALL_FEATURES)} features  {ALL_FEATURES}")
print(f"Reduced feature set: {len(REDUCED_FEATURES)} features  {REDUCED_FEATURES}")

y = df[TARGET].values

# ═══════════════════════════════════════════════════════════════════════
# 2. STRATIFIED SPLIT: 40% train / 40% val / 20% test
# ═══════════════════════════════════════════════════════════════════════
#  Step 1: 80% (train+val) / 20% test
#  Step 2: 50/50 of the 80% -> 40% train + 40% val of the original
X_all = df[ALL_FEATURES].values

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X_all, y, test_size=0.20, stratify=y, random_state=RANDOM_SEED
)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.50, stratify=y_trainval,
    random_state=RANDOM_SEED
)

print(f"\nSplit sizes:")
print(f"  Train: {len(y_train):,}  ({len(y_train)/len(y)*100:.1f}%)")
print(f"  Val:   {len(y_val):,}  ({len(y_val)/len(y)*100:.1f}%)")
print(f"  Test:  {len(y_test):,}  ({len(y_test)/len(y)*100:.1f}%)")

# Verify class distribution in each split
for name, ys in [("Train", y_train), ("Val", y_val), ("Test", y_test)]:
    counts = np.bincount(ys)
    pcts = counts / len(ys) * 100
    dist_str = "  ".join(f"C{i}:{c}({p:.1f}%)" for i, (c, p) in enumerate(zip(counts, pcts)))
    print(f"  {name} classes: {dist_str}")

# ═══════════════════════════════════════════════════════════════════════
# 3. SCALING — MinMaxScaler fitted on TRAIN ONLY
# ═══════════════════════════════════════════════════════════════════════
scaler_full = MinMaxScaler()
scaler_full.fit(X_train)

X_train_full = scaler_full.transform(X_train)
X_val_full   = scaler_full.transform(X_val)
X_test_full  = scaler_full.transform(X_test)

# Save the fitted scaler
scaler_path = os.path.join(MODEL_DIR, "scaler.pkl")
joblib.dump(scaler_full, scaler_path)
print(f"\nScaler saved: {scaler_path} ({os.path.getsize(scaler_path):,} bytes)")

# Build indices for the reduced feature set
full_col_indices = {c: i for i, c in enumerate(ALL_FEATURES)}
reduced_indices  = [full_col_indices[c] for c in REDUCED_FEATURES]

X_train_reduced = X_train_full[:, reduced_indices]
X_val_reduced   = X_val_full[:, reduced_indices]
X_test_reduced  = X_test_full[:, reduced_indices]

# Also save a reduced-feature scaler (re-fit on raw train data for that subset)
scaler_reduced = MinMaxScaler()
X_train_raw_reduced = X_train[:, reduced_indices]
scaler_reduced.fit(X_train_raw_reduced)
scaler_reduced_path = os.path.join(MODEL_DIR, "scaler_reduced.pkl")
joblib.dump(scaler_reduced, scaler_reduced_path)

# ═══════════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def count_params(model, model_type):
    """Count trainable parameters."""
    if model_type == "lr":
        return model.coef_.size + model.intercept_.size
    elif model_type == "dt":
        tree = model.tree_
        return tree.node_count   # report node count for trees
    elif model_type == "mlp":
        total = 0
        for w in model.coefs_:
            total += w.size
        for b in model.intercepts_:
            total += b.size
        return total
    return -1


def measure_latency(model, single_sample, warmup=LATENCY_WARMUP, n_iter=LATENCY_ITERS):
    """Measure single-sample inference latency using perf_counter_ns."""
    # Warm-up
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
        "mean_us":  np.mean(lat) / 1e3,
        "p50_us":   np.percentile(lat, 50) / 1e3,
        "p95_us":   np.percentile(lat, 95) / 1e3,
        "p99_us":   np.percentile(lat, 99) / 1e3,
        "min_us":   np.min(lat) / 1e3,
        "max_us":   np.max(lat) / 1e3,
        "n_iters":  n_iter,
    }


def evaluate_model(model, X_test_data, y_test_data, model_name, model_type,
                   feature_set_name, model_path):
    """Full evaluation: metrics + latency + model info."""
    y_pred = model.predict(X_test_data)

    acc     = accuracy_score(y_test_data, y_pred)
    prec_m  = precision_score(y_test_data, y_pred, average="macro", zero_division=0)
    rec_m   = recall_score(y_test_data, y_pred, average="macro", zero_division=0)
    f1_m    = f1_score(y_test_data, y_pred, average="macro", zero_division=0)

    cr = classification_report(y_test_data, y_pred, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_test_data, y_pred)

    n_params = count_params(model, model_type)
    model_size = os.path.getsize(model_path)

    single_sample = X_test_data[0:1]
    lat = measure_latency(model, single_sample)

    result = {
        "model_name":      model_name,
        "feature_set":     feature_set_name,
        "n_features":      X_test_data.shape[1],
        "accuracy":        acc,
        "macro_precision":  prec_m,
        "macro_recall":    rec_m,
        "macro_f1":        f1_m,
        "param_count":     n_params,
        "model_size_bytes": model_size,
        "mean_latency_us": lat["mean_us"],
        "p50_latency_us":  lat["p50_us"],
        "p95_latency_us":  lat["p95_us"],
        "p99_latency_us":  lat["p99_us"],
        "min_latency_us":  lat["min_us"],
        "max_latency_us":  lat["max_us"],
        "class_report":    cr,
        "confusion_matrix": cm,
    }
    return result


def plot_confusion_matrix(cm, labels, title, save_path):
    """Save a confusion matrix heatmap."""
    fig, ax = plt.subplots(figsize=(6, 5))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues",
                xticklabels=labels, yticklabels=labels,
                linewidths=0.5, ax=ax, cbar_kws={"shrink": 0.8})
    ax.set_xlabel("Predicted", fontsize=11)
    ax.set_ylabel("Actual", fontsize=11)
    ax.set_title(title, fontsize=13, pad=10)
    plt.tight_layout()
    plt.savefig(save_path, dpi=180)
    plt.close()


# ═══════════════════════════════════════════════════════════════════════
# 4. DEFINE MODELS
# ═══════════════════════════════════════════════════════════════════════

model_specs = [
    {
        "name":       "Logistic Regression",
        "short_name": "logistic_regression",
        "type":       "lr",
        "model":      LogisticRegression(
            max_iter=2000,
            solver="lbfgs",
            random_state=RANDOM_SEED,
            n_jobs=-1,
        ),
    },
    {
        "name":       "Decision Tree",
        "short_name": "decision_tree",
        "type":       "dt",
        "model":      DecisionTreeClassifier(
            max_depth=DT_MAX_DEPTH,
            random_state=RANDOM_SEED,
        ),
    },
    {
        "name":       "MLP (16, 8)",
        "short_name": "mlp",
        "type":       "mlp",
        "model":      MLPClassifier(
            hidden_layer_sizes=MLP_HIDDEN,
            max_iter=MLP_MAX_ITER,
            random_state=RANDOM_SEED,
            early_stopping=True,
            validation_fraction=0.1,
            n_iter_no_change=20,
        ),
    },
]

# ═══════════════════════════════════════════════════════════════════════
# 5. TRAIN & EVALUATE — BOTH FEATURE SETS
# ═══════════════════════════════════════════════════════════════════════

feature_sets = {
    "full": {
        "X_train": X_train_full,
        "X_val":   X_val_full,
        "X_test":  X_test_full,
        "features": ALL_FEATURES,
    },
    "reduced": {
        "X_train": X_train_reduced,
        "X_val":   X_val_reduced,
        "X_test":  X_test_reduced,
        "features": REDUCED_FEATURES,
    },
}

all_results = []

for fs_name, fs_data in feature_sets.items():
    print(f"\n{'─' * 70}")
    print(f"Feature set: {fs_name.upper()} ({len(fs_data['features'])} features)")
    print(f"{'─' * 70}")

    for spec in model_specs:
        mname     = spec["name"]
        sname     = spec["short_name"]
        mtype     = spec["type"]

        # Clone the model (fresh instance each time)
        from sklearn.base import clone
        model = clone(spec["model"])

        print(f"\n  Training {mname} ({fs_name})...", end=" ", flush=True)
        t0 = time.perf_counter()
        model.fit(fs_data["X_train"], y_train)
        train_time = time.perf_counter() - t0
        print(f"done ({train_time:.2f}s)")

        # Validation accuracy (quick sanity check)
        val_acc = accuracy_score(y_val, model.predict(fs_data["X_val"]))
        print(f"    Val accuracy: {val_acc:.4f}")

        # Save model
        model_filename = f"{sname}_{fs_name}.pkl" if fs_name == "reduced" else f"{sname}.pkl"
        model_path = os.path.join(MODEL_DIR, model_filename)
        joblib.dump(model, model_path)
        print(f"    Saved: {model_path} ({os.path.getsize(model_path):,} bytes)")

        # Full test evaluation
        print(f"    Evaluating on test set...", end=" ", flush=True)
        result = evaluate_model(
            model, fs_data["X_test"], y_test,
            mname, mtype, fs_name, model_path,
        )
        result["train_time_s"] = train_time
        result["val_accuracy"] = val_acc
        all_results.append(result)
        print(f"Acc={result['accuracy']:.4f}  F1={result['macro_f1']:.4f}  "
              f"Lat={result['mean_latency_us']:.1f} us")

        # Confusion matrix plot
        class_labels = sorted(np.unique(y_test))
        cm_filename = f"confusion_matrix_{sname}.png" if fs_name == "full" \
                      else f"confusion_matrix_{sname}_reduced.png"
        cm_path = os.path.join(RESULT_DIR, cm_filename)
        cm_title = f"{mname} — {fs_name.capitalize()} Features"
        plot_confusion_matrix(
            result["confusion_matrix"],
            [f"Fault {l}" for l in class_labels],
            cm_title, cm_path,
        )
        print(f"    CM plot: {cm_path}")


# ═══════════════════════════════════════════════════════════════════════
# 6. SAVE METRICS CSV
# ═══════════════════════════════════════════════════════════════════════

rows = []
for r in all_results:
    rows.append({
        "Model":            r["model_name"],
        "Feature Set":      r["feature_set"],
        "N Features":       r["n_features"],
        "Accuracy":         round(r["accuracy"], 6),
        "Macro Precision":  round(r["macro_precision"], 6),
        "Macro Recall":     round(r["macro_recall"], 6),
        "Macro F1":         round(r["macro_f1"], 6),
        "Val Accuracy":     round(r["val_accuracy"], 6),
        "Param Count":      r["param_count"],
        "Model Size (B)":   r["model_size_bytes"],
        "Train Time (s)":   round(r["train_time_s"], 4),
        "Mean Lat (us)":    round(r["mean_latency_us"], 2),
        "P50 Lat (us)":     round(r["p50_latency_us"], 2),
        "P95 Lat (us)":     round(r["p95_latency_us"], 2),
        "P99 Lat (us)":     round(r["p99_latency_us"], 2),
    })

metrics_df = pd.DataFrame(rows)
metrics_csv = os.path.join(RESULT_DIR, "baseline_metrics.csv")
metrics_df.to_csv(metrics_csv, index=False)
print(f"\nMetrics saved: {metrics_csv}")

# ═══════════════════════════════════════════════════════════════════════
# 7. GENERATE MARKDOWN REPORT
# ═══════════════════════════════════════════════════════════════════════

report_path = os.path.join(REPORT_DIR, "Baseline_Model_Report.md")

with open(report_path, "w", encoding="utf-8") as f:
    f.write("# EngineFaultDB — Phase 2: Baseline Model Benchmark Report\n\n")
    f.write("**All values measured from actual model runs on the audited dataset.**\n\n")
    f.write("---\n\n")

    # ── Experiment setup ─────────────────────────────────────────────
    f.write("## 1. Experiment Setup\n\n")
    f.write("| Parameter | Value |\n| --- | --- |\n")
    f.write(f"| Dataset | `EngineFaultDB_Final.csv` |\n")
    f.write(f"| Rows after dedup | {after:,} |\n")
    f.write(f"| Train / Val / Test | 40% / 40% / 20% (stratified) |\n")
    f.write(f"| Train size | {len(y_train):,} |\n")
    f.write(f"| Val size | {len(y_val):,} |\n")
    f.write(f"| Test size | {len(y_test):,} |\n")
    f.write(f"| Scaler | MinMaxScaler (fit on train only) |\n")
    f.write(f"| Random seed | {RANDOM_SEED} |\n")
    f.write(f"| Latency warmup | {LATENCY_WARMUP} iters |\n")
    f.write(f"| Latency measurement | {LATENCY_ITERS} single-sample predictions |\n")
    f.write(f"| Timer | `time.perf_counter_ns()` (monotonic, high-resolution) |\n\n")

    # ── Model configurations ─────────────────────────────────────────
    f.write("## 2. Model Configurations\n\n")
    f.write("### Model A — Logistic Regression (Linear Baseline)\n\n")
    f.write("```\nSolver: lbfgs\nMulti-class: multinomial (default in sklearn 1.9)\nMax iterations: 2000\n```\n\n")
    f.write(f"### Model B — Decision Tree (Lightweight Non-Linear)\n\n")
    f.write(f"```\nMax depth: {DT_MAX_DEPTH} (edge-deployment constraint)\n"
            f"Criterion: gini (default)\n```\n\n")
    f.write(f"### Model C — MLP (Neural Network Baseline)\n\n")
    f.write(f"```\nHidden layers: {MLP_HIDDEN}\nActivation: relu (default)\n"
            f"Solver: adam (default)\nMax iterations: {MLP_MAX_ITER}\n"
            f"Early stopping: True (patience=20, validation_fraction=0.1)\n```\n\n")

    # ── Feature set definitions ──────────────────────────────────────
    f.write("## 3. Feature Sets\n\n")
    f.write("### Full (14 features)\n\n")
    f.write(f"`{', '.join(ALL_FEATURES)}`\n\n")
    f.write("### Reduced (12 features)\n\n")
    f.write("Removed `AFR` (r=1.00 with Lambda) and `Speed` (r=0.997 with RPM).\n\n")
    f.write(f"`{', '.join(REDUCED_FEATURES)}`\n\n")

    # ── Summary table ────────────────────────────────────────────────
    f.write("## 4. Results Summary\n\n")

    # Full feature set table
    f.write("### Experiment 1 — Full Feature Set (14 features)\n\n")
    f.write("| Model | Accuracy | Macro P | Macro R | Macro F1 | Params | Size | Mean Lat | P95 Lat | P99 Lat |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for r in all_results:
        if r["feature_set"] == "full":
            sz = r["model_size_bytes"]
            sz_str = f"{sz/1024:.1f} KB" if sz >= 1024 else f"{sz} B"
            f.write(f"| {r['model_name']} | {r['accuracy']:.4f} | "
                    f"{r['macro_precision']:.4f} | {r['macro_recall']:.4f} | "
                    f"{r['macro_f1']:.4f} | {r['param_count']:,} | {sz_str} | "
                    f"{r['mean_latency_us']:.1f} us | {r['p95_latency_us']:.1f} us | "
                    f"{r['p99_latency_us']:.1f} us |\n")
    f.write("\n")

    # Reduced feature set table
    f.write("### Experiment 2 — Reduced Feature Set (12 features)\n\n")
    f.write("| Model | Accuracy | Macro P | Macro R | Macro F1 | Params | Size | Mean Lat | P95 Lat | P99 Lat |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for r in all_results:
        if r["feature_set"] == "reduced":
            sz = r["model_size_bytes"]
            sz_str = f"{sz/1024:.1f} KB" if sz >= 1024 else f"{sz} B"
            f.write(f"| {r['model_name']} | {r['accuracy']:.4f} | "
                    f"{r['macro_precision']:.4f} | {r['macro_recall']:.4f} | "
                    f"{r['macro_f1']:.4f} | {r['param_count']:,} | {sz_str} | "
                    f"{r['mean_latency_us']:.1f} us | {r['p95_latency_us']:.1f} us | "
                    f"{r['p99_latency_us']:.1f} us |\n")
    f.write("\n")

    # ── Per-class detail ─────────────────────────────────────────────
    f.write("## 5. Per-Class Metrics (Test Set — Full Feature Set)\n\n")
    for r in all_results:
        if r["feature_set"] == "full":
            f.write(f"### {r['model_name']}\n\n")
            f.write("| Class | Precision | Recall | F1 | Support |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            cr = r["class_report"]
            for cls_key in sorted([k for k in cr.keys() if k.isdigit()], key=int):
                d = cr[cls_key]
                f.write(f"| Fault {cls_key} | {d['precision']:.4f} | "
                        f"{d['recall']:.4f} | {d['f1-score']:.4f} | "
                        f"{int(d['support'])} |\n")
            f.write("\n")

    # ── Per-class detail (reduced) ───────────────────────────────────
    f.write("## 6. Per-Class Metrics (Test Set — Reduced Feature Set)\n\n")
    for r in all_results:
        if r["feature_set"] == "reduced":
            f.write(f"### {r['model_name']}\n\n")
            f.write("| Class | Precision | Recall | F1 | Support |\n")
            f.write("| --- | --- | --- | --- | --- |\n")
            cr = r["class_report"]
            for cls_key in sorted([k for k in cr.keys() if k.isdigit()], key=int):
                d = cr[cls_key]
                f.write(f"| Fault {cls_key} | {d['precision']:.4f} | "
                        f"{d['recall']:.4f} | {d['f1-score']:.4f} | "
                        f"{int(d['support'])} |\n")
            f.write("\n")

    # ── Confusion matrices ───────────────────────────────────────────
    f.write("## 7. Confusion Matrices\n\n")
    f.write("### Full Feature Set\n\n")
    f.write("| Logistic Regression | Decision Tree | MLP |\n")
    f.write("| --- | --- | --- |\n")
    f.write("| ![LR](../results/confusion_matrix_logistic_regression.png) "
            "| ![DT](../results/confusion_matrix_decision_tree.png) "
            "| ![MLP](../results/confusion_matrix_mlp.png) |\n\n")
    f.write("### Reduced Feature Set\n\n")
    f.write("| Logistic Regression | Decision Tree | MLP |\n")
    f.write("| --- | --- | --- |\n")
    f.write("| ![LR](../results/confusion_matrix_logistic_regression_reduced.png) "
            "| ![DT](../results/confusion_matrix_decision_tree_reduced.png) "
            "| ![MLP](../results/confusion_matrix_mlp_reduced.png) |\n\n")

    # ── Feature-set comparison ───────────────────────────────────────
    f.write("## 8. Feature-Set Comparison (Full vs Reduced)\n\n")
    f.write("| Model | Full Acc | Reduced Acc | Delta Acc | Full F1 | Reduced F1 | Delta F1 | Full Lat | Reduced Lat |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n")
    full_results = {r["model_name"]: r for r in all_results if r["feature_set"] == "full"}
    red_results  = {r["model_name"]: r for r in all_results if r["feature_set"] == "reduced"}
    for mname in full_results:
        rf = full_results[mname]
        rr = red_results[mname]
        da = rr["accuracy"] - rf["accuracy"]
        df1 = rr["macro_f1"] - rf["macro_f1"]
        f.write(f"| {mname} | {rf['accuracy']:.4f} | {rr['accuracy']:.4f} | "
                f"{da:+.4f} | {rf['macro_f1']:.4f} | {rr['macro_f1']:.4f} | "
                f"{df1:+.4f} | {rf['mean_latency_us']:.1f} us | "
                f"{rr['mean_latency_us']:.1f} us |\n")
    f.write("\n")

    # ── Latency detail ───────────────────────────────────────────────
    f.write("## 9. Latency Profile (Host Machine)\n\n")
    f.write("> **Note:** These are host-machine latencies measured with `time.perf_counter_ns()`. "
            "They are NOT ECU or embedded latencies.\n\n")
    f.write("| Model | Feature Set | Mean | P50 | P95 | P99 | Min | Max |\n")
    f.write("| --- | --- | --- | --- | --- | --- | --- | --- |\n")
    for r in all_results:
        f.write(f"| {r['model_name']} | {r['feature_set']} | "
                f"{r['mean_latency_us']:.1f} us | {r['p50_latency_us']:.1f} us | "
                f"{r['p95_latency_us']:.1f} us | {r['p99_latency_us']:.1f} us | "
                f"{r['min_latency_us']:.1f} us | {r['max_latency_us']:.1f} us |\n")
    f.write("\n")

    # ── Saved artifacts ──────────────────────────────────────────────
    f.write("## 10. Saved Artifacts\n\n")
    f.write("```\n")
    f.write("models/\n")
    for fn in sorted(os.listdir(MODEL_DIR)):
        sz = os.path.getsize(os.path.join(MODEL_DIR, fn))
        f.write(f"    {fn:40s}  {sz:>10,} bytes\n")
    f.write("\nresults/\n")
    for fn in sorted(os.listdir(RESULT_DIR)):
        sz = os.path.getsize(os.path.join(RESULT_DIR, fn))
        f.write(f"    {fn:40s}  {sz:>10,} bytes\n")
    f.write("```\n\n")

    # ── Reproducibility ──────────────────────────────────────────────
    f.write("## 11. Reproducibility\n\n")
    f.write("```bash\n")
    f.write("cd d:\\WiDe\\EngineFaultDB-main\n")
    f.write("python baseline_benchmark.py\n")
    f.write("```\n\n")
    f.write("Dependencies: Python 3.13+, pandas, numpy, matplotlib, seaborn, scikit-learn, joblib\n\n")

    f.write("---\n*End of Phase 2 report.*\n")

print(f"Report saved: {report_path}")

# ═══════════════════════════════════════════════════════════════════════
# 8. FINAL CONSOLE SUMMARY
# ═══════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("PHASE 2 COMPLETE — SUMMARY")
print("=" * 70)

print("\n--- Full Feature Set (14 features) ---")
for r in all_results:
    if r["feature_set"] == "full":
        print(f"  {r['model_name']:25s}  Acc={r['accuracy']:.4f}  F1={r['macro_f1']:.4f}  "
              f"Params={r['param_count']:>6,}  Size={r['model_size_bytes']:>8,}B  "
              f"Lat={r['mean_latency_us']:.1f}us")

print("\n--- Reduced Feature Set (12 features) ---")
for r in all_results:
    if r["feature_set"] == "reduced":
        print(f"  {r['model_name']:25s}  Acc={r['accuracy']:.4f}  F1={r['macro_f1']:.4f}  "
              f"Params={r['param_count']:>6,}  Size={r['model_size_bytes']:>8,}B  "
              f"Lat={r['mean_latency_us']:.1f}us")

print(f"\nAll outputs saved to: models/, results/, reports/")
print("Done.")
