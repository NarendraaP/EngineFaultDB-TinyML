# Paper 1 Final Numerical Consistency Audit

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*  
**Audited Manuscript:** [`papers/Paper1_QoS_Runtime/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/paper.tex)  
**Authoritative References:** [`results/phase5_policy_comparison.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_policy_comparison.csv), [`results/phase5_ablation_results.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_ablation_results.csv), [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv)  
**Audit Date:** August 20, 2026  

---

## 1. Master Numerical Cross-Verification Matrix

| # | Quantitative Metric / Claim Description | Manuscript Value | Authoritative Artifact Value | Source Artifact Reference | Status |
| :---: | :--- | :---: | :---: | :--- | :---: |
| **1** | Total Experimental Configurations | $80$ ($5 \times 4 \times 4$) | $80$ configurations | `phase5_policy_comparison.csv` | **PASS** |
| **2** | Evaluated Test Stream Frames | $11,200$ test frames | $11,200$ test frames | `phase5_runtime_traces.csv` | **PASS** |
| **3** | Mode `FAST` Parameters & Size | $176$ params, $2,976$\,Bytes | $176$ params, $2,976$\,Bytes | `tinyml_model_profile_verified.csv` (Row 10) | **PASS** |
| **4** | Mode `FAST` Active MACs | $160$ active MACs | $160$ active MACs | `tinyml_model_profile_verified.csv` (Row 10) | **PASS** |
| **5** | Mode `FAST` Accuracy & F1 | Acc: $0.716339$, F1: $0.722001$ | Acc: $0.716339$, F1: $0.722001$ | `tinyml_model_profile_verified.csv` (Row 10) | **PASS** |
| **6** | Mode `BALANCED` Parameters & Size | $412$ params, $3,920$\,Bytes | $412$ params, $3,920$\,Bytes | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **7** | Mode `BALANCED` Active MACs | $96$ active MACs | $96$ active MACs | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **8** | Mode `BALANCED` Accuracy & F1 | Acc: $0.748214$, F1: $0.756251$ | Acc: $0.748214$, F1: $0.756251$ | `tinyml_model_profile_verified.csv` (Row 9) | **PASS** |
| **9** | Mode `HIGH_FIDELITY` Parameters & Size | $328$ params, $3,584$\,Bytes | $328$ params, $3,584$\,Bytes | `tinyml_model_profile_verified.csv` (Row 12) | **PASS** |
| **10** | Mode `HIGH_FIDELITY` Active MACs | $304$ active MACs | $304$ active MACs | `tinyml_model_profile_verified.csv` (Row 12) | **PASS** |
| **11** | Mode `HIGH_FIDELITY` Accuracy & F1 | Acc: $0.751429$, F1: $0.738717$ | Acc: $0.751429$, F1: $0.738717$ | `tinyml_model_profile_verified.csv` (Row 12) | **PASS** |
| **12** | $68.4\%$ Active Compute Reduction Claim | $68.4\%$ ($(304-96)/304$) | $(304-96)/304 = 68.421\%$ | Derived from verified MACs | **PASS** |
| **13** | Accuracy Delta under Mode Switch | $-0.37\%$ ($0.751875 \rightarrow 0.748214$) | $0.751875 - 0.748214 = 0.003661$ | `phase5_policy_comparison.csv` | **PASS** |
| **14** | Macro F1 Delta under Mode Switch | $+0.0172$ ($0.739048 \rightarrow 0.756251$) | $0.756251 - 0.739048 = 0.017203$ | `phase5_policy_comparison.csv` | **PASS** |
| **15** | Workload Contention Multipliers | LOW: $1.0\times$, MED: $1.5\times$, HIGH: $3.0\times$, BURST: $5.0\times$ | $1.0, 1.5, 3.0, 5.0$ | `phase5/simulator/trace_simulator.py` | **PASS** |
| **16** | Evaluated Deadline Values | $D \in \{5, 10, 20, 50, 100\}\,\text{ms}$ | $5, 10, 20, 50, 100\,\text{ms}$ | `phase5/run_phase5_pipeline.py` | **PASS** |
| **17** | Policy Table: LOW ACCURACY | Acc: $0.751875$, F1: $0.739048$ | Acc: $0.751875$, F1: $0.739048$ | `phase5_policy_comparison.csv` (Row 2) | **PASS** |
| **18** | Policy Table: LOW BALANCED | Acc: $0.751875$, F1: $0.739048$ | Acc: $0.751875$, F1: $0.739048$ | `phase5_policy_comparison.csv` (Row 3) | **PASS** |
| **19** | Policy Table: LOW DEADLINE | Acc: $0.748214$, F1: $0.756251$ | Acc: $0.748214$, F1: $0.756251$ | `phase5_policy_comparison.csv` (Row 4) | **PASS** |
| **20** | Policy Table: HIGH BALANCED | Acc: $0.748214$, F1: $0.756251$ | Acc: $0.748214$, F1: $0.756251$ | `phase5_policy_comparison.csv` (Row 11) | **PASS** |
| **21** | Policy Table: BURST DEADLINE | Acc: $0.716071$, F1: $0.721781$ | Acc: $0.716071$, F1: $0.721781$ | `phase5_policy_comparison.csv` (Row 16) | **PASS** |
| **22** | Ablation A: Static HF vs QoS | HF Acc: $0.751875$, QoS: $0.748214$ | HF: $0.751875$, QoS: $0.748214$ | `phase5_ablation_results.csv` (Rows 2, 3) | **PASS** |
| **23** | Ablation B: Static Fast vs QoS | Fast Acc: $0.716071$, Gain: $+3.21\%$ | Fast: $0.716071$, Gain: $+0.032143$ | `phase5_ablation_results.csv` (Rows 4, 5) | **PASS** |
| **24** | Ablation C: Workload Awareness | No WL: $0.7519$ ($0$ sw), With WL: $0.7482$ ($1$ sw) | No WL: $0.751875$, With WL: $0.748214$ | `phase5_ablation_results.csv` (Rows 6, 7) | **PASS** |
| **25** | Ablation D: Deadline Gating | Unconstrained P95: $21.83\,\mu\text{s}$, Constrained: $18.49\,\mu\text{s}$ | Unconstrained: $21.8345$, Constrained: $18.4914$ | `phase5_ablation_results.csv` (Rows 8, 9) | **PASS** |

---

## 2. Summary Audit Verdict

```
======================================================================
PAPER 1 FINAL NUMERICAL AUDIT: PASS (100% Agreement)
======================================================================
  Total Numerical Checks:         25
  Exact Matches with Artifacts:   25 (100.0%)
  Discrepancies:                  0
  Unresolved Issues:              0
======================================================================
```
