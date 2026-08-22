from enum import Enum, auto
from typing import Dict, Any, Tuple, List
import os
from .model_registry import ModelRegistry
from .model_adapter import TFLiteModelAdapter

class ExecutionMode(Enum):
    FAST = auto()
    BALANCED = auto()
    HIGH_FIDELITY = auto()

class QoSPolicy(Enum):
    ACCURACY_PRIORITY = auto()
    BALANCED = auto()
    DEADLINE_PRIORITY = auto()
    COMPUTE_PRIORITY = auto()

class WorkloadLevel(Enum):
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    BURST = auto()

class QoSRuntime:
    def __init__(self, registry: ModelRegistry, base_dir: str = '.'):
        self.registry = registry
        self.base_dir = base_dir
        self.adapters = {}
        self.mode_entries = {}
        self._current_mode = ExecutionMode.HIGH_FIDELITY
        self._setup_modes()

    def _setup_modes(self):
        # Specific verified models mapping
        mode_mapping = {
            ExecutionMode.FAST: 'student_a_8_4_fp32',
            ExecutionMode.BALANCED: 'pruned_mlp_14f_75pct',
            ExecutionMode.HIGH_FIDELITY: 'student_b_16_4_fp32'
        }

        for mode, model_name in mode_mapping.items():
            entry = self.registry.get_model(model_name)
            if entry is None:
                raise ValueError(f"Model {model_name} not found in registry")
            
            path = self.registry.get_model_path(model_name)
            adapter = TFLiteModelAdapter()
            adapter.load(os.path.join(self.base_dir, path))
            
            self.adapters[mode] = adapter
            self.mode_entries[mode] = entry

    @property
    def current_mode(self) -> ExecutionMode:
        return self._current_mode
        
    @current_mode.setter
    def current_mode(self, mode: ExecutionMode):
        self._current_mode = mode

    def predict(self, sample) -> int:
        adapter = self.adapters[self._current_mode]
        return adapter.predict(sample)

    def get_mode_info(self) -> Dict[str, Any]:
        entry = self.mode_entries[self._current_mode]
        return {
            'model_name': entry.model,
            'test_accuracy': entry.test_accuracy,
            'test_macro_f1': entry.test_macro_f1,
            'file_size_bytes': entry.file_size_bytes,
            'active_macs': entry.active_macs,
            'measured_host_latency_us': entry.mean_latency_us
        }

class QoSScheduler:
    def __init__(self, runtime: QoSRuntime, policy: QoSPolicy):
        self.runtime = runtime
        self.policy = policy
        self.switch_count = 0
        self.switch_log = []

    def select_model(self, deadline_ms: float, workload: WorkloadLevel, current_latency_us: float) -> Tuple[ExecutionMode, str]:
        deadline_us = deadline_ms * 1000.0
        
        workload_multiplier = {
            WorkloadLevel.LOW: 1.0,
            WorkloadLevel.MEDIUM: 1.5,
            WorkloadLevel.HIGH: 3.0,
            WorkloadLevel.BURST: 5.0
        }[workload]

        fast_latency = self.runtime.mode_entries[ExecutionMode.FAST].mean_latency_us * workload_multiplier
        bal_latency = self.runtime.mode_entries[ExecutionMode.BALANCED].mean_latency_us * workload_multiplier
        hf_latency = self.runtime.mode_entries[ExecutionMode.HIGH_FIDELITY].mean_latency_us * workload_multiplier

        selected_mode = ExecutionMode.HIGH_FIDELITY
        reason = "Default to high fidelity"

        if self.policy == QoSPolicy.ACCURACY_PRIORITY:
            if hf_latency <= deadline_us:
                selected_mode = ExecutionMode.HIGH_FIDELITY
                reason = "Accuracy Priority: HF fits deadline"
            elif bal_latency <= deadline_us:
                selected_mode = ExecutionMode.BALANCED
                reason = "Accuracy Priority: Downgrade to Balanced to meet deadline"
            else:
                selected_mode = ExecutionMode.FAST
                reason = "Accuracy Priority: Downgrade to Fast to meet deadline"

        elif self.policy == QoSPolicy.BALANCED:
            if workload in (WorkloadLevel.BURST, WorkloadLevel.HIGH):
                if bal_latency <= deadline_us:
                    selected_mode = ExecutionMode.BALANCED
                    reason = "Balanced: Heavy workload, use Balanced"
                else:
                    selected_mode = ExecutionMode.FAST
                    reason = "Balanced: Heavy workload and tight deadline, use Fast"
            else:
                if hf_latency <= deadline_us:
                    selected_mode = ExecutionMode.HIGH_FIDELITY
                    reason = "Balanced: Low workload, use HF"
                elif bal_latency <= deadline_us:
                    selected_mode = ExecutionMode.BALANCED
                    reason = "Balanced: Use Balanced to meet deadline"
                else:
                    selected_mode = ExecutionMode.FAST
                    reason = "Balanced: Downgrade to Fast to meet deadline"

        elif self.policy == QoSPolicy.DEADLINE_PRIORITY:
            if workload == WorkloadLevel.BURST or fast_latency > deadline_us * 0.5:
                selected_mode = ExecutionMode.FAST
                reason = "Deadline Priority: Aggressive fast mode for safety"
            elif bal_latency <= deadline_us * 0.8:
                selected_mode = ExecutionMode.BALANCED
                reason = "Deadline Priority: Balanced mode has enough headroom"
            else:
                selected_mode = ExecutionMode.FAST
                reason = "Deadline Priority: Fast mode needed"

        elif self.policy == QoSPolicy.COMPUTE_PRIORITY:
            selected_mode = ExecutionMode.BALANCED
            reason = "Compute Priority: Balanced (96 MACs) preferred for compute efficiency"
            if workload == WorkloadLevel.BURST or bal_latency > deadline_us:
                selected_mode = ExecutionMode.FAST
                reason = "Compute Priority: Forced to Fast due to burst/deadline"

        if selected_mode != self.runtime.current_mode:
            self.switch_count += 1
            self.switch_log.append(f"Switch from {self.runtime.current_mode.name} to {selected_mode.name} (Reason: {reason})")
            self.runtime.current_mode = selected_mode

        return selected_mode, reason

    def get_switch_count(self) -> int:
        return self.switch_count

    def get_switch_log(self) -> List[str]:
        return self.switch_log
