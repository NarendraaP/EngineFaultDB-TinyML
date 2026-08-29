# Phase 18E — Hardware Claim Integration Matrix

> **Date:** 2026-08-29  
> **Auditor Role:** Scientific Publishing & Evidence Integration Specialist  
> **Target Manuscripts:** Papers 1, 2, 3, 4, and 5  
> **Status:** `INTEGRATION_ROADMAP_DEFINED`  

---

## 1. Evidence Tier Taxonomy

To ensure scientific rigor, all empirical, analytical, and simulated results are classified according to the 5-Tier Provenance Taxonomy:

| Tier Level | Designation | Definition | Examples in EngineFaultDB-TinyML |
|:---:|:---|:---|:---|
| **Tier 1** | **Direct Physical Measurement** | Measured directly on physical microcontroller silicon with calibrated monotonic timers. | ESP32 execution latency ($64.55\text{--}89.90\,\mu\text{s}$), SRAM allocation ($61.9\,\text{KB}$), Allocator-committed arena ($916\,\text{B}$). |
| **Tier 2** | **Reproducible Simulation / Host Empirical** | Empirical timing on host x86_64 or trace-driven discrete-event simulation. | Host x86_64 latency ($0.98\text{--}1.43\,\mu\text{s}$), simulated contention workload traces (LOW/MED/HIGH/BURST). |
| **Tier 3** | **Derived / Extrapolated** | Mathematically derived from empirical or analytical parameters. | Theoretical active MAC counts, compute reduction percentages ($26.36\%$ test, $89.8\%$ nominal), Host/ESP32 ratios ($62.9\times\text{--}76.8\times$). |
| **Tier 4** | **Literature-Supported** | Values cited from established peer-reviewed literature or standards. | Automotive deadline thresholds ($5\text{--}100\,\text{ms}$), CAN-bus baud rates ($500\,\text{kbps}$). |
| **Tier 5** | **Future / Unsupported** | Hypothesized or unmeasured claims not yet backed by experimental data. | Multi-ECU distributed scheduling, hardware power consumption in Joules/mW (requires power analyzer). |

---

## 2. Master Claim Integration Matrix

The table below governs exactly how physical ESP32 measurements must be worded and placed across Papers 1–5:

