# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Industrial Informatics*  
IEEE Industrial Electronics Society  

**Date:** August 22, 2026  
**Manuscript Title:** Hierarchical Multi-Fidelity Machine Learning for Compute-Efficient Automotive Diagnostics  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Regular Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit the original research manuscript entitled **"Hierarchical Multi-Fidelity Machine Learning for Compute-Efficient Automotive Diagnostics"** for publication consideration in *IEEE Transactions on Industrial Informatics*.

### Research Problem & Motivation
Real-time fault detection and isolation in automotive powertrains imposes substantial computational burdens on Electronic Control Units (ECUs). In real-world operation, internal combustion engines operate in nominal, healthy regimes for >90% of their lifespan. Indiscriminately executing monolithic multi-class neural networks across every healthy observation squanders critical ECU computing capacity.

### Key Contributions & Major Empirical Findings
1. **Asymmetric Hierarchical Inference Architecture:** We develop a domain-specific two-tier cascade combining a lightweight binary anomaly filter (Decision Tree d=5, 0 MACs) with an uncertainty-gated deep neural diagnostician (MLP, 384 MACs).
2. **Empirical Diagnostic Benchmark:** Evaluated on the 55,998-record EngineFaultDB physical benchmark, our cascade matches the diagnostic accuracy of a monolithic deep network (74.64% vs. 74.66%) while achieving:
   - A **26.36% empirical reduction in active MACs** (282.8 vs. 384.0 expected MACs) on the balanced test distribution.
   - An **89.8% derived expected computational reduction** under the explicitly defined operational assumption of 90% nominal telemetry streams.
3. **High Anomaly Recall via Validation-Only Calibration:** Through validation-only threshold tuning (theta* = 0.05), the cascade achieves **99.98% anomaly recall on the evaluated test partition** (0.00025 false-negative rate, missing only 2 anomalies out of 8,000 in the test set). The architecture is not claimed to be formally safety-certified.
4. **Dataset Scope:** The manuscript explicitly declares that EngineFaultDB represents controlled steady-state dynamometer observations rather than transient on-road drive cycles.

### Declarations
- **Originality & Dual Submission:** [CONFIRM ORIGINALITY / NO SIMULTANEOUS SUBMISSION - The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere].
- **Reproducibility:** All model weights, evaluation scripts, and dataset splits are publicly accessible.

Thank you for your editorial review.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
