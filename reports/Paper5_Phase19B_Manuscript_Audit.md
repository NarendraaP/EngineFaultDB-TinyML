# Paper 5 — Phase 19B First Draft Manuscript Audit Report

> **Manuscript Title:** On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers  
> **Audited File:** [`papers/Paper5_ESP32_Deployment/submission/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper5_ESP32_Deployment/submission/paper.tex)  
> **PDF Output:** [`papers/Paper5_ESP32_Deployment/submission/paper.pdf`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper5_ESP32_Deployment/submission/paper.pdf) (655 KB, 4 pages, IEEE Double-Column)  
> **Compilation Status:** `TECTONIC_BUILD_PASS` (Exit Code 0)  
> **Audit Status:** `ALL_CHECKS_VERIFIED_PASS`  

---

## 1. Numerical & Quantitative Integrity Verification

Every numerical figure in `paper.tex` was audited against the authoritative datasets:

```
+---------------------------------------------------------------------------------------------------------+
| METRIC / VARIABLE          | AUDITED MANUSCRIPT VALUE      | AUTHORITATIVE SOURCE VALUE    | VERDICT    |
+----------------------------+-------------------------------+-------------------------------+------------+
| student_a Mean Latency     | 64.55 us                      | 64.55 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_a P95 Latency      | 69.00 us                      | 69.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_a P99 Latency      | 76.00 us                      | 76.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_a Max Latency      | 77.00 us                      | 77.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_b Mean Latency     | 72.96 us                      | 72.96 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_b P95 Latency      | 83.00 us                      | 83.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_b P99 Latency      | 83.00 us                      | 83.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| student_b Max Latency      | 84.00 us                      | 84.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_12f Mean Latency       | 76.77 us                      | 76.77 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_12f P95 Latency        | 83.00 us                      | 83.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_12f P99 Latency        | 90.00 us                      | 90.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_12f Max Latency        | 90.00 us                      | 90.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_14f Mean Latency       | 89.90 us                      | 89.90 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_14f P95 Latency        | 95.00 us                      | 95.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_14f P99 Latency        | 101.00 us                     | 101.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| mlp_14f Max Latency        | 102.00 us                     | 102.00 us (esp32_benchmark.csv)| ✅ EXACT   |
| Distillation Speedup       | 28.20% ((89.90-64.55)/89.90)  | 28.198%                       | ✅ EXACT   |
| Host-to-ESP32 Slowdown     | 62.87x to 76.77x              | 62.87x to 76.77x              | ✅ EXACT   |
| Tensor Arena Allocation    | 8,192 Bytes                   | 8,192 Bytes                   | ✅ EXACT   |
| Tensor Arena Committed     | 916 Bytes                     | 916 Bytes                     | ✅ EXACT   |
| Static Internal SRAM       | 61,944 Bytes (18.90%)         | 61,944 Bytes                  | ✅ EXACT   |
| Flash Firmware Footprint   | 330,153 Bytes (25.19%)        | 330,153 Bytes                 | ✅ EXACT   |
| Dynamic Heap Leakage       | 0 Bytes (25,200 runs)         | 0 Bytes                       | ✅ EXACT   |
| Single-Sample Compute Rate | 15,491.9 inf/sec (1/64.55us)  | 15,491.86 inf/sec             | ✅ EXACT   |
+---------------------------------------------------------------------------------------------------------+
```

---

## 2. Hardware Identity & Toolchain Audit

- **MCU Hardware Target:** Espressif ESP32-D0WD-V3 (Revision v3.1, Xtensa LX6 dual-core @ 240 MHz).
- **Memory Peripherals:** $4\,\text{MB}$ Quad-SPI Flash, $320\,\text{KB}$ on-chip SRAM, **0 PSRAM**.
- **USB Bridge Distinction:** Correctly specifies the WCH CH9102 USB-to-UART bridge on `COM7` as an external interface without conflating it with the core microcontroller silicon.
- **Kernel Definition:** Explicitly notes the portable reference C++ integer matrix multiplication kernel registered under `ref_fc`, avoiding misleading claims of ESP-NN vector assembly.

---

## 3. Claim Scope & Boundary Enforcement

1. **NO Formal WCET Claims:** The maximum observed latency ($102\,\mu\text{s}$) is explicitly framed as an *empirical maximum observed latency* across $24,000$ measured inferences under benchmark conditions, disclaiming static WCET bounds.
2. **NO End-to-End Throughput Claims:** Reciprocal latencies ($15,491.9\,\text{inf/sec}$) are qualified as *single-sample inference-rate compute equivalents*, with explicit disclaimers regarding sensor ADC acquisition and CAN-bus latency.
3. **NO Causal Frequency Claims:** Host slowdowns ($62.9\times\text{--}76.8\times$) are reported as *observed slowdown ratios* rather than single-factor CPU frequency effects.
4. **NO Overblown SOTA / Novelty Terms:** Zero instances of forbidden promotional phrasing ("first", "pioneering", "universal", "unprecedented").

---

## 4. Preservation of Portfolio Independence

The audit confirmed that Paper 5 maintains strict epistemological independence from Papers 1–4:
- **Paper 1 (QoS Runtime):** Dynamic scheduling simulation and multi-model switching state machines.
- **Paper 2 (Model Pareto):** Analytical 3D Pareto optimization (Accuracy vs. Serialized Size vs. Active MACs).
- **Paper 3 (Engine Diagnostics):** Domain-specific hierarchical cascade and physical sensor overlap physics.
- **Paper 4 (Verification Taxonomy):** 7-dimensional software verification protocol and discrepancy taxonomy.
- **Paper 5 (This Manuscript):** Direct physical on-device characterization, empirical latency distributions, host-to-silicon translation analysis, and memory arena layout on bare-metal Xtensa silicon.

---

## 5. First Draft Audit Verdict

### `READY_FOR_REVIEW`
The manuscript adheres strictly to all non-overclaiming rules, compiles with Exit Code 0 via Tectonic, and is fully grounded in audited empirical hardware evidence.
