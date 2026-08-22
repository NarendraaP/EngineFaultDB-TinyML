# Research Publication Strategy & Roadmap — Phases 1–5

**Project:** QoS-Aware TinyML Runtime Research  
**Dataset:** EngineFaultDB (`EngineFaultDB_Final.csv`, 55,998 rows)  
**Authoritative Evidence Base:** Complete Phases 1–5  
**Physical Hardware Status:** `PENDING_PHYSICAL_ESP32`  
**Date:** August 20, 2026  

---

## 1. Executive Recommendation

```
RECOMMENDED PAPER COUNT = 4 STANDALONE PAPERS (CURRENT EVIDENCE)
                         + 1 FUTURE HARDWARE DEPLOYMENT PAPER (POST-ESP32)
                         =================================================
                         TOTAL PLANNED PORTFOLIO: 5 HIGH-IMPACT PUBLICATIONS
```

### Publication Portfolio Classification
- **CORE PAPERS (Current Evidence):**
  - **Paper 1 (Flagship Systems):** *QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention*
  - **Paper 2 (Edge ML / TinyML):** *Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML*
  - **Paper 3 (Domain / Industrial Informatics):** *Hierarchical Multi-Fidelity Machine Learning Framework for Real-Time Engine Fault Diagnostics*
- **STRONG SECONDARY / METHODOLOGY PAPER (Current Evidence):**
  - **Paper 4 (Methodology / Software Engineering):** *Methodological Pitfalls and Empirical Verification Protocols in Microcontroller TinyML Research*
- **FUTURE PAPER (Pending Physical Hardware):**
  - **Paper 5 (Hardware Deployment):** *On-Device Deployment and Real-Time Hardware Validation of QoS-Aware TinyML on ESP32 Microcontrollers*
- **DO NOT SPLIT (Rejected Salami Slices):**
  - *Workload Contention Slice:* Must remain within Paper 1.
  - *Quantization vs Pruning Slice:* Must remain within Paper 2.
  - *Feature Redundancy Slice:* Must remain within Paper 3.
  - *Threshold Sweeping Slice:* Must remain within Paper 3.

---

## 2. Paper-by-Paper Comprehensive Proposals

---

### 📄 PAPER 1: QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI
- **Target Venues:** *IEEE Transactions on Computers*, *ACM Transactions on Embedded Computing Systems (TECS)*, or *IEEE Real-Time Systems Symposium (RTSS)*.
- **Research Question:** How can resource-constrained edge systems dynamically balance multi-class inference accuracy, active compute load, and strict deadline compliance under unpredictable CPU contention without accessing ground truth?
- **Hypothesis:** A Pareto-guided multi-fidelity runtime dynamically switching between quantized/pruned models based on deadline headroom can maintain $>74.8\%$ diagnostic accuracy while reducing active computational MACs by $>65\%$ under heavy contention compared to static execution.
- **Technical Contribution:**
  1. Multi-fidelity runtime architecture with single-sample execution abstraction (`ModelAdapter`).
  2. Pareto-optimal controller mapping operational modes (`FAST`, `BALANCED`, `HIGH_FIDELITY`).
  3. Four dynamic QoS policies (`ACCURACY_PRIORITY`, `BALANCED`, `DEADLINE_PRIORITY`, `COMPUTE_PRIORITY`).
  4. Trace-driven simulation methodology evaluating contention degradation over 11,200 held-out test frames.
- **Independent Variables:** Configured Deadline ($5, 10, 20, 50, 100\text{ ms}$), Workload Contention Level (`LOW`, `MEDIUM`, `HIGH`, `BURST`), QoS Policy.
- **Dependent Variables:** Overall Accuracy, Macro F1, Anomaly False-Negative Rate, Deadline Compliance Rate, Model Switch Rate, Active MACs, Host Latency (Mean, P95, P99).
- **Datasets & Workloads:** EngineFaultDB (11,200 test samples) under 4 synthetic CPU contention profiles.
- **Models Used:** `student_a_8_4_fp32` (FAST), `pruned_mlp_14f_75pct` (BALANCED), `student_b_16_4_fp32` (HIGH_FIDELITY).
- **Baselines:** Static High-Fidelity execution, Static Fast execution, QoS without workload awareness, QoS without deadline constraints.
- **Ablation Studies:** 4-way controlled ablation study (Ablations A, B, C, D in `results/phase5_ablation_results.csv`).
- **Primary Figures:**
  - `figures/phase5_policy_comparison.png` (4-panel heatmap matrix)
  - `figures/phase5_accuracy_vs_workload.png` (Accuracy vs Workload)
  - `figures/phase5_deadline_compliance_vs_workload.png` (Deadline compliance across deadlines)
  - `figures/phase5_ablation.png` (4-panel ablation comparisons)
