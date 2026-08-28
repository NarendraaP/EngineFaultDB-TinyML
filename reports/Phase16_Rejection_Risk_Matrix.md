# Phase 16 — Rejection Risk Matrix

**Date:** August 28, 2026
**Scope:** Papers 1-4

---

## Summary Matrix

| Paper | Title (Short) | Venue | Rev A | Rev B | Rev C | Rev D | Consensus | Survive? |
|-------|--------------|-------|-------|-------|-------|-------|-----------|----------|
| **1** | QoS Runtime | IEEE TC | BORDERLINE | WEAK_REJECT | BORDERLINE | WEAK_ACCEPT | BORDERLINE | BORDERLINE |
| **2** | TinyML Pareto | ACM TODAES | WEAK_REJECT | BORDERLINE | WEAK_REJECT | BORDERLINE | WEAK_REJECT | UNLIKELY_SURVIVE |
| **3** | Engine Diagnostics | IEEE TII | WEAK_REJECT | BORDERLINE | WEAK_ACCEPT | BORDERLINE | BORDERLINE | BORDERLINE |
| **4** | TinyML Verification | IEEE TSE | STRONG_REJECT | WEAK_REJECT | BORDERLINE | WEAK_ACCEPT | WEAK_REJECT | UNLIKELY_SURVIVE |

---

## Top Rejection Reasons by Paper

### Paper 1 — QoS Runtime (IEEE TC)

| Rank | Rejection Reason | Severity | Minimum Fix |
|------|-----------------|----------|-------------|
| 1 | No physical hardware validation | CRITICAL | Deploy on ESP32/Cortex-M4 with real timing measurements |
| 2 | Incremental novelty (NestDNN, BranchyNet precede this) | HIGH | Add learned scheduling baseline; reframe as empirical study |
| 3 | Single dataset, single domain, single seed | HIGH | Add second dataset + 3 random seeds with variance |

### Paper 2 — TinyML Pareto (ACM TODAES)

| Rank | Rejection Reason | Severity | Minimum Fix |
|------|-----------------|----------|-------------|
| 1 | x86 host latency is irrelevant for TinyML Pareto claims | CRITICAL | Deploy to physical MCU for latency dimension |
| 2 | Sparsity/storage finding is already known (TFLite limitation) | HIGH | Implement custom sparse kernel or acknowledge as known |
| 3 | Toy model scale (412 parameters) limits generalizability | HIGH | Add structured pruning comparison; scale up models |

### Paper 3 — Engine Diagnostics (IEEE TII)

| Rank | Rejection Reason | Severity | Minimum Fix |
|------|-----------------|----------|-------------|
| 1 | 384 MACs baseline is trivially small; cascade overhead may exceed savings | HIGH | Use larger baseline model or demonstrate on constrained 8-bit MCU |
| 2 | No multi-class DT/RF baseline | HIGH | Add standalone DT/RF multi-class comparison |
| 3 | Temporal fault persistence ignored | MEDIUM | Add drive-cycle simulation with contiguous fault blocks |

### Paper 4 — TinyML Verification (IEEE TSE)

| Rank | Rejection Reason | Severity | Minimum Fix |
|------|-----------------|----------|-------------|
| 1 | No physical MCU evaluation for a deployment verification paper | CRITICAL | Run audit on actual hardware targets |
| 2 | Single case study (12 MLPs, 1 dataset) | CRITICAL | Apply framework to 3+ diverse public model suites |
| 3 | Framework is a TFLite-specific script, not a generalizable methodology | HIGH | Abstract verification predicates to cover ONNX/PyTorch Mobile |

---

## Cross-Paper Risk Patterns

### Systemic Vulnerability: No Hardware Validation
**ALL four papers** lack physical microcontroller deployment. This is the single most common rejection vector across the entire portfolio. For papers targeting IEEE TC, ACM TODAES, IEEE TII, and IEEE TSE, the absence of any physical embedded measurement is a serious deficiency.

### Systemic Vulnerability: Single Dataset
All four papers use only EngineFaultDB. While this provides internal consistency, reviewers at different venues would independently flag the narrow evaluation scope.

### Systemic Vulnerability: Host Timing as Proxy
Papers 1, 2, and 4 use x86_64 host timing measurements, which are fundamentally unrepresentative of MCU execution characteristics.

### Systemic Vulnerability: Toy Model Scale
The models range from 176 to 412 parameters with 96-384 MACs. This is at the extreme low end even for TinyML. Reviewers may question whether findings generalize to typical TinyML workloads.

---

## Portfolio Vulnerability Ranking

| Rank | Paper | Primary Vulnerability | Risk Level |
|------|-------|----------------------|------------|
| 1 (Most Vulnerable) | **Paper 4** | Single case study + no hardware + TFLite-coupled | HIGH |
| 2 | **Paper 2** | x86 latency + known sparsity finding + toy scale | HIGH |
| 3 | **Paper 1** | No hardware + incremental novelty | MEDIUM-HIGH |
| 4 (Least Vulnerable) | **Paper 3** | Strongest domain framing but trivial MAC scale | MEDIUM |

---

## Rejection Probability Estimates

| Paper | Reject at First Review | Major Revision | Accept |
|-------|----------------------|----------------|--------|
| Paper 1 | 35% | 50% | 15% |
| Paper 2 | 55% | 35% | 10% |
| Paper 3 | 30% | 50% | 20% |
| Paper 4 | 60% | 30% | 10% |
