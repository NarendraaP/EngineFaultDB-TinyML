# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Embedded Systems Letters* / *ACM Transactions on Design Automation of Electronic Systems*  

**Date:** August 22, 2026  
**Manuscript Title:** Empirical Pareto Frontier of Model Compression for Ultra-Low-Resource TinyML  
**Author(s):** Antigravity Research Team  
**Article Type:** Research Letter / Technical Paper  

Dear Editor-in-Chief and Editorial Board Members,

We submit our original research manuscript entitled **\"Empirical Pareto Frontier of Model Compression for Ultra-Low-Resource TinyML\"** for consideration.

### Research Problem & Motivation
Ultra-low-power microcontrollers (MCUs) operate under strict memory ($\le 64$\,KB SRAM, $\le 256$\,KB Flash) and computational limits. While individual compression techniques (quantization, pruning, distillation, feature selection) are widely studied in isolation, their joint multi-objective interactions under sub-4\,KB storage and sub-400 MAC constraints remain insufficiently characterized across serialized deployment binaries.

### Key Contributions & Major Empirical Findings
1. **Four-Objective Empirical Pareto Frontier:** We empirically evaluate 12 disk-serialized TensorFlow Lite FlatBuffer models on 55,998 multi-sensor engine records across Test Accuracy, Model Size, Theoretical Active MACs, and Empirical Host Latency, identifying exactly 6 non-dominated Pareto configurations.
2. **FlatBuffer Sparsity-Storage Discovery:** We expose that unstructured magnitude pruning achieves significant computational reduction (\%$ pruning requires only $ active MACs) but exhibits *computational sparsity without demonstrated storage compression* in standard FlatBuffers (,920$\,B vs. ,892$\,B), proving that structural distillation is required for physical Flash savings.
3. **Integer Purity:** Full INT8 quantization achieves zero-floating-point execution graphs ($ float32 tensors) with minimal accuracy variation ($-0.04\%$ to $+0.44\%$).

### Venue Fit & Originality Declaration
This paper delivers actionable, low-level artifact benchmarks essential for embedded systems engineers designing resource-constrained edge AI architectures.

This manuscript is original, has not been published elsewhere, and is not under consideration by another journal or conference.

Sincerely,  
**Antigravity Research Team**  
*QoS-Aware TinyML Research Platform*  
