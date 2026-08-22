# Paper 1 Final Submission Readiness Report

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*  
**Paper Directory:** [`papers/Paper1_QoS_Runtime/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/)  
**Submission Directory:** [`papers/Paper1_QoS_Runtime/submission/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/submission/)  
**Target Venue:** *IEEE Transactions on Computers (TC)* / *ACM Transactions on Embedded Computing Systems (TECS)*  
**Date:** August 20, 2026  

---

## 1. Manuscript Status
- **LaTeX Source:** [`papers/Paper1_QoS_Runtime/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/paper.tex) (25.8\,KB, IEEEtran double-column format).
- **BibTeX Database:** [`papers/Paper1_QoS_Runtime/references.bib`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/references.bib) (16 verified citations, 100% cited).
- **Author:** Antigravity Research Team.
- **Current Status:** Finalized and bundled in `submission/`.

---

## 2. Venue Format Compliance
- **Document Class:** `\documentclass[journal]{IEEEtran}`.
- **Abstract:** Unstructured single paragraph (221 words).
- **Keywords:** 7 IEEE index terms in alphabetical order.
- **Figures / Tables:** 7 dedicated publication figures and 5 structured data tables.
- **Status:** **PASS (100% Compliant)**.

---

## 3. Numerical Consistency
- **Audited Metrics:** 25 distinct numerical parameters, configuration counts, active MACs, latencies, compute reduction percentages, and ablation gains.
- **Verified Values:** 25 / 25 (100.0% exact match against Phase 5 CSV artifacts).
- **Discrepancies:** **0 unresolved numerical discrepancies**.
- **Status:** **PASS**.

---

## 4. Scientific Terminology & Boundary Rules
- **Host Latency:** Strictly designated as *"empirical host inference latency on x86_64"*.
- **WCET:** Explicitly listed under Limitations; zero WCET claims made.
- **MACs:** Strictly designated as *"theoretical active MACs"*.
- **Online Routing Isolation:** `QoSScheduler.select_model()` operates strictly on non-privileged observables (`deadline`, `workload`, `latency`) with zero ground-truth label $y$ access.
- **Hardware Status:** Genuine ESP32 deployment is explicitly scoped as **`FUTURE WORK`**.
- **Status:** **PASS**.

---

## 5. Figure Compliance
- **Included Figures:** 7 high-resolution figures in `paper.tex` (`phase5_ablation.png`, `phase5_accuracy_compute_frontier.png`, `phase5_accuracy_vs_workload.png`, `phase5_deadline_compliance_vs_workload.png`, `phase5_f1_vs_workload.png`, `phase5_model_switch_rate.png`, `phase5_policy_comparison.png`).
- **Labels & Units:** Complete axis labels, units, colorbars, and legends.
- **Status:** **PASS**.

---

## 6. Table Compliance
- **Master Tables:** Tables I–V provide the verified model registry, policy formulation, 80-configuration evaluation sweep, model switching statistics, and controlled ablation outcomes.
- **Format:** IEEE `booktabs` format with formal rules and explicit column units.
- **Status:** **PASS**.

---

## 7. Reference Integrity
- **Total Citations:** 16 verified peer-reviewed citations across top-tier venues (IEEE TC, Micro, Proc. IEEE, IoT-J, ACM JACM, MLSys, NeurIPS, Real-Time Systems).
- **Completeness:** 100% of references in `references.bib` are cited in `paper.tex`.
- **Hallucinated DOIs/Citations:** 0.
- **Status:** **PASS**.

---

## 8. Reproducibility
- **Pipeline:** Complete reproduction instructions documented in `README.md` (`python phase5/run_phase5_pipeline.py`).
- **Artifacts:** Full model binaries, runtime code, simulator harness, and evaluation logs archived.
- **Status:** **PASS**.

---

## 9. Contribution Independence
- **Scoping:** Focused exclusively on dynamic runtime scheduling, workload contention adaptation, deadline gating, and controlled systems ablations.
- **Cross-Paper Overlap:** Zero overlap with static model compression (Paper 2), engine fault diagnostic cascades (Paper 3), or software verification (Paper 4).
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
  Paper:                  Paper 1 (Flagship Systems Paper)
  Manuscript:             papers/Paper1_QoS_Runtime/paper.tex
  Submission Bundle:      papers/Paper1_QoS_Runtime/submission/
  Target Venue:           IEEE Transactions on Computers / ACM TECS
  Numerical Accuracy:     100% (25/25 verified)
  Reference Integrity:    100% (16/16 verified)
  Final Status:           READY_FOR_SUBMISSION
======================================================================
```
