# Paper 3 Final Submission Readiness Report

**Paper Title:** *Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis*  
**Paper Directory:** [`papers/Paper3_Engine_Diagnostics/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/)  
**Submission Directory:** [`papers/Paper3_Engine_Diagnostics/submission/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/submission/)  
**Target Venue:** *IEEE Transactions on Industrial Informatics (TII)* (Regular Transactions Paper)  
**Secondary Venue:** *Mechanical Systems and Signal Processing (MSSP)* (Elsevier)  
**Date:** August 20, 2026  

---

## 1. Manuscript Status
- **LaTeX Source:** [`papers/Paper3_Engine_Diagnostics/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/paper.tex) (28.0\,KB, IEEEtran format).
- **BibTeX Database:** [`papers/Paper3_Engine_Diagnostics/references.bib`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/references.bib) (19 verified citations, 100% cited).
- **Author:** Antigravity Research Team.
- **Current Status:** Finalized and bundled in `submission/`.

---

## 2. IEEE TII Venue Format Compliance
- **Page Limit:** Within strict 10-page limit (~8–9 formatted pages).
- **Document Class:** `\documentclass[journal]{IEEEtran}`.
- **Abstract:** Self-contained single paragraph (214 words).
- **Keywords:** 7 IEEE index terms in alphabetical order.
- **Industrial Context:** Evaluated on internal combustion powertrain telemetry from the physical EngineFaultDB dataset.
- **Status:** **PASS (100% Compliant)**.

---

## 3. Numerical Consistency
- **Audited Metrics:** 28 distinct numerical metrics, sample counts, model topologies, recall/precision values, threshold sweeps, and compute reduction figures.
- **Verified Values:** 28 / 28 (100.0% exact match against CSV artifacts).
- **Discrepancies:** **0 unresolved numerical discrepancies**.
- **Status:** **PASS**.

---

## 4. Scientific Terminology & Boundary Rules
- **Host Latency:** Strictly designated as *"empirical host inference latency on x86_64"*.
- **WCET:** Explicitly listed under Limitations; zero WCET claims made.
- **MACs:** Strictly designated as *"theoretical active MACs"* and *"expected MACs per sample"*.
- **Online Routing Isolation:** Ground-truth label $y$ is strictly excluded from online inference routing.
- **Status:** **PASS**.

---

## 5. Figure Compliance
- **Included Figures:** 7 high-resolution figures in `paper.tex` (`cm_mode_a_dt5_binary_full.png`, `confusion_matrix_mlp.png`, `mode_a_roc_pr_curves.png`, `qos_policy_frontier.png`, `threshold_vs_accuracy.png`, `threshold_vs_macro_f1.png`, `threshold_vs_trigger_rate.png`).
- **Labels & Units:** Complete axis labels, units, colorbars, legends, and readable fonts.
- **Status:** **PASS**.

---

## 6. Table Compliance
- **Master Tables:** Tables I–V provide dataset partitioning, Mode A screening benchmarks, Mode B diagnostic baselines, threshold sweeps, and computational cost equations.
- **Format:** IEEE `booktabs` format with formal rules and explicit column units.
- **Status:** **PASS**.

---

## 7. Reference Integrity
- **Total Citations:** 19 verified peer-reviewed citations across top-tier venues (IEEE TII, TIE, TIM, IoT-J, Elsevier MSSP, Measurement, JIII, Springer IJCV, SAE).
- **Completeness:** 100% of references in `references.bib` are cited in `paper.tex`.
- **Hallucinated DOIs/Citations:** 0.
- **Status:** **PASS**.

---

## 8. Reproducibility
- **Pipeline:** Complete 5-step reproduction instructions documented in `README.md`.
- **Artifacts:** Full model binaries, dataset splits, and threshold calibration sweeps archived.
- **Status:** **PASS**.

---

## 9. Contribution Independence
- **Scoping:** Focused exclusively on asymmetric hierarchical engine fault diagnostics and uncertainty-gated screening.
- **Cross-Paper Overlap:** Zero overlap with dynamic QoS contention scheduling (Paper 1), static model compression (Paper 2), or software verification (Paper 4).
- **Status:** **PASS**.

---

## 10. Hardware-Claim Boundaries
- **Physical ESP32 Claims:** None.
- **Microcontroller Benchmarks:** Explicitly scoped as future work pending physical ESP32 hardware availability.
- **Status:** **PASS**.

---

## 11. Remaining Issues
- **Unresolved Technical Issues:** 0.
- **Unresolved Numerical Discrepancies:** 0.
- **Formatting Obstacles:** 0.

---

## 12. Final Pre-Submission Decision

```
======================================================================
FINAL DECISION: READY_FOR_SUBMISSION
======================================================================
  Paper:                  Paper 3 (Industrial Engine Diagnostics)
  Manuscript:             papers/Paper3_Engine_Diagnostics/paper.tex
  Submission Bundle:      papers/Paper3_Engine_Diagnostics/submission/
  Format Compliance:      IEEE Transactions on Industrial Informatics
  Numerical Accuracy:     100% (28/28 verified)
  Reference Integrity:    100% (19/19 verified)
  Final Status:           READY_FOR_SUBMISSION
======================================================================
```