- **Primary Tables:**
  - Policy comparison table across 80 configurations (`results/phase5_policy_comparison.csv`).
  - Ablation summary table (`results/phase5_ablation_results.csv`).
- **Expected Scientific Conclusion:** Dynamic QoS-aware model switching provides a superior Pareto trade-off under contention, eliminating deadline misses while matching the macro F1 ($0.7563$) of high-fidelity models at a fraction of the compute cost.
- **Available Evidence:** `[A] Host Empirical`, `[B] Trace-Driven Simulation`, `[C] Model Experiments` (100% complete in Phase 5).
- **Missing Evidence:** Physical on-chip execution timings (optional upgrade; does not block submission as a simulation/systems paper).

---

### 📄 PAPER 2: Empirical Pareto Frontier of Model Compression Paradigms for TinyML
- **Target Venues:** *IEEE Embedded Systems Letters (ESL)*, *ACM Transactions on Design Automation of Electronic Systems (TODAES)*, or *TinyML Research Symposium*.
- **Research Question:** How do post-training integer quantization, magnitude pruning, and student distillation interact under strict sub-4KB memory and sub-400 MAC budgets, and why do theoretical MAC reductions decouple from FlatBuffer storage compression?
- **Hypothesis:** Knowledge distillation produces denser structural compression with higher accuracy retention than unstructured pruning, while full INT8 quantization achieves identical functional accuracy with pure integer arithmetic (0 float32 tensors).
- **Technical Contribution:**
  1. Systematic multi-paradigm compression benchmark comparing 12 candidate models across quantization, pruning, and distillation.
  2. Proof and analysis of the FlatBuffer sparsity-storage decoupling phenomenon in standard TFLite runtimes.
  3. Formal verification of full integer arithmetic graphs (INT8 input/output with zero floating-point kernels).
  4. Multi-objective Pareto frontier extraction across Accuracy, Active MACs, Latency, and Storage Footprint.
- **Independent Variables:** Compression Paradigm (FP32 baseline, Full INT8, Pruning 0–75%, Distillation 8-4 / 16-4), Feature Dimensionality (14f vs 12f).
- **Dependent Variables:** Parameters, FlatBuffer File Size (Bytes/KB), Theoretical MACs, Active MACs, Zero-Weight Percentage, Single-Sample Latency (Mean, Median, P95, P99, Min, Max), Test Accuracy, Macro F1.
- **Datasets & Models:** 12 serialized `.tflite` models evaluated on 11,200 EngineFaultDB test samples.
- **Baselines:** Uncompressed baseline MLP (14f FP32, 412 parameters, 384 MACs).
- **Ablations:** 14-feature vs 12-feature inputs, INT8 vs FP32 precision across identical architectures.
- **Primary Figures:**
  - `figures/pareto_frontier.png` (Multi-objective Pareto frontier)
  - `figures/accuracy_vs_macs.png` (Accuracy vs Active MACs)
  - `figures/accuracy_vs_model_size.png` (Accuracy vs Storage Size)
  - `figures/fp32_vs_int8_accuracy.png` (Quantization fidelity comparison)
- **Primary Tables:**
  - Authoritative verified model profile table (`results/tinyml_model_profile_verified.csv`).
- **Expected Scientific Conclusion:** Student distillation (`student_b_16_4_fp32`) achieves the optimal accuracy-size trade-off ($75.14\%$ accuracy at $3.50\text{ KB}$), while 75% pruning achieves the lowest active computational load ($96\text{ MACs}$) without compressing dense storage.
- **Available Evidence:** `[A] Host Empirical`, `[C] Model Experiments`, `[D] Verified FlatBuffer Profiles` (100% complete in Phase 4.5).
- **Missing Evidence:** None. 100% submission-ready.

---

### 📄 PAPER 3: Hierarchical Multi-Fidelity Machine Learning Framework for Real-Time Engine Fault Diagnostics
- **Target Venues:** *IEEE Transactions on Industrial Informatics*, *Mechanical Systems and Signal Processing (MSSP)*, or *Reliability Engineering & System Safety*.
- **Research Question:** How can domain-specific sensor collinearity analysis and an asymmetric hierarchical cascade optimize diagnostic throughput and compute efficiency in combustion engine fault classification?
- **Hypothesis:** Leveraging collinearity reduction to eliminate redundant sensor dimensions combined with a low-complexity binary screening classifier will bypass $42.8\%$ of heavy multi-class evaluations with zero false-negative leakage on critical fault classes.
- **Technical Contribution:**
  1. Statistical sensor collinearity audit discovering perfect redundant pairs (`AFR`/`Lambda`, `Speed`/`RPM`) on 55,998 operational records.
  2. Input dimensionality optimization reducing sensor acquisition complexity from 14 to 12 features with $99.6\%$ accuracy retention.
  3. Hierarchical asymmetric cascading architecture (Binary Decision Tree Mode A $\rightarrow$ Multi-Class MLP Mode B).
  4. Strictly validation-calibrated optimal threshold selection ($T_{opt}=0.80$) preventing test-set contamination.
