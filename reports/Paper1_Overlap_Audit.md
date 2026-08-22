# Paper 1 Overlap Audit & Scoping Boundaries

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention*  
**Paper Directory:** [`papers/Paper1_QoS_Runtime/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/)  
**Comparative Baselines:** Paper 2 (Compression/Pareto), Paper 3 (Engine Diagnostics), Paper 4 (Verification Methodology)  
**Date:** August 20, 2026  

---

## 1. Distinct Roles Across the 4-Paper Portfolio

| Paper Dimension | **Paper 1 (Flagship Systems)** | Paper 2 (Edge ML / TinyML) | Paper 3 (Industrial Diagnostics) | Paper 4 (Software Engineering) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Theme** | **Dynamic Runtime Scheduling under Contention** | Static Model Compression \& Pareto Frontier | Asymmetric Hierarchical Diagnostic Cascade | Empirical Verification \& Auditing Protocols |
| **Core Scientific Question** | **Can dynamic model selection maintain QoS and prevent deadline violations under unpredictable CPU contention?** | How do quantization, pruning, and distillation trade accuracy against memory/MACs? | How can binary screening reduce diagnostic inference load on nominal streams? | How can TinyML claims be independently audited to expose measurement discrepancies? |
| **Core Technical Artifact** | **`QoSRuntime`, `QoSScheduler`, 4 dynamic policies, 80 configurations, 4 ablations.** | 12 candidate models, FlatBuffer sparsity proof, 6 Pareto models. | Mode A decision trees, ROC/PR gating, validation threshold sweeps. | 15-point verification checklist, 20-discrepancy resolution case study. |
| **Relationship to Paper 1** | **Primary Subject** | Paper 1 uses Pareto models as input components. | Paper 1 uses multi-fidelity concepts as architectural background. | Paper 1 adheres to the verification protocols established in Paper 4. |
| **Target Venue** | ***IEEE Trans. Computers / ACM TECS / IEEE RTSS-WIP*** | *IEEE Embedded Systems Letters / ACM TODAES* | *IEEE Trans. Industrial Informatics / MSSP* | *IEEE Trans. Software Engineering / ACM TOSEM* |

---

## 2. Strict Boundary Rules for Paper 1

1. **NO Static Compression Re-Presentation:** Paper 1 does NOT re-derive the 12-model compression benchmark, magnitude pruning sparsity equations, or static Pareto dominance proofs. It simply references the verified models (`student_a_8_4_fp32`, `pruned_mlp_14f_75pct`, `student_b_16_4_fp32`) as pre-existing runtime assets.
2. **NO Applied Diagnostic Cascade Re-Presentation:** Paper 1 does NOT focus on combustion engine physics or binary anomaly ROC curves; it frames its evaluation around systems metrics (workload contention, deadline compliance, model switching, macro F1 retention).
3. **NO Verification Methodology Claims:** Paper 1 does NOT present verification taxonomies as its contribution.
4. **Flagship Systems Focus:** Paper 1 is squarely centered on dynamic runtime scheduling, adaptive multi-fidelity execution, trace-driven workload simulation, policy sensitivity, and controlled systems ablations.

---

## 3. Verdict on Scientific Independence

- **Overlap with Paper 2:** **LOW** (Dynamic runtime systems vs. static model compression).
- **Overlap with Paper 3:** **LOW** (Dynamic contention scheduling vs. domain-specific diagnostic cascade).
- **Overlap with Paper 4:** **LOW** (Runtime architecture vs. software engineering verification).
- **Overall Independence Verdict:** **PASS — STRONG FLAGSHIP SYSTEMS PUBLICATION**.
