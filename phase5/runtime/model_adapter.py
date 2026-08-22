import abc
import time
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
from sklearn.model_selection import train_test_split
from typing import Tuple, Dict, Any

class ModelAdapter(abc.ABC):
    @abc.abstractmethod
    def load(self, model_path: str):
        pass

    @abc.abstractmethod
    def predict(self, sample: np.ndarray) -> int:
        pass

    @abc.abstractmethod
    def predict_proba(self, sample: np.ndarray) -> np.ndarray:
        pass

    @abc.abstractmethod
    def metadata(self) -> Dict[str, Any]:
        pass

    @abc.abstractmethod
    def latency_measurement(self, sample: np.ndarray, n_iterations: int = 1000) -> Dict[str, float]:
        pass


class TFLiteModelAdapter(ModelAdapter):
    def __init__(self):
        self.interpreter = None
        self.input_details = None
        self.output_details = None
        self.is_int8 = False
        self.input_scale = 0.0
        self.input_zero_point = 0
        self.output_scale = 0.0
        self.output_zero_point = 0
        self.model_path = ""

    def load(self, model_path: str):
        self.model_path = model_path
        self.interpreter = tf.lite.Interpreter(model_path=model_path)
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        input_dtype = self.input_details[0]['dtype']
        if input_dtype == np.int8:
            self.is_int8 = True
            if 'quantization' in self.input_details[0] and self.input_details[0]['quantization'][0] > 0:
                self.input_scale, self.input_zero_point = self.input_details[0]['quantization']
                self.output_scale, self.output_zero_point = self.output_details[0]['quantization']
            else:
                # Fallback if quantization params missing but dtype is int8
                self.input_scale, self.input_zero_point = 1.0, 0
                self.output_scale, self.output_zero_point = 1.0, 0

    def predict_proba(self, sample: np.ndarray) -> np.ndarray:
        # Single-sample inference only
        sample = sample.reshape(1, -1)
        
        if self.is_int8:
            # Quantize
            sample_q = np.round(sample / self.input_scale + self.input_zero_point)
            sample_q = np.clip(sample_q, -128, 127).astype(np.int8)
            self.interpreter.set_tensor(self.input_details[0]['index'], sample_q)
        else:
            sample_f = sample.astype(np.float32)
            self.interpreter.set_tensor(self.input_details[0]['index'], sample_f)

        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])

        if self.is_int8:
            # Dequantize
            output_data = (output_data.astype(np.float32) - self.output_zero_point) * self.output_scale
            
        return output_data

    def predict(self, sample: np.ndarray) -> int:
        proba = self.predict_proba(sample)
        return int(np.argmax(proba, axis=1)[0])

    def metadata(self) -> Dict[str, Any]:
        return {
            'is_int8': self.is_int8,
            'model_path': self.model_path
        }

    def latency_measurement(self, sample: np.ndarray, n_iterations: int = 1000) -> Dict[str, float]:
        latencies = []
        
        # Warm up 100 iterations
        for _ in range(100):
            self.predict(sample)

        # Measure
        for _ in range(n_iterations):
            start = time.perf_counter()
            self.predict(sample)
            end = time.perf_counter()
            latencies.append((end - start) * 1e6)

        return {
            'mean': float(np.mean(latencies)),
            'median': float(np.median(latencies)),
            'p95': float(np.percentile(latencies, 95)),
            'p99': float(np.percentile(latencies, 99)),
            'min': float(np.min(latencies)),
            'max': float(np.max(latencies))
        }


class DataPreprocessor:
    def __init__(self, data_path: str = 'EngineFaultDB_Final.csv', scaler_path: str = 'models/scaler.pkl'):
        self.data_path = data_path
        self.scaler_path = scaler_path
        self.scaler = joblib.load(self.scaler_path)

    def get_test_samples(self) -> Tuple[np.ndarray, np.ndarray]:
        df = pd.read_csv(self.data_path)
        feature_cols = [c for c in df.columns if c != 'Fault']
        X = df[feature_cols].values
        y = df['Fault'].values
        
        # Split 40/40/20 to extract the 20% test set with seed 42
        X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=0.20, random_state=42, stratify=y)
        
        # Scale
        X_test_scaled = self.scaler.transform(X_test)
        
        return X_test_scaled, y_test

    def preprocess_single(self, raw_features: np.ndarray) -> np.ndarray:
        return self.scaler.transform(raw_features.reshape(1, -1))[0]
