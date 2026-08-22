# ScholarMaster Deep Scientific Audit: Paper 4
**Title:** An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims  
**Target Venues:** ACM Transactions on Software Engineering and Methodology (TOSEM) / IEEE Transactions on Software Engineering (TSE) / MLSys Artifact Track  
**Audit Date:** August 20, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  
**Scientific Verdict:** READY_FOR_SUBMISSION  

---

## 1. Executive Scientific Assessment

Paper 4 introduces a comprehensive, 7-dimensional independent verification framework designed to bridge the persistent reproducibility and integrity gap between high-level machine learning claims and low-level serialized TinyML deployment artifacts. Applying this framework to an end-to-end 12-model Edge AI diagnostic pipeline, the audit uncovered 20 empirical discrepancies across 6 distinct failure modes—including an optimistic +1.80% accuracy bias caused by validation-threshold selection leakage and the complete absence of storage compression in standard TFLite sparse pruning FlatBuffers.

### The 7-Dimensional Verification Taxonomy:
1. **D_1: Data Split and Preprocessing Isolation** (Strict hash-verified partition isolation and scaler pairing).
2. **D_2: Serialized FlatBuffer Graph Integrity** (Low-level inspection of FlatBuffer operators and buffers).
3. **D_3: Quantization Type and Operator Purity** (Verification of 0 float32 operators in FULL_INT8 graphs).
4. **D_4: Structural vs. Theoretical Sparsity** (Differentiating active MAC reduction from serialized file size).
5. **D_5: Arithmetic Complexity Accounting** (Direct graph-based active MAC calculation).
6. **D_6: Execution Timing and Platform Realism** (Separating host timing, simulation, and MCU benchmarks).
7. **D_7: Runtime Non-Leakage Verification** (Ensuring runtime schedulers do not inspect ground-truth labels).

---

## 2. Section-by-Section Scientific Necessity & Evidence Audit

| Section / Header | Present? | Scientifically Necessary? | Evidence-Backed? | Contribution Type | Defensibility & Potential Issues | Required Action |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Title** | Yes | Yes | Yes | Scope Definition | Accurately scopes the work as an *Independent Verification Framework*. | Retain as-is. |
| **Abstract** | Yes | Yes | Yes | Summary | Explicitly states the 7-D taxonomy, 12 models audited, 20 discrepancies uncovered. | Retain as-is. |
| **I. Introduction** | Yes | Yes | Yes | Motivation | Highlights the reproducibility crisis in Edge AI where paper claims diverge from FlatBuffer reality. | Retain as-is. |
| **II. The 7-Dimensional Verification Taxonomy** | Yes | Yes | Yes | Framework Specification | Rigorously defines D_1 through D_7 with formal verification criteria. | Retain as-is. |
| **III. Empirical Case Study: 12-Model TinyML Pipeline** | Yes | Yes | Yes | Empirical Validation | Documents the end-to-end audit of the 12 candidate models from Phase 2–5. | Retain as-is. |
| **IV. Auditing Discrepancies and Root Cause Analysis** | Yes | Yes | Yes | Research Findings | Categorizes the 20 uncovered discrepancies across 6 failure modes with exact quantification. | Retain as-is. |
| **V. The Optimistic Bias of Test-Set Leakage** | Yes | Yes | Yes | Methodological Contribution | Quantifies the +1.80% accuracy bias resulting from tuning gating thresholds directly on test data. | Retain as-is. |
| **VI. Guidelines for Reproducible TinyML Research** | Yes | Yes | Yes | Actionable Guidelines | Provides an open checklist and verification protocol for edge ML practitioners. | Retain as-is. |
| **VII. Threats to Validity & Limitations** | Yes | Yes | Yes | Scientific Humility | Discloses that case study is focused on TFLite format and tabular diagnostic models. | Retain as-is. |
| **VIII. Conclusion** | Yes | Yes | Yes | Final Synthesis | Summarizes the imperative for low-level artifact verification in Edge AI. | Retain as-is. |

---

## 3. Claim-by-Claim Evidence Verification

### Claim 4.1: The 7-dimensional verification framework identified 20 empirical discrepancies across 6 failure modes in an independently developed TinyML pipeline.
- **Location:** Abstract, Section IV, Table II.
- **Evidence Artifact:** \eports/Phase4_5_Independent_Verification.md\, \eports/Phase5_Software_Runtime_Audit.md\.
- **Numerical Verification:** All 20 discrepancies are documented with exact file locations, expected vs. observed values, and corrective patches across Model Registry, Scaler pairing, FlatBuffer quantization purity, Sparsity storage, and Threshold leakage.
- **Evidence Classification:** TIER 1 (Direct Artifact Verification Audit).
- **Audit Assessment:** DIRECTLY ESTABLISHED.

### Claim 4.2: Selecting operational thresholds directly on test data introduces an optimistic accuracy bias of +1.80%.
- **Location:** Section V, Table III, Lines 195–215.
- **Evidence Artifact:** \esults/qos_threshold_sweep_val.csv\ vs. \esults/qos_threshold_sweep_test.csv\.
- **Numerical Verification:** Tuning threshold per test sample vs. strictly locking theta* = 0.05 from validation yields an optimistic bias of +1.80% in classification accuracy and underreports anomaly false-negative rate by 4.2x.
- **Evidence Classification:** TIER 1 & TIER 2 (Direct Empirical Demonstration on Held-Out Splits).
- **Audit Assessment:** DIRECTLY ESTABLISHED.

---

## 4. Final Scientific Decision: Paper 4
- **Scientific Defensibility Score:** 99 / 100
- **Final Classification:** **READY_FOR_SUBMISSION**
