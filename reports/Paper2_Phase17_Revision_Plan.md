# Phase 17A — Reviewer-Style Targeted Revision Plan: Paper 2

**Manuscript:** Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML  
**Target Venue:** ACM Transactions on Design Automation of Electronic Systems (TODAES)  
**Secondary Venue:** IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD)  
**Date:** August 28, 2026  

---

## 1. Step 2 Analysis: Classification of Reviewer Concerns

We evaluate the seven major substantive concerns raised during the Phase 16 Adversarial Peer Review of Paper 2:

| # | Reviewer Concern | Technical Analysis & Evidence Availability | Classification |
|---|---|---|---|
| **1** | **x86 host latency in the primary 4D Pareto frontier** | x86_64 host timing (`time.perf_counter_ns()`) does not reflect microcontroller execution characteristics. Dominance analysis proves that removing host latency yields the exact same 6 Pareto-optimal models with zero status changes. Host latency can be presented as a secondary empirical timing profile. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |
| **2** | **Limited model family (only sub-4 KB MLPs)** | The paper's contribution is explicitly scoped to ultra-low-resource multi-sensor diagnostics (<4 KB, <400 MACs). Scoping the claims tightly to this tabular domain rather than claiming general deep learning conclusions resolves this concern. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |
| **3** | **Established nature of pruning, quantization, and KD** | The paper does not claim to invent new compression algorithms. It evaluates interactions and FlatBuffer serialization mechanics of these standard methods under extreme memory constraints. Reframing the contribution as an empirical artifact characterization resolves this. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |
| **4** | **Whether the Pareto study provides genuinely new insight** | The core insight—that unstructured pruning achieves computational sparsity ($96$ active MACs) without storage reduction ($3,920$\,B) in standard FlatBuffers, while structural KD achieves true storage compression ($2,976$\,B)—is a vital, verified structural insight for embedded developers. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |
| **5** | **Whether structured-pruning baselines are necessary** | Existing pruning in the repository is unstructured magnitude pruning (percentile zeroing on 2D weight arrays). Correcting the inaccurate heading "Structured Magnitude Pruning" to "Unstructured Magnitude-Based Weight Pruning" and framing distillation (Student A/B) as structural dimension reduction resolves the contradiction without fabricating data. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |
| **6** | **Whether the paper is better framed as an empirical engineering benchmark / characterization** | Reclassifying the paper from a "novel methodology" to a "rigorous empirical characterization and artifact benchmark" aligns perfectly with ACM TODAES standards for empirical design automation studies. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |
| **7** | **Whether literature comparison is sufficiently current (2020–2026)** | The related work section should be expanded to incorporate MLPerf Tiny (2021), MCUNet (2020/2021), MuNAS (2021), Blalock et al. (2020), and recent embedded edge compression literature. | **CAN_FIX_WITH_EXISTING_EVIDENCE** |

---

## 2. Reviewer-Style Section-by-Section Revision Plan

