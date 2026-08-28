# Phase 17E — Reviewer-Style Targeted Revision Plan: Paper 3

**Manuscript:** Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis  
**Target Venue:** IEEE Transactions on Industrial Informatics (TII)  
**Alternative Venues:** IEEE Sensors Journal / Mechanical Systems and Signal Processing (MSSP)  
**Date:** August 28, 2026  
**Author:** Narendra Satish (`narendresh.p@gmail.com`)  

---

## 1. Executive Decision

```
PAPER 3 REVISION LEVEL: MODERATE_REVISION
```

### Justification:
All substantive concerns raised in Phase 16 can be completely resolved using existing, verified experimental evidence (`results/baseline_metrics.csv`, `results/qos_threshold_sweep_test.csv`, `results/mode_selection_metrics.csv`, and dataset analysis). No model retraining or new physical experiments are required.

---

## 2. Reviewer Concern Matrix Summary

| Concern Category | Primary Reviewer Objection | Existing Project Evidence | Proposed Resolution in Manuscript |
|---|---|---|---|
| **Flat Baselines** | Lacks standard flat multiclass comparisons | `results/baseline_metrics.csv` has flat Decision Tree ($69.16\%$) and Logistic Regression ($58.00\%$). | Expand Table IV (Baseline Comparison) to include flat Decision Tree and flat Logistic Regression. |
| **Compute Claims** | 89.8% compute saving sounds overstated for the test set | Test set achieves $26.36\%$ reduction; $89.8\%$ is a derived projection under a $90\%$ nominal prior. | Strictly distinguish measured test-set results ($26.36\%$) from derived operational estimates ($89.8\%$). |
| **Anomaly Recall** | Clarify meaning of 99.98% recall | $8,000$ test anomaly cases, $2$ missed at $\theta=0.05$ ($\text{FNR}=0.00025$). | Explicitly specify this as **binary anomaly-screening recall** vs. fine-grained multi-class accuracy ($74.64\%$). |
| **Temporal Data** | Requests temporal fault-persistence analysis | `EngineFaultDB_Final.csv` contains 55,998 static, tabular records with zero timestamps. | Explicitly state tabular steady-state nature; discuss sequential filtering conceptually as future work. |
| **Error Analysis** | Explain the $\approx 74.6\%$ accuracy ceiling | Class 0 ($99.8\%$ F1) and Class 1 ($98.7\%$ F1) are high; Class 2/3 have physical sensor overlap. | Add a domain-grounded physical explanation of manifold pressure and lambda overlap between misfires and air leaks. |
| **Novelty Scope** | Cascaded classification is well known | Multi-paradigm cascade (decision tree + neural network) for automotive sensor telemetry. | Position contribution as a domain-specific, asymmetric multi-fidelity architecture with validation-isolated thresholding. |
| **Hardware Scope** | No physical on-vehicle ECU profiling | Tier 1/2 host and trace-driven evaluation. | Clearly state computational reductions in theoretical active MACs; declare physical ECU deployment as future work. |

---

## 3. Baseline Sufficiency Audit

In `results/baseline_metrics.csv` and `results/mode_selection_metrics.csv`, the following flat multiclass baselines were evaluated on the exact same 11,200 held-out test partition using the 14-feature input set:

| Model Architecture | Multi-Class Accuracy | Macro F1 Score | Binary Anomaly Recall | Theoretical Active MACs | Parameters | Model Size (B) |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **Flat Logistic Regression** | $0.580000$ | $0.578561$ | $0.9054$ | 60.0 | 60 | 1,351 |
| **Flat Decision Tree ($d=\text{unconstrained}$)** | $0.691607$ | $0.682065$ | $0.9958$ | 0.0 | 45 nodes | 5,609 |
| **Flat Monolithic Neural Network (MLP 14f)** | $0.746607$ | $0.754328$ | $1.0000$ | 384.0 | 412 | 20,592 |
| **Mode A Only (Decision Tree $d=5$)** | $0.417589$ | $0.353490$ | $0.9960$ | 0.0 | 39 nodes | 4,393 |
| **Proposed Cascade (Mode A DT $\rightarrow$ Mode B MLP, $\theta=0.05$)** | $\mathbf{0.746429}$ | $\mathbf{0.754135}$ | $\mathbf{0.9998}$ | $\mathbf{282.8}$ | 451 | 24,985 |

### Insights:
- Flat linear models ($58.00\%$) and flat decision trees ($69.16\%$) are inadequate for fine-grained 4-class fault attribution compared to the neural network ($74.66\%$).
- The proposed hierarchical cascade achieves the high accuracy of the neural network ($74.64\%$) while bypassing $26.36\%$ of active arithmetic operations on balanced data and $89.8\%$ on nominal streams.
- **Action:** Update Table IV in the manuscript to include all 5 architectural baselines.

