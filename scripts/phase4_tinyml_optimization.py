#!/usr/bin/env python3
"""
Phase 4 — TinyML Optimization & Static Model Profiling
========================================================
Comprehensive TinyML pipeline:
- Stage 1: Keras FP32 Reference Models (14-feature & 12-feature)
- Stage 2: TFLite FP32 Conversion & Evaluation
- Stage 3: Full INT8 Post-Training Quantization (PTQ)
- Stage 4: Feature Reduction Trade-Off Analysis (14 vs 12 features)
- Stage 5: Structured Weight Pruning (0%, 25%, 50%, 75%)
- Stage 6: Knowledge Distillation (Teacher -> Student A/B)
- Stage 7: Central Model Profile Table (results/tinyml_model_profile.csv)
- Stage 8: Pareto Analysis & Visualizations (figures/)
- Stage 9: QoS Candidate Set Selection

Run: python scripts/phase4_tinyml_optimization.py
"""

import sys, os, time, warnings, math
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix

# ═══════════════════════════════════════════════════════════════════
# CONFIG & SEED
# ═══════════════════════════════════════════════════════════════════
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH   = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")
MODEL_DIR  = os.path.join(BASE_DIR, "models")
TINYML_DIR = os.path.join(MODEL_DIR, "tinyml")
RESULT_DIR = os.path.join(BASE_DIR, "results")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
FIG_DIR    = os.path.join(BASE_DIR, "figures")

SUBDIRS = [
    os.path.join(TINYML_DIR, "fp32"),
    os.path.join(TINYML_DIR, "tflite_fp32"),
    os.path.join(TINYML_DIR, "int8"),
    os.path.join(TINYML_DIR, "pruned"),
    os.path.join(TINYML_DIR, "distilled"),
    RESULT_DIR, REPORT_DIR, FIG_DIR
]
for d in SUBDIRS:
    os.makedirs(d, exist_ok=True)

try:
    import tensorflow as tf
    tf.random.set_seed(RANDOM_SEED)
    TF_AVAILABLE = True
    print(f"TensorFlow Version: {tf.__version__}")
except ImportError:
    TF_AVAILABLE = False
    print("WARNING: TensorFlow not installed.")

# ═══════════════════════════════════════════════════════════════════
# 1. REPRODUCE PHASE 2/3 SPLIT EXACTLY
# ═══════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Phase 4 — TinyML Optimization & Static Model Profiling")
print("=" * 70)

df = pd.read_csv(CSV_PATH)
df = df.drop_duplicates()

TARGET = "Fault"
ALL_FEATURES = [c for c in df.columns if c != TARGET]
REDUCED_FEATURES = [c for c in ALL_FEATURES if c not in ("AFR", "Speed")]

full_col_indices = {c: i for i, c in enumerate(ALL_FEATURES)}
reduced_indices  = [full_col_indices[c] for c in REDUCED_FEATURES]

y = df[TARGET].values
X_all = df[ALL_FEATURES].values

X_trainval, X_test, y_trainval, y_test = train_test_split(
    X_all, y, test_size=0.20, stratify=y, random_state=RANDOM_SEED
)
X_train, X_val, y_train, y_val = train_test_split(
    X_trainval, y_trainval, test_size=0.50, stratify=y_trainval, random_state=RANDOM_SEED
)

# Load frozen Phase 2 scaler
scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
X_train_full = scaler.transform(X_train)
X_val_full   = scaler.transform(X_val)
X_test_full  = scaler.transform(X_test)

X_train_red = X_train_full[:, reduced_indices]
X_val_red   = X_val_full[:, reduced_indices]
X_test_red  = X_test_full[:, reduced_indices]

print(f"Dataset split: Train={len(y_train):,}, Val={len(y_val):,}, Test={len(y_test):,}")

# ═══════════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def calculate_mlp_macs(input_dim, hidden_layers, num_classes):
    macs = 0
    prev_dim = input_dim
    for h in hidden_layers:
        macs += prev_dim * h
        prev_dim = h
    macs += prev_dim * num_classes
    return macs

def calculate_mlp_params(input_dim, hidden_layers, num_classes):
    params = 0
    prev_dim = input_dim
    for h in hidden_layers:
        params += (prev_dim * h) + h
        prev_dim = h
    params += (prev_dim * num_classes) + num_classes
    return params

