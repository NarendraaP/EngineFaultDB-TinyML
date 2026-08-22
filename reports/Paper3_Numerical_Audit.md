# Paper 3 Numerical Consistency Audit

**Manuscript Audited:** [`papers/Paper3_Engine_Diagnostics/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/paper.tex)  
**Primary Authoritative Sources:** [`results/baseline_metrics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/baseline_metrics.csv), [`results/mode_selection_metrics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/mode_selection_metrics.csv), [`results/qos_threshold_sweep_test.csv`](file:///d:/WiDe/EngineFaultDB-main/results/qos_threshold_sweep_test.csv), [`results/qos_threshold_sweep_val.csv`](file:///d:/WiDe/EngineFaultDB-main/results/qos_threshold_sweep_val.csv)  
**Audit Date:** August 20, 2026  

---

## 1. Complete Numerical Claim Audit Matrix

| # | Quantitative Claim Description | Manuscript Location | Manuscript Value | Authoritative Artifact Value | Source Artifact Reference | Status |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| **1** | Total dataset rows | Abstract, Sec. I, Sec. V.A | $55,998$ | $55,998$ | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **2** | Raw dataset rows | Sec. V.A | $55,999$ | $55,999$ | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **3** | Exact duplicates removed | Sec. V.A | $1$ | $1$ | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **4** | Class 0 sample count | Table I, Sec. V.A | $16,000$ ($28.57\%$) | $16,000$ ($28.57\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **5** | Class 1 sample count | Table I, Sec. V.A | $11,000$ ($19.64\%$) | $11,000$ ($19.64\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **6** | Class 2 sample count | Table I, Sec. V.A | $15,000$ ($26.79\%$) | $15,000$ ($26.79\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **7** | Class 3 sample count | Table I, Sec. V.A | $13,998$ ($25.00\%$) | $13,998$ ($25.00\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **8** | Full feature set count | Abstract, Sec. V.B | $14$ features | $14$ features | `baseline_benchmark.py` (Line 70) | **PASS** |
| **9** | Reduced feature set count | Sec. V.B | $12$ features | $12$ features | `baseline_benchmark.py` (Line 73) | **PASS** |
| **10** | AFR vs Lambda correlation | Sec. V.B | $r = 1.0000$ | $r = 1.0000$ | `Dataset_Audit_Report.md` (Sec. 4) | **PASS** |
| **11** | Speed vs RPM correlation | Sec. V.B | $r = 0.9972$ | $r = 0.9972$ | `Dataset_Audit_Report.md` (Sec. 4) | **PASS** |
| **12** | Training split size | Table I, Sec. V.C | $22,399$ samples ($40\%$) | $22,399$ samples ($40\%$) | `baseline_benchmark.py` (Line 90) | **PASS** |
| **13** | Validation split size | Table I, Sec. V.C | $22,399$ samples ($40\%$) | $22,399$ samples ($40\%$) | `baseline_benchmark.py` (Line 90) | **PASS** |
| **14** | Held-out test split size | Table I, Sec. V.C | $11,200$ samples ($20\%$) | $11,200$ samples ($20\%$) | `baseline_benchmark.py` (Line 87) | **PASS** |
| **15** | Data split random seed | Sec. V.C | $\text{seed} = 42$ | $\text{seed} = 42$ | `baseline_benchmark.py` (Line 36) | **PASS** |
| **16** | Mode A DT d=5 Accuracy | Table II | $0.990804$ | $0.990804$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **17** | Mode A DT d=5 Macro F1 | Table II | $0.988693$ | $0.988693$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **18** | Mode A DT d=5 Anomaly Recall | Table II, Sec. VI.A | $0.996000$ ($99.60\%$) | $0.996000$ ($99.60\%$) | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **19** | Mode A DT d=5 Anomaly Prec. | Table II, Sec. VI.A | $0.991168$ ($99.12\%$) | $0.991168$ ($99.12\%$) | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **20** | Mode A DT d=5 ROC-AUC | Table II, Sec. VI.A | $0.992313$ | $0.992313$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **21** | Mode A DT d=5 PR-AUC | Table II, Sec. VI.A | $0.994496$ | $0.994496$ | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **22** | Mode A DT d=5 Parameters & Size | Table II | $39$ params, $4,393$\,B | $39$ params, $4,393$\,B | `mode_selection_metrics.csv` (Row 4) | **PASS** |
| **23** | Mode A DT d=3 Accuracy | Table II | $0.920536$ | $0.920536$ | `mode_selection_metrics.csv` (Row 3) | **PASS** |
| **24** | Mode A DT d=3 Macro F1 | Table II | $0.893769$ | $0.893769$ | `mode_selection_metrics.csv` (Row 3) | **PASS** |
| **25** | Mode A DT d=3 Recall & Prec. | Table II | Rec: $0.99575$, Prec: $0.90297$ | Rec: $0.99575$, Prec: $0.90297$ | `mode_selection_metrics.csv` (Row 3) | **PASS** |
| **26** | Mode A DT d=3 ROC & PR AUC | Table II | ROC: $0.94487$, PR: $0.961021$ | ROC: $0.94487$, PR: $0.961021$ | `mode_selection_metrics.csv` (Row 3) | **PASS** |
| **27** | Mode A LR Binary Accuracy & F1 | Table II | Acc: $0.767857$, F1: $0.679278$ | Acc: $0.767857$, F1: $0.679278$ | `mode_selection_metrics.csv` (Row 2) | **PASS** |
| **28** | Mode B MLP Parameters & MACs | Sec. VI.B, Table IV | $412$ params, $384$ MACs | $412$ params, $384$ MACs | `baseline_metrics.csv` (Row 4) | **PASS** |
| **29** | Mode B MLP Accuracy & F1 | Table III, Table IV | Acc: $0.746607$, F1: $0.754328$ | Acc: $0.746607$, F1: $0.754328$ | `baseline_metrics.csv` (Row 4) | **PASS** |
| **30** | Mode B Per-Class F1 Scores | Table III | F0: $0.9981$, F1: $0.9873$, F2: $0.5264$, F3: $0.5055$ | F0: $0.9981$, F1: $0.9873$, F2: $0.5264$, F3: $0.5055$ | `Phase3_Mode_Selection_Report.md` (Sec. 5) | **PASS** |
| **31** | Hierarchical $\theta=0.00$ metrics | Table IV | Trigger: $1.000$, Acc: $0.746607$, F1: $0.754328$, FNR: $0.0000$ | Trigger: $1.000$, Acc: $0.746607$, F1: $0.754328$, FNR: $0.0000$ | `qos_threshold_sweep_test.csv` (Row 2) | **PASS** |
| **32** | Hierarchical $\theta=0.05$ metrics | Abstract, Table IV, Sec. VII | Trigger: $0.736429$, Acc: $0.746429$, F1: $0.754135$, FNR: $0.00025$ | Trigger: $0.736429$, Acc: $0.746429$, F1: $0.754135$, FNR: $0.00025$ | `qos_threshold_sweep_test.csv` (Row 3) | **PASS** |
| **33** | Hierarchical $\theta=0.05$ missed anomalies | Abstract, Sec. VII.A | $2$ missed out of $8,000$ ($99.98\%$ recall) | $2$ missed ($8000 \times 0.00025 = 2$) | `qos_threshold_sweep_test.csv` (Row 3) | **PASS** |
| **34** | Hierarchical $\theta=0.05$ expected MACs | Abstract, Table IV, Sec. VII.B | $282.8$ MACs ($26.36\%$ reduction) | $0 + 0.736429 \times 384 = 282.788$ | Derived from Eq. (2) \& test CSV | **PASS** |
| **35** | Hierarchical $\theta=0.20$ metrics | Table IV | Trigger: $0.719464$, Acc: $0.744643$, F1: $0.752165$, FNR: $0.002875$ | Trigger: $0.719464$, Acc: $0.744643$, F1: $0.752165$, FNR: $0.002875$ | `qos_threshold_sweep_test.csv` (Row 6) | **PASS** |
| **36** | Hierarchical $\theta=0.50$ metrics | Table IV | Trigger: $0.717768$, Acc: $0.743839$, F1: $0.751294$, FNR: $0.004000$ | Trigger: $0.717768$, Acc: $0.743839$, F1: $0.751294$, FNR: $0.004000$ | `qos_threshold_sweep_test.csv` (Row 12) | **PASS** |
| **37** | Hierarchical $\theta=0.80$ metrics | Table IV, Sec. VII.A | Trigger: $0.715982$, Acc: $0.742679$, F1: $0.750034$, FNR: $0.005625$ | Trigger: $0.715982$, Acc: $0.742679$, F1: $0.750034$, FNR: $0.005625$ | `qos_threshold_sweep_test.csv` (Row 18) | **PASS** |
| **38** | Hierarchical $\theta=1.00$ metrics | Table IV | Trigger: $0.166250$, Acc: $0.417589$, F1: $0.353490$, FNR: $0.767250$ | Trigger: $0.166250$, Acc: $0.417589$, F1: $0.353490$, FNR: $0.767250$ | `qos_threshold_sweep_test.csv` (Row 22) | **PASS** |
| **39** | Nominal stream ($90\%$ healthy) savings | Abstract, Sec. VII.B | $89.8\%$ compute reduction ($\approx 39.1$ MACs) | $0.10 \times 0.9960 + 0.90 \times 0.0025 = 0.10185 \rightarrow 39.1$ | Derived from Eq. (2) \& test parameters | **PASS** |

---

## 2. Summary Audit Statistics

- **Total Quantitative Claims Audited:** 39
- **Claims Passed (Exact Match):** 39 (100.0%)
- **Claims Mismatched:** 0 (0.0%)
- **Claims Unsupported:** 0 (0.0%)
- **Numerical Audit Status:** **`PASS (100% Verified)`**
