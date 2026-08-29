# Phase 20 — Cross-Paper Independence & Novelty Separation Audit

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** Verification of Unique Scientific Questions and Contribution Separation Across Papers 1–5  
**Date:** August 29, 2026  

---

## 1. Objective

To prevent redundant or overlapping publication claims, this audit evaluates the research questions, methodological cores, and unique scientific contributions across all five manuscripts, confirming that no paper relies on another paper's primary contribution as its own novel thesis.

---

## 2. Independence and Contribution Mapping

| Paper | Shared Hardware Evidence | Unique Research Question & Primary Novel Contribution | Distinct Target Audience / Field |
|---|---|---|---|
| **Paper 1** | Candidate model feasibility ($64.55\text{--}89.90\,\si{\micro\second}$) | **QoS-Aware Dynamic Multi-Fidelity Runtime:** How can embedded systems dynamically switch between heterogeneous candidate models to maintain deterministic deadline compliance under fluctuating computational workloads? | Real-Time Systems, Operating Systems & Embedded Systems Architecture (**IEEE TC**) |
| **Paper 2** | Hardware latency corroboration ($28.20\%$ speedup) | **Multi-Objective Pareto Model Compression:** What is the optimal Pareto trade-off between task accuracy, serialized storage footprint, and active MAC count under structured pruning versus channel distillation? | Design Automation, Hardware-Software Co-Design & ML Compression (**ACM TODAES**) |
| **Paper 3** | Stage-1 screening model latency ($64.55\,\si{\micro\second}$) | **Cascaded Hierarchical Edge Diagnostics:** How can a two-stage anomaly screening cascade achieve near-perfect anomaly recall ($99.98\%$) while slashing average computational workload by $89.8\%$ for industrial engine telemetry? | Industrial Electronics, Condition Monitoring & Applied AI (**IEEE TII**) |
| **Paper 4** | Physical deployment case study verification | **Artifact-Driven Verification Protocol & Defect Taxonomy:** What executable software engineering verification procedures are required to identify and eliminate training-to-deployment defects in compiled TinyML binaries? | Software Engineering, Quality Assurance & Empirical Systems (**ACM LCTES / IEEE Software**) |
| **Paper 5** | Full physical characterization ($N=24,000$, zero-I/O timing, memory accounting) | **Empirical Silicon Characterization & Host Translation Gap:** What are the empirical latency distributions, parameter scaling behaviors, memory subsystem footprints, and host-to-silicon translation divergences for sub-4 KB INT8 models on commercial microcontrollers? | Embedded Computing, IoT Systems & Edge Hardware Benchmarking (**ACM TECS / IEEE IoT-J / IEEE TCAD**) |

---

## 3. Detailed Separation Analysis

1. **Paper 1 vs. Paper 5:**
   * *Paper 1* is an algorithmic and runtime systems paper introducing dynamic QoS degradation policies, multi-fidelity scheduling state machines, and contention handling. It utilizes the ESP32 latency only as a grounding check for model execution bounds.
   * *Paper 5* is an empirical hardware characterization study presenting deep microarchitectural analysis of Xtensa LX6 execution, zero-I/O timing protocols, host-to-silicon rank inversions, and tensor arena memory allocation.
2. **Paper 2 vs. Paper 5:**
   * *Paper 2* focuses on the algorithmic Pareto frontier across compression techniques (structured channel pruning vs. knowledge distillation) on the 14-feature and 12-feature datasets.
   * *Paper 5* focuses on the physical execution behavior and timing distributions of the resulting compiled artifacts on physical silicon.
3. **Paper 3 vs. Paper 5:**
   * *Paper 3* focuses on cyber-physical engine diagnosis, cost-sensitive threshold calibration ($\theta^*$), and hierarchical multi-class fault classification.
   * *Paper 5* is domain-agnostic with respect to the diagnostic application, focusing strictly on embedded integer execution mechanics and microarchitectural behavior.
4. **Paper 4 vs. Paper 5:**
   * *Paper 4* establishes a software engineering verification methodology, defect taxonomy, and executable test harness for edge AI pipelines.
   * *Paper 5* is an empirical benchmarking and profiling study on physical silicon.

---

## 4. Synthesis and Independence Verdict

* **Claim Overlap:** **NONE (0%)**
* **Shared Evidence Role:** Physical ESP32 measurements serve as a consistent, reproducible hardware anchor that grounds all five papers in authentic commercial silicon while each paper addresses a completely separate, independent scientific domain.

**PAPER INDEPENDENCE VERDICT: PRESERVED AND FULLY ORTHOGONAL**
