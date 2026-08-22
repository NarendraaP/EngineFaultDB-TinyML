# Reproducibility Guide: Paper 1 (QoS-Aware Multi-Fidelity Runtime)

This submission package contains the complete source code, LaTeX manuscript, figures, and reproducibility instructions for:
**"QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention"**

## 1. Dataset Source
- **Benchmark:** EngineFaultDB physical automotive combustion engine telemetry benchmark (55,998 multi-sensor records, 14 input features).
- **Split Protocol:** Stratified 40% train (22,399 rows), 40% validation (22,400 rows), 20% held-out test (11,199 rows), fixed seed seed=42.

## 2. Software Environment
- **Python:** 3.10+
- **Key Dependencies:** tensorflow>=2.10, numpy, scikit-learn, pandas, matplotlib, tectonic (for LaTeX compilation).

## 3. Key Scripts & Reproduction Workflow
To reproduce the complete 80-configuration grid sweep, active MAC profiling, and 4 ablation experiments:
```bash
python phase5/run_phase5_pipeline.py
```
Outputs are written deterministically to:
- results/phase5_policy_comparison.csv
- results/phase5_ablation_results.csv
- results/phase5_model_switch_statistics.csv

## 4. Model Artifacts
The runtime utilizes three verified Pareto-optimal models from the verified model profile (results/tinyml_model_profile_verified.csv):
- FAST: models/tinyml/distilled/student_a_8_4.tflite (2,976 B, 160 MACs)
- BALANCED: models/tinyml/pruned/mlp_14f_pruned_75.tflite (3,920 B, 96 MACs)
- HIGH_FIDELITY: models/tinyml/distilled/student_b_16_4.tflite (3,584 B, 304 MACs)

## 5. Scope & Limitations
- All latency metrics represent single-sample host measurements on an x86_64 CPU.
- Contention is simulated using synthetic multipliers; physical RTOS preemption and hardware timers on ESP32 silicon are planned future extensions.
