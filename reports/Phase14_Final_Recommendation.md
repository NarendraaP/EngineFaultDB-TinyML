# Phase 14: Final Scientific Recommendation & Submission Readiness
**Audit Date:** August 22, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  
**Final Scope:** Complete 4-Manuscript Portfolio (Paper 1 through Paper 4)  

---

## 1. Master Portfolio Ranking & Defensibility Summary

| Paper | Highest Defensible Novelty Level | Novelty Confidence | SOTA Status | Main Prior-Art Threat | Main Defensible Contribution | Submission Readiness |
| :--- | :---: | :---: | :--- | :--- | :--- | :---: |
| **Paper 1** (QoS Runtime) | **Level 2** (Novel Combination) | **8.5 / 10** | SOTA-WITHIN-DEFINED-REGIME | Dynamic early-exit networks (FreeML, BranchyNet) on edge GPUs/CPUs. | Ground-truth-independent closed-loop QoS scheduler managing an ensemble of verified sub-4KB TFLite models under CPU contention. | **SUBMIT-AFTER-MINOR-REFRAMING** |
| **Paper 2** (TinyML Pareto) | **Level 3** (Empirical Characterization) | **9.0 / 10** | STRONG-EMPIRICAL-RESULT | MLPerf Tiny reference benchmarks and generic compression surveys. | Unified 4-paradigm empirical Pareto mapping on identical splits + FlatBuffer discovery that magnitude pruning yields zero file size reduction in standard TFLite. | **SUBMIT-AFTER-MINOR-REFRAMING** |
| **Paper 3** (Engine Diagnostics) | **Level 1–2** (Domain Integration) | **8.8 / 10** | STRONG-EMPIRICAL-RESULT | Generic cascaded classifiers and industrial IoT anomaly screeners. | Asymmetric 2-tier diagnostic cascade exploiting nominal operational prior dominance ($>90\%$) with zero-leakage validation threshold calibration. | **SUBMIT-AFTER-MINOR-REFRAMING** |
| **Paper 4** (Verification Framework) | **Level 3–4** (Methodological Framework) | **9.5 / 10** | SOTA-ESTABLISHED | High-level MLOps Model Cards and general ML reproducibility checklists. | 7-dimensional verification taxonomy for compiled TinyML artifacts, uncovering 20 discrepancies and proving the $+1.80\%$ threshold leakage bias. | **SUBMIT-AFTER-MINOR-REFRAMING** |

---

## 2. Final Submission Classification by Manuscript

1. **Paper 1:** **SUBMIT-AFTER-MINOR-REFRAMING**  
   - *Reframing Completed:* Scoped strictly as a trace-driven simulation study; claims of hardware energy or MCU WCET guarantees are completely omitted; 68.4% compute reduction explicitly specified as theoretical active MACs.
2. **Paper 2:** **SUBMIT-AFTER-MINOR-REFRAMING**  
   - *Reframing Completed:* Formally presented as an empirical 4D Pareto characterization and low-level FlatBuffer audit rather than a new algorithmic compression method.
3. **Paper 3:** **SUBMIT-AFTER-MINOR-REFRAMING**  
   - *Reframing Completed:* Framed as a domain-specific asymmetric compute optimization exploiting physical nominal-state prior dominance ($>90\%$) with zero-leakage threshold calibration.
4. **Paper 4:** **SUBMIT-AFTER-MINOR-REFRAMING**  
   - *Reframing Completed:* Framed as an empirical verification protocol demonstrated on an end-to-end TinyML case study and extensible to general Edge AI pipelines.

---

## 3. Answer to the Central Reviewer Question

> **“If I submit these four papers to knowledgeable IEEE/ACM reviewers in 2026, what are the strongest legitimate reasons they could reject each paper, and what is the minimum change required to make each contribution scientifically defensible?”**

### 📄 Paper 1 (QoS Runtime)
- **Strongest Legitimate Rejection Reason:** *"The paper is a trace-driven simulation study using synthetic contention multipliers and host-measured execution times rather than physical MCU measurements on an ARM Cortex-M or ESP32 running FreeRTOS."*
- **Minimum Change Required for Defensibility:** The manuscript must explicitly disclaim hardware WCET and hardware energy claims in the Abstract, Introduction, and Threats to Validity, framing the contribution strictly as an algorithmic systems simulation of closed-loop QoS scheduling for micro-models. *(Fully implemented in current manuscript).*

### 📄 Paper 2 (TinyML Pareto)
- **Strongest Legitimate Rejection Reason:** *"The compression techniques evaluated (PTQ INT8, magnitude pruning, KD, feature selection) are standard methods. The paper lacks a new algorithmic compression formulation."*
- **Minimum Change Required for Defensibility:** The manuscript must present the work explicitly as an *empirical Pareto characterization and low-level FlatBuffer artifact benchmark*, focusing heavily on the critical finding that standard TFLite FlatBuffers store pruned zeros as dense floats (,920\,\text{B}$). *(Fully implemented in current manuscript).*

### 📄 Paper 3 (Engine Diagnostics)
- **Strongest Legitimate Rejection Reason:** *"Hierarchical/cascaded classification is a textbook technique. What is the fundamental novelty beyond applying a decision tree before an MLP?"*
- **Minimum Change Required for Defensibility:** The manuscript must emphasize the physical powertrain domain insight ($>90\%$ nominal operation), the mathematical expected cost formulation ($\mathbb{E}[C] = C_A + r_B C_B$), and the rigorous validation-only threshold calibration that achieves .8\%$ compute reduction with .98\%$ anomaly safety. *(Fully implemented in current manuscript).*

### 📄 Paper 4 (Verification Framework)
- **Strongest Legitimate Rejection Reason:** *"The 7-D taxonomy is evaluated on a single case study of 12 tabular diagnostic models. Can it genuinely be called a universal verification framework?"*
- **Minimum Change Required for Defensibility:** The manuscript must tone down claims of 'universal framework' and frame the contribution as an *independent verification protocol for compiled TinyML artifacts, empirically validated on an end-to-end Edge AI diagnostic pipeline*. *(Fully implemented in current manuscript).*

---

## 4. Final Verdict: Ready for Phase 15 Manuscript Refinements
All 4 manuscripts are scientifically sound, completely unconfounded, and accompanied by camera-ready 300 DPI figures and clean LaTeX sources. Proceed to Phase 15 for any final line-level text polishing.
