import pandas as pd

df = pd.read_csv('results/phase5_policy_comparison.csv')
print(f'Total configurations: {len(df)}')

print('\n--- Deadline=20ms, Workload=HIGH ---')
subset = df[(df['deadline_ms']==20) & (df['workload']=='HIGH')]
for _, row in subset.iterrows():
    print(f"  {row['policy']:22s}: Acc={row['accuracy']:.4f} F1={row['macro_f1']:.4f} DL_Comp={row['deadline_compliance']:.4f} Switches={row['total_switches']}")

print('\n--- Deadline=10ms, All Workloads, BALANCED policy ---')
subset = df[(df['deadline_ms']==10) & (df['policy']=='BALANCED')]
for _, row in subset.iterrows():
    print(f"  WL={row['workload']:8s}: Acc={row['accuracy']:.4f} F1={row['macro_f1']:.4f} DL={row['deadline_compliance']:.4f} Sw={row['total_switches']} Fast={row['time_in_FAST']:.2f} Bal={row['time_in_BALANCED']:.2f} HF={row['time_in_HIGH_FIDELITY']:.2f}")

print('\n=== ABLATION RESULTS ===')
abl = pd.read_csv('results/phase5_ablation_results.csv')
for _, row in abl.iterrows():
    print(f"  {row['ablation']:40s}: Acc={row['accuracy']:.4f} F1={row['macro_f1']:.4f} DL={row['deadline_compliance']:.4f} Sw={row['switch_count']}")

print('\n=== MODEL SWITCH STATISTICS (first 12) ===')
sw = pd.read_csv('results/phase5_model_switch_statistics.csv')
print(sw.head(12).to_string())
