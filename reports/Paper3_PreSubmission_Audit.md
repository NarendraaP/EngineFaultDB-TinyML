# Paper 3 Pre-Submission Scientific Audit Report

**Manuscript Audited:** [`papers/Paper3_Engine_Diagnostics/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/paper.tex)  
**BibTeX Database:** [`papers/Paper3_Engine_Diagnostics/references.bib`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/references.bib)  
**Primary Authoritative Sources:** [`results/baseline_metrics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/baseline_metrics.csv), [`results/mode_selection_metrics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/mode_selection_metrics.csv), [`results/qos_threshold_sweep_test.csv`](file:///d:/WiDe/EngineFaultDB-main/results/qos_threshold_sweep_test.csv), [`results/qos_threshold_sweep_val.csv`](file:///d:/WiDe/EngineFaultDB-main/results/qos_threshold_sweep_val.csv)  
**Audit Date:** August 20, 2026  

---

## 1. Section-by-Section Scientific Audit

---

### A. Numerical Consistency
- **Audit Findings:** All $39$ quantitative values cited in `paper.tex` (dataset sample counts, class distributions, train/val/test splits, Mode~A screening metrics, Mode~B diagnostic metrics, threshold-sweep trigger rates, anomaly false-negative rates, and expected theoretical MACs) match the underlying authoritative CSV artifacts with $100.0\%$ exactness.
- **Detailed Log:** [`reports/Paper3_Numerical_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Paper3_Numerical_Audit.md)
- **Status:** **PASS**

---

### B. Scientific Terminology & Boundary Rules
- **WCET Audit:** Confirmed. No claims of Worst-Case Execution Time (WCET) are made.
- **MCU & ECU Latency Audit:** Confirmed. No hardware MCU or physical ECU execution timings are claimed. Host timings are strictly identified as empirical host measurements on x86_64.
- **Energy Audit:** Confirmed. No physical energy measurements (mJ / mW) are claimed. Compute savings are strictly characterized in terms of expected theoretical active MAC reductions.
- **MAC Terminology:** Confirmed. Operational reductions are qualified as "expected theoretical active MACs per sample".
- **Real-Time Context:** Confirmed. Real-time requirements are scoped as application domain motivation rather than claimed microcontroller hardware guarantees.
- **Status:** **PASS**

---

### C. Dataset Integrity
- **Audited Parameters:** $55,998$ total rows ($55,999$ raw rows minus 1 duplicate removed during Phase 1 audit).
- **Class Balance:** Class 0 ($16,000, 28.57\%$), Class 1 ($11,000, 19.64\%$), Class 2 ($15,000, 26.79\%$), Class 3 ($13,998, 25.00\%$).
- **Collinearity Proof:** AFR vs $\lambda$ ($r = 1.0000$), Speed vs RPM ($r = 0.9972$).
- **Temporal Scope:** Properly scoped as tabular automotive physical telemetry. Zero unsupported time-series assumptions are made.
- **Status:** **PASS**

---

### D. Mode A Binary Screening Verification
- **Model Topology:** Decision Tree ($d=5$) achieves $99.0804\%$ accuracy, $99.1168\%$ anomaly precision, $99.6000\%$ anomaly recall, $0.992313$ ROC-AUC, and $0.994496$ PR-AUC on held-out test data.
- **Independence:** Probability $P(\text{Anomalous} \mid \mathbf{x})$ is derived strictly from model input features without accessing ground truth.
- **Status:** **PASS**

---

### E. Mode B Multiclass Diagnostician Verification
- **Model Topology:** Multi-Layer Perceptron ($14 \rightarrow 16 \rightarrow 8 \rightarrow 4$, 412 parameters, 384 active MACs) achieves $74.6607\%$ accuracy and $0.754328$ macro F1 on the test partition.
- **Per-Class F1:** Fault 0 ($0.9981$), Fault 1 ($0.9873$), Fault 2 ($0.5264$), Fault 3 ($0.5055$).
- **Status:** **PASS**

---

### F. Threshold Gating & Test-Set Isolation Verification
- **Validation-Driven Tuning:** Threshold $\theta \in [0.00, 1.00]$ was swept across 21 operating points on the validation partition (`qos_threshold_sweep_val.csv`) to identify optimal operating points ($\theta = 0.05$ to $\theta = 0.80$).
- **Test-Set Isolation:** The test set (`qos_threshold_sweep_test.csv`) was evaluated strictly once per operating point. Zero test data was used during threshold calibration, preventing optimistic threshold optimization bias.
- **Status:** **PASS**

---

### G. Computational Cost Model Verification
- **Formulation:** $\mathbb{E}[C_{\text{hierarchical}}] = C_A + r_B(\theta) C_B$ (Equation 2).
- **Mode A Cost:** Mode A (Decision Tree $d=5$) requires at most 5 comparison operations ($0$ MACs).
- **Calculated Savings:** At $\theta = 0.05$, $r_B = 0.736429 \implies 282.8$ expected MACs ($26.36\%$ reduction on test partition). On nominal streams ($90\%$ healthy frames), expected compute is $\approx 39.1$ MACs ($89.8\%$ reduction).
- **Status:** **PASS**

---

### H. Reference Verification
- **Database Audited:** `papers/Paper3_Engine_Diagnostics/references.bib` ($18$ citations).
- **Authenticity Check:** All 18 references are verified as genuine, peer-reviewed publications across IEEE (*TII*, *TIE*, *TIM*, *IoT-J*), Elsevier (*MSSP*, *Measurement*, *JIII*), Springer (*IJCV*, *Cognitive Computation*), and SAE. Zero hallucinated references.
- **Status:** **PASS**

---

### I. Figure and Table Verification
- **Tables I–V:** Accurately structured with exact values from repository CSVs.
- **Figures 1–4:** Correctly mapped in `papers/Paper3_Engine_Diagnostics/figures/` with correct labels and formatting.
- **Status:** **PASS**

---

### J. Reproducibility
- **Split & Seed:** Fixed stratified 3-way split ($40/40/20$, `seed=42`).
- **Pipelines:** Fully reproducible from `baseline_benchmark.py` and Phase 3 verification artifacts.
- **Status:** **PASS**

---

### K. Paper Overlap & Scoping Isolation
- **Independence:** Paper 3 does NOT include the Phase 5 dynamic QoS scheduler (Paper 1), the 12-model compression Pareto benchmark (Paper 2), or the audit methodology (Paper 4).
- **Focus:** Exclusively focused on cyber-physical engine fault diagnostics and hierarchical multi-fidelity inference.
- **Status:** **PASS**

---

## 2. Final Pre-Submission Decision

```
======================================================================
FINAL AUDIT VERDICT: READY_FOR_SUBMISSION
======================================================================
  Manuscript:             papers/Paper3_Engine_Diagnostics/paper.tex
  BibTeX References:      papers/Paper3_Engine_Diagnostics/references.bib
  Evidence Map:           reports/Paper3_Evidence_Map.md
  Overlap Audit:          reports/Paper3_Overlap_Audit.md
  Numerical Audit:        reports/Paper3_Numerical_Audit.md
  Pre-Submission Audit:   reports/Paper3_PreSubmission_Audit.md
======================================================================
```

The manuscript [`papers/Paper3_Engine_Diagnostics/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/paper.tex) has **passed the independent pre-submission scientific audit** and is fully ready for journal formatting and submission.