| Claim Category | Current / Candidate Wording | Physical Silicon Evidence | Evidence Tier | Allowed? | Recommended Audited Wording | Target Paper | Target Section | Integration Action |
|:---|:---|:---|:---:|:---:|:---|:---:|:---:|:---:|
| **Worst-Case Latency** | "WCET is 102 us guaranteeing real-time response." | Max observed latency $L_{\max} = 102\,\mu\text{s}$ over 24,000 runs. | Tier 1 | ❌ NO | "Empirical maximum observed latency was $102\,\mu\text{s}$ across $24,000$ physical single-sample inferences." | Paper 1 / Paper 5 | Results / Evaluation | `ADD_TO_MAIN_RESULTS` (with corrected wording) |
| **Deadline Margin** | "Physical execution complies with all real-time deadlines." | $L_{\max} = 102\,\mu\text{s}$ vs $D = 5\text{--}100\,\text{ms}$ ($2.04\%\text{--}0.10\%$ utilization). | Tier 1 + Tier 4 | ✅ YES | "Physical single-sample inference completed in $64.55\text{--}89.90\,\mu\text{s}$ on ESP32 silicon, maintaining $>97.9\%$ empirical feasibility margin under $5\text{--}100\,\text{ms}$ deadlines." | Paper 1 | Discussion / Section V | `ADD_TO_DISCUSSION` |
| **Dynamic Scheduler on Silicon** | "The dynamic QoS scheduler runs in real time on ESP32 silicon." | Single-model inference tested on ESP32; dynamic scheduler evaluated on host trace simulator. | Tier 1 (Models) + Tier 2 (Scheduler) | ❌ NO (Mixed claim) | "While individual model inference was verified on physical ESP32 silicon, dynamic multi-model scheduler switching was evaluated via trace-driven simulation." | Paper 1 | Limitations | `ADD_TO_LIMITATIONS` |
| **Pareto Dimensionality** | "Adding physical latency creates a 4D Pareto frontier." | Latency scales monotonically with parameter count ($176 \rightarrow 412$ params $\rightarrow 64.55 \rightarrow 89.90\,\mu\text{s}$). | Tier 1 | ❌ NO | "Physical MCU latency serves as an independent deployment validation dimension, confirming the 3D analytical Pareto frontier (Accuracy, Size, Active MACs) on silicon." | Paper 2 | Section V / Evaluation | `ADD_TO_MAIN_RESULTS` (as secondary axis) |
| **Distillation Speedup** | "Distillation yields a 28.2% latency speedup on real silicon." | `student_a` ($64.55\,\mu\text{s}$) vs `mlp_14f` ($89.90\,\mu\text{s}$). | Tier 1 | ✅ YES | "On 240 MHz Xtensa LX6 silicon, knowledge distillation (`student_a`) reduces physical inference latency by $28.2\%$ ($64.55\,\mu\text{s}$ vs $89.90\,\mu\text{s}$) relative to uncompressed `mlp_14f`." | Paper 2 | Discussion | `ADD_TO_DISCUSSION` |
| **Diagnostic Throughput** | "Engine fault diagnostic throughput is 15,490 samples/sec." | Mean latency $64.55\,\mu\text{s}$ ($1 / 64.55\,\mu\text{s} = 15,491.9\,\text{inf/sec}$). | Tier 1 + Tier 3 | ❌ NO (Unqualified) | "The Stage-1 screening classifier achieves a single-sample inference-rate compute equivalent of $15,491.9\,\text{inf/sec}$ on a single 240 MHz core (pure compute bound, batch=1)." | Paper 3 | Section VI / Discussion | `ADD_TO_DISCUSSION` |
| **Verification Provenance** | "Verification protocol confirms host-to-silicon scaling." | Host ($0.98\text{--}1.43\,\mu\text{s}$) vs ESP32 ($64.55\text{--}89.90\,\mu\text{s}$), ratio $62.9\times\text{--}76.8\times$. | Tier 1 + Tier 2 | ✅ YES | "The framework validates artifact provenance by quantifying the $62.9\times\text{--}76.8\times$ empirical slowdown from host x86_64 simulation to physical 240 MHz MCU execution." | Paper 4 | Section IV / Case Study | `ADD_TO_MAIN_RESULTS` |
| **Memory Footprint** | "Peak dynamic memory is 916 Bytes." | TFLM `MicroAllocator::used_bytes()` committed $916\,\text{B}$ at initialization. | Tier 1 | ❌ NO (Misleading term) | "TFLM MicroAllocator committed $916\,\text{Bytes}$ of static working tensor arena memory with zero runtime heap allocations." | Paper 5 | Architecture & Benchmarks | `RESERVE_FOR_PAPER_5` |
| **Comprehensive Hardware Profile** | Full 24,000-sample latency percentiles (P25, Med, P75, P95, P99, IQR) across 4 models. | 4 models $\times$ 3 rounds $\times$ 2,000 runs. | Tier 1 | ✅ YES | Full percentile distribution tables, repeatability standard deviations, and memory breakdown. | Paper 5 | Core Empirical Results | `RESERVE_FOR_PAPER_5` |

---

## 3. Kernel & Toolchain Scope Classification

The audit determined that the benchmark firmware utilizes the **portable reference `FullyConnected` operator** (`ref_fc::RegisterOp()`) within TensorFlow Lite for Microcontrollers (`Chirale_TensorFLowLite @ 2.0.0`):

- **Classification:** **`STANDARD_TFLM_REFERENCE_DEPLOYMENT`**
- **Hardware Implications:**
  1. The measured latencies ($64.55\text{--}89.90\,\mu\text{s}$) reflect standard, un-accelerated C++ integer arithmetic compiled with `-O3`.
  2. Proprietary DSP assembly optimizations (such as Espressif ESP-NN SIMD intrinsics or Xtensa Tie extensions) were NOT enabled.
  3. Consequently, the measured numbers represent **conservative, highly portable baseline performance** achievable on any standard Xtensa LX6 deployment.
- **Reporting Requirement:** All papers citing this data must explicitly document that the results reflect standard reference TFLM kernels.
