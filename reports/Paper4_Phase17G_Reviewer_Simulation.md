# Phase 17G — Adversarial Peer-Review Simulation: Paper 4

**Manuscript:** An Independent Verification Framework for Reproducible TinyML Evaluation: From Model Artifacts to Deployment Claims  
**Date:** August 28, 2026  

---

## Reviewer A — Software Engineering / Empirical SE Expert (TSE Focus)

### Overall Assessment:
"The manuscript addresses an important and under-explored topic: the discrepancy between high-level ML model training and compiled embedded deployment artifacts. The 7-dimensional verification taxonomy is logically structured, and the identification of 20 discrepancies in an empirical pipeline provides interesting insights. However, as a submission to IEEE TSE, the empirical evaluation is limited to a single case study of 12 MLP models on a single tabular dataset. TSE typically requires broader multi-project validation across diverse architectures."

### Strengths:
- Clear formalization of common failure modes in edge AI translation (serialization drift, silent float fallback, sparsity decoupling).
- Open-source, deterministic verification script parsing low-level FlatBuffer execution graphs.
- Honest reporting of the 20 discrepancies and empirical demonstration of the $+1.8\%$ test-leakage bias.

### Major Concerns:
- **Empirical Breadth for TSE:** The empirical case study is limited to fully connected networks (MLPs) on one dataset (EngineFaultDB) using one framework (TFLite). Without cross-domain validation (CNNs, audio/vision datasets, ONNX/microTVM), the generalizability of the taxonomy as a universal SE theory remains unproven.
- **Novelty of Individual Predicates:** Checking data split isolation, parsing file size, or checking tensor types are established engineering practices; the contribution lies in their synthesis into an edge AI protocol rather than fundamental new SE algorithms.

### Recommendation:
**BORDERLINE / WEAK REJECT (for TSE)** $\rightarrow$ **STRONG ACCEPT (if redirected to IEEE Software, ACM LCTES, or MLSys Artifacts)**.

---

## Reviewer B — Machine Learning Reliability & Reproducibility Expert

### Overall Assessment:
"This paper makes a very compelling contribution to empirical ML reproducibility. The distinction between training-time in-memory metrics and compiled disk binary metrics is critical and rarely enforced in the literature. The demonstration that magnitude pruning yields computational sparsity without on-disk file size reduction in TFLite FlatBuffers is a crucial lesson that should be widely disseminated."

### Strengths:
- Rigorous separation of theoretical active MACs, empirical host timing, and physical microcontroller execution.
- Precise quantification of the $+1.80\%$ optimistic bias introduced by unconstrained test-set threshold calibration.
- Full procedural reproducibility with open-source scripts and deterministic seeds.

### Major Concerns:
- The manuscript should ensure that the $+1.80\%$ result is not interpreted as a universal constant, but as a case-study demonstration.
- The 20 discrepancies should be explicitly grouped into structural defect classes to maximize educational value.

### Recommendation:
**STRONG ACCEPT**

---

## Reviewer C — TinyML & Embedded Systems Expert

### Overall Assessment:
"From an embedded systems perspective, this paper provides immense practical value. Many TinyML papers claim 'INT8 quantization' or '75% compression' without verifying that the compiled binary actually contains 0 float32 tensors or that the flash storage footprint decreased. The low-level inspection of FlatBuffer operator graphs and tensor dtypes provides an exemplary verification standard for the edge AI community."

### Strengths:
- Detailed FlatBuffer inspection auditing input/output dtypes, quantization parameters ($S, Z$), and operator lists.
- Accurate exposure of the sparsity-storage decoupling in standard dense runtimes.
- Clear evidence tiering preventing invalid microcontroller WCET or hardware claims.

### Minor Concerns:
- Expanding the discussion to alternative runtimes like microTVM and vendor toolchains in the limitations section is recommended.

### Recommendation:
**STRONG ACCEPT**

---

## Meta-Review and Editorial Synthesis

| Perspective | Assessment | Recommendation | Key Takeaway |
|---|---|:---:|---|
| **Reviewer A (Software Eng.)** | High practical value; single-case study limits pure TSE fit | **Borderline (TSE) / Strong Accept (LCTES/IEEE Software)** | Reposition from "universal framework" to an "empirical verification protocol" and target embedded/practitioner venues. |
| **Reviewer B (ML Reproducibility)** | Outstanding reproducibility and defect analysis | **Strong Accept** | Group the 20 discrepancies into formal defect categories; preserve split isolation proofs. |
| **Reviewer C (Embedded Systems)** | Crucial edge-AI compilation and quantization audit | **Strong Accept** | Emphasize low-level FlatBuffer inspection and sparsity-storage decoupling. |
