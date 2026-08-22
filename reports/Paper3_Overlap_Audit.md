# Paper 3 Overlap Audit & Scientific Boundary Analysis

**Paper Title:** *Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis*  
**Paper Directory:** [`papers/Paper3_Engine_Diagnostics/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/)  
**Comparative Baselines:** Paper 1 ([`reports/Research_Publication_Strategy.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Research_Publication_Strategy.md)), Paper 2 ([`papers/Paper2_TinyML_Pareto/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/paper.tex)), Paper 4  
**Date:** August 20, 2026  

---

## 1. Core Thesis Comparison Across the Portfolio

| Paper Dimension | Paper 1 (QoS Systems) | Paper 2 (TinyML Pareto) | **Paper 3 (Engine Diagnostics)** | Paper 4 (Methodology) |
| :--- | :--- | :--- | :--- | :--- |
| **Central Research Question** | How to schedule multi-model execution under dynamic CPU contention and strict deadlines? | How do model compression paradigms alter memory, compute, and latency trade-offs? | **Can hierarchical binary anomaly screening reduce multi-class diagnostic evaluations without sacrificing fault recall?** | What empirical traps distort edge ML benchmarks and how can verification protocols fix them? |
| **Core Technical Contribution** | Dynamic QoS runtime, 4 scheduling policies, deadline controller. | Multi-paradigm compression benchmark, FlatBuffer sparsity proof, 6 Pareto models. | **Asymmetric binary-screening to multi-class cascade, feature redundancy reduction, threshold routing.** | 15-point TinyML verification protocol, 20 discrepancy resolution case studies. |
| **Primary Independent Variable** | Deadline ($5$--$100$\,ms) \& Workload Contention (`LOW`--`BURST`). | Compression Paradigm (INT8, Pruning, Distillation, 12f vs 14f). | **Gating Confidence Threshold ($\theta \in [0.00, 1.00]$) \& Screening Model Topology (DT $d=3, 5$, LR).** | Verification Protocol Rigor \& Split-Isolated Threshold Calibration. |
| **Primary Dependent Variables** | Deadline Compliance Rate, Model Switch Frequency. | Active MACs, FlatBuffer File Size (Bytes), Zero-Weight \%. | **Mode B Trigger Rate, Anomaly False-Negative Rate, Expected MACs/sample.** | Numerical Discrepancy Count, Test Accuracy Optimization Bias. |
| **Target Venues** | *IEEE Trans. Computers / ACM TECS / IEEE RTSS-WIP* | *IEEE Embedded Systems Letters / ACM TODAES* | ***IEEE Trans. Industrial Informatics / Mechanical Systems and Signal Processing (MSSP)*** | *IEEE Trans. Software Engineering / ACM TOSEM* |

---

## 2. Explicit Scientific Boundaries of Paper 3

To prevent content overlap and eliminate any risk of duplication:

1. **NO Dynamic QoS Scheduler:** Paper 3 does NOT include the Phase 5 dynamic deadline-driven QoS scheduler (`QoSScheduler`, 4 policies, workload contention multipliers). All scheduling logic is strictly reserved for Paper 1.
2. **NO Compression / Sparsity Deep-Dive:** Paper 3 does NOT perform the 12-model compression benchmark, FlatBuffer tensor auditing, or multi-objective Pareto frontier extraction. Those contributions belong exclusively to Paper 2.
3. **NO Physical MCU Latency Claims:** Paper 3 does NOT report MCU execution or physical energy measurements, preserving boundaries for future Paper 5.
4. **Distinct Diagnostic Focus:** Paper 3 is squarely focused on applied cyber-physical fault diagnosis: sensor collinearity reduction, binary anomaly filtering,ROC/PR trade-offs, and expected computational workload savings on automotive combustion telemetry.

---

## 3. Verdict on Scientific Independence

- **Overlap with Paper 1:** **LOW** (Domain diagnostic cascade vs dynamic systems runtime scheduler).
- **Overlap with Paper 2:** **LOW** (Hierarchical inference vs static compression/Pareto analysis).
- **Overlap with Paper 4:** **LOW** (Diagnostic application vs verification methodology).
- **Overall Independence Verdict:** **PASS — STRONG STANDALONE DOMAIN PUBLICATION**.
