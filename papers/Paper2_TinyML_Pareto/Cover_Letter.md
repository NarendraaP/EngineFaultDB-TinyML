# Submission Cover Letter

**To:** Editor-in-Chief  
*ACM Transactions on Design Automation of Electronic Systems (TODAES)*  
Association for Computing Machinery  

**Date:** August 28, 2026  
**Manuscript Title:** Empirical Pareto Characterization of Model Compression Paradigms for Ultra-Low-Resource TinyML  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit the research manuscript entitled **"Empirical Pareto Characterization of Model Compression Paradigms for Ultra-Low-Resource TinyML"** for publication consideration in *ACM Transactions on Design Automation of Electronic Systems (TODAES)*.

### Research Problem & Motivation
Ultra-low-power microcontrollers (MCUs) operate under strict memory ($\le 64$\,KB SRAM, $\le 256$\,KB Flash) and computational boundaries. While individual compression techniques (quantization, pruning, distillation, feature selection) are widely studied in isolation, their joint multi-objective interactions under sub-4\,KB storage and sub-400 MAC constraints remain insufficiently characterized across serialized deployment binaries.

### Key Contributions & Major Empirical Findings
1. **Empirical 3-Objective Deployment-Resource Pareto Characterization:** We empirically profile 12 disk-serialized TensorFlow Lite FlatBuffer models on 55,998 multi-sensor engine diagnostic records across Test Accuracy (maximize), Serialized Binary Size (minimize), and Theoretical Active MACs (minimize), identifying exactly 6 non-dominated Pareto configurations.
2. **Robustness of the Deployment Frontier:** We demonstrate that formulating the primary Pareto space over deterministic deployment resources preserves the exact set of six Pareto-optimal configurations, with empirical host latency reported as a secondary execution baseline.
3. **Low-Level FlatBuffer Artifact Benchmark:** We expose that unstructured magnitude pruning achieves significant arithmetic reduction (75% pruning requires only 96 active MACs) but exhibits **"computational sparsity without demonstrated storage compression"** in standard FlatBuffers (3,920 B vs. 3,892 B dense baseline), proving that structural distillation is required for physical Flash reduction.
4. **Integer Purity:** Full INT8 quantization achieves zero-floating-point execution graphs (0 float32 tensors) with minimal accuracy variation (-0.04% to +0.44%).
5. **Venue & Page Alignment:** The 6-page manuscript is formatted and submission-ready for ACM TODAES (or IEEE TCAD).

### Declarations
- **Originality & Dual Submission:** [CONFIRM ORIGINALITY / NO SIMULTANEOUS SUBMISSION - The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere].
- **Reproducibility:** All 12 candidate FlatBuffer models, preprocessing scalers, and verification scripts are publicly archived.

Thank you for your editorial consideration.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
