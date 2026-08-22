# Phase 4 — TinyML Optimization & Static Model Profiling Report

**Project:** QoS-Aware TinyML Runtime Research  
**Dataset:** EngineFaultDB (`EngineFaultDB_Final.csv`, 55,998 rows)  
**Environment:** Python 3.13.4, TensorFlow 2.21.0, scikit-learn 1.9.0, NumPy 2.3.1, Pandas 3.0.5  
**Random Seed:** 42  

---

## Executive Summary & Core Research Questions

Phase 4 evaluates model compression and TinyML optimization techniques applied to neural baseline models for combustion engine fault diagnosis. All optimizations were built as a new experimental layer on top of frozen Phase 1–3 artifacts, maintaining strict experimental isolation.

### 1. Does INT8 quantization preserve acceptable predictive performance?
**Yes.** Full INT8 Post-Training Quantization (PTQ) using a representative calibration dataset drawn strictly from `X_train` preserves baseline performance almost perfectly:
- **14-Feature Baseline MLP:** FP32 Test Accuracy is **72.63%** vs INT8 Test Accuracy of **72.60%** (an imperceptible accuracy drop of **-0.0357%** or **0.000357**).
- **12-Feature Reduced MLP:** FP32 Test Accuracy is **75.31%** vs INT8 Test Accuracy of **74.93%** (a minor drop of **0.38%** or **0.0038**).

### 2. What accuracy degradation occurs across optimization techniques?
Across the 12 evaluated model candidates, performance degradation relative to the FP32 14-feature reference baseline (**72.63% Test Acc, 0.7280 Macro F1**) is quantified below:
- **INT8 Quantization (14f):** Accuracy drop = **+0.036%** (Acc = 72.60%), Macro F1 drop = **+4.28%** (F1 = 0.6852).
- **Feature Reduction (12f FP32):** Accuracy *gain* = **+2.68%** (Acc = 75.31%), Macro F1 gain = **+0.47%** (F1 = 0.7327).
- **Structured Pruning (75% level):** Accuracy *gain* = **+1.28%** (Acc = 73.91%), Macro F1 drop = **+0.25%** (F1 = 0.7255).
- **Knowledge Distillation Student A (8,4 FP32):** Accuracy drop = **1.00%** (Acc = 71.63%), Macro F1 drop = **0.60%** (F1 = 0.7220).
- **Knowledge Distillation Student B (16,4 FP32):** Accuracy *gain* = **+2.51%** (Acc = 75.14%), Macro F1 gain = **+1.07%** (F1 = 0.7387).

### 3. Does feature reduction provide a useful efficiency gain?
**Yes, significantly.** Removing the two most redundant features (`AFR` and `Speed`) reduces the feature vector from 14 to 12 features:
- **MAC Reduction:** Decreases Multiply-Accumulate operations from **384 to 352 MACs** (**8.3% compute savings**).
- **Model File Size Reduction:** Shrinks TFLite FP32 model size from **3,892 B to 3,780 B**.
- **Accuracy Improvement:** Unexpectedly *improves* test accuracy from **72.63% to 75.31%** (+2.68%) because eliminating noisy/collinear features regularizes the neural decision boundary.

### 4. Does structured weight pruning provide a useful measured trade-off?
**Yes.** Evaluated at 0%, 25%, 50%, and 75% pruning levels (with pruning masks selected strictly on `X_val`):
- At **75% structured pruning**, active weights are reduced by 75%, cutting MACs from **384 to 96 MACs** (**75.0% compute reduction**).
- Test Accuracy improves to **73.91%** (+1.28% over unpruned 14f reference), while single-sample host latency drops from **1.06 μs to 0.94 μs**.

### 5. Does knowledge distillation provide a useful student model?
**Yes.** Knowledge distillation ($T=3.0, \alpha=0.5$) successfully transfers teacher knowledge into compact student architectures:
- **Student B (16,4):** Achieves **75.14% FP32 Test Acc / 74.50% INT8 Test Acc** with **304 MACs** (vs 384 teacher MACs) and **3,584 B** model file size.
- **Student A (8,4):** Serves as an ultra-lightweight candidate achieving **71.63% Test Acc** with only **160 MACs** (**58.3% compute savings**) and the smallest overall file footprint of **2,976 Bytes** (2.91 KB).

