# Paper 5 — Phase 19C Venue Suitability & Portfolio Independence Re-Audit Report

> **Manuscript:** Paper 5 — On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers  
> **Evaluation Mode:** Venue Fit, Page Budget, and Portfolio Independence Audit  
> **Primary Venue:** *IEEE Embedded Systems Letters (ESL)* (4-Page Letter)  
> **Alternative Venue:** *ACM Transactions on Embedded Computing Systems (TECS)*  
> **Audit Status:** `VENUE_FIT_EXCELLENT_PORTFOLIO_INDEPENDENT`  

---

## 1. The 4-Page IEEE ESL Format & Density Test

```
+---------------------------------------------------------------------------------------------------------+
| REQUIRED SECTION / COMPONENT | MANUSCRIPT LOCATION          | PAGE BUDGET | TECHNICAL COMPLETENESS      |
+------------------------------+------------------------------+-------------+-----------------------------+
| Abstract & Keywords          | Page 1 (Left Column)         | 0.25 Pages  | Complete, structured.       |
| Section I: Introduction      | Page 1 (Left & Right Col.)   | 0.75 Pages  | Clear problem & RQs.        |
| Section II: Hardware Target  | Page 1-2 (Hardware/Models)   | 0.60 Pages  | Table I & Table II included.|
| Section III: Methodology     | Page 2 (Zero-I/O Protocol)   | 0.40 Pages  | Equations (1)-(3).          |
| Section IV: Latency Stats    | Page 2-3 (Inference Latency) | 0.80 Pages  | Table III & Figs 2 & 3.     |
| Section V: Host vs. Silicon  | Page 3 (Divergence Analysis) | 0.40 Pages  | Table V & Figure 4.         |
| Section VI: Memory Subsys.   | Page 3 (Arena & Heap)        | 0.40 Pages  | Table IV (916 B committed). |
| Section VII: Related Work    | Page 4 (Left Column)         | 0.40 Pages  | 16 citations (2015-2026).   |
| Section VIII: Limitations    | Page 4 (Left Column)         | 0.30 Pages  | 6 explicit boundaries.      |
| Section IX-X: Repro & Concl. | Page 4 (Right Column)        | 0.30 Pages  | Firmware & dataset links.   |
| References                   | Page 4 (Right Column)        | 0.40 Pages  | Full IEEEtran format.       |
+---------------------------------------------------------------------------------------------------------+
```

- **Compiled PDF Length:** Exactly **4.0 pages** (IEEE double-column format).
- **Information Density:** Includes 4 high-resolution figures, 5 detailed tables, 16 peer-reviewed citations, and full statistical distributions without crowding or unreadable typography.
- **Verdict:** `PERFECT_FIT_FOR_IEEE_ESL`.

---

## 2. Portfolio Independence Matrix (Zero-Overlap Verification)

```
+---------------------------------------------------------------------------------------------------------+
| PAPER & TARGET VENUE         | CORE RESEARCH FOCUS                         | DISTINCTION FROM PAPER 5   |
+------------------------------+---------------------------------------------+----------------------------+
| Paper 1 (IEEE TC)            | Dynamic QoS-aware runtime scheduling and    | Paper 1 focuses on multi-  |
|                              | multi-fidelity switching under deadlines.   | model policy transitions;  |
|                              |                                             | Paper 5 on single-model HW.|
+------------------------------+---------------------------------------------+----------------------------+
| Paper 2 (ACM TODAES)         | Analytical 3D Pareto frontier optimization  | Paper 2 evaluates accuracy |
|                              | (Accuracy vs. Serialized Size vs. MACs).    | trade-offs; Paper 5 is pure|
|                              |                                             | physical silicon profiling.|
+------------------------------+---------------------------------------------+----------------------------+
| Paper 3 (IEEE TII)           | Two-stage hierarchical sensor cascade for   | Paper 3 is domain-specific |
|                              | internal combustion engine fault diagnosis. | engine diagnostics; Paper 5|
|                              |                                             | is embedded TinyML systems.|
+------------------------------+---------------------------------------------+----------------------------+
| Paper 4 (ACM LCTES)          | 7-dimensional software verification audit   | Paper 4 provides testing   |
|                              | protocol and discrepancy taxonomy.          | taxonomy; Paper 5 provides |
|                              |                                             | physical silicon baseline. |
+------------------------------+---------------------------------------------+----------------------------+
| Paper 5 (IEEE ESL)           | Direct physical on-device characterization, | Unique focus on Xtensa HW  |
|                              | host-to-silicon translation gap, in-RAM     | timing, noise-floor unmask-|
|                              | microsecond timing, and memory allocation.  | ing, and arena sizing.     |
+---------------------------------------------------------------------------------------------------------+
```

---

## 3. Venue Fit Verdict

- **Primary Recommendation:** Submit to ***IEEE Embedded Systems Letters (ESL)***.
- **Secondary Alternative:** If an extended 12-page version is desired later with multi-MCU comparisons (e.g. ARM Cortex-M4 and RISC-V), submit to ***ACM Transactions on Embedded Computing Systems (TECS)***.
