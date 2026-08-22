# Paper 3 Numerical Source & Evidence Audit

**Paper Title:** *Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis*  
**Paper Directory:** [`papers/Paper3_Engine_Diagnostics/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/)  
**Audited Sources:** [`results/mode_selection_metrics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/mode_selection_metrics.csv), [`results/baseline_metrics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/baseline_metrics.csv), [`results/qos_threshold_sweep_test.csv`](file:///d:/WiDe/EngineFaultDB-main/results/qos_threshold_sweep_test.csv), [`results/qos_threshold_sweep_val.csv`](file:///d:/WiDe/EngineFaultDB-main/results/qos_threshold_sweep_val.csv), [`reports/Dataset_Audit_Report.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Dataset_Audit_Report.md)  
**Date:** August 20, 2026  

---

## 1. Master Numerical Verification Matrix

| Metric Description | Exact Value in Authoritative Artifact | Artifact Source | Status |
| :--- | :---: | :--- | :---: |
| **Raw Dataset Sample Count** | $55,999$ rows | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **Deduplicated Dataset Count** | $55,998$ rows ($1$ duplicate removed) | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **Class 0 (Normal Operation)** | $16,000$ samples ($28.57\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **Class 1 (Fuel Rich Mixture)** | $11,000$ samples ($19.64\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **Class 2 (Ignition Misfire)** | $15,000$ samples ($26.79\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **Class 3 (Air Intake Leak)** | $13,998$ samples ($25.00\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **Stratified Split Ratios** | $40\%$ Train ($22,399$), $40\%$ Val ($22,399$), $20\%$ Test ($11,200$) | `baseline_benchmark.py` (Line 90) | **PASS** |
| **Data Split Random Seed** | $\text{seed} = 42$ | `baseline_benchmark.py` (Line 36) | **PASS** |
| **Mode A Model Topology** | Decision Tree depth $d = 5$ (Full 14f and Reduced 12f) | `mode_selection_metrics.csv` (Row 4 & 7) | **PASS** |
| **Mode A Parameter Count** | $39$ parameters, $4,393$\,Bytes | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode A Test Accuracy** | $0.990804$ ($99.08\%$) | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode A Macro F1** | $0.988693$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode A Anomaly Precision** | $0.991168$ ($99.12\%$) | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode A Anomaly Recall** | $0.996000$ ($99.60\%$) | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode A ROC-AUC** | $0.992313$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode A PR-AUC** | $0.994496$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **Mode B Model Topology** | MLP $14 \rightarrow 16 \rightarrow 8 \rightarrow 4$ ($412$ parameters, $384$ MACs) | `baseline_metrics.csv` (Row 4) | **PASS** |
| **Mode B Test Accuracy** | $0.746607$ ($74.66\%$) | `baseline_metrics.csv` (Row 4) | **PASS** |
| **Mode B Macro F1** | $0.754328$ | `baseline_metrics.csv` (Row 4) | **PASS** |
| **Mode B Per-Class F1 (F0, F1, F2, F3)** | F0: $0.9981$, F1: $0.9873$, F2: $0.5264$, F3: $0.5055$ | `Phase3_Mode_Selection_Report.md` | **PASS** |
| **Hierarchical $\theta=0.00$ (Always-On)** | Trigger: $1.000000$, Acc: $0.746607$, F1: $0.754328$, Exp MACs: $384.0$ | `qos_threshold_sweep_test.csv` (Row 2) | **PASS** |
| **Hierarchical $\theta=0.05$ (Calibrated)** | Trigger: $0.736429$, Acc: $0.746429$, F1: $0.754135$, Exp MACs: $282.8$ | `qos_threshold_sweep_test.csv` (Row 3) | **PASS** |
| **Hierarchical $\theta=0.05$ Missed Anomalies**| Anomaly FNR = $0.000250 \implies \mathbf{2}$ missed out of $8,000$ test anomalies | `qos_threshold_sweep_test.csv` (Row 3) | **PASS** |
| **Hierarchical $\theta=0.20$ Performance** | Trigger: $0.719464$, Acc: $0.744643$, F1: $0.752165$, FNR: $0.002875$ (23 missed) | `qos_threshold_sweep_test.csv` (Row 6) | **PASS** |
| **Hierarchical $\theta=0.50$ Performance** | Trigger: $0.717768$, Acc: $0.743839$, F1: $0.751294$, FNR: $0.004000$ (32 missed) | `qos_threshold_sweep_test.csv` (Row 12) | **PASS** |
| **Hierarchical $\theta=0.80$ Performance** | Trigger: $0.715982$, Acc: $0.742679$, F1: $0.750034$, FNR: $0.005625$ (45 missed) | `qos_threshold_sweep_test.csv` (Row 18) | **PASS** |
| **Hierarchical $\theta=1.00$ (Mode A Only)** | Trigger: $0.166250$, Acc: $0.417589$, F1: $0.353490$, FNR: $0.767250$ | `qos_threshold_sweep_test.csv` (Row 22) | **PASS** |
| **Nominal Stream ($90\%$ Healthy) Compute**| Trigger rate $\approx 10.18\% \implies \mathbf{39.1}$ expected MACs ($\mathbf{89.8\%}$ reduction) | Derived from Eq. (2) \& test parameters | **PASS** |

---

## 2. Summary Audit Verdict

```
======================================================================
PAPER 3 NUMERICAL SOURCE AUDIT: PASS (100% Verified)
======================================================================
  Total Numerical Claims Checked:  28
  Exact Matches with Artifacts:   28 (100.0%)
  Discrepancies:                  0
  Unresolved Issues:              0
======================================================================
```
