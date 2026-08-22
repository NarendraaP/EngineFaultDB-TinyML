# ESP32 Hardware Impact on Publications

**Project:** QoS-Aware TinyML Runtime Research  
**Hardware Status:** `PENDING_PHYSICAL_ESP32`  
**Auxiliary Hardware Available:** Arduino Uno (ATmega328P) and Arduino Mega 2560 (ATmega2560)  
**Date:** August 20, 2026  

---

## 1. Overview & Methodological Ground Rules

To prevent premature or unsupported claims in peer-reviewed venues, this document evaluates the precise impact of physical ESP32 on-device measurements on the proposed publications.

### Core Distinctions
- **Host Simulation & Model Profiles:** 100% empirical on the host PC. Fully publishable for algorithmic, modeling, diagnostic, and methodological papers without hardware fabrication.
- **On-Device Physical Validation:** Essential only when a paper's central scientific hypothesis explicitly claims real-time microcontroller hardware performance, on-chip SRAM footprint, or physical energy consumption.

---

## 2. Paper-by-Paper ESP32 Dependency Assessment

---

### Paper P1: QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI
- **Primary Domain:** Systems / Real-Time Scheduling / Edge AI Architecture
- **Can Be Completed Without ESP32?** **YES.**
  - *Rationale:* The core systems contribution—the multi-fidelity runtime architecture, Pareto model controller, 4 QoS policies, trace-driven simulation across 80 configurations, and 4 ablation studies—is fully evaluated via rigorous trace-driven host simulation.
- **Would ESP32 Significantly Strengthen It?** **YES (Substantially).**
  - *Impact:* Adding physical ESP32 execution timings elevates the paper from a *Systems/Simulation Conference Paper* (e.g., IEEE RTSS Work-in-Progress, ACM SAC, or IEEE Edge) to a *Top-Tier Embedded/Real-Time Journal* (e.g., IEEE Transactions on Computers, IEEE TCAD, or ACM TECS).
- **Is ESP32 Essential for its Central Claim?** **NO**, provided the paper explicitly scopes its evaluation as a *Trace-Driven Multi-Fidelity Runtime Simulation* and makes zero claims of hardware WCET or physical ECU compatibility.
- **Required ESP32 Measurements (if added):**
  1. On-device single-sample inference latency per mode via `esp_timer_get_time()`.
  2. Model switching latency overhead in SRAM.
  3. Static and dynamic tensor arena SRAM allocation.
  4. Real-time deadline compliance under hardware FreeRTOS thread contention.

---

### Paper P2: Empirical Pareto Frontier of Model Compression Paradigms for TinyML
- **Primary Domain:** TinyML / Model Compression / Edge Machine Learning
- **Can Be Completed Without ESP32?** **YES (100% Complete Now).**
  - *Rationale:* The research questions focus on model-level compression mechanics: theoretical active MAC reduction, parameter density, quantized integer tensor arithmetic (INT8 FlatBuffers with 0 float32 tensors), and the structural decoupling of FlatBuffer file sizes from magnitude pruning. All of these are intrinsic properties of the serialized models and TensorFlow Lite execution graphs.
- **Would ESP32 Significantly Strengthen It?** **MODERATE.**
  - *Impact:* On-chip flash footprint and on-device INT8 kernel speedups would add practical confirmation, but the theoretical and host empirical model analysis is already self-contained and submission-ready for venues like *IEEE Embedded Systems Letters*, *TinyML Research Symposium*, or *ACM Transactions on Embedded Computing Systems*.
- **Is ESP32 Essential for its Central Claim?** **NO.**
- **Required ESP32 Measurements (if added):**
  1. On-chip flash storage bytes per model (`.rodata` footprint).
  2. Measured TFLM execution latency per model at 240 MHz.

---

### Paper P3: Hierarchical Multi-Fidelity Machine Learning for Real-Time Engine Fault Diagnostics
- **Primary Domain:** Applied Machine Learning / Fault Diagnostics / Industrial Informatics
- **Can Be Completed Without ESP32?** **YES (100% Complete Now).**
  - *Rationale:* The central contribution is domain-specific: sensor collinearity reduction, input dimensionality optimization (14f $\rightarrow$ 12f), and an asymmetric binary-screening to multi-class cascade with strictly validation-calibrated thresholds ($T_{opt}=0.80$). This is evaluated entirely on the EngineFaultDB dataset using standard ML metrics (ROC, PR, Confusion Matrices, Anomaly False Negative Rate).
