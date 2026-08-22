#!/usr/bin/env python3
"""
Phase 5E/5F — Trace-Driven Simulator & Synthetic Workload Generator
=====================================================================
Simulates the QoS-aware multi-fidelity runtime across EngineFaultDB
test samples with configurable workloads, deadlines, and policies.

EVIDENCE CATEGORY: (B) TRACE-DRIVEN HOST SIMULATION
All latency values are HOST EMPIRICAL — not MCU measurements.
"""

import sys, os, time, warnings
warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
import pandas as pd
from enum import Enum
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass, field

from phase5.runtime.model_registry import ModelRegistry
from phase5.runtime.model_adapter import TFLiteModelAdapter, DataPreprocessor
from phase5.runtime.qos_runtime import (
    ExecutionMode, QoSPolicy, WorkloadLevel, QoSRuntime, QoSScheduler
)

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)


# ══════════════════════════════════════════════════════════════════
# SYNTHETIC WORKLOAD GENERATOR (Phase 5F)
# ══════════════════════════════════════════════════════════════════
@dataclass
class WorkloadProfile:
    """
    Defines a synthetic host-side workload profile.
    These are experimental simulation parameters, NOT ECU measurements.
    """
    name: str
    level: WorkloadLevel
    latency_multiplier: float  # Simulates CPU contention effect on host latency
    jitter_std: float          # Latency jitter standard deviation (microseconds)
    description: str = ""


WORKLOAD_PROFILES = {
    WorkloadLevel.LOW: WorkloadProfile(
        name="LOW", level=WorkloadLevel.LOW,
        latency_multiplier=1.0, jitter_std=0.1,
        description="Minimal host CPU contention; baseline latency"
    ),
    WorkloadLevel.MEDIUM: WorkloadProfile(
        name="MEDIUM", level=WorkloadLevel.MEDIUM,
        latency_multiplier=1.5, jitter_std=0.3,
        description="Moderate host CPU contention"
    ),
    WorkloadLevel.HIGH: WorkloadProfile(
        name="HIGH", level=WorkloadLevel.HIGH,
        latency_multiplier=3.0, jitter_std=0.8,
        description="Heavy host CPU contention"
    ),
    WorkloadLevel.BURST: WorkloadProfile(
        name="BURST", level=WorkloadLevel.BURST,
        latency_multiplier=5.0, jitter_std=2.0,
        description="Burst host CPU contention with high jitter"
    ),
}


def generate_workload_sequence(n_samples: int, profile: WorkloadProfile,
                                seed: int = RANDOM_SEED) -> np.ndarray:
    """
    Generate a reproducible sequence of workload-adjusted latency multipliers.
    Returns array of per-sample latency scaling factors.
    """
    rng = np.random.RandomState(seed)
    base = np.full(n_samples, profile.latency_multiplier)
    jitter = rng.normal(0, profile.jitter_std, n_samples)
    # Ensure multiplier >= 1.0 (latency can't decrease below baseline)
    return np.maximum(base + jitter, 1.0)


# ══════════════════════════════════════════════════════════════════
# TRACE-DRIVEN SIMULATOR (Phase 5E)
# ══════════════════════════════════════════════════════════════════
@dataclass
class TraceFrame:
    """One frame of the trace-driven simulation."""
    sample_index: int
    true_label: int          # Post-hoc evaluation ONLY
    selected_model: str
    execution_mode: str
    model_switch_event: bool
    confidence: float        # Max class probability
    host_inference_latency_us: float
    configured_deadline_ms: float
    deadline_met: bool
    final_prediction: int
    final_correct: bool      # Post-hoc evaluation ONLY


