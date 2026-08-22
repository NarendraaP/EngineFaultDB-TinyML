# Paper 4 Final Pre-Submission Checklist

**Paper Title:** *An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims*  
**Audited Manuscript:** [`papers/Paper4_TinyML_Verification/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/paper.tex)  
**Date:** August 20, 2026  

---

## 1. Comprehensive Pre-Submission Checklist

- [x] **[PASS] Manuscript complete:** All 21 required sections and formal environments complete.
- [x] **[PASS] Numerical consistency:** 100% agreement across all 36 quantitative values and Table II discrepancy rows.
- [x] **[PASS] Dataset consistency:** $55,998$ physical records, 4 classes, $40/40/20$ stratified split with `seed=42`.
- [x] **[PASS] Leakage verification:** Scaler fit strictly on train split; $+1.8\%$ threshold leakage bias documented.
- [x] **[PASS] INT8 verification:** All 4 INT8 models verified as `FULL_INT8` ($0$ float32 tensors, $8$ int8 tensors).
- [x] **[PASS] Pruning terminology:** Formally designated as *"computational sparsity without demonstrated storage compression"*.
- [x] **[PASS] MAC terminology:** Formally designated as *"theoretical active MACs"* ($384 \rightarrow 96$).
- [x] **[PASS] Timing terminology:** Formally designated as *"empirical host inference latency on x86_64"*.
- [x] **[PASS] Reference integrity:** 18 peer-reviewed citations in `references.bib`, 100% cited in `paper.tex`.
- [x] **[PASS] Figure integrity:** 4 high-resolution figures (`pareto_frontier.png`, `fp32_vs_int8_accuracy.png`, `accuracy_vs_macs.png`, etc.) accurately labeled.
- [x] **[PASS] Table integrity:** Tables I–II accurately constructed from authoritative verification records.
- [x] **[PASS] Reproducibility:** Reproduction instructions fully documented in `README.md`.
- [x] **[PASS] Novelty/scoping:** Positioned as an empirical software engineering verification framework.
- [x] **[PASS] Paper overlap:** Scoping boundaries strictly preserved against Papers 1, 2, and 3.
- [x] **[PASS] LaTeX compilation:** Programmatically verified syntax, valid package imports, balanced environments.
- [x] **[PASS] No unsupported hardware claims:** Genuine ESP32 deployment explicitly declared as `FUTURE WORK`.

---

## 2. Final Checklist Verdict

```
======================================================================
PAPER 4 SUBMISSION CHECKLIST: 16/16 PASS (100% Verified)
======================================================================
```
