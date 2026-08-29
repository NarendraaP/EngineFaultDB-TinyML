# Phase 18D — Paper Impact & Publication Evidence Assessment

> **Date:** 2026-08-29  
> **Auditor Role:** Scientific Publishing & Manuscript Impact Auditor  
> **Target Manuscripts:** Papers 1, 2, 3, 4, and 5  
> **Audited Physical Evidence:** 24,000 Verified On-Device Measurements on ESP32-D0WD-V3  

---

## 1. Executive Summary of Paper Impacts

The physical microcontroller benchmark completed in Phase 18C and independently audited in Phase 18D represents a major milestone in transitioning the research program from simulation-based and host-empirical characterizations to physical silicon verification.

```
+----------------------------------------------------------------------------------------------------+
| MANUSCRIPT       | VENUE DIRECTION          | IMPACT CLASSIFICATION     | KEY SCIENTIFIC UPGRADE   |
+------------------+--------------------------+---------------------------+--------------------------+
| Paper 1 (QoS)    | IEEE Trans. Computers    | SUBSTANTIAL_UPGRADE       | Physical deadline margin |
| Paper 2 (Pareto) | ACM TODAES               | SUBSTANTIAL_UPGRADE       | Hardware Pareto axis     |
| Paper 3 (Engine) | IEEE Trans. Ind. Inform. | SUPPORTING_EVIDENCE       | Edge screening timing    |
| Paper 4 (Verif.) | ACM LCTES / IEEE Soft.   | SUBSTANTIAL_UPGRADE       | Evidence-tier grounding |
| Paper 5 (ESP32)  | Embedded/TinyML Journal  | NEW_HARDWARE_CLAIM_UNLOCKED| Complete empirical core |
+----------------------------------------------------------------------------------------------------+
```

---

## 2. Detailed Manuscript-by-Manuscript Impact Analysis

### 2.1 Paper 1 — QoS-Aware Multi-Fidelity Runtime
- **Target Venue:** *IEEE Transactions on Computers (TC)*
- **Impact Classification:** **`SUBSTANTIAL_UPGRADE`**
- **Current State (Frozen Phase 17D):** Mode transitions, deadline compliance, and workload scaling are characterized via trace-driven host simulation with host empirical baseline latencies.
- **Physical Silicon Upgrade:**
  - **Empirical Feasibility:** On physical ESP32 silicon @ 240 MHz, single-sample inference completes in **$64.55\,\mu\text{s}$** (`student_a`) to **$89.90\,\mu\text{s}$** (`mlp_14f`), leaving **$>97.96\%$ feasibility headroom** against the tightest evaluated deadline ($D=5\,\text{ms}$).
  - **Tier 4 Evidence:** Provides concrete physical hardware backing that QoS mode switching is not constrained by compute latency on commodity 32-bit automotive-grade MCUs.
- **Audited Claim Recommendation:**
  > *"The evaluated TinyML models completed single-sample INT8 inference in 64.55–89.90 $\mu\text{s}$ mean latency on physical ESP32-D0WD-V3 silicon, demonstrating that all QoS switching modes operate with >97.9% timing headroom under 5–100 ms real-time deadlines."*

---

### 2.2 Paper 2 — TinyML Pareto Frontier Optimization
- **Target Venue:** *ACM Transactions on Design Automation of Electronic Systems (TODAES)*
- **Impact Classification:** **`SUBSTANTIAL_UPGRADE`**
- **Current State (Frozen Phase 17B):** Primary Pareto optimization axes are Accuracy, Serialized Model Size, and Theoretical Active MACs, with host empirical latencies as secondary characterization.
- **Physical Silicon Upgrade:**
  - **Hardware Validation Axis:** Physical latency confirms that Knowledge Distillation (`student_a_8_4_int8`: $64.55\,\mu\text{s}$) achieves a **$28.2\%$ real-world execution speedup** over the uncompressed baseline (`mlp_14f_int8`: $89.90\,\mu\text{s}$) on 32-bit Xtensa registers.
  - **Strict Monotonicity:** Confirms that parameter reductions translate directly into physical execution speedups ($176 \rightarrow 328 \rightarrow 380 \rightarrow 412$ parameters yields $64.55 \rightarrow 72.96 \rightarrow 76.77 \rightarrow 89.90\,\mu\text{s}$).
