# Paper Overlap Analysis & Independence Audit — Phases 1–5

**Project:** QoS-Aware TinyML Runtime Research  
**Dataset:** EngineFaultDB (`EngineFaultDB_Final.csv`, 55,998 rows)  
**Date:** August 20, 2026  

---

## 1. Candidate Papers Under Evaluation

We evaluate 6 potential paper concepts to determine true scientific independence versus overlap:

- **P1 (Flagship Systems):** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*
- **P2 (Edge ML / Compression):** *Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML*
- **P3 (Domain / Diagnostics):** *Hierarchical Multi-Fidelity Machine Learning Framework for Real-Time Engine Fault Diagnostics*
- **P4 (Methodology / Benchmarking):** *Methodological Pitfalls and Empirical Verification Protocols in Microcontroller TinyML Research*
- **P5 (Synthetic Scheduling Slice):** *Workload Contention Modeling and Adaptive Degradation for Edge Computing*
- **P6 (Quantization-Pruning Slice):** *INT8 Quantization versus Magnitude Pruning for Low-Power Microcontrollers*

---

## 2. Inter-Paper Overlap Matrix

| | P1 (QoS Systems) | P2 (TinyML Compression) | P3 (Engine Diagnostics) | P4 (Audit & Verification) | P5 (Workload Slice) | P6 (Quant/Prune Slice) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **P1** | — | **LOW** (Uses Pareto models as inputs) | **LOW** (Focuses on dynamic scheduling) | **LOW** (Evaluates systems, not audit methodology) | **HIGH** (P5 is a subset of P1) | **MEDIUM** (P1 uses pruned/quantized models) |
| **P2** | **LOW** | — | **LOW** (Model-level compression vs domain cascade) | **LOW** (P2 provides models; P4 audits discrepancies) | **LOW** | **HIGH** (P6 is an isolated subset of P2) |
| **P3** | **LOW** | **LOW** | — | **LOW** (Domain application vs verification protocol) | **LOW** | **LOW** |
| **P4** | **LOW** | **LOW** | **LOW** | — | **LOW** | **MEDIUM** (P4 uses P2/P3 audit case studies) |
| **P5** | **HIGH** | **LOW** | **LOW** | **LOW** | — | **LOW** |
| **P6** | **MEDIUM** | **HIGH** | **LOW** | **MEDIUM** | **LOW** | — |

---

## 3. The Six-Paper Independence Test

Each of the 6 candidate papers is subjected to the rigorous 6-question independence test:

---

### Candidate Paper P1: QoS-Aware Multi-Fidelity Runtime (Systems / Embedded AI)
1. **Unique Research Question:** How can resource-constrained edge systems dynamically balance multi-class inference fidelity, compute load, and strict deadline compliance under unpredictable CPU contention without accessing ground truth?
2. **Unique Technical Contribution:** The multi-fidelity QoS runtime architecture with Pareto-guided model selection, 4 QoS policies (`ACCURACY_PRIORITY`, `BALANCED`, `DEADLINE_PRIORITY`, `COMPUTE_PRIORITY`), and dynamic single-sample scheduling.
3. **Primary Experiment:** Trace-driven simulation across 80 configurations (5 deadlines $\times$ 4 workloads $\times$ 4 policies) over 11,200 held-out test frames, plus 4 controlled ablation studies.
4. **Non-Relocatable Result:** Demonstrating that the `BALANCED` policy achieves a **68.4% active MAC reduction** (96 vs 304 MACs) with a **$+0.0173$ higher macro F1** under high contention compared to static execution.
5. **Standalone Novelty:** Remains completely novel as an embedded systems / real-time AI scheduling framework even if all other papers are disregarded.
6. **Salami-Slicing Risk:** None.
- **VERDICT: PASS (Strong Standalone)**

---

### Candidate Paper P2: Empirical Pareto Frontier of TinyML Compression (Edge ML)
1. **Unique Research Question:** How do post-training integer quantization, magnitude pruning, and student distillation interact under sub-4KB memory and sub-400 MAC budgets, and why do theoretical MAC savings diverge from storage compression in edge FlatBuffers?
2. **Unique Technical Contribution:** Comprehensive multi-paradigm compression benchmark of 12 candidate models, mathematical proof of FlatBuffer density-vs-sparsity decoupling, full integer INT8 graph verification (0 float32 tensors), and multi-objective Pareto frontier identification.
3. **Primary Experiment:** Single-sample profiling across 12 models measuring file size, parameter count, theoretical vs active MACs, host latency distributions (Mean, Median, P95, P99, Min, Max), Test Accuracy, and Macro F1.
4. **Non-Relocatable Result:** Demonstrating that 75% magnitude pruning yields 4x active MAC reduction (384 $\rightarrow$ 96 MACs) while preserving 74.82% accuracy, but maintains a dense 3,920-byte FlatBuffer storage footprint unless specialized sparse kernels are implemented.
5. **Standalone Novelty:** Remains completely novel as a deep-dive model compression and TinyML architectural efficiency study.
6. **Salami-Slicing Risk:** None.
- **VERDICT: PASS (Strong Standalone)**

---

