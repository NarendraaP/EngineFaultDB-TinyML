# Research Paper Contribution Matrix — Phases 1–5

**Project:** QoS-Aware TinyML Runtime Research  
**Dataset:** EngineFaultDB (`EngineFaultDB_Final.csv`, 55,998 rows)  
**Authoritative Evidence Base:** Phases 1, 2, 3, 4, 4.5, 5 (Verified Model Profile, Runtime Traces, Policy Comparison, Ablation Studies, Scientific Audits)  
**Date:** August 20, 2026  

---

## 1. Evidence Strength Taxonomy

All evidence across the project is strictly categorized according to the following empirical hierarchy:

| Category Code | Evidence Classification | Definition & Scope | Integrity Constraint |
| :--- | :--- | :--- | :--- |
| **[A]** | **HOST EMPIRICAL** | Single-sample execution timings, parameter counts, FlatBuffer file sizes, memory footprint, and numerical outputs measured on the host PC. | Must never be cited as on-chip MCU latency. |
| **[B]** | **TRACE-DRIVEN SIMULATION** | Dynamic scheduling, workload contention injection, deadline compliance, and model switching evaluated over 11,200 held-out test frames. | Must never be cited as hardware WCET or ECU execution. |
| **[C]** | **MODEL-LEVEL EXPERIMENT** | Train/val/test performance (Accuracy, Precision, Recall, Macro F1, Confusion Matrices, ROC/PR curves) under strict stratified split ($40/40/20$, seed=42). | Complete test-set isolation; zero threshold optimization leakage. |
| **[D]** | **STATISTICAL / AUDIT ANALYSIS** | Collinearity analysis, feature correlation matrices, 20-point discrepancy verifications, and 11-point scientific audit verifications. | Verifiable mathematical proofs and code inspection records. |
| **[E]** | **AUXILIARY AVR EXPERIMENT** | Hardware bootloader interrogation, device signature extraction (`0x1E 0x95 0x0F`), and UART characterization on auxiliary ATmega328P/ATmega2560 boards. | Isolated to auxiliary boundaries; never cited as ESP32 or TinyML performance. |
| **[F]** | **FUTURE MCU EMPIRICAL** | Physical on-device execution measurements on genuine ESP32 silicon. | **STATUS = PENDING_PHYSICAL_ESP32** (Zero synthetic data). |

---

## 2. Contribution Discovery & Extraction

The project evidence base was audited across 11 potential research topics to determine candidate standalone validity:

| Research Topic Area | Associated Project Phase | Evidence Available | Evidence Strength | Standalone Feasibility |
| :--- | :--- | :--- | :--- | :--- |
| **A. TinyML Model Optimization & Pareto Frontier** | Phase 4, 4.5 | 12 models, 4 paradigms, Pareto frontier mapping, size vs MACs | `[A], [C], [D]` | **CORE CONTRIBUTION** (Paper 2) |
| **B. INT8 Quantization & Feature Reduction** | Phase 2, 4, 4.5 | Full INT8 verified tensors, 12f vs 14f ablation | `[A], [C], [D]` | SUPPORTING EXPERIMENT (Combine with A or C) |
| **C. Structured Pruning vs Active MACs** | Phase 4, 4.5 | 4 pruning levels, FlatBuffer density vs MAC decoupling | `[A], [C], [D]` | SUPPORTING EXPERIMENT (Combine with A) |
| **D. Knowledge Distillation for TinyML** | Phase 4, 4.5 | Student A (8-4) & Student B (16-4) architecture evaluations | `[A], [C], [D]` | SUPPORTING EXPERIMENT (Combine with A) |
| **E. Multi-Fidelity Cascaded Routing** | Phase 3 | Binary screening $\rightarrow$ MLP cascade, validation-only $T_{opt}=0.80$ | `[B], [C], [D]` | **CORE CONTRIBUTION** (Paper 3) |
| **F. QoS-Aware Runtime Scheduling** | Phase 5 | 4 QoS policies, dynamic mode switching, 80 test configurations | `[A], [B], [C]` | **CORE CONTRIBUTION** (Paper 1 - Flagship) |
| **G. Deadline-Aware Degradation** | Phase 5 | Deadlines 5–100 ms, deadline compliance tracking | `[B], [C]` | SUPPORTING EXPERIMENT (Integrate into Paper 1) |
| **H. Workload Contention Modeling** | Phase 5 | 4 synthetic workload profiles (`LOW`, `MED`, `HIGH`, `BURST`) | `[B]` | SUPPORTING EXPERIMENT (Integrate into Paper 1) |
| **I. 4-Way System Ablation Studies** | Phase 5 | Static Best vs QoS, Static Small vs QoS, $\pm$Workload, $\pm$Deadline | `[B], [C]` | SUPPORTING EXPERIMENT (Integrate into Paper 1) |
| **J. TinyML Audit & Verification Protocol** | Phase 3, 4.5, 5 | 20 discrepancy fixes, 11-point audit, single-sample timing rules | `[D]` | **CORE CONTRIBUTION** (Paper 4) |
| **K. Physical ESP32 Hardware Deployment** | Phase 5.1, 5K | Hardware discovery protocols, C headers, interface specifications | `[E], [F]` | **FUTURE PAPER** (Pending ESP32 silicon) |