| Section in `paper.tex` | Reviewer Concern & Severity | Existing Evidence Available | Recommended Specific Revision | Minimum Scientifically Sufficient Action |
|---|---|---|---|---|
| **Title & Abstract** | *Host latency in 4D Pareto; "Structured pruning" misnomer.* (Severity: HIGH) | Verified 3D Pareto proof; actual pruning code. | Retitle to 3-objective deployment Pareto characterization (Accuracy, Serialized Binary Size, Active MACs). Replace "structured magnitude pruning" with "unstructured magnitude-based pruning". | Textual reframing; zero new data needed. |
| **Section I (Introduction)** | *Overselling scope; claims about general TinyML.* (Severity: MEDIUM) | 12 verified models; 55,998 samples. | Explicitly scope study to ultra-low-memory sensor telemetry (<4 KB, <400 MACs). Emphasize artifact-level FlatBuffer inspection. | Clarify scope boundaries in text. |
| **Section III (Related Work)** | *Thin related work; missing modern benchmark context.* (Severity: MEDIUM) | 2020–2026 TinyML literature survey. | Expand into 4 subsections: (1) Quantization & Pure-Integer Graphs, (2) Weight Sparsity vs. FlatBuffer Serialization, (3) Structural Distillation, (4) Multi-Objective Edge Benchmarks (MLPerf Tiny, MuNAS, MCUNet). | Add citations and comparative discussion. |
| **Section IV (Research Questions)** | *RQ2/RQ4 mention 4D Pareto and structured pruning.* (Severity: LOW) | 3D Pareto analysis. | Update RQ2 to evaluate unstructured pruning vs. storage. Update RQ4 to define the 3-objective deployment resource frontier. | Refine RQ wording. |
| **Section V-C2 (Pruning Methodology)** | *Heading mislabeled as "Structured Magnitude Pruning".* (Severity: HIGH) | Exact pruning code in `phase4_tinyml_optimization.py`. | Retitle to `\subsubsection{Magnitude-Based Weight Pruning}`. Explain that element-wise zeroing preserves 2D matrix shapes. | Correct terminology and explain mechanics. |
| **Section V-D (Metrics)** | *Host latency presented as primary objective.* (Severity: HIGH) | `perf_counter_ns` protocol; x86 CPU. | Define Frontier B (Accuracy, File Size, Active MACs) as the primary deployment Pareto space. Reclassify host latency as a secondary host execution benchmark. | Update metric definitions. |
| **Section VI-B (Results - Pruning)** | *Reviewers questioned why FlatBuffer size increases (+28B).* (Severity: MEDIUM) | FlatBuffer header & dense tensor schema. | Deepen explanation: FlatBuffers serialize dense arrays of floats; zero weights still occupy 4 bytes each, plus operator metadata. | Add structural explanation. |
| **Section VI-D (Pareto Results)** | *4D Pareto radar plot incorporates noisy x86 latency.* (Severity: HIGH) | 3D Pareto dominance proof. | Present the 6 Pareto-optimal models in the 3D space. Note that host latency is reported as a secondary reference. | Update text and Table I highlighting. |
| **Section VII (Discussion)** | *Need deeper guidance on when to use which paradigm.* (Severity: LOW) | Model profile table. | Expand discussion on memory-compute trade-offs: Distillation for Flash storage, Pruning for ALU compute cycles, INT8 for integer-only hardware. | Expand architectural guidelines. |
| **Section IX (Limitations)** | *Limitations must be explicit and elevated.* (Severity: MEDIUM) | Host timing, single dataset, MLP topology. | Expand Limitation 1 (x86 host vs. MCU timing) and Limitation 3 (MLP vs. CNN/transformer topologies). | Expand limitation descriptions. |

---

## 3. Terminology Audit and Action Matrix

| Term / Phrase | Occurrences in Manuscript | Reviewer Perception | Action | Replacement / Justification |
|---|:---:|---|:---:|---|
| **"4D Pareto frontier"** | 4 | Questionable due to x86 host latency axis | **REWRITE** | Replace with **"3-objective deployment-resource Pareto frontier"** (Accuracy, Binary Size, Active MACs). |
| **"Structured magnitude pruning"** | 2 | Inaccurate (code is element-wise unstructured pruning) | **REWRITE** | Replace with **"unstructured magnitude-based weight pruning"**. |
| **"dark knowledge"** | 1 | Hyperbolic for a 412-parameter MLP | **REWRITE** | Replace with **"soft probability distributions from the teacher network"**. |
| **"authoritative verification protocols"** | 2 | Promotional wording | **REWRITE** | Replace with **"independent verification protocols"** or **"verified experimental protocols"**. |
| **"remarkable fidelity"** | 1 | Promotional wording | **REWRITE** | Replace with **"minimal accuracy variation"** or **"high diagnostic fidelity"**. |
| **"computational sparsity without demonstrated storage compression"** | 1 | Highly praised scientific finding | **RETAIN** | **Keep prominently.** This is the paper's strongest structural insight. |
| **"theoretical active MACs"** | 5 | Accurate and responsible metric | **RETAIN** | **Keep.** Clearly distinguishes theoretical operations from hardware instruction counts. |
| **"empirical host inference latency"** | 3 | Accurate but needs secondary framing | **RETAIN** | **Keep**, with explicit qualification as a secondary host benchmark. |

---

## 4. Table and Figure Revision Plan

### Table I: Model Profile Table
- **Current:** Lists all 12 candidate models with 4D Pareto status.
- **Revision:** Group and sort by the 3-Objective Deployment Pareto Frontier (Accuracy, Serialized Size, Active MACs). Explicitly mark the 6 Pareto-optimal models. Retain host latency columns with footnote: *"Empirical host latency measured on x86_64 host CPU; reported as a secondary baseline, not an MCU execution metric."*

