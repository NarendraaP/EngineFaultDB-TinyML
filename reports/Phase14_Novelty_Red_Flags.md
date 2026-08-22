# Phase 14: Hostile Reviewer Novelty Red-Flag Report
**Audit Date:** August 22, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  
**Strict Mandate:** Actively identify every potential vulnerability, overclaim, or ambiguous phrasing that a hostile, expert IEEE/ACM reviewer could attack, and specify the exact defensive correction.  

---

## 1. Paper 1 Red Flags (QoS Runtime)

### Red Flag 1.1: Conflating Trace-Driven Simulation with Physical Hardware WCET
- **Exact Vulnerability:** If a reviewer interprets latency scaling (t) \cdot L_i + \epsilon(t)$ as a measured hardware execution time on an actual MCU, they will reject for missing hardware measurements.
- **Closest Prior Art:** FreeML, TinyEngine (evaluated directly on STM32 / Cortex-M hardware).
- **Severity:** HIGH
- **Correction:** Explicitly maintain in the Abstract, Section IV, and Section VIII that all latencies represent *host-measured execution scaled via a trace-driven multiplicative contention model*. Explicitly state: *"Physical MCU hardware deployment, energy measurement, and hardware WCET guarantees are outside the scope of this software simulation study."* (Already implemented in manuscript).

### Red Flag 1.2: Calling the 68.4% Active MAC Reduction "Energy Savings"
- **Exact Vulnerability:** Reviewer notes that active MAC reduction does not scale linearly with battery energy due to static leakage and memory bus overhead.
- **Closest Prior Art:** Sze et al. (Energy-efficient deep learning survey).
- **Severity:** MEDIUM
- **Correction:** Restrict all phrasing to *\"theoretical active arithmetic operations (MACs)\"* and avoid claiming unmeasured battery runtime extensions.

---

## 2. Paper 2 Red Flags (TinyML Model Compression)

### Red Flag 2.1: Overclaiming Algorithmic Compression Novelty
- **Exact Vulnerability:** A reviewer could state: *"Pruning, INT8 quantization, and distillation are standard methods since 2016. What is the algorithmic novelty?"*
- **Closest Prior Art:** Han et al. (Deep Compression 2016), MLPerf Tiny (2021).
- **Severity:** HIGH
- **Correction:** Clearly frame the paper as a *systematic empirical Pareto characterization and low-level FlatBuffer artifact benchmark*, not a new pruning algorithm. Emphasize the novel discovery that magnitude pruning yields zero file size reduction in standard TFLite FlatBuffers (,920\,\text{B}$).

### Red Flag 2.2: Generality Across Model Architectures
- **Exact Vulnerability:** Reviewer notes that findings on MLPs might not directly apply to 2D CNNs or Vision Transformers.
- **Closest Prior Art:** MobileNet, MicroNet.
- **Severity:** MEDIUM
- **Correction:** Explicitly declare in Threats to Validity that the 12 candidate models represent sub-4KB tabular Edge AI architectures and that convolutional tensor buffers may exhibit different metadata overhead ratios.

---

## 3. Paper 3 Red Flags (Hierarchical Diagnostics)

### Red Flag 3.1: Claiming "First Hierarchical Fault Diagnosis Framework"
- **Exact Vulnerability:** Hierarchical classifiers and binary anomaly screeners have existed in industrial diagnostic literature for over a decade.
- **Closest Prior Art:** Traita et al. (Cascaded classifiers 2020), Kulkarni et al. (2021).
- **Severity:** HIGH
- **Correction:** Frame the contribution as a *domain-specific asymmetric cost optimization that exploits the physical nominal operational prior ($>90\%$) with a zero-leakage validation-calibrated threshold gating protocol*.

### Red Flag 3.2: Steady-State vs. Transient Drive-Cycle Generalization
- **Exact Vulnerability:** Reviewer notes that EngineFaultDB is collected under controlled steady-state dynamometer conditions rather than noisy on-road drive cycles.
- **Closest Prior Art:** Real-world OBD-II telemetry datasets.
- **Severity:** MEDIUM
- **Correction:** Transparently disclose the steady-state dynamometer nature of the benchmark in Section VIII (Threats to Validity) and identify transient on-road validation as future work.

---

## 4. Paper 4 Red Flags (Verification Framework)

### Red Flag 4.1: Claiming a "Universal Verification Taxonomy for All TinyML"
- **Exact Vulnerability:** Reviewer could argue: *"You validated this on one 12-model pipeline. How can you claim a universal framework for all edge AI?"*
- **Closest Prior Art:** ML Reproducibility Checklists (Pineau et al.).
- **Severity:** HIGH
- **Correction:** Frame the 7-dimensional taxonomy as an *empirical verification protocol demonstrated on an end-to-end TinyML case study and extensible to general Edge AI pipelines*.

### Red Flag 4.2: Discrepancies Dismissed as "Project Bugs"
- **Exact Vulnerability:** Reviewer argues that the 20 uncovered discrepancies are simply implementation bugs rather than research findings.
- **Closest Prior Art:** Software engineering defect studies in ML (e.g., Islam et al., Zhang et al.).
- **Severity:** MEDIUM
- **Correction:** Emphasize that standard Python APIs (model.evaluate()) reported identical .00\%$ accuracy for models with corrupted integer graphs, proving that low-level FlatBuffer discrepancies are invisible to standard ML evaluation pipelines.

---

## 5. Summary of Red-Flag Mitigation Status

| Paper | Critical Red Flags | High Red Flags | Medium Red Flags | Mitigation Status in Manuscripts |
| :--- | :---: | :---: | :---: | :--- |
| **Paper 1** | 0 | 1 | 1 | **Fully Mitigated** (Host simulation & theoretical MAC framing enforced). |
| **Paper 2** | 0 | 1 | 1 | **Fully Mitigated** (Framed strictly as empirical Pareto characterization). |
| **Paper 3** | 0 | 1 | 1 | **Fully Mitigated** (Framed as domain-specific asymmetric cost optimization). |
| **Paper 4** | 0 | 1 | 1 | **Fully Mitigated** (Framed as empirical verification protocol from case study). |
