# Paper 5 — Phase 19A Research Design & Formal Specification

> **Manuscript Identifier:** Paper 5 — On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers  
> **Author:** Narendra Satish (`narendresh.p@gmail.com`)  
> **Physical Silicon Baseline:** ESP32-D0WD-V3 rev v3.1 (Xtensa LX6 dual-core @ 240 MHz, 4 MB Flash, 320 KB SRAM, COM7)  
> **Phase Status:** `RESEARCH_DESIGN_ESTABLISHED` (Audited against 24,000 physical on-device measurements)  

---

## 1. Executive Summary and Central Purpose

Paper 5 is designed as a focused, high-rigor embedded systems empirical paper that addresses the critical gap between high-level machine learning model design and bare-metal microcontroller execution. While Papers 1–4 establish the theoretical QoS runtime, multi-objective Pareto frontier, domain diagnostic hierarchy, and artifact verification taxonomy respectively, Paper 5 provides the **definitive physical systems evidence**:
1. How disk-serialized, sub-4 KB `FULL_INT8` TinyML models execute on physical 32-bit Xtensa microcontroller silicon.
2. How empirical on-device latencies diverge from host-side x86_64 simulation timings.
3. How static Flash, internal SRAM, and dynamic tensor arena memory buffers are partitioned on bare metal.

---

## 2. Central Research Questions (RQs)

Based on the verified experimental dataset ($N=24,000$ measured inferences across 4 `FULL_INT8` models, 3 independent rounds, in-RAM hardware timer buffering, and allocator memory inspection), we formulate four directly answerable Research Questions:

```
+---------------------------------------------------------------------------------------------------------+
| RESEARCH QUESTION                                  | SCIENTIFIC FOCUS            | EMPIRICAL EVIDENCE   |
+----------------------------------------------------+-----------------------------+----------------------+
| RQ1: Silicon Execution Behavior                    | On-chip latency distribution| 24,000 runs, P95/P99 |
| How do ultra-small FULL_INT8 models execute on     | and statistical dispersion  | timer logs, CI width |
| 240 MHz Xtensa LX6 silicon?                        | under repeated trials.      | < +/- 0.22 us.       |
+----------------------------------------------------+-----------------------------+----------------------+
| RQ2: Resource-to-Latency Translation               | Parameter scaling vs.       | 176 to 412 params    |
| How do parameter counts and theoretical MACs       | measured execution cycles   | vs. 64.55 to 89.90 us|
| translate to physical on-device inference latency? | on non-SIMD integer ALU.    | (R^2 > 0.95).        |
+----------------------------------------------------+-----------------------------+----------------------+
| RQ3: Host-to-Silicon Divergence                    | x86_64 vs. Xtensa LX6       | 62.9x to 76.8x ratio;|
| How large is the latency divergence between host   | relative ranking and noise  | x86 noise floor vs.  |
| simulation and physical microcontroller execution? | floor distortion.           | strict MCU ranking.  |
+----------------------------------------------------+-----------------------------+----------------------+
| RQ4: Memory Layout & Arena Determinism             | Flash, SRAM, Arena, and     | 330 KB Flash, 62 KB  |
| How is memory partitioned between firmware,        | dynamic heap stability      | SRAM, 916 B arena,   |
| static arrays, and TFLM tensor arena buffers?      | during repeated inference.  | 0 B heap leakage.    |
+----------------------------------------------------+-----------------------------+----------------------+
```

---

## 3. Evidence-to-RQ Mapping Matrix

Every claim in Paper 5 is mapped directly to authoritative empirical data in `phase5/measurements/`:

| Paper 5 Section | Addressed RQ | Authoritative Input File | Key Quantitative Metric |
|:---|:---:|:---|:---|
| **Section III: Benchmark Methodology** | RQ1, RQ4 | `phase5/firmware/src/main.cpp` | $N=24,000$ measured runs, $1,200$ warmup, `esp_timer_get_time()` |
| **Section IV: Silicon Latency Profile** | RQ1 | `esp32_model_benchmark.csv` | Mean ($64.55\text{--}89.90\,\mu\text{s}$), P95 ($69\text{--}95\,\mu\text{s}$), Max ($77\text{--}102\,\mu\text{s}$) |
| **Section V: Compute-to-Latency Scaling**| RQ2 | `esp32_full_benchmark.json` | Distillation speedup: $28.2\%$ (`student_a` vs `mlp_14f`), $R^2 \ge 0.95$ |
| **Section VI: Host-to-MCU Divergence** | RQ3 | `tinyml_model_profile_verified.csv` | Slowdown ratio: $62.87\times\text{--}76.77\times$, ranking reversal unmasked |
| **Section VII: Memory Subsystems** | RQ4 | `esp32_model_benchmark.csv` | Flash: $330\,\text{KB}$, SRAM: $61.9\,\text{KB}$, Arena: $916\,\text{B}$ committed ($88.8\%$ headroom) |

---

## 4. Structural Manuscript Blueprint (Target: 4–6 Page Letter / Article)

```
I. INTRODUCTION
   A. The Deployment Reality Gap in TinyML
   B. Memory and Compute Boundaries on 32-Bit Microcontrollers
   C. Contributions of this Paper

II. EXPERIMENTAL DEPLOYMENT ARCHITECTURE
    A. Physical Silicon Target: ESP32-D0WD-V3 (Xtensa LX6 @ 240 MHz)
    B. Toolchain, Runtime & Portable Quantized FullyConnected Kernel
    C. Evaluated FULL_INT8 Candidate Models (176 to 412 Parameters)

III. RIGOROUS ON-DEVICE BENCHMARKING PROTOCOL
     A. Microsecond Hardware Monotonic Timer Instrumentation
     B. In-RAM Latency Accumulation and Percentile Extraction
     C. Multi-Round Statistical Protocol (3 Rounds x 2,000 Iterations)

IV. EMPIRICAL SILICON LATENCY CHARACTERIZATION
    A. Parametric Execution Distributions (Mean, P50, P95, P99, Max)
    B. Inter-Round Repeatability and Confidence Interval Bounds
    C. Feasibility Margins Under Industrial Deadlines (5 ms to 100 ms)

V. HOST-TO-SILICON LATENCY DIVERGENCE ANALYSIS
   A. Quantifying the 62.9x - 76.8x Host-to-MCU Slowdown
   B. Unmasking Noise-Floor Distortions in Host Sub-Microsecond Profiling
   C. Distillation Acceleration on Physical Registers (28.2% Speedup)

VI. MEMORY DECONSTRUCTION & RUNTIME DETERMINISM
    A. Flash Footprint (Partition vs. Image vs. Model Byte Arrays)
    B. Static SRAM vs. Tensor Arena Allocator Commitment (916 Bytes)
    C. Heap Invariance (Zero Runtime Allocations across 25,200 Inferences)

VII. THREATS TO VALIDITY & EMBEDDED LIMITATIONS
     A. Reference Kernels vs. SIMD Assembly (ESP-NN)
     B. Absence of Physical Power Analyzer Instrumentation
     C. Empirical Maximum Latency vs. Formal Static WCET

VIII. CONCLUSION & REPRODUCIBILITY
      A. Summary of Systems Insights
      B. Open-Source Firmware & Measurement Artifact Availability
```

---

## 5. Explicit Scientific Stance & Prohibited Overclaims

Paper 5 enforces strict scientific discipline across all claims:
1. **NO Algorithmic Novelty Claims:** Paper 5 does NOT claim a new compression algorithm, new runtime, or new neural architecture. It is an **empirical hardware characterization and deployment analysis paper**.
2. **NO Formal WCET Claims:** The paper explicitly frames $102\,\mu\text{s}$ as an **empirical maximum observed latency** across $N=24,000$ physical trials under benchmark conditions.
3. **NO End-to-End Throughput Claims:** Reports single-sample inference-rate compute equivalents ($15,491.9\,\text{inf/sec}$), explicitly qualifying that practical system throughput depends on sensor ADC sampling and bus communication.
4. **NO Inferred Energy Claims:** Reports latency and memory without fabricating energy or power numbers.
