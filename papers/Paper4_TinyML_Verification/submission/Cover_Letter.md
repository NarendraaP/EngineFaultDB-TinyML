# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Software Engineering*  
IEEE Computer Society  

**Date:** August 22, 2026  
**Manuscript Title:** An Independent Verification Framework for Reproducible TinyML Evaluation  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Focused Empirical Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit the research manuscript entitled **"An Independent Verification Framework for Reproducible TinyML Evaluation"** for publication consideration in *IEEE Transactions on Software Engineering*.

### Research Problem & Motivation
The deployment of deep learning models on resource-constrained microcontrollers (TinyML) involves complex, multi-stage software compilation pipelines (quantization, pruning, FlatBuffer serialization, and C-array code generation). In empirical edge AI literature, training-time in-memory metrics frequently diverge from disk-serialized binary behavior, theoretical weight sparsity is conflated with physical storage compression, and host timings are improperly extrapolated to microcontroller real-time guarantees.

### Key Contributions & Major Empirical Findings
1. **Empirical Verification Protocol:** We formulate an artifact-driven verification protocol spanning seven core dimensions (D1-D7): Data Isolation, Serialized Binary Integrity, Quantization Graph Inspection, Sparsity vs. Storage Accounting, MAC Profiling, Timing Protocols, and Runtime Routing Non-Leakage.
2. **End-to-End Case Study & Discrepancy Resolution:** Demonstrated on an end-to-end TinyML diagnostic case study auditing 12 candidate neural network models, our independent audit uncovered and resolved 20 numerical discrepancies between training-time logs and verified binary artifacts (with metric variances up to 7.82%).
3. **Quantified Leakage Bias:** We **empirically demonstrate a +1.80% optimistic accuracy bias when the gating threshold is selected directly on the test partition**, highlighting the necessity of split-isolated threshold calibration for defensible empirical claims.
4. **Scope Demarcation:** The protocol is demonstrated on tabular MLPs serialized in TFLite FlatBuffers; further validation across 2D CNNs, vision transformers, and alternative runtimes is identified as necessary for broader generalization.

### Declarations
- **Originality & Dual Submission:** [CONFIRM ORIGINALITY / NO SIMULTANEOUS SUBMISSION - The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere].
- **Artifact Availability:** The complete verification suite (scripts/phase4_5_verification.py) and audited model binaries are open-sourced for peer inspection.

Thank you for your editorial review and consideration.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
