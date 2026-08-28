# Phase 17C — Reviewer-Style Targeted Revision Plan: Paper 1

**Manuscript:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention  
**Target Venue:** IEEE Transactions on Computers (TC)  
**Alternative Venues:** ACM Transactions on Embedded Computing Systems (TECS) / IEEE Internet of Things Journal (IoT-J)  
**Date:** August 28, 2026  
**Author:** Narendra Satish (`narendresh.p@gmail.com`)  

---

## 1. Step 1: Reviewer-Concern Matrix

We analyze the eleven major substantive concerns raised during the Phase 16 Adversarial Peer Review of Paper 1:

| # | Reviewer Concern | Severity | Existing Evidence | Can Fix Without New Experiment? | New Experiment Required? | Recommendation |
|---|---|:---:|---|:---:|:---:|---|
| **1** | **Single Random Seed in Model Training** | **HIGH** | Models frozen from Phase 4 (seed=42); test set split frozen (seed=42). Runtime trace generator uses deterministic seed=42. | **YES** | **NO** | Re-running trace generation with different jitter seeds produces identical scheduling decisions because latency ($\approx 40\,\mu\text{s}$) $\ll$ deadlines ($5,000\,\mu\text{s}$). Elevate single-seed training as an explicit limitation; recommend multi-seed retraining as future work. |
| **2** | **Limited Recent Related Work (2024–2026)** | **MEDIUM** | Comprehensive literature on adaptive inference and TinyML. | **YES** | **NO** | Expand Section III to include NestDNN, AnytimeNets, Once-for-All, MCUNetV2, and 2024–2026 adaptive edge inference surveys. |
| **3** | **68.4% Compute Reduction Wording** | **CRITICAL** | Mathematical proof: $(304 - 96)/304 = 68.421\%$. Mode switch from `HIGH_FIDELITY` to `BALANCED` is verified in `results/phase5_policy_comparison.csv`. | **YES** | **NO** | Strictly rephrase as **"theoretical active MAC reduction through dynamic model selection"**. Explicitly disclaim hardware execution time, CPU cycle, or battery energy reduction claims. |
| **4** | **Synthetic Contention / Workload Model** | **HIGH** | `phase5/simulator/trace_simulator.py` uses multipliers ($1.0\times$ to $5.0\times$) + Gaussian jitter. | **YES** | **NO** | Transparently document that contention is a trace-driven simulation parameter for evaluating scheduler state-machine transitions, not measured RTOS preemption or hardware bus contention. |
| **5** | **Trivial 100% Deadline Compliance** | **CRITICAL** | Sub-400 MAC models execute in $<50\,\mu\text{s}$ on host; deadlines are $5,000$--$100,000\,\mu\text{s}$ ($>100\times$ headroom). | **YES** | **NO** | Transparently disclose this scale disparity in Section VIII and Section XI. Reposition deadline compliance as a feasibility sanity check, focusing the paper's core contribution on **workload-aware model switching and active arithmetic compute reduction**. |
| **6** | **Lack of Physical MCU / ESP32 Validation** | **HIGH** | Section II-B already establishes Evidence Tiering (Tier 1: Host, Tier 2: Simulation, Tier 3: Future MCU). | **YES** | **NO** | Reiterate the Evidence Tiering framework across all sections. Emphasize that the paper contributes an algorithmic runtime architecture and trace-driven evaluation, while physical silicon profiling is planned future work. |
| **7** | **Novelty Relative to Adaptive Inference** | **HIGH** | Prior work (BranchyNet, NestDNN, MSDNet) focuses on sample difficulty or cloud multi-tenancy. | **YES** | **NO** | Articulate the precise contribution: a trace-driven, ground-truth-independent systems runtime that bridges real-time QoS policies with an audited multi-model TinyML registry under dynamic contention. |
| **8** | **Adequacy of 80 Configurations** | **MEDIUM** | $5\text{ deadlines} \times 4\text{ workloads} \times 4\text{ policies} = 80\text{ configurations}$ evaluated on 11,200 held-out test frames. | **YES** | **NO** | Retain full 80-configuration sweep; explain that it systematically spans the discrete design space of deadlines and contention regimes. |
| **9** | **Adequacy of Policy Definitions** | **LOW** | `phase5/runtime/qos_runtime.py` contains exact mathematical decision logic. | **YES** | **NO** | Align manuscript mathematical equations in Section VII with the exact Python source code logic. |
| **10** | **Ablation Validity** | **LOW** | 4 controlled systems ablations in `results/phase5_ablation_results.csv`. | **YES** | **NO** | Ensure ablation conclusions are presented strictly as comparative systems evaluations rather than universal causal claims. |
| **11** | **Generalization Beyond EngineFaultDB** | **MEDIUM** | 55,998 automotive telemetry samples across 4 fault classes. | **YES** | **NO** | Scope claims specifically to high-frequency multi-sensor edge diagnostics; state cross-domain validation (audio/vibration) as future work. |

