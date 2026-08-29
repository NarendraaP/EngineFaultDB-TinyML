# Phase 18F — Paper 2 Hardware Evidence Integration Audit Report

> **Manuscript:** Paper 2 — Multi-Objective Pareto Optimization of TinyML Models for Edge Diagnostics  
> **Target Venue:** *ACM Transactions on Design Automation of Electronic Systems (TODAES)*  
> **Audited File:** [`papers/Paper2_TinyML_Pareto/submission/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/submission/paper.tex)  
> **Compilation Status:** `TECTONIC_BUILD_PASS` (Exit Code 0, 928 KB PDF)  
> **Audit Verdict:** `READY_WITH_HARDWARE_EVIDENCE`  

---

## 1. Integrated Hardware Evidence Verification

The physical microcontroller measurements integrated into Section V-F and Section VI of Paper 2 were verified:

| Model Identifier | Parameter Count | Binary Size | Physical Mean Latency | P95 Latency | P99 Latency | Max Latency | Host-to-ESP32 Ratio | Verified Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `student_a_8_4_int8` | 176 | 3,208 Bytes | $64.55\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $76.00\,\si{\micro\second}$ | $77\,\si{\micro\second}$ | $63.3\times$ | ✅ VERIFIED |
| `student_b_16_4_int8` | 328 | 3,576 Bytes | $72.96\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $84\,\si{\micro\second}$ | $74.5\times$ | ✅ VERIFIED |
| `mlp_12f_int8` | 380 | 3,712 Bytes | $76.77\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $90.00\,\si{\micro\second}$ | $90\,\si{\micro\second}$ | $76.8\times$ | ✅ VERIFIED |
| `mlp_14f_int8` | 412 | 3,728 Bytes | $89.90\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $101.00\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $62.9\times$ | ✅ VERIFIED |

---

## 2. Pareto Frontier Integrity Audit

1. **Frontier Preservation:** The primary optimization frontier remains strictly 3-dimensional: **Accuracy (maximize), Serialized Size (minimize), and Theoretical Active MACs (minimize)**.
2. **Deployment Validation Role:** Physical on-device latency is correctly categorized as a **secondary deployment validation dimension** that complements the primary mathematical frontier without modifying its non-dominated set.
3. **Speedup Calculation:** Knowledge distillation (`student_a`) achieves an observed physical latency reduction of:
   $$\Delta L = \frac{89.90 - 64.55}{89.90} \times 100\% = \mathbf{28.2\%}$$
   relative to the uncompressed `mlp_14f` baseline, appropriately scoped as an *observed latency reduction within the evaluated four-model set*.
4. **Ranking Comparison:** The audit confirmed that physical microcontroller latency scales strictly monotonically with parameter count ($176 \rightarrow 328 \rightarrow 380 \rightarrow 412$ params), providing cleaner arithmetic differentiation than host x86 measurements.

---

## 3. Simulated Peer Review

> **Reviewer (Design Automation / Embedded ML Perspective):**  
> *"Does the addition of physical latency disrupt the primary Pareto frontier or overclaim distillation benefits?"*  
> **Auditor Assessment:** **PASS.** Section V-F explicitly maintains the 3-objective primary frontier, introduces physical latency as secondary deployment validation, and scopes the 28.2% speedup strictly within the evaluated four-model set.
