# Phase 18E — Paper 1 Hardware Evidence Integration Plan

> **Manuscript:** Paper 1 — QoS-Aware TinyML Runtime for Edge Fault Diagnostics  
> **Target Venue:** *IEEE Transactions on Computers (TC)*  
> **Integration Verdict:** `HARDWARE_SUPPORTING_EVIDENCE` (Targeted upgrades in Discussion & Limitations)  

---

## 1. Executive Summary

Paper 1 introduces a multi-fidelity QoS-aware runtime that dynamically selects between lightweight (`FAST`), balanced (`BALANCED`), and high-fidelity (`HIGH_FIDELITY`) models based on workload contention and deadline constraints.

The physical ESP32 benchmark provides concrete **Tier 1 hardware backing** that candidate model inference latencies ($64.55\text{--}89.90\,\mu\text{s}$) are two orders of magnitude faster than automotive diagnostic deadlines ($5\text{--}100\,\text{ms}$), providing $>97.96\%$ feasibility headroom.

---

## 2. Claim-by-Claim Integration Categorization

| Proposed Hardware Claim | Evidence Category | Recommended Action | Placement in Paper 1 | Exact Recommended Phrasing |
|:---|:---:|:---:|:---:|:---|
| **Physical Model Inference Timing** | Tier 1 (Direct Physical) | `ADD_TO_DISCUSSION` | Section V-B (Practical Feasibility) | *"To establish physical feasibility on real edge silicon, the candidate models were deployed to an ESP32 microcontroller (Xtensa LX6 dual-core @ 240 MHz). Measured single-sample inference latencies were $64.55\,\mu\text{s}$ (`student_a`), $72.96\,\mu\text{s}$ (`student_b`), and $89.90\,\mu\text{s}$ (`mlp_14f`), confirming that on-chip model execution consumes less than $2.04\%$ of the tightest $5\,\text{ms}$ deadline budget."* |
| **Deadline Compliance Headroom** | Tier 1 + Tier 4 | `ADD_TO_DISCUSSION` | Section V-C (Deadline Analysis) | *"Across $24,000$ physical on-device measurements, the maximum observed single-sample execution latency was $102\,\mu\text{s}$, yielding an empirical feasibility headroom of $97.96\%$ at $D=5\,\text{ms}$ and $99.90\%$ at $D=100\,\text{ms}$."* |
| **Scheduler Verification Boundary** | Tier 2 (Host Simulation) | `ADD_TO_LIMITATIONS` | Section VI (Threats to Validity) | *"While single-model inference execution was empirically verified on physical ESP32 silicon, the multi-model dynamic switching policies and workload contention models were evaluated via trace-driven host simulation. Complete RTOS-integrated on-chip multi-task scheduling is investigated in complementary deployment studies."* |
| **Comprehensive Latency Percentiles** | Tier 1 (Distributions) | `RESERVE_FOR_PAPER_5` | — | Full percentile distributions (P25, P75, IQR, multi-round variances) are reserved for Paper 5. |
| **WCET / Hard Real-Time Guarantee** | Unsupported | `DO_NOT_USE` | — | Never claim formal WCET or safety-critical hard real-time guarantees from empirical distributions. |

---

## 3. Preservation of Paper 1 Scope & Independence

- **Preserving Main Contributions:** The core contribution of Paper 1 remains the **QoS scheduler design, multi-policy adaptation strategies, and workload-driven state transitions**.
- **Role of Hardware Data:** Physical hardware metrics serve exclusively as **validation evidence** in the Discussion/Limitations sections to demonstrate real-world physical viability, without diluting the theoretical and algorithmic focus of the paper.