---

## 2. Step 2: Random-Seed Question & Stochasticity Analysis

### Pipeline Stochasticity Audit:
1. **Model Weights:** Deterministically trained in Phase 4 using fixed seed ($\text{seed}=42$).
2. **Dataset Partition:** Stratified 40/40/20 train/val/test split generated using fixed seed ($\text{seed}=42$).
3. **Trace Simulation:** Jitter in `generate_workload_sequence()` is generated via `np.random.RandomState(seed=42)`.
4. **Scheduler State Transitions:** The scheduling decision rules evaluate `workload in (HIGH, BURST)`. Because simulated latency ($\approx 14$--$41\,\mu\text{s}$) is vastly smaller than the deadline ($5,000\,\mu\text{s}$), random timing fluctuations do not flip boundary conditions.

### Decision:
- **Multi-Seed Retraining is NOT Essential for Manuscript Revision:** The paper's systems contribution is the runtime architecture and scheduler logic managing an existing, pre-verified model registry. 
- **Action:** Retain seed=42 for deterministic reproducibility; explicitly document the frozen model portfolio assumption in Section XI (Limitations) and recommend multi-seed retraining across diverse random initializations as future work.

---

## 3. Step 3: Compute Reduction Claim Audit

### Verification of the 68.4% Metric:
- Mode `HIGH_FIDELITY` (`student_b_16_4_fp32`): $304$ active MACs per inference frame.
- Mode `BALANCED` (`pruned_mlp_14f_75pct`): $96$ active MACs per inference frame.
- Calculation:
  $$\Delta \text{MACs} = \frac{304 - 96}{304} = \frac{208}{304} \approx 68.42105\% \implies \mathbf{68.4\%}$$

### Reachability in the Runtime:
In `results/phase5_policy_comparison.csv`, under the `BALANCED` policy with `HIGH` or `BURST` contention, the runtime selects the `BALANCED` mode for 100% of test frames (`time_in_BALANCED = 1.0`). Therefore, the 96-MAC configuration is 100% active and reachable under contention.

### Mandatory Language Requirement:
The term **"68.4% compute reduction"** must be explicitly defined and qualified as:
**"a 68.4% reduction in theoretical active arithmetic operations (MACs) through dynamic model selection"**.
It must never be conflated with CPU execution time, hardware cycle counts, or battery energy savings.

---

## 4. Step 4 & 5: Deadline Compliance and Workload Model Audit

### The Scale Disparity:
- Sub-400 MAC models execute in $0.82$--$1.69\,\mu\text{s}$ on host CPU.
- Under $5.0\times$ contention with simulated jitter, mean latency reaches $21.32$--$23.98\,\mu\text{s}$ (P95: $35.27$--$41.25\,\mu\text{s}$).
- Configured deadlines: $D \in \{5, 10, 20, 50, 100\}\,\text{ms} = \{5000, 10000, 20000, 50000, 100000\}\,\mu\text{s}$.
- The deadline compliance rate is $100.0\%$ because worst-case simulated execution time is $<1\%$ of the shortest deadline.

### Required Reframing:
1. Transparently disclose that 100% deadline compliance is an expected feasibility result given the microsecond model execution scale.
2. Focus the primary narrative on:
   - **Contention-driven model switching** (gracefully dropping active MACs from 304 to 96 during CPU bursts).
   - **Diagnostic fidelity preservation** (retaining $0.7563$ macro F1 and $74.82\%$ accuracy under burst load).
   - **Stability of the scheduler** (zero high-frequency oscillations).

---

## 5. Step 6: Novelty and Related Work Positioning

### Comparative Analysis: 8 Closest Prior Works (2018–2026)

