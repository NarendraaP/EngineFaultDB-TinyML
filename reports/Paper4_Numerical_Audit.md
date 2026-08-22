# Paper 4 Numerical Consistency Audit

**Manuscript Audited:** [`papers/Paper4_TinyML_Verification/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/paper.tex)  
**Primary Authoritative Sources:** [`reports/Phase4_5_Independent_Verification.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase4_5_Independent_Verification.md), [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv), [`reports/Phase3_Scientific_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase3_Scientific_Audit.md)  
**Audit Date:** August 20, 2026  

---

## 1. Complete Numerical Claim Audit Matrix

Every single quantitative value, discrepancy delta, and tensor property in `paper.tex` was extracted and cross-referenced against the authoritative verification records:

| # | Quantitative Claim Description | Manuscript Location | Manuscript Value | Authoritative Artifact Value | Source Artifact Reference | Status |
| :---: | :--- | :--- | :---: | :---: | :--- | :---: |
| **1** | Total numerical discrepancies audited | Abstract, Sec. II, Sec. V.A | $20$ discrepancies | $20$ discrepancies | `Phase4_5_Independent_Verification.md` (Sec. 11) | **PASS** |
| **2** | Maximum discrepancy percentage | Abstract, Sec. V.A | $7.82\%$ (F1 divergence) | $7.82\%$ (`mlp_14f_int8` Macro F1) | `Phase4_5_Independent_Verification.md` (Item 6) | **PASS** |
| **3** | Threshold optimization leakage bias | Abstract, Sec. V.D | $+1.8\%$ optimistic bias | $+1.8\%$ optimistic bias | `Phase3_Scientific_Audit.md` (Sec. 4) | **PASS** |
| **4** | Total audited candidate models | Abstract, Sec. I, Sec. V | $12$ candidate models | $12$ candidate models | `tinyml_model_profile_verified.csv` | **PASS** |
| **5** | Discrepancy 1: `tflite_mlp_14f_fp32` Acc | Table III | Initial: $0.726339$, Ver: $0.750000$ ($\Delta = 0.023661, 3.26\%$) | Initial: $0.726339$, Ver: $0.750000$ | `Phase4_5_Independent_Verification.md` (Item 1) | **PASS** |
| **6** | Discrepancy 2: `tflite_mlp_14f_fp32` F1 | Table III | Initial: $0.728019$, Ver: $0.756608$ ($\Delta = 0.028589, 3.93\%$) | Initial: $0.728019$, Ver: $0.756608$ | `Phase4_5_Independent_Verification.md` (Item 2) | **PASS** |
| **7** | Discrepancy 3: `tflite_mlp_12f_fp32` Acc | Table III | Initial: $0.753125$, Ver: $0.747143$ ($\Delta = 0.005982, 0.79\%$) | Initial: $0.753125$, Ver: $0.747143$ | `Phase4_5_Independent_Verification.md` (Item 3) | **PASS** |
| **8** | Discrepancy 4: `tflite_mlp_12f_fp32` F1 | Table III | Initial: $0.732679$, Ver: $0.725414$ ($\Delta = 0.007265, 0.99\%$) | Initial: $0.732679$, Ver: $0.725414$ | `Phase4_5_Independent_Verification.md` (Item 4) | **PASS** |
| **9** | Discrepancy 5: `tflite_mlp_14f_int8` Acc | Table III | Initial: $0.725982$, Ver: $0.750357$ ($\Delta = 0.024375, 3.36\%$) | Initial: $0.725982$, Ver: $0.750357$ | `Phase4_5_Independent_Verification.md` (Item 5) | **PASS** |
| **10** | Discrepancy 6: `tflite_mlp_14f_int8` F1 | Table III | Initial: $0.685213$, Ver: $0.738824$ ($\Delta = 0.053611, 7.82\%$) | Initial: $0.685213$, Ver: $0.738824$ | `Phase4_5_Independent_Verification.md` (Item 6) | **PASS** |
| **11** | Discrepancy 7: `tflite_mlp_12f_int8` Acc | Table III | Initial: $0.749286$, Ver: $0.747857$ ($\Delta = 0.001429, 0.19\%$) | Initial: $0.749286$, Ver: $0.747857$ | `Phase4_5_Independent_Verification.md` (Item 7) | **PASS** |
| **12** | Discrepancy 8: `tflite_mlp_12f_int8` F1 | Table III | Initial: $0.670692$, Ver: $0.715534$ ($\Delta = 0.044842, 6.69\%$) | Initial: $0.670692$, Ver: $0.715534$ | `Phase4_5_Independent_Verification.md` (Item 8) | **PASS** |
| **13** | Discrepancy 9: `pruned_mlp_14f_0pct` Acc | Table III | Initial: $0.726339$, Ver: $0.750000$ ($\Delta = 0.023661, 3.26\%$) | Initial: $0.726339$, Ver: $0.750000$ | `Phase4_5_Independent_Verification.md` (Item 9) | **PASS** |
| **14** | Discrepancy 10: `pruned_mlp_14f_0pct` F1 | Table III | Initial: $0.728019$, Ver: $0.756608$ ($\Delta = 0.028589, 3.93\%$) | Initial: $0.728019$, Ver: $0.756608$ | `Phase4_5_Independent_Verification.md` (Item 10) | **PASS** |
| **15** | Discrepancy 11: `pruned_mlp_14f_25pct` Acc | Table III | Initial: $0.727143$, Ver: $0.750536$ ($\Delta = 0.023393, 3.22\%$) | Initial: $0.727143$, Ver: $0.750536$ | `Phase4_5_Independent_Verification.md` (Item 11) | **PASS** |
| **16** | Discrepancy 12: `pruned_mlp_14f_25pct` F1 | Table III | Initial: $0.730783$, Ver: $0.751490$ ($\Delta = 0.020707, 2.83\%$) | Initial: $0.730783$, Ver: $0.751490$ | `Phase4_5_Independent_Verification.md` (Item 12) | **PASS** |
| **17** | Discrepancy 13: `pruned_mlp_14f_50pct` Acc | Table III | Initial: $0.726964$, Ver: $0.749464$ ($\Delta = 0.022500, 3.10\%$) | Initial: $0.726964$, Ver: $0.749464$ | `Phase4_5_Independent_Verification.md` (Item 13) | **PASS** |
| **18** | Discrepancy 14: `pruned_mlp_14f_50pct` F1 | Table III | Initial: $0.729384$, Ver: $0.756572$ ($\Delta = 0.027188, 3.73\%$) | Initial: $0.729384$, Ver: $0.756572$ | `Phase4_5_Independent_Verification.md` (Item 14) | **PASS** |
| **19** | Discrepancy 15: `pruned_mlp_14f_75pct` Acc | Table III | Initial: $0.739107$, Ver: $0.748214$ ($\Delta = 0.009107, 1.23\%$) | Initial: $0.739107$, Ver: $0.748214$ | `Phase4_5_Independent_Verification.md` (Item 15) | **PASS** |
| **20** | Discrepancy 16: `pruned_mlp_14f_75pct` F1 | Table III | Initial: $0.725546$, Ver: $0.756251$ ($\Delta = 0.030705, 4.23\%$) | Initial: $0.725546$, Ver: $0.756251$ | `Phase4_5_Independent_Verification.md` (Item 16) | **PASS** |
| **21** | Discrepancy 17: `student_a_8_4_int8` Acc | Table III | Initial: $0.710714$, Ver: $0.711429$ ($\Delta = 0.000715, 0.10\%$) | Initial: $0.710714$, Ver: $0.711429$ | `Phase4_5_Independent_Verification.md` (Item 17) | **PASS** |
| **22** | Discrepancy 18: `student_a_8_4_int8` F1 | Table III | Initial: $0.683858$, Ver: $0.684788$ ($\Delta = 0.000930, 0.14\%$) | Initial: $0.683858$, Ver: $0.684788$ | `Phase4_5_Independent_Verification.md` (Item 18) | **PASS** |
| **23** | Discrepancy 19: `student_b_16_4_int8` Acc | Table III | Initial: $0.745000$, Ver: $0.745625$ ($\Delta = 0.000625, 0.08\%$) | Initial: $0.745000$, Ver: $0.745625$ | `Phase4_5_Independent_Verification.md` (Item 19) | **PASS** |
| **24** | Discrepancy 20: `student_b_16_4_int8` F1 | Table III | Initial: $0.689024$, Ver: $0.689601$ ($\Delta = 0.000577, 0.08\%$) | Initial: $0.689024$, Ver: $0.689601$ | `Phase4_5_Independent_Verification.md` (Item 20) | **PASS** |
| **25** | INT8 zero float32 tensors | Abstract, Sec. IV.C, Sec. V.B | $0$ float32 tensors, $8$ int8 tensors | $0$ float32 tensors, $8$ int8 tensors | `Phase4_5_Independent_Verification.md` (Sec. 4) | **PASS** |
| **26** | Pruning 75% active MACs | Sec. IV.D, Sec. V.C | $96$ active MACs ($75\%$ reduction from $384$) | $96$ active MACs | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **27** | Pruning 75% file size | Sec. IV.D, Sec. V.C | $3,920$\,Bytes ($+28$\,B over $3,892$\,B baseline) | $3,920$\,Bytes | `Phase4_5_Independent_Verification.md` (Sec. 6) | **PASS** |
| **28** | Pruning 75% zero weights count | Sec. V.C | $298$ zeroes ($73.34\%$) | $298$ zeroes ($73.34\%$) | `Phase4_5_Independent_Verification.md` (Sec. 6) | **PASS** |
| **29** | Warmup iterations count | Sec. IV.E | $N_{\text{warmup}} \ge 100$ | $100$ warmup iterations | `Phase4_5_Independent_Verification.md` (Sec. 9) | **PASS** |
| **30** | Representative dataset size | Sec. IV.A | $N = 100$ samples from training set | $100$ calibration samples | `Phase4_5_Independent_Verification.md` (Sec. 8) | **PASS** |

---

## 2. Summary Audit Statistics

- **Total Quantitative Claims Audited:** 30
- **Claims Passed (Exact Match):** 30 (100.0%)
- **Claims Mismatched:** 0 (0.0%)
- **Claims Unsupported:** 0 (0.0%)
- **Numerical Audit Status:** **`PASS (100% Verified)`**
