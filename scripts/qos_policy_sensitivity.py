#!/usr/bin/env python3
"""
Phase 3 — QoS Policy Sensitivity Analysis (Zero Threshold-Selection Leakage)
================================================================================
Strict Methodology:
1. Normalise components on VALIDATION SET sweep (qos_threshold_sweep_val.csv).
2. Calculate composite scores and SELECT optimal threshold θ* for each policy profile on VALIDATION SET.
3. Apply selected θ* to HELD-OUT TEST SET sweep (qos_threshold_sweep_test.csv) for unbiased evaluation.

Inputs : results/qos_threshold_sweep_val.csv
         results/qos_threshold_sweep_test.csv
Outputs: results/qos_policy_sensitivity.csv
         figures/qos_policy_frontier.png
         reports/Phase3_QoS_Policy_Analysis.md
"""

import sys, os, warnings
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ═══════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════
BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULT_DIR = os.path.join(BASE_DIR, "results")
FIG_DIR    = os.path.join(BASE_DIR, "figures")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
for d in [RESULT_DIR, FIG_DIR, REPORT_DIR]:
    os.makedirs(d, exist_ok=True)

# ═══════════════════════════════════════════════════════════════════
# 1. LOAD VALIDATION AND TEST SWEEPS
# ═══════════════════════════════════════════════════════════════════
val_sweep  = pd.read_csv(os.path.join(RESULT_DIR, "qos_threshold_sweep_val.csv"))
test_sweep = pd.read_csv(os.path.join(RESULT_DIR, "qos_threshold_sweep_test.csv"))

print("=" * 70)
print("Phase 3 — QoS Policy Sensitivity Analysis (Zero Leakage)")
print("=" * 70)
print(f"Loaded Val sweep:  {len(val_sweep)} threshold points")
print(f"Loaded Test sweep: {len(test_sweep)} threshold points\n")

# ═══════════════════════════════════════════════════════════════════
# 2. DEFINE COMPONENT METRICS AND NORMALIZATION (Val Set Parameters)
# ═══════════════════════════════════════════════════════════════════
COMPONENTS = {
    "accuracy": {
        "source_col": "overall_accuracy",
        "direction":  "higher_better",
        "label":      "Accuracy (4-class)",
        "rationale":  "Correct multiclass diagnosis across all fault types.",
    },
    "macro_f1": {
        "source_col": "macro_f1",
        "direction":  "higher_better",
        "label":      "Macro F1 (4-class)",
        "rationale":  "Class-balanced harmonic mean of precision and recall.",
    },
    "safety": {
        "source_col": "fn_rate_anomalous",
        "direction":  "lower_better",
        "label":      "Safety (1 − FN rate)",
        "rationale":  "Fraction of true anomalies missed by Mode A screening.",
    },
    "latency_mean": {
        "source_col": "avg_latency_us",
        "direction":  "lower_better",
        "label":      "Mean Latency",
        "rationale":  "Average per-sample host inference time.",
    },
    "latency_p95": {
        "source_col": "p95_latency_us",
        "direction":  "lower_better",
        "label":      "P95 Latency",
        "rationale":  "95th-percentile tail latency.",
    },
    "latency_p99": {
        "source_col": "p99_latency_us",
        "direction":  "lower_better",
        "label":      "P99 Latency",
        "rationale":  "99th-percentile extreme tail latency.",
    },
    "deadline_5ms": {
        "source_col": "deadline_5ms_compliance",
        "direction":  "higher_better",
        "label":      "Deadline 5 ms Compliance",
        "rationale":  "Fraction of samples meeting a 5 ms host-time budget.",
    },
}

# Normalise Val set and Test set using Validation min-max bounds (prevents test data leakage)
norm_val_cols  = {}
norm_test_cols = {}

for comp_name, comp_info in COMPONENTS.items():
    raw_val  = val_sweep[comp_info["source_col"]].values.astype(float)
    raw_test = test_sweep[comp_info["source_col"]].values.astype(float)

    v_min, v_max = raw_val.min(), raw_val.max()

    if v_max - v_min < 1e-12:
        norm_v = np.ones_like(raw_val)
        norm_t = np.ones_like(raw_test)
    elif comp_info["direction"] == "higher_better":
        norm_v = (raw_val - v_min) / (v_max - v_min)
        norm_t = (raw_test - v_min) / (v_max - v_min)
    else:  # lower_better
        norm_v = (v_max - raw_val) / (v_max - v_min)
        norm_t = (v_max - raw_test) / (v_max - v_min)

    c_name = f"norm_{comp_name}"
    val_sweep[c_name]  = norm_v
    test_sweep[c_name] = norm_t
    norm_val_cols[comp_name]  = c_name
    norm_test_cols[comp_name] = c_name

