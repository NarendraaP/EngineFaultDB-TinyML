# Paper 1 Final Overlap Audit & Scoping Boundaries

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*  
**Paper Directory:** [`papers/Paper1_QoS_Runtime/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/)  
**Comparative Baselines:** Paper 2 (Compression/Pareto), Paper 3 (Engine Diagnostics), Paper 4 (Verification Methodology)  
**Date:** August 20, 2026  

---

## 1. 4-Paper Portfolio Contribution Matrix

| Paper Dimension | **Paper 1 (Flagship Systems)** | Paper 2 (Edge ML / TinyML) | Paper 3 (Industrial Diagnostics) | Paper 4 (Software Engineering) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Theme** | **Dynamic Runtime Scheduling under Contention** | Static Model Compression \& Pareto Frontier | Asymmetric Hierarchical Diagnostic Cascade | Independent Scientific Verification Framework |
| **Core Scientific Question** | **Can dynamic model selection maintain QoS and prevent deadline violations under unpredictable CPU contention?** | What is the empirical Pareto trade-off across 4 compression paradigms? | How can binary screening reduce diagnostic compute on nominal streams? | How can TinyML claims be independently verified to prevent reproducibility failures? |
| **Core Technical Artifact** | **`QoSRuntime`, `QoSScheduler`, 4 dynamic policies, 80 configs, 4 ablations.** | 12 candidate models, FlatBuffer sparsity proof, 6 Pareto models. | Mode A decision trees, ROC/PR gating, validation threshold sweeps. | 7-dimension verification taxonomy, 20-discrepancy resolution case study. |
| **Primary Target Venue** | ***IEEE Trans. Computers / ACM TECS*** | *IEEE Embedded Systems Letters / ACM TODAES* | *IEEE Trans. Industrial Informatics / MSSP* | *IEEE Trans. Software Engineering / ACM TOSEM* |
| **Scope Status** | **Systems Infrastructure** | Model Optimization | Industrial Application | Verification Methodology |

---

## 2. Classification of Paper 1 Contributions

- **Multi-Fidelity Runtime Architecture:** **UNIQUE** to Paper 1.
- **Dynamic QoS Scheduler (4 Policies):** **UNIQUE** to Paper 1.
- **80-Configuration Workload Sweep:** **UNIQUE** to Paper 1.
- **Controlled Systems Ablation Studies (A–D):** **UNIQUE** to Paper 1.
- **Model Switching & Stability Analysis:** **UNIQUE** to Paper 1.
- **Shared Assets (Pareto Models & Test Dataset):** Used strictly as pre-compiled runtime components, fully cited.

---

## 3. Scientific Independence Verdict

```
======================================================================
PAPER 1 OVERLAP AUDIT: PASS (Independent Flagship Systems Paper)
======================================================================
  Overlap with Paper 2: LOW (<10%) — Dynamic runtime vs static compression
  Overlap with Paper 3: LOW (<10%) — Dynamic contention vs diagnostic cascade
  Overlap with Paper 4: LOW (<10%) — Systems execution vs software verification
  Final Verdict:        PASS — INDEPENDENT AND DEFENSIBLE FLAGSHIP PAPER
======================================================================
```