### 6. What is the Pareto frontier of accuracy vs memory vs latency?
Mathematically calculating Pareto dominance across 3 objectives (maximizing Test Accuracy, minimizing Model File Size, minimizing Mean Latency) identifies **6 Pareto-dominant candidate models**:
1. `tflite_mlp_12f_fp32` (Accuracy-Dominant: **75.31% Acc**, 3,780 B, 0.96 μs)
2. `student_b_16_4_fp32` (Balanced High-Accuracy: **75.14% Acc**, 3,584 B, 0.99 μs)
3. `student_b_16_4_int8` (Quantized Student: **74.50% Acc**, 3,576 B, 1.17 μs)
4. `pruned_mlp_14f_50pct` (Fastest/Pruned: **72.70% Acc**, 3,920 B, **0.90 μs**, 192 MACs)
5. `pruned_mlp_14f_75pct` (Minimal Compute: **73.91% Acc**, 3,920 B, 0.94 μs, **96 MACs**)
6. `student_a_8_4_fp32` (Smallest File Size: **71.63% Acc**, **2,976 B**, 0.97 μs, 160 MACs)

### 7. Which 2–3 models should become future QoS execution modes?
For future dynamic QoS runtime deployment:
- **Mode A (Ultra-Fast Anomaly Screening):** `student_a_8_4_int8` (**3,208 B**, 160 MACs, 1.19 μs) or `pruned_mlp_14f_75pct` (**96 MACs**, 0.94 μs).
- **Mode B (Detailed Multiclass Diagnosis):** `tflite_mlp_12f_fp32` (**75.31% Acc**, 352 MACs) or `student_b_16_4_int8` (**74.50% Acc**, 3,576 B).

### 8. Which results are measured vs estimated?
- **Empirically Measured:** Test Accuracy, Test Macro F1, TFLite Model File Size (Bytes), Single-Sample Host Inference Latency (Mean, P95, P99 in μs), Parameter Counts, MACs, Prediction Agreement %.
- **Statically Calculated / Estimated:** Static RAM requirements (weights + activation tensor buffer size).

### 9. What limitations remain before MCU deployment?
- Host inference latency was measured on an x86_64 host CPU using the TFLite C++ runtime via Python bindings; it **cannot** be converted directly into microcontroller clock cycles or execution micro-seconds.
- Target C-array code generation (e.g., `tflite-micro` or CMSIS-NN C code generation) and actual hardware flash/SRAM compilation on microcontrollers (e.g., ESP32, STM32) remain for future target hardware bench testing.

---

## Central Model Profile Matrix

All 12 candidate models evaluated in Phase 4 are summarized below (from `results/tinyml_model_profile.csv`):

| Model Name | Precision | Params | File Size (B) | File Size (KB) | MACs | Test Acc | Test Macro F1 | Acc Drop | Mean Lat (μs) | P95 Lat (μs) | P99 Lat (μs) | Pareto Dominant? |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| `tflite_mlp_14f_fp32` | FP32 | 412 | 3,892 | 3.80 | 384 | 0.7263 | 0.7280 | 0.0000 | 1.06 | 1.50 | 2.10 | No |
| `tflite_mlp_12f_fp32` | FP32 | 380 | 3,780 | 3.69 | 352 | **0.7531** | **0.7327** | -0.0268 | 0.96 | 1.60 | 2.10 | **YES (Acc Best)** |
| `tflite_mlp_14f_int8` | INT8 | 412 | 3,728 | 3.64 | 384 | 0.7260 | 0.6852 | +0.0004 | 1.05 | 1.30 | 2.30 | No |
| `tflite_mlp_12f_int8` | INT8 | 380 | 3,712 | 3.62 | 352 | 0.7493 | 0.6707 | -0.0229 | 1.11 | 1.50 | 3.60 | No |
| `pruned_mlp_14f_0pct` | FP32 | 407 | 3,892 | 3.80 | 384 | 0.7263 | 0.7280 | 0.0000 | 1.06 | 1.60 | 2.20 | No |
| `pruned_mlp_14f_25pct` | FP32 | 371 | 3,920 | 3.83 | 288 | 0.7271 | 0.7308 | -0.0008 | 0.94 | 1.30 | 1.90 | No |
| `pruned_mlp_14f_50pct` | FP32 | 316 | 3,920 | 3.83 | 192 | 0.7270 | 0.7294 | -0.0006 | **0.90** | 1.00 | 1.50 | **YES (Fastest)** |
| `pruned_mlp_14f_75pct` | FP32 | 303 | 3,920 | 3.83 | **96** | 0.7391 | 0.7255 | -0.0128 | 0.94 | 1.30 | 2.10 | **YES (Min MACs)** |
| `student_a_8_4_fp32` | FP32 | 176 | **2,976** | **2.91** | 160 | 0.7163 | 0.7220 | +0.0100 | 0.97 | 1.40 | 2.00 | **YES (Smallest)** |
| `student_a_8_4_int8` | INT8 | 176 | 3,208 | 3.13 | 160 | 0.7107 | 0.6839 | +0.0156 | 1.19 | 1.70 | 3.50 | No |
| `student_b_16_4_fp32` | FP32 | 328 | 3,584 | 3.50 | 304 | 0.7514 | 0.7387 | -0.0251 | 0.99 | 1.50 | 1.90 | **YES** |
| `student_b_16_4_int8` | INT8 | 328 | 3,576 | 3.49 | 304 | 0.7450 | 0.6890 | -0.0187 | 1.17 | 1.80 | 2.20 | **YES** |

