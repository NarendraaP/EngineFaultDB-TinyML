#!/usr/bin/env python3
"""
Phase 5G/5H/5I/5J/5M — Complete QoS-Aware TinyML Runtime Experiment Pipeline
===============================================================================
Runs all trace-driven experiments, policy sensitivity, ablation studies,
and generates all required CSV results and publication figures.

EVIDENCE CATEGORY: (B) TRACE-DRIVEN HOST SIMULATION
All latency values are HOST EMPIRICAL — not MCU measurements.
All ESP32-dependent measurements: STATUS = PENDING_PHYSICAL_ESP32

Run:  python phase5/run_phase5_pipeline.py
"""

import sys, os, time, warnings
warnings.filterwarnings("ignore")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from phase5.runtime.model_registry import ModelRegistry
from phase5.runtime.model_adapter import DataPreprocessor
from phase5.runtime.qos_runtime import (
    ExecutionMode, QoSPolicy, WorkloadLevel, QoSRuntime, QoSScheduler
)
from phase5.simulator.trace_simulator import (
    TraceSimulator, AblationEngine, WORKLOAD_PROFILES
)

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

RESULT_DIR = os.path.join(BASE_DIR, "results")
FIGURE_DIR = os.path.join(BASE_DIR, "figures")
os.makedirs(RESULT_DIR, exist_ok=True)
os.makedirs(FIGURE_DIR, exist_ok=True)

DEADLINES = [5, 10, 20, 50, 100]  # ms
WORKLOADS = [WorkloadLevel.LOW, WorkloadLevel.MEDIUM, WorkloadLevel.HIGH, WorkloadLevel.BURST]
POLICIES = [QoSPolicy.ACCURACY_PRIORITY, QoSPolicy.BALANCED,
            QoSPolicy.DEADLINE_PRIORITY, QoSPolicy.COMPUTE_PRIORITY]

# ══════════════════════════════════════════════════════════════════
# SETUP
# ══════════════════════════════════════════════════════════════════
print("=" * 70)
print("PHASE 5 — QoS-Aware TinyML Runtime Experiment Pipeline")
print("EVIDENCE CATEGORY: (B) TRACE-DRIVEN HOST SIMULATION")
print("=" * 70)

t0 = time.time()

print("\n[1/7] Loading model registry...")
registry = ModelRegistry(os.path.join(RESULT_DIR, "tinyml_model_profile_verified.csv"))
registry.load()
pareto_models = registry.get_pareto_models()
print(f"  Loaded {len(registry.get_all_models())} models, {len(pareto_models)} Pareto-optimal")

print("\n[2/7] Loading test data...")
preprocessor = DataPreprocessor(
    data_path=os.path.join(BASE_DIR, "EngineFaultDB_Final.csv"),
    scaler_path=os.path.join(BASE_DIR, "models", "scaler.pkl")
)
X_test, y_test = preprocessor.get_test_samples()
print(f"  Test set: {X_test.shape[0]} samples, {X_test.shape[1]} features")
print(f"  Class distribution: {dict(zip(*np.unique(y_test, return_counts=True)))}")

print("\n[3/7] Initializing QoS Runtime...")
runtime = QoSRuntime(registry, base_dir=BASE_DIR)
print(f"  Modes: FAST={runtime.mode_entries[ExecutionMode.FAST].model}, "
      f"BALANCED={runtime.mode_entries[ExecutionMode.BALANCED].model}, "
      f"HF={runtime.mode_entries[ExecutionMode.HIGH_FIDELITY].model}")

# ══════════════════════════════════════════════════════════════════
# PHASE 5G — FULL TRACE-DRIVEN EXPERIMENTS
# ══════════════════════════════════════════════════════════════════
print("\n[4/7] Running trace-driven experiments (5G)...")
print(f"  {len(DEADLINES)} deadlines x {len(WORKLOADS)} workloads x {len(POLICIES)} policies = "
      f"{len(DEADLINES) * len(WORKLOADS) * len(POLICIES)} configurations")

all_traces = []
policy_results = []
switch_stats = []

total_configs = len(DEADLINES) * len(WORKLOADS) * len(POLICIES)
config_idx = 0

