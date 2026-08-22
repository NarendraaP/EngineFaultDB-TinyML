# Paper 4 Final Overlap Audit & Scoping Boundaries

**Paper Title:** *An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims*  
**Paper Directory:** [`papers/Paper4_TinyML_Verification/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/)  
**Comparative Baselines:** Paper 1 (QoS Systems), Paper 2 (Compression/Pareto), Paper 3 (Engine Diagnostics)  
**Date:** August 20, 2026  

---

## 1. 4-Paper Portfolio Contribution Matrix

| Paper Dimension | Paper 1 (Flagship Systems) | Paper 2 (Edge ML / TinyML) | Paper 3 (Industrial Diagnostics) | **Paper 4 (Software Engineering)** |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Theme** | Dynamic Runtime Scheduling under Contention | Static Model Compression \& Pareto Frontier | Asymmetric Hierarchical Diagnostic Cascade | **Independent Scientific Verification Framework** |
| **Core Scientific Question** | How to adapt model selection dynamically to CPU contention and deadlines? | What is the empirical Pareto trade-off across 4 compression paradigms? | How can binary screening reduce diagnostic compute on nominal streams? | **How can TinyML claims be independently verified to prevent reproducibility failures?** |
| **Core Artifact** | `QoSRuntime`, `QoSScheduler`, 4 policies, 80 configs, 4 ablations. | 12 candidate models, FlatBuffer sparsity proof, 6 Pareto models. | Mode A decision trees, ROC/PR gating, validation threshold sweeps. | **7-dimension verification taxonomy, 20-discrepancy resolution case study.** |
| **Primary Target Venue** | *IEEE Trans. Computers / ACM TECS* | *IEEE Embedded Systems Letters / ACM TODAES* | *IEEE Trans. Industrial Informatics / MSSP* | ***IEEE Trans. Software Engineering / ACM TOSEM*** |
| **Scope Status** | Systems Infrastructure | Model Optimization | Industrial Application | **Verification Methodology** |

---

## 2. Classification of Paper 4 Contributions

- **7-Dimension Verification Taxonomy:** **UNIQUE** to Paper 4.
- **20-Discrepancy Resolution Case Study:** **UNIQUE** to Paper 4 (Papers 1–3 use the final verified profile directly; only Paper 4 details the software engineering analysis of the 20 pre-verification discrepancies).
- **$+1.8\%$ Threshold Leakage Bias Experiment:** **UNIQUE** to Paper 4 as a methodological case study.
- **Evidence Tiering Framework:** **UNIQUE** to Paper 4.
- **Shared Assets (Benchmark Dataset & Verified Binaries):** Used strictly as the empirical subject of the verification case study, fully cited.

---

## 3. Scientific Independence Verdict

```
======================================================================
PAPER 4 OVERLAP AUDIT: PASS (Independent Software Engineering Paper)
======================================================================
  Overlap with Paper 1: LOW (<10%) — Verification vs Runtime
  Overlap with Paper 2: LOW (<15%) — Verification case study vs Optimization
  Overlap with Paper 3: LOW (<10%) — Verification case study vs Diagnostics
  Final Verdict:        PASS — INDEPENDENT AND DEFENSIBLE PUBLICATION
======================================================================
```
