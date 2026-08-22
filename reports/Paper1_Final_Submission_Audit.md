# Paper 1 Final Publication Audit Report (Flagship Systems Paper)

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*  
**Paper Directory:** [`papers/Paper1_QoS_Runtime/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/)  
**Submission Directory:** [`papers/Paper1_QoS_Runtime/submission/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/submission/)  
**Target Venue:** *IEEE Transactions on Computers (TC)* / *ACM Transactions on Embedded Computing Systems (TECS)*  
**Date:** August 20, 2026  

---

## 1. Audit Objective
Conduct an exhaustive scientific, systems, and publication readiness audit of Paper 1, ensuring 100% numerical consistency with Phase 5 CSV artifacts, strict ground-truth non-leakage, rigorous boundary preservation against Papers 2–4, and zero unsupported hardware claims.

---

## 2. Manuscript Inventory
- **LaTeX Source:** [`papers/Paper1_QoS_Runtime/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/paper.tex) (25.8\,KB, standard IEEEtran double-column format).
- **BibTeX Database:** [`papers/Paper1_QoS_Runtime/references.bib`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/references.bib) (16 verified citations, 100% cited).
- **Supporting Files:** [`README.md`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/README.md), [`Paper1_Evidence_Map.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Paper1_Evidence_Map.md).
- **Publication Figures:** 7 dedicated figures in `figures/` (`phase5_ablation.png`, `phase5_accuracy_compute_frontier.png`, `phase5_accuracy_vs_workload.png`, `phase5_deadline_compliance_vs_workload.png`, `phase5_f1_vs_workload.png`, `phase5_model_switch_rate.png`, `phase5_policy_comparison.png`).

---

## 3. Authoritative Evidence Sources
All claims in Paper 1 are anchored to:
- [`results/phase5_policy_comparison.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_policy_comparison.csv)
- [`results/phase5_ablation_results.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_ablation_results.csv)
- [`results/phase5_model_switch_statistics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_model_switch_statistics.csv)
- [`results/phase5_runtime_traces.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_runtime_traces.csv)
- [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv)

---

## 4. Numerical Verification
- **Audited Parameters:** 25 distinct quantitative metrics, sample counts, active MACs, latencies, compute reduction percentages, and ablation gains.
- **Pass Rate:** 25 / 25 (100.0% exact match).
- **Discrepancies:** 0.

---

## 5. 80-Configuration Experiment Verification
- **Matrix Formulation:** 5 deadlines ($5, 10, 20, 50, 100$\,ms) $\times$ 4 workloads (LOW, MEDIUM, HIGH, BURST) $\times$ 4 policies (`ACCURACY_PRIORITY`, `BALANCED`, `DEADLINE_PRIORITY`, `COMPUTE_PRIORITY`) = 80 distinct configurations evaluated across 11,200 held-out test frames.
- **Verification:** Verified all 80 rows in `results/phase5_policy_comparison.csv`.

---

## 6. Runtime Decision Logic
- **Architecture:** The runtime formalizes 3 operational modes (`FAST`, `BALANCED`, `HIGH_FIDELITY`) selected online by `QoSScheduler.select_model()`.
- **Implementation:** Code in `phase5/runtime/qos_runtime.py` exactly implements the 4 policies described in Section VI.

---

## 7. Ground-Truth Isolation
- **Online Non-Leakage:** Audited `phase5/runtime/qos_runtime.py` (lines 83–153). The model selector accepts strictly `(deadline_ms, workload, current_latency_us)` with zero access to `y_test`. Ground truth is used exclusively in post-hoc trace evaluation.

---

## 8. Test-Set Isolation
- **Dataset Partitioning:** 55,998 samples split into $40\%$ train ($22,399$), $40\%$ validation ($22,399$), and $20\%$ test ($11,200$) with $\text{seed}=42$.
- **Scaler Isolation:** `MinMaxScaler` fit strictly on train split; zero test-set leakage.

---

## 9. Model Registry Verification
- **Modes:**
  - `FAST`: `student_a_8_4_fp32` (176 params, 2,976 B, 160 MACs, 0.716339 acc)
  - `BALANCED`: `pruned_mlp_14f_75pct` (412 params, 3,920 B, 96 MACs, 0.748214 acc)
  - `HIGH_FIDELITY`: `student_b_16_4_fp32` (328 params, 3,584 B, 304 MACs, 0.751429 acc)
- **Status:** PASS (Exact match with `tinyml_model_profile_verified.csv`).

---

## 10. Policy Verification
- **Behaviors:**
  - `ACCURACY_PRIORITY`: Prefers `HIGH_FIDELITY` ($304$ MACs).
  - `BALANCED`: Proactively switches to `BALANCED` ($96$ MACs) under `HIGH` or `BURST` contention.
  - `DEADLINE_PRIORITY`: Aggressively selects `FAST` ($160$ MACs) during bursts.
  - `COMPUTE_PRIORITY`: Prefers `BALANCED` ($96$ MACs).
