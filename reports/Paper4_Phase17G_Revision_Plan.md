# Phase 17G — Comprehensive Revision Plan: Paper 4

**Manuscript:** An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims  
**Date:** August 28, 2026  
**Author:** Narendra Satish (`narendresh.p@gmail.com`)  

---

## 1. Executive Decision

```
PAPER 4 REVISION LEVEL: MODERATE_REVISION
VENUE STRATEGY: RETARGET TO EMBEDDED / PRACTITIONER SE (ACM LCTES / IEEE Software / CASES / NeurIPS D&B)
```

### Scientific Justification:
The scientific and empirical evidence in Paper 4 is sound, rigorous, and fully verified (`scripts/phase4_5_verification.py`, `results/tinyml_model_profile_verified.csv`). The manuscript does not require new experiments or retraining. However, to achieve maximum defensibility and avoid rejection risks associated with single-case-study scope at general software engineering theory journals (IEEE TSE / ACM TOSEM), Paper 4 should be repositioned as an **"Artifact-Driven Empirical Verification Protocol and Defect Taxonomy for Compiled TinyML Deployment Artifacts"** and targeted at high-impact embedded systems / AI engineering venues.

---

## 2. Core Revision Action Items for Phase 17H

### Item 1: Reframing Core Terminology (Framework $\rightarrow$ Protocol)
- **Action:** Replace overbroad claims of a "universal verification framework" with **"empirical verification protocol and defect taxonomy for compiled TinyML deployment artifacts"**.
- **Rationale:** Aligns scientific claims precisely with the demonstrated empirical case study (12 models on physical telemetry).

### Item 2: Formalizing the 7 Programmatic Predicates ($\mathcal{P}_1 \dots \mathcal{P}_7$)
- **Action:** Formulate explicit mathematical and programmatic predicates in Section IV for all 7 dimensions:
  - $\mathcal{P}_1$ (Data Split Disjointness & Scaler Provenance)
  - $\mathcal{P}_2$ (Direct Disk Binary Execution)
  - $\mathcal{P}_3$ (Quantization Dtype Purity, 0 float32 tensors)
  - $\mathcal{P}_4$ (Sparsity vs. Storage Decoupling)
  - $\mathcal{P}_5$ (Active vs. Dense MAC Accounting)
  - $\mathcal{P}_6$ (Warmup & Monotonic Host Timing Protocol)
  - $\mathcal{P}_7$ (Runtime Non-Leakage & Scope Demarcation)

### Item 3: Structuring the 20 Discrepancies into 4 Defect Modes
- **Action:** Group Table II (Discrepancy Resolution) into four distinct software engineering failure modes:
  1. **Mode 1: Serialization Drift** (Training-time logging before final fine-tuning/export, $\Delta \text{Acc} \le 3.26\%$).
  2. **Mode 2: In-Memory Fake-Quantization vs. True Integer Arithmetic** (Quantization calibration state shifts, $\Delta \text{F1} \le 7.82\%$).
  3. **Mode 3: Sparsity-Storage Decoupling** (Weight zeroing without FlatBuffer byte compression).
  4. **Mode 4: Arithmetic & Quantization Rounding** (Minor integer discretization rounding, $\Delta \le 0.19\%$).

### Item 4: Contextualizing the $+1.80\%$ Leakage Bias
- **Action:** Explicitly frame the $+1.80\%$ test-accuracy increase as a *demonstrative case-study quantification* of the optimistic bias introduced when runtime routing thresholds are tuned directly on test partitions rather than isolated validation sets.

### Item 5: Expanding Limitations to 7 Explicit Dimensions (Section VIII)
- **Action:** Explicitly detail all 7 limitation boundaries:
  1. Empirical case study evaluated on fully connected tabular topologies (MLPs).
  2. 2D CNNs, vision transformers, and recurrent audio architectures require future empirical toolchain extensions.
  3. Inspection scripts specifically parse TensorFlow Lite FlatBuffer schema.
  4. Alternative embedded runtimes (ONNX Runtime Mobile, microTVM, STM32Cube.AI) are unverified.
  5. Latency metrics represent host x86_64 empirical timing, not bare-metal microcontroller WCET.
  6. Dataset scope reflects physical dynamometer sensor records from a single engine platform.
  7. Threshold bias ($+1.80\%$) is an empirical demonstration specific to this pipeline.

---

## 3. Ranked Publication Target Recommendations

| Rank | Recommended Venue | Track / Type | Justification |
|:---:|---|---|---|
| **1** | **ACM LCTES / IEEE/ACM CASES** | Regular Research Paper | Perfect fit for embedded software tools, compiler artifacts, and runtime verification. |
| **2** | **IEEE Software** | AI Engineering / Quality Theme | High-impact dissemination for practitioners deploying and auditing TinyML pipelines. |
| **3** | **NeurIPS Datasets & Benchmarks** | Benchmark Auditing Track | Outstanding alignment with artifact inspection, checklists, and reproducibility audits. |
| **4** | **IEEE Transactions on Computers / ACM TECS** | Regular Paper | Strong fit as an empirical systems/software verification methodology. |

---

## 4. Final Classification Summary

```
REQUIRED EXPERIMENTS: NONE (Existing verified evidence fully supports the paper's claims)
STRONGLY RECOMMENDED: Group 20 discrepancies into 4 formal defect categories; formalize programmatic predicates P1-P7.
FINAL VENUE: ACM LCTES / IEEE Software / IEEE/ACM CASES (Primary)
```