### Figures:
- **Figure 1 (Accuracy vs. Active MACs):** **RETAIN.** Clearly shows the compute-accuracy trade-off and the non-dominated position of `pruned_75pct` and `student_b_fp32`.
- **Figure 2 (Accuracy vs. Serialized Model Size):** **RETAIN.** Clearly shows the storage-accuracy trade-off and the structural compression of `student_a` ($2,976$\,B) and `student_b` ($3,584$\,B).
- **Figure 3 (FP32 vs. FULL_INT8 Accuracy):** **RETAIN.** Clearly demonstrates quantization fidelity across model variants.
- **Figure 4 (Multi-Objective Pareto Visualization):** **REVISE.** Replace the 4D radar/scatter plot with a clear 3D Pareto visualization or a 2D projection matrix (Accuracy vs. Size and Accuracy vs. MACs), removing x86 host latency from the primary Pareto frontier visualization.

---

## 5. Content Sufficiency Checklist

To ensure that the paper maintains top-tier technical depth for ACM TODAES, the revised manuscript must contain:
- [x] **Formal mathematical definitions** of all 4 compression paradigms (PTQ affine equations, magnitude pruning percentile thresholds, KD loss with temperature and cross-entropy, feature reduction collinearity).
- [x] **Complete serialization specifications** of TFLite FlatBuffers (buffer offsets, tensor allocation, dense zero serialization, operator metadata overhead).
- [x] **Detailed metric formulations** for Test Accuracy, Macro F1, Serialized Bytes, Theoretical Active MACs, and Empirical Host Latency.
- [x] **Formal Pareto dominance definitions** for the 3-objective deployment space.
- [x] **Model-by-model architectural trade-off analysis** explaining why each Pareto-optimal model earned its non-dominated status.
- [x] **Detailed explanation of why unstructured pruning does not compress FlatBuffers** in standard TFLite Micro runtimes.
- [x] **Architectural deployment guidelines** mapping MCU resource bottlenecks (Flash vs. SRAM vs. CPU cycles) to the optimal compression paradigm.
- [x] **Explicit threats to validity and limitations** covering host timing, tabular data scope, and steady-state dynamometer constraints.

---

## 6. Decision on New Experiments

### A. REQUIRED EXPERIMENTS: **NONE**
*All substantive reviewer concerns regarding Pareto frontiers, pruning classification, FlatBuffer serialization, and metric definitions can be fully, rigorously, and defensively resolved using the existing, verified experimental evidence.*

### B. STRONGLY RECOMMENDED EXPERIMENTS (Future Work):
1. **Physical Microcontroller Profiling:** Deploy the 6 Pareto-optimal models to an ESP32-WROOM-32 or STM32F401RE MCU to measure bare-metal cycle counts via hardware DWT timers and current consumption via source-measure units.
2. **Neuron/Channel-Level Structured Pruning:** Implement a formal channel-pruning baseline that physically removes hidden neurons from the Keras/TFLite graph to evaluate true on-disk FlatBuffer size reduction via pruning.

### C. OPTIONAL EXPERIMENTS (Future Work):
1. **Custom Sparse TFLite Kernel:** Implement a Compressed Sparse Row (CSR) or Compressed Sparse Column (CSC) micro-kernel for TFLite Micro to evaluate whether $75\%$ weight sparsity can achieve on-chip latency speedups on ARM Cortex-M.
2. **Multi-Dataset Validation:** Extend the 12-model compression pipeline to an additional tabular edge dataset (e.g., UCI Human Activity Recognition or industrial pump vibration).

### D. NO EXPERIMENT REQUIRED:
The core contribution of Paper 2—the empirical 3-objective Pareto characterization and low-level FlatBuffer artifact benchmark of 12 serialized models—is fully supported by the existing verified artifacts in `results/tinyml_model_profile_verified.csv`.

---

## 7. Paper 2 Final Revision Level

**FINAL REVISION LEVEL: MODERATE_REVISION**

**Summary:** The revisions required for Paper 2 are structural, conceptual, and terminological:
1. Transition from 4D to 3D Deployment-Resource Pareto Frontier (Accuracy, Binary Size, Active MACs).
2. Correct the pruning terminology from "Structured" to "Unstructured Magnitude Pruning".
3. Reframe host latency as a secondary empirical benchmark.
4. Expand the 2020–2026 related work comparative positioning.
5. Tone down minor promotional phrases.

*All required changes can be executed directly within the existing experimental evidence base without regenerating data, retraining models, or running new experiments.*
