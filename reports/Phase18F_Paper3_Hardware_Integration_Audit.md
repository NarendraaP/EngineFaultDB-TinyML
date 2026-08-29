# Phase 18F — Paper 3 Hardware Evidence Integration Audit Report

> **Manuscript:** Paper 3 — Hierarchical and Cascaded TinyML for Real-Time Engine Fault Diagnostics  
> **Target Venue:** *IEEE Transactions on Industrial Informatics (TII)*  
> **Audited File:** [`papers/Paper3_Engine_Diagnostics/submission/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/submission/paper.tex)  
> **Compilation Status:** `TECTONIC_BUILD_PASS` (Exit Code 0, 1.26 MB PDF)  
> **Audit Verdict:** `READY_WITH_HARDWARE_EVIDENCE`  

---

## 1. Integrated Hardware Evidence Verification

The physical microcontroller measurements integrated into Section VII-C and Section IX of Paper 3 were verified:

| Diagnostic Stage | Model Identifier | Parameters | Physical Mean Latency | P95 Latency | P99 Latency | Max Latency | Compute Equivalent | Verified Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Stage 1 (Screening)** | `student_a_8_4_int8` | 176 | $64.55\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $76.00\,\si{\micro\second}$ | $77\,\si{\micro\second}$ | $15,491.9\,\text{inf/sec}$ | ✅ VERIFIED |
| **Stage 2 (Diagnostic)**| `mlp_14f_int8` | 412 | $89.90\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $101.00\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $11,123.5\,\text{inf/sec}$ | ✅ VERIFIED |

---

## 2. Claim Scope & Boundary Audit

1. **Throughput Qualification:** The $15,491.9\,\text{inferences/sec}$ figure is explicitly defined as a **single-sample inference-rate compute equivalent** under pure compute-bound batch=1 conditions.
2. **System I/O Boundaries:** Section VII-C explicitly notes: *"Crucially, this metric represents isolated model inference compute capacity and is not an end-to-end sensor-to-decision throughput measurement; practical telemetry processing rates will be governed by physical ADC sampling intervals and CAN-bus communication bandwidth."*
3. **ECU & Vehicle Boundaries:** Limitation 7 explicitly states: *"While isolated single-sample inference latency was physically profiled on 240 MHz ESP32 silicon, complete on-vehicle bare-metal CAN-bus ECU integration, vehicle drive cycles, and safety certification remain future work."*
4. **Memory Accounting:** Correctly states that TFLM committed $916\,\text{Bytes}$ of working tensor arena buffer with zero dynamic heap allocations.

---

## 3. Simulated Peer Review

> **Reviewer (Industrial Informatics / Automotive Systems Perspective):**  
> *"Does the paper claim full vehicle ECU integration from generic evaluation board benchmarks?"*  
> **Auditor Assessment:** **PASS.** Section VII-C and Limitation 7 strictly bound the claims to isolated microcontroller model inference feasibility, explicitly disclaiming end-to-end CAN-bus throughput and safety certification.
