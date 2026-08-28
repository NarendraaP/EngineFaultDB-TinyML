# Reproducibility Guide: Paper 2 (TinyML Model Compression Pareto Characterization)

This submission package contains the complete source code, LaTeX manuscript, figures, and reproducibility instructions for:
**"Empirical Pareto Characterization of Model Compression Paradigms for Ultra-Low-Resource TinyML"**

## 1. Dataset Source
- **Benchmark:** EngineFaultDB physical benchmark (55,998 multi-sensor records, 14 features).
- **Split Protocol:** Stratified 40/40/20 train/val/test split with seed=42.

## 2. Reproduction Workflow
To verify the metrics of all 12 serialized TFLite FlatBuffers and re-extract the empirical 3-objective deployment-resource Pareto frontier:
```bash
python scripts/phase4_5_verification.py
```
Authoritative verified metrics are archived in:
- `results/tinyml_model_profile_verified.csv`

## 3. Serialized Model Artifacts
All 12 candidate FlatBuffers are archived in `models/tinyml/`:
- `tflite_fp32/` (Uncompressed FP32 baseline)
- `int8/` (Full INT8 post-training quantized models)
- `pruned/` (Unstructured magnitude-pruned models: 0%, 25%, 50%, 75%)
- `distilled/` (Student A and Student B FP32/INT8 models)

## 4. Scope & Primary Framework
- Primary Pareto optimization is evaluated over Test Accuracy (maximize), Serialized Binary Size (minimize), and Theoretical Active MACs (minimize).
- Measured host latencies reflect x86_64 single-sample execution and are reported as a secondary reference benchmark; they do not establish MCU Worst-Case Execution Time (WCET).
