# Reproducibility Guide: Paper 2 (TinyML Model Compression Pareto Frontier)

This submission package contains the complete source code, LaTeX manuscript, figures, and reproducibility instructions for:
**"Empirical Pareto Frontier of Model Compression for Ultra-Low-Resource TinyML"**

## 1. Dataset Source
- **Benchmark:** EngineFaultDB physical benchmark (55,998 multi-sensor records, 14 features).
- **Split Protocol:** Stratified 40/40/20 train/val/test split with seed=42.

## 2. Reproduction Workflow
To verify the metrics of all 12 serialized TFLite FlatBuffers and re-extract the empirical Pareto frontier:
```bash
python scripts/phase4_5_verification.py
```
Authoritative verified metrics are archived in:
- results/tinyml_model_profile_verified.csv

## 3. Serialized Model Artifacts
All 12 candidate FlatBuffers are archived in models/tinyml/:
- tflite_fp32/ (Uncompressed FP32 baseline)
- int8/ (Full INT8 post-training quantized models)
- pruned/ (Magnitude pruned models: 0%, 25%, 50%, 75%)
- distilled/ (Student A and Student B FP32/INT8 models)

## 4. Scope & Limitations
- Storage sizes reflect raw disk-serialized .tflite FlatBuffer binaries.
- Measured host latencies reflect x86_64 execution and do not establish MCU Worst-Case Execution Time (WCET).
