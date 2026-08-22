#!/usr/bin/env python3
"""
Phase 3 — QoS Runtime Simulator v1 (Strict Val/Test Separation)
===================================================================
Simulates a two-stage cascade:
    Mode A (binary screening) → Mode B (multiclass diagnosis)

Uses ACTUAL trained models from Phase 2 and Phase 3.
Measures ACTUAL host inference latency per sample.
Does NOT claim ECU timing or WCET.

Strict Validation/Test Separation:
- Validation set sweep -> used for threshold selection (zero leakage)
- Test set sweep -> used for final evaluation of selected thresholds

Run:  python scripts/qos_runtime_simulator.py
"""

import sys, os, time, warnings
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

# ═══════════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════════
RANDOM_SEED = 42

# Threshold sweep: 0.00 to 1.00 in steps of 0.05
THRESHOLDS = np.round(np.arange(0.00, 1.05, 0.05), 2)

# Deadline sweep
DEADLINES_MS = [5, 10, 20, 50]

# Reference threshold for sample trace
REFERENCE_THETA = 0.50

# Paths
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH   = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")
MODEL_DIR  = os.path.join(BASE_DIR, "models")
RESULT_DIR = os.path.join(BASE_DIR, "results")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
FIG_DIR    = os.path.join(BASE_DIR, "figures")

for d in [RESULT_DIR, REPORT_DIR, FIG_DIR]:
    os.makedirs(d, exist_ok=True)

# Model files
MODE_A_MODEL = os.path.join(MODEL_DIR, "mode_a_dt5_binary_reduced.pkl")
MODE_B_MODEL = os.path.join(MODEL_DIR, "mlp.pkl")
SCALER_PATH  = os.path.join(MODEL_DIR, "scaler.pkl")

# ═══════════════════════════════════════════════════════════════════
# 1. REPRODUCE PHASE 2 SPLIT (verbatim)
# ═══════════════════════════════════════════════════════════════════
print("=" * 70)
print("Phase 3 — QoS Runtime Simulator v1 (Scientific Audit Compliant)")
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

print(f"Dataset split: Train={len(y_train):,}, Val={len(y_val):,}, Test={len(y_test):,}")

# ═══════════════════════════════════════════════════════════════════
# 2. LOAD MODELS AND SCALER
# ═══════════════════════════════════════════════════════════════════
scaler  = joblib.load(SCALER_PATH)
model_a = joblib.load(MODE_A_MODEL)
model_b = joblib.load(MODE_B_MODEL)

# Prepare scaled data
X_val_scaled_full   = scaler.transform(X_val)
X_val_scaled_red    = X_val_scaled_full[:, reduced_indices]
X_test_scaled_full  = scaler.transform(X_test)
X_test_scaled_red   = X_test_scaled_full[:, reduced_indices]

y_val_bin  = (y_val > 0).astype(int)
y_test_bin = (y_test > 0).astype(int)

# ═══════════════════════════════════════════════════════════════════
# 3. MEASURE INFERENCE LATENCY (Per-Sample)
# ═══════════════════════════════════════════════════════════════════
print(f"\n{'─' * 70}")
print("MEASURING PER-SAMPLE INFERENCE LATENCY")
print(f"{'─' * 70}")

# Warmup
dummy_a = X_test_scaled_red[0:1]
for _ in range(2000):
    model_a.predict_proba(dummy_a)

dummy_b = X_test_scaled_full[0:1]
for _ in range(2000):
    model_b.predict_proba(dummy_b)

def run_per_sample_inference(X_scaled_red, X_scaled_full):
    n_samples = len(X_scaled_red)
    a_probas = np.zeros(n_samples)
    a_lat_ns = np.zeros(n_samples, dtype=np.int64)
    b_preds  = np.zeros(n_samples, dtype=int)
    b_lat_ns = np.zeros(n_samples, dtype=np.int64)

    for i in range(n_samples):
        # Mode A single-sample
        s_a = X_scaled_red[i:i+1]
        t0 = time.perf_counter_ns()
        pa = model_a.predict_proba(s_a)
        t1 = time.perf_counter_ns()
        a_probas[i] = pa[0, 1]
        a_lat_ns[i] = t1 - t0

        # Mode B single-sample
        s_b = X_scaled_full[i:i+1]
        t0 = time.perf_counter_ns()
        pb = model_b.predict_proba(s_b)
        t1 = time.perf_counter_ns()
        b_preds[i]  = model_b.classes_[np.argmax(pb[0])]
        b_lat_ns[i] = t1 - t0

    return a_probas, a_lat_ns / 1e3, b_preds, b_lat_ns / 1e3

