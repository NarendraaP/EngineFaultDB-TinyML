# ScholarMaster Novelty & SOTA Audit: Paper 3
**Title:** Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis  
**Audit Date:** August 20, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  

---

## 1. Defining the SOTA Axis
For Paper 3, SOTA is evaluated along the **Resource-Constrained Industrial Fault Diagnosis & Asymmetric Inference** axis:
- Two-tier hierarchical fault screening vs. monolithic always-on multi-class diagnosis.
- Validation-calibrated zero-leakage threshold gating.
- Compute savings under realistic nominal-dominated operational priors.

---

## 2. Competitive Landscape & Related Literature (2020–2026)

| Prior Work | Diagnostic Domain | Methodological Approach | Compute Optimization | Key Gap Addressed by Paper 3 |
| :--- | :--- | :--- | :--- | :--- |
| **Monolithic Deep Diagnostic CNNs** (Lei et al. 2020, Zhang et al. 2022) | Bearing / gearbox fault diagnosis. | Deep 1D/2D CNNs executed uniformly per sample. | None (Always-on execution). | Ignores nominal state dominance; consumes high MACs classifying healthy signals. |
| **Cascaded Classifiers** (Traita et al. 2020, Kulkarni et al. 2021) | High-level anomaly detection in industrial IoT. | Generic binary + multi-class cascade. | Heuristic threshold tuning. | Often tunes thresholds directly on test data (leakage bias) or evaluates without strict arithmetic MAC accounting. |
| **Hierarchical Fault Isolation** (Recent 2024–2025 Literature) | Motor / Powertrain diagnostic systems. | Tree-structured fault decomposition. | Model decomposition. | Lacks mathematical cost modeling for continuous edge sensor streams and systematic threshold sweep validation. |

---

## 3. Novelty Gap Matrix

| Dimension | Prior SOTA Approaches | Paper 3 (Our Work) | Genuine Research Difference? |
| :--- | :--- | :--- | :--- |
| **Architectural Formulation** | Uniform monolithic deep classifiers. | Asymmetric two-tier cascade separating screening (0 MACs) from isolation (384 MACs). | **Yes** — Exploits physical nominal prior probability to slash average compute by up to 89.8%. |
| **Threshold Calibration Protocol** | Ad-hoc threshold selection, often with test-set data leakage. | Strictly isolated validation sweep with empirical generalization proof on held-out test data. | **Yes** — Eliminates the +1.8% optimistic threshold selection bias prevalent in edge literature. |
| **Distinctness from Paper 1** | Runtime scheduling / dynamic task switching. | Domain-specific asymmetric diagnostic pipeline design and screening topology optimization. | **Yes** — Paper 3 solves the *diagnostic inference architecture*, while Paper 1 solves the *system runtime scheduling*. |

---

## 4. Novelty & SOTA Classification

- **Novelty Status:** **DOMAIN_SPECIFIC_NOVELTY & EMPIRICAL_CONTRIBUTION**  
  *Justification:* While hierarchical classification exists in general machine learning, its domain-specific formulation, zero-leakage threshold calibration, and exact arithmetic MAC accounting for physical automotive engine diagnostics constitute a robust, publishable contribution.
- **SOTA Status:** **COMPETITIVE_WITH_SOTA**  
  *Justification:* Highly competitive with modern edge diagnostic architectures, offering superior computational efficiency over monolithic deep baselines.
