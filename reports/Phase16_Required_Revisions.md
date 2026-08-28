# Phase 16 — Required Revisions

**Date:** August 28, 2026
**Scope:** Papers 1-4

---

## Revision Priority Legend

| Priority | Description |
|----------|-------------|
| **CRITICAL** | Without this revision, the paper faces near-certain rejection |
| **HIGH** | Strongly impacts acceptance probability; reviewers will flag |
| **MEDIUM** | Improves paper quality; some reviewers may request |
| **LOW** | Polish items; unlikely to cause rejection alone |

## Revision Category Legend

| Category | Description |
|----------|-------------|
| **NO_REVISION_REQUIRED** | Section is adequate |
| **MINOR_REVISION** | Textual/framing changes only |
| **MODERATE_REVISION** | New analysis of existing data or expanded discussion |
| **MAJOR_REVISION** | New experiments with existing infrastructure |
| **NEW_EXPERIMENT_REQUIRED** | Requires hardware or new dataset acquisition |

---

## Paper 1 — QoS-Aware Multi-Fidelity Runtime

### CRITICAL Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 1.1 | Add variance estimates from 3+ random seeds for all 80 configurations | MODERATE_REVISION | 1 day |
| 1.2 | Reframe "68.4% compute reduction" to explicitly state this is model-selection (not per-model optimization) | MINOR_REVISION | 1 hour |

### HIGH Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 1.3 | Expand Related Work: add NestDNN, AnytimeNets, Once-for-All, MCUNet, recent 2023-2026 adaptive inference | MINOR_REVISION | 2 hours |
| 1.4 | Add paragraph explaining why 100% deadline compliance is trivially achieved (sub-us latency vs ms deadlines) | MINOR_REVISION | 1 hour |
| 1.5 | Add basic ESP32 or Cortex-M4 timing measurements (even minimal) | NEW_EXPERIMENT_REQUIRED | 1-2 weeks |
| 1.6 | Add at least one learned scheduling baseline (contextual bandit or RL-based model selector) | MAJOR_REVISION | 3-5 days |

### MEDIUM Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 1.7 | Evaluate on a second dataset (e.g., HAR, industrial vibration) | NEW_EXPERIMENT_REQUIRED | 1 week |
| 1.8 | Discuss practical significance of switching within 3.6% accuracy band | MINOR_REVISION | 1 hour |
| 1.9 | Address naming confusion: BALANCED model has higher F1 than HIGH_FIDELITY | MINOR_REVISION | 30 min |

### LOW Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 1.10 | Vary abstract sentence length; reduce repetition of "zero ground-truth leakage" | MINOR_REVISION | 30 min |
| 1.11 | Add Docker/container specification for reproducibility | MINOR_REVISION | 1 hour |

---

## Paper 2 — Empirical Pareto Frontier of Model Compression

### CRITICAL Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 2.1 | Remove or heavily caveat x86 host latency from Pareto frontier analysis | MODERATE_REVISION | 2 hours |
| 2.2 | Acknowledge that unstructured pruning not reducing FlatBuffer size is a known TFLite limitation, not a novel finding | MINOR_REVISION | 1 hour |

### HIGH Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 2.3 | Add structured pruning baselines (neuron/channel removal) | MAJOR_REVISION | 3-5 days |
| 2.4 | Deploy at least one model to physical MCU for latency/energy measurement | NEW_EXPERIMENT_REQUIRED | 1-2 weeks |
| 2.5 | Remove promotional language ("authoritative verification protocols", "remarkable fidelity") | MINOR_REVISION | 1 hour |
| 2.6 | Ablate KD hyperparameters (temperature T, alpha) | MAJOR_REVISION | 2-3 days |

### MEDIUM Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 2.7 | Justify why MLP was chosen over temporal architectures (LSTM, 1D-CNN) for time-series data | MINOR_REVISION | 1 hour |
| 2.8 | Expand Pareto frontier with more than 12 data points (e.g., NAS-generated topologies) | MAJOR_REVISION | 1 week |
| 2.9 | Provide confusion matrix to show which faults are confused | MODERATE_REVISION | 2 hours |

### LOW Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 2.10 | Tone down "dark knowledge" terminology for 412-parameter teacher | MINOR_REVISION | 30 min |
| 2.11 | Discuss the trivial 28B metadata overhead in proportion | MINOR_REVISION | 30 min |

---

## Paper 3 — Hierarchical Multi-Fidelity Engine Diagnostics

### CRITICAL Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 3.1 | Add multi-class Decision Tree (depth 5-10) and Random Forest baseline to demonstrate cascade necessity | MAJOR_REVISION | 2-3 days |