### Candidate Paper P3: Hierarchical Multi-Fidelity Engine Diagnostics (Fault Diagnostics / Automotive)
1. **Unique Research Question:** How can domain-specific sensor collinearity and an asymmetric hierarchical cascade optimize real-time fault detection efficiency across multi-cylinder combustion engine sensor streams?
2. **Unique Technical Contribution:** Statistical feature redundancy discovery (AFR/Lambda $r=1.000$, Speed/RPM $r=0.999$), input dimensionality reduction to 12 features with 99.6% accuracy retention, asymmetric binary screening $\rightarrow$ multi-class MLP cascade, and validation-only optimal threshold calibration ($T_{opt}=0.80$) with zero test leakage.
3. **Primary Experiment:** Train/val/test evaluation of Decision Tree, Logistic Regression, and MLP classifiers on 14-feature and 12-feature subsets, followed by receiver operating characteristic (ROC), precision-recall (PR), and threshold sweep experiments.
4. **Non-Relocatable Result:** 42.8% reduction in execution activations for nominal frames with zero degradation in catastrophic fault recall ($1.000$ recall on Fault 1 and Fault 3) and zero test-set contamination.
5. **Standalone Novelty:** Fully standalone as an applied automotive informatics, machinery diagnostics, and cyber-physical monitoring paper.
6. **Salami-Slicing Risk:** None.
- **VERDICT: PASS (Strong Standalone)**

---

### Candidate Paper P4: Methodological Pitfalls & Verification Protocols in TinyML (Methodology / Software Engineering)
1. **Unique Research Question:** What methodological flaws commonly distort TinyML literature (e.g., test-set contamination during threshold selection, batch latency misreported as single-sample, host timings claimed as MCU WCET, dense storage misreported as compression), and how can a standardized verification protocol prevent them?
2. **Unique Technical Contribution:** A 15-point empirical verification protocol for edge ML research, coupled with an audited case study demonstrating how 20 distinct numerical discrepancies and 3 terminology errors were uncovered and resolved.
3. **Primary Experiment:** Dual-pass independent verification of serialized FlatBuffer binaries, exact tensor graph inspection, timing jitter isolation, and ablation of validation-vs-test threshold optimization leakage.
4. **Non-Relocatable Result:** Empirical demonstration that selecting routing thresholds directly on the test set produces an artificial $+1.8\%$ optimistic accuracy bias, proving the absolute necessity of split-isolated threshold optimization.
5. **Standalone Novelty:** Highly valuable to the reproducibility, benchmarking, and empirical software engineering communities (e.g., IEEE Transactions on Software Engineering, ACM TOMS, or MLSys Artifact/Benchmarking tracks).
6. **Salami-Slicing Risk:** Low, provided the paper is framed squarely around benchmarking methodology, reproducibility traps, and verification formalisms.
- **VERDICT: PASS (Strong Standalone)**

---

### Candidate Paper P5: Workload Contention Modeling for Edge AI
1. **Unique Research Question:** How does synthetic CPU contention impact fixed-priority inference?
2. **Analysis:** P5 merely isolates the synthetic workload multipliers ($1.0\times, 1.5\times, 3.0\times, 5.0\times$) and runs the same scheduler from P1.
3. **Salami-Slicing Assessment:** P5 lacks a distinct algorithmic or systems contribution. Publishing P5 separately would strip P1 of its core evaluation, resulting in two weak papers.
- **VERDICT: FAIL (Must be consolidated into P1)**

---

### Candidate Paper P6: INT8 Quantization vs Magnitude Pruning for Microcontrollers
1. **Unique Research Question:** Does INT8 or Pruning achieve higher compression on sensor MLPs?
2. **Analysis:** P6 merely takes 4 rows from the 12-model profile in P2 (comparing `mlp_14f_int8` vs `pruned_mlp_14f_75pct`).
3. **Salami-Slicing Assessment:** Dividing the 12-model compression study into separate "quantization" and "pruning" papers is classic salami slicing and would be rejected for trivial scope.
- **VERDICT: FAIL (Must be consolidated into P2)**

---

## 4. Evaluation of 7+ Paper Scenarios

Attempts to split the project into 7 or more papers (e.g., separating feature selection, baseline models, threshold analysis, workload generator, and individual ablation studies) are **categorically rejected**:
- It fragments unified scientific narratives.
- It produces papers with insufficient experimental depth that would fail peer review at reputable venues.
- It violates scientific publishing ethics regarding incremental duplication.

---

## 5. Comprehensive Research Gap Analysis

| Gap ID | Identified Research Gap | Status & Severity | Resolution Path |
| :--- | :--- | :--- | :--- |
| **G1** | Physical on-chip execution timing & SRAM memory profiling on genuine ESP32 silicon. | **REQUIRES ESP32** (High value for future work; does not block current software papers). | Execute C++ firmware via PlatformIO once hardware is available (`phase5/hardware/esp32_interface.md`). |
| **G2** | Multi-dataset validation (evaluating the QoS runtime on a second industrial sensor dataset, e.g., C-MAPSS or IMS Bearings). | **OPTIONAL STRENGTHENING** (Moderate value; EngineFaultDB already provides 55,998 rows and 11,200 test samples). | Recommended for journal expansion of P1. |
| **G3** | Dynamic closed-loop feedback controller adjusting thresholds continuously at runtime. | **REQUIRES NEW ALGORITHM** (Future research direction). | Potential follow-up research topic. |
| **G4** | Physical power consumption / current draw measurements under model switching. | **REQUIRES ESP32** (Hardware measurement). | Capture via USB power profiler / Nordic PPK2 during future hardware phase. |
| **G5** | Mathematical formulation of the 15-point TinyML audit protocol. | **REQUIRED FOR CURRENT PAPERS** (Already complete in Phase 4.5 & Phase 5N audits). | Formalize protocol definitions in P4 manuscript. |

---

## 6. Synthesis

- **Defensible Independent Papers from Existing Evidence:** **Exactly 4 Papers (P1, P2, P3, P4)**.
- **Future Physical Deployment Paper:** **1 Paper (P7)** upon physical ESP32 availability.
- **Total Publications:** **4 Software/Methodology Papers Now + 1 Physical Deployment Paper Later = 5 Total Papers**.