for deadline in DEADLINES:
    for workload in WORKLOADS:
        for policy in POLICIES:
            config_idx += 1
            if config_idx % 10 == 0 or config_idx == 1:
                print(f"  Config {config_idx}/{total_configs}: "
                      f"deadline={deadline}ms, workload={workload.name}, policy={policy.name}")
            
            # Reset runtime to HIGH_FIDELITY before each run
            runtime.current_mode = ExecutionMode.HIGH_FIDELITY
            
            sim = TraceSimulator(runtime, policy)
            sim.run_trace(X_test, y_test, deadline, workload, seed=RANDOM_SEED)
            metrics = sim.get_summary_metrics()
            
            # Save a subset of trace frames for the CSV (first 500 per config to keep file manageable)
            trace_df = sim.to_dataframe()
            trace_df['policy'] = policy.name
            trace_df['workload'] = workload.name
            all_traces.append(trace_df.head(500))
            
            # Policy comparison row
            model_freq = metrics.get('model_activation_frequency', {})
            mode_times = {}
            for mode in [ExecutionMode.FAST, ExecutionMode.BALANCED, ExecutionMode.HIGH_FIDELITY]:
                model_name = runtime.mode_entries[mode].model
                mode_times[mode.name] = model_freq.get(model_name, 0) / metrics['total_samples']
            
            policy_row = {
                'deadline_ms': deadline,
                'workload': workload.name,
                'policy': policy.name,
                'accuracy': metrics['overall_accuracy'],
                'macro_f1': metrics['macro_f1'],
                'anomaly_fn_rate': metrics['anomaly_fn_rate'],
                'model_switch_rate': metrics['model_switch_rate'],
                'avg_host_latency_us': metrics['avg_host_latency_us'],
                'p95_host_latency_us': metrics['p95_host_latency_us'],
                'p99_host_latency_us': metrics.get('p99_host_latency_us',
                    float(np.percentile([f.host_inference_latency_us for f in sim.frames], 99))),
                'deadline_compliance': metrics['deadline_compliance'],
                'time_in_FAST': mode_times.get('FAST', 0),
                'time_in_BALANCED': mode_times.get('BALANCED', 0),
                'time_in_HIGH_FIDELITY': mode_times.get('HIGH_FIDELITY', 0),
                'total_switches': metrics['total_switches'],
                'evidence_category': 'TRACE-DRIVEN HOST SIMULATION',
            }
            policy_results.append(policy_row)
            
            # Switch statistics
            for model_name, count in model_freq.items():
                switch_stats.append({
                    'deadline_ms': deadline,
                    'workload': workload.name,
                    'policy': policy.name,
                    'model': model_name,
                    'activation_count': count,
                    'activation_fraction': count / metrics['total_samples'],
                })

# Save results
print("\n  Saving trace results...")
traces_df = pd.concat(all_traces, ignore_index=True)
traces_df.to_csv(os.path.join(RESULT_DIR, "phase5_runtime_traces.csv"), index=False)
print(f"  -> results/phase5_runtime_traces.csv ({len(traces_df)} rows)")

policy_df = pd.DataFrame(policy_results)
policy_df.to_csv(os.path.join(RESULT_DIR, "phase5_policy_comparison.csv"), index=False)
print(f"  -> results/phase5_policy_comparison.csv ({len(policy_df)} rows)")

switch_df = pd.DataFrame(switch_stats)
switch_df.to_csv(os.path.join(RESULT_DIR, "phase5_model_switch_statistics.csv"), index=False)
print(f"  -> results/phase5_model_switch_statistics.csv ({len(switch_df)} rows)")

# ══════════════════════════════════════════════════════════════════
# PHASE 5J — ABLATION STUDIES
# ══════════════════════════════════════════════════════════════════
print("\n[5/7] Running ablation studies (5J)...")
ablation = AblationEngine(runtime)
ablation_results = []

test_deadline = 10.0  # ms
test_workload = WorkloadLevel.HIGH
test_policy = QoSPolicy.BALANCED

# Ablation A: Static highest-accuracy vs QoS-aware
print("  Ablation A: Static HIGH_FIDELITY vs QoS-aware...")
static_hf = ablation.run_static_model(X_test, y_test, ExecutionMode.HIGH_FIDELITY,
                                        test_deadline, test_workload)
static_hf['ablation'] = 'A_static_highest_accuracy'
ablation_results.append(static_hf)

