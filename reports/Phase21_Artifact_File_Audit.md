# Phase 21 — Artifact & Submission File Audit

**Project:** `d:\WiDe\EngineFaultDB-main`  
**Scope:** File Integrity, LaTeX Assets, Figures, Bibliographies, and Firmware Verification Across Papers 1–5  
**Date:** August 29, 2026  

---

## 1. Submission Package File Inventory

### Paper 1 (`papers/Paper1_QoS_Runtime/submission/`)
* `paper.tex` — Complete LaTeX manuscript source (383 lines) $\rightarrow$ **PRESENT**
* `paper.pdf` — Compiled PDF ($1.45\,\text{MiB}$, 7.0 pages, Tectonic Exit 0) $\rightarrow$ **PRESENT**
* `references.bib` — BibTeX bibliography database $\rightarrow$ **PRESENT**
* `Cover_Letter.md` — Submission cover letter for *IEEE TC* $\rightarrow$ **PRESENT**
* `README.md` — Reproducibility instructions $\rightarrow$ **PRESENT**
* `figures/phase5_policy_comparison.png` $\rightarrow$ **PRESENT**
* `figures/phase5_accuracy_vs_workload.png` $\rightarrow$ **PRESENT**
* `figures/phase5_f1_vs_workload.png` $\rightarrow$ **PRESENT**
* `figures/phase5_deadline_compliance_vs_workload.png` $\rightarrow$ **PRESENT**
* `figures/phase5_model_switch_rate.png` $\rightarrow$ **PRESENT**
* `figures/phase5_accuracy_compute_frontier.png` $\rightarrow$ **PRESENT**
* `figures/phase5_ablation.png` $\rightarrow$ **PRESENT**

---

### Paper 2 (`papers/Paper2_TinyML_Pareto/submission/`)
* `paper.tex` — Complete LaTeX manuscript source (369 lines) $\rightarrow$ **PRESENT**
* `paper.pdf` — Compiled PDF ($928.8\,\text{KiB}$, 7.0 pages, Tectonic Exit 0) $\rightarrow$ **PRESENT**
* `references.bib` — BibTeX bibliography database $\rightarrow$ **PRESENT**
* `Cover_Letter.md` — Submission cover letter for *ACM TODAES* $\rightarrow$ **PRESENT**
* `README.md` — Reproducibility instructions $\rightarrow$ **PRESENT**
* `figures/pareto_frontier.png` $\rightarrow$ **PRESENT**
* `figures/accuracy_vs_macs.png` $\rightarrow$ **PRESENT**
* `figures/accuracy_vs_model_size.png` $\rightarrow$ **PRESENT**
* `figures/accuracy_vs_latency.png` $\rightarrow$ **PRESENT**
* `figures/f1_vs_model_size.png` $\rightarrow$ **PRESENT**
* `figures/fp32_vs_int8_accuracy.png` $\rightarrow$ **PRESENT**

---

### Paper 3 (`papers/Paper3_Engine_Diagnostics/submission/`)
* `paper.tex` — Complete LaTeX manuscript source (389 lines) $\rightarrow$ **PRESENT**
* `paper.pdf` — Compiled PDF ($1.26\,\text{MiB}$, 7.0 pages, Tectonic Exit 0) $\rightarrow$ **PRESENT**
* `references.bib` — BibTeX bibliography database $\rightarrow$ **PRESENT**
* `Cover_Letter.md` — Submission cover letter for *IEEE TII* $\rightarrow$ **PRESENT**
* `README.md` — Reproducibility instructions $\rightarrow$ **PRESENT**
* `figures/engine_fault_architecture.png` $\rightarrow$ **PRESENT**
* `figures/decision_tree_topology.png` $\rightarrow$ **PRESENT**
* `figures/confusion_matrix_cascade.png` $\rightarrow$ **PRESENT**
* `figures/threshold_sweep.png` $\rightarrow$ **PRESENT**
* `figures/f1_radar.png` $\rightarrow$ **PRESENT**
* `figures/compute_vs_recall.png` $\rightarrow$ **PRESENT**

---

### Paper 4 (`papers/Paper4_TinyML_Verification/submission/`)
* `paper.tex` — Complete LaTeX manuscript source (328 lines) $\rightarrow$ **PRESENT**
* `paper.pdf` — Compiled PDF ($724.1\,\text{KiB}$, 6.0 pages, Tectonic Exit 0) $\rightarrow$ **PRESENT**
* `references.bib` — BibTeX bibliography database $\rightarrow$ **PRESENT**
* `Cover_Letter.md` — Submission cover letter for *ACM LCTES* $\rightarrow$ **PRESENT**
* `README.md` — Reproducibility instructions $\rightarrow$ **PRESENT**
* `figures/verification_pipeline.png` $\rightarrow$ **PRESENT**
* `figures/discrepancy_taxonomy.png` $\rightarrow$ **PRESENT**
* `figures/bias_evaluation.png` $\rightarrow$ **PRESENT**
* `figures/evidence_hierarchy.png` $\rightarrow$ **PRESENT**

---

### Paper 5 (`papers/Paper5_ESP32_Deployment/submission/`)
* `paper.tex` — Complete LaTeX manuscript source (454 lines, 7-page expanded version) $\rightarrow$ **PRESENT**
* `paper.pdf` — Compiled PDF ($697.7\,\text{KiB}$, 7.0 pages, Tectonic Exit 0) $\rightarrow$ **PRESENT**
* `references.bib` — BibTeX bibliography database $\rightarrow$ **PRESENT**
* `Cover_Letter.md` — Submission cover letter for *ACM TECS* $\rightarrow$ **PRESENT**
* `README.md` — Reproducibility instructions $\rightarrow$ **PRESENT**
* `figures/physical_pipeline.png` $\rightarrow$ **PRESENT**
* `figures/latency_distributions.png` $\rightarrow$ **PRESENT**
* `figures/params_vs_latency.png` $\rightarrow$ **PRESENT**
* `figures/host_vs_esp32.png` $\rightarrow$ **PRESENT**

---

## 2. Shared Code, Model & Hardware Assets Inventory

* **Physical Firmware Sources:** `phase5/firmware/` (PlatformIO, C++ sources, TFLM headers) $\rightarrow$ **VERIFIED**
* **Model FlatBuffers & Headers:** `models/tinyml/int8/` (`.tflite` binaries and `.h` byte arrays) $\rightarrow$ **VERIFIED**
* **Raw Hardware Serial Logs:** `phase5/measurements/esp32_raw_serial_benchmark.txt` $\rightarrow$ **VERIFIED**
* **Parsed Benchmark Datasets:** `phase5/measurements/esp32_full_benchmark.json` and `esp32_model_benchmark.csv` $\rightarrow$ **VERIFIED**
* **Engine Benchmark Dataset:** `EngineFaultDB_Final.csv` ($55,998$ records) $\rightarrow$ **VERIFIED**

---

**ARTIFACT AUDIT VERDICT: ALL SUBMISSION FILES PRESENT, VALIDATED, AND SYNCHRONIZED**
