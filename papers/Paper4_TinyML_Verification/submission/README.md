# Paper 4: An Independent Verification Framework for Reproducible TinyML Evaluation

**Author:** Antigravity Research Team  
**Artifact Base:** Phase 4.5 Independent Verification Scripts, Model FlatBuffers, and Discrepancy Audits  
**Primary Target Venue:** *IEEE Transactions on Software Engineering (TSE)* / *ACM Transactions on Software Engineering and Methodology (TOSEM)*  
**Secondary Target Venue:** *IEEE Transactions on Reliability*  

---

## 1. Directory Structure

```
papers/Paper4_TinyML_Verification/
├── paper.tex            # Complete IEEE-style LaTeX manuscript (double-column)
├── references.bib       # 18 verified BibTeX literature citations (100% cited)
├── figures/             # Verification case-study figures
│   ├── accuracy_vs_macs.png
│   ├── fp32_vs_int8_accuracy.png
│   └── pareto_frontier.png
├── tables/              # Data tables
├── submission/          # Self-contained submission bundle
└── README.md            # Comprehensive reproducibility documentation
```

---

## 2. Reproduction Pipeline

### 2.1. Environment and Dependencies
```bash
pip install tensorflow==2.15.0 scikit-learn==1.3.2 pandas numpy matplotlib
```

### 2.2. Execution Steps
1. **Model Binary Verification:**
   - Execute `scripts/phase4_5_verification.py` to independently inspect all 12 candidate `.tflite` FlatBuffer files, tensor data types, zero-weight counts, and single-sample host latencies.
   - Generates the authoritative reference profile: `results/tinyml_model_profile_verified.csv`.
2. **Discrepancy Audit Reproduction:**
   - Review `reports/Phase4_5_Independent_Verification.md` comparing initial training-time logs against verified disk FlatBuffers (resolving 20 numerical discrepancies).
3. **Threshold Leakage Bias Reproduction:**
   - Compare validation-isolated threshold sweep (`results/qos_threshold_sweep_val.csv`) against test-set direct optimization (`results/qos_threshold_sweep_test.csv`), confirming the $+1.8\%$ optimistic accuracy bias.

---

## 3. Key Scientific Claims & Verified Artifact Cross-Reference

| Manuscript Claim | Authoritative Source Artifact | Verified Value |
| :--- | :--- | :---: |
| **7-Dimension Taxonomy** | Table I in `paper.tex` | Data, Serialized, Quant, Sparsity, MAC, Timing, Routing |
| **20 Resolved Discrepancies** | `reports/Phase4_5_Independent_Verification.md` | 20 discrepancies (max $7.82\%$ in Macro F1) |
| **FULL_INT8 Graph Verification**| `results/tinyml_model_profile_verified.csv` | Exactly $0$ float32 tensors, $8$ int8 tensors |
| **Sparsity-Storage Decoupling** | `results/tinyml_model_profile_verified.csv` (Row 9) | $298$ zero weights ($73.34\%$), $96$ MACs, $3,920$\,B file size |
| **Threshold Leakage Bias** | `reports/Phase3_Scientific_Audit.md` (Sec. 3) | $\mathbf{+1.8\%}$ optimistic accuracy bias |
| **Dataset Stratified Isolation**| `reports/Dataset_Audit_Report.md` | $55,998$ physical records ($40/40/20$ split, $\text{seed}=42$) |
| **Hardware Boundary** | `phase5/hardware/esp32_interface.md` | Genuine ESP32 deployment classified as **FUTURE WORK** |

---

## 4. LaTeX Compilation Instructions

To compile the manuscript into a PDF:

```bash
cd papers/Paper4_TinyML_Verification

# Standard pdflatex + bibtex build:
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Or using latexmk:
latexmk -pdf paper.tex
```
