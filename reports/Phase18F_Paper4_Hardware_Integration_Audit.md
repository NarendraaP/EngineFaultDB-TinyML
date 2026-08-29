# Phase 18F — Paper 4 Hardware Evidence Integration Audit Report

> **Manuscript:** Paper 4 — An Artifact-Driven Verification Protocol for Reproducible TinyML Deployment Evaluation  
> **Target Venue:** *ACM LCTES / IEEE Software / CASES*  
> **Audited File:** [`papers/Paper4_TinyML_Verification/submission/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/submission/paper.tex)  
> **Compilation Status:** `TECTONIC_BUILD_PASS` (Exit Code 0, 724 KB PDF)  
> **Audit Verdict:** `READY_WITH_HARDWARE_EVIDENCE`  

---

## 1. Integrated Hardware Evidence Verification

The physical microcontroller evidence integrated into Paper 4 was verified:

| Evaluation Dimension | Section Placement | Integrated Physical Evidence | Verification Status |
|:---|:---:|:---|:---:|
| **D6: Timing Predicate ($\mathcal{P}_6$)** | Section III-F | $(\text{Warmup} \ge 100) \land (\text{Batch} = 1) \land (\text{Timer} \in \{\text{perf\_counter}, \text{esp\_timer}\}) \land (\text{Tier} \in \{\text{HOST}, \text{MCU}\})$ | ✅ VERIFIED |
| **Physical Deployment Case Study** | Section IV-E | Full 4-model on-device latency suite on ESP32-D0WD-V3 ($64.55\text{--}89.90\,\si{\micro\second}$) with host-to-silicon slowdowns ($62.9\times\text{--}76.8\times$) | ✅ VERIFIED |
| **Evidence Tier Framework** | Section V (Table V) | Explicit 5-tier taxonomy: Tier 1 Direct Physical, Tier 2 Host Empirical, Tier 3 Simulation, Tier 4 Derived, Tier 5 Future | ✅ VERIFIED |
| **Limitations & WCET Boundary** | Section VII | Formal WCET disclaimed; power analyzer boundaries noted | ✅ VERIFIED |

---

## 2. Methodological & Provenance Audit

1. **Evidence Provenance:** Paper 4 demonstrates why reporting host latency as a surrogate for embedded microcontroller execution produces misleading claims, empirically quantifying the $62.9\times\text{--}76.8\times$ slowdown from x86_64 host simulation to 240 MHz physical silicon.
2. **Artifact Lifecycle Case Study:** Formally illustrates the progression across all four deployment boundaries:
   $$\text{In-Memory Keras Model} \rightarrow \text{Exported TFLite FlatBuffer} \rightarrow \text{C-Header Array} \rightarrow \text{Physical Bare-Metal Binary}$$
3. **Claim Scope Discipline:** Section IV-E explicitly frames the physical experiment as an *additional empirical deployment tier within the case study*, avoiding over-generalization to a claim of universal verification completeness.

---

## 3. Simulated Peer Review

> **Reviewer (Software Engineering / Reproducibility Perspective):**  
> *"Does the hardware experiment add genuine methodological value to the verification protocol?"*  
> **Auditor Assessment:** **PASS.** The ESP32 deployment provides a concrete exemplar of artifact verification in action, demonstrating how the framework isolates toolchain boundaries, measures cross-tier slowdowns, and verifies memory determinism on real silicon.