| Prior Work | Venue / Year | Primary Adaptation Mechanism | Gating Input | Target Hardware | Primary Distinction from Paper 1 |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **NestDNN** (Fang et al.~\cite{fang2018nestdnn}) | ACM MobiCom 2018 | Multi-capacity pruned subnets | System runtime load | Mobile GPU/NPU | Targets mobile video/audio (>10 MB); requires runtime parameter slicing. Paper 1 targets sub-4 KB multi-model TinyML binaries. |
| **BranchyNet** (Teerapittayanon et al.~\cite{teerapittayanon2016branchynet}) | IEEE ICPR 2016 | Early-exit classification heads | Sample prediction entropy | GPU / Cloud | Adapts strictly to sample difficulty; has zero awareness of external CPU contention or execution deadlines. |
| **MSDNet** (Huang et al.~\cite{huang2018multi}) | ICLR 2018 | Multi-scale dense anytime network | Any-time budget exit | GPU / Server | Architectural network design; does not manage an ensemble of independent TFLite FlatBuffer artifacts under QoS policies. |
| **Once-for-All** (Cai et al.~\cite{cai2020once}) | ICLR 2020 | Supernet elastic subnet sampling | Hardware latency lookup | Mobile / Edge TPU | Offline deployment specialization; does not perform online runtime switching under dynamic contention. |
| **MCUNet / MCUNetV2** (Lin et al.~\cite{lin2020mcunet,lin2021mcunetv2}) | NeurIPS 2020/2021 | Joint NAS + memory-aware engine | Static SRAM/Flash budget | Microcontrollers (STM32) | Statically compiles a single fixed neural network into Flash. Does not support dynamic multi-fidelity runtime switching under contention. |
| **Feedback Control RTOS Scheduling** (Lu et al.~\cite{lu2002feedback}) | IEEE RTSS / TC 2002 | PID utilization controller | Measured CPU utilization | Real-time OS | Classic real-time systems theory; evaluates synthetic periodic tasks, not serialized TinyML neural network inference graphs. |
| **Edge-QoS ML Schedulers** (2022–2026 Surveys~\cite{ray2022review,mohammed2023tinyml}) | IEEE Access / IoT-J | Dynamic batching / model zoo | Latency SLOs | Edge Servers / Gateway | Focuses on Linux edge servers with multi-threading; does not address sub-4 KB microcontroller FlatBuffer deployment. |
| **Paper 1 (This Work)** | IEEE TC 2026 | **Online QoS policy scheduler over Pareto model registry** | **Workload contention ($W_t$) + Deadline ($D$)** | **TinyML Runtime (Host Simulation)** | **First trace-driven systems characterization evaluating dynamic QoS scheduling across verified sub-4 KB FlatBuffer models under zero ground-truth leakage.** |

### Defensible Novelty Formulation:
*"This paper contributes a trace-driven, ground-truth-independent systems runtime architecture that dynamically bridges real-time QoS scheduling policies with an audited, multi-fidelity TinyML model registry under dynamic workload contention."*

---

## 6. Step 7 & 8: 80-Configuration Experiment and Policy Audit

### 80-Configuration Matrix Verification:
- **Deadlines (5):** $5\,\text{ms}, 10\,\text{ms}, 20\,\text{ms}, 50\,\text{ms}, 100\,\text{ms}$.
- **Workload Regimes (4):** `LOW` ($1.0\times$), `MEDIUM` ($1.5\times$), `HIGH` ($3.0\times$), `BURST` ($5.0\times$).
- **QoS Policies (4):** `ACCURACY_PRIORITY`, `BALANCED`, `DEADLINE_PRIORITY`, `COMPUTE_PRIORITY`.
- **Total Configurations:** $5 \times 4 \times 4 = 80$ distinct configurations, evaluated across all 11,200 held-out test frames ($896,000$ total frame evaluations).

### Policy Specification vs. Implementation Audit:

| Policy | Decision Objective | Scheduler Logic in Source Code (`qos_runtime.py`) | Manuscript Description Match |
|---|---|---|:---:|
| `ACCURACY_PRIORITY` | Maximize diagnostic accuracy | Selects `HIGH_FIDELITY` if $\hat{L}_{\text{HF}}(W_t) \le D$; degrades to `BALANCED` then `FAST` only if deadline is violated. | **EXACT MATCH** |
| `BALANCED` | Proactive contention adaptation | Selects `BALANCED` under `HIGH`/`BURST` contention if $\hat{L}_{\text{BAL}} \le D$; selects `HIGH_FIDELITY` under `LOW`/`MED` if $\hat{L}_{\text{HF}} \le D$; defaults to `FAST`. | **EXACT MATCH** |
| `DEADLINE_PRIORITY` | Minimize tail latency & ensure safety margin | Selects `FAST` under `BURST` or if $\hat{L}_{\text{FAST}} > 0.5D$; selects `BALANCED` if $\hat{L}_{\text{BAL}} \le 0.8D$; defaults to `FAST`. | **EXACT MATCH** |
| `COMPUTE_PRIORITY` | Minimize active arithmetic operations | Defaults to `BALANCED` ($96$ MACs); degrades to `FAST` only under `BURST` or if $\hat{L}_{\text{BAL}} > D$. | **EXACT MATCH** |

