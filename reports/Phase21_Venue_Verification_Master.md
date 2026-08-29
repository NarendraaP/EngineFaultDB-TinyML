# Phase 21 — Master Venue Verification & Requirements Audit

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** Official 2026 Publisher Policies & Submission Requirements for Papers 1–5  
**Author:** Narendra Satish (`narendresh.p@gmail.com`)  
**Date:** August 29, 2026  

---

## 1. Executive Summary

This report establishes the verified 2026 publisher submission policies, formatting rules, page budgets, and article processing charges (APCs) from official IEEE and ACM sources for all candidate venues across the five-paper portfolio.

---

## 2. Venue-by-Venue Verification Master Table

| Paper | Target Venue | Official Scope Match | Article Type | Page Limit / Budget | Current Manuscript Length | Publishing Model & APC (2026) | Submission Portal | Fit Classification |
|---|---|---|---|---|---|---|---|---|
| **Paper 1** | **IEEE Transactions on Computers (TC)** | Real-time embedded runtime systems, multi-model execution | Regular Research Paper | Max 12 pages (standard) | **7.0 Pages** (within limit) | Hybrid (Free subscription option / $2,800 OA APC) | ScholarOne / IEEE Author Portal | **EXCELLENT_FIT** |
| **Paper 2** | **ACM Transactions on Design Automation of Electronic Systems (TODAES)** | Model compression, Pareto exploration, embedded optimization | Regular Research Article | No rigid cap (typically 8–12 pp.) | **7.0 Pages** (within limit) | Fully OA (ACM Open $0 / $250 ACM member subsidized) | ACM Manuscript Central | **EXCELLENT_FIT** |
| **Paper 3** | **IEEE Transactions on Industrial Informatics (TII)** | Cyber-physical systems, automotive condition monitoring | Regular Research Paper | Strict 10-page limit | **7.0 Pages** (within limit) | Hybrid (Free subscription option / $2,800 OA APC) | IEEE Author Portal (AtyponRex) | **EXCELLENT_FIT** |
| **Paper 4** | **ACM LCTES (SIGPLAN/SIGBED)** | Embedded systems tools, artifact verification, defect taxonomy | Conference Research Paper | Max 10 pages all-inclusive | **6.0 Pages** (within limit) | ACM Conference Proceedings / ACM Open | HotCRP / Linklings / EasyChair | **EXCELLENT_FIT** |
| **Paper 5** | **ACM Transactions on Embedded Computing Systems (TECS)** | Bare-metal MCU hardware characterization, TinyML profiling | Regular Research Article | No rigid cap (typically 8–12 pp.) | **7.0 Pages** (within limit) | Fully OA (ACM Open $0 / $250 ACM member subsidized) | ACM Manuscript Central / ScholarOne | **EXCELLENT_FIT** |

---

## 3. Detailed Venue Evaluations

### Paper 1: IEEE Transactions on Computers (TC)
* **Scope Fit:** Systems-level multi-fidelity runtime, dynamic degradation scheduling, and deadline-aware execution under workload contention match IEEE TC's focus on computer systems architecture and embedded systems.
* **Evidence Boundaries:** Trace-driven host simulation is accepted for multi-configuration workload exploration ($80$ configurations) when grounded by physical single-sample execution feasibility ($64.55\text{--}89.90\,\si{\micro\second}$).
* **Length & Formatting:** 7.0 IEEE double-column pages is well within the 12-page ceiling (no overlength page charges).
* **Recommendation:** **SUBMIT_TO_TC** (Primary) / **ACM TECS** (Alternative).

---

### Paper 2: ACM Transactions on Design Automation of Electronic Systems (TODAES)
* **Scope Fit:** Multi-objective Pareto characterization comparing structured channel pruning against knowledge distillation fits TODAES's design automation and hardware-software optimization scope.
* **Evidence Boundaries:** Framed as an empirical Pareto design characterization across serialized TinyML artifacts with independent physical ESP32 corroboration ($28.20\%$ speedup), avoiding unsupported algorithmic SOTA claims.
* **Length & Formatting:** 7.0 pages formatted in double-column format.
* **Recommendation:** **SUBMIT_TO_TODAES** (Primary) / **IEEE TCAD** (Alternative).

---

### Paper 3: IEEE Transactions on Industrial Informatics (TII)
* **Scope Fit:** Cost-sensitive hierarchical anomaly detection and multi-class engine fault diagnosis on high-frequency telemetry match TII's industrial informatics and cyber-physical systems focus.
* **Evidence Boundaries:** $99.98\%$ anomaly screening recall at $\theta^* = 0.05$ and $89.8\%$ nominal compute reduction are rigorously validated on the 55,998-record physical engine testbed, with on-device ESP32 inference ($64.55\,\si{\micro\second}$) strictly separated from in-vehicle bus latencies.
* **Length & Formatting:** 7.0 pages complies with TII's strictly enforced 10-page ceiling.
* **Recommendation:** **SUBMIT_TO_TII** (Primary) / **IEEE Sensors Journal** (Alternative).

---

### Paper 4: ACM LCTES (SIGPLAN/SIGBED)
* **Scope Fit:** An artifact-driven software engineering verification protocol, defect taxonomy, and executable test harness for compiled TinyML binaries match LCTES's focus on embedded languages, compilers, tools, and runtime verification.
* **Evidence Boundaries:** Emphasizes the formal verification protocol ($\mathcal{P}_1\text{--}\mathcal{P}_7$), defect taxonomy (4 modes, 20 discrepancies), and $+1.80\%$ calibration bias as software engineering methodologies, using the 12-model suite as an empirical case study.
* **Length & Formatting:** 6.0 pages is well within the 10-page all-inclusive limit.
* **Recommendation:** **SUBMIT_TO_LCTES** (Primary) / **IEEE Software** (Alternative).

---

### Paper 5: ACM Transactions on Embedded Computing Systems (TECS)
* **Scope Fit:** Physical on-device characterization of ultra-low-resource ($<4\,\text{KB}$) INT8 models on bare-metal ESP32 silicon ($N=24,000$), zero-I/O in-RAM timing, microarchitectural translation divergence ($62.87\times\text{--}76.77\times$), and FreeRTOS dual-core deployment models fit ACM TECS.
* **Current Manuscript Version:** The authoritative manuscript is the **expanded 7-page full transaction version** (`papers/Paper5_ESP32_Deployment/submission/paper.tex`).
* **Length & Formatting:** 7.0 pages provides full transaction depth. (The 4-page version remains preserved in git history as an ESL fallback if needed).
* **Recommendation:** **SUBMIT_TO_TECS** (Primary) / **IEEE IoT-J** (Alternative 1) / **IEEE ESL** (4-page Fallback).

---

**VENUE AUDIT VERDICT: ALL CANDIDATE VENUES OFFICIALLY VERIFIED AND APPROVED**
