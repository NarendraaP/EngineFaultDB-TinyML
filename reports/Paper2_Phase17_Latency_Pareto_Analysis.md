# Phase 17A — Latency and Pareto Frontier Analysis: Paper 2

**Manuscript:** Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML  
**Target Venue:** ACM Transactions on Design Automation of Electronic Systems (TODAES) / IEEE TCAD  
**Date:** August 28, 2026  

---

## 1. Executive Summary

This report evaluates whether empirical host inference latency (measured on an x86_64 host CPU) should remain a primary objective in the Pareto optimization of TinyML model compression paradigms. Based on mathematical dominance analysis and embedded systems principles, we formally compare the 4-Objective Frontier A against the 3-Objective Frontier B.

**Key Finding:** Exactly the same six candidate models populate the Pareto frontier under both 4D (Accuracy, Binary Size, Active MACs, Host Latency) and 3D (Accuracy, Binary Size, Active MACs) formulations. Zero models change their Pareto status. Removing x86 host latency from the primary Pareto frontier eliminates a critical reviewer vulnerability while preserving 100% of the paper's Pareto classifications.

---

## 2. Mathematical Definition of Evaluated Frontiers

### Frontier A: 4-Objective Space
$$\mathcal{O}_A(m) = \Big( \max \text{Accuracy}(m), \min \text{Size}_{\text{Bytes}}(m), \min \text{MACs}_{\text{Active}}(m), \min \text{Latency}_{\text{Host}}(m) \Big)$$

A model $m_1$ dominates $m_2$ ($m_1 \succ_A m_2$) if and only if:
1. $\text{Accuracy}(m_1) \ge \text{Accuracy}(m_2)$
2. $\text{Size}(m_1) \le \text{Size}(m_2)$
3. $\text{MACs}(m_1) \le \text{MACs}(m_2)$
4. $\text{Latency}(m_1) \le \text{Latency}(m_2)$
and at least one inequality is strictly satisfied.

### Frontier B: 3-Objective Deployment-Resource Space
$$\mathcal{O}_B(m) = \Big( \max \text{Accuracy}(m), \min \text{Size}_{\text{Bytes}}(m), \min \text{MACs}_{\text{Active}}(m) \Big)$$

A model $m_1$ dominates $m_2$ ($m_1 \succ_B m_2$) if and only if:
1. $\text{Accuracy}(m_1) \ge \text{Accuracy}(m_2)$
2. $\text{Size}(m_1) \le \text{Size}(m_2)$
3. $\text{MACs}(m_1) \le \text{MACs}(m_2)$
and at least one inequality is strictly satisfied.

---

## 3. Comprehensive Model-by-Model Pareto Comparison

Using the independently verified model profile (`results/tinyml_model_profile_verified.csv`), we calculate exact dominance relationships across all 12 candidate models.