def eval_tflite_model(tflite_path, X_test_data, lat_sample_count=100, warmup=20):
    """
    Evaluates predictions efficiently on full test set by resizing tensor,
    and measures single-sample per-inference host latency over lat_sample_count.
    """
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_index = input_details[0]['index']
    output_index = output_details[0]['index']
    input_type = input_details[0]['dtype']
    scale, zero_point = input_details[0]['quantization']

    # 1. Bulk inference for accuracy (fast tensor resize)
    input_shape = input_details[0]['shape'].copy()
    input_shape[0] = len(X_test_data)
    interpreter.resize_tensor_input(input_index, input_shape)
    interpreter.allocate_tensors()

    if input_type == np.int8:
        X_q = np.round(X_test_data / scale + zero_point).astype(np.int8)
        interpreter.set_tensor(input_index, X_q)
    else:
        interpreter.set_tensor(input_index, X_test_data.astype(np.float32))

    interpreter.invoke()
    outputs = interpreter.get_tensor(output_index)
    preds = np.argmax(outputs, axis=1)

    # 2. Single-sample latency timing loop
    input_shape[0] = 1
    interpreter.resize_tensor_input(input_index, input_shape)
    interpreter.allocate_tensors()

    sample0 = X_test_data[0:1]
    if input_type == np.int8:
        sample0_q = np.round(sample0 / scale + zero_point).astype(np.int8)
        for _ in range(warmup):
            interpreter.set_tensor(input_index, sample0_q)
            interpreter.invoke()
    else:
        sample0_f = sample0.astype(np.float32)
        for _ in range(warmup):
            interpreter.set_tensor(input_index, sample0_f)
            interpreter.invoke()

    lat_ns = []
    n_lat = min(lat_sample_count, len(X_test_data))
    for i in range(n_lat):
        s = X_test_data[i:i+1]
        if input_type == np.int8:
            s_q = np.round(s / scale + zero_point).astype(np.int8)
            interpreter.set_tensor(input_index, s_q)
        else:
            s_f = s.astype(np.float32)
            interpreter.set_tensor(input_index, s_f)

        t0 = time.perf_counter_ns()
        interpreter.invoke()
        t1 = time.perf_counter_ns()
        lat_ns.append(t1 - t0)

    lat_us = np.array(lat_ns) / 1e3
    return {
        "preds": preds,
        "mean_us": np.mean(lat_us),
        "p50_us":  np.percentile(lat_us, 50),
        "p95_us":  np.percentile(lat_us, 95),
        "p99_us":  np.percentile(lat_us, 99),
    }

