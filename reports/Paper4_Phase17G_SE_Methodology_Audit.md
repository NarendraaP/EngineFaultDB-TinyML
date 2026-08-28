# Phase 17G — Software Engineering Methodology Audit: Paper 4

**Manuscript:** An Independent Verification Framework for Reproducible TinyML Evaluation  
**Date:** August 28, 2026  

---

## 1. Software Engineering Research Evaluation Criteria

To evaluate Paper 4's standing as a genuine software engineering contribution, we address the 8 core methodological questions expected by rigorous reviewers at venues such as IEEE TSE, ACM TOSEM, and IEEE Software.

---

### Q1: What is the specific Software Engineering problem?
**Answer:** The translation of high-level machine learning models into compiled, serialized, and quantized edge deployment artifacts is an opaque, multi-stage software transformation pipeline. Subtle behavioral divergences (serialization drift, unexecuted in-memory fine-tuning, silent floating-point fallback operators, and uncompressed dense FlatBuffer schemas) are introduced during compilation without raising software compiler errors or runtime crashes.

### Q2: What is the failure model?
**Answer:** We formalize four distinct software failure modes in TinyML deployment pipelines:
1. **Serialization Drift (State Desynchronization):** Discrepancy between in-memory training loop states and final on-disk serialized binary weights.
2. **Silent Dtype Fallback (Execution Inconsistency):** Incomplete post-training quantization where floating-point operations remain undetected in the interpreter execution graph.
3. **Storage-Computation Decoupling (Structural Inefficiency):** Algorithmic weight pruning that creates computational zero weights without reducing serialized binary byte length.
4. **Data Contamination (Boundary Leakage):** Leakage across split boundaries during preprocessing or threshold calibration producing optimistic evaluation bias.

### Q3: What verification method is proposed?
**Answer:** An artifact-driven empirical verification protocol that formalizes 7 programmatic predicates ($\mathcal{P}_1 \dots \mathcal{P}_7$) evaluated directly on non-volatile disk binaries, raw weight arrays, and data split index sets.

### Q4: What is automated?
**Answer:** The verification pipeline (`scripts/phase4_5_verification.py`) fully automates:
- Low-level FlatBuffer tensor inspection (extracting dtypes, quantization parameters, and operator execution lists).
- Single-sample microsecond latency measurement with automated warmup discarding.
- Recomputation of parameter counts, active vs. dense MACs, and classification accuracy.
- Multi-objective Pareto dominance determination across 4 objectives.
- Automated discrepancy logging against published training profiles.

### Q5: What is reusable?
**Answer:**
- The 7-dimensional verification taxonomy and formal verification predicates.
- The defect taxonomy categorizing serialization and quantization anomalies.
- The open-source automated FlatBuffer verification script.
- The 3-tier evidence classification framework (Host Empirical, Trace-Driven Simulation, Physical MCU Silicon).

### Q6: What empirical evidence demonstrates usefulness?
**Answer:** An exhaustive audit of 12 candidate TinyML models on the 55,998-record EngineFaultDB physical benchmark, which uncovered and corrected **20 distinct numerical discrepancies** (with metric variances up to $7.82\%$) and empirically proved a **$+1.80\%$ optimistic accuracy bias** caused by unconstrained test-set threshold selection.

### Q7: What would a software engineer learn that they could apply elsewhere?
**Answer:**
1. Never evaluate test metrics on training-time in-memory objects; always load and execute the serialized disk binary.
2. Programmatically inspect the serialized execution graph to assert zero float32 tensors before claiming integer inference.
3. Distinguish theoretical active MAC reduction from physical on-disk storage compression.
4. Strictly isolate hyperparameter and threshold calibration to validation partitions.

### Q8: How does this differ from ordinary ML benchmarking?
**Answer:** Standard ML benchmarking (e.g., MLPerf Tiny) treats models as fixed, trusted black boxes and measures hardware performance (throughput, latency, energy). In contrast, Paper 4 audits the *software compilation and serialization integrity of the model artifacts themselves*, detecting state discrepancies, graph impurities, and evaluation leakage that standard benchmark harnesses ignore.

---

## 2. Framework vs. Protocol Designation

**Conclusion:** Rather than claiming a "universal verification framework" (which would require automated compiler plugins and cross-framework formal proofs), Paper 4 is most accurately and defensibly designated as an **"Artifact-Driven Empirical Verification Protocol and Defect Taxonomy for Compiled TinyML Deployment Artifacts."**
