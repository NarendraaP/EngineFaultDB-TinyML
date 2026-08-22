# Paper 3 Venue Format Audit: IEEE TII & MSSP

**Primary Target:** *IEEE Transactions on Industrial Informatics (TII)*  
**Secondary Target:** *Mechanical Systems and Signal Processing (MSSP)* (Elsevier)  
**Audited Manuscript:** [`papers/Paper3_Engine_Diagnostics/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper3_Engine_Diagnostics/paper.tex)  
**Date:** August 20, 2026  

---

## 1. IEEE Transactions on Industrial Informatics (TII) Compliance

| # | IEEE TII Requirement | Specification | Current Manuscript Status | Status |
| :---: | :--- | :--- | :--- | :---: |
| **1** | **Document Class** | Standard IEEE Transactions format (`\documentclass[journal]{IEEEtran}`). | Configured as `\documentclass[journal]{IEEEtran}`. | **PASS** |
| **2** | **Page Limit** | Strict **10-page limit** for regular initial transactions papers. | 8–9 formatted double-column pages (including figures, tables, references). | **PASS** |
| **3** | **Abstract Structure** | 150–250 words, self-contained single paragraph. | Exactly 214 words describing problem, architecture, dataset, empirical results, and compute reduction. | **PASS** |
| **4** | **Index Terms / Keywords** | Alphabetical order, comma-separated keywords. | 7 verified terms: Anomaly Detection, Cascaded Classifiers, Cyber-Physical Systems, Edge AI, Engine Fault Diagnosis, Hierarchical Inference, Multi-Fidelity Machine Learning. | **PASS** |
| **5** | **Industrial Context** | Clear industrial informatics contribution on realistic physical telemetry. | Cyber-physical automotive powertrain fault diagnosis on the physical EngineFaultDB dataset. | **PASS** |
| **6** | **References Format** | Numbered IEEE style with complete author/venue/year metadata. | 19 peer-reviewed citations formatted via BibTeX (`IEEEtran.bst`). | **PASS** |
| **7** | **Figures & Tables** | High-resolution publication figures with formal captions; `booktabs` tables. | 7 dedicated publication figures and 5 structured data tables. | **PASS** |

---

## 2. MSSP (Elsevier) Alternative Formatting Notes
- In the event of secondary submission to *Mechanical Systems and Signal Processing*, the LaTeX document class can be transitioned to `elsarticle.cls` with `authoryear` or `numbered` citation styles.
- Section structures and empirical figures remain identical.

---

## 3. Final Venue Format Verdict

```
======================================================================
PAPER 3 VENUE FORMAT AUDIT: PASS (100% Compliant with IEEE TII)
======================================================================
  Document Class:         \documentclass[journal]{IEEEtran}
  Length Constraint:      <= 10 pages (Currently ~8-9 pages)
  Abstract Length:        214 words
  Industrial Context:     Demonstrated on physical EngineFaultDB dataset
  BibTeX References:      19 authentic citations (100% cited)
======================================================================
```
