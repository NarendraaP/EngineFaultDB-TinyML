# Submission Cover Letter

**To:** Editor-in-Chief  
*ACM Transactions on Design Automation of Electronic Systems (TODAES)*  
Association for Computing Machinery  

**Date:** August 22, 2026  
**Manuscript Title:** Empirical Pareto Frontier of Model Compression for Ultra-Low-Resource TinyML  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit the research manuscript entitled **"Empirical Pareto Frontier of Model Compression for Ultra-Low-Resource TinyML"** for publication consideration in *ACM Transactions on Design Automation of Electronic Systems (TODAES)*.

### Research Problem & Motivation
Ultra-low-power microcontrollers (MCUs) operate under strict memory (<=64 KB SRAM, <=256 KB Flash) and computational limits. While individual compression techniques (quantization, pruning, distillation, feature selection) are widely studied in isolation, their joint multi-objective interactions under sub-4 KB storage and sub-400 MAC constraints remain insufficiently characterized across serialized deployment binaries.

### Key Contributions & Major Empirical Findings
1. **Empirical 4D Pareto Characterization:** We empirically evaluate 12 disk-serialized TensorFlow Lite FlatBuffer models on 55,998 multi-sensor engine records across Test Accuracy, Model Size, Theoretical Active MACs, and Empirical Host Latency, identifying exactly 6 non-dominated Pareto configurations.
2. **Low-Level FlatBuffer Artifact Benchmark:** We expose that unstructured magnitude pruning achieves significant arithmetic reduction (75% pruning requires only 96 active MACs) but exhibits **"computational sparsity without demonstrated storage compression"** in standard FlatBuffers (3,920 B vs. 3,892 B), proving that structural distillation is required for physical Flash reduction.
3. **Integer Purity:** Full INT8 quantization achieves zero-floating-point execution graphs (0 float32 tensors) with minimal accuracy variation (-0.04% to +0.44%).
4. **Venue & Page Alignment Note:** The current 6-page manuscript is formatted and submission-ready for ACM TODAES (or IEEE TCAD). IEEE Embedded Systems Letters would require a separate 4-page condensation.

### Declarations
- **Originality & Dual Submission:** [CONFIRM ORIGINALITY / NO SIMULTANEOUS SUBMISSION - The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere].
- **Reproducibility:** All 12 candidate FlatBuffer models, preprocessing scalers, and verification scripts are publicly archived.

Thank you for your editorial consideration.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
