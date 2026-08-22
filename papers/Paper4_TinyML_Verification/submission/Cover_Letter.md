# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Software Engineering* / *ACM TOSEM*  

**Date:** August 22, 2026  
**Manuscript Title:** An Independent Verification Framework for Reproducible TinyML Evaluation  
**Author(s):** Antigravity Research Team  
**Article Type:** Research Paper / Focused Empirical Study  

Dear Editor-in-Chief and Editorial Board Members,

We submit our original research manuscript entitled **\"An Independent Verification Framework for Reproducible TinyML Evaluation\"** for publication consideration in *IEEE Transactions on Software Engineering*.

### Research Problem & Motivation
The deployment of deep learning models on resource-constrained microcontrollers (TinyML) involves complex, multi-stage software compilation pipelines (quantization, pruning, FlatBuffer serialization, and C-array code generation). In empirical edge AI literature, training-time in-memory metrics frequently diverge from disk-serialized binary behavior, theoretical weight sparsity is conflated with physical storage compression, and host timings are improperly extrapolated to microcontroller real-time guarantees.

### Key Contributions & Major Empirical Findings
1. **Seven-Dimensional Verification Protocol:** We formalize an artifact-driven verification protocol spanning Data Isolation, Serialized Binary Integrity, Quantization Graph Inspection, Sparsity and MAC Accounting, Timing Protocols, Runtime Routing Non-Leakage, and Hardware Boundary Scoping.
2. **Empirical Discrepancy Resolution:** In an extensive case study auditing 12 candidate models, our independent audit exposed and resolved 20 numerical discrepancies between training-time logs and verified binary artifacts (with metric variances up to .82\%$).
3. **Leakage Quantification:** We empirically quantify that evaluating gating thresholds directly on test data introduces an artificial $+1.80\%$ optimistic accuracy bias, proving that split-isolated threshold calibration is mandatory for defensible scientific claims.

### Venue Fit & Originality Declaration
This manuscript contributes formal verification predicates, evidence tiering, and empirical auditing methodologies directly to the software engineering of machine learning systems (SE4ML).

The manuscript is completely original and is not under review elsewhere. All verification suites are open-sourced for peer evaluation.

Sincerely,  
**Antigravity Research Team**  
*QoS-Aware TinyML Research Platform*  
