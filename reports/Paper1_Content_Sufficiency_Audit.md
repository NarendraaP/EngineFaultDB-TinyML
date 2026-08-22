# ScholarMaster Content Sufficiency & Scientific Depth Audit: Paper 1
**Title:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention  
**Venue Target:** IEEE Embedded Systems Letters (ESL) / IEEE Transactions on Computer-Aided Design of Integrated Circuits and Systems (TCAD)  
**Audit Date:** August 20, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  
**Overall Verdict:** CONTENT_SUFFICIENT (Appropriate for IEEE ESL / TCAD Systems Scope)  

---

## 1. Section-Level Content Sufficiency

| Section / Subsection | Substantive? | Scientific Reasoning? | Sufficient Explanation? | Equations / Formalism? | Evidence / Literature? | Classification | Technical Depth Assessment |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Title & Abstract** | Yes | Yes | Yes | Concise | Yes | ADEQUATE | Clearly defines scope, 80-grid evaluations, 3 Pareto modes, and zero-leakage scheduler. |
| **I. Introduction** | Yes | Yes | Yes | Conceptual | Yes | ADEQUATE | Explains why static model deployment fails under time-varying ECU load contention. |
| **II. System Architecture & Multi-Fidelity Runtime** | Yes | Yes | Yes | System Diagram / API | Yes | ADEQUATE | Formulates Model Registry, Model Adapter, and execution modes (FAST, BALANCED, HIGH_FIDELITY). |
| **III. Deadline-Aware QoS Scheduling Policies** | Yes | Yes | Yes | Eq. (1)-(3) | Yes | ADEQUATE | Formally defines utility objective, deadline constraint, and 4 distinct policies. |
| **IV. Experimental Methodology** | Yes | Yes | Yes | Mathematical model | Yes | ADEQUATE | Defines workload multiplier (t)$, Gaussian jitter $\epsilon(t)$, and 80-grid parameters. |
| **V. Results: Accuracy, Compliance & Switching** | Yes | Yes | Yes | Tables I-III, Figs 2-4 | Yes | ADEQUATE | Explains what happened, why policies behave differently, and quantifies trade-offs. |
| **VI. Ablation Studies** | Yes | Yes | Yes | Table IV, Fig 5 | Yes | ADEQUATE | Isolates dynamic switching gain, policy sensitivity, jitter impact, and feature dimensionality. |
| **VII. Discussion: Automotive & Systems Context** | Yes | Yes | Yes | Analytical | Yes | ADEQUATE | Explains powertrain co-location benefits; clearly demarcates host timing from MCU WCET. |
| **VIII. Threats to Validity & Limitations** | Yes | Yes | Yes | Transparent | Yes | ADEQUATE | Explicitly lists simulation boundaries, synthetic contention model, absence of hardware measurements. |
| **IX. Conclusion** | Yes | Yes | Yes | Synthesis | Yes | ADEQUATE | Summarizes key findings without making unsupported claims. |

---

## 2. Research Question -> Evidence Depth Audit

| RQ | Hypothesis | Experiment | Variables | Metric | Authoritative Evidence | Empirical Result | Interpretation | Adequacy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **RQ1: Deadline Compliance** | Dynamic QoS switching maintains $>99\%$ compliance under contention. | 80-grid sweep across 5 deadlines and 4 workloads. | Deadline (-100\,\mu\text{s}$), Workload (LOW-BURST), Policy. | Deadline Compliance (\%) | esults/phase5_policy_comparison.csv | .0\%$ compliance for DEADLINE_PRIORITY and BALANCED under BURST (\,\mu\text{s}$). | Degrades to FAST (.86\,\mu\text{s}$) to absorb load spikes. | FULLY_ANSWERED |
| **RQ2: Accuracy Retention** | ACCURACY_PRIORITY retains highest classification fidelity. | Comparative trace evaluation on 11,200 test samples. | QoS Policy, Workload Contention. | 4-class Accuracy, Macro F1 | esults/phase5_policy_comparison.csv | .14\%$ Accuracy, .7387$ F1 in LOW contention; degrades gracefully under BURST. | Confirms Pareto-optimal high-capacity model selection when headroom permits. | FULLY_ANSWERED |
| **RQ3: Compute Reduction** | Multi-fidelity runtime reduces active MACs by up to .4\%$. | Arithmetic operation trace accounting. | Selected mode per frame. | Theoretical Active MACs | esults/tinyml_model_profile_verified.csv | From $ MACs (HIGH_FIDELITY) to $ MACs (BALANCED) = .421\%$ reduction. | Validates theoretical arithmetic reduction without claiming direct battery savings. | FULLY_ANSWERED |
| **RQ4: Switching Stability** | Closed-loop scheduler avoids pathological thrashing under jitter. | Ablation Study 3 (Latency Jitter Sweep $\sigma \in [0, 0.5]$). | Latency Jitter $\sigma$, Switching Count. | Switch Count, Compliance (\%) | esults/phase5_ablation_results.csv | Switch count stabilizes; compliance drops by $<1.2\%$ at $\sigma = 0.5$. | Demonstrates hysteresis and smoothing stability under noisy telemetry. | FULLY_ANSWERED |

---

## 3. Contribution Depth Audit

| Contribution Claim | Technical Content | Experimental Evidence | Baseline Comparison | Novelty Depth | Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **1. Multi-Fidelity Runtime Architecture** | Model Registry + Adapter for standard FlatBuffers. | Verified execution on 11,200 single-sample frames. | Monolithic static deployment. | MODERATE (Modular architecture for $<4\,\text{KB}$ models). | STRONG |
| **2. Non-Leaking Deadline-Aware Scheduler** | State machine based on telemetry and headroom. | 80-configuration factorial grid (,000$ evaluations). | Static FAST/BALANCED/HIGH, Random Switching. | STRONG (Zero label-routing leakage). | STRONG |
| **3. Multi-Dimensional Systems Characterization** | Theoretical MAC reduction, compliance, switching metrics. | 4 systematic ablations isolating key system factors. | Uncompressed baseline, flat feature sets. | STRONG (Extensive parameter sweeps). | STRONG |

---

## 4. Content-to-Venue Fit
- **Target Venue:** IEEE Embedded Systems Letters (ESL) / IEEE TCAD.
- **Evaluation:** **APPROPRIATE**. Fits standard IEEE 4-page to 6-page double-column systems format with high scientific density.
- **Scientific Content Score:** **9.2 / 10**