class TraceSimulator:
    """
    Trace-driven QoS runtime simulator.
    
    EVIDENCE CATEGORY: (B) TRACE-DRIVEN HOST SIMULATION
    
    The scheduler NEVER accesses ground truth labels.
    Ground truth is used ONLY for post-hoc evaluation after prediction.
    """
    
    def __init__(self, runtime: QoSRuntime, policy: QoSPolicy):
        self.runtime = runtime
        self.scheduler = QoSScheduler(runtime, policy)
        self.policy = policy
        self.frames: List[TraceFrame] = []
    
    def run_trace(self, X_test: np.ndarray, y_test: np.ndarray,
                  deadline_ms: float, workload: WorkloadLevel,
                  seed: int = RANDOM_SEED) -> List[TraceFrame]:
        """
        Run trace-driven simulation on test samples.
        
        The scheduler selects models based on:
        - deadline constraint
        - workload level
        - measured host latency
        
        The scheduler does NOT access y_test (ground truth).
        y_test is used ONLY for post-hoc correctness evaluation.
        """
        profile = WORKLOAD_PROFILES[workload]
        multipliers = generate_workload_sequence(len(X_test), profile, seed)
        
        self.frames = []
        prev_mode = self.runtime.current_mode
        current_latency_us = self.runtime.mode_entries[prev_mode].mean_latency_us
        
        for i in range(len(X_test)):
            sample = X_test[i]
            
            # Step 1: Scheduler selects model (NO ground truth access)
            mode, reason = self.scheduler.select_model(
                deadline_ms=deadline_ms,
                workload=workload,
                current_latency_us=current_latency_us
            )
            
            switch_event = (mode != prev_mode)
            prev_mode = mode
            
            # Step 2: Run single-sample inference and measure host latency
            start = time.perf_counter()
            prediction = self.runtime.predict(sample)
            elapsed_us = (time.perf_counter() - start) * 1e6
            
            # Apply workload multiplier to simulate contention
            simulated_latency_us = elapsed_us * multipliers[i]
            current_latency_us = simulated_latency_us
            
            # Step 3: Get confidence (max probability)
            adapter = self.runtime.adapters[mode]
            proba = adapter.predict_proba(sample)
            confidence = float(np.max(proba))
            
            # Step 4: Check deadline compliance
            deadline_met = (simulated_latency_us / 1000.0) <= deadline_ms
            
            # Step 5: Post-hoc evaluation ONLY (ground truth never touches scheduler)
            true_label = int(y_test[i])
            correct = (prediction == true_label)
            
            model_name = self.runtime.mode_entries[mode].model
            
            frame = TraceFrame(
                sample_index=i,
                true_label=true_label,
                selected_model=model_name,
                execution_mode=mode.name,
                model_switch_event=switch_event,
                confidence=confidence,
                host_inference_latency_us=simulated_latency_us,
                configured_deadline_ms=deadline_ms,
                deadline_met=deadline_met,
                final_prediction=prediction,
                final_correct=correct
            )
            self.frames.append(frame)
        
        return self.frames
    
    def get_summary_metrics(self) -> Dict[str, Any]:
        """Compute summary metrics from the trace."""
        if not self.frames:
            return {}
        
        n = len(self.frames)
        latencies = [f.host_inference_latency_us for f in self.frames]
        correct_count = sum(1 for f in self.frames if f.final_correct)
        deadline_met_count = sum(1 for f in self.frames if f.deadline_met)
        switch_count = sum(1 for f in self.frames if f.model_switch_event)
        
        # Per-model activation frequency
        model_counts = {}
        for f in self.frames:
            model_counts[f.selected_model] = model_counts.get(f.selected_model, 0) + 1
        
        # Compute macro F1 from predictions vs true labels
        from sklearn.metrics import f1_score, recall_score
        y_true = [f.true_label for f in self.frames]
        y_pred = [f.final_prediction for f in self.frames]
        macro_f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
        
        # Anomaly false-negative rate (for non-zero fault classes)
        anomaly_mask = [f.true_label != 0 for f in self.frames]
        if any(anomaly_mask):
            anomaly_true = [f.true_label for f in self.frames if f.true_label != 0]
            anomaly_pred = [f.final_prediction for f, m in zip(self.frames, anomaly_mask) if m]
            anomaly_fn_rate = sum(1 for t, p in zip(anomaly_true, anomaly_pred) if p == 0) / len(anomaly_true)
        else:
            anomaly_fn_rate = 0.0
        
        return {
            'overall_accuracy': correct_count / n,
            'macro_f1': macro_f1,
            'anomaly_fn_rate': anomaly_fn_rate,
            'model_switch_rate': switch_count / n,
            'model_activation_frequency': model_counts,
            'avg_host_latency_us': float(np.mean(latencies)),
            'p95_host_latency_us': float(np.percentile(latencies, 95)),
            'p99_host_latency_us': float(np.percentile(latencies, 99)),
            'deadline_compliance': deadline_met_count / n,
            'total_samples': n,
            'total_switches': switch_count,
        }
    
    def to_dataframe(self) -> pd.DataFrame:
        """Export trace frames to DataFrame."""
        return pd.DataFrame([vars(f) for f in self.frames])