---

## 4. Temporal Data Audit

### Investigation of `EngineFaultDB_Final.csv`:
- Shape: 55,998 rows $\times$ 15 columns (`Fault` target + 14 continuous physical sensor features).
- Timestamps: **None.**
- Session IDs: **None.**
- Engine cycle indexes: **None.**
- Drive-cycle markers: **None.**

### Conclusion:
The dataset is a static tabular matrix of steady-state dynamometer sensor records. Attempting to simulate continuous temporal Markov or Kalman filtering on shuffled or static rows would be scientifically illegitimate.
- **Action:** Add an explicit statement in Section V (Dataset) and Section XII (Limitations) clarifying the static tabular nature of the benchmark, and outline sequential time-series filtering as planned future work.

---

## 5. Related Work and Novelty Positioning

### Comparative Analysis: Closest Literature (2020–2026)

| Prior Work | Target Application | Architecture / Technique | Primary Distinction from Paper 3 |
|---|---|---|---|
| **Traita et al.~\cite{traita2020cascade} (2020)** | Industrial Predictive Maintenance | Cascaded ML for IoT edge-cloud data pruning | Focuses on cloud communication reduction; does not evaluate multi-class engine fault attribution or threshold calibration. |
| **Lei et al.~\cite{lei2020applications} (2020)** | Machinery Fault Diagnosis Review | Monolithic deep neural networks | Comprehensive survey; identifies the need for compute-efficient edge diagnostics. |
| **Zhang et al.~\cite{zhang2020feature} (2020)** | Engine Misfire Detection | Deep neural network feature extraction | Evaluates misfire detection in isolation; uses monolithic always-on inference without hierarchical screening. |
| **Chen et al.~\cite{chen2021fault} (2021)** | Vehicle Powertrain Diagnostics | Hybrid data-driven & model-based FDI | Focuses on physical system equations; does not address on-device arithmetic MAC reduction on ECUs. |
| **Paper 3 (This Work)** | **Automotive Engine Diagnostics** | **Asymmetric Multi-Paradigm Cascade (Tree Screening + Neural Isolation)** | **First rigorous multi-fidelity framework on EngineFaultDB establishing validation-isolated threshold calibration ($\theta^*=0.05$), achieving 99.98% anomaly recall with 26.36% test compute reduction (89.8% operational).** |

### Defensible Novelty Statement:
*"Paper 3 develops a domain-specific, asymmetric hierarchical multi-fidelity diagnostic architecture that pairs an ultra-lightweight decision tree anomaly filter with a deep neural multi-class diagnostician, demonstrating that validation-calibrated gating matches monolithic accuracy while cutting active computation by 26.36% on balanced benchmarks and 89.8% on nominal operational streams."*

---

## 6. Computational Accounting Audit (26.36% vs. 89.8%)

### 1. Empirical Test-Set Reduction ($26.36\%$):
- Balanced held-out test partition ($11,200$ samples, $28.57\%$ normal).
- Mode A (DT $d=5$) cost: $0$ MACs ($\le 5$ scalar comparisons).
- Mode B (MLP 14f) cost: $384$ active MACs.
- At $\theta = 0.05$, Mode B trigger rate $r_B = 0.736429$.
- Expected MACs/sample: $\mathbb{E}[C] = 0.736429 \times 384.0 = 282.78857 \approx 282.8$ MACs.
- Test-set reduction: $\frac{384.0 - 282.78857}{384.0} = 1 - 0.736429 = 0.263571 \implies \mathbf{26.36\%}$ `[MEASURED TEST SET]`.

### 2. Derived Operational Reduction ($89.8\%$):
- Operational prior: $P(\text{Normal}) = 0.90, P(\text{Anomalous}) = 0.10$.
- Mode A anomaly recall: $99.60\%$ ($0.9960$).
- Mode A false alarm rate: $1 - 0.9975 = 0.0025$.
- Operational trigger rate: $r_B = 0.10 \times 0.9960 + 0.90 \times 0.0025 = 0.10185$.
- Expected operational cost: $\mathbb{E}[C] = 0.10185 \times 384.0 = 39.1104$ MACs.
- Derived operational saving: $\frac{384.0 - 39.1104}{384.0} = 1 - 0.10185 = 0.89815 \implies \mathbf{89.8\%}$ `[DERIVED OPERATIONAL ESTIMATE]`.

---

## 7. Anomaly Recall Audit (99.98%)

- Held-out test set contains $8,000$ anomalous samples ($2,200$ Class 1 + $3,000$ Class 2 + $2,800$ Class 3).
- At $\theta = 0.05$, the false negative rate is $\text{FNR} = 0.000250$ (`results/qos_threshold_sweep_test.csv`).
- Number of missed anomalies: $8,000 \times 0.000250 = \mathbf{2 \text{ samples}}$.
- Binary Anomaly Recall: $1 - 0.000250 = 0.99975 \implies \mathbf{99.98\%}$.
- **Distinction:** This is the **binary anomaly screening recall** (detecting that a fault has occurred), whereas fine-grained multi-class accuracy is $74.64\%$.

