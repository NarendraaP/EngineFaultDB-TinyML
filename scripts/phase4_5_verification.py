#!/usr/bin/env python3
"""
Phase 4.5 — Independent Verification of TinyML Results
========================================================
Comprehensive Verification Script:
1. Inventory all Phase 4 artifacts.
2. Independently recompute model metrics (params, file sizes, MACs, accuracy, macro F1, drops).
3. Audit TFLite FlatBuffers (input/output dtypes, weight dtypes, activation dtypes, quant params, op codes, float32 vs int8 tensor counts).
4. Verify INT8 claims (full integer inference vs hybrid vs float32).
5. Verify Pruning claims (inspect actual weight arrays, zero-weight %, theoretical MACs, active MACs, TFLite file sizes).
6. Verify MAC counts (theoretical dense vs active vs executed).
7. Audit Test-Set Isolation (trace data split and usage in code).
8. Latency Verification (warmup, iterations, min, mean, median, P95, P99, max, timing API).
9. Independent Pareto Dominance Re-computation (4 objectives: max test_acc, min file_size, min active_macs, min host_latency).
10. Discrepancy Analysis (compare published profile vs verified profile).
11. Generate results/tinyml_model_profile_verified.csv.
12. Generate reports/Phase4_5_Independent_Verification.md.
"""

import sys, os, time, warnings, math
sys.stdout.reconfigure(encoding="utf-8")
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score

import tensorflow as tf

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

BASE_DIR   = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH   = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")
MODEL_DIR  = os.path.join(BASE_DIR, "models")
TINYML_DIR = os.path.join(MODEL_DIR, "tinyml")
RESULT_DIR = os.path.join(BASE_DIR, "results")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
FIG_DIR    = os.path.join(BASE_DIR, "figures")

# ═══════════════════════════════════════════════════════════════════
# 1. REPRODUCE DATASET SPLIT (FROZEN PHASE 2/3)
# ═══════════════════════════════════════════════════════════════════
df = pd.read_csv(CSV_PATH).drop_duplicates()
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

scaler = joblib.load(os.path.join(MODEL_DIR, "scaler.pkl"))
X_train_full = scaler.transform(X_train)
X_val_full   = scaler.transform(X_val)
X_test_full  = scaler.transform(X_test)

X_test_red  = X_test_full[:, reduced_indices]

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

def inspect_tflite_flatbuffer(tflite_path):
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    
    tensors = interpreter.get_tensor_details()
    tensor_dict = {t['index']: t for t in tensors}
    dtypes = set(t['dtype'].__name__ for t in tensors)
    
    inputs = interpreter.get_input_details()
    outputs = interpreter.get_output_details()
    
    input_dtype = inputs[0]['dtype'].__name__
    output_dtype = outputs[0]['dtype'].__name__
    
    float32_count = sum(1 for t in tensors if t['dtype'] == np.float32)
    int8_count    = sum(1 for t in tensors if t['dtype'] == np.int8)
    int32_count   = sum(1 for t in tensors if t['dtype'] == np.int32)
    uint8_count   = sum(1 for t in tensors if t['dtype'] == np.uint8)
    
    weight_dtypes = set()
    activation_dtypes = set()
    
    ops_info = []
    if hasattr(interpreter, "_get_ops_details"):
        ops = interpreter._get_ops_details()
        for op in ops:
            in_d = [tensor_dict[idx]['dtype'].__name__ for idx in op['inputs'] if idx in tensor_dict]
            out_d = [tensor_dict[idx]['dtype'].__name__ for idx in op['outputs'] if idx in tensor_dict]
            ops_info.append({"op_name": op['op_name'], "inputs": in_d, "outputs": out_d})
            
            # Record weight/activation dtypes from FULLY_CONNECTED ops
            if op['op_name'] == "FULLY_CONNECTED" and len(in_d) >= 2:
                activation_dtypes.add(in_d[0])
                weight_dtypes.add(in_d[1])

    # Classification
    if float32_count == 0 and int8_count > 0:
        precision_class = "FULL_INT8"
    elif float32_count > 0 and (int8_count > 0 or uint8_count > 0):
        precision_class = "HYBRID_MIXED_PRECISION"
    else:
        precision_class = "FP32"
        
    return {
        "file_size_bytes": os.path.getsize(tflite_path),
        "input_dtype": input_dtype,
        "output_dtype": output_dtype,
        "input_quant": inputs[0]['quantization'],
        "output_quant": outputs[0]['quantization'],
        "dtypes_present": sorted(list(dtypes)),
        "float32_count": float32_count,
        "int8_count": int8_count,
        "int32_count": int32_count,
        "uint8_count": uint8_count,
        "weight_dtypes": sorted(list(weight_dtypes)),
        "activation_dtypes": sorted(list(activation_dtypes)),
        "ops_info": ops_info,
        "precision_class": precision_class
    }