print("  Running Val set per-sample inference...", end=" ", flush=True)
val_a_probas, val_a_lat_us, val_b_preds, val_b_lat_us = run_per_sample_inference(
    X_val_scaled_red, X_val_scaled_full
)
print("done")

print("  Running Test set per-sample inference...", end=" ", flush=True)
test_a_probas, test_a_lat_us, test_b_preds, test_b_lat_us = run_per_sample_inference(
    X_test_scaled_red, X_test_scaled_full
)
print("done")


# ═══════════════════════════════════════════════════════════════════
# 4. SWEEP FUNCTION
# ═══════════════════════════════════════════════════════════════════
def run_sweep(y_true, y_bin, a_probas, a_lat_us, b_preds, b_lat_us):
    sweep_rows = []
    for theta in THRESHOLDS:
        alpha = (a_probas >= theta).astype(int)
        final_pred = np.where(alpha == 0, 0, b_preds)
        total_lat = a_lat_us + alpha * b_lat_us

        trigger_rate = np.mean(alpha)
        acc          = accuracy_score(y_true, final_pred)
        f1           = f1_score(y_true, final_pred, average="macro", zero_division=0)
        avg_lat      = np.mean(total_lat)
        p50_lat      = np.percentile(total_lat, 50)
        p95_lat      = np.percentile(total_lat, 95)
        p99_lat      = np.percentile(total_lat, 99)

        true_anom_mask = (y_bin == 1)
        fn_anom = np.sum((alpha == 0) & true_anom_mask)
        fn_rate = fn_anom / np.sum(true_anom_mask) if np.sum(true_anom_mask) > 0 else 0.0

        correct_normal = np.sum((final_pred == 0) & (y_true == 0))
        norm_pres = correct_normal / np.sum(y_bin == 0) if np.sum(y_bin == 0) > 0 else 0.0

        dl_compliance = {}
        for dl_ms in DEADLINES_MS:
            dl_compliance[dl_ms] = np.mean(total_lat <= dl_ms * 1000)

        row = {
            "threshold":           theta,
            "trigger_rate":        round(trigger_rate, 6),
            "mode_b_activation":   round(trigger_rate, 6),
            "overall_accuracy":    round(acc, 6),
            "macro_f1":            round(f1, 6),
            "avg_latency_us":      round(avg_lat, 2),
            "p50_latency_us":      round(p50_lat, 2),
            "p95_latency_us":      round(p95_lat, 2),
            "p99_latency_us":      round(p99_lat, 2),
            "fn_rate_anomalous":   round(fn_rate, 6),
            "normal_preservation":  round(norm_pres, 6),
        }
        for dl_ms in DEADLINES_MS:
            row[f"deadline_{dl_ms}ms_compliance"] = round(dl_compliance[dl_ms], 6)

        sweep_rows.append(row)
    return pd.DataFrame(sweep_rows)

print("\nGenerating Validation Set Sweep...", end=" ", flush=True)
val_sweep_df = run_sweep(y_val, y_val_bin, val_a_probas, val_a_lat_us, val_b_preds, val_b_lat_us)
val_sweep_path = os.path.join(RESULT_DIR, "qos_threshold_sweep_val.csv")
val_sweep_df.to_csv(val_sweep_path, index=False)
print(f"done ({val_sweep_path})")

print("Generating Test Set Sweep...", end=" ", flush=True)
test_sweep_df = run_sweep(y_test, y_test_bin, test_a_probas, test_a_lat_us, test_b_preds, test_b_lat_us)
# Also save as default qos_threshold_sweep.csv for backward compatibility
test_sweep_path = os.path.join(RESULT_DIR, "qos_threshold_sweep.csv")
test_sweep_df.to_csv(test_sweep_path, index=False)
test_sweep_path_alt = os.path.join(RESULT_DIR, "qos_threshold_sweep_test.csv")
test_sweep_df.to_csv(test_sweep_path_alt, index=False)
print(f"done ({test_sweep_path})")


