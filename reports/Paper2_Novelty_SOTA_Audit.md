# ScholarMaster Novelty & SOTA Audit: Paper 2
**Title:** Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML  
**Audit Date:** August 20, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  

---

## 1. Defining the SOTA Axis
For Paper 2, SOTA is evaluated along the **TinyML Model Compression & Multi-Objective Pareto Benchmarking** axis:
- Comparative characterization of multiple compression paradigms on identical datasets and train/val/test splits.
- Multi-dimensional Pareto mapping across storage footprint, active arithmetic complexity (MACs), inference latency, and task accuracy.
- Low-level artifact verification of serialized FlatBuffers.

---

## 2. Competitive Landscape & Related Literature (2020–2026)

| Prior Work | Scope | Compression Techniques Compared | Verification Level | Key Gap Addressed by Paper 2 |
| :--- | :--- | :--- | :--- | :--- |
| **Han et al. (Deep Compression, 2016)** | Vision models (AlexNet, VGG). | Pruning + Quantization + Huffman coding. | Theoretical parameter counts. | Evaluated on large server models; did not examine sub-KB FlatBuffer packaging overhead on microcontrollers. |
| **MLPerf Tiny Benchmark (Banbury et al. 2021)** | Standardized TinyML benchmark suite. | Fixed INT8 reference models across 4 tasks. | Empirical latency & energy on boards. | Standardizes benchmark tasks but does not perform multi-paradigm Pareto frontier exploration for a single diagnostic task. |
| **MicroNet / TinyML Survey (Dutta et al. 2021, Sze et al. 2020)** | Broad architectural survey. | High-level synthesis of pruning, quantization, NAS. | Literature synthesis. | Aggregates reported numbers from disparate papers with incompatible splits and metric definitions. |
| **Recent Pruning/Distillation Papers (2024–2026)** | Algorithmic proposals for MCU compression. | Single paradigm (e.g., structured pruning or student distillation). | Isolated paradigm testing. | Typically compares the proposed algorithm against an uncompressed baseline, omitting a cross-paradigm Pareto analysis under identical data partitions. |

---

## 3. Novelty Gap Matrix

| Dimension | Existing Literature | Paper 2 (Our Work) | Genuine Research Difference? |
| :--- | :--- | :--- | :--- |
| **Evaluation Scope** | Single compression technique or high-level meta-analysis. | Unified, simultaneous 4-paradigm factorial evaluation on identical splits. | **Yes** — Completely eliminates split/scaler confounders across techniques. |
| **Artifact Inspection** | Assumes theoretical sparsity equals storage reduction. | Direct byte-level FlatBuffer graph audit uncovering zero-storage compression in standard TFLite pruning. | **Yes** — Crucial practical contribution exposing the disparity between mathematical sparsity and FlatBuffer deployment size. |
| **Pareto Dimensionality** | 2D trade-offs (Accuracy vs. Size or Accuracy vs. MACs). | 4D Pareto space (Accuracy, File Size, Active MACs, Latency) with strict non-domination proofs. | **Yes** — Identifies exact 6 non-dominated models spanning distinct edge operational niches. |

---

## 4. Novelty & SOTA Classification

- **Novelty Status:** **EMPIRICAL_CONTRIBUTION & NOVEL_EMPIRICAL_CHARACTERIZATION**  
  *Justification:* Paper 2 does not claim a new compression algorithm; rather, it provides a definitive, highly rigorous empirical characterization and Pareto mapping of 4 established compression paradigms for ultra-low-resource Edge AI.
- **SOTA Status:** **SOTA_WITHIN_SCOPE**  
  *Justification:* Sets a state-of-the-art benchmark for multi-objective compression trade-off analysis in sub-4KB TinyML deployments.