### HIGH Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 3.2 | Address temporal fault persistence: add simulated drive-cycle evaluation with contiguous fault blocks | MODERATE_REVISION | 2-3 days |
| 3.3 | Discuss DT probability calibration (Platt scaling / isotonic regression) | MODERATE_REVISION | 1-2 days |
| 3.4 | Remove promotional language ("astounding 89.8% reduction") | MINOR_REVISION | 30 min |
| 3.5 | Scale up Mode B model to demonstrate cascade value at meaningful MAC counts (>10K MACs) | MAJOR_REVISION | 1 week |

### MEDIUM Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 3.6 | Quantify false positive cost vs false negative cost in domain terms | MODERATE_REVISION | 1 day |
| 3.7 | Discuss switching overhead (wake-up tax for Mode B SRAM/Flash loading) | MODERATE_REVISION | 1 day |
| 3.8 | Add physical MCU energy profiling | NEW_EXPERIMENT_REQUIRED | 1-2 weeks |

### LOW Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 3.9 | Link Figures 1a/1b x-axes explicitly | MINOR_REVISION | 30 min |
| 3.10 | Tone down "monolithic inefficiency" and "squandering memory bandwidth" language | MINOR_REVISION | 30 min |

---

## Paper 4 — TinyML Verification Taxonomy

### CRITICAL Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 4.1 | Apply verification framework to 3+ diverse public model suites (CNN/audio/vision from MLPerf Tiny or EdgeImpulse) | NEW_EXPERIMENT_REQUIRED | 2-3 weeks |
| 4.2 | Run verified models on at least one physical MCU (Cortex-M4/M7) to report actual latency and SRAM | NEW_EXPERIMENT_REQUIRED | 1-2 weeks |

### HIGH Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 4.3 | Abstract verification predicates beyond TFLite (at minimum discuss ONNX/PyTorch Mobile applicability) | MODERATE_REVISION | 3-5 days |
| 4.4 | Consolidate 20 discrepancies to reflect actual distinct root causes (estimated ~10) | MODERATE_REVISION | 1 day |
| 4.5 | Reframe from "Scientific Verification Protocol" to "Empirical Verification Case Study" | MINOR_REVISION | 2 hours |
| 4.6 | Expand Related Work to cover MLOps, formal verification, and MLPerf literature | MINOR_REVISION | 2 hours |

### MEDIUM Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 4.7 | Provide CI/CD integration example (GitHub Actions, MLflow) | MODERATE_REVISION | 2-3 days |
| 4.8 | Discuss whether +1.80% bias generalizes or is dataset-specific | MINOR_REVISION | 1 hour |
| 4.9 | Tone down nomenclature: "Scientific Verification Protocol" to more modest framing | MINOR_REVISION | 30 min |

### LOW Revisions
| # | Revision | Category | Effort |
|---|----------|----------|--------|
| 4.10 | Add threat to validity section addressing single-project bias | MINOR_REVISION | 1 hour |

---

## Cross-Paper Required Revisions

### Hardware Validation (ALL PAPERS)
**Priority: CRITICAL for Papers 2 and 4, HIGH for Papers 1 and 3**

All four papers would significantly benefit from at least minimal physical MCU deployment. This is the single most impactful revision across the portfolio. A single ESP32 or STM32 board could serve all four papers:
- Paper 1: Runtime timing under FreeRTOS
- Paper 2: Real inference latency for Pareto dimension
- Paper 3: Energy measurement for cascade savings
- Paper 4: Hardware verification of serialized models

**Estimated effort:** 2-3 weeks for basic deployment + timing across all papers.

### Multi-Dataset Evaluation (Papers 1, 2, 4)
**Priority: HIGH**

Adding even one additional dataset (HAR-UCI, CIFAR-10 tiny subset, or public vibration dataset) would dramatically strengthen the generalizability argument for all papers.

### Statistical Rigor (Papers 1, 2)
**Priority: CRITICAL for Paper 1, HIGH for Paper 2**

Multiple random seeds (minimum 3) with reported variance/confidence intervals.

---

## Effort Estimation Summary

| Paper | CRITICAL Items | Total Effort (without hardware) | Total Effort (with hardware) |
|-------|---------------|--------------------------------|------------------------------|
| Paper 1 | 2 | 1-2 days | 2-3 weeks |
| Paper 2 | 2 | 1-2 days | 2-3 weeks |
| Paper 3 | 1 | 3-5 days | 2-3 weeks |
| Paper 4 | 2 | N/A (hardware required) | 4-5 weeks |
