# Paper 1 Evidence Map & Experimental Traceability

**Paper Title:** *QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention*  
**Paper Directory:** [`papers/Paper1_QoS_Runtime/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/)  
**Primary Evidence Sources:** [`results/phase5_policy_comparison.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_policy_comparison.csv), [`results/phase5_ablation_results.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_ablation_results.csv), [`results/phase5_model_switch_statistics.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_model_switch_statistics.csv), [`results/phase5_runtime_traces.csv`](file:///d:/WiDe/EngineFaultDB-main/results/phase5_runtime_traces.csv), [`phase5/runtime/qos_runtime.py`](file:///d:/WiDe/EngineFaultDB-main/phase5/runtime/qos_runtime.py)  
**Date:** August 20, 2026  

---

## 1. Experimental Traceability Matrix

Every claim, mathematical parameter, policy result, and ablation outcome in Paper 1 is mapped to its underlying source artifact:

| Manuscript Component | Specific Claim / Metric Value | Authoritative Source Artifact | Source Location / Column | Evidence Classification |
| :--- | :--- | :--- | :--- | :--- |
| **Model Registry (FAST)** | `student_a_8_4_fp32`: $160$ MACs, $2,976$\,B, Acc = $0.716339$, F1 = $0.722001$. | `tinyml_model_profile_verified.csv` | Row 10 | **DIRECTLY VERIFIED** |
| **Model Registry (BALANCED)** | `pruned_mlp_14f_75pct`: $96$ MACs, $3,920$\,B, Acc = $0.748214$, F1 = $0.756251$. | `tinyml_model_profile_verified.csv` | Row 9 | **DIRECTLY VERIFIED** |
| **Model Registry (HIGH\_FIDELITY)** | `student_b_16_4_fp32`: $304$ MACs, $3,584$\,B, Acc = $0.751429$, F1 = $0.738717$. | `tinyml_model_profile_verified.csv` | Row 12 | **DIRECTLY VERIFIED** |
| **Workload Multipliers** | `LOW` ($1.0\times$), `MEDIUM` ($1.5\times$), `HIGH` ($3.0\times$), `BURST` ($5.0\times$). | `phase5/simulator/trace_simulator.py` | Lines 25–38 | **SIMULATION PARAMETER** |
| **Deadlines Evaluated** | $D \in \{5, 10, 20, 50, 100\}\text{ ms}$. | `phase5/run_phase5_pipeline.py` | Line 42 | **SIMULATION PARAMETER** |
| **Experimental Matrix** | $5 \text{ deadlines} \times 4 \text{ workloads} \times 4 \text{ policies} = 80 \text{ configurations}$. | `results/phase5_policy_comparison.csv` | Full CSV (80 rows) | **TRACE-DRIVEN SIMULATION** |
| **Test Stream Size** | $11,200$ test frames evaluated per trace; $40,000$ recorded frames in detailed trace file. | `results/phase5_runtime_traces.csv` | File size $4.65$\,MB | **TRACE-DRIVEN SIMULATION** |
| **ACCURACY\_PRIORITY Result** | Stays in `HIGH_FIDELITY` across all workloads; Acc = $0.751875$, F1 = $0.739048$, Switches = 0. | `results/phase5_policy_comparison.csv` | Rows 2, 6, 10, 14 | **TRACE-DRIVEN SIMULATION** |
| **BALANCED Policy (Low/Med)** | Operates in `HIGH_FIDELITY` ($304$ MACs); Acc = $0.751875$, F1 = $0.739048$. | `results/phase5_policy_comparison.csv` | Rows 3, 7 | **TRACE-DRIVEN SIMULATION** |
| **BALANCED Policy (High/Burst)**| Switches to `BALANCED` ($96$ MACs); Acc = $0.748214$, F1 = $0.756251$, Switches = 1. | `results/phase5_policy_comparison.csv` | Rows 11, 15 | **TRACE-DRIVEN SIMULATION** |
| **68.4% Compute Reduction Claim**| $(304 - 96) / 304 = 68.421\% \approx 68.4\%$ reduction in theoretical active MACs per inference. | Derived from verified MACs | Equation (4) in Paper 1 | **DERIVED** |
| **DEADLINE\_PRIORITY (Burst)** | Switches to `FAST` ($160$ MACs); Acc = $0.716071$, F1 = $0.721781$, Switches = 1. | `results/phase5_policy_comparison.csv` | Row 16 | **TRACE-DRIVEN SIMULATION** |
| **COMPUTE\_PRIORITY Policy** | Always prefers `BALANCED` ($96$ MACs); degrades to `FAST` under `BURST`. | `results/phase5_policy_comparison.csv` | Rows 5, 9, 13, 17 | **TRACE-DRIVEN SIMULATION** |
| **Ablation A (Static Best vs QoS)**| Static HF ($0.7519$ Acc, $0.7390$ F1) vs QoS Balanced ($0.7482$ Acc, $0.7563$ F1, $-68.4\%$ MACs). | `results/phase5_ablation_results.csv` | Rows 2, 3 | **TRACE-DRIVEN SIMULATION** |
| **Ablation B (Static Small vs QoS)**| Static Fast ($0.7161$ Acc, $0.7218$ F1) vs QoS Balanced ($0.7482$ Acc, $0.7563$ F1, $+3.21\%$ Acc). | `results/phase5_ablation_results.csv` | Rows 4, 5 | **TRACE-DRIVEN SIMULATION** |
| **Ablation C (Workload Awareness)**| No WL Awareness ($0.7519$ Acc, $0$ switches) vs With WL Awareness ($0.7482$ Acc, $1$ switch). | `results/phase5_ablation_results.csv` | Rows 6, 7 | **TRACE-DRIVEN SIMULATION** |
| **Ablation D (Deadline Gating)**| No Deadline ($0.7519$ Acc) vs With Deadline ($0.7482$ Acc, controlled host execution). | `results/phase5_ablation_results.csv` | Rows 8, 9 | **TRACE-DRIVEN SIMULATION** |
| **Runtime Non-Leakage** | `QoSScheduler.select_model()` accepts strictly `(deadline, workload, latency)`, zero label $y$ access. | `phase5/runtime/qos_runtime.py` | Lines 83–153 | **DIRECTLY VERIFIED** |
| **Hardware Physical Execution**| Physical on-chip execution on genuine ESP32 silicon. | `phase5/hardware/esp32_interface.md` | Status header | **FUTURE WORK (Pending ESP32)** |

---

## 2. Evidence Tier Classification

- **Tier 1 (Host Empirical Measurements):** Single-sample latency profiling, FlatBuffer sizes, and verified parameter/MAC counts of the 12 candidate models on x86_64 host.
- **Tier 2 (Trace-Driven Runtime Simulation):** 80 experimental configurations and 4 controlled ablation studies evaluated over 11,200 held-out test frames under synthetic workload contention.
- **Tier 3 (Physical MCU Measurements):** On-device hardware timers, SRAM tensor arena allocation, and FreeRTOS task preemption. (*Classified strictly as FUTURE WORK*).