# ══════════════════════════════════════════════════════════════════
# ABLATION ENGINE (Phase 5J)
# ══════════════════════════════════════════════════════════════════
class AblationEngine:
    """
    Performs controlled ablation comparisons for the QoS runtime.
    
    Ablation A: Static highest-accuracy vs QoS-aware
    Ablation B: Static smallest vs QoS-aware
    Ablation C: QoS WITHOUT workload awareness vs WITH
    Ablation D: QoS WITHOUT deadline vs WITH deadline
    """
    
    def __init__(self, runtime: QoSRuntime):
        self.runtime = runtime
    
    def run_static_model(self, X_test: np.ndarray, y_test: np.ndarray,
                         mode: ExecutionMode, deadline_ms: float,
                         workload: WorkloadLevel,
                         seed: int = RANDOM_SEED) -> Dict[str, Any]:
        """Run inference with a fixed model (no switching)."""
        profile = WORKLOAD_PROFILES[workload]
        multipliers = generate_workload_sequence(len(X_test), profile, seed)
        
        self.runtime.current_mode = mode
        adapter = self.runtime.adapters[mode]
        model_name = self.runtime.mode_entries[mode].model
        
        predictions = []
        latencies = []
        
        for i in range(len(X_test)):
            start = time.perf_counter()
            pred = adapter.predict(X_test[i])
            elapsed = (time.perf_counter() - start) * 1e6
            simulated = elapsed * multipliers[i]
            predictions.append(pred)
            latencies.append(simulated)
        
        from sklearn.metrics import f1_score
        accuracy = sum(1 for p, t in zip(predictions, y_test) if p == t) / len(y_test)
        macro_f1 = f1_score(y_test, predictions, average='macro', zero_division=0)
        deadline_met = sum(1 for l in latencies if l / 1000.0 <= deadline_ms) / len(latencies)
        
        return {
            'model': model_name,
            'mode': mode.name,
            'accuracy': accuracy,
            'macro_f1': macro_f1,
            'avg_latency_us': float(np.mean(latencies)),
            'p95_latency_us': float(np.percentile(latencies, 95)),
            'deadline_compliance': deadline_met,
            'switch_count': 0,
        }
    
    def run_qos_aware(self, X_test: np.ndarray, y_test: np.ndarray,
                      deadline_ms: float, workload: WorkloadLevel,
                      policy: QoSPolicy,
                      seed: int = RANDOM_SEED) -> Dict[str, Any]:
        """Run QoS-aware model selection."""
        sim = TraceSimulator(self.runtime, policy)
        sim.run_trace(X_test, y_test, deadline_ms, workload, seed)
        metrics = sim.get_summary_metrics()
        return {
            'model': 'QoS-Aware',
            'mode': f'QoS_{policy.name}',
            'accuracy': metrics['overall_accuracy'],
            'macro_f1': metrics['macro_f1'],
            'avg_latency_us': metrics['avg_host_latency_us'],
            'p95_latency_us': metrics['p95_host_latency_us'],
            'deadline_compliance': metrics['deadline_compliance'],
            'switch_count': metrics['total_switches'],
        }
    
    def run_qos_no_workload_awareness(self, X_test: np.ndarray, y_test: np.ndarray,
                                       deadline_ms: float,
                                       policy: QoSPolicy,
                                       seed: int = RANDOM_SEED) -> Dict[str, Any]:
        """Run QoS-aware but always treat workload as LOW (no awareness)."""
        sim = TraceSimulator(self.runtime, policy)
        # Force workload to LOW in scheduler but apply actual HIGH contention
        profile = WORKLOAD_PROFILES[WorkloadLevel.HIGH]
        multipliers = generate_workload_sequence(len(X_test), profile, seed)
        
        self.runtime.current_mode = ExecutionMode.HIGH_FIDELITY
        scheduler = QoSScheduler(self.runtime, policy)
        
        predictions = []
        latencies = []
        switches = 0
        prev_mode = self.runtime.current_mode
        current_latency_us = self.runtime.mode_entries[prev_mode].mean_latency_us
        
        for i in range(len(X_test)):
            # Scheduler sees LOW workload (unaware of actual contention)
            mode, _ = scheduler.select_model(deadline_ms, WorkloadLevel.LOW, current_latency_us)
            if mode != prev_mode:
                switches += 1
                prev_mode = mode
            
            start = time.perf_counter()
            pred = self.runtime.predict(X_test[i])
            elapsed = (time.perf_counter() - start) * 1e6
            simulated = elapsed * multipliers[i]
            
            predictions.append(pred)
            latencies.append(simulated)
            current_latency_us = simulated
        
        from sklearn.metrics import f1_score
        accuracy = sum(1 for p, t in zip(predictions, y_test) if p == t) / len(y_test)
        macro_f1 = f1_score(y_test, predictions, average='macro', zero_division=0)
        deadline_met = sum(1 for l in latencies if l / 1000.0 <= deadline_ms) / len(latencies)
        
        return {
            'model': 'QoS-NoWorkloadAwareness',
            'mode': f'QoS_NoWL_{policy.name}',
            'accuracy': accuracy,
            'macro_f1': macro_f1,
            'avg_latency_us': float(np.mean(latencies)),
            'p95_latency_us': float(np.percentile(latencies, 95)),
            'deadline_compliance': deadline_met,
            'switch_count': switches,
        }
    
    def run_qos_no_deadline(self, X_test: np.ndarray, y_test: np.ndarray,
                            workload: WorkloadLevel,
                            seed: int = RANDOM_SEED) -> Dict[str, Any]:
        """Run QoS-aware but with infinite deadline (no constraint)."""
        return self.run_qos_aware(
            X_test, y_test,
            deadline_ms=1e6,  # Effectively infinite
            workload=workload,
            policy=QoSPolicy.ACCURACY_PRIORITY,
            seed=seed
        )


if __name__ == "__main__":
    print("Trace Simulator module loaded successfully.")
    print("Use run_phase5_pipeline.py to execute experiments.")