# ═══════════════════════════════════════════════════════════════════
# 5. TEST SAMPLE TRACE (at θ = 0.50)
# ═══════════════════════════════════════════════════════════════════
n_test = len(y_test)
trace_rows = []
for i in range(n_test):
    prob_anom = test_a_probas[i]
    alpha = int(prob_anom >= REFERENCE_THETA)
    mode_a_pred = 0 if prob_anom < REFERENCE_THETA else 1

    if alpha == 0:
        final_pred = 0
        mode_b_pred_val = np.nan
        mode_b_lat_val  = 0.0
    else:
        final_pred = int(test_b_preds[i])
        mode_b_pred_val = int(test_b_preds[i])
        mode_b_lat_val  = test_b_lat_us[i]

    total_lat = test_a_lat_us[i] + alpha * mode_b_lat_val

    trace_rows.append({
        "sample_idx":       i,
        "true_fault":       int(y_test[i]),
        "mode_a_prob_anom": round(prob_anom, 6),
        "threshold":        REFERENCE_THETA,
        "mode_b_triggered":  alpha,
        "mode_a_pred":      mode_a_pred,
        "mode_b_pred":      mode_b_pred_val,
        "final_pred":       final_pred,
        "mode_a_lat_us":    round(test_a_lat_us[i], 2),
        "mode_b_lat_us":    round(mode_b_lat_val, 2),
        "total_lat_us":     round(total_lat, 2),
    })

trace_df = pd.DataFrame(trace_rows)
for dl_ms in DEADLINES_MS:
    trace_df[f"deadline_{dl_ms}ms_met"] = (trace_df["total_lat_us"] <= dl_ms * 1000).astype(int)

trace_path = os.path.join(RESULT_DIR, "qos_sample_trace.csv")
trace_df.to_csv(trace_path, index=False)
print(f"Saved Test Sample Trace: {trace_path}")


# ═══════════════════════════════════════════════════════════════════
# 6. DEADLINE SWEEP (Test Set)
# ═══════════════════════════════════════════════════════════════════
deadline_rows = []
for theta in THRESHOLDS:
    alpha = (test_a_probas >= theta).astype(int)
    final_pred = np.where(alpha == 0, 0, test_b_preds)
    total_lat = test_a_lat_us + alpha * test_b_lat_us

    overall_acc = accuracy_score(y_test, final_pred)
    macro_f1    = f1_score(y_test, final_pred, average="macro", zero_division=0)
    trigger_rate = np.mean(alpha)

    for dl_ms in DEADLINES_MS:
        dl_us = dl_ms * 1000
        met_mask = (total_lat <= dl_us)
        compliance = np.mean(met_mask)

        if np.sum(met_mask) > 0:
            acc_met = accuracy_score(y_test[met_mask], final_pred[met_mask])
            f1_met  = f1_score(y_test[met_mask], final_pred[met_mask], average="macro", zero_division=0)
        else:
            acc_met = np.nan
            f1_met  = np.nan

        deadline_rows.append({
            "threshold":        theta,
            "deadline_ms":      dl_ms,
            "trigger_rate":     round(trigger_rate, 6),
            "compliance_rate":  round(compliance, 6),
            "overall_accuracy": round(overall_acc, 6),
            "overall_macro_f1": round(macro_f1, 6),
            "accuracy_met":     round(acc_met, 6) if not np.isnan(acc_met) else np.nan,
            "f1_met":           round(f1_met, 6) if not np.isnan(f1_met) else np.nan,
            "avg_latency_us":   round(np.mean(total_lat), 2),
            "p95_latency_us":   round(np.percentile(total_lat, 95), 2),
            "p99_latency_us":   round(np.percentile(total_lat, 99), 2),
        })

deadline_df = pd.DataFrame(deadline_rows)
deadline_path = os.path.join(RESULT_DIR, "qos_deadline_sweep.csv")
deadline_df.to_csv(deadline_path, index=False)
print(f"Saved Deadline Sweep: {deadline_path}")

print(f"\n{'=' * 70}")
print("QoS RUNTIME SIMULATOR v1 — COMPLETE (Strict Val/Test Separation)")
print(f"{'=' * 70}\n")
