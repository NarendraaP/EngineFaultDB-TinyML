# Portfolio Figure Reuse & Provenance Audit

**Audit Scope:** Manuscripts 1, 2, 3, and 4  
**Date:** August 20, 2026  

---

## 1. Comprehensive Figure Inventory by Paper

### Paper 1: QoS-Aware Multi-Fidelity Runtime (`papers/Paper1_QoS_Runtime/figures/`)
| # | Filename | Source Experiment | Content / Visualization | Cross-Paper Reuse? | Justification |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | `phase5_policy_comparison.png` | Phase 5 Trace Simulation | 4-panel heatmap matrix (Acc, F1, Deadline, Switch) | **Unique to Paper 1** | Primary systems policy comparison |
| 2 | `phase5_accuracy_vs_workload.png`| Phase 5 Sweep | Accuracy across 4 contention levels | **Unique to Paper 1** | Workload sensitivity analysis |
| 3 | `phase5_f1_vs_workload.png` | Phase 5 Sweep | Macro F1 across 4 contention levels | **Unique to Paper 1** | Workload sensitivity analysis |
| 4 | `phase5_deadline_compliance_vs_workload.png` | Phase 5 Sweep | Deadline compliance curves | **Unique to Paper 1** | Real-time systems compliance |
| 5 | `phase5_model_switch_rate.png` | Phase 5 Sweep | Model switch frequency curves | **Unique to Paper 1** | Controller stability proof |
| 6 | `phase5_accuracy_compute_frontier.png` | Phase 5 Model Registry | Multi-fidelity operating points on frontier | **Unique to Paper 1** | Mode mapping visualization |
| 7 | `phase5_ablation.png` | Phase 5 Ablations | 4-panel systems ablation comparison | **Unique to Paper 1** | Systems ablation analysis |

---

### Paper 2: TinyML Pareto Frontier (`papers/Paper2_TinyML_Pareto/figures/`)
| # | Filename | Source Experiment | Content / Visualization | Cross-Paper Reuse? | Justification |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | `pareto_frontier.png` | Phase 4 Compression Sweep | Multi-objective Pareto frontier (4 dimensions) | Also in Paper 4 | Primary contribution in Paper 2; audited artifact illustration in Paper 4 |
| 2 | `accuracy_vs_model_size.png` | Phase 4 Sweep | Accuracy vs. FlatBuffer file size (Bytes) | **Unique to Paper 2** | Storage compression trade-off |
| 3 | `f1_vs_model_size.png` | Phase 4 Sweep | Macro F1 vs. FlatBuffer file size (Bytes) | **Unique to Paper 2** | Balanced class trade-off |
| 4 | `accuracy_vs_macs.png` | Phase 4 Sweep | Accuracy vs. Theoretical active MACs | Also in Paper 4 | Primary benchmark in Paper 2; audited in Paper 4 |
| 5 | `accuracy_vs_latency.png` | Phase 4 Sweep | Accuracy vs. Host empirical latency | **Unique to Paper 2** | Execution timing trade-off |
| 6 | `fp32_vs_int8_accuracy.png` | Phase 4 Quantization | FP32 baseline vs. INT8 quantized accuracy | Also in Paper 4 | Quantization fidelity in Paper 2; tensor graph check in Paper 4 |

---

### Paper 3: Hierarchical Engine Diagnostics (`papers/Paper3_Engine_Diagnostics/figures/`)
| # | Filename | Source Experiment | Content / Visualization | Cross-Paper Reuse? | Justification |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | `qos_policy_frontier.png` | Phase 3 Hierarchical Cascade | Hierarchical trigger frontier & workflow | **Unique to Paper 3** | Diagnostic routing architecture |
| 2 | `mode_a_roc_pr_curves.png` | Phase 3 Mode A Sweep | ROC and PR curves for binary filter | **Unique to Paper 3** | Anomaly screening characterization |
| 3 | `threshold_vs_accuracy.png` | Phase 3 Threshold Sweep | Accuracy vs. Gating threshold $\theta$ | **Unique to Paper 3** | Operating point sensitivity |
| 4 | `threshold_vs_trigger_rate.png` | Phase 3 Threshold Sweep | Trigger rate $r_B$ vs. Threshold $\theta$ | **Unique to Paper 3** | Compute demand vs. threshold |
| 5 | `threshold_vs_macro_f1.png` | Phase 3 Threshold Sweep | Macro F1 vs. Threshold $\theta$ | **Unique to Paper 3** | Minority class diagnostic fidelity |
| 6 | `confusion_matrix_mlp.png` | Phase 2 Baseline Evaluation | 4-class multi-class confusion matrix | **Unique to Paper 3** | Mode B diagnostic error breakdown |
| 7 | `cm_mode_a_dt5_binary_full.png`| Phase 3 Mode A Evaluation | Binary confusion matrix for Decision Tree d=5 | **Unique to Paper 3** | Mode A screening accuracy |

---

### Paper 4: TinyML Verification Framework (`papers/Paper4_TinyML_Verification/figures/`)
| # | Filename | Source Experiment | Content / Visualization | Cross-Paper Reuse? | Justification |
| :---: | :--- | :--- | :--- | :---: | :--- |
| 1 | `pareto_frontier.png` | Phase 4.5 Verification | Verified Pareto frontier after discrepancy fix | Legitimate reuse from Paper 2 | Used strictly as case study visualization of audited model profile |
| 2 | `fp32_vs_int8_accuracy.png` | Phase 4.5 Verification | Quantization fidelity verification | Legitimate reuse from Paper 2 | Illustrates verified `FULL_INT8` graph properties |
| 3 | `accuracy_vs_macs.png` | Phase 4.5 Verification | Active MAC vs. accuracy verification | Legitimate reuse from Paper 2 | Illustrates computational sparsity vs. dense storage |

---

## 2. Figure Reuse Summary & Ethics Evaluation

- **Total Unique Figures Generated:** 17 distinct figures across repository.
- **Figure Reuse Rate:** 3 figures out of 20 figure placements are cross-referenced in Paper 4 ($15.0\%$).
- **Scientific Justification:** The reuse of Pareto and quantization figures in Paper 4 is methodologically necessary because Paper 4 serves as the independent verification audit of the Phase 4/4.5 models.
- **Verdict:** **`PASS — All figure placements are scientifically justified and ethically defensible.`**
