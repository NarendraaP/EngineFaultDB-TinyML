import pandas as pd
import os
from dataclasses import dataclass
from typing import List, Optional, Dict

@dataclass
class ModelEntry:
    model: str
    features: int
    precision: str
    parameters: int
    file_size_bytes: int
    file_size_kb: float
    actual_zero_weight_percentage: float
    theoretical_macs: int
    active_macs: int
    mean_latency_us: float
    median_latency_us: float
    p95_latency_us: float
    p99_latency_us: float
    min_latency_us: float
    max_latency_us: float
    test_accuracy: float
    test_macro_f1: float
    accuracy_drop: float
    macro_f1_drop: float
    input_dtype: str
    output_dtype: str
    float32_tensors: int
    int8_tensors: int
    pareto_status: str

class ModelRegistry:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path
        self.models: Dict[str, ModelEntry] = {}
        
        # Explicit mapping as requested
        self.path_mapping = {
            'mlp_14f_fp32': 'models/tinyml/tflite_fp32/mlp_14f_fp32.tflite',
            'mlp_12f_fp32': 'models/tinyml/tflite_fp32/mlp_12f_fp32.tflite',
            'mlp_14f_int8': 'models/tinyml/int8/mlp_14f_int8.tflite',
            'mlp_12f_int8': 'models/tinyml/int8/mlp_12f_int8.tflite',
            'pruned_mlp_14f_0pct': 'models/tinyml/pruned/mlp_14f_pruned_0.tflite',
            'pruned_mlp_14f_25pct': 'models/tinyml/pruned/mlp_14f_pruned_25.tflite',
            'pruned_mlp_14f_50pct': 'models/tinyml/pruned/mlp_14f_pruned_50.tflite',
            'pruned_mlp_14f_75pct': 'models/tinyml/pruned/mlp_14f_pruned_75.tflite',
            'student_a_8_4_fp32': 'models/tinyml/distilled/student_a_8_4.tflite',
            'student_a_8_4_int8': 'models/tinyml/distilled/student_a_8_4_int8.tflite',
            'student_b_16_4_fp32': 'models/tinyml/distilled/student_b_16_4.tflite',
            'student_b_16_4_int8': 'models/tinyml/distilled/student_b_16_4_int8.tflite'
        }

    def load(self):
        df = pd.read_csv(self.csv_path)
        for _, row in df.iterrows():
            entry = ModelEntry(
                model=str(row['model']),
                features=int(row['features']),
                precision=str(row['precision']),
                parameters=int(row['parameters']),
                file_size_bytes=int(row['file_size_bytes']),
                file_size_kb=float(row['file_size_kb']),
                actual_zero_weight_percentage=float(row['actual_zero_weight_percentage']),
                theoretical_macs=int(row['theoretical_macs']),
                active_macs=int(row['active_macs']),
                mean_latency_us=float(row['mean_latency_us']),
                median_latency_us=float(row['median_latency_us']),
                p95_latency_us=float(row['p95_latency_us']),
                p99_latency_us=float(row['p99_latency_us']),
                min_latency_us=float(row['min_latency_us']),
                max_latency_us=float(row['max_latency_us']),
                test_accuracy=float(row['test_accuracy']),
                test_macro_f1=float(row['test_macro_f1']),
                accuracy_drop=float(row['accuracy_drop']),
                macro_f1_drop=float(row['macro_f1_drop']),
                input_dtype=str(row['input_dtype']),
                output_dtype=str(row['output_dtype']),
                float32_tensors=int(row['float32_tensors']),
                int8_tensors=int(row['int8_tensors']),
                pareto_status=str(row['pareto_status'])
            )
            self.models[entry.model] = entry

    def get_model(self, name: str) -> Optional[ModelEntry]:
        return self.models.get(name)

    def get_pareto_models(self) -> List[ModelEntry]:
        return [m for m in self.models.values() if m.pareto_status == 'PARETO_OPTIMAL']

    def get_all_models(self) -> List[ModelEntry]:
        return list(self.models.values())

    def get_model_path(self, name: str) -> str:
        # Returns absolute path
        rel_path = self.path_mapping.get(name, "")
        if not rel_path:
            return ""
        return os.path.abspath(rel_path)

    def export_snapshot(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        data = [vars(m) for m in self.models.values()]
        df = pd.DataFrame(data)
        df.to_csv(path, index=False)
