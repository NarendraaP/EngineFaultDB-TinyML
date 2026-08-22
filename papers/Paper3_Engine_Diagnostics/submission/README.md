# Reproducibility Guide: Paper 3 (Hierarchical Multi-Fidelity Diagnostics)

This submission package contains the complete source code, LaTeX manuscript, figures, and reproducibility instructions for:
**"Hierarchical Multi-Fidelity Machine Learning for Compute-Efficient Automotive Diagnostics"**

## 1. Dataset Source
- **Benchmark:** EngineFaultDB physical benchmark (55,998 records).
- **Pre-processing:** MinMaxScaler fitted strictly on training data (models/scaler.pkl).

## 2. Reproduction Workflow
To re-evaluate the screening models, threshold sweep, and hierarchical cascade:
```bash
python baseline_benchmark.py
```
Outputs are recorded in:
- results/baseline_results.csv
- results/feature_importance_dt.csv

## 3. Model Artifacts
- Mode A Screening Models: models/dt_depth3.pkl, models/dt_depth5.pkl, models/lr_baseline.pkl
- Mode B Diagnostician: models/mlp_model.h5 / models/tinyml/tflite_fp32/mlp_14f_fp32.tflite

## 4. Scope & Limitations
- EngineFaultDB was collected under steady-state dynamometer test-bench conditions.
- Compute reductions are reported in theoretical active MACs and expected mathematical cost.
