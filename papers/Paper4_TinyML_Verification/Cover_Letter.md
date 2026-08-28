# Submission Cover Letter

**To:** Program Chairs and Editors  
*ACM SIGPLAN/SIGBED Conference on Languages, Compilers, and Tools for Embedded Systems (LCTES)* / *IEEE Software*  

**Date:** August 28, 2026  
**Manuscript Title:** An Artifact-Driven Verification Protocol for Reproducible TinyML Deployment Evaluation  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Original Research Paper  

Dear Program Chairs and Editorial Board Members,

I am pleased to submit the original research manuscript entitled **"An Artifact-Driven Verification Protocol for Reproducible TinyML Deployment Evaluation"** for publication consideration.

### Research Problem & Motivation
The deployment of deep learning models on resource-constrained microcontrollers (TinyML) involves complex, multi-stage software translation and compilation pipelines (post-training quantization, magnitude pruning, FlatBuffer schema serialization, and C-array code generation). In empirical edge AI literature, training-time in-memory metrics frequently diverge from disk-serialized binary behavior, theoretical weight sparsity is routinely conflated with physical storage compression, and host simulation timings are improperly extrapolated to microcontroller real-time guarantees.

### Key Contributions & Major Empirical Findings
1. **7-Dimensional Artifact Verification Protocol:** We formulate an artifact-driven empirical verification protocol spanning seven core dimensions (D1--D7): Data Isolation, Serialized Binary Integrity, Quantization Graph Inspection, Sparsity vs. Storage Decoupling, Computation Accounting, Timing Protocols, and Runtime Non-Leakage.
2. **Formal Programmatic Predicates:** We formalize seven executable verification predicates ($\mathcal{P}_1 \dots \mathcal{P}_7$) with deterministic pass/fail execution procedures that parse compiled disk binaries directly.
3. **End-to-End Case Study & Defect Taxonomy:** Demonstrated on an end-to-end TinyML case study auditing 12 candidate neural network models on the 55,998-record EngineFaultDB physical benchmark, our audit uncovered, categorized, and resolved 20 numerical discrepancies across four defect modes (with metric variances up to $7.82\%$).
4. **Quantified Threshold Contamination Bias:** We **empirically demonstrate a $+1.80\%$ optimistic accuracy bias when runtime gating thresholds are optimized directly on test data**, proving that split-isolated calibration is mandatory for defensible deployment claims.
5. **Rigorous Evidence Tiering & Scope Boundaries:** We formalize a 5-tier evidence classification framework separating direct empirical measurements, reproducible trace simulations, and derived operational estimates. The manuscript clearly bounds its empirical demonstration to tabular feedforward networks in TFLite FlatBuffers.

### Declarations
- **Originality & Dual Submission:** The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere.
- **Artifact Availability:** The complete verification suite (`scripts/phase4_5_verification.py`), audited model binaries, and discrepancy logs are open-sourced for peer inspection.

Thank you for your editorial consideration.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