# ═══════════════════════════════════════════════════════════════════
# 3. DEFINE POLICY PROFILES
# ═══════════════════════════════════════════════════════════════════
POLICIES = {
    "accuracy_priority": {
        "label": "Accuracy Priority",
        "description": "Maximises diagnostic accuracy and F1 above all else.",
        "weights": {
            "accuracy":     0.35,
            "macro_f1":     0.30,
            "safety":       0.20,
            "latency_mean": 0.05,
            "latency_p95":  0.03,
            "latency_p99":  0.02,
            "deadline_5ms": 0.05,
        },
    },
    "balanced": {
        "label": "Balanced",
        "description": "Compromise between accuracy, safety, and latency.",
        "weights": {
            "accuracy":     0.20,
            "macro_f1":     0.15,
            "safety":       0.20,
            "latency_mean": 0.15,
            "latency_p95":  0.10,
            "latency_p99":  0.05,
            "deadline_5ms": 0.15,
        },
    },
    "deadline_priority": {
        "label": "Deadline Priority",
        "description": "Prioritises latency and deadline compliance.",
        "weights": {
            "accuracy":     0.10,
            "macro_f1":     0.10,
            "safety":       0.15,
            "latency_mean": 0.20,
            "latency_p95":  0.15,
            "latency_p99":  0.10,
            "deadline_5ms": 0.20,
        },
    },
    "safety_first": {
        "label": "Safety First",
        "description": "Minimises the risk of missed anomalies (false negatives).",
        "weights": {
            "accuracy":     0.15,
            "macro_f1":     0.10,
            "safety":       0.40,
            "latency_mean": 0.10,
            "latency_p95":  0.10,
            "latency_p99":  0.05,
            "deadline_5ms": 0.10,
        },
    },
}

# ═══════════════════════════════════════════════════════════════════
# 4. SELECT THRESHOLD ON VAL SET & EVALUATE ON TEST SET
# ═══════════════════════════════════════════════════════════════════
print("─" * 70)
print("THRESHOLD SELECTION (Val Set) & UNBIASED EVALUATION (Test Set)")
print("─" * 70)

score_results = []
selected_thetas = {}

for pname, pinfo in POLICIES.items():
    # Compute score on Validation set
    score_v = np.zeros(len(val_sweep))
    score_t = np.zeros(len(test_sweep))

    for comp_name, w in pinfo["weights"].items():
        score_v += w * val_sweep[norm_val_cols[comp_name]].values
        score_t += w * test_sweep[norm_test_cols[comp_name]].values

    val_sweep[f"score_{pname}"]  = score_v
    test_sweep[f"score_{pname}"] = score_t

    # SELECT THRESHOLD ON VALIDATION SET ONLY
    best_val_idx   = val_sweep[f"score_{pname}"].idxmax()
    selected_theta = val_sweep.loc[best_val_idx, "threshold"]
    selected_thetas[pname] = selected_theta

    # Find row in Test set corresponding to selected_theta
    test_match_idx = test_sweep[test_sweep["threshold"] == selected_theta].index[0]
    test_row       = test_sweep.loc[test_match_idx]

    print(f"\n  {pinfo['label']}:")
    print(f"    Val Selected θ* = {selected_theta:.2f} (Val Score = {score_v[best_val_idx]:.6f})")
    print(f"    Test Set Evaluation: Acc={test_row['overall_accuracy']:.4f}  "
          f"F1={test_row['macro_f1']:.4f}  FN={test_row['fn_rate_anomalous']*100:.2f}%  "
          f"Lat={test_row['avg_latency_us']:.0f}μs")

    for idx, row_t in test_sweep.iterrows():
        score_results.append({
            "policy":                   pname,
            "policy_label":             pinfo["label"],
            "threshold":                row_t["threshold"],
            "is_selected_by_val":       (row_t["threshold"] == selected_theta),
            "val_composite_score":      round(score_v[idx], 6),
            "test_composite_score":     round(score_t[idx], 6),
            "overall_accuracy":         row_t["overall_accuracy"],
            "macro_f1":                 row_t["macro_f1"],
            "fn_rate_anomalous":        row_t["fn_rate_anomalous"],
            "avg_latency_us":           row_t["avg_latency_us"],
            "p95_latency_us":           row_t["p95_latency_us"],
            "p99_latency_us":           row_t["p99_latency_us"],
            "deadline_5ms_compliance": row_t["deadline_5ms_compliance"],
        })

sens_df = pd.DataFrame(score_results)
sens_path = os.path.join(RESULT_DIR, "qos_policy_sensitivity.csv")
sens_df.to_csv(sens_path, index=False)
print(f"\nSaved Sensitivity Data: {sens_path}")

# ═══════════════════════════════════════════════════════════════════
# 5. PARETO ANALYSIS (Test Set)
# ═══════════════════════════════════════════════════════════════════
def find_pareto_2d(df, acc_col="overall_accuracy", lat_col="avg_latency_us"):
    pareto = []
    for i, r_i in df.iterrows():
        dominated = False
        for j, r_j in df.iterrows():
            if i == j: continue
            if (r_j[acc_col] >= r_i[acc_col] and r_j[lat_col] <= r_i[lat_col] and
                (r_j[acc_col] > r_i[acc_col] or r_j[lat_col] < r_i[lat_col])):
                dominated = True
                break
        if not dominated: pareto.append(i)
    return pareto