runtime.current_mode = ExecutionMode.HIGH_FIDELITY
qos_a = ablation.run_qos_aware(X_test, y_test, test_deadline, test_workload, test_policy)
qos_a['ablation'] = 'A_qos_aware'
ablation_results.append(qos_a)

# Ablation B: Static smallest vs QoS-aware
print("  Ablation B: Static FAST vs QoS-aware...")
static_fast = ablation.run_static_model(X_test, y_test, ExecutionMode.FAST,
                                         test_deadline, test_workload)
static_fast['ablation'] = 'B_static_smallest'
ablation_results.append(static_fast)

runtime.current_mode = ExecutionMode.HIGH_FIDELITY
qos_b = ablation.run_qos_aware(X_test, y_test, test_deadline, test_workload, test_policy)
qos_b['ablation'] = 'B_qos_aware'
ablation_results.append(qos_b)

# Ablation C: QoS WITHOUT workload awareness vs WITH
print("  Ablation C: QoS without vs with workload awareness...")
runtime.current_mode = ExecutionMode.HIGH_FIDELITY
qos_no_wl = ablation.run_qos_no_workload_awareness(X_test, y_test, test_deadline, test_policy)
qos_no_wl['ablation'] = 'C_qos_no_workload_awareness'
ablation_results.append(qos_no_wl)

runtime.current_mode = ExecutionMode.HIGH_FIDELITY
qos_with_wl = ablation.run_qos_aware(X_test, y_test, test_deadline, test_workload, test_policy)
qos_with_wl['ablation'] = 'C_qos_with_workload_awareness'
ablation_results.append(qos_with_wl)

# Ablation D: QoS WITHOUT deadline vs WITH deadline
print("  Ablation D: QoS without vs with deadline constraints...")
runtime.current_mode = ExecutionMode.HIGH_FIDELITY
qos_no_dl = ablation.run_qos_no_deadline(X_test, y_test, test_workload)
qos_no_dl['ablation'] = 'D_qos_no_deadline'
ablation_results.append(qos_no_dl)

runtime.current_mode = ExecutionMode.HIGH_FIDELITY
qos_with_dl = ablation.run_qos_aware(X_test, y_test, test_deadline, test_workload, test_policy)
qos_with_dl['ablation'] = 'D_qos_with_deadline'
ablation_results.append(qos_with_dl)

ablation_df = pd.DataFrame(ablation_results)
ablation_df['evidence_category'] = 'TRACE-DRIVEN HOST SIMULATION'
ablation_df.to_csv(os.path.join(RESULT_DIR, "phase5_ablation_results.csv"), index=False)
print(f"  -> results/phase5_ablation_results.csv ({len(ablation_df)} rows)")

# ══════════════════════════════════════════════════════════════════
# PHASE 5M — FIGURES
# ══════════════════════════════════════════════════════════════════
print("\n[6/7] Generating figures (5M)...")

plt.rcParams.update({'font.size': 10, 'figure.dpi': 150})

# --- Figure 1: Accuracy vs Workload ---
fig, ax = plt.subplots(figsize=(10, 6))
for policy in POLICIES:
    subset = policy_df[(policy_df['policy'] == policy.name) & (policy_df['deadline_ms'] == 20)]
    ax.plot([w.name for w in WORKLOADS], subset['accuracy'].values, 'o-', label=policy.name, linewidth=2)
ax.set_xlabel('Workload Profile')
ax.set_ylabel('Overall Accuracy')
ax.set_title('Accuracy vs Workload (Deadline=20ms)\n[TRACE-DRIVEN HOST SIMULATION]')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0.5, 1.0)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_accuracy_vs_workload.png"))
plt.close(fig)
print("  -> figures/phase5_accuracy_vs_workload.png")

# --- Figure 2: F1 vs Workload ---
fig, ax = plt.subplots(figsize=(10, 6))
for policy in POLICIES:
    subset = policy_df[(policy_df['policy'] == policy.name) & (policy_df['deadline_ms'] == 20)]
    ax.plot([w.name for w in WORKLOADS], subset['macro_f1'].values, 's-', label=policy.name, linewidth=2)
ax.set_xlabel('Workload Profile')
ax.set_ylabel('Macro F1 Score')
ax.set_title('Macro F1 vs Workload (Deadline=20ms)\n[TRACE-DRIVEN HOST SIMULATION]')
ax.legend()
ax.grid(True, alpha=0.3)
ax.set_ylim(0.4, 1.0)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_f1_vs_workload.png"))
plt.close(fig)
print("  -> figures/phase5_f1_vs_workload.png")