| Model Identifier | Precision | Features | Params | Size (B) | Active MACs | Test Accuracy | Macro F1 | Host Latency (μs) | Frontier A Status (4D) | Frontier B Status (3D) | Status Change |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `student_b_16_4_fp32` | FP32 | 14 | 328 | 3,584 | 304 | **0.751429** | 0.738717 | 0.82 | **PARETO_OPT** | **PARETO_OPT** | NONE |
| `pruned_mlp_14f_25pct` | FP32 | 14 | 412 | 3,920 | 288 | 0.750536 | 0.751490 | 1.69 | **PARETO_OPT** | **PARETO_OPT** | NONE |
| `pruned_mlp_14f_50pct` | FP32 | 14 | 412 | 3,920 | 192 | 0.749464 | 0.756572 | 0.86 | **PARETO_OPT** | **PARETO_OPT** | NONE |
| `pruned_mlp_14f_75pct` | FP32 | 14 | 412 | 3,920 | **96** | 0.748214 | 0.756251 | 0.83 | **PARETO_OPT** | **PARETO_OPT** | NONE |
| `student_b_16_4_int8` | FULL_INT8 | 14 | 328 | 3,576 | 304 | 0.745625 | 0.689601 | 0.98 | **PARETO_OPT** | **PARETO_OPT** | NONE |
| `student_a_8_4_fp32` | FP32 | 14 | 176 | **2,976** | 160 | 0.716339 | 0.722001 | 0.86 | **PARETO_OPT** | **PARETO_OPT** | NONE |
| `tflite_mlp_14f_int8` | FULL_INT8 | 14 | 412 | 3,728 | 384 | 0.750357 | 0.738824 | 1.43 | DOMINATED | DOMINATED | NONE |
| `tflite_mlp_14f_fp32` | FP32 | 14 | 412 | 3,892 | 384 | 0.750000 | 0.756608 | 0.99 | DOMINATED | DOMINATED | NONE |
| `pruned_mlp_14f_0pct` | FP32 | 14 | 412 | 3,892 | 384 | 0.750000 | 0.756608 | 0.95 | DOMINATED | DOMINATED | NONE |
| `tflite_mlp_12f_int8` | FULL_INT8 | 12 | 380 | 3,712 | 352 | 0.747857 | 0.715534 | 1.00 | DOMINATED | DOMINATED | NONE |
| `tflite_mlp_12f_fp32` | FP32 | 12 | 380 | 3,780 | 352 | 0.747143 | 0.725414 | 0.87 | DOMINATED | DOMINATED | NONE |
| `student_a_8_4_int8` | FULL_INT8 | 14 | 176 | 3,208 | 160 | 0.711429 | 0.684788 | 1.02 | DOMINATED | DOMINATED | NONE |

---

## 4. Dominance Analysis and Proof of Equivalence

### Why the 6 Pareto-Optimal Models Remain Non-Dominated in 3D:
1. **`student_b_16_4_fp32`**: Achieves the **global maximum test accuracy ($75.1429\%$)** across all 12 models. No model has higher accuracy, so it cannot be dominated on accuracy by any candidate.
2. **`student_a_8_4_fp32`**: Achieves the **global minimum serialized file size ($2,976$\,B)** across all 12 models. No model has a smaller footprint, so it cannot be dominated on storage.
3. **`pruned_mlp_14f_75pct`**: Achieves the **global minimum theoretical active MAC count ($96$ MACs)** across all 12 models. No model has fewer active operations, so it cannot be dominated on computation.
4. **`pruned_mlp_14f_50pct`** ($192$ MACs, $74.9464\%$ Acc, $3,920$\,B): Has fewer MACs ($192$) than `student_b_fp32` ($304$) and higher accuracy ($74.95\%$) than `pruned_75pct` ($74.82\%$) and `student_a_fp32` ($71.63\%$).
5. **`pruned_mlp_14f_25pct`** ($288$ MACs, $75.0536\%$ Acc, $3,920$\,B): Has fewer MACs ($288$) than `student_b_fp32` ($304$) and higher accuracy ($75.05\%$) than `pruned_50pct` ($74.95\%$).
6. **`student_b_16_4_int8`** ($304$ MACs, $74.5625\%$ Acc, $3,576$\,B): Has smaller file size ($3,576$\,B) than `student_b_fp32` ($3,584$\,B) and higher accuracy than `student_a_fp32` ($71.63\%$).

