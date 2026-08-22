# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Industrial Informatics*  
IEEE Industrial Electronics Society  

**Date:** August 22, 2026  
**Manuscript Title:** Hierarchical Multi-Fidelity Machine Learning for Compute-Efficient Automotive Diagnostics  
**Author(s):** Antigravity Research Team  
**Article Type:** Regular Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

We are pleased to submit our original research manuscript entitled **\"Hierarchical Multi-Fidelity Machine Learning for Compute-Efficient Automotive Diagnostics\"** for publication in *IEEE Transactions on Industrial Informatics*.

### Research Problem & Motivation
Real-time fault detection and isolation in automotive powertrains imposes substantial computational burdens on Electronic Control Units (ECUs). In real-world operation, internal combustion engines operate in nominal, healthy regimes for $>90\%$ of their lifespan. Indiscriminately executing monolithic multi-class neural networks across every healthy observation squanders critical ECU computing capacity.

### Key Contributions & Major Empirical Findings
1. **Asymmetric Hierarchical Inference Architecture:** We develop a two-tier cascade combining a lightweight binary anomaly filter (Decision Tree =5$, $ MACs) with an uncertainty-gated deep neural diagnostician (MLP, $ MACs).
2. **Empirical Diagnostic Benchmark:** Evaluated on the 55,998-record EngineFaultDB physical benchmark, our cascade matches the diagnostic accuracy of a monolithic deep network (.64\%$ vs. .66\%$) while eliminating .36\%$ of expensive multi-class evaluations on balanced test data (and an expected .8\%$ on \%$ nominal operational telemetry).
3. **Safety Guarantee:** Through validation-only threshold tuning ($\theta^* = 0.05$), the system maintains a .98\%$ anomaly detection recall (.00025$ false-negative rate, missing only 2 anomalies out of 8,000).

### Venue Fit & Originality Declaration
*IEEE Transactions on Industrial Informatics* is the leading venue for industrial cyber-physical systems, intelligent diagnostics, and edge computing. Our work delivers an efficient, safety-compliant diagnostic architecture designed specifically for embedded vehicle controllers.

This manuscript is original and is not currently under submission elsewhere.

Sincerely,  
**Antigravity Research Team**  
*QoS-Aware TinyML Research Platform*  