# --- Figure 3: Deadline Compliance vs Workload ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for ax_idx, deadline in enumerate([10, 50]):
    ax = axes[ax_idx]
    for policy in POLICIES:
        subset = policy_df[(policy_df['policy'] == policy.name) & (policy_df['deadline_ms'] == deadline)]
        ax.plot([w.name for w in WORKLOADS], subset['deadline_compliance'].values,
                'D-', label=policy.name, linewidth=2)
    ax.set_xlabel('Workload Profile')
    ax.set_ylabel('Deadline Compliance Rate')
    ax.set_title(f'Deadline Compliance (D={deadline}ms)')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.set_ylim(-0.05, 1.05)
fig.suptitle('Deadline Compliance vs Workload\n[TRACE-DRIVEN HOST SIMULATION]', fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_deadline_compliance_vs_workload.png"))
plt.close(fig)
print("  -> figures/phase5_deadline_compliance_vs_workload.png")

# --- Figure 4: Model Switch Rate ---
fig, ax = plt.subplots(figsize=(10, 6))
for policy in POLICIES:
    rates = []
    for deadline in DEADLINES:
        subset = policy_df[(policy_df['policy'] == policy.name) &
                           (policy_df['deadline_ms'] == deadline) &
                           (policy_df['workload'] == 'HIGH')]
        if len(subset) > 0:
            rates.append(subset['model_switch_rate'].values[0])
        else:
            rates.append(0)
    ax.plot([str(d) for d in DEADLINES], rates, '^-', label=policy.name, linewidth=2)
ax.set_xlabel('Deadline (ms)')
ax.set_ylabel('Model Switch Rate')
ax.set_title('Model Switch Rate vs Deadline (Workload=HIGH)\n[TRACE-DRIVEN HOST SIMULATION]')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_model_switch_rate.png"))
plt.close(fig)
print("  -> figures/phase5_model_switch_rate.png")

# --- Figure 5: Policy Comparison Heatmap ---
fig, axes = plt.subplots(2, 2, figsize=(14, 12))
metrics_to_plot = [
    ('accuracy', 'Accuracy', axes[0, 0]),
    ('macro_f1', 'Macro F1', axes[0, 1]),
    ('deadline_compliance', 'Deadline Compliance', axes[1, 0]),
    ('model_switch_rate', 'Switch Rate', axes[1, 1]),
]
for metric_key, metric_label, ax in metrics_to_plot:
    pivot = policy_df[policy_df['deadline_ms'] == 20].pivot_table(
        index='workload', columns='policy', values=metric_key, aggfunc='first'
    )
    # Reorder rows
    row_order = ['LOW', 'MEDIUM', 'HIGH', 'BURST']
    pivot = pivot.reindex(row_order)
    im = ax.imshow(pivot.values, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
    ax.set_xticks(range(len(pivot.columns)))
    ax.set_xticklabels(pivot.columns, rotation=45, ha='right', fontsize=8)
    ax.set_yticks(range(len(pivot.index)))
    ax.set_yticklabels(pivot.index)
    ax.set_title(f'{metric_label} (D=20ms)')
    # Annotate cells
    for i in range(len(pivot.index)):
        for j in range(len(pivot.columns)):
            val = pivot.values[i, j]
            ax.text(j, i, f'{val:.3f}', ha='center', va='center', fontsize=8,
                    color='white' if val < 0.5 else 'black')
    plt.colorbar(im, ax=ax, fraction=0.046)
fig.suptitle('Policy Comparison Heatmap (D=20ms)\n[TRACE-DRIVEN HOST SIMULATION]', fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_policy_comparison.png"))
plt.close(fig)
print("  -> figures/phase5_policy_comparison.png")

# --- Figure 6: Accuracy-Compute Frontier ---
fig, ax = plt.subplots(figsize=(10, 7))
for m in registry.get_all_models():
    color = 'green' if m.pareto_status == 'PARETO_OPTIMAL' else 'gray'
    marker = '*' if m.pareto_status == 'PARETO_OPTIMAL' else 'o'
    size = 200 if m.pareto_status == 'PARETO_OPTIMAL' else 80
    ax.scatter(m.active_macs, m.test_accuracy, c=color, marker=marker, s=size,
               edgecolors='black', linewidths=0.5, zorder=3)
    ax.annotate(m.model.replace('_', '\n'), (m.active_macs, m.test_accuracy),
                fontsize=6, ha='center', va='bottom', xytext=(0, 8),
                textcoords='offset points')
# Connect Pareto frontier
pareto_sorted = sorted(pareto_models, key=lambda m: m.active_macs)
ax.plot([m.active_macs for m in pareto_sorted],
        [m.test_accuracy for m in pareto_sorted],
        'g--', alpha=0.5, linewidth=1.5, label='Pareto Frontier')
ax.set_xlabel('Active MACs (Theoretical)')
ax.set_ylabel('Test Accuracy')
ax.set_title('Accuracy vs Compute Frontier\n(from Phase 4.5 Verified Profile)')
ax.legend()
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_accuracy_compute_frontier.png"))
plt.close(fig)
print("  -> figures/phase5_accuracy_compute_frontier.png")

# --- Figure 7: Ablation Study ---
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
ablation_pairs = [
    ('A', 'Static Highest Acc vs QoS', ['A_static_highest_accuracy', 'A_qos_aware']),
    ('B', 'Static Smallest vs QoS', ['B_static_smallest', 'B_qos_aware']),
    ('C', 'No Workload Awareness vs With', ['C_qos_no_workload_awareness', 'C_qos_with_workload_awareness']),
    ('D', 'No Deadline vs With Deadline', ['D_qos_no_deadline', 'D_qos_with_deadline']),
]
metrics_ablation = ['accuracy', 'macro_f1', 'deadline_compliance']
colors_ab = ['#e74c3c', '#2ecc71']

for idx, (label, title, keys) in enumerate(ablation_pairs):
    ax = axes[idx // 2][idx % 2]
    rows = ablation_df[ablation_df['ablation'].isin(keys)]
    x = np.arange(len(metrics_ablation))
    width = 0.35
    for j, key in enumerate(keys):
        row = rows[rows['ablation'] == key].iloc[0]
        vals = [row[m] for m in metrics_ablation]
        short_label = key.split('_', 1)[1].replace('_', ' ').title()
        ax.bar(x + j * width, vals, width, label=short_label, color=colors_ab[j], alpha=0.85)
    ax.set_xticks(x + width / 2)
    ax.set_xticklabels(['Accuracy', 'Macro F1', 'Deadline\nCompliance'], fontsize=9)
    ax.set_title(f'Ablation {label}: {title}', fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.2, axis='y')

fig.suptitle('Ablation Studies (D=10ms, Workload=HIGH)\n[TRACE-DRIVEN HOST SIMULATION]', fontsize=13)
fig.tight_layout()
fig.savefig(os.path.join(FIGURE_DIR, "phase5_ablation.png"))
plt.close(fig)
print("  -> figures/phase5_ablation.png")

# ══════════════════════════════════════════════════════════════════
# SUMMARY
# ══════════════════════════════════════════════════════════════════
elapsed = time.time() - t0
print(f"\n[7/7] Pipeline complete in {elapsed:.1f}s")
print("\n" + "=" * 70)
print("GENERATED RESULT FILES:")
print("=" * 70)
for f in ["phase5_runtime_traces.csv", "phase5_policy_comparison.csv",
          "phase5_model_switch_statistics.csv", "phase5_ablation_results.csv"]:
    path = os.path.join(RESULT_DIR, f)
    size = os.path.getsize(path) if os.path.exists(path) else 0
    print(f"  results/{f}: {size:,} bytes")

print("\nGENERATED FIGURES:")
for f in ["phase5_accuracy_vs_workload.png", "phase5_f1_vs_workload.png",
          "phase5_deadline_compliance_vs_workload.png", "phase5_model_switch_rate.png",
          "phase5_policy_comparison.png", "phase5_accuracy_compute_frontier.png",
          "phase5_ablation.png"]:
    path = os.path.join(FIGURE_DIR, f)
    exists = os.path.exists(path)
    print(f"  figures/{f}: {'OK' if exists else 'MISSING'}")

print("\nEVIDENCE CATEGORY: (B) TRACE-DRIVEN HOST SIMULATION")
print("All ESP32-dependent measurements: STATUS = PENDING_PHYSICAL_ESP32")
print("=" * 70)