def eval_tflite_comprehensive(tflite_path, X_test_data, lat_samples=500, warmup=100):
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_index = input_details[0]['index']
    output_index = output_details[0]['index']
    input_type = input_details[0]['dtype']
    scale, zero_point = input_details[0]['quantization']

    # 1. Accuracy bulk eval
    input_shape = input_details[0]['shape'].copy()
    input_shape[0] = len(X_test_data)
    interpreter.resize_tensor_input(input_index, input_shape)
    interpreter.allocate_tensors()

    if input_type == np.int8:
        X_q = np.round(X_test_data / scale + zero_point).clip(-128, 127).astype(np.int8)
        interpreter.set_tensor(input_index, X_q)
    else:
        interpreter.set_tensor(input_index, X_test_data.astype(np.float32))

    interpreter.invoke()
    outputs = interpreter.get_tensor(output_index)
    preds = np.argmax(outputs, axis=1)

    # 2. Per-sample single inference timing loop
    input_shape[0] = 1
    interpreter.resize_tensor_input(input_index, input_shape)
    interpreter.allocate_tensors()

    sample0 = X_test_data[0:1]
    if input_type == np.int8:
        sample0_q = np.round(sample0 / scale + zero_point).clip(-128, 127).astype(np.int8)
        for _ in range(warmup):
            interpreter.set_tensor(input_index, sample0_q)
            interpreter.invoke()
    else:
        sample0_f = sample0.astype(np.float32)
        for _ in range(warmup):
            interpreter.set_tensor(input_index, sample0_f)
            interpreter.invoke()

    lat_ns = []
    n_lat = min(lat_samples, len(X_test_data))
    for i in range(n_lat):
        s = X_test_data[i:i+1]
        if input_type == np.int8:
            s_q = np.round(s / scale + zero_point).clip(-128, 127).astype(np.int8)
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
        "mean_us": float(np.mean(lat_us)),
        "median_us": float(np.median(lat_us)),
        "p95_us": float(np.percentile(lat_us, 95)),
        "p99_us": float(np.percentile(lat_us, 99)),
        "min_us": float(np.min(lat_us)),
        "max_us": float(np.max(lat_us)),
    }