---

## 3. Candidate Paper Contribution Matrix

| ID | Candidate Paper Concept | Core Problem Addressed | Primary Novel Contribution | Main Evidence Base | Independent Research Question? | Overlap Risk | Standalone Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **P1** | **QoS-Aware Multi-Fidelity TinyML Runtime** | Real-time deadline misses & compute contention under dynamic edge workloads. | Multi-mode Pareto scheduler with 4 QoS policies and workload-adaptive degradation. | Phase 5: 80 configurations, 4 ablations, `phase5_runtime_traces.csv`, 7 figures. | **YES (Systems)** | Low (Focuses on dynamic scheduling & runtime systems). | **STRONG STANDALONE (Flagship)** |
| **P2** | **Empirical Pareto Analysis of TinyML Compression** | Compression-accuracy-latency trade-offs across quantization, pruning, and distillation. | Multi-paradigm TinyML comparison; decoupling of theoretical active MACs from dense FlatBuffer file sizes. | Phase 4 & 4.5: 12 models profile, Pareto frontier, single-sample latency distributions. | **YES (Edge ML)** | Low (Focuses on model optimization & compression mechanics). | **STRONG STANDALONE** |
| **P3** | **Hierarchical Multi-Fidelity Engine Diagnostics** | Inefficient multi-class inference for high-frequency internal combustion engine fault monitoring. | Domain-specific sensor collinearity reduction + asymmetric binary screening cascade with zero leakage. | Phase 1, 2, 3: Collinearity audit, 12f/14f models, validation-only $T_{opt}=0.80$, 42.8% compute saving. | **YES (Diagnostics)** | Low (Focuses on automotive fault diagnostics & domain ML). | **STRONG STANDALONE** |
| **P4** | **Verification Protocols & Benchmarking Pitfalls in TinyML** | Pervasive methodological errors (data leakage, batch timing, false WCET, dense pruning claims) in edge ML. | 15-point empirical verification protocol; case study resolving 20 real discrepancies in embedded AI workflows. | Phase 3 Audit, Phase 4.5 Verification, Phase 5 Audit, verified vs reported discrepancies. | **YES (Methodology)** | Low (Focuses on research reproducibility & benchmarking science). | **STRONG STANDALONE** |
| **P5** | **Workload Contention Modeling for Edge AI** | Simulating CPU starvation on microcontrollers without hardware tracing. | Synthetic contention injection equations. | Phase 5F simulator only. | **NO** | **HIGH** (Integral component of P1). | **BETTER AS PART OF P1** |
| **P6** | **INT8 Quantization vs Pruning for Sensor ML** | Sub-4KB model trade-offs. | INT8 vs 75% pruning comparison. | Subset of Phase 4 profile. | **NO** | **HIGH** (Integral component of P2). | **BETTER AS PART OF P2** |
| **P7** | **Physical ESP32 On-Device Runtime Deployment** | Real-world hardware validation of multi-model execution. | Physical MCU profiling on ESP32 silicon. | Phase 5K interface + future on-device hardware data. | **YES (Hardware)** | Low (Empirical hardware paper). | **FUTURE STANDALONE (Pending ESP32)** |

---

## 4. Maximum Defensible Paper Count

Based on strict evaluation against salami slicing, scientific novelty, and domain specialization:

- **Current Evidence Base (Phases 1–5):** Supports exactly **4 Genuinely Independent, Technically Strong Standalone Papers** (P1, P2, P3, P4).
- **Future Physical Expansion (Post-ESP32):** Supports **1 Additional Hardware Deployment Paper** (P7), bringing the total to **5 Papers**.
- Any attempt to split the current software/simulation work into 6 or 7+ papers would result in salami slicing (e.g. carving out workload models or isolated quantization tables), degrading scientific rigor.