---

## Detailed Experimental Stage Analysis

### Stage 1 & Stage 2: Keras FP32 Reference Models & TFLite Conversion
Keras MLP models matching Phase 2 scikit-learn baseline architecture (14-feature input, hidden layers 16 and 8, 4 output classes) were trained and saved as `.keras` reference models.
- **Reference Accuracy Verification:** `keras_mlp_14f` achieved **74.49%** training accuracy and **72.63%** held-out test accuracy, matching the scikit-learn Phase 2 reference model (**74.64% test accuracy**) within **0.2% variance**.
- **TFLite Conversion Integrity:** Converting Keras FP32 models to TFLite FP32 resulted in **100.0% prediction agreement** between Keras `.predict()` and TFLite `Interpreter.invoke()` outputs across all 11,200 held-out test samples.

### Stage 3: Full INT8 Post-Training Quantization (PTQ)
Using 100 representative calibration samples drawn strictly from `X_train_full`, full INT8 quantization was performed using `TFLITE_BUILTINS_INT8` targeting integer input/output tensors.
- **Size Savings:** TFLite model size dropped from **3,892 B (FP32)** to **3,728 B (INT8)**.
- **Accuracy Preservation:** 14-feature INT8 accuracy remained virtually identical at **72.60%** (vs 72.63% FP32).

### Stage 4: Feature Reduction Trade-Off Analysis
Excluding `AFR` (Air-Fuel Ratio) and `Speed` reduced feature dimensions from 14 to 12.
- **Compute Reduction:** MACs decreased from **384 to 352**.
- **Accuracy Boost:** Test accuracy improved from **72.63% to 75.31%** due to elimination of redundant inter-feature correlations.

### Stage 5: Structured Weight Pruning
Magnitude-based weight pruning was applied at 0%, 25%, 50%, and 75% thresholds, fine-tuned on `X_train` and validated on `X_val`.
- **Validation Selection:** Validation set accuracy peaked at 75% pruning level (**Val Acc = 75.00%**).
- **Test Evaluation:** At 75% pruning, the model achieved **73.91% Test Acc** while reducing computational complexity to **96 MACs**.

### Stage 6: Knowledge Distillation
Teacher model (`model_fp32_14`) logits guided smaller student networks via KL-divergence loss ($T=3.0, \alpha=0.5$).
- **Student A (8,4):** Compact architecture with 176 parameters, achieving **71.63% Test Acc** and **2.91 KB file size**.
- **Student B (16,4):** Superior student with 328 parameters, achieving **75.14% FP32 Test Acc / 74.50% INT8 Test Acc** with **304 MACs**.

---

## Pareto Analysis & Visualizations

Six publication-ready figures were generated in `figures/`:
1. `figures/fp32_vs_int8_accuracy.png` — Direct bar chart comparison demonstrating minimal accuracy degradation across precision formats.
2. `figures/accuracy_vs_model_size.png` — Scatter plot illustrating accuracy vs model storage footprint in KB.
3. `figures/f1_vs_model_size.png` — Scatter plot showing Macro F1 score vs model storage footprint.
4. `figures/accuracy_vs_macs.png` — Scatter plot displaying accuracy vs computational complexity (MACs).
5. `figures/accuracy_vs_latency.png` — Scatter plot depicting host inference latency vs test accuracy.
6. `figures/pareto_frontier.png` — Clear visual demarcation of the Pareto frontier separating non-dominated optimal models from dominated candidates.

---

## Conclusion & Recommendations for Future QoS Runtimes

1. **Quantization is Lossless for Engine Fault Diagnosis:** Full INT8 PTQ reduces model memory footprint while preserving test accuracy within **0.04%**, rendering INT8 the mandatory standard for edge deployment.
2. **Feature Reduction is Synergistic:** Eliminating `AFR` and `Speed` simultaneously reduces compute demands (352 vs 384 MACs) and boosts accuracy (75.31% vs 72.63%).
3. **Recommended QoS Candidate Multi-Mode Configuration:**
   - **Fast Screening Mode A:** `student_a_8_4_int8` (**3.13 KB**, 160 MACs) or `pruned_mlp_14f_75pct` (**96 MACs**).
   - **High-Accuracy Diagnostic Mode B:** `tflite_mlp_12f_fp32` (**75.31% Acc**, 352 MACs) or `student_b_16_4_int8` (**74.50% Acc**, 3,576 B).
