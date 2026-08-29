# Phase 21 — Cross-Portfolio Related Paper Disclosure Matrix

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** Transparent Salami-Slicing Prevention & Portfolio Inter-Relationship Disclosure  
**Date:** August 29, 2026  

---

## 1. Objective

Because Papers 1–5 originate from the same broader TinyML research project and utilize the EngineFaultDB dataset and ESP32 silicon, this matrix explicitly defines the relationship between each pair of papers, detailing shared versus unique elements, and providing standard disclosure text for submission cover letters.

---

## 2. Cross-Paper Relationship Matrix

| Manuscript Pair | Shared Baseline Assets | Shared Hardware? | Shared Figures / Tables? | Primary Unique Contribution | Salami Slicing Risk | Recommended Disclosure |
|---|---|---|---|---|:---:|---|
| **Paper 1 ↔ Paper 2** | Model definitions (`student_a`, `mlp_14f`) | ESP32 latency bounds | **None** (Separate figures) | **P1:** Dynamic QoS runtime & multi-fidelity scheduling.<br>**P2:** Multi-objective static Pareto compression frontier. | **None (Orthogonal)** | Disclose P2 as complementary compression study. |
| **Paper 1 ↔ Paper 3** | EngineFaultDB dataset splits | ESP32 latency bounds | **None** (Separate figures) | **P1:** Deadline-aware dynamic execution under contention.<br>**P3:** Two-stage cost-sensitive anomaly screening cascade. | **None (Orthogonal)** | Disclose P3 as application-specific diagnostic study. |
| **Paper 1 ↔ Paper 4** | 12 candidate models | ESP32 latency bounds | **None** (Separate figures) | **P1:** Dynamic runtime systems architecture.<br>**P4:** Software engineering artifact verification protocol. | **None (Orthogonal)** | Disclose P4 as verification methodology study. |
| **Paper 1 ↔ Paper 5** | Model artifacts & ESP32 silicon | ESP32 physical latencies | **None** (P5 has full distributions) | **P1:** Multi-model runtime scheduling under contention.<br>**P5:** Pure empirical on-device hardware characterization ($N=24,000$). | **None (Orthogonal)** | Disclose P5 as hardware characterization companion. |
| **Paper 2 ↔ Paper 3** | EngineFaultDB dataset | ESP32 latency bounds | **None** (Separate figures) | **P2:** Pareto exploration of pruning vs. distillation.<br>**P3:** Cascaded hierarchical fault diagnostic architecture. | **None (Orthogonal)** | Disclose P3 as domain diagnostic application. |
| **Paper 2 ↔ Paper 4** | 12 model FlatBuffers | ESP32 latency bounds | **None** (Separate figures) | **P2:** Multi-objective compression design trade-offs.<br>**P4:** Defect taxonomy & verification test harness. | **None (Orthogonal)** | Disclose P4 as artifact verification framework. |
| **Paper 2 ↔ Paper 5** | Model FlatBuffers & ESP32 | ESP32 physical latencies | **None** (P5 has full distributions) | **P2:** Algorithmic compression Pareto frontier.<br>**P5:** Physical microcontroller execution & host translation gap. | **None (Orthogonal)** | Disclose P5 as empirical silicon profiling study. |
| **Paper 3 ↔ Paper 4** | EngineFaultDB dataset & models | ESP32 latency bounds | **None** (Separate figures) | **P3:** Domain engine fault diagnostic cascade.<br>**P4:** General SE artifact verification methodology. | **None (Orthogonal)** | Disclose P4 as verification methodology. |
| **Paper 3 ↔ Paper 5** | Stage-1 model artifact | ESP32 physical latencies | **None** (Separate figures) | **P3:** Hierarchical anomaly detection & cost calibration.<br>**P5:** Silicon-level latency distributions and memory analysis. | **None (Orthogonal)** | Disclose P5 as hardware benchmarking study. |
| **Paper 4 ↔ Paper 5** | 12 candidate models | ESP32 physical latencies | **None** (Separate figures) | **P4:** Executable verification protocol & defect taxonomy.<br>**P5:** Bare-metal latency profiling & microarchitecture analysis. | **None (Orthogonal)** | Disclose P5 as on-device characterization study. |

---

## 3. Standard Cover Letter Disclosure Text

To ensure full transparency with journal editors and program chairs, every cover letter includes the following standard disclosure:

> *"The candidate neural network models evaluated in this manuscript are part of a broader embedded TinyML research initiative on internal combustion engine diagnostics (EngineFaultDB). While complementary manuscripts explore [Dynamic Runtime Scheduling / Pareto Compression / Hierarchical Diagnostics / Software Verification / Physical Silicon Profiling], this manuscript addresses a distinct and self-contained research question with orthogonal contributions, separate experimental evaluations, and no overlapping manuscript text or duplicated figures."*

---

**DISCLOSURE AUDIT VERDICT: FULL TRANSPARENCY MAINTAINED, ZERO SALAMI SLICING RISK**