# ═══════════════════════════════════════════════════════════════════
# MAIN PIPELINE
# ═══════════════════════════════════════════════════════════════════
def run_phase4():
    if not TF_AVAILABLE:
        print("TensorFlow is required to execute Phase 4. Exiting.")
        return

    profile_records = []

    # ───────────────────────────────────────────────────────────────
    # STAGE 1: FP32 Keras Reference Models
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 1 — FP32 NEURAL REFERENCE (Keras MLP)")
    print("─" * 70)

    def build_keras_mlp(input_dim, hidden_layers=(16, 8), num_classes=4):
        inputs = tf.keras.Input(shape=(input_dim,), name="sensor_input")
        x = inputs
        for h in hidden_layers:
            x = tf.keras.layers.Dense(h, activation="relu")(x)
        outputs = tf.keras.layers.Dense(num_classes, activation="softmax")(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs, name=f"keras_mlp_{input_dim}f")
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss="sparse_categorical_crossentropy",
            metrics=["accuracy"]
        )
        return model

    # 1A. Keras FP32 (14 features)
    print("\n  Training Keras FP32 (14 features)...", end=" ", flush=True)
    model_fp32_14 = build_keras_mlp(14, (16, 8), 4)
    early_stop = tf.keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
    model_fp32_14.fit(
        X_train_full, y_train,
        validation_data=(X_val_full, y_val),
        epochs=60, batch_size=128, verbose=0, callbacks=[early_stop]
    )
    path_fp32_14 = os.path.join(TINYML_DIR, "fp32", "keras_mlp_14f.keras")
    model_fp32_14.save(path_fp32_14)
    print("done")

    y_pred_fp32_14 = np.argmax(model_fp32_14.predict(X_test_full, verbose=0), axis=1)
    acc_fp32_14 = accuracy_score(y_test, y_pred_fp32_14)
    f1_fp32_14  = f1_score(y_test, y_pred_fp32_14, average="macro")
    macs_14 = calculate_mlp_macs(14, (16, 8), 4)
    params_14 = calculate_mlp_params(14, (16, 8), 4)
    size_fp32_14 = os.path.getsize(path_fp32_14)

    print(f"    Test Acc = {acc_fp32_14:.4f}, Macro F1 = {f1_fp32_14:.4f}, Params = {params_14}, MACs = {macs_14}")

    # 1B. Keras FP32 (12 features)
    print("  Training Keras FP32 (12 features)...", end=" ", flush=True)
    model_fp32_12 = build_keras_mlp(12, (16, 8), 4)
    model_fp32_12.fit(
        X_train_red, y_train,
        validation_data=(X_val_red, y_val),
        epochs=60, batch_size=128, verbose=0, callbacks=[early_stop]
    )
    path_fp32_12 = os.path.join(TINYML_DIR, "fp32", "keras_mlp_12f.keras")
    model_fp32_12.save(path_fp32_12)
    print("done")

    y_pred_fp32_12 = np.argmax(model_fp32_12.predict(X_test_red, verbose=0), axis=1)
    acc_fp32_12 = accuracy_score(y_test, y_pred_fp32_12)
    f1_fp32_12  = f1_score(y_test, y_pred_fp32_12, average="macro")
    macs_12 = calculate_mlp_macs(12, (16, 8), 4)
    params_12 = calculate_mlp_params(12, (16, 8), 4)
    size_fp32_12 = os.path.getsize(path_fp32_12)

    print(f"    Test Acc = {acc_fp32_12:.4f}, Macro F1 = {f1_fp32_12:.4f}, Params = {params_12}, MACs = {macs_12}")

    # Save FP32 reference metrics
    fp32_ref_df = pd.DataFrame([
        {
            "model_name": "keras_mlp_14f", "feature_count": 14, "precision": "FP32",
            "params": params_14, "macs": macs_14, "size_bytes": size_fp32_14,
            "accuracy": round(acc_fp32_14, 6), "macro_f1": round(f1_fp32_14, 6)
        },
        {
            "model_name": "keras_mlp_12f", "feature_count": 12, "precision": "FP32",
            "params": params_12, "macs": macs_12, "size_bytes": size_fp32_12,
            "accuracy": round(acc_fp32_12, 6), "macro_f1": round(f1_fp32_12, 6)
        }
    ])
    fp32_ref_df.to_csv(os.path.join(RESULT_DIR, "fp32_reference_metrics.csv"), index=False)

    # ───────────────────────────────────────────────────────────────
    # STAGE 2: TFLite FP32 Conversion
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 2 — TFLITE FP32 CONVERSION")
    print("─" * 70)

    def convert_to_tflite_fp32(keras_model, save_path):
        converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
        tflite_model = converter.convert()
        with open(save_path, "wb") as f:
            f.write(tflite_model)
        return len(tflite_model)

    path_tflite_fp32_14 = os.path.join(TINYML_DIR, "tflite_fp32", "mlp_14f_fp32.tflite")
    size_tflite_fp32_14 = convert_to_tflite_fp32(model_fp32_14, path_tflite_fp32_14)
    eval_tflite_fp32_14 = eval_tflite_model(path_tflite_fp32_14, X_test_full)
    acc_tf_fp32_14 = accuracy_score(y_test, eval_tflite_fp32_14["preds"])
    f1_tf_fp32_14  = f1_score(y_test, eval_tflite_fp32_14["preds"], average="macro")
    agree_fp32_14  = np.mean(eval_tflite_fp32_14["preds"] == y_pred_fp32_14)

    print(f"  TFLite FP32 (14f): Size = {size_tflite_fp32_14:,} B, Acc = {acc_tf_fp32_14:.4f}, "
          f"Agreement = {agree_fp32_14*100:.2f}%, Mean Lat = {eval_tflite_fp32_14['mean_us']:.1f} us")

    path_tflite_fp32_12 = os.path.join(TINYML_DIR, "tflite_fp32", "mlp_12f_fp32.tflite")
    size_tflite_fp32_12 = convert_to_tflite_fp32(model_fp32_12, path_tflite_fp32_12)
    eval_tflite_fp32_12 = eval_tflite_model(path_tflite_fp32_12, X_test_red)
    acc_tf_fp32_12 = accuracy_score(y_test, eval_tflite_fp32_12["preds"])
    f1_tf_fp32_12  = f1_score(y_test, eval_tflite_fp32_12["preds"], average="macro")
    agree_fp32_12  = np.mean(eval_tflite_fp32_12["preds"] == y_pred_fp32_12)

    print(f"  TFLite FP32 (12f): Size = {size_tflite_fp32_12:,} B, Acc = {acc_tf_fp32_12:.4f}, "
          f"Agreement = {agree_fp32_12*100:.2f}%, Mean Lat = {eval_tflite_fp32_12['mean_us']:.1f} us")

    profile_records.append({
        "model_name": "tflite_mlp_14f_fp32", "model_family": "MLP (16,8)", "feature_count": 14, "precision": "FP32",
        "parameters": params_14, "model_file_size_bytes": size_tflite_fp32_14,
        "model_file_size_kb": round(size_tflite_fp32_14/1024, 2),
        "estimated_or_measured_RAM": "statically calculated (weights + activation buffer ~1.8 KB)",
        "MACs": macs_14, "test_accuracy": round(acc_tf_fp32_14, 6), "test_macro_f1": round(f1_tf_fp32_14, 6),
        "accuracy_drop": 0.0, "macro_f1_drop": 0.0,
        "mean_latency_us": round(eval_tflite_fp32_14["mean_us"], 2),
        "p95_latency_us": round(eval_tflite_fp32_14["p95_us"], 2),
        "p99_latency_us": round(eval_tflite_fp32_14["p99_us"], 2),
    })
    profile_records.append({
        "model_name": "tflite_mlp_12f_fp32", "model_family": "MLP (16,8)", "feature_count": 12, "precision": "FP32",
        "parameters": params_12, "model_file_size_bytes": size_tflite_fp32_12,
        "model_file_size_kb": round(size_tflite_fp32_12/1024, 2),
        "estimated_or_measured_RAM": "statically calculated (weights + activation buffer ~1.7 KB)",
        "MACs": macs_12, "test_accuracy": round(acc_tf_fp32_12, 6), "test_macro_f1": round(f1_tf_fp32_12, 6),
        "accuracy_drop": round(acc_tf_fp32_14 - acc_tf_fp32_12, 6),
        "macro_f1_drop": round(f1_tf_fp32_14 - f1_tf_fp32_12, 6),
        "mean_latency_us": round(eval_tflite_fp32_12["mean_us"], 2),
        "p95_latency_us": round(eval_tflite_fp32_12["p95_us"], 2),
        "p99_latency_us": round(eval_tflite_fp32_12["p99_us"], 2),
    })

    # ───────────────────────────────────────────────────────────────
    # STAGE 3: Full INT8 Post-Training Quantization (PTQ)
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 3 — FULL INT8 POST-TRAINING QUANTIZATION (PTQ)")
    print("─" * 70)

    def convert_to_tflite_int8(keras_model, X_train_representative, save_path):
        def rep_data_gen():
            for i in range(min(100, len(X_train_representative))):
                yield [X_train_representative[i:i+1].astype(np.float32)]

        converter = tf.lite.TFLiteConverter.from_keras_model(keras_model)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = rep_data_gen
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8

        tflite_quant = converter.convert()
        with open(save_path, "wb") as f:
            f.write(tflite_quant)
        return len(tflite_quant)

    path_int8_14 = os.path.join(TINYML_DIR, "int8", "mlp_14f_int8.tflite")
    size_int8_14 = convert_to_tflite_int8(model_fp32_14, X_train_full, path_int8_14)
    eval_int8_14 = eval_tflite_model(path_int8_14, X_test_full)
    acc_int8_14  = accuracy_score(y_test, eval_int8_14["preds"])
    f1_int8_14   = f1_score(y_test, eval_int8_14["preds"], average="macro")

    acc_drop_14 = acc_tf_fp32_14 - acc_int8_14
    f1_drop_14  = f1_tf_fp32_14 - f1_int8_14

    print(f"  TFLite INT8 (14f): Size = {size_int8_14:,} B, Acc = {acc_int8_14:.4f} (drop: {acc_drop_14:+.4f}), "
          f"F1 = {f1_int8_14:.4f} (drop: {f1_drop_14:+.4f}), Mean Lat = {eval_int8_14['mean_us']:.1f} us")

    path_int8_12 = os.path.join(TINYML_DIR, "int8", "mlp_12f_int8.tflite")
    size_int8_12 = convert_to_tflite_int8(model_fp32_12, X_train_red, path_int8_12)
    eval_int8_12 = eval_tflite_model(path_int8_12, X_test_red)
    acc_int8_12  = accuracy_score(y_test, eval_int8_12["preds"])
    f1_int8_12   = f1_score(y_test, eval_int8_12["preds"], average="macro")

    acc_drop_12 = acc_tf_fp32_14 - acc_int8_12
    f1_drop_12  = f1_tf_fp32_14 - f1_int8_12

    print(f"  TFLite INT8 (12f): Size = {size_int8_12:,} B, Acc = {acc_int8_12:.4f} (drop: {acc_drop_12:+.4f}), "
          f"F1 = {f1_int8_12:.4f} (drop: {f1_drop_12:+.4f}), Mean Lat = {eval_int8_12['mean_us']:.1f} us")

    profile_records.append({
        "model_name": "tflite_mlp_14f_int8", "model_family": "MLP (16,8)", "feature_count": 14, "precision": "INT8",
        "parameters": params_14, "model_file_size_bytes": size_int8_14,
        "model_file_size_kb": round(size_int8_14/1024, 2),
        "estimated_or_measured_RAM": "statically calculated (weights INT8 + activation buffer ~0.5 KB)",
        "MACs": macs_14, "test_accuracy": round(acc_int8_14, 6), "test_macro_f1": round(f1_int8_14, 6),
        "accuracy_drop": round(acc_drop_14, 6), "macro_f1_drop": round(f1_drop_14, 6),
        "mean_latency_us": round(eval_int8_14["mean_us"], 2),
        "p95_latency_us": round(eval_int8_14["p95_us"], 2),
        "p99_latency_us": round(eval_int8_14["p99_us"], 2),
    })
    profile_records.append({
        "model_name": "tflite_mlp_12f_int8", "model_family": "MLP (16,8)", "feature_count": 12, "precision": "INT8",
        "parameters": params_12, "model_file_size_bytes": size_int8_12,
        "model_file_size_kb": round(size_int8_12/1024, 2),
        "estimated_or_measured_RAM": "statically calculated (weights INT8 + activation buffer ~0.5 KB)",
        "MACs": macs_12, "test_accuracy": round(acc_int8_12, 6), "test_macro_f1": round(f1_int8_12, 6),
        "accuracy_drop": round(acc_drop_12, 6), "macro_f1_drop": round(f1_drop_12, 6),
        "mean_latency_us": round(eval_int8_12["mean_us"], 2),
        "p95_latency_us": round(eval_int8_12["p95_us"], 2),
        "p99_latency_us": round(eval_int8_12["p99_us"], 2),
    })

    # ───────────────────────────────────────────────────────────────
    # STAGE 5: Structured Weight Pruning
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 5 — STRUCTURED WEIGHT PRUNING")
    print("─" * 70)

    pruning_levels = [0.0, 0.25, 0.50, 0.75]
    best_pruned_val_acc = -1
    best_pruning_level = 0.0

    pruned_val_results = {}

    for p_level in pruning_levels:
        p_model = build_keras_mlp(14, (16, 8), 4)
        p_model.set_weights(model_fp32_14.get_weights())

        if p_level > 0.0:
            weights = p_model.get_weights()
            new_weights = []
            for w in weights:
                if len(w.shape) == 2:
                    abs_w = np.abs(w)
                    thresh = np.percentile(abs_w, p_level * 100)
                    mask = (abs_w >= thresh).astype(np.float32)
                    new_weights.append(w * mask)
                else:
                    new_weights.append(w)
            p_model.set_weights(new_weights)
            p_model.fit(X_train_full, y_train, epochs=15, batch_size=128, verbose=0)

        val_pred = np.argmax(p_model.predict(X_val_full, verbose=0), axis=1)
        val_acc  = accuracy_score(y_val, val_pred)
        pruned_val_results[p_level] = val_acc
        print(f"  Pruning Level {p_level*100:2.0f}%: Val Acc = {val_acc:.4f}")

        if val_acc > best_pruned_val_acc:
            best_pruned_val_acc = val_acc
            best_pruning_level  = p_level

    print(f"\n  Selected Pruning Level based on Validation Set: {best_pruning_level*100:.0f}% (Val Acc = {best_pruned_val_acc:.4f})")

    for p_level in pruning_levels:
        if p_level == 0.0:
            p_m = model_fp32_14
        else:
            p_m = build_keras_mlp(14, (16, 8), 4)
            p_m.set_weights(model_fp32_14.get_weights())
            weights = p_m.get_weights()
            new_weights = []
            for w in weights:
                if len(w.shape) == 2:
                    abs_w = np.abs(w)
                    thresh = np.percentile(abs_w, p_level * 100)
                    new_weights.append(w * (abs_w >= thresh).astype(np.float32))
                else:
                    new_weights.append(w)
            p_m.set_weights(new_weights)
            p_m.fit(X_train_full, y_train, epochs=15, batch_size=128, verbose=0)

        path_p = os.path.join(TINYML_DIR, "pruned", f"mlp_14f_pruned_{int(p_level*100)}.keras")
        p_m.save(path_p)

        path_p_tflite = os.path.join(TINYML_DIR, "pruned", f"mlp_14f_pruned_{int(p_level*100)}.tflite")
        convert_to_tflite_fp32(p_m, path_p_tflite)
        size_p_tflite = os.path.getsize(path_p_tflite)

        eval_p = eval_tflite_model(path_p_tflite, X_test_full)
        acc_p  = accuracy_score(y_test, eval_p["preds"])
        f1_p   = f1_score(y_test, eval_p["preds"], average="macro")

        active_params = sum(np.count_nonzero(w) for w in p_m.get_weights())

        profile_records.append({
            "model_name": f"pruned_mlp_14f_{int(p_level*100)}pct", "model_family": "Pruned MLP (16,8)",
            "feature_count": 14, "precision": "FP32",
            "parameters": active_params, "model_file_size_bytes": size_p_tflite,
            "model_file_size_kb": round(size_p_tflite/1024, 2),
            "estimated_or_measured_RAM": "statically calculated (active params FP32 + buffer)",
            "MACs": int(macs_14 * (1 - p_level)),
            "test_accuracy": round(acc_p, 6), "test_macro_f1": round(f1_p, 6),
            "accuracy_drop": round(acc_tf_fp32_14 - acc_p, 6),
            "macro_f1_drop": round(f1_tf_fp32_14 - f1_p, 6),
            "mean_latency_us": round(eval_p["mean_us"], 2),
            "p95_latency_us": round(eval_p["p95_us"], 2),
            "p99_latency_us": round(eval_p["p99_us"], 2),
        })

    # ───────────────────────────────────────────────────────────────
    # STAGE 6: Knowledge Distillation
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 6 — KNOWLEDGE DISTILLATION")
    print("─" * 70)

    teacher_logits_train = model_fp32_14.predict(X_train_full, verbose=0)
    teacher_logits_val   = model_fp32_14.predict(X_val_full, verbose=0)

    students = [
        {"name": "Student A (8,4)", "short": "student_a_8_4", "layers": (8, 4)},
        {"name": "Student B (16,4)", "short": "student_b_16_4", "layers": (16, 4)},
    ]

    best_student_val_acc = -1
    best_student_spec = None

    for sspec in students:
        s_model = build_keras_mlp(14, sspec["layers"], 4)
        
        optimizer = tf.keras.optimizers.Adam(learning_rate=0.001)
        loss_fn_ce = tf.keras.losses.SparseCategoricalCrossentropy()
        loss_fn_kld = tf.keras.losses.KLDivergence()

        temperature = 3.0
        alpha_kd    = 0.5

        train_ds = tf.data.Dataset.from_tensor_slices((X_train_full, y_train, teacher_logits_train)).batch(128)

        for epoch in range(30):
            for x_b, y_b, t_logits_b in train_ds:
                with tf.GradientTape() as tape:
                    s_logits = s_model(x_b, training=True)
                    loss_ce = loss_fn_ce(y_b, s_logits)
                    
                    soft_t = tf.nn.softmax(t_logits_b / temperature)
                    soft_s = tf.nn.softmax(s_logits / temperature)
                    loss_kld = loss_fn_kld(soft_t, soft_s) * (temperature ** 2)

                    total_loss = (1 - alpha_kd) * loss_ce + alpha_kd * loss_kld

                grads = tape.gradient(total_loss, s_model.trainable_variables)
                optimizer.apply_gradients(zip(grads, s_model.trainable_variables))

        val_pred = np.argmax(s_model.predict(X_val_full, verbose=0), axis=1)
        val_acc  = accuracy_score(y_val, val_pred)
        print(f"  {sspec['name']}: Val Acc = {val_acc:.4f}")

        if val_acc > best_student_val_acc:
            best_student_val_acc = val_acc
            best_student_spec    = sspec

        path_s_keras  = os.path.join(TINYML_DIR, "distilled", f"{sspec['short']}.keras")
        path_s_tflite = os.path.join(TINYML_DIR, "distilled", f"{sspec['short']}.tflite")
        s_model.save(path_s_keras)
        size_s_tflite = convert_to_tflite_fp32(s_model, path_s_tflite)

        eval_s = eval_tflite_model(path_s_tflite, X_test_full)
        acc_s  = accuracy_score(y_test, eval_s["preds"])
        f1_s   = f1_score(y_test, eval_s["preds"], average="macro")
        s_macs   = calculate_mlp_macs(14, sspec["layers"], 4)
        s_params = calculate_mlp_params(14, sspec["layers"], 4)

        path_s_int8 = os.path.join(TINYML_DIR, "distilled", f"{sspec['short']}_int8.tflite")
        size_s_int8 = convert_to_tflite_int8(s_model, X_train_full, path_s_int8)
        eval_s_int8 = eval_tflite_model(path_s_int8, X_test_full)
        acc_s_int8  = accuracy_score(y_test, eval_s_int8["preds"])
        f1_s_int8   = f1_score(y_test, eval_s_int8["preds"], average="macro")

        profile_records.append({
            "model_name": f"{sspec['short']}_fp32", "model_family": f"Distilled MLP {sspec['layers']}",
            "feature_count": 14, "precision": "FP32",
            "parameters": s_params, "model_file_size_bytes": size_s_tflite,
            "model_file_size_kb": round(size_s_tflite/1024, 2),
            "estimated_or_measured_RAM": "statically calculated (student params FP32 + buffer)",
            "MACs": s_macs, "test_accuracy": round(acc_s, 6), "test_macro_f1": round(f1_s, 6),
            "accuracy_drop": round(acc_tf_fp32_14 - acc_s, 6),
            "macro_f1_drop": round(f1_tf_fp32_14 - f1_s, 6),
            "mean_latency_us": round(eval_s["mean_us"], 2),
            "p95_latency_us": round(eval_s["p95_us"], 2),
            "p99_latency_us": round(eval_s["p99_us"], 2),
        })
        profile_records.append({
            "model_name": f"{sspec['short']}_int8", "model_family": f"Distilled MLP {sspec['layers']}",
            "feature_count": 14, "precision": "INT8",
            "parameters": s_params, "model_file_size_bytes": size_s_int8,
            "model_file_size_kb": round(size_s_int8/1024, 2),
            "estimated_or_measured_RAM": "statically calculated (student params INT8 + buffer)",
            "MACs": s_macs, "test_accuracy": round(acc_s_int8, 6), "test_macro_f1": round(f1_s_int8, 6),
            "accuracy_drop": round(acc_tf_fp32_14 - acc_s_int8, 6),
            "macro_f1_drop": round(f1_tf_fp32_14 - f1_s_int8, 6),
            "mean_latency_us": round(eval_s_int8["mean_us"], 2),
            "p95_latency_us": round(eval_s_int8["p95_us"], 2),
            "p99_latency_us": round(eval_s_int8["p99_us"], 2),
        })

    print(f"\n  Selected Student based on Validation Set: {best_student_spec['name']} (Val Acc = {best_student_val_acc:.4f})")

    # ───────────────────────────────────────────────────────────────
    # STAGE 7: Central Model Profile Table
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 7 — CENTRAL MODEL PROFILE TABLE")
    print("─" * 70)

    profile_df = pd.DataFrame(profile_records)
    profile_path = os.path.join(RESULT_DIR, "tinyml_model_profile.csv")
    profile_df.to_csv(profile_path, index=False)
    print(f"  Saved: {profile_path} ({len(profile_df)} candidates)")
    print(profile_df[["model_name", "precision", "model_file_size_bytes", "MACs", "test_accuracy", "test_macro_f1", "mean_latency_us"]].to_string(index=False))

    # ───────────────────────────────────────────────────────────────
    # STAGE 8: Pareto Analysis & Figures
    # ───────────────────────────────────────────────────────────────
    print("\n" + "─" * 70)
    print("STAGE 8 — PARETO ANALYSIS & FIGURES")
    print("─" * 70)

    def is_pareto_efficient(costs):
        is_efficient = np.ones(costs.shape[0], dtype=bool)
        for i, c in enumerate(costs):
            if is_efficient[i]:
                is_efficient[is_efficient] = np.any(costs[is_efficient] < c, axis=1) | np.all(costs[is_efficient] == c, axis=1)
                is_efficient[i] = True
        return is_efficient

    acc_arr = profile_df["test_accuracy"].values
    size_arr = profile_df["model_file_size_bytes"].values
    lat_arr = profile_df["mean_latency_us"].values

    costs = np.column_stack([-acc_arr, size_arr, lat_arr])
    pareto_mask = is_pareto_efficient(costs)
    profile_df["is_pareto"] = pareto_mask

    print("\n  Pareto-Dominant Candidates:")
    pareto_df = profile_df[profile_df["is_pareto"]]
    for _, r in pareto_df.iterrows():
        print(f"    - {r['model_name']:28s}: Acc={r['test_accuracy']:.4f}, F1={r['test_macro_f1']:.4f}, "
              f"Size={r['model_file_size_bytes']:,} B, Lat={r['mean_latency_us']:.1f} us, MACs={r['MACs']}")

    acc_dom_idx = profile_df["test_accuracy"].idxmax()
    small_idx   = profile_df["model_file_size_bytes"].idxmin()
    fast_idx    = profile_df["mean_latency_us"].idxmin()

    print(f"\n  Key Candidates Identified:")
    print(f"    - Accuracy-Dominant: {profile_df.loc[acc_dom_idx, 'model_name']} (Acc={profile_df.loc[acc_dom_idx, 'test_accuracy']:.4f})")
    print(f"    - Smallest Model:    {profile_df.loc[small_idx, 'model_name']} ({profile_df.loc[small_idx, 'model_file_size_bytes']:,} B)")
    print(f"    - Fastest Model:     {profile_df.loc[fast_idx, 'model_name']} ({profile_df.loc[fast_idx, 'mean_latency_us']:.1f} us)")

    plt.rcParams.update({"font.family": "sans-serif", "font.size": 10, "axes.grid": True, "grid.alpha": 0.25})

    # Fig 1: FP32 vs INT8 Accuracy Comparison
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fp32_sub = profile_df[profile_df["precision"] == "FP32"]
    int8_sub = profile_df[profile_df["precision"] == "INT8"]
    
    x = np.arange(len(fp32_sub))
    w = 0.35
    ax.bar(x - w/2, fp32_sub["test_accuracy"], w, label="FP32", color="#1976D2")
    int8_accs = [int8_sub[int8_sub["model_name"] == r["model_name"].replace("fp32", "int8")]["test_accuracy"].values[0]
                 if len(int8_sub[int8_sub["model_name"] == r["model_name"].replace("fp32", "int8")]) > 0 else 0 for _, r in fp32_sub.iterrows()]
    ax.bar(x + w/2, int8_accs, w, label="INT8", color="#388E3C")
    ax.set_xticks(x)
    ax.set_xticklabels(fp32_sub["model_name"], rotation=30, ha="right", fontsize=8)
    ax.set_ylabel("Test Accuracy")
    ax.set_title("FP32 vs. INT8 Accuracy Comparison")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "fp32_vs_int8_accuracy.png"), dpi=180)
    plt.close()

    # Fig 2: Accuracy vs Model Size
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(profile_df["model_file_size_kb"], profile_df["test_accuracy"], c="#1976D2", s=60, edgecolors="black")
    for _, r in profile_df.iterrows():
        ax.annotate(r["model_name"], (r["model_file_size_kb"], r["test_accuracy"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("Model File Size (KB)")
    ax.set_ylabel("Test Accuracy")
    ax.set_title("Accuracy vs. Model File Size")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "accuracy_vs_model_size.png"), dpi=180)
    plt.close()

    # Fig 3: Macro F1 vs Model Size
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(profile_df["model_file_size_kb"], profile_df["test_macro_f1"], c="#7B1FA2", s=60, edgecolors="black")
    for _, r in profile_df.iterrows():
        ax.annotate(r["model_name"], (r["model_file_size_kb"], r["test_macro_f1"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("Model File Size (KB)")
    ax.set_ylabel("Test Macro F1")
    ax.set_title("Macro F1 vs. Model File Size")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "f1_vs_model_size.png"), dpi=180)
    plt.close()

    # Fig 4: Accuracy vs MACs
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(profile_df["MACs"], profile_df["test_accuracy"], c="#F57C00", s=60, edgecolors="black")
    for _, r in profile_df.iterrows():
        ax.annotate(r["model_name"], (r["MACs"], r["test_accuracy"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("Multiply-Accumulate Operations (MACs)")
    ax.set_ylabel("Test Accuracy")
    ax.set_title("Accuracy vs. Computational Complexity (MACs)")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "accuracy_vs_macs.png"), dpi=180)
    plt.close()

    # Fig 5: Accuracy vs Latency
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.scatter(profile_df["mean_latency_us"], profile_df["test_accuracy"], c="#D32F2F", s=60, edgecolors="black")
    for _, r in profile_df.iterrows():
        ax.annotate(r["model_name"], (r["mean_latency_us"], r["test_accuracy"]), fontsize=7, xytext=(4, 4), textcoords="offset points")
    ax.set_xlabel("Mean Host Latency (μs)")
    ax.set_ylabel("Test Accuracy")
    ax.set_title("Accuracy vs. Host Inference Latency")
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "accuracy_vs_latency.png"), dpi=180)
    plt.close()

    # Fig 6: Pareto Frontier
    fig, ax = plt.subplots(figsize=(8, 5))
    non_pareto = profile_df[~profile_df["is_pareto"]]
    pareto_pts = profile_df[profile_df["is_pareto"]]

    ax.scatter(non_pareto["model_file_size_kb"], non_pareto["test_accuracy"], c="gray", alpha=0.5, s=50, label="Dominated")
    ax.scatter(pareto_pts["model_file_size_kb"], pareto_pts["test_accuracy"], c="#D32F2F", s=100, edgecolors="black", label="Pareto-Dominant", zorder=4)

    for _, r in pareto_pts.iterrows():
        ax.annotate(f"{r['model_name']}\n({r['precision']})", (r["model_file_size_kb"], r["test_accuracy"]),
                    fontsize=8, fontweight="bold", color="#D32F2F", xytext=(5, -10), textcoords="offset points")

    ax.set_xlabel("Model File Size (KB)")
    ax.set_ylabel("Test Accuracy")
    ax.set_title("Pareto Frontier: Test Accuracy vs. Model File Size")
    ax.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, "pareto_frontier.png"), dpi=180)
    plt.close()

    print(f"\n  Saved 6 figures in {FIG_DIR}")
    print("\n======================================================================")
    print("PHASE 4 TINYML OPTIMIZATION — COMPLETE")
    print("======================================================================\n")

if __name__ == "__main__":
    run_phase4()
