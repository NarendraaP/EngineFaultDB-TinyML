# ScholarMaster Reviewer Simulation: Paper 1
**Title:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention  
**Simulated Peer Review Date:** August 20, 2026  

---

## Reviewer A — Systems / Embedded ML Expert
- **Strongest Aspect:** Clean, closed-loop state machine that operates strictly on external system telemetry (headroom, contention level) without ground-truth label leakage.
- **Weakest Aspect:** Latency values are host-measured and scaled via synthetic multiplicative contention rather than measured on a real MCU running FreeRTOS.
- **Missing Experiment:** Physical hardware validation on an ARM Cortex-M or ESP32 board.
- **Missing Explanation:** Clarification that .4\%$ active MAC reduction is theoretical arithmetic operations, not hardware wall-clock speedup.
- **Biggest Novelty Concern:** Multi-fidelity computing is established in server/desktop domains; novelty lies in micro-scale FlatBuffer ensemble runtime.
- **Biggest SOTA Concern:** None, provided the scope remains bounded to trace-driven simulation.
- **Likely Rejection Reason (if any):** Absence of physical micro-controller hardware measurements if submitted to a pure hardware venue.
- **Required Revision:** Ensure threats to validity explicitly declare host-simulation boundaries (already completed).
- **Recommendation:** **WEAK_ACCEPT** (Acceptable for IEEE ESL as a simulation/systems study).

---

## Reviewer B — Machine Learning / TinyML Expert
- **Strongest Aspect:** Excellent use of verified Pareto-optimal models ($ to $ MACs, $<4\,\text{KB}$) spanning distinct operating niches.
- **Weakest Aspect:** Tabular diagnostic models (MLP) rather than 2D CNNs or Transformers.
- **Missing Experiment:** None; 80 configurations and 4 ablations provide comprehensive ML coverage.
- **Missing Explanation:** Discussion of how calibration or out-of-distribution samples might affect downstream fault classification.
- **Biggest Novelty Concern:** None; the multi-model adaptation approach is well justified.
- **Likely Rejection Reason (if any):** Model scale is small ($ params), though appropriate for ultra-low-power microcontrollers.
- **Recommendation:** **STRONG_ACCEPT**.

---

## Reviewer C — Methodology / Research Software Expert
- **Strongest Aspect:** Methodological rigor is outstanding. Zero test-set leakage, deterministic seeds ($), stratified splits (/40/20$), and full 4-ablation verification.
- **Weakest Aspect:** Synthetic Gaussian jitter model for contention.
- **Missing Experiment:** None; reproducibility artifacts are complete.
- **Missing Explanation:** None.
- **Biggest Reproducibility Concern:** None; all pipeline scripts and seeds are published.
- **Recommendation:** **STRONG_ACCEPT**.

---

## Consensus Recommendation: ACCEPT / MINOR REVISION (Score: 8.5 / 10)