- **Would ESP32 Significantly Strengthen It?** **LOW / MARGINAL.**
  - *Impact:* Venues in this field (*IEEE Transactions on Industrial Informatics*, *Mechanical Systems and Signal Processing*, *Reliability Engineering & System Safety*) prioritize fault diagnostic recall, false-negative minimization, and sensor feature selection over specific silicon benchmarks.
- **Is ESP32 Essential for its Central Claim?** **NO.**
- **Required ESP32 Measurements (if added):** None required for submission.

---

### Paper P4: Methodological Pitfalls & Verification Protocols in Microcontroller TinyML Research
- **Primary Domain:** Software Engineering / Empirical Reproducibility / Edge AI Benchmarking
- **Can Be Completed Without ESP32?** **YES (100% Complete Now).**
  - *Rationale:* The paper analyzes methodological errors and verification protocols. The evidence base consists of the 20 real discrepancies identified during the independent audit, the mathematical demonstration of test-set threshold leakage ($+1.8\%$ optimistic bias), and the formalization of the 15-point verification checklist.
- **Would ESP32 Significantly Strengthen It?** **LOW.**
  - *Impact:* The paper's strength lies in auditing and software engineering rigor (*IEEE Transactions on Software Engineering*, *ACM Transactions on Software Engineering and Methodology*, or *IEEE Software*).
- **Is ESP32 Essential for its Central Claim?** **NO.**
- **Required ESP32 Measurements (if added):** None required.

---

### Paper P7 (Future Paper): On-Device Deployment & Hardware Validation of QoS-Aware TinyML on ESP32 Silicon
- **Primary Domain:** Microcontroller Hardware / Physical Edge Deployment
- **Can Be Completed Without ESP32?** **NO (Entirely contingent on physical hardware).**
- **Is ESP32 Essential for its Central Claim?** **YES (100% Essential).**
  - *Rationale:* This paper will report exclusively physical on-device measurements: actual ESP32-WROOM-32 / ESP32-S3 execution times, hardware FreeRTOS task preemption, physical power/energy consumption (mJ per inference), and validation of the C byte array interfaces specified in `phase5/hardware/esp32_interface.md`.
- **Target Venues:** *IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD)*, *IEEE Internet of Things Journal*, or *ACM Transactions on Sensor Networks*.

---

## 3. Comparative Summary Matrix

| Candidate Paper | Submission Readiness Today | ESP32 Impact on Paper | Target Venue Tier Today (Host/Sim) | Target Venue Tier with ESP32 |
| :--- | :--- | :--- | :--- | :--- |
| **P1: QoS-Aware Runtime** | Ready (Simulation scope) | **High** (Elevates to Top Journal) | IEEE RTSS-WIP / IEEE Edge / ACM SAC | IEEE Trans. Computers / ACM TECS |
| **P2: TinyML Pareto Analysis** | **Ready Now** | Moderate | IEEE ESL / TinyML Summit / Sensors | IEEE TCAD / ACM TODAES |
| **P3: Engine Diagnostics Cascade** | **Ready Now** | Low (Domain ML focus) | IEEE TII / MSSP / Applied Soft Comp. | IEEE TII / MSSP |
| **P4: TinyML Audit Protocol** | **Ready Now** | Low (Methodology focus) | IEEE TSE / IEEE Software / MLSys Artifacts | IEEE TSE / ACM TOSEM |
| **P7: ESP32 Hardware Validation** | Blocked (Awaiting hardware) | **Mandatory** (Cannot exist without ESP32) | *Not Applicable* | IEEE IoT-J / IEEE TCAD / IEEE Sensors |

---

## 4. Hardware Integration Roadmap (When ESP32 Arrives)

When physical ESP32 silicon is connected:
1. **Zero Architecture Redesign:** The C-array headers (`phase5/firmware/include/`) and test vectors (`mcu_test_vectors.h`) are already compiled and pre-verified.
2. **Execution Steps:**
   - Flash baseline TFLite Micro firmware (`phase5/firmware/main_tflm_baseline.cpp`) via PlatformIO.
   - Profile all 4 candidate INT8 models over 1,000 single-sample UART iterations at 115,200 baud.
   - Populate [`phase5/hardware/esp32_interface.md`](file:///d:/WiDe/EngineFaultDB-main/phase5/hardware/esp32_interface.md) result schema.
3. **Publication Impact:**
   - Instantly unlocks Paper P7 as a dedicated hardware paper, OR
   - Substantially upgrades Paper P1 into a flagship full-stack software+hardware journal manuscript.