### Why the 6 Dominated Models Remain Dominated in 3D:
- `tflite_mlp_14f_fp32` ($75.00\%$, $3,892$\,B, $384$ MACs) is strictly dominated by `student_b_16_4_fp32` ($75.14\% > 75.00\%$, $3,584\,\text{B} < 3,892\,\text{B}$, $304 < 384$ MACs).
- `pruned_mlp_14f_0pct` ($75.00\%$, $3,892$\,B, $384$ MACs) is identical in 3D metrics to `tflite_mlp_14f_fp32` and is strictly dominated by `student_b_16_4_fp32`.
- `tflite_mlp_14f_int8` ($75.04\%$, $3,728$\,B, $384$ MACs) is dominated by `student_b_16_4_fp32` ($75.14\% > 75.04\%$, $3,584\,\text{B} < 3,728\,\text{B}$, $304 < 384$ MACs).
- `tflite_mlp_12f_fp32` ($74.71\%$, $3,780$\,B, $352$ MACs) is dominated by `student_b_16_4_fp32` ($75.14\% > 74.71\%$, $3,584\,\text{B} < 3,780\,\text{B}$, $304 < 352$ MACs).
- `tflite_mlp_12f_int8` ($74.79\%$, $3,712$\,B, $352$ MACs) is dominated by `student_b_16_4_fp32` ($75.14\% > 74.79\%$, $3,584\,\text{B} < 3,712\,\text{B}$, $304 < 352$ MACs).
- `student_a_8_4_int8` ($71.14\%$, $3,208$\,B, $160$ MACs) is strictly dominated by `student_a_8_4_fp32` ($71.63\% > 71.14\%$, $2,976\,\text{B} < 3,208\,\text{B}$, $160 = 160$ MACs).

---

## 5. Scientific and Reviewer Rationale for Transition to Frontier B

### 1. Inherent Flaw of x86 Latency in TinyML Characterization
Host inference latency measured via `time.perf_counter_ns()` on an x86_64 CPU (0.82–1.69 μs) is governed by superscalar out-of-order execution, deep instruction pipelines, branch predictors, and multi-level L1/L2/L3 caches. Embedded microcontrollers (e.g., ARM Cortex-M0+/M4, Xtensa LX6/LX7) lack these architectural mechanisms. Presenting x86 execution time as a primary axis of a "TinyML Pareto Frontier" is a fundamental systems mismatch that reviewers rightly flagged.

### 2. Elimination of Measurement Noise Artifacts
On x86 hosts, sub-microsecond timing differences (e.g., 0.82 μs vs. 0.86 μs) are subject to OS thread scheduling, interrupt preemption, and thermal throttling jitter. In fact, running `phase4_5_verification.py` repeatedly shows minor fluctuations in measured host latency that can spuriously alter 4D dominance if latency is treated as a hard objective. In contrast, **Frontier B (Accuracy, Size, Active MACs) is 100% deterministic, immutable, and mathematically pure.**

### 3. Preserves Full Scientific Scope as a Secondary Benchmark
Host latency does not need to be hidden or deleted. It should be presented transparently in Section VI as a **secondary host execution benchmark**, clearly distinguished from microcontroller hardware timings.

---

## 6. Recommendation

**Transition Paper 2's primary theoretical framework to the 3-Objective Deployment-Resource Pareto Frontier (Accuracy, Serialized File Size, Theoretical Active MACs).**

### Specific Manuscript Adjustments:
1. **Title & Abstract:** Update "empirical 4D Pareto characterization" to "empirical 3-objective deployment-resource Pareto characterization (Accuracy, Serialized Binary Size, Theoretical Active MACs)".
2. **Section V-D (Metrics):** Define Frontier B as the primary Pareto space; reclassify host latency as a secondary empirical timing profile.
3. **Table I:** Group and highlight the 6 Pareto-optimal models based on the 3D frontier.
4. **Figure 4:** Re-plot the Pareto frontier in 3D (Accuracy vs. Size vs. MACs) or as a 2D projection matrix (Accuracy vs. MACs and Accuracy vs. Size), eliminating the 4D radar/latency plot.
5. **Section VI-D:** Add explicit reasoning: *"Because host execution times on x86_64 architectures reflect cache and superscalar dynamics not present on bare-metal microcontrollers, we formulate our primary deployment Pareto frontier strictly over deterministic deployment resources (accuracy, serialized binary storage, and active arithmetic operations), while reporting host latency as a secondary reference benchmark."*