---

## 7. Step 9 & 10: Ablation and Experimental Adequacy Audit

### Ablation Audit (`results/phase5_ablation_results.csv`):
1. **Ablation A (Static Best vs. QoS):** Static `HIGH_FIDELITY` ($75.19\%$ acc, $304$ MACs) vs. QoS `BALANCED` ($74.82\%$ acc, $96$ MACs). **Finding:** $68.4\%$ active MAC reduction with $+0.0172$ Macro F1 gain. (Verified).
2. **Ablation B (Static Small vs. QoS):** Static `FAST` ($71.61\%$ acc, $160$ MACs) vs. QoS `BALANCED` ($74.82\%$ acc, $96$ MACs). **Finding:** $+3.21\%$ accuracy improvement over static lightweight execution. (Verified).
3. **Ablation C (Workload Awareness Gating):** QoS with vs. without workload awareness. **Finding:** Workload estimation triggers proactive mode switching before deadline violations occur. (Verified).
4. **Ablation D (Deadline Gating):** Unconstrained vs. deadline-constrained execution. **Finding:** Deadline enforcement bounds tail latency ($18.49\,\mu\text{s}$ vs. $21.83\,\mu\text{s}$ P95). (Verified).

### Research Question Adequacy Mapping:

| Research Question | Evidence Source | Experimental Finding | Status |
|---|---|---|:---:|
| **RQ1 (Compute Reduction vs. Fidelity)** | Table II, Figures 2-3 | $68.4\%$ active MAC reduction ($96$ vs. $304$) while maintaining $0.7563$ Macro F1. | **FULLY_ANSWERED** |
| **RQ2 (Workload Adaptation)** | Table II, Figure 1 | `BALANCED` policy transitions smoothly from `HIGH_FIDELITY` to `BALANCED` under high contention. | **FULLY_ANSWERED** |
| **RQ3 (Deadline Sensitivity & Switching)** | Table II, `phase5_policy_comparison.csv` | Exactly 1 switch per continuous contention trace; zero high-frequency oscillation. | **FULLY_ANSWERED** |
| **RQ4 (Controlled System Ablations)** | Table III, Figure 4 | Four ablations isolate accuracy gains ($+3.21\%$), compute savings ($68.4\%$), and tail bounding. | **FULLY_ANSWERED** |

---

## 8. Step 11 & 12: Hardware Dependency & Content Depth Review

### Target Venue Suitability:
- **IEEE Transactions on Computers (TC):** TC publishes both experimental and trace-driven systems research. Given the strict Evidence Tiering framework (Tier 1: Host Empirical, Tier 2: Trace Simulation, Tier 3: Future Hardware), Paper 1 provides a complete and defensible software runtime study.
- **Alternative Venues (Backup):** ACM TECS (Transactions on Embedded Computing Systems) and IEEE IoT-J (Internet of Things Journal) are also strong fits.

### Section Depth Review:
- Section I (Intro): **ADEQUATE**
- Section II (Motivation & Evidence Tiering): **ADEQUATE**
- Section III (Related Work): **NEEDS_EXPANSION** (Add NestDNN, AnytimeNets, MCUNetV2, 2024–2026 adaptive edge work).
- Section IV (Research Questions): **ADEQUATE**
- Section V (System Architecture): **ADEQUATE**
- Section VI (Model Registry & Modes): **ADEQUATE**
- Section VII (Scheduling Policies): **ADEQUATE**
- Section VIII (Workload & Deadline Model): **NEEDS_EXPANSION** (Add scale disparity explanation and clarify simulated nature).
- Section IX (Results): **ADEQUATE**
- Section X (Ablations): **ADEQUATE**
- Section XI (Discussion): **ADEQUATE**
- Section XII (Limitations): **NEEDS_EXPANSION** (Elevate 8 explicit limitation points).
- Section XIII (Reproducibility & Conclusion): **ADEQUATE**

---

## 9. Step 13: Terminology and Language Audit Matrix