- **Status:** PASS.

---

## 11. Workload Verification
- **Contention Multipliers:** LOW ($1.0\times$), MEDIUM ($1.5\times$), HIGH ($3.0\times$), BURST ($5.0\times$) in `phase5/simulator/trace_simulator.py`.
- **Status:** PASS.

---

## 12. Deadline Verification
- **Deadlines:** $5, 10, 20, 50, 100$\,ms evaluated with compliance tracked in `results/phase5_policy_comparison.csv`.
- **Status:** PASS.

---

## 13. Ablation Verification
- **Controlled Ablations:** All 4 ablations match `phase5_ablation_results.csv` exactly:
  - Ablation A: Static Best vs QoS ($-68.4\%$ MACs, $+0.0173$ F1)
  - Ablation B: Static Fast vs QoS ($+3.21\%$ accuracy gain)
  - Ablation C: Workload awareness vs static
  - Ablation D: Deadline gating vs unconstrained
- **Status:** PASS.

---

## 14. Computational Accounting
- **Terminology:** Formally designated as *"theoretical active MACs"*.
- **The $68.4\%$ Claim:** Derived from $(304 - 96) / 304 = 68.421\% \approx 68.4\%$.
- **Status:** PASS.

---

## 15. Latency Verification
- **Terminology:** Single-sample execution times are strictly designated as *"empirical host inference latency on x86_64"*.
- **WCET:** Zero claims of embedded WCET or hard real-time guarantees.
- **Status:** PASS.

---

## 16. ESP32 / Hardware Claim Audit
- **Hardware Status:** Genuine ESP32 deployment is explicitly scoped as **`FUTURE WORK`**.
- **Status:** PASS.

---

## 17. Figure Audit
- **Verification:** 7 high-resolution publication figures verified in `figures/`. All axes, units, legends, and data points reflect verified CSV logs.
- **Status:** PASS.

---

## 18. Table Audit
- **Verification:** Tables I–V accurately constructed from authoritative result CSVs in IEEE `booktabs` format.
- **Status:** PASS.

---

## 19. Reproducibility Audit
- **Reproduction Pipeline:** Documented in `README.md` (`python phase5/run_phase5_pipeline.py`).
- **Status:** PASS.

---

## 20. Reference Audit
- **Coverage:** 16 / 16 citations in `references.bib` actively cited in `paper.tex` (100% synchronized).
- **Authenticity:** All 16 citations verified in top-tier venues (IEEE TC, Micro, Proc. IEEE, IoT-J, ACM JACM, MLSys, NeurIPS, Real-Time Systems).
- **Status:** PASS.

---

## 21. Novelty Audit
- **Positioning:** Grounded as a trace-driven multi-fidelity TinyML runtime that dynamically trades model fidelity against computational demand under CPU contention.
- **Wording:** Bounded by empirical evidence; unsupported absolute superlatives removed.
- **Status:** PASS.

---

## 22. Paper Overlap Audit
- **Boundary Preservation:** Scoping strictly decoupled from Paper 2 (model compression), Paper 3 (engine diagnostics), and Paper 4 (software verification).
- **Status:** PASS.

---

## 23. Language Audit
- **Scan Results:** 0 instances of over-claiming language ("world's first", "hard real-time guarantee", "WCET", "production-ready").
- **Status:** PASS.

---

## 24. LaTeX Build Audit
- **Source Integrity:** Verified syntax, package imports, table alignments, and BibTeX keys. Ready for standard IEEE PDF generation.
- **Status:** PASS.

---

## 25. Corrections Applied
- Synchronized title to *"QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention"*.
- Configured document class to standard IEEE Transactions (`\documentclass[journal]{IEEEtran}`).
- Synchronized all 16 BibTeX references with 100% active citations in text.
- Added explicit `\section{Reproducibility}` before `\section{Future Hardware Validation}`.

---

## 26. Remaining Issues
- **Unresolved Technical Issues:** 0.
- **Unresolved Numerical Discrepancies:** 0.
- **Submission Blockers:** 0.

---

## 27. Final Decision

```
======================================================================
PAPER 1 FINAL PUBLICATION STATUS
======================================================================

STATUS: READY_FOR_SUBMISSION

======================================================================
Submission Package Files:
  - papers/Paper1_QoS_Runtime/submission/paper.tex
  - papers/Paper1_QoS_Runtime/submission/references.bib
  - papers/Paper1_QoS_Runtime/submission/README.md
  - papers/Paper1_QoS_Runtime/submission/Paper1_Evidence_Map.md
  - papers/Paper1_QoS_Runtime/submission/figures/*
======================================================================
```
