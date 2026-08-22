# Paper 4 Final Publication Audit Report

**Paper Title:** *An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims*  
**Paper Directory:** [`papers/Paper4_TinyML_Verification/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/)  
**Submission Directory:** [`papers/Paper4_TinyML_Verification/submission/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/submission/)  
**Target Venue:** *IEEE Transactions on Software Engineering (TSE)* / *ACM Transactions on Software Engineering and Methodology (TOSEM)*  
**Date:** August 20, 2026  

---

## 1. Audit Objective
Conduct an independent, line-by-line scientific and publication readiness audit of Paper 4, ensuring 100% agreement with authoritative project artifacts, strict boundary preservation against Papers 1–3, and zero unsupported hardware claims.

---

## 2. Manuscript Inventory
- **LaTeX Source:** [`papers/Paper4_TinyML_Verification/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/paper.tex) (24.8\,KB, standard IEEEtran double-column format).
- **BibTeX Database:** [`papers/Paper4_TinyML_Verification/references.bib`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/references.bib) (18 verified citations, 100% cited).
- **Supporting Documentation:** [`README.md`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/README.md), [`Paper4_Evidence_Map.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Paper4_Evidence_Map.md).
- **Publication Figures:** 3 dedicated case-study figures in `figures/` (`pareto_frontier.png`, `fp32_vs_int8_accuracy.png`, `accuracy_vs_macs.png`).

---

## 3. Numerical Verification
- **Audit Findings:** 36 distinct quantitative parameters, sample counts, tensor counts, and discrepancy metrics audited programmatically against `results/tinyml_model_profile_verified.csv` and `reports/Phase4_5_Independent_Verification.md`.
- **Pass Rate:** 36 / 36 (100.0% exact match).
- **Discrepancies:** 0 unresolved discrepancies.

---

## 4. Leakage Verification
- **Scaler Isolation:** Verified that `MinMaxScaler` is fit strictly on the training partition ($22,399$ samples) and transformed onto validation ($22,399$) and test ($11,200$) partitions.
- **Split Isolation:** Verified disjoint index sets with fixed seed ($\text{seed}=42$).
- **Runtime Non-Leakage:** Audited `phase5/runtime/qos_runtime.py` to confirm that online routing functions have zero access to ground truth $y$.

---

## 5. Quantization Verification
- **Audit Findings:** Low-level tensor inspection of the 4 INT8 candidate models confirms verified **`FULL_INT8`** status:
  - Input: `int8`
  - Output: `int8`
  - Weights & Activations: `int8`
  - Biases: `int32`
  - Float32 Tensors: Exactly $0$ float32 tensors.

---

## 6. Sparsity Verification
- **Terminology:** Formally enforced as *"computational sparsity without demonstrated storage compression"*.
- **Findings:** $75\%$ magnitude pruning achieves $298$ zero weights ($73.34\%$), but serialized FlatBuffer file size remains dense at $3,920$\,Bytes ($+28$\,B over unpruned baseline).

---

## 7. MAC Verification
- **Terminology:** Formally designated as *"theoretical active MACs"* ($384 \rightarrow 96$ active MACs).
- **Hardware Distinction:** Explicitly states that theoretical active MAC reduction does not guarantee hardware execution speedup on dense matrix engines.

---

## 8. Timing Verification
- **Terminology:** Single-sample execution times are strictly designated as *"empirical host inference latency on x86_64"*.
- **WCET Distinction:** Zero claims of embedded WCET, ECU latencies, or real-time guarantees.

---

## 9. Seven-Dimension Taxonomy Audit
The manuscript fully details all 7 operational dimensions:
1. Data Isolation
2. Serialized Binary Integrity
3. Quantization Graph Inspection
4. Sparsity & Storage Accounting
5. Computation Accounting
6. Timing Protocols
7. Runtime Non-Leakage & Deployment Claim Boundaries

---

## 10. +1.8% Leakage-Bias Reproduction
- **Finding:** Optimizing threshold gating parameters directly on held-out test data produces an artificial $+1.8\%$ optimistic accuracy bias relative to unbiased validation-calibrated thresholding ($74.64\%$). This confirms the necessity of split-isolated calibration.

---

## 11. Reference Audit
- **Database Audited:** `references.bib` (18 citations).
- **Coverage:** 18 / 18 cited in `paper.tex` (100% synchronized).
- **Authenticity:** All 18 citations verified in top-tier software engineering and machine learning venues (IEEE TSE, Micro, JMLR, NeurIPS, ICSE, MLSys).

---

## 12. Figure and Table Audit
- **Figures:** 3 high-resolution case-study figures verified.
- **Tables:** Table I (Taxonomy) and Table II (Comprehensive 20-row Discrepancy Table) accurately formatted in IEEE `booktabs` style.

---

## 13. Reproducibility Audit
- **Pipeline:** Complete reproduction instructions provided in `README.md` (`scripts/phase4_5_verification.py`).

---

## 14. Novelty Audit
- **Positioning:** Grounded as an empirical software engineering framework and methodology for TinyML artifact verification.
- **Wording:** All claims bounded by empirical evidence; unsupported absolute superlatives removed.

---

## 15. Paper Overlap Audit
- **Boundary Preservation:** Scoping strictly decoupled from Paper 1 (QoS systems), Paper 2 (static compression), and Paper 3 (engine diagnostics).
- **Status:** PASS (Independent Software Engineering publication).

---

## 16. Language Audit
- **Scan Results:** 0 instances of over-claiming language ("first ever", "world's first", "guaranteed real-time", "production-ready").

---

## 17. LaTeX Build Audit
- **Source Integrity:** Verified syntax, package imports, table alignments, and BibTeX keys. Ready for standard IEEE PDF generation.

---

## 18. Corrections Applied
- Synchronized document class to standard IEEE Transactions (`\documentclass[journal]{IEEEtran}`).
- Synchronized all 18 BibTeX references with 100% active citations in text.
- Added explicit sample counts ($55,998$, $22,399$, $22,399$, $11,200$, $\text{seed}=42$) to Section V case study.

---

## 19. Remaining Issues
- **Unresolved Technical Issues:** 0.
- **Unresolved Numerical Discrepancies:** 0.
- **Submission Blockers:** 0.

---

## 20. Final Decision

```
======================================================================
PAPER 4 FINAL PUBLICATION STATUS
======================================================================

STATUS: READY_FOR_SUBMISSION

======================================================================
Submission Package Files:
  - papers/Paper4_TinyML_Verification/submission/paper.tex
  - papers/Paper4_TinyML_Verification/submission/references.bib
  - papers/Paper4_TinyML_Verification/submission/README.md
  - papers/Paper4_TinyML_Verification/submission/Paper4_Evidence_Map.md
  - papers/Paper4_TinyML_Verification/submission/figures/*
======================================================================
```
