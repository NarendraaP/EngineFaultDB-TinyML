# Paper 3: Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis

**Author:** Antigravity Research Team  
**Artifact Base:** Phases 1–3 Verified Datasets, Mode Selection Benchmarks, and Cascaded Evaluator  
**Primary Target Venue:** *IEEE Transactions on Industrial Informatics (TII)* (Regular Transactions Paper, $\le 10$ pages)  
**Secondary Target Venue:** *Mechanical Systems and Signal Processing (MSSP)* (Elsevier)  

---

## 1. Directory Structure

```
papers/Paper3_Engine_Diagnostics/
├── paper.tex            # Complete IEEE-style LaTeX manuscript (double-column)
├── references.bib       # 19 verified BibTeX literature citations (100% cited)
├── figures/             # 7 publication-ready figures
│   ├── cm_mode_a_dt5_binary_full.png
│   ├── confusion_matrix_mlp.png
│   ├── mode_a_roc_pr_curves.png
│   ├── qos_policy_frontier.png
│   ├── threshold_vs_accuracy.png
│   ├── threshold_vs_macro_f1.png
│   └── threshold_vs_trigger_rate.png
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
1. **Dataset Audit & Partitioning:**
   - Dataset: `EngineFaultDB_Final.csv` ($55,998$ records).
   - Stratified 3-way split: $40\%$ train ($22,399$), $40\%$ val ($22,399$), $20\%$ test ($11,200$) with `seed=42`.
2. **Mode A Binary Anomaly Filter Training:**
   - Execute `phase3_mode_selection.py` to train and evaluate Decision Tree ($d=5$) and Logistic Regression binary filters on 14-feature and 12-feature inputs.
   - Results exported to `results/mode_selection_metrics.csv`.
3. **Mode B Multiclass Diagnostician Baseline:**
   - Execute `baseline_benchmark.py` to train the reference 4-class MLP ($14 \rightarrow 16 \rightarrow 8 \rightarrow 4$).
   - Results exported to `results/baseline_metrics.csv`.
4. **Validation-Driven Threshold Calibration ($\theta \in [0.00, 1.00]$):**
   - Execute the sweep across 21 threshold operating points on `val` partition (`results/qos_threshold_sweep_val.csv`).
   - Optimal operating points ($\theta = 0.05$ to $\theta = 0.80$) selected.
5. **Held-Out Test Set Evaluation:**
   - Execute final cascade evaluation on held-out test partition (`results/qos_threshold_sweep_test.csv`).

---

## 3. Key Scientific Claims & Verified Artifact Cross-Reference

| Manuscript Claim | Authoritative Source Artifact | Verified Value |
| :--- | :--- | :---: |
| **Dataset Properties** | `reports/Dataset_Audit_Report.md` | $55,998$ records, 4 classes, split $40/40/20$ |
| **Mode A Performance** | `results/mode_selection_metrics.csv` (Row 4) | $99.08\%$ Acc, $99.60\%$ Anomaly Recall, $0.9923$ ROC-AUC |
| **Mode B Baseline** | `results/baseline_metrics.csv` (Row 4) | $74.66\%$ Acc, $0.7543$ Macro F1, $384$ MACs |
| **Hierarchical Cascade ($\theta=0.05$)** | `results/qos_threshold_sweep_test.csv` (Row 3) | $74.64\%$ Acc, $0.7541$ F1, $282.8$ expected MACs ($26.36\%$ reduction) |
| **Diagnostic Safety** | `results/qos_threshold_sweep_test.csv` (Row 3) | **2 missed anomalies out of 8,000** ($99.98\%$ recall) |
| **Operational Telemetry Saving** | Derived from Eq. (2) on $90\%$ healthy stream | $\mathbf{89.8\%}$ reduction ($\approx 39.1$ MACs/sample) |
| **Test-Set Isolation** | Validation calibration vs test evaluation | Zero test-set leakage |

---

## 4. LaTeX Compilation Instructions

To compile the manuscript into a PDF:

```bash
cd papers/Paper3_Engine_Diagnostics

# Standard pdflatex + bibtex build:
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Or using latexmk:
latexmk -pdf paper.tex
```
