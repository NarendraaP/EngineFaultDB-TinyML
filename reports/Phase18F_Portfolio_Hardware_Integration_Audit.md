# Phase 18F — Portfolio Hardware Integration Master Audit Report

> **Date:** 2026-08-29  
> **Auditor Role:** Portfolio Scientific Quality Assurance & Cross-Manuscript Auditor  
> **Evaluated Portfolio:** Papers 1, 2, 3, and 4  
> **Physical Silicon Evidence:** 24,000 Verified On-Device Measurements on ESP32-D0WD-V3  
> **Overall Portfolio Verdict:** `ALL_PAPERS_READY_WITH_HARDWARE_EVIDENCE`  

---

## 1. Portfolio Synthesis & Build Verification

All four modified manuscripts were compiled from source using Tectonic:

| Manuscript | Focus Area | Target Venue | Tectonic Build | PDF Output Size | Final Audit Status |
|:---|:---|:---|:---:|:---:|:---:|
| **Paper 1** | QoS-Aware Multi-Fidelity Runtime | *IEEE Trans. Computers* | ✅ Exit Code 0 | 1.45 MB | `READY_WITH_HARDWARE_EVIDENCE` |
| **Paper 2** | TinyML Model Compression Pareto | *ACM TODAES* | ✅ Exit Code 0 | 928 KB | `READY_WITH_HARDWARE_EVIDENCE` |
| **Paper 3** | Hierarchical Engine Diagnostics | *IEEE Trans. Ind. Inform.* | ✅ Exit Code 0 | 1.26 MB | `READY_WITH_HARDWARE_EVIDENCE` |
| **Paper 4** | TinyML Verification Protocol | *ACM LCTES / IEEE Software*| ✅ Exit Code 0 | 724 KB | `READY_WITH_HARDWARE_EVIDENCE` |

---

## 2. Numerical Immutability Audit

The audit verified that all historical non-hardware metrics remained 100% frozen, while all newly integrated physical hardware values exactly matched the authoritative measurement files:

| Verification Dimension | Authoritative Source File | Portfolio Check | Drift Count | Status |
|:---|:---|:---|:---:|:---:|
| **Model Accuracies / Macro F1s** | `results/tinyml_model_profile_verified.csv` | Checked across Papers 1–4 | **0** | ✅ 100% Frozen |
| **FlatBuffer File Sizes** | `results/tinyml_model_profile_verified.csv` | Checked across Papers 1–4 | **0** | ✅ 100% Frozen |
| **Theoretical Active MACs** | `results/tinyml_model_profile_verified.csv` | Checked across Papers 1–4 | **0** | ✅ 100% Frozen |
| **QoS Policy Comparison Metrics** | `results/phase5_policy_comparison.csv` | Checked in Paper 1 | **0** | ✅ 100% Frozen |
| **Cascade Threshold Metrics** | `results/baseline_metrics.csv` | Checked in Paper 3 | **0** | ✅ 100% Frozen |
| **Physical ESP32 Latencies** | `phase5/measurements/esp32_model_benchmark.csv` | Checked across Papers 1–4 | **0** | ✅ 100% Concordance |

---

## 3. Scientific Claim & Boundary Compliance Matrix

The portfolio was audited against the mandatory claim rules established in Phase 18D and 18E:

```
+---------------------------------------------------------------------------------------------------------+
| CLAIM RESTRICTION               | ENFORCEMENT METHOD                          | PORTFOLIO COMPLIANCE    |
+---------------------------------+---------------------------------------------+-------------------------+
| No "WCET" claims                | Replaced with empirical latency / headroom  | ✅ 100% COMPLIANT       |
| No "End-to-End Throughput"      | Replaced with single-sample compute equiv.  | ✅ 100% COMPLIANT       |
| No "Validated Pareto Frontier"  | Framed as secondary deployment validation   | ✅ 100% COMPLIANT       |
| No "Peak Dynamic Memory"        | Framed as allocator-committed arena buffer  | ✅ 100% COMPLIANT       |
| No Causal CPU Frequency Claims  | Framed as observed host/ESP32 slowdown ratio| ✅ 100% COMPLIANT       |
| No Universal Monotonicity       | Scoped to the evaluated four-model set      | ✅ 100% COMPLIANT       |
+---------------------------------------------------------------------------------------------------------+
```

---

## 4. Preservation of Research Independence Across Papers 1–5

The audit verified that sharing the validated physical ESP32 measurements does NOT create scientific redundancy across manuscripts:
- **Paper 1:** Utilizes physical latency to validate the **empirical feasibility margin of the QoS runtime** under automotive deadlines.
- **Paper 2:** Utilizes physical latency as a **secondary deployment validation dimension** confirming the analytical 3D Pareto frontier.
- **Paper 3:** Utilizes physical latency to demonstrate **real-time edge screening feasibility** for engine telemetry.
- **Paper 4:** Utilizes physical latency as a **methodological case study of Tier 2 vs. Tier 4 evidence provenance**.
- **Paper 5 (Future):** Will serve as the dedicated manuscript for **full physical embedded systems architecture, on-device latency distributions, and bare-metal memory budgeting**.
