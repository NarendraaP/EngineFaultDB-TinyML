# Phase 18E — Paper 2 Hardware Evidence Integration Plan

> **Manuscript:** Paper 2 — Multi-Objective Pareto Optimization of TinyML Models for Edge Diagnostics  
> **Target Venue:** *ACM Transactions on Design Automation of Electronic Systems (TODAES)*  
> **Integration Verdict:** `HARDWARE_SUPPORTING_EVIDENCE` (Secondary Deployment Validation Axis)  

---

## 1. Executive Summary

Paper 2 establishes an analytical and empirical Pareto frontier across compression techniques (knowledge distillation, unstructured pruning, INT8 quantization) using three primary optimization objectives:
1. **Diagnostic Accuracy / Macro F1**
2. **Serialized Binary Size (Bytes)**
3. **Theoretical Active MAC Count**

The physical ESP32 benchmark provides **Tier 1 empirical hardware grounding**, proving that analytical parameter reductions translate directly into physical execution speedups on 32-bit Xtensa registers.

---

## 2. Pareto Frontier Dimensionality & Preservation

### Audit Finding on Pareto Dimensions:
- **Decision:** Physical on-device latency must **REMAIN A SECONDARY DEPLOYMENT VALIDATION AXIS**, rather than being merged into a 4-objective primary mathematical Pareto frontier.
- **Scientific Justification:** 
  1. Serialized model size and active MAC counts are deterministic, platform-invariant mathematical properties of the model graph.
  2. Microcontroller execution latency depends on toolchain optimization (`-O3`), memory alignment, and framework kernels (e.g., reference vs DSP-accelerated).
  3. Keeping the primary frontier 3-dimensional ensures hardware independence while using physical ESP32 latency as a concrete silicon validation case study.

### Dominance and Trade-off Verification on Physical Silicon:
Physical measurements confirm that the Pareto trade-off curve is strictly preserved on physical silicon:

| Model ID | Params | Active MACs | Size (Bytes) | Test Accuracy | Macro F1 | Physical ESP32 Latency | Pareto Status on Silicon |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| `student_a_8_4_int8` | 176 | 160 | 3,208 B | 71.14% | 0.6848 | **64.55 $\mu\text{s}$** (Fastest) | **PARETO_OPTIMAL** (Minimal Latency & Size) |
| `student_b_16_4_int8` | 328 | 304 | 3,576 B | 74.56% | 0.6896 | **72.96 $\mu\text{s}$** | **PARETO_OPTIMAL** (High Accuracy INT8) |
| `mlp_12f_int8` | 380 | 352 | 3,712 B | 74.79% | 0.7155 | **76.77 $\mu\text{s}$** | **PARETO_OPTIMAL** (Reduced Features) |
| `mlp_14f_int8` | 412 | 384 | 3,728 B | 75.04% | 0.7388 | **89.90 $\mu\text{s}$** | **PARETO_OPTIMAL** (Maximum Accuracy INT8) |

> **Audit Conclusion:** No model is dominated when physical latency is evaluated. The speedup from `mlp_14f` ($89.90\,\mu\text{s}$) to `student_a` ($64.55\,\mu\text{s}$) is **$28.2\%$**, demonstrating a substantial runtime efficiency gain on physical silicon.

---

## 3. Host vs. Silicon Ranking Comparison

| Model | Parameters | Host Latency (Mean) | Host Rank | ESP32 Latency (Mean) | ESP32 Rank | Latency Slowdown Ratio |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| `student_a_8_4_int8` | 176 | 1.02 $\mu\text{s}$ | Rank 3 | **64.55 $\mu\text{s}$** | **Rank 1 (Fastest)** | $63.28\times$ |
| `student_b_16_4_int8` | 328 | 0.98 $\mu\text{s}$ | Rank 1 | **72.96 $\mu\text{s}$** | **Rank 2** | $74.45\times$ |
| `mlp_12f_int8` | 380 | 1.00 $\mu\text{s}$ | Rank 2 | **76.77 $\mu\text{s}$** | **Rank 3** | $76.77\times$ |
| `mlp_14f_int8` | 412 | 1.43 $\mu\text{s}$ | Rank 4 | **89.90 $\mu\text{s}$** | **Rank 4 (Slowest)** | $62.87\times$ |

### Scientific Significance:
On host x86_64, sub-microsecond timing noise ($\approx 0.98\text{--}1.02\,\mu\text{s}$) obscured the minor parameter difference between `student_a` (176 params) and `student_b` (328 params). On physical microcontroller silicon, the timing scales **strictly monotonically with arithmetic operations**, confirming the necessity of hardware-in-the-loop TinyML validation.

---

## 4. Recommended Integration Action in Paper 2

- **Section V-D (Hardware Deployment Validation):** Add a concise subsection and summary table reporting the physical ESP32 mean latencies and host-to-silicon ratios as secondary deployment validation.
- **Section VI (Discussion):** Highlight the $28.2\%$ physical speedup achieved by knowledge distillation on physical Xtensa LX6 silicon.