- **Integration Rule:** Physical latency should be introduced as an **independent deployment validation dimension**, maintaining the primary mathematical Pareto frontier intact while grounding it in silicon reality.

---

### 2.3 Paper 3 — Hierarchical Engine Fault Diagnosis
- **Target Venue:** *IEEE Transactions on Industrial Informatics (TII)*
- **Impact Classification:** **`SUPPORTING_EVIDENCE`**
- **Current State (Frozen Phase 17F):** Cascaded anomaly screening ($\theta^*=0.05$) reduces compute overhead by $26.36\%$ on test distribution and $89.8\%$ on nominal distributions.
- **Physical Silicon Upgrade:**
  - **Screening Latency:** Physical execution demonstrates that the Stage-1 screening model (`student_a`) executes in **$64.55\,\mu\text{s}$**, confirming that anomalous sensor events can be screened at up to **15,490 frames per second** on a single microcontroller core.
  - **Diagnostic Feasibility:** Confirms that edge sensor telemetry does not experience compute bottlenecks during multi-sensor fault monitoring.

---

### 2.4 Paper 4 — Independent TinyML Verification Protocol
- **Target Venue:** *ACM LCTES / IEEE Software / CASES*
- **Impact Classification:** **`SUBSTANTIAL_UPGRADE`**
- **Current State (Frozen Phase 17H):** Proposes a formal 7-dimensional verification taxonomy distinguishing Tier 1 (analytical), Tier 2 (host empirical), Tier 3 (simulation), and Tier 4 (physical MCU) evidence.
- **Physical Silicon Upgrade:**
  - **Empirical Demonstration of Evidence Tiers:** Phase 18C/18D provides an exemplary case study demonstrating the exact numerical scaling between Tier 2 (x86_64 host: $0.98\text{--}1.43\,\mu\text{s}$) and Tier 4 (physical ESP32: $64.55\text{--}89.90\,\mu\text{s}$), revealing a consistent **$62.9\times\text{--}76.8\times$ slowdown ratio**.
  - **Reproducibility Protocol:** Directly demonstrates the framework's protocol for detecting compiler mismatches (such as the CMSIS-NN ARM kernel issue identified and resolved in Phase 18B).

---

### 2.5 Paper 5 — On-Device ESP32 TinyML Deployment & Validation
- **Target Venue:** *Specialized Embedded Systems / TinyML Journal*
- **Impact Classification:** **`NEW_HARDWARE_CLAIM_UNLOCKED`**
- **Evidence Ready for Manuscript Drafting:**
  1. **Interrogated Silicon Specifications:** ESP32-D0WD-V3 rev v3.1 @ 240 MHz, 4 MB Flash, 320 KB SRAM.
  2. **Comprehensive Latency Distributions:** 24,000 measured single-sample inferences across 4 FULL_INT8 models with exact percentiles (P25, Median, P75, P95, P99, IQR, Min, Max).
  3. **Strict Memory Separation:** Complete breakdown of Flash program footprint (330 KB / 25.2%), Static SRAM (61.9 KB / 18.9%), Tensor Arena Allocator commitment (916 Bytes), and Free Dynamic Heap (237.4 KB).
  4. **Multi-Round Stability:** 3 independent rounds confirming inter-round standard deviation $<0.03\,\mu\text{s}$ on deterministic models.
  5. **Zero Memory Leaks:** 0 bytes heap loss across 25,200 total physical executions.

---

## 3. Recommended Roadmap

1. **Keep Papers 1–4 Text Frozen for Now:** Do not automatically edit Papers 1–4 until coordinated revision phases are scheduled.
2. **Use Audited Citations:** When physical data is referenced in future revisions, adhere strictly to the audited phrasings defined in [`reports/Phase18D_Independent_Hardware_Benchmark_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase18D_Independent_Hardware_Benchmark_Audit.md).
3. **Paper 5 Initiation:** The complete empirical dataset is now fully verified and archived, providing the experimental foundation for Paper 5.
