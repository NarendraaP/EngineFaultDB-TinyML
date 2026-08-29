# Phase 18F — Paper 1 Hardware Evidence Integration Audit Report

> **Manuscript:** Paper 1 — QoS-Aware TinyML Runtime for Edge Fault Diagnostics  
> **Target Venue:** *IEEE Transactions on Computers (TC)*  
> **Audited File:** [`papers/Paper1_QoS_Runtime/submission/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper1_QoS_Runtime/submission/paper.tex)  
> **Compilation Status:** `TECTONIC_BUILD_PASS` (Exit Code 0, 1.45 MB PDF)  
> **Audit Verdict:** `READY_WITH_HARDWARE_EVIDENCE`  

---

## 1. Integrated Hardware Evidence Verification

The physical microcontroller evidence integrated into Paper 1 was verified against authoritative benchmark files ([`phase5/measurements/esp32_model_benchmark.csv`](file:///d:/WiDe/EngineFaultDB-main/phase5/measurements/esp32_model_benchmark.csv)):

| Model Identifier | Section Placement | Parameter / Byte Size | Physical Mean Latency | P95 Latency | P99 Latency | Max Latency | Feasibility Headroom ($D=5\,\text{ms}$) | Verified Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `student_a_8_4_int8` | Section VIII-D | 176 params / 3,208 B | $64.55\,\si{\micro\second}$ | $69.00\,\si{\micro\second}$ | $76.00\,\si{\micro\second}$ | $77\,\si{\micro\second}$ | $98.46\%$ | ✅ VERIFIED |
| `student_b_16_4_int8` | Section VIII-D | 328 params / 3,576 B | $72.96\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $84\,\si{\micro\second}$ | $98.32\%$ | ✅ VERIFIED |
| `mlp_12f_int8` | Section VIII-D | 380 params / 3,712 B | $76.77\,\si{\micro\second}$ | $83.00\,\si{\micro\second}$ | $90.00\,\si{\micro\second}$ | $90\,\si{\micro\second}$ | $98.20\%$ | ✅ VERIFIED |
| `mlp_14f_int8` | Section VIII-D | 412 params / 3,728 B | $89.90\,\si{\micro\second}$ | $95.00\,\si{\micro\second}$ | $101.00\,\si{\micro\second}$ | $102\,\si{\micro\second}$ | $97.96\%$ | ✅ VERIFIED |

---

## 2. Claim Scope & Boundary Audit

1. **Worst-Case Latency:** Paper 1 does not claim formal static WCET bounds; it cites the empirical maximum observed latency ($102\,\si{\micro\second}$) across $24,000$ physical inferences.
2. **Deadline Compliance:** Framed as **empirical feasibility headroom** ($97.96\%$ at $5\,\text{ms}$ and $99.90\%$ at $100\,\text{ms}$), not as a hard real-time safety guarantee.
3. **Execution Separation:** Section VIII-D and Section X explicitly distinguish **physical single-model execution** (`interpreter->Invoke()`) from **simulated dynamic multi-model QoS switching and contention**.
4. **Memory Accounting:** Tensor memory is cited as $916\,\text{Bytes}$ of static allocator-committed arena buffer with zero dynamic heap allocations.

---

## 3. Simulated Peer Review

> **Reviewer (Real-Time Systems Perspective):**  
> *"Does the paper properly separate simulated scheduler dynamics from physical on-chip model execution?"*  
> **Auditor Assessment:** **PASS.** Section VIII-D and Limitation 1 explicitly state that while isolated model inference is physically executed on 240 MHz ESP32 silicon, dynamic QoS state transitions and contention injection are evaluated via trace-driven simulation.
