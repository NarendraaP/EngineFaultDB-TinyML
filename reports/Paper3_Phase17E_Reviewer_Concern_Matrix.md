# Phase 17E — Reviewer Concern Matrix: Paper 3

**Manuscript:** Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis  
**Target Venue:** IEEE Transactions on Industrial Informatics (TII)  
**Alternative Venues:** IEEE Sensors Journal / Mechanical Systems and Signal Processing (MSSP)  
**Date:** August 28, 2026  

---

## 1. Comprehensive Reviewer Concern Matrix

| # | Reviewer Concern | Severity | Existing Evidence in Project | Can Fix with Existing Evidence? | New Analysis Needed? | New Experiment Needed? | Decision & Action |
|---|---|:---:|---|:---:|:---:|:---:|---|
| **1** | **Missing Strong Flat Multiclass Baselines** | **HIGH** | `results/baseline_metrics.csv` contains flat Decision Tree ($69.16\%$ acc, $0.6821$ F1) and Logistic Regression ($58.00\%$ acc, $0.5786$ F1). | **YES** | **YES** | **NO** | Incorporate flat Decision Tree and flat Logistic Regression into Table IV (Baseline Comparison) to contextualize the MLP and cascade performance. |
| **2** | **Temporal Fault-Persistence Discussion** | **HIGH** | `EngineFaultDB_Final.csv` contains 55,998 static, independent sensor vectors without timestamps or session IDs. | **YES** | **YES** | **NO** | Conclude that temporal persistence cannot be legitimately evaluated on this tabular dataset. Add a dedicated discussion on sequential filtering (Kalman/Markov) and elevate it as an explicit limitation. |
| **3** | **Hierarchical Classification is Already Established** | **HIGH** | Extensive literature (Viola-Jones, BranchyNet, industrial cascaded diagnostics). | **YES** | **YES** | **NO** | Remove any implication that hierarchical routing is universally novel. Frame the contribution as a domain-specific, asymmetric multi-paradigm cascade (tree screening + neural diagnostician) tailored for multi-sensor powertrain diagnostics. |
| **4** | **Single-Dataset / Lab-Bench Domain Validation** | **MEDIUM** | EngineFaultDB physical dynamometer benchmark (55,998 records). | **YES** | **NO** | **NO** | Acknowledge single-dataset scope; clearly describe dynamometer test-bench conditions and state cross-vehicle / on-road drive-cycle validation as future work. |
| **5** | **Steady-State Dynamometer Data vs. Dynamic Driving** | **MEDIUM** | Dataset captures stationary engine operating states. | **YES** | **NO** | **NO** | Explicitly discuss steady-state dynamometer instrumentation vs. transient on-road driving dynamics in Section XII (Limitations). |
| **6** | **Nominal-Operation Prior Assumption (89.8% compute)** | **CRITICAL** | Mathematical derivation: $r_B = 0.10 \times 0.9960 + 0.90 \times (1 - 0.9975) = 0.10185 \implies 89.8\%$ reduction. | **YES** | **YES** | **NO** | Strictly distinguish the measured test-set compute reduction ($26.36\%$) from the derived/projected reduction under the $90\%$ nominal prior ($89.8\%$). Never present $89.8\%$ as a direct empirical test-set measurement. |
| **7** | **Class-Specific Error Analysis (Misfire vs. Air Leak Confusion)** | **MEDIUM** | Per-class breakdown in Table II: Class 0 ($99.8\%$ F1), Class 1 ($98.7\%$ F1), Class 2 ($52.6\%$ F1), Class 3 ($50.6\%$ F1). | **YES** | **YES** | **NO** | Provide a domain-grounded physical explanation of why ignition misfires (Class 2) and intake air leaks (Class 3) exhibit sensor overlap under steady-state conditions. |
| **8** | **Distinguish Measured Results vs. Operational Estimates** | **CRITICAL** | Test set metrics ($26.36\%$, $74.64\%$, $99.98\%$) vs. projected $90\%$ nominal stream ($89.8\%$). | **YES** | **YES** | **NO** | Add explicit labels in all text and tables: `[MEASURED TEST SET]` vs. `[DERIVED OPERATIONAL ESTIMATE]`. |
| **9** | **Lack of Physical ECU / Microcontroller Validation** | **HIGH** | Evidence tiering: Tier 1/2 software validation on x86; no physical ECU deployment. | **YES** | **NO** | **NO** | Transparently disclose that all computational reductions are reported in theoretical active MACs and host timings. Physical on-vehicle ECU profiling is declared as future work. |

---

## 2. Summary of Decisions

1. **New Experiments Required:** **NONE.** All concerns can be resolved using existing verified results (`results/baseline_metrics.csv`, `results/qos_threshold_sweep_test.csv`, and `results/mode_selection_metrics.csv`).
2. **Analysis Required:**
   - Integrate flat Decision Tree and flat Logistic Regression baselines into Table IV.
   - Clarify the mathematical distinction between the directly measured $26.36\%$ test-set reduction and the derived $89.8\%$ operational reduction.
   - Document the physical sensor overlap causing Class 2/3 confusion.
   - Document the static tabular nature of the dataset and the absence of temporal timestamps.