- **Independent Variables:** Feature Subset (14f vs 12f), Classifier Architecture (LR, DT depth-3, DT depth-5, MLP), Routing Confidence Threshold ($T \in [0.50, 0.95]$).
- **Dependent Variables:** Fault Classification Accuracy, Per-Class Precision/Recall/F1, Confusion Matrices, ROC-AUC, PR-AUC, Diagnostic Activation Rate, Trigger Rate.
- **Datasets & Models:** EngineFaultDB (55,998 samples across 4 operating classes: Normal, Fault 1, Fault 2, Fault 3).
- **Baselines:** Single-stage monolithic multi-class MLP, Single-stage Decision Tree, 14-feature unoptimized baseline.
- **Ablations:** Full 14f vs Reduced 12f across all models; Threshold sweeps ($T=0.50$ to $T=0.95$).
- **Primary Figures:**
  - `results/mode_a_roc_pr_curves.png` (Mode A screening ROC and PR curves)
  - `figures/qos_policy_frontier.png` (Cascading trigger-rate frontier)
  - `results/confusion_matrix_mlp.png` & `results/confusion_matrix_mlp_reduced.png`
  - `figures/threshold_vs_accuracy.png` & `figures/threshold_vs_trigger_rate.png`
- **Primary Tables:**
  - Dataset distribution and correlation matrix (`Dataset_Audit_Report.md`).
  - Baseline model comparison table (`results/baseline_metrics.csv`).
  - Cascading validation vs test threshold sweep table (`results/qos_threshold_sweep_test.csv`).
- **Expected Scientific Conclusion:** Feature redundancy removal combined with asymmetric confidence-gated cascading reduces diagnostic compute by $42.8\%$ while guaranteeing $1.000$ recall on catastrophic fault states.
- **Available Evidence:** `[C] Model Experiments`, `[D] Statistical Audits` (100% complete in Phases 1–3).
- **Missing Evidence:** None. 100% submission-ready.

---

### 📄 PAPER 4: Methodological Pitfalls and Empirical Verification Protocols in Microcontroller TinyML Research
- **Target Venues:** *IEEE Transactions on Software Engineering (TSE)*, *IEEE Software*, or *ACM Transactions on Software Engineering and Methodology (TOSEM)*.
- **Research Question:** What empirical and methodological pitfalls systematically bias published TinyML benchmarks, and how can an automated 15-point verification protocol restore reproducibility and measurement integrity?
- **Hypothesis:** Subtle methodological flaws—such as test-set threshold optimization, batch latency extrapolation, and confusing theoretical sparsity with storage compression—produce statistically significant optimistic biases in edge AI claims that automated artifact auditing can expose and resolve.
- **Technical Contribution:**
  1. Formalization of a 15-point TinyML Scientific Verification Protocol covering data leakage, timing jitter isolation, tensor graph verification, and evidence categorization.
  2. Quantitative demonstration of threshold optimization leakage creating a $+1.8\%$ artificial accuracy bias when test sets are re-used.
  3. Real-world case study documenting the discovery, categorization, and formal resolution of 20 numerical discrepancies and 3 terminology errors in serialized embedded AI models.
  4. Reproducible auditing framework incorporating deterministic seeds, single-sample timing harnesses, and strict host-vs-MCU evidence boundaries.
- **Independent Variables:** Verification Methodology (Unverified reported claims vs Independently audited artifacts), Threshold Split Protocol (Validation-isolated vs Test-contaminated).
- **Dependent Variables:** Discrepancy Magnitude, Accuracy Bias Percentage, Tensor Count Verification (FP32 vs INT8), Active MAC vs Dense Storage Disparity.
- **Primary Figures:**
  - Verified vs original discrepancy distributions (`Phase4_5_Independent_Verification.md`).
  - Verification workflow decision tree diagram.
- **Primary Tables:**
  - 20-point discrepancy resolution matrix (`Phase4_5_Independent_Verification.md`).
  - 11-point scientific audit compliance checklist (`Phase5_Software_Runtime_Audit.md`).
