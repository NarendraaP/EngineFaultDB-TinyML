# Phase 17G — Generalization and Empirical Scope Audit: Paper 4

**Manuscript:** An Independent Verification Framework for Reproducible TinyML Evaluation  
**Date:** August 28, 2026  

---

## 1. Evaluation of Generalization Claims

This audit evaluates the empirical scope of Paper 4, comparing the demonstrated evidence against claims of broad applicability across model families, modalities, and execution runtimes.

| Scope Dimension | Actual Demonstrated Evidence | Generalization Claim in Paper | Support Classification | Recommended Manuscript Action |
|---|---|---|:---:|---|
| **Model Topology** | Multi-Layer Perceptrons (MLPs) with 12 and 14 input features, hidden layers (16,8), (8,4), (16,4). | Tabular neural architectures; discussion mentions 2D CNNs, RNNs, and vision transformers. | **PARTIALLY_SUPPORTED** | Explicitly state in Limitations that the empirical case study evaluates fully connected topologies; declare convolutional and attention graph verification as future work. |
| **Model Compression** | 4 paradigms: dense baseline, post-training INT8 quantization, magnitude pruning (0%, 25%, 50%, 75%), knowledge distillation. | Comprehensive compression paradigm coverage for tabular TinyML. | **SUPPORTED** | Strong empirical coverage across all 4 standard compression techniques. |
| **Input Data Modality** | Multi-channel continuous physical telemetry (14 engine sensor channels). | Tabular cyber-physical sensor streams; discussion mentions audio and vision benchmarks. | **PARTIALLY_SUPPORTED** | Explicitly bound the empirical validation to multi-sensor tabular cyber-physical telemetry. |
| **Serialization Format** | TensorFlow Lite FlatBuffers (`.tflite`) and Keras models (`.keras`). | TFLite FlatBuffer inspection; general principles discussed for ONNX / C-arrays. | **SUPPORTED (for TFLite) / PARTIAL (others)** | Acknowledge that programmatic inspection scripts parse TFLite schema; conceptual predicates generalize to ONNX/microTVM schemas. |
| **Execution Runtime** | TFLite Interpreter (Python C-API binding on x86_64 host). | Empirical host benchmarking with explicit tiering; discussion of TFLite Micro on MCUs. | **SUPPORTED (as host verification)** | Prohibit any claim of physical bare-metal MCU timing or energy profiling; explicitly maintain Tier 1 (Host Empirical) scope. |
| **Leakage & Bias Quantification** | Threshold optimization on held-out test partition yielding $+1.80\%$ optimistic accuracy bias. | Gating threshold leakage bias in multi-stage / dynamic inference pipelines. | **SUPPORTED (as empirical demonstration)** | Present the $+1.80\%$ result strictly as a case-study quantification of threshold contamination, not a universal constant. |

---

## 2. Definitive Scope Boundary Statement

The verified empirical scope of Paper 4 is:
1. **Model Scope:** 12 candidate feedforward neural network models across dense FP32, post-training INT8 quantization, magnitude pruning ($0\%$--$75\%$), and student knowledge distillation.
2. **Data Scope:** 55,998 physical sensor records from the EngineFaultDB benchmark partitioned under strict $40/40/20$ stratified splits.
3. **Software Scope:** TensorFlow Lite FlatBuffer binary inspection, Keras weight array extraction, and Python runtime timing on x86_64 architecture.
4. **Out of Scope (Explicitly Declared as Future Work):** 2D convolutional networks, vision transformers, recurrent audio models, alternative runtimes (microTVM, ONNX Runtime Mobile, STM32Cube.AI), and bare-metal physical microcontroller hardware measurements.
