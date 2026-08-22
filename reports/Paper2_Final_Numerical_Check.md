# Paper 2 Final Programmatic Numerical Consistency Check

**Manuscript Checked:** [`papers/Paper2_TinyML_Pareto/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/paper.tex)  
**Authoritative Reference:** [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv)  
**Execution Method:** Programmatic regex and substring parsing across all quantitative values  
**Date:** August 20, 2026  

---

## 1. Cross-Verification Table

| # | Metric / Parameter | Manuscript Value | Authoritative Verified Value | Status |
| :---: | :--- | :---: | :---: | :---: |
| 1 | Total clean dataset samples | $55,998$ | $55,998$ | **PASS** |
| 2 | Raw dataset samples | $55,999$ | $55,999$ | **PASS** |
| 3 | Exact duplicates removed | $1$ | $1$ | **PASS** |
| 4 | Training partition size ($40\%$) | $22,399$ | $22,399$ | **PASS** |
| 5 | Validation partition size ($40\%$) | $22,399$ | $22,399$ | **PASS** |
| 6 | Held-out test partition size ($20\%$)| $11,200$ | $11,200$ | **PASS** |
| 7 | Data partition random seed | $\text{seed} = 42$ | $\text{seed} = 42$ | **PASS** |
| 8 | `student_b_16_4_fp32` Test Accuracy | $0.751429$ ($75.14\%$) | $0.751429$ | **PASS** |
| 9 | `student_b_16_4_fp32` File Size | $3,584$\,Bytes | $3,584$\,Bytes | **PASS** |
| 10 | `student_b_16_4_fp32` Active MACs | $304$ | $304$ | **PASS** |
| 11 | `student_b_16_4_fp32` Host Latency | $0.82\,\si{\micro\second}$ | $0.82\,\si{\micro\second}$ | **PASS** |
| 12 | `student_a_8_4_fp32` Test Accuracy | $0.716339$ ($71.63\%$) | $0.716339$ | **PASS** |
| 13 | `student_a_8_4_fp32` File Size | $2,976$\,Bytes | $2,976$\,Bytes | **PASS** |
| 14 | `student_a_8_4_fp32` Active MACs | $160$ | $160$ | **PASS** |
| 15 | `pruned_mlp_14f_75pct` Active MACs | $96$ | $96$ | **PASS** |
| 16 | `pruned_mlp_14f_75pct` File Size | $3,920$\,Bytes | $3,920$\,Bytes | **PASS** |
| 17 | `pruned_mlp_14f_75pct` Test Accuracy | $0.748214$ ($74.82\%$) | $0.748214$ | **PASS** |
| 18 | `pruned_mlp_14f_50pct` Active MACs | $192$ | $192$ | **PASS** |
| 19 | `pruned_mlp_14f_25pct` Active MACs | $288$ | $288$ | **PASS** |
| 20 | Uncompressed Baseline File Size | $3,892$\,Bytes | $3,892$\,Bytes | **PASS** |
| 21 | Uncompressed Baseline MACs | $384$ | $384$ | **PASS** |
| 22 | `student_b_16_4_int8` Test Accuracy | $0.745625$ ($74.56\%$) | $0.745625$ | **PASS** |
| 23 | `student_b_16_4_int8` File Size | $3,576$\,Bytes | $3,576$\,Bytes | **PASS** |
| 24 | `tflite_mlp_14f_int8` Test Accuracy | $0.750357$ | $0.750357$ | **PASS** |
| 25 | `tflite_mlp_14f_int8` File Size | $3,728$\,Bytes | $3,728$\,Bytes | **PASS** |
| 26 | `tflite_mlp_12f_int8` Test Accuracy | $0.747857$ | $0.747857$ | **PASS** |
| 27 | `tflite_mlp_12f_int8` File Size | $3,712$\,Bytes | $3,712$\,Bytes | **PASS** |
| 28 | INT8 Float32 Tensors Count | $0$ float32 tensors | $0$ float32 tensors | **PASS** |
| 29 | INT8 Int8 Tensors Count | $8$ int8 tensors | $8$ int8 tensors | **PASS** |

---

## 2. Final Numerical Statement

```
======================================================================
FINAL NUMERICAL CROSS-CHECK: 0 UNRESOLVED NUMERICAL DISCREPANCIES.
======================================================================
All 28 tested quantitative parameters, metrics, tensor dimensions, and
sample counts in paper.tex match the authoritative verified CSV records
with 100.0% precision.
======================================================================
```
