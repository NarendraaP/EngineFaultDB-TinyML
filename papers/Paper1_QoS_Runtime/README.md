# Paper 1: QoS-Aware Multi-Fidelity Runtime for Real-Time Embedded AI under Dynamic Workload Contention

**Author:** Narendra Satish  
**Artifact Base:** Phase 5 QoS-Aware Multi-Fidelity Runtime, Model Registry, and Trace Simulator  
**Primary Target Venue:** *IEEE Transactions on Computers (TC)* / *ACM Transactions on Embedded Computing Systems (TECS)*  
**Conference Target:** *IEEE Real-Time Systems Symposium (RTSS - Brief Presentations)*  

---

## 1. Directory Structure

```
papers/Paper1_QoS_Runtime/
├── paper.tex            # Complete IEEE-style LaTeX manuscript (double-column)
├── references.bib       # 16 verified BibTeX literature citations (100% cited)
├── figures/             # 7 publication-ready system figures
│   ├── phase5_ablation.png
│   ├── phase5_accuracy_compute_frontier.png
│   ├── phase5_accuracy_vs_workload.png
│   ├── phase5_deadline_compliance_vs_workload.png
│   ├── phase5_f1_vs_workload.png
│   ├── phase5_model_switch_rate.png
│   └── phase5_policy_comparison.png
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
1. **Model Registry Validation:**
   - Execute `phase5/runtime/model_registry.py` to load and verify the 12 candidate models from `results/tinyml_model_profile_verified.csv`.
2. **Runtime Execution & Policy Sweeps:**
   - Execute `python phase5/run_phase5_pipeline.py` to run the 80 configurations (5 deadlines $\times$ 4 workloads $\times$ 4 policies) across 11,200 held-out test frames using `seed=42`.
   - Results exported to:
     - `results/phase5_policy_comparison.csv`
     - `results/phase5_ablation_results.csv`
     - `results/phase5_model_switch_statistics.csv`
     - `results/phase5_runtime_traces.csv`
3. **Audit Verification:**
   - Execute `phase5/run_phase5_audit.py` to confirm zero ground-truth label leakage and test-set isolation.

---

## 3. Key Scientific Claims & Verified Artifact Cross-Reference

| Manuscript Claim | Authoritative Source Artifact | Verified Value |
| :--- | :--- | :---: |
| **Operational Modes** | `phase5/runtime/qos_runtime.py` | `FAST` ($160$ MACs), `BALANCED` ($96$ MACs), `HIGH_FIDELITY` ($304$ MACs) |
| **80 Experimental Configurations** | `results/phase5_policy_comparison.csv` | 5 deadlines $\times$ 4 workloads $\times$ 4 policies = 80 configurations |
| **68.4% Compute Reduction** | Derived from Eq. (4) ($(304-96)/304$) | **$68.421\%$ active MAC reduction** |
| **Diagnostic Macro F1 Retention**| `results/phase5_policy_comparison.csv` | $0.7390 \rightarrow \mathbf{0.7563}$ ($+0.0173$ F1 boost under `BALANCED`) |
| **Ablation Accuracy Gain** | `results/phase5_ablation_results.csv` (Ablation B) | $\mathbf{+3.21\%}$ ($0.7482$ vs. $0.7161$) over static minimal execution |
| **Runtime Ground-Truth Isolation**| `phase5/runtime/qos_runtime.py` | Zero access to ground-truth label $y$ during online inference |
| **Hardware Boundary** | `phase5/hardware/esp32_interface.md` | Physical ESP32 deployment classified as **FUTURE WORK** |

---

## 4. LaTeX Compilation Instructions

To compile the manuscript into a PDF:

```bash
cd papers/Paper1_QoS_Runtime

# Standard pdflatex + bibtex build:
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex

# Or using latexmk:
latexmk -pdf paper.tex
```
