# Paper 2: Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML

**Author:** Narendra Satish  
**Artifact Base:** Phases 1–4.5 Verified Datasets and Model FlatBuffers  
**Target Venue:** *IEEE Embedded Systems Letters (ESL)* (Letters format, $\le 4$ pages)  
**Alternative Venue:** *ACM Transactions on Design Automation of Electronic Systems (TODAES)*  

---

## 1. Directory Structure

```
papers/Paper2_TinyML_Pareto/
├── paper.tex            # Complete IEEE-style LaTeX manuscript (10pt double-column)
├── references.bib       # 20 verified BibTeX literature citations (100% cited)
├── figures/             # High-resolution publication figures
│   ├── pareto_frontier.png
│   ├── accuracy_vs_macs.png
│   ├── accuracy_vs_model_size.png
│   ├── accuracy_vs_latency.png
│   ├── f1_vs_model_size.png
│   └── fp32_vs_int8_accuracy.png
├── tables/              # Model profile data tables
├── submission/          # Self-contained submission bundle
└── README.md            # Comprehensive reproducibility documentation
```

---

## 2. Reproduction Pipeline

### 2.1. Environment and Dependencies
The pipeline requires Python 3.10+ and standard TinyML/data-science libraries:
```bash
pip install tensorflow==2.15.0 scikit-learn==1.3.2 pandas numpy matplotlib
```

### 2.2. Execution Steps
1. **Dataset Audit & Split:**
   - Source dataset: `EngineFaultDB_Final.csv` ($55,998$ physical engine operating records).
   - Stratified 3-way partition: $40\%$ train ($22,399$), $40\%$ val ($22,399$), $20\%$ test ($11,200$) with `seed=42`.
2. **Baseline Training & Feature Reduction:**
   - Execute `baseline_benchmark.py` to train FP32 14-feature and 12-feature MLP baselines.
3. **Quantization (PTQ FULL_INT8):**
   - Execute `phase4_quantization.py` to export 8-bit integer FlatBuffers using representative dataset calibration ($N=100$ train samples).
4. **Structured Magnitude Pruning:**
   - Execute `phase4_pruning.py` to train and fine-tune $0\%, 25\%, 50\%, 75\%$ sparse models.
5. **Knowledge Distillation:**
   - Execute `phase4_distillation.py` to distill knowledge from teacher into Student A ($8, 4$) and Student B ($16, 4$).
6. **Independent Verification & Pareto Extraction:**
   - Execute `scripts/phase4_5_verification.py` to parse all 12 disk `.tflite` binaries and generate `results/tinyml_model_profile_verified.csv`.

---

## 3. Authoritative Scientific Claims & Evidence Cross-Reference

| Manuscript Claim | Authoritative Source Artifact | Verified Value |
| :--- | :--- | :---: |
| **All 12 Model Metrics** | `results/tinyml_model_profile_verified.csv` | Exact match (28/28 verified) |
| **FULL_INT8 Verification** | `reports/Phase4_5_Independent_Verification.md` (Sec. 4 & 5) | $0$ float32 tensors, $8$ int8 tensors |
| **Pruning Decoupling** | `reports/Phase4_5_Independent_Verification.md` (Sec. 6) | $3,920$\,B storage vs. $96$ active MACs |
| **6 Pareto-Optimal Models** | `results/tinyml_model_profile_verified.csv` (`pareto_status`) | 6 optimal / 6 dominated |
| **Global Accuracy Leader** | `student_b_16_4_fp32` | $75.1429\%$ Acc, $3,584$\,B, $304$ MACs |
| **Minimal Compute Leader** | `pruned_mlp_14f_75pct` | $74.8214\%$ Acc, $3,920$\,B, **96 MACs** |
| **Minimal Storage Leader** | `student_a_8_4_fp32` | $71.6339\%$ Acc, **2,976 B**, $160$ MACs |
| **Test-Set Isolation** | `baseline_benchmark.py` & `phase4_5_verification.py` | $20\%$ held-out test split, `seed=42` |

---

## 4. LaTeX Compilation Instructions

To compile the manuscript into a camera-ready PDF:

```bash
cd papers/Paper2_TinyML_Pareto

# Standard pdflatex + bibtex build:
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Or using latexmk:
latexmk -pdf paper.tex
```
