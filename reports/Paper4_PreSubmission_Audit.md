# Paper 4 Pre-Submission Scientific Audit Report

**Manuscript Audited:** [`papers/Paper4_TinyML_Verification/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/paper.tex)  
**BibTeX Database:** [`papers/Paper4_TinyML_Verification/references.bib`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/references.bib)  
**Primary Authoritative Sources:** [`reports/Phase4_5_Independent_Verification.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase4_5_Independent_Verification.md), [`scripts/phase4_5_verification.py`](file:///d:/WiDe/EngineFaultDB-main/scripts/phase4_5_verification.py), [`results/tinyml_model_profile_verified.csv`](file:///d:/WiDe/EngineFaultDB-main/results/tinyml_model_profile_verified.csv), [`reports/Phase3_Scientific_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Phase3_Scientific_Audit.md)  
**Audit Date:** August 20, 2026  

---

## 1. Section-by-Section Scientific Audit

---

### A. Numerical Consistency
- **Audit Findings:** All $30$ quantitative claims and the complete $20$-item discrepancy resolution table in `paper.tex` match the authoritative records in `Phase4_5_Independent_Verification.md` with $100.0\%$ precision.
- **Detailed Log:** [`reports/Paper4_Numerical_Audit.md`](file:///d:/WiDe/EngineFaultDB-main/reports/Paper4_Numerical_Audit.md)
- **Status:** **PASS**

---

### B. Scientific Terminology & Claim Boundaries
- **WCET Audit:** Confirmed. Host single-sample execution times are explicitly demarcated as "empirical host inference latency on x86_64" and prohibited from being labeled as microcontroller WCET.
- **MAC Terminology:** Confirmed. Non-zero arithmetic operations are strictly qualified as "theoretical active MACs".
- **Pruning Storage Claim:** Confirmed. Magnitude pruning is characterized as "computational sparsity without demonstrated storage compression", explicitly highlighting the dense $3,920$\,B FlatBuffer file size.
- **Tone & Universal Claim Rules:** Confirmed. The manuscript avoids universal over-claims, using defensible formulations such as "provides a verification procedure", "detects inconsistencies", "supports reproducible reporting", and "distinguishes measured from inferred quantities".
- **Status:** **PASS**

---

### C. Dataset Integrity
- **Audited Parameters:** 3-way stratified partition ($40\%$ train, $40\%$ val, $20\%$ test, `seed=42`). Normalization scaling fitted strictly on training data.
- **Status:** **PASS**

---

### D. INT8 Quantization Graph Verification
- **Audit Findings:** Verified protocol for low-level FlatBuffer tensor inspection (`_get_ops_details()`, `get_tensor_details()`), requiring $0$ float32 tensors for `FULL_INT8` classification.
- **Status:** **PASS**

---

### E. Pruning & Sparsity Formalisms
- **Audit Findings:** The manuscript provides a clear 4-way distinction among Structural Sparsity, Theoretical Active MACs, Serialized Storage Compression, and Execution Speedup.
- **Status:** **PASS**

---

### F. Timing Protocols & Latency Profiling
- **Audit Findings:** Timing protocol auditing enforces high-resolution monotonic timing, warmup iteration discard ($N_{\text{warmup}} \ge 100$), single-sample input shape ($1 \times D$), and statistical distribution reporting (Mean, Median, P95, P99, Min, Max).
- **Status:** **PASS**

---

### G. Runtime Non-Leakage & Threshold Audit
- **Audit Findings:** Verifies that runtime controller receives strictly $(\mathbf{x}, \text{deadline}, \text{workload})$ with zero access to ground truth $y$. Confirms the $+1.8\%$ optimistic bias created by optimizing thresholds on test data.
- **Status:** **PASS**

---

### H. Reference Verification
- **Database Audited:** `papers/Paper4_TinyML_Verification/references.bib` ($16$ citations).
- **Authenticity Check:** All 16 references are verified as genuine, peer-reviewed publications across IEEE (*TSE*, *ICSE*, *Micro*, *Proc. IEEE*, *CAS*), ACM (*TOSEM*, *SenSys*), MLSys, NeurIPS, and JMLR. Zero hallucinated references.
- **Status:** **PASS**

---

### I. Figure and Table Verification
- **Table I (Taxonomy) & Table III (Discrepancies):** Accurately formulated from repository verification artifacts.
- **Figures 1–3:** Correctly mapped in `papers/Paper4_TinyML_Verification/figures/` with exact Pareto and quantization highlights.
- **Status:** **PASS**

---

### J. Reproducibility
- **Pipeline Scripts:** The verification suite (`scripts/phase4_5_verification.py`) and verified profile CSV are fully documented and reproducible.
- **Status:** **PASS**

---

### K. Paper Overlap & Scoping Isolation
- **Independence:** Paper 4 is strictly focused on verification methodology, software engineering formalisms, and artifact auditing. It does NOT overlap with the dynamic QoS scheduler (Paper 1), the compression Pareto trade-off study (Paper 2), or applied engine fault diagnosis (Paper 3).
- **Target Venues:** *IEEE Transactions on Software Engineering (TSE)*, *ACM Transactions on Software Engineering and Methodology (TOSEM)*, *IEEE Software*, or *MLSys Artifact Track*.
- **Status:** **PASS**

---

## 2. Final Pre-Submission Decision

```
======================================================================
FINAL AUDIT VERDICT: READY_FOR_SUBMISSION
======================================================================
  Manuscript:             papers/Paper4_TinyML_Verification/paper.tex
  BibTeX References:      papers/Paper4_TinyML_Verification/references.bib
  Evidence Map:           reports/Paper4_Evidence_Map.md
  Overlap Audit:          reports/Paper4_Overlap_Audit.md
  Numerical Audit:        reports/Paper4_Numerical_Audit.md (30/30 PASS)
  Pre-Submission Audit:   reports/Paper4_PreSubmission_Audit.md
======================================================================
```

The manuscript [`papers/Paper4_TinyML_Verification/paper.tex`](file:///d:/WiDe/EngineFaultDB-main/papers/Paper4_TinyML_Verification/paper.tex) has **passed the independent pre-submission scientific audit** and is fully ready for journal formatting and submission.
