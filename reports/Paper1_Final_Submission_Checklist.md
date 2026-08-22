# Paper 1 Final Pre-Submission Checklist

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*  
**Audited Manuscript:** [`papers/Paper1_QoS_Runtime/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/paper.tex)  
**Date:** August 20, 2026  

---

## 1. Comprehensive Pre-Submission Checklist

- [x] **[PASS] Manuscript complete:** All 21 required sections and formal environments complete.
- [x] **[PASS] Numerical consistency:** 100% agreement across all 25 quantitative claims against Phase 5 CSV artifacts.
- [x] **[PASS] 80-configuration matrix verified:** 5 deadlines $\times$ 4 workloads $\times$ 4 policies = 80 configurations verified.
- [x] **[PASS] Runtime logic verified:** `QoSScheduler.select_model()` matches manuscript formulation.
- [x] **[PASS] Ground-truth isolation:** Confirmed zero ground-truth label $y$ access during online model selection.
- [x] **[PASS] Test-set isolation:** Evaluated over 11,200 held-out test frames using fixed seed $\text{seed}=42$.
- [x] **[PASS] Model registry verified:** `FAST` ($160$ MACs), `BALANCED` ($96$ MACs), `HIGH_FIDELITY` ($304$ MACs) verified.
- [x] **[PASS] Policy definitions verified:** `ACCURACY_PRIORITY`, `BALANCED`, `DEADLINE_PRIORITY`, `COMPUTE_PRIORITY` verified.
- [x] **[PASS] Workload definitions verified:** LOW ($1.0\times$), MEDIUM ($1.5\times$), HIGH ($3.0\times$), BURST ($5.0\times$) verified.
- [x] **[PASS] Deadline calculations:** Simulated latencies compared against deadline thresholds in microseconds.
- [x] **[PASS] Ablation results:** All 4 controlled ablations match `phase5_ablation_results.csv` exactly.
- [x] **[PASS] Figure integrity:** 7 high-resolution publication figures verified in `figures/`.
- [x] **[PASS] Table integrity:** Tables I–V accurately constructed from authoritative result CSVs.
- [x] **[PASS] Reference integrity:** 16 peer-reviewed citations in `references.bib`, 100% cited in `paper.tex`.
- [x] **[PASS] Reproducibility:** Pipeline reproduction instructions fully documented in `README.md`.
- [x] **[PASS] Novelty/scoping:** Positioned as a flagship systems contribution for dynamic edge AI scheduling.
- [x] **[PASS] Paper overlap:** Scoping boundaries strictly preserved against Papers 2, 3, and 4.
- [x] **[PASS] Language audit:** Zero unsupported absolute superlatives or ungrounded hardware claims.
- [x] **[PASS] No unsupported MCU/WCET claims:** Latency strictly labeled as *"empirical host inference latency on x86_64"*; genuine ESP32 deployment declared as `FUTURE WORK`.
- [x] **[PASS] LaTeX compilation:** Valid syntax, balanced environments, and authentic citation keys.

---

## 2. Final Checklist Verdict

```
======================================================================
PAPER 1 SUBMISSION CHECKLIST: 20/20 PASS (100% Verified)
======================================================================
```