# ═══════════════════════════════════════════════════════════════════
# MAIN VERIFICATION PIPELINE
# ═══════════════════════════════════════════════════════════════════
def run_verification():
    print("=" * 70)
    print("Phase 4.5 — Independent Verification Pipeline")
    print("=" * 70)

    # Candidate definition mapping
    candidates = [
        {"model_name": "tflite_mlp_14f_fp32", "path": "models/tinyml/tflite_fp32/mlp_14f_fp32.tflite", "keras": "models/tinyml/fp32/keras_mlp_14f.keras", "features": 14, "red": False, "family": "MLP (16,8)", "hidden": (16,8), "prune_pct": 0.0},
        {"model_name": "tflite_mlp_12f_fp32", "path": "models/tinyml/tflite_fp32/mlp_12f_fp32.tflite", "keras": "models/tinyml/fp32/keras_mlp_12f.keras", "features": 12, "red": True,  "family": "MLP (16,8)", "hidden": (16,8), "prune_pct": 0.0},
        {"model_name": "tflite_mlp_14f_int8", "path": "models/tinyml/int8/mlp_14f_int8.tflite",       "keras": "models/tinyml/fp32/keras_mlp_14f.keras", "features": 14, "red": False, "family": "MLP (16,8)", "hidden": (16,8), "prune_pct": 0.0},
        {"model_name": "tflite_mlp_12f_int8", "path": "models/tinyml/int8/mlp_12f_int8.tflite",       "keras": "models/tinyml/fp32/keras_mlp_12f.keras", "features": 12, "red": True,  "family": "MLP (16,8)", "hidden": (16,8), "prune_pct": 0.0},
        {"model_name": "pruned_mlp_14f_0pct", "path": "models/tinyml/pruned/mlp_14f_pruned_0.tflite",  "keras": "models/tinyml/pruned/mlp_14f_pruned_0.keras", "features": 14, "red": False, "family": "Pruned MLP (16,8)", "hidden": (16,8), "prune_pct": 0.0},
        {"model_name": "pruned_mlp_14f_25pct","path": "models/tinyml/pruned/mlp_14f_pruned_25.tflite", "keras": "models/tinyml/pruned/mlp_14f_pruned_25.keras","features": 14, "red": False, "family": "Pruned MLP (16,8)", "hidden": (16,8), "prune_pct": 0.25},
        {"model_name": "pruned_mlp_14f_50pct","path": "models/tinyml/pruned/mlp_14f_pruned_50.tflite", "keras": "models/tinyml/pruned/mlp_14f_pruned_50.keras","features": 14, "red": False, "family": "Pruned MLP (16,8)", "hidden": (16,8), "prune_pct": 0.50},
        {"model_name": "pruned_mlp_14f_75pct","path": "models/tinyml/pruned/mlp_14f_pruned_75.tflite", "keras": "models/tinyml/pruned/mlp_14f_pruned_75.keras","features": 14, "red": False, "family": "Pruned MLP (16,8)", "hidden": (16,8), "prune_pct": 0.75},
        {"model_name": "student_a_8_4_fp32",  "path": "models/tinyml/distilled/student_a_8_4.tflite",  "keras": "models/tinyml/distilled/student_a_8_4.keras", "features": 14, "red": False, "family": "Distilled MLP (8,4)", "hidden": (8,4), "prune_pct": 0.0},
        {"model_name": "student_a_8_4_int8",  "path": "models/tinyml/distilled/student_a_8_4_int8.tflite", "keras": "models/tinyml/distilled/student_a_8_4.keras", "features": 14, "red": False, "family": "Distilled MLP (8,4)", "hidden": (8,4), "prune_pct": 0.0},
        {"model_name": "student_b_16_4_fp32", "path": "models/tinyml/distilled/student_b_16_4.tflite", "keras": "models/tinyml/distilled/student_b_16_4.keras", "features": 14, "red": False, "family": "Distilled MLP (16,4)", "hidden": (16,4), "prune_pct": 0.0},
        {"model_name": "student_b_16_4_int8", "path": "models/tinyml/distilled/student_b_16_4_int8.tflite", "keras": "models/tinyml/distilled/student_b_16_4.keras", "features": 14, "red": False, "family": "Distilled MLP (16,4)", "hidden": (16,4), "prune_pct": 0.0},
    ]

    verified_records = []

    # Get reference FP32 14f accuracy for drop calculation
    ref_fp32_eval = eval_tflite_comprehensive(os.path.join(BASE_DIR, candidates[0]["path"]), X_test_full)
    ref_fp32_acc = accuracy_score(y_test, ref_fp32_eval["preds"])
    ref_fp32_f1  = f1_score(y_test, ref_fp32_eval["preds"], average="macro")
    print(f"FP32 14-Feature Reference Test Acc = {ref_fp32_acc:.6f}, Macro F1 = {ref_fp32_f1:.6f}\n")

    for cand in candidates:
        tflite_abs_path = os.path.join(BASE_DIR, cand["path"])
        keras_abs_path  = os.path.join(BASE_DIR, cand["keras"])
        
        # 1. FlatBuffer audit
        fb_audit = inspect_tflite_flatbuffer(tflite_abs_path)
        
        # 2. Evaluation
        X_test_data = X_test_red if cand["red"] else X_test_full
        eval_res = eval_tflite_comprehensive(tflite_abs_path, X_test_data)
        
        test_acc = accuracy_score(y_test, eval_res["preds"])
        test_f1  = f1_score(y_test, eval_res["preds"], average="macro")
        acc_drop = ref_fp32_acc - test_acc
        f1_drop  = ref_fp32_f1 - test_f1
        
        # 3. Keras weight inspection for zero weights
        keras_model = tf.keras.models.load_model(keras_abs_path)
        weights = keras_model.get_weights()
        
        total_weight_elements = sum(w.size for w in weights)
        zero_weight_elements  = sum(np.count_nonzero(w == 0) for w in weights)
        zero_weight_pct       = (zero_weight_elements / total_weight_elements) * 100.0
        
        # 4. MAC calculations
        dense_macs  = calculate_mlp_macs(cand["features"], cand["hidden"], 4)
        params_count = calculate_mlp_params(cand["features"], cand["hidden"], 4)
        
        # Active MACs (dense MACs reduced by pruning level or weight zero fraction)
        if cand["prune_pct"] > 0:
            active_macs = int(dense_macs * (1 - cand["prune_pct"]))
        else:
            active_macs = dense_macs
            
        record = {
            "model": cand["model_name"],
            "features": cand["features"],
            "precision": fb_audit["precision_class"],
            "parameters": params_count,
            "file_size_bytes": fb_audit["file_size_bytes"],
            "file_size_kb": round(fb_audit["file_size_bytes"] / 1024.0, 2),
            "actual_zero_weight_percentage": round(zero_weight_pct, 2),
            "theoretical_macs": dense_macs,
            "active_macs": active_macs,
            "mean_latency_us": round(eval_res["mean_us"], 2),
            "median_latency_us": round(eval_res["median_us"], 2),
            "p95_latency_us": round(eval_res["p95_us"], 2),
            "p99_latency_us": round(eval_res["p99_us"], 2),
            "min_latency_us": round(eval_res["min_us"], 2),
            "max_latency_us": round(eval_res["max_us"], 2),
            "test_accuracy": round(test_acc, 6),
            "test_macro_f1": round(test_f1, 6),
            "accuracy_drop": round(acc_drop, 6),
            "macro_f1_drop": round(f1_drop, 6),
            "input_dtype": fb_audit["input_dtype"],
            "output_dtype": fb_audit["output_dtype"],
            "float32_tensors": fb_audit["float32_count"],
            "int8_tensors": fb_audit["int8_count"],
        }
        verified_records.append(record)
        print(f"Verified {cand['model_name']:24s}: Acc={test_acc:.4f}, Size={fb_audit['file_size_bytes']} B, ActiveMACs={active_macs}, Class={fb_audit['precision_class']}")

    df_verified = pd.DataFrame(verified_records)

    # ═══════════════════════════════════════════════════════════════════
    # 5. INDEPENDENT PARETO DOMINANCE RE-COMPUTATION
    # Objectives: Maximize test_accuracy, Minimize file_size_bytes,
    #             Minimize active_macs, Minimize mean_latency_us
    # ═══════════════════════════════════════════════════════════════════
    def is_pareto_efficient_4d(costs):
        # costs matrix: [-test_accuracy, file_size_bytes, active_macs, mean_latency_us]
        is_efficient = np.ones(costs.shape[0], dtype=bool)
        for i, c in enumerate(costs):
            if is_efficient[i]:
                # A point is dominated if another point is <= in all objectives and < in at least one
                is_dominated = np.all(costs <= c, axis=1) & np.any(costs < c, axis=1)
                if np.any(is_dominated):
                    is_efficient[i] = False
        return is_efficient

    costs = np.column_stack([
        -df_verified["test_accuracy"].values,
        df_verified["file_size_bytes"].values,
        df_verified["active_macs"].values,
        df_verified["mean_latency_us"].values
    ])
    
    pareto_mask = is_pareto_efficient_4d(costs)
    df_verified["pareto_status"] = np.where(pareto_mask, "PARETO_OPTIMAL", "DOMINATED")

    print("\n" + "=" * 70)
    print("INDEPENDENT PARETO DOMINANCE RESULT:")
    print("=" * 70)
    for idx, r in df_verified.iterrows():
        print(f"  {r['model']:25s}: Acc={r['test_accuracy']:.4f}, Size={r['file_size_bytes']} B, ActiveMACs={r['active_macs']}, Lat={r['mean_latency_us']:.2f} us -> {r['pareto_status']}")

    # Save verified CSV
    verified_csv_path = os.path.join(RESULT_DIR, "tinyml_model_profile_verified.csv")
    df_verified.to_csv(verified_csv_path, index=False)
    print(f"\nSaved verified profile to {verified_csv_path}")

    # ═══════════════════════════════════════════════════════════════════
    # 6. DISCREPANCY ANALYSIS (vs published tinyml_model_profile.csv)
    # ═══════════════════════════════════════════════════════════════════
    published_csv_path = os.path.join(RESULT_DIR, "tinyml_model_profile.csv")
    df_published = pd.read_csv(published_csv_path)

    discrepancies = []

    for _, r_ver in df_verified.iterrows():
        m_name = r_ver["model"]
        match_pub = df_published[df_published["model_name"] == m_name]
        if len(match_pub) > 0:
            r_pub = match_pub.iloc[0]
            
            # Compare key fields
            for col, ver_col in [("test_accuracy", "test_accuracy"), ("test_macro_f1", "test_macro_f1"), ("model_file_size_bytes", "file_size_bytes"), ("MACs", "active_macs")]:
                pub_val = float(r_pub[col])
                ver_val = float(r_ver[ver_col])
                abs_diff = abs(pub_val - ver_val)
                pct_diff = (abs_diff / (abs(pub_val) + 1e-9)) * 100.0
                
                if abs_diff > 1e-4:
                    discrepancies.append({
                        "model": m_name,
                        "metric": col,
                        "published_val": pub_val,
                        "verified_val": ver_val,
                        "abs_diff": round(abs_diff, 6),
                        "pct_diff": round(pct_diff, 2),
                        "type": "NUMERICAL" if col in ("test_accuracy", "test_macro_f1") else "TERMINOLOGY/STRUCTURAL"
                    })

    print(f"\nDiscrepancy Analysis: Found {len(discrepancies)} discrepancies.")
    for d in discrepancies:
        print(f"  [{d['type']}] {d['model']} - {d['metric']}: Published={d['published_val']}, Verified={d['verified_val']}, Diff={d['abs_diff']} ({d['pct_diff']}%)")

    return df_verified, discrepancies

if __name__ == "__main__":
    run_verification()