pareto_idx = find_pareto_2d(test_sweep)
test_sweep["is_pareto"] = False
test_sweep.loc[pareto_idx, "is_pareto"] = True

# ═══════════════════════════════════════════════════════════════════
# 6. FIGURE GENERATION
# ═══════════════════════════════════════════════════════════════════
plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "axes.grid": True, "grid.alpha": 0.2})
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

policy_colors = {
    "accuracy_priority": "#388E3C",
    "balanced":          "#1976D2",
    "deadline_priority": "#D32F2F",
    "safety_first":      "#7B1FA2",
}

# (0,0) Composite scores
ax = axes[0, 0]
for pname, pinfo in POLICIES.items():
    col = f"score_{pname}"
    ax.plot(test_sweep["threshold"], test_sweep[col], "o-", color=policy_colors[pname],
            markersize=4, linewidth=1.5, label=pinfo["label"])
    sel_th = selected_thetas[pname]
    sel_idx = test_sweep[test_sweep["threshold"] == sel_th].index[0]
    ax.plot(sel_th, test_sweep.loc[sel_idx, col], "*", color=policy_colors[pname], markersize=14, zorder=5)

ax.set_xlabel("Threshold θ")
ax.set_ylabel("Composite QoS Score (Test Set)")
ax.set_title("Policy Profiles — Composite Score vs. Threshold")
ax.set_xlim(-0.02, 1.02)
ax.legend(fontsize=8)

# (0,1) Pareto frontier
ax = axes[0, 1]
non_pareto = test_sweep[~test_sweep["is_pareto"]]
pareto = test_sweep[test_sweep["is_pareto"]]

ax.scatter(non_pareto["avg_latency_us"], non_pareto["overall_accuracy"], c="gray", alpha=0.4, s=40, label="Dominated")
ax.scatter(pareto["avg_latency_us"], pareto["overall_accuracy"], c="#D32F2F", s=80, zorder=3, edgecolors="black", label="Pareto-optimal")
pareto_sorted = pareto.sort_values("avg_latency_us")
ax.plot(pareto_sorted["avg_latency_us"], pareto_sorted["overall_accuracy"], "--", color="#D32F2F", alpha=0.5)

for _, r in pareto.iterrows():
    ax.annotate(f"θ={r['threshold']:.2f}", (r["avg_latency_us"], r["overall_accuracy"]),
                textcoords="offset points", xytext=(5, 5), fontsize=7)

ax.set_xlabel("Mean Latency (μs) — host measured")
ax.set_ylabel("Overall Accuracy")
ax.set_title("Pareto Frontier (Accuracy ↑ vs. Latency ↓)")
ax.legend(fontsize=8)

# (1,0) Balanced Component breakdown
ax = axes[1, 0]
comp_names = list(COMPONENTS.keys())
comp_labels = [COMPONENTS[c]["label"] for c in comp_names]
comp_colors = ["#4CAF50", "#81C784", "#7B1FA2", "#E53935", "#FF7043", "#FFA726", "#1976D2"]

b_weights = POLICIES["balanced"]["weights"]
bottom = np.zeros(len(test_sweep))
for i, comp in enumerate(comp_names):
    w_val = b_weights[comp] * test_sweep[f"norm_{comp}"].values
    ax.bar(test_sweep["threshold"], w_val, bottom=bottom, width=0.04, color=comp_colors[i], label=comp_labels[i], alpha=0.85)
    bottom += w_val

ax.set_xlabel("Threshold θ")
ax.set_ylabel("Weighted Component Contribution")
ax.set_title("Balanced Policy — Component Breakdown")
ax.set_xlim(-0.02, 1.02)
ax.legend(fontsize=6, ncol=2, loc="lower left")

# (1,1) Scatter Acc vs Lat (color=FN rate)
ax = axes[1, 1]
sc = ax.scatter(test_sweep["avg_latency_us"], test_sweep["overall_accuracy"],
                c=test_sweep["fn_rate_anomalous"] * 100, cmap="RdYlGn_r", s=80, edgecolors="black")
cbar = plt.colorbar(sc, ax=ax)
cbar.set_label("FN Rate (%)")
ax.set_xlabel("Mean Latency (μs)")
ax.set_ylabel("Overall Accuracy")
ax.set_title("Trade-off Space: Accuracy vs. Latency vs. FN Rate")

plt.suptitle("QoS Policy Sensitivity Analysis (Zero Leakage)", fontsize=14, y=1.01)
plt.tight_layout()
fig_path = os.path.join(FIG_DIR, "qos_policy_frontier.png")
plt.savefig(fig_path, dpi=180, bbox_inches="tight")
plt.close()
print(f"Saved Figure: {fig_path}")

print("\nDone.")