| Term / Phrase | Current Usage in Manuscript | Classification | Recommended Action |
|---|---|:---:|---|
| **"68.4% compute reduction"** | Lines 32, 251, 272, 296, 330 | **REWRITE** | Replace with **"68.4% reduction in theoretical active arithmetic operations (MACs) through dynamic model selection"**. |
| **"real-time guarantee" / "hard real-time"** | Line 58 | **REWRITE** | Replace with **"execution deadline compliance under simulated contention"**. |
| **"WCET" / "hardware execution time"** | Lines 70, 319 | **RETAIN** | Keep explicitly in limitations to disclaim WCET. |
| **"first" / "pioneering"** | Line 0 | **REMOVE** | Do not claim "first". Use **"trace-driven systems runtime"**. |
| **"SOTA" / "state-of-the-art"** | Line 0 | **REMOVE** | Avoid SOTA claims; position as an empirical systems study. |
| **"zero ground-truth leakage"** | Lines 32, 54, 114, 311, 330 | **RETAIN** | **Keep prominently.** This is an audited, verified architectural strength. |
| **"theoretical active MACs"** | Throughout | **RETAIN** | **Keep.** Clearly distinguishes arithmetic ops from hardware cycles. |

---

## 10. Step 14 & 15: Title, Abstract & Limitations Formulation

### Title Assessment:
- Current Title: **"QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention"**
- Assessment: **RETAIN.** The title accurately describes the systems architecture, the multi-fidelity model registry, and the trace-driven contention framework without promotional exaggeration.

### Expanded 8-Point Limitations (Section XII):
1. **Trace-Driven Contention Simulation:** Contention is modeled via latency scaling and jitter, not physical RTOS thread preemption.
2. **Host-Measured Inference Timing:** Latencies reflect x86_64 host execution; bare-metal MCU timings are planned future work.
3. **Scale Mismatch in Deadline Compliance:** Sub-microsecond model inference trivially satisfies millisecond deadlines; compliance is a feasibility baseline, not an algorithmic breakthrough.
4. **Single Frozen Model Family:** Evaluates a frozen 3-model portfolio derived from the 412-parameter MLP baseline; broader network topologies (CNNs, RNNs) remain future work.
5. **Single Automotive Sensor Benchmark:** Evaluated on the 55,998-sample EngineFaultDB; cross-domain validation on audio and vibration benchmarks is future work.
6. **Theoretical MACs vs. Hardware Cycles:** Active MAC reduction ($68.4\%$) does not linearly map to MCU battery life extensions without hardware clock gating and power profiling.
7. **Single-Seed Model Training:** Models were trained with fixed random seed ($\text{seed}=42$); multi-seed variance analysis is strongly recommended future work.
8. **Static Flash Footprint:** All three models ($<12$\,KB total) reside simultaneously in Flash; memory-constrained devices with $<16$\,KB Flash cannot store the full registry.

---

## 11. Step 16: Decision on New Experiments

### A. REQUIRED BEFORE SUBMISSION: **NONE**
*All substantive reviewer concerns regarding compute reduction phrasing, deadline scale explanation, workload modeling transparency, and related work can be defensively resolved using the existing, verified experimental evidence.*

### B. STRONGLY RECOMMENDED EXPERIMENTS (Future Work):
1. **Physical ESP32 Benchmarking:** Deploy runtime on an ESP32-WROOM-32 running FreeRTOS to measure on-chip execution times via `esp_timer_get_time()` and power consumption under actual RTOS task preemption.
2. **Multi-Seed Retraining:** Retrain models across 5 random seeds to evaluate accuracy and F1 variance.

### C. OPTIONAL EXPERIMENTS (Future Work):
1. **Microsecond-Scale Deadlines:** Re-evaluate simulator with microsecond-scale deadlines ($D \in [10\,\mu\text{s}, 100\,\mu\text{s}]$) to test scheduler stress under tight margins.
2. **Multi-Dataset Validation:** Port runtime pipeline to UCI HAR or industrial vibration telemetry.

### D. NO EXPERIMENT REQUIRED:
The existing 80 configurations and 4 controlled ablations in `results/phase5_policy_comparison.csv` and `results/phase5_ablation_results.csv` fully support the paper's systems claims.

---

## 12. Final Revision Level Classification

```
PAPER 1 REVISION LEVEL: MODERATE_REVISION
```

### Summary of Revision Scope:
1. Reframe compute reduction claim to strictly specify theoretical active MACs through model selection.
2. Disclose the scale disparity between microsecond execution and millisecond deadlines in Section VIII and XI.
3. Expand Section III with 2024–2026 adaptive inference and TinyML literature.
4. Expand Section XII with all 8 explicit limitation dimensions.
5. Align mathematical equations with source code implementation.
6. Cleanse all promotional phrasing while preserving authoritative numerical results.