- **Expected Scientific Conclusion:** Independent artifact verification and split-isolated thresholding are vital to prevent distorted performance claims in edge AI literature; standardized protocols ensure true reproducibility.
- **Available Evidence:** `[D] Statistical & Discrepancy Audits` (100% complete across Phases 3, 4.5, and 5N).
- **Missing Evidence:** None. 100% submission-ready.

---

### 📄 FUTURE PAPER 5: On-Device Deployment and Hardware Validation of QoS-Aware TinyML on ESP32 Microcontrollers
- **Target Venues:** *IEEE Internet of Things Journal*, *IEEE Transactions on Computer-Aided Design (TCAD)*, or *ACM Transactions on Sensor Networks*.
- **Prerequisite:** Physical ESP32 hardware availability (`STATUS = PENDING_PHYSICAL_ESP32`).
- **Core Focus:** Real-world on-chip validation of the C byte-array runtime (`esp32_interface.md`), hardware timer profiling via `esp_timer_get_time()`, physical SRAM tensor arena allocation, FreeRTOS task preemption latency, and power profiling.

---

## 3. Publication Strategy Roadmap & Execution Details

### A. Recommended Publication Order & Writing Priority

```
Step 1: Write Paper 3 (Engine Fault Diagnostics Cascade)
        -> Fastest to write; self-contained domain contribution; 100% empirical evidence ready.

Step 2: Write Paper 2 (TinyML Model Compression & Pareto Frontier)
        -> Strong edge ML core; complete 12-model verified FlatBuffer dataset; zero missing data.

Step 3: Write Paper 4 (TinyML Methodology & Verification Protocols)
        -> Highly novel software engineering / benchmarking contribution based on Phase 4.5/5N audits.

Step 4: Write Paper 1 (QoS-Aware Multi-Fidelity Runtime - Flagship Systems)
        -> Synthesizes all software and simulation assets into the flagship systems manuscript.

Step 5: Execute Physical Hardware & Write Paper 5 (On-Device ESP32 Deployment)
        -> Immediately upon physical ESP32 arrival using pre-compiled phase5/firmware/ assets.
```

---

### B. Strategic Analysis Summary

| Strategy Metric | Designated Paper | Justification |
| :--- | :--- | :--- |
| **Paper to Write First** | **Paper 3** | Mature dataset, complete ROC/PR curves, self-contained automotive diagnostics narrative. |
| **Strongest Current Evidence** | **Paper 2** | Full INT8 FlatBuffers, 12 verified models, exact parameter/MAC/byte counts with zero estimation. |
| **Strongest Systems Contribution** | **Paper 1** | Dynamic scheduling under contention, 80 configurations, 4 QoS policies, 4-way system ablations. |
| **Paper Most Benefiting from ESP32** | **Paper 1 (or Paper 5)** | Elevates simulation-based scheduling to verified physical on-chip real-time execution. |

---

### C. Cross-Paper Experiment Sharing vs Exclusivity Boundaries

To eliminate any risk of self-plagiarism or duplicate publication:

- **Shared Supporting Artifacts (Allowed Across Papers):**
  - The base EngineFaultDB dataset description (`55,998` rows).
  - The canonical stratified data split ($40/40/20$, `seed=42`).
  - Standard MinMax normalization scaler (`models/scaler.pkl`).
- **Exclusive Scientific Assets (Strictly Segregated to Single Papers):**
  - *Paper 1 Exclusive:* 80-configuration trace simulation results (`phase5_policy_comparison.csv`), 4-way ablation studies (`phase5_ablation_results.csv`), and Phase 5 runtime scheduler code.
  - *Paper 2 Exclusive:* 12-model compression profile (`tinyml_model_profile_verified.csv`), sparsity-vs-storage decoupling analysis, and Pareto frontier plots.
  - *Paper 3 Exclusive:* Sensor collinearity matrices, 12f vs 14f input dimensionality reduction, and Mode A binary ROC/PR curves.
  - *Paper 4 Exclusive:* 20-discrepancy resolution audit table, mathematical threshold leakage demonstration, and 15-point TinyML verification protocol.
  - *Paper 5 Exclusive:* Physical on-chip ESP32 measurements, microsecond timer calibration, and FreeRTOS task timings.

---

## 4. Final Strategic Conclusion

The research conducted across Phases 1 through 5 provides a fully documented, methodologically airtight foundation supporting **4 distinct, top-tier standalone software/methodology publications right now**, with a direct, friction-free path to a **5th physical deployment publication** once physical ESP32 silicon is connected.