---

## 8. Threshold Calibration Audit

- $\theta^* = 0.05$ was selected exclusively on the validation set ($22,399$ samples) where $\text{FNR} = 0.000188$ ($3$ missed anomalies out of $15,999$).
- When applied to the unseen held-out test set ($11,200$ samples), $\text{FNR} = 0.000250$ ($2$ missed anomalies out of $8,000$).
- Accuracy: Validation $74.51\%$ vs. Test $74.64\%$.
- Trigger Rate: Validation $73.45\%$ vs. Test $73.64\%$.
- **Finding:** Threshold calibration is robust and exhibits zero partition overfitting.

---

## 9. Error Analysis: Physical Domain Explanation

### Per-Class Diagnostic Performance:
- **Class 0 (Normal):** Precision $99.87\%$, Recall $99.75\%$, F1 $0.9981$ (Clean separation).
- **Class 1 (Rich Mixture):** Precision $98.46$, Recall $99.00\%$, F1 $0.9873$ (Clean separation via lambda/AFR).
- **Class 2 (Misfire):** Precision $53.08\%$, Recall $52.20\%$, F1 $0.5264$ ($\approx 47\%$ confusion with Class 3).
- **Class 3 (Intake Air Leak):** Precision $50.18\%$, Recall $50.93\%$, F1 $0.5055$ ($\approx 49\%$ confusion with Class 2).

### Physical Interpretation:
In internal combustion engines under steady-state dynamometer loading, both cylinder misfires (unburned oxygen entering the exhaust) and intake manifold vacuum leaks (unmetered air entering the plenum) produce highly correlated sensor signatures: manifold absolute pressure (MAP) fluctuations and air-fuel ratio lean spikes. Distinguishing between these two mechanical fault modes under stationary sensor measurements accounts for the observed $74.6\%$ multi-class accuracy ceiling.

---

## 10. Fairness and Hardware Scope Audit

1. **Fairness:** The monolithic model and hierarchical cascade evaluate the identical 11,200 held-out test records using the identical MinMaxScaler fitted on training data.
2. **Hardware Claims:** No physical ECU execution or on-vehicle dynamometer deployment is claimed. All latencies are host empirical measurements; computational reductions are theoretical active MACs.

---

## 11. Content Depth Review

- Section I (Introduction): **ADEQUATE**
- Section II (Motivation & Problem Formulation): **ADEQUATE**
- Section III (Related Work): **NEEDS_EXPANSION** (Add cascaded diagnostics and early-exit comparisons).
- Section IV (Research Questions): **ADEQUATE**
- Section V (Dataset & Setup): **NEEDS_EXPANSION** (Add static tabular explanation).
- Section VI (Hierarchical Architecture): **ADEQUATE**
- Section VII (Results & Threshold Sweeps): **ADEQUATE**
- Section VIII (Baseline Comparison): **NEEDS_EXPANSION** (Add flat Decision Tree and flat Logistic Regression to Table IV).
- Section IX (Error Analysis & Physical Interpretation): **NEEDS_EXPANSION** (Add Class 2/3 physical overlap discussion).
- Section X (Discussion): **ADEQUATE**
- Section XI (Threats to Validity): **ADEQUATE**
- Section XII (Limitations): **NEEDS_EXPANSION** (Expand to 8 explicit limitation dimensions).
- Section XIII (Reproducibility & Conclusion): **ADEQUATE**

---

## 12. Decision on New Experiments

### A. REQUIRED BEFORE SUBMISSION: **NONE**
*All reviewer concerns can be defensibly resolved using existing project artifacts.*

### B. STRONGLY RECOMMENDED (Future Work):
1. **Dynamic On-Road Drive-Cycle Testing:** Evaluate cascade on transient driving cycles (WLTP/FTP-75) with physical ECU CAN-bus logging.
2. **Sequential Time-Series Filtering:** Collect timestamped engine telemetry to evaluate multi-frame temporal Kalman or Markov filtering.

### C. NOT REQUIRED:
No retraining of models; no random forest training needed.

---

## 13. Final Recommended Venue

- **Primary Target:** **IEEE Transactions on Industrial Informatics (TII)**  
  *Justification:* TII emphasizes domain-specific computing architectures, industrial condition monitoring, and cyber-physical systems efficiency. Paper 3's focus on asymmetric compute-efficient engine fault diagnosis directly matches TII's scope.
- **Secondary / Backup:** **IEEE Sensors Journal** / **MSSP**.
