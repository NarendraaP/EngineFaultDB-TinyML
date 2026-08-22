# Paper 2 Numerical Consistency Audit

**Manuscript Audited:** [`papers/Paper2_TinyML_Pareto/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/paper.tex)  
**Authoritative Source:** [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv)  
**Verification Baseline:** [`reports/Phase4_5_Independent_Verification.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase4_5_Independent_Verification.md)  
**Audit Date:** August 20, 2026  

---

## 1. Complete Numerical Claim Audit Matrix

Every single quantitative value in `paper.tex` was extracted, cross-referenced, and audited against the authoritative experimental artifacts:

| # | Specific Quantitative Claim | Manuscript Location in `paper.tex` | Manuscript Value | Authoritative Artifact Value | Source Artifact Reference | Audit Status |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| **1** | Total dataset sample count | Abstract, Sec. I, Sec. V.A | $55,998$ rows | $55,998$ rows | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **2** | Raw dataset sample count | Sec. V.A | $55,999$ raw rows | $55,999$ raw rows | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **3** | Exact duplicate removed | Sec. V.A | $1$ duplicate | $1$ duplicate | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **4** | Class 0 sample count | Sec. V.A | $16,000$ ($28.57\%$) | $16,000$ ($28.57\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **5** | Class 1 sample count | Sec. V.A | $11,000$ ($19.64\%$) | $11,000$ ($19.64\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **6** | Class 2 sample count | Sec. V.A | $15,000$ ($26.79\%$) | $15,000$ ($26.79\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **7** | Class 3 sample count | Sec. V.A | $13,998$ ($25.00\%$) | $13,998$ ($25.00\%$) | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **8** | Full feature set count | Abstract, Sec. V.A.1 | $14$ features | $14$ features | `baseline_benchmark.py` (Line 70) | **PASS** |
| **9** | Reduced feature set count | Sec. V.A.1 | $12$ features | $12$ features | `baseline_benchmark.py` (Line 73) | **PASS** |
| **10** | AFR vs Lambda correlation | Sec. V.A.1 | $r = 1.0000$ | $r = 1.0000$ | `Dataset_Audit_Report.md` (Sec. 4) | **PASS** |
| **11** | Speed vs RPM correlation | Sec. V.A.1 | $r = 0.9972$ | $r = 0.9972$ | `Dataset_Audit_Report.md` (Sec. 4) | **PASS** |
| **12** | Training split size | Sec. V.A.2 | $22,399$ samples ($40\%$) | $22,399$ samples ($40\%$) | `baseline_benchmark.py` (Line 90) | **PASS** |
| **13** | Validation split size | Sec. V.A.2 | $22,399$ samples ($40\%$) | $22,399$ samples ($40\%$) | `baseline_benchmark.py` (Line 90) | **PASS** |
| **14** | Held-out test split size | Sec. V.A.2, Sec. V.D | $11,200$ samples ($20\%$) | $11,200$ samples ($20\%$) | `baseline_benchmark.py` (Line 87) | **PASS** |
| **15** | Data split random seed | Sec. V.A.2, Sec. VIII.A | $\text{seed} = 42$ | $\text{seed} = 42$ | `baseline_benchmark.py` (Line 36) | **PASS** |
| **16** | Baseline MLP parameters | Sec. V.B, Table I | $412$ parameters | $412$ parameters | `tinyml_model_profile_verified.csv` | **PASS** |
| **17** | Baseline MLP theoretical MACs | Sec. V.B, Table I | $384$ MACs | $384$ MACs | `tinyml_model_profile_verified.csv` | **PASS** |
| **18** | PTQ representative calibration size | Sec. V.C.1 | $100$ samples | $100$ samples | `Phase4_5_Independent_Verification.md` | **PASS** |
| **19** | Distillation temperature & weight | Sec. V.C.3 | $\tau = 3.0, \alpha = 0.5$ | $\tau = 3.0, \alpha = 0.5$ | `Phase4_5_Independent_Verification.md` | **PASS** |
| **20** | Student A parameters & MACs | Sec. V.C.3, Table I | $176$ params, $160$ MACs | $176$ params, $160$ MACs | `tinyml_model_profile_verified.csv` | **PASS** |
| **21** | Student B parameters & MACs | Sec. V.C.3, Table I | $328$ params, $304$ MACs | $328$ params, $304$ MACs | `tinyml_model_profile_verified.csv` | **PASS** |
| **22** | Host latency timing protocol | Sec. V.D | $100$ warmup, $500$ measured | $100$ warmup, $500$ measured | `Phase4_5_Independent_Verification.md` | **PASS** |
| **23** | `tflite_mlp_14f_fp32` metrics | Table I | Acc: $0.750000$, F1: $0.756608$, Size: $3,892$\,B, Lat: $0.99\,\mu\text{s}$ | Acc: $0.750000$, F1: $0.756608$, Size: $3,892$\,B, Lat: $0.99\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **24** | `tflite_mlp_12f_fp32` metrics | Table I | Acc: $0.747143$, F1: $0.725414$, Size: $3,780$\,B, Lat: $0.87\,\mu\text{s}$ | Acc: $0.747143$, F1: $0.725414$, Size: $3,780$\,B, Lat: $0.87\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **25** | `tflite_mlp_14f_int8` metrics | Table I, Sec. VI.A | Acc: $0.750357$, F1: $0.738824$, Size: $3,728$\,B, Lat: $1.43\,\mu\text{s}$ | Acc: $0.750357$, F1: $0.738824$, Size: $3,728$\,B, Lat: $1.43\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **26** | `tflite_mlp_12f_int8` metrics | Table I, Sec. VI.A | Acc: $0.747857$, F1: $0.715534$, Size: $3,712$\,B, Lat: $1.00\,\mu\text{s}$ | Acc: $0.747857$, F1: $0.715534$, Size: $3,712$\,B, Lat: $1.00\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **27** | `pruned_mlp_14f_0pct` metrics | Table I | Acc: $0.750000$, F1: $0.756608$, Size: $3,892$\,B, Lat: $0.95\,\mu\text{s}$ | Acc: $0.750000$, F1: $0.756608$, Size: $3,892$\,B, Lat: $0.95\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **28** | `pruned_mlp_14f_25pct` metrics | Table I | Acc: $0.750536$, F1: $0.751490$, Size: $3,920$\,B, Lat: $1.69\,\mu\text{s}$ | Acc: $0.750536$, F1: $0.751490$, Size: $3,920$\,B, Lat: $1.69\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **29** | `pruned_mlp_14f_50pct` metrics | Table I | Acc: $0.749464$, F1: $0.756572$, Size: $3,920$\,B, Lat: $0.86\,\mu\text{s}$ | Acc: $0.749464$, F1: $0.756572$, Size: $3,920$\,B, Lat: $0.86\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **30** | `pruned_mlp_14f_75pct` metrics | Table I, Sec. VI.B | Acc: $0.748214$, F1: $0.756251$, Size: $3,920$\,B, Active: $96$, Lat: $0.83\,\mu\text{s}$ | Acc: $0.748214$, F1: $0.756251$, Size: $3,920$\,B, Active: $96$, Lat: $0.83\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **31** | `student_a_8_4_fp32` metrics | Table I, Sec. VI.C | Acc: $0.716339$, F1: $0.722001$, Size: $2,976$\,B, Lat: $0.86\,\mu\text{s}$ | Acc: $0.716339$, F1: $0.722001$, Size: $2,976$\,B, Lat: $0.86\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **32** | `student_a_8_4_int8` metrics | Table I | Acc: $0.711429$, F1: $0.684788$, Size: $3,208$\,B, Lat: $1.02\,\mu\text{s}$ | Acc: $0.711429$, F1: $0.684788$, Size: $3,208$\,B, Lat: $1.02\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **33** | `student_b_16_4_fp32` metrics | Table I, Sec. VI.C | Acc: $0.751429$, F1: $0.738717$, Size: $3,584$\,B, Lat: $0.82\,\mu\text{s}$ | Acc: $0.751429$, F1: $0.738717$, Size: $3,584$\,B, Lat: $0.82\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **34** | `student_b_16_4_int8` metrics | Table I | Acc: $0.745625$, F1: $0.689601$, Size: $3,576$\,B, Lat: $0.98\,\mu\text{s}$ | Acc: $0.745625$, F1: $0.689601$, Size: $3,576$\,B, Lat: $0.98\,\mu\text{s}$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **35** | INT8 zero float32 tensors | Abstract, Sec. VI.A | $0$ float32 tensors, $8$ int8 tensors | $0$ float32 tensors, $8$ int8 tensors | `Phase4_5_Independent_Verification.md` | **PASS** |
| **36** | Pruning zero weights counts | Sec. VI.B | $0\%$ ($0$), $25\%$ ($95$), $50\%$ ($195$), $75\%$ ($298$) | $0\%$ ($0$), $25\%$ ($95$), $50\%$ ($195$), $75\%$ ($298$) | `Phase4_5_Independent_Verification.md` | **PASS** |
| **37** | Pruning actual zero percentages | Sec. VI.B | $23.36\%$, $47.96\%$, $73.34\%$ | $23.36\%$, $47.96\%$, $73.34\%$ | `Phase4_5_Independent_Verification.md` | **PASS** |
| **38** | Pruning FlatBuffer size increase | Sec. VI.B | $+28$\,B ($3,920$\,B vs $3,892$\,B) | $+28$\,B ($3,920$\,B vs $3,892$\,B) | `Phase4_5_Independent_Verification.md` | **PASS** |
| **39** | Student B storage reduction | Abstract, Sec. VI.C | $7.9\%$ reduction ($3,584$\,B vs $3,892$\,B) | $7.91\%$ reduction | `Phase4_5_Independent_Verification.md` | **PASS** |
| **40** | Student B MAC reduction | Sec. VI.C | $20.8\%$ reduction ($304$ vs $384$ MACs) | $20.83\%$ reduction | `Phase4_5_Independent_Verification.md` | **PASS** |
| **41** | Student A storage reduction | Sec. VI.C | $23.5\%$ reduction ($2,976$\,B vs $3,892$\,B) | $23.54\%$ reduction | `Phase4_5_Independent_Verification.md` | **PASS** |
| **42** | Count of Pareto-optimal models | Abstract, Sec. VI.D | Exactly $6$ models | Exactly $6$ models | `tinyml_model_profile_verified.csv` | **PASS** |

---

## 2. Summary Audit Statistics

- **Total Quantitative Claims Audited:** 42
- **Claims Passed (Exact Match):** 42 (100.0%)
- **Claims Mismatched:** 0 (0.0%)
- **Claims Unsupported:** 0 (0.0%)
- **Numerical Audit Status:** **`PASS (100% Verified)`**
