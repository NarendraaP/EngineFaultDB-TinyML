# Paper 2 Final Figure Audit

**Manuscript:** [`papers/Paper2_TinyML_Pareto/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/paper.tex)  
**Figure Directory:** [`papers/Paper2_TinyML_Pareto/figures/`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper2_TinyML_Pareto/figures/)  
**Date:** August 20, 2026  

---

## 1. Figure Inventory and Verification

| # | Figure Filename | Manuscript Ref | Caption / Scope | X-Axis Label & Units | Y-Axis Label & Units | Data Source | Verified? |
| :---: | :--- | :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | `accuracy_vs_macs.png` | Fig. 1 | Test Accuracy vs. Theoretical Active MACs across all 12 evaluated models. | Active MACs (count) | Test Accuracy ($\%$) | `tinyml_model_profile_verified.csv` | **PASS** |
| **2** | `accuracy_vs_model_size.png` | Fig. 2 | Test Accuracy vs. Serialized TFLite File Size (Bytes). | Model File Size (Bytes) | Test Accuracy ($\%$) | `tinyml_model_profile_verified.csv` | **PASS** |
| **3** | `fp32_vs_int8_accuracy.png` | Fig. 3 | Comparative classification accuracy between FP32 and verified FULL\_INT8 models. | Model Architecture | Test Accuracy ($\%$) | `tinyml_model_profile_verified.csv` | **PASS** |
| **4** | `pareto_frontier.png` | Fig. 4 | Multi-objective Pareto frontier mapping test accuracy, active MACs, file size, and latency. | Active MACs | Test Accuracy ($\%$) (Size/Color mapped) | `tinyml_model_profile_verified.csv` | **PASS** |

---

## 2. Unused Figures in Directory

- `accuracy_vs_latency.png` (Available in `figures/`, omitted from `paper.tex` to maintain strict 4-page IEEE ESL brevity).
- `f1_vs_model_size.png` (Available in `figures/`, omitted from `paper.tex` to maintain strict 4-page IEEE ESL brevity).

---

## 3. Scientific Integrity & Cross-Paper Reuse Check

- **Figure Provenance:** All 4 figures were generated directly from `results/tinyml_model_profile_verified.csv` during Phase 4.
- **Cross-Paper Reuse:** Figures `pareto_frontier.png`, `fp32_vs_int8_accuracy.png`, and `accuracy_vs_macs.png` are cross-referenced in Paper 4 strictly as audited artifact illustrations of the verification case study. This reuse is methodologically justified and documented.
- **Verdict:** **`PASS — All figures are high-resolution, accurately labeled, and scientifically valid.`**
