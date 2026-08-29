# Phase 18E — Paper 3 Hardware Evidence Integration Plan

> **Manuscript:** Paper 3 — Hierarchical and Cascaded TinyML for Real-Time Engine Fault Diagnostics  
> **Target Venue:** *IEEE Transactions on Industrial Informatics (TII)*  
> **Integration Verdict:** `HARDWARE_SUPPORTING_EVIDENCE` (Targeted Edge Feasibility Validation)  

---

## 1. Executive Summary

Paper 3 introduces a hierarchical and cascaded classification framework for internal combustion engine diagnostics:
- **Stage 1 (Binary Anomaly Screening):** Ultra-lightweight screening filter ($\theta^* = 0.05$) to bypass nominal engine cycles.
- **Stage 2 (Multiclass Fault Isolation):** Higher-capacity diagnostic classifier invoked only upon detected anomalies.

The physical ESP32 benchmark provides **Tier 1 supporting evidence** that on-device single-sample inference latency ($64.55\,\mu\text{s}$ for `student_a`, $89.90\,\mu\text{s}$ for `mlp_14f`) easily supports high-frequency engine sensor telemetry without computational bottlenecks.

---

## 2. Claim-by-Claim Integration Categorization

| Proposed Hardware Claim | Evidence Category | Recommended Action | Placement in Paper 3 | Recommended Audited Phrasing |
|:---|:---:|:---:|:---:|:---|
| **Edge Diagnostic Feasibility** | Tier 1 (Direct Physical) | `ADD_TO_DISCUSSION` | Section V-D (Practical Edge Deployment) | *"To confirm real-time execution feasibility on industrial edge hardware, the candidate screening model was deployed to a physical ESP32 microcontroller (Xtensa LX6 @ 240 MHz). Single-sample INT8 inference executed in $64.55\,\mu\text{s}$ mean latency, demonstrating that edge microcontrollers can process incoming multi-sensor telemetry with negligible computational overhead."* |
| **Compute-Equivalent Ingestion Rate** | Tier 1 + Tier 3 | `ADD_TO_DISCUSSION` | Section V-D | *"At an isolated inference duration of $64.55\,\mu\text{s}$, the Stage-1 classifier achieves a pure compute-equivalent processing capacity of $15,491.9\,\text{inferences/sec}$ on a single core, leaving $>98\%$ of CPU cycles available for ADC acquisition and CAN-bus communications."* |
| **End-to-End System Throughput** | Unsupported | `DO_NOT_USE` | — | Never claim $15,490\,\text{samples/sec}$ as full "end-to-end system throughput", as ADC sampling, feature normalization, and I/O will bound practical ingestion rates. |
| **Automotive ECU Safety Guarantee** | Unsupported | `DO_NOT_USE` | — | Never claim automotive safety certification or production ECU equivalence from generic ESP32 evaluation boards. |

---

## 3. Recommended Integration Scope in Paper 3

- **Target Addition:** Exactly one concise subsection in Section V (e.g., Section V-D: *Microcontroller Hardware Feasibility*) comprising 1–2 paragraphs and a compact summary table comparing screening vs diagnostic model execution times on ESP32 silicon.
- **Independence:** Paper 3 remains focused on **domain-specific fault diagnosis, class imbalance handling, and cascaded screening accuracy**.
