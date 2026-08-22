# Paper 4 Overlap Audit & Scoping Analysis

**Paper Title:** *An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims*  
**Paper Directory:** [`papers/Paper4_TinyML_Verification/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/)  
**Comparative Baselines:** Paper 1 (QoS Systems), Paper 2 ([`papers/Paper2_TinyML_Pareto/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/paper.tex)), Paper 3 ([`papers/Paper3_Engine_Diagnostics/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/paper.tex))  
**Date:** August 20, 2026  

---

## 1. Portfolio Role Comparison

| Paper Dimension | Paper 1 (QoS Systems) | Paper 2 (TinyML Pareto) | Paper 3 (Engine Diagnostics) | **Paper 4 (Verification Methodology)** |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Domain** | Embedded Systems / Real-Time Scheduling | Edge ML / Model Compression | Automotive Cyber-Physical Fault Diagnostics | **Empirical Software Engineering / ML Reproducibility** |
| **Central Question** | How to dynamically schedule models under CPU contention? | How do compression paradigms alter Pareto trade-offs? | How to structure hierarchical binary-to-multi-class diagnostic cascades? | **How to systematically audit and verify TinyML claims from raw artifacts to deployment assertions?** |
| **Core Contribution** | Dynamic QoS runtime, 4 policies, trace simulation. | 12-model compression benchmark, FlatBuffer sparsity proof. | Feature redundancy removal, asymmetric screening cascade. | **7-dimensional TinyML verification framework, 20-discrepancy resolution case study.** |
| **Target Venues** | *IEEE Trans. Computers / ACM TECS* | *IEEE Embedded Systems Letters / ACM TODAES* | *IEEE Trans. Industrial Informatics / MSSP* | ***IEEE Trans. Software Engineering / ACM TOSEM / MLSys Artifacts*** |

---

## 2. Explicit Scientific Boundaries of Paper 4

1. **NO Scheduler Algorithms:** Paper 4 does NOT formulate dynamic QoS scheduling algorithms (Paper 1).
2. **NO Compression Optimization Claims:** Paper 4 does NOT propose new compression techniques or claim Pareto frontier discovery as its primary contribution (Paper 2). Instead, it uses the 12 candidate models strictly as an empirical case study on discrepancy resolution and FlatBuffer tensor verification.
3. **NO Engine Fault Diagnostic Novelty:** Paper 4 does NOT claim domain contributions in combustion engines (Paper 3).
4. **Methodological & Audit Focus:** Paper 4 is exclusively dedicated to scientific verification protocols, data isolation proofs, tensor graph inspection formalisms, terminology corrections, and reproducibility auditing for edge ML pipelines.

---

## 3. Verdict on Scientific Independence

- **Overlap with Paper 1:** **LOW** (Verification protocol vs dynamic scheduling systems).
- **Overlap with Paper 2:** **LOW** (Benchmarking audit case study vs model compression analysis).
- **Overlap with Paper 3:** **LOW** (Methodology vs applied automotive diagnostics).
- **Overall Independence Verdict:** **PASS — STRONG STANDALONE METHODOLOGY PUBLICATION**.
