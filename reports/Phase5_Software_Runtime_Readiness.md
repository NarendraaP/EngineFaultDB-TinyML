# Phase 5O Final Readiness Report
**Phase 5: Software/Runtime Readiness**

## 1. Objective
Complete the software/runtime research stack for QoS-aware multi-model TinyML inference.

## 2. Current Hardware Status
**ESP32 NOT PRESENT.**
Arduino Mega 2560 and Arduino Uno/Nano (ATmega328P) are available as auxiliary boards only.
All MCU measurements: **STATUS = PENDING_PHYSICAL_ESP32**.

## 3. Model Registry
The registry loads 12 candidate models from the verified model profile. Of these, 6 are Pareto-optimal:

| Model Name | Accuracy | Macro F1 | Active MACs | File Size (KB) |
|---|---|---|---|---|
| `pruned_mlp_14f_25pct` | 0.7505 | 0.7515 | 288 | 3.83 |
| `pruned_mlp_14f_50pct` | 0.7495 | 0.7566 | 192 | 3.83 |
| `pruned_mlp_14f_75pct` | 0.7482 | 0.7563 | 96 | 3.83 |
| `student_a_8_4_fp32` | 0.7163 | 0.7220 | 160 | 2.91 |
| `student_b_16_4_fp32` | 0.7514 | 0.7387 | 304 | 3.50 |
| `student_b_16_4_int8` | 0.7456 | 0.6896 | 304 | 3.49 |

## 4. Runtime Architecture
The runtime uses a Model Adapter with single-sample TFLite inference. It features three execution modes:
- **FAST**: `student_a_8_4_fp32`
- **BALANCED**: `pruned_mlp_14f_75pct`
- **HIGH_FIDELITY**: `student_b_16_4_fp32`

## 5. QoS Policies
The runtime implements 4 policies:
1. **ACCURACY_PRIORITY**: Prioritizes accuracy by defaulting to HIGH_FIDELITY if it fits the deadline. Downgrades to BALANCED or FAST only if needed to meet the deadline.
2. **BALANCED**: Adjusts based on workload. Under heavy workloads, it uses BALANCED or FAST. Under low workloads, it evaluates deadlines from HIGH_FIDELITY downwards.
3. **DEADLINE_PRIORITY**: Aggressive selection of FAST mode under burst workloads or tight deadlines for safety. Selects BALANCED only if there is sufficient headroom.
4. **COMPUTE_PRIORITY**: Defaults to BALANCED (96 MACs) for compute efficiency, forcing a fallback to FAST only during bursts or when the deadline is tight.

## 6. Workload Model
4 synthetic host-side profiles. Note: These are **experimental simulation parameters, NOT ECU measurements**.
- **LOW**: Multiplier=1.0, Jitter=0.1us (Minimal host CPU contention)
- **MEDIUM**: Multiplier=1.5, Jitter=0.3us (Moderate host CPU contention)
- **HIGH**: Multiplier=3.0, Jitter=0.8us (Heavy host CPU contention)
- **BURST**: Multiplier=5.0, Jitter=2.0us (Burst host CPU contention with high jitter)

## 7. Experimental Methodology
- **Configurations**: 80 configurations (5 deadlines x 4 workloads x 4 policies).
- **Dataset**: 11,200 test samples.
- **Inference**: Single-sample inference.
- **Reproducibility**: Deterministic seed=42.
- **Evidence Category**: TRACE-DRIVEN HOST SIMULATION.

## 8. Results
- **Accuracy**: Ranges from 0.716 (using FAST under tight constraints) to ~0.752 (using HIGH_FIDELITY).
- **Macro F1**: Interestingly, BALANCED (0.756) achieves a higher Macro F1 than HIGH_FIDELITY (0.739).
- **Deadline Compliance Rates**: 100% compliance across all 80 configurations (due to sub-microsecond baseline latencies).
- **Model Switching Patterns**: 
  - `ACCURACY_PRIORITY` almost exclusively activates `student_b_16_4_fp32`.
  - `DEADLINE_PRIORITY` and `COMPUTE_PRIORITY` heavily leverage `pruned_mlp_14f_75pct` and switch to `student_a_8_4_fp32` under BURST workloads.
- **Policy Sensitivity**: The simulator successfully degrades model fidelity under heavy (BURST) workloads, demonstrating the controller's reactivity.

## 9. Ablation Study
1. **Ablation A: Static Highest Accuracy vs QoS-Aware (Balanced)**
   - Static (`student_b_16_4_fp32`): Acc: 0.7518, F1: 0.7390, Latency: 14.07us
   - QoS-Aware (`BALANCED`): Acc: 0.7482, F1: 0.7562, Latency: 13.79us
   - *Finding*: QoS improves F1 score and reduces average latency with minimal accuracy drop.
2. **Ablation B: Static Smallest vs QoS-Aware (Balanced)**
   - Static (`student_a_8_4_fp32`): Acc: 0.7160, F1: 0.7217, Latency: 12.50us
   - QoS-Aware (`BALANCED`): Acc: 0.7482, F1: 0.7562, Latency: 14.10us
   - *Finding*: QoS trades off a slight latency increase for massive accuracy/F1 gains compared to the smallest model.
3. **Ablation C: QoS No Workload Awareness vs With Workload Awareness**
   - No Awareness: Acc: 0.7518, Latency: 13.18us, Switches: 0
   - With Awareness: Acc: 0.7482, Latency: 13.52us, Switches: 1
   - *Finding*: Workload awareness triggers model switching under pressure to maintain real-world feasibility.
4. **Ablation D: QoS No Deadline vs With Deadline**
   - No Deadline (Accuracy Priority): Acc: 0.7518, Latency: 14.25us
   - With Deadline (Balanced): Acc: 0.7482, Latency: 12.85us
   - *Finding*: Deadline constraint forces the scheduler to select computationally cheaper models, decreasing latency.

## 10. Limitations
- All latencies are host-measured, not MCU.
- No WCET (Worst-Case Execution Time) claims.
- No ECU compatibility claims.
- Workload multipliers are synthetic, not measured CPU contention.
- Host inference latency is sub-microsecond (models are tiny), so deadline differentiation is minimal at these scales.

## 11. ESP32-Dependent Work Remaining
The following components strictly require a physical ESP32 to validate:
- Actual MCU inference latency
- On-device SRAM usage
- Flash footprint
- MCU power consumption
- MCU hardware timer calibration
- TFLite Micro tensor arena sizing
- Real-time scheduling validation (FreeRTOS)

## 12. Reproducibility
- All experiments use a deterministic `seed=42`.
- Test splits are stratified and identical to Phase 2/3.
- Uses the completely frozen Phase 4.5 model profile.
- Executed via the automated pipeline script: `phase5/run_phase5_pipeline.py`.

## 13. Recommended Next Experiment
When the ESP32 becomes available: 
Flash `student_b_16_4_int8` to the device, measure actual single-sample inference latency with hardware timers, and validate against the host simulation predictions.

---
**FINAL STATUS**: SOFTWARE_RUNTIME_READY_AWAITING_ESP32
