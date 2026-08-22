# Paper 4 Final Numerical Consistency Audit

**Paper Title:** *An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims*  
**Audited Manuscript:** [`papers/Paper4_TinyML_Verification/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/paper.tex)  
**Authoritative References:** [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv), [`reports/Phase4_5_Independent_Verification.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase4_5_Independent_Verification.md), [`reports/Dataset_Audit_Report.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Dataset_Audit_Report.md)  
**Date:** August 20, 2026  

---

## 1. Master Numerical Cross-Verification Matrix

| # | Metric / Claim Description | Manuscript Value | Authoritative Verified Value | Source Artifact | Status |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | Total Clean Dataset Samples | $55,998$ | $55,998$ | `Dataset_Audit_Report.md` (Sec. 1) | **PASS** |
| **2** | Train Partition Size ($40\%$) | $22,399$ | $22,399$ | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **3** | Validation Partition Size ($40\%$) | $22,399$ | $22,399$ | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **4** | Held-Out Test Partition Size ($20\%$)| $11,200$ | $11,200$ | `Dataset_Audit_Report.md` (Sec. 2) | **PASS** |
| **5** | Partition Random Seed | $\text{seed} = 42$ | $\text{seed} = 42$ | `baseline_benchmark.py` (Line 36) | **PASS** |
| **6** | Audited Candidate Models Count | $12$ | $12$ | `tinyml_model_profile_verified.csv` | **PASS** |
| **7** | Total Discrepancies Resolved | $20$ | $20$ | `Phase4_5_Independent_Verification.md` | **PASS** |
| **8** | Max Discrepancy Percentage | $7.82\%$ (`mlp_14f_int8` Macro F1) | $7.82\%$ ($0.6852 \rightarrow 0.7388$) | Table II, Row 6 | **PASS** |
| **9** | Test-Set Threshold Leakage Bias | $+1.8\%$ optimistic accuracy bias | $+1.8\%$ | `Phase3_Scientific_Audit.md` (Sec. 3) | **PASS** |
| **10** | FLOAT32 Tensors in FULL_INT8 Models | $0$ float32 tensors | $0$ float32 tensors | `tinyml_model_profile_verified.csv` | **PASS** |
| **11** | INT8 Tensors in FULL_INT8 Models | $8$ int8 tensors | $8$ int8 tensors | `tinyml_model_profile_verified.csv` | **PASS** |
| **12** | $75\%$ Pruning Zero-Weight Count | $298$ zero weights | $298$ zero weights ($73.34\%$) | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **13** | $75\%$ Pruning Active MACs | $96$ active MACs | $96$ active MACs | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **14** | Dense Baseline Active MACs | $384$ MACs | $384$ MACs | `tinyml_model_profile_verified.csv` (Row 1) | **PASS** |
| **15** | $75\%$ Pruned FlatBuffer File Size | $3,920$\,Bytes ($+28$\,B over dense) | $3,920$\,Bytes | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **16** | Unpruned Dense Baseline File Size | $3,892$\,Bytes | $3,892$\,Bytes | `tinyml_model_profile_verified.csv` (Row 1) | **PASS** |

---

## 2. Table II (Discrepancy Table) Source Verification

All 20 rows of Table II in `paper.tex` were verified against `reports/Phase4_5_Independent_Verification.md`:
- Row 1–2: `tflite_mlp_14f_fp32` (Acc diff $0.023661$, F1 diff $0.028589$) — **PASS**
- Row 3–4: `tflite_mlp_12f_fp32` (Acc diff $0.005982$, F1 diff $0.007265$) — **PASS**
- Row 5–6: `tflite_mlp_14f_int8` (Acc diff $0.024375$, F1 diff $0.053611$) — **PASS**
- Row 7–8: `tflite_mlp_12f_int8` (Acc diff $0.001429$, F1 diff $0.044842$) — **PASS**
- Row 9–10: `pruned_mlp_14f_0pct` (Acc diff $0.023661$, F1 diff $0.028589$) — **PASS**
- Row 11–12: `pruned_mlp_14f_25pct` (Acc diff $0.023393$, F1 diff $0.020707$) — **PASS**
- Row 13–14: `pruned_mlp_14f_50pct` (Acc diff $0.022500$, F1 diff $0.027188$) — **PASS**
- Row 15–16: `pruned_mlp_14f_75pct` (Acc diff $0.009107$, F1 diff $0.030705$) — **PASS**
- Row 17–18: `student_a_8_4_int8` (Acc diff $0.000715$, F1 diff $0.000930$) — **PASS**
- Row 19–20: `student_b_16_4_int8` (Acc diff $0.000625$, F1 diff $0.000577$) — **PASS**

---

## 3. Final Numerical Consistency Verdict

```
======================================================================
PAPER 4 NUMERICAL CONSISTENCY AUDIT: PASS (100% Agreement)
======================================================================
  Total Numerical Checks:         16 main claims + 20 discrepancy rows
  Exact Matches with Artifacts:   36 (100.0%)
  Numerical Discrepancies:        0
  Unresolved Issues:              0
======================================================================
```
