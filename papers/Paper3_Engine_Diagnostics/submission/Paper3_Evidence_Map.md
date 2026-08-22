# Paper 3 Evidence Map & Experimental Traceability

**Paper Title:** *Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis*  
**Paper Directory:** [`papers/Paper3_Engine_Diagnostics/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/)  
**Primary Evidence Sources:** Phases 1, 2, and 3 Artifacts (`results/baseline_metrics.csv`, `results/mode_selection_metrics.csv`, `results/qos_threshold_sweep_val.csv`, `results/qos_threshold_sweep_test.csv`, `reports/Phase3_Mode_Selection_Report.md`)  
**Date:** August 20, 2026  

---

## 1. Traceability Matrix

Every claim, metric, table, and figure in Paper 3 is mapped to its underlying source artifact and empirical categorization:

| Research Question / Topic | Specific Claim / Metric Value | Authoritative Artifact | Artifact Section / Column | Evidence Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Dataset Properties** | $55,998$ physical engine telemetry records, 4 classes. | `Dataset_Audit_Report.md` | Section 1 & 2 | **DIRECTLY MEASURED** |
| **Class Imbalance** | Normal ($16,000, 28.57\%$), Fault 1 ($11,000, 19.64\%$), Fault 2 ($15,000, 26.79\%$), Fault 3 ($13,998, 25.00\%$). | `Dataset_Audit_Report.md` | Section 2 | **DIRECTLY MEASURED** |
| **Feature Redundancy** | AFR vs $\lambda$ ($r = 1.0000$), Speed vs RPM ($r = 0.9972$). | `Dataset_Audit_Report.md` | Section 4 | **DIRECTLY MEASURED** |
| **Data Partitioning** | $40\%$ train ($22,399$), $40\%$ val ($22,399$), $20\%$ test ($11,200$), `seed=42`. | `baseline_benchmark.py` | Lines 81–95 | **DIRECTLY MEASURED** |
| **Binary Class Mapping** | Class 0 $\rightarrow$ Normal ($3,200$ test, $28.57\%$), Classes 1, 2, 3 $\rightarrow$ Anomalous ($8,000$ test, $71.43\%$). | `reports/Phase3_Mode_Selection_Report.md` | Section 2 | **DERIVED** |
| **Mode A (DT d=5 Full)** | Accuracy = $0.990804$, Macro F1 = $0.988693$, Recall = $0.9960$, Precision = $0.9912$, ROC-AUC = $0.992313$, PR-AUC = $0.994496$. | `results/mode_selection_metrics.csv` | Row 4 | **DIRECTLY MEASURED** |
| **Mode A (DT d=3 Full)** | Accuracy = $0.920536$, Macro F1 = $0.893769$, Recall = $0.99575$, Precision = $0.90297$, ROC-AUC = $0.944870$, PR-AUC = $0.961021$. | `results/mode_selection_metrics.csv` | Row 3 | **DIRECTLY MEASURED** |
| **Mode A (LR Full)** | Accuracy = $0.767857$, Macro F1 = $0.679278$, Recall = $0.905375$, Precision = $0.797160$, ROC-AUC = $0.871447$, PR-AUC = $0.950750$. | `results/mode_selection_metrics.csv` | Row 2 | **DIRECTLY MEASURED** |
| **Mode B (MLP 14f Baseline)** | Accuracy = $0.746607$, Macro F1 = $0.754328$, 412 parameters, 384 theoretical MACs. | `results/baseline_metrics.csv` | Row 4 | **DIRECTLY MEASURED** |
| **Mode B Per-Class F1** | Fault 0 F1 = $0.9981$, Fault 1 F1 = $0.9873$, Fault 2 F1 = $0.5264$, Fault 3 F1 = $0.5055$. | `reports/Phase3_Mode_Selection_Report.md` | Section 5 | **DIRECTLY MEASURED** |
| **Validation Thresholds** | $\theta \in [0.00, 1.00]$ evaluated across 21 operating points on validation partition ($22,399$ samples). | `results/qos_threshold_sweep_val.csv` | Full table | **SIMULATED / EVALUATED** |
| **Test Threshold $\theta=0.00$** | Trigger Rate = $1.000$, Acc = $0.746607$, Macro F1 = $0.754328$, Anomaly FN = $0.0000$. | `results/qos_threshold_sweep_test.csv` | Row 2 | **DIRECTLY MEASURED** |
| **Test Threshold $\theta=0.05$** | Trigger Rate = $0.736429$, Acc = $0.746429$, Macro F1 = $0.754135$, Anomaly FN = $0.00025$ ($2$ missed / $8,000$). | `results/qos_threshold_sweep_test.csv` | Row 3 | **DIRECTLY MEASURED** |
| **Test Threshold $\theta=0.10$** | Trigger Rate = $0.736429$, Acc = $0.746429$, Macro F1 = $0.754135$, Anomaly FN = $0.00025$. | `results/qos_threshold_sweep_test.csv` | Row 4 | **DIRECTLY MEASURED** |
| **Test Threshold $\theta=0.20$** | Trigger Rate = $0.719464$, Acc = $0.744643$, Macro F1 = $0.752165$, Anomaly FN = $0.002875$ ($23$ missed / $8,000$). | `results/qos_threshold_sweep_test.csv` | Row 6 | **DIRECTLY MEASURED** |
| **Test Threshold $\theta=0.50$** | Trigger Rate = $0.717768$, Acc = $0.743839$, Macro F1 = $0.751294$, Anomaly FN = $0.004000$ ($32$ missed / $8,000$). | `results/qos_threshold_sweep_test.csv` | Row 12 | **DIRECTLY MEASURED** |
| **Test Threshold $\theta=0.80$** | Trigger Rate = $0.715982$, Acc = $0.742679$, Macro F1 = $0.750034$, Anomaly FN = $0.005625$ ($45$ missed / $8,000$). | `results/qos_threshold_sweep_test.csv` | Row 18 | **DIRECTLY MEASURED** |
| **Test Threshold $\theta=1.00$** | Trigger Rate = $0.166250$, Acc = $0.417589$, Macro F1 = $0.353490$, Anomaly FN = $0.767250$. | `results/qos_threshold_sweep_test.csv` | Row 22 | **DIRECTLY MEASURED** |
| **Theoretical Cost Model** | $C_{\text{always}} = C_B = 384$ MACs; $C_{\text{hierarchical}} = C_A + r_B \cdot C_B$. | Derived theoretical model | Equation (8) in Paper 3 | **DERIVED** |
| **Expected Compute Saving** | At $\theta = 0.05$, expected MACs = $282.8$ ($26.36\%$ reduction); At $\theta = 0.80$, expected MACs = $274.9$ ($28.40\%$ reduction). | Computed from test trigger rates | Section VI in Paper 3 | **DERIVED** |

---

## 2. Integrity & Boundary Verification

- **Real-Time MCU Execution:** Not claimed. Explicitly identified as `TRACE-DRIVEN EVALUATION`.
- **Latency Values:** Explicitly labeled as `HOST EMPIRICAL INFERENCE LATENCY`.
- **Test-Set Isolation:** Threshold selection performed exclusively on validation partition (`results/qos_threshold_sweep_val.csv`), with zero test data contamination.
