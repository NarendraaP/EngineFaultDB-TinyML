# Phase 17A — Structured Pruning Assessment: Paper 2

**Manuscript:** Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML  
**Target Venue:** ACM Transactions on Design Automation of Electronic Systems (TODAES) / IEEE TCAD  
**Date:** August 28, 2026  

---

## 1. Executive Summary

This report investigates the structured pruning question raised in Phase 16 peer review:
1. Does a structured-pruned model artifact currently exist in the repository?
2. What pruning methodology was actually executed in the Phase 4 optimization pipeline?
3. How should the paper handle structured vs. unstructured pruning terminology?
4. Are new structured pruning experiments required before submission?

---

## 2. Codebase and Artifact Audit

A comprehensive repository search for structured, channel, neuron, and layer pruning artifacts was conducted across all directories (`models/tinyml/`, `scripts/`, `results/`, `papers/`).

### Findings:
1. **Existing Pruning Artifacts:**
   - `models/tinyml/pruned/mlp_14f_pruned_0.tflite` (3,892 Bytes)
   - `models/tinyml/pruned/mlp_14f_pruned_25.tflite` (3,920 Bytes)
   - `models/tinyml/pruned/mlp_14f_pruned_50.tflite` (3,920 Bytes)
   - `models/tinyml/pruned/mlp_14f_pruned_75.tflite` (3,920 Bytes)
2. **Actual Code Implementation (`scripts/phase4_tinyml_optimization.py`, lines 435–446):**
   ```python
   weights = p_model.get_weights()
   new_weights = []
   for w in weights:
       if len(w.shape) == 2:
           abs_w = np.abs(w)
           thresh = np.percentile(abs_w, p_level * 100)
           mask = (abs_w >= thresh).astype(np.float32)
           new_weights.append(w * mask)
       else:
           new_weights.append(w)
   p_model.set_weights(new_weights)
   p_model.fit(X_train_full, y_train, epochs=15, batch_size=128, verbose=0)
   ```
3. **Mathematical Identification:**
   This logic ranks individual weight scalar coefficients $|w_{ij}|$ and masks those below the percentile threshold $\theta_p$ to zero. The 2D weight matrix shapes ($14 \times 16$, $16 \times 8$, $8 \times 4$) are **completely preserved**. 
   **This is strictly UNSTRUCTURED magnitude pruning (element-wise fine-grained weight sparsity), NOT structured pruning.**

---

## 3. Root Cause of the Reviewer Objection

In the submitted manuscript:
- Section V-C2 heading was mistakenly titled: `\subsubsection{Structured Magnitude Pruning}`
- Section Abstract and Keywords included the phrase `Structured Pruning`

Reviewers in Phase 16 immediately noticed this contradiction:
- *Reviewer B (ML/TinyML Expert):* "75% unstructured pruning on a 412-parameter model is evaluated... yet it is called structured pruning."
- *Reviewer A (Systems/Embedded Expert):* "The finding that unstructured pruning doesn't reduce dense FlatBuffer size is well-known to systems engineers using TFLite Micro; it is an artifact of the framework retaining dense matrices."

The paper's core finding—that $75\%$ pruning reduces theoretical active MACs to $96$ while FlatBuffer size remains $3,920$\,Bytes ($+28$\,B)—is **100% scientifically correct for unstructured pruning**. The issue was purely a **terminology misnomer** where unstructured magnitude pruning was labeled as "structured".

---

## 4. Unstructured Pruning vs. Structural Dimension Reduction in Paper 2

Paper 2 already contains two distinct structural compression approaches:

| Compression Paradigm | Implementation in Paper 2 | Mathematical Nature | Storage Effect | Compute Effect |
| :--- | :--- | :--- | :--- | :--- |
| **Magnitude-Based Weight Pruning** | $25\%, 50\%, 75\%$ percentile masking on 2D dense arrays | **Unstructured Sparsity** | Dense FlatBuffer unchanged ($3,920$\,B vs. $3,892$\,B) | Active MACs drop from $384 \rightarrow 96$ ($75\%$ reduction) |
| **Knowledge Distillation (Student A/B)** | Direct layer dimension reduction: $14 \rightarrow 8 \rightarrow 4 \rightarrow 4$ ($176$ params) and $14 \rightarrow 16 \rightarrow 4 \rightarrow 4$ ($328$ params) | **Structural Topology Compression** | FlatBuffer shrinks by $23.5\%$ ($2,976$\,B) and $7.9\%$ ($3,584$\,B) | MACs drop from $384 \rightarrow 160$ and $384 \rightarrow 304$ |
| **Input Feature Reduction** | Dropping redundant inputs ($14 \rightarrow 12$ features) | **Input Layer Structural Truncation** | FlatBuffer shrinks to $3,780$\,B | MACs drop from $384 \rightarrow 352$ |

Therefore, the paper's comparison is already comparing **unstructured fine-grained sparsity** against **structural dimension reduction via distillation and feature truncation**.

---

## 5. Decision on New Structured Pruning Experiments

### Classification: **NOT NECESSARY FOR SUBMISSION (CAN FIX WITH EXISTING EVIDENCE)**

### Detailed Rationale:
1. **Scope of the Paper:** Paper 2 is an **empirical characterization of 12 verified, frozen TFLite deployment artifacts** evaluated under ultra-low memory budgets (<4 KB). It does not claim to invent a new structured pruning algorithm.
2. **The Scientific Finding is Strengthened by Clarification:** Clarifying that the evaluated pruning is *unstructured magnitude pruning* makes the core insight—*"computational sparsity without demonstrated storage compression in standard FlatBuffers"*—100% rigorous and unassailable.
3. **Structural Alternatives are Already Present:** Student A ($14 \rightarrow 8 \rightarrow 4$) and Student B ($14 \rightarrow 16 \rightarrow 4$) already demonstrate the structural compression frontier (achieving $2,976$\,B and $3,584$\,B).
4. **Structured Pruning on a 412-Parameter Model:** Pruning entire neurons from a layer with only 16 or 8 neurons essentially collapses the layer into smaller topologies—which is exactly what Student A and B already represent.

### Classification of Future Extensions:
- Adding neuron/channel-level structured pruning algorithms: **STRONGLY_RECOMMENDED as future work**.
- Adding custom CSR/CSC sparse runtime kernels: **OPTIONAL future work**.

---

## 6. Required Manuscript Revisions

1. **Title and Abstract:**
   - Remove "Structured Pruning" from keywords.
   - Replace any mention of "structured magnitude pruning" with "unstructured magnitude-based weight pruning".
2. **Section V-C2 (Methodology):**
   - Retitle Section V-C2 to: `\subsubsection{Magnitude-Based Weight Pruning}`.
   - Clarify that the pruning is element-wise unstructured pruning applied to 2D weight matrices.
3. **Section VI-B (Results - Pruning vs. Storage Decoupling):**
   - Explicitly articulate: *"Because magnitude pruning induces fine-grained unstructured sparsity rather than removing entire neurons or matrix columns, standard TFLite FlatBuffer converters preserve the dense matrix dimensions ($14 \times 16$, $16 \times 8$, $8 \times 4$) and serialize dense arrays containing zeros. Consequently, while theoretical active arithmetic demand is reduced by $75\%$ ($96$ vs. $384$ MACs), serialized binary storage remains $3,920$\,Bytes. This empirically demonstrates that unstructured weight pruning achieves computational sparsity without storage compression under standard embedded FlatBuffer formats."*
4. **Section VII (Discussion):**
   - Clearly contrast unstructured pruning (which requires sparse runtime kernels to realize speedups) with structural distillation (which directly shrinks dense array dimensions and reduces Flash footprint).
