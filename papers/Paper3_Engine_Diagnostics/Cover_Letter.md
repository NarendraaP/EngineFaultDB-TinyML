# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Industrial Informatics*  
IEEE Industrial Electronics Society  

**Date:** August 28, 2026  
**Manuscript Title:** Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Regular Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit the original research manuscript entitled **"Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis"** for publication consideration in *IEEE Transactions on Industrial Informatics*.

### Research Problem & Motivation
Real-time condition monitoring and fault isolation in automotive powertrains impose substantial computational burdens on Electronic Control Units (ECUs) and embedded microcontrollers. In real-world operation, internal combustion engines operate in nominal, healthy regimes for over $90\%$ of their lifespan. Indiscriminately executing monolithic multi-class deep neural networks across every healthy sensor observation squanders critical ECU computing capacity.

### Key Contributions & Major Empirical Findings
1. **Asymmetric Hierarchical Inference Architecture:** We develop a domain-specific two-tier cascade combining an ultra-lightweight binary anomaly filter (Decision Tree $d=5$, $0$ MACs) with an uncertainty-gated multi-class neural diagnostician (MLP, $384$ MACs).
2. **Empirical Diagnostic Benchmark & Baseline Context:** Evaluated on the 55,998-record EngineFaultDB physical benchmark, our cascade matches the diagnostic accuracy of a continuously executing monolithic deep network ($74.64\%$ vs. $74.66\%$) while significantly outperforming flat linear ($58.00\%$) and flat decision tree ($69.16\%$) baselines.
3. **Rigorous Computational Accounting:**
   - **Direct Test-Set Measurement [MEASURED TEST SET]:** Achieves a **$26.36\%$ empirical reduction in active arithmetic operations** ($282.8$ vs. $384.0$ expected MACs) on the balanced test distribution.
   - **Derived Operational Estimate [DERIVED OPERATIONAL ESTIMATE]:** Yields an **$89.8\%$ derived expected computational reduction** under the operational assumption of $90\%$ nominal telemetry streams ($39.1$ expected MACs).
4. **High Binary Anomaly-Screening Recall via Validation Calibration:** Through validation-only threshold calibration ($\theta^* = 0.05$), the cascade achieves **$99.98\%$ binary anomaly-screening recall** on the held-out test partition ($0.00025$ false-negative rate, missing only 2 anomalies out of 8,000 in the test set).
5. **Physical Error Analysis & Scope Boundaries:** The manuscript provides a domain-grounded physical analysis of sensor overlap between misfires and intake air leaks, and explicitly documents that EngineFaultDB represents static tabular steady-state dynamometer observations rather than continuous transient on-road drive cycles.

### Declarations
- **Originality & Dual Submission:** The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere.
- **Reproducibility:** All model weights, evaluation scripts, and dataset splits are publicly accessible.

Thank you for your editorial consideration.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
