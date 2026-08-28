# Phase 17G — Prior Art and Novelty Positioning Audit: Paper 4

**Manuscript:** An Independent Verification Framework for Reproducible TinyML Evaluation  
**Date:** August 28, 2026  

---

## 1. Prior Art Comparative Analysis (2020–2026)

We audited the 10 closest published works in machine learning reproducibility, TinyML benchmarking, software engineering for ML, and neural network verification.

| Prior Work | Primary Domain / Focus | Level of Abstraction | Artifact Type | Coverage of D1–D7 Dimensions | Key Differences / Gaps Addressed by Paper 4 |
|---|---|---|---|---|---|
| **Pineau et al.~\cite{pineau2021improving} (2021)** | ML Reproducibility Checklist | High-level scientific reporting guidelines | Code & narrative | Covers D1 (splits), D6 (seeds); does not cover D2--D5, D7 | Focuses on high-level ML papers; does not inspect binary artifact compilation, quantization graphs, or embedded FlatBuffers. |
| **Kapoor \& Narayanan~\cite{kapoor2023leakage} (2023)** | Data Leakage Survey across 17 Fields | Empirical meta-science audit | Code repositories | Covers D1 (data leakage); does not cover D2--D7 | Examines broad statistical leakage; does not address edge AI compilation, quantization, or sparsity-storage decoupling. |
| **Banbury et al.~\cite{banbury2021benchmarking} (2021)** | MLPerf Tiny Benchmark Suite | Standardized hardware benchmarking | C/C++ harness & hardware | Covers D6 (hardware latency/energy); does not audit D2, D4, D7 | Measures hardware throughput on fixed golden models; does not formalize software verification predicates or audit serialization drift. |
| **David et al.~\cite{david2021tensorflow} (2021)** | TensorFlow Lite Micro | Embedded runtime architecture | C++ interpreter | Covers D2, D3 runtime execution | Describes interpreter runtime mechanics; does not provide an independent verification protocol or defect audit. |
| **Blalock et al.~\cite{blalock2020state} (2020)** | What is the State of Pruning? | Meta-analysis of pruning literature | In-memory PyTorch/TF | Covers D4 (pruning metrics), D5 (MACs) | Identifies inconsistent baseline issues; does not examine post-training FlatBuffer export or physical storage density. |
| **Sculley et al.~\cite{sculley2015hidden} / Amershi et al.~\cite{amershi2019software}** | Software Engineering for ML / Technical Debt | SE design patterns & MLOps | Full pipeline | Covers high-level SE lifecycle | Outlines SE challenges conceptually; does not provide low-level verification scripts for compiled microcontroller binaries. |
| **Lin et al.~\cite{lin2020mcunet} (2020)** | MCUNet: TinyML on Microcontrollers | Model-compiler co-design | TinyEngine & C-code | Covers D3 (quantization), D6 (latency) | Develops custom inference engine; does not provide an independent verification or discrepancy audit methodology. |
| **Jacob et al.~\cite{jacob2018quantization} / Gholami et al.~\cite{gholami2022survey}** | Quantization Schemes & Surveys | Mathematical quantization theory | Quantized tensors | Covers D3 (quantization math) | Establishes quantization theory; does not formulate end-to-end verification checks across data, storage, and runtime. |
| **Paper 4 (This Work)** | **Compiled TinyML Verification Protocol** | **End-to-End Artifact Verification** | **Compiled FlatBuffers, Scalers, Code** | **Full 7-Dimensional Coverage (D1--D7)** | **First empirical protocol connecting training-time data isolation to compiled disk FlatBuffer graph inspection, exposing 20 discrepancies and sparsity-storage decoupling.** |

---

## 2. "First" / "Pioneering" Language Audit

We audited all instances of promotional or unproven priority language in Paper 4:

1. **"first-of-its-kind" / "pioneering":**  
   - *Status:* **REMOVED / NARROWED.**  
   - *Rationale:* Verification protocols, checklists, and ML audits exist in various forms. Claiming an absolute "first" is scientifically indefensible.
2. **"universal verification framework":**  
   - *Status:* **REWRITTEN to "empirical verification protocol for compiled TinyML deployment artifacts".**  
   - *Rationale:* The protocol is demonstrated on an end-to-end 12-model MLP case study; framing it as a "universal framework" overstates empirical scope.
3. **"formal verification":**  
   - *Status:* **REWRITTEN to "programmatic verification predicates and empirical artifact auditing".**  
   - *Rationale:* "Formal verification" in computer science implies automated theorem proving or SMT-solver based model checking (e.g., Marabou, Reluplex). Paper 4 performs empirical software testing and artifact property verification.

---

## 3. Defensible Novelty Statement

*"Paper 4 establishes an empirical verification protocol and defect taxonomy for compiled TinyML deployment artifacts. The contribution formalizes actionable verification predicates across seven core pipeline dimensions—from data split isolation to compiled FlatBuffer tensor graph inspection—and demonstrates their necessity through an exhaustive audit of 12 candidate models, resolving 20 numerical discrepancies and exposing fundamental sparsity-storage decoupling in embedded edge AI."*
