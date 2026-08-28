# Phase 16 — Adversarial Peer-Review Simulation: Paper 1

**Manuscript Title:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention
**Target Venue:** IEEE Transactions on Computers (TC)
**Review Date:** August 28, 2026

---

## Reviewer A — Systems / Embedded Systems Expert

### 1. Overall Assessment
The paper proposes a dynamic model-selection runtime for TinyML that switches among three pre-trained models based on workload contention and deadline pressure. While the systems framing is competent and the evidence tiering is commendable, the contribution is limited by the absence of any physical embedded platform validation and the simplistic nature of the synthetic contention model.

### 2. Major Strengths
- **Clear three-tier evidence hierarchy** that explicitly separates host simulation from MCU measurements, preventing overclaiming. This is a mature and responsible methodological choice.
- **Systematic 80-configuration sweep** (5 deadlines x 4 workloads x 4 policies) provides reasonable coverage of the parameter space.
- **Controlled ablation studies** (4 ablations) isolate the contribution of individual runtime components (workload awareness, deadline gating).
- **Practical Flash storage argument** is compelling: three sub-4 KB models fit comfortably in typical MCU Flash budgets.
- **Zero ground-truth leakage** is formally argued and audited.

### 3. Major Concerns
- **No physical hardware validation whatsoever.** For a paper targeting IEEE TC, the complete absence of any microcontroller measurement is a significant gap. Even a minimal ESP32 or Cortex-M4 deployment showing basic timing would strengthen the paper considerably.
- **Synthetic contention model is overly simplistic.** Multiplicative scaling factors (1.0x, 1.5x, 3.0x, 5.0x) with Gaussian jitter do not capture the bursty, non-stationary, priority-inversion patterns of real RTOS workloads. Real contention involves priority inheritance, interrupt latency jitter, DMA contention, and cache thrashing.
- **All models operate in sub-microsecond host latency range** (0.82-0.86 us base). At these timescales, even under 5x multiplier, inference completes in ~4 us. No realistic embedded deadline (5-100 ms) would ever be violated. The deadline compliance result of 100% across all 80 configs is therefore trivial and uninformative.
- **The "68.4% MAC reduction" is between two different models, not a runtime optimization.** The runtime simply selects the 96-MAC model instead of the 304-MAC model. This is model selection, not computational optimization.

### 4. Minor Concerns
- The paper uses "QoS-Aware" prominently but the QoS formalization is limited to threshold-based mode selection. There is no feedback control loop, no utility function optimization.
- Table 3 caption states "D = 5 ms" but the text discusses results across all 5 deadlines. Clarify which deadline the table represents.
- The term "Multi-Fidelity" may create confusion with multi-fidelity optimization literature.

### 5. Novelty Assessment
- Dynamic multi-fidelity model selection: **NOVEL_SYSTEM_INTEGRATION** (known concept applied to TinyML context)
- Four scheduling policies: **INCREMENTAL** (threshold-based mode selection rules are straightforward)
- Trace-driven simulation methodology: **ALREADY_KNOWN** (standard technique in embedded systems)
- Evidence tiering framework: **NOVEL_METHODOLOGY** (useful but minor)

### 6. SOTA/Related-Work Assessment
**CANNOT_BE_ESTABLISHED** — No comparison with existing adaptive inference systems (NestDNN, BranchyNet, anytime networks) under equivalent constraints.

### 7. Experimental Adequacy
The 80-configuration sweep is systematic but the synthetic nature of the workload model limits external validity. No hardware measurement makes it impossible to validate MAC reductions translate to real savings.

### 8. Methodological Rigor
Generally sound within simulation scope. Evidence tiering and non-leakage auditing are commendable. Fixed random seed is appropriate.

### 9. Statistical/Evaluation Concerns
- No confidence intervals or variance estimates across multiple runs.
- All results are single-seed deterministic runs without repetition.
- 100% deadline compliance across all configurations suggests the regime does not stress the system sufficiently.

### 10. Reproducibility Concerns
Code and models are open-sourced. Fixed seed documented. Reproduction command provided. **Adequate.**

### 11. Content/Depth Concerns
- Related Work is thin (~10 references). Missing NestDNN, anytime nets, model zoos.
- Discussion could be deeper on when/why switching provides diminishing returns.

### 12. Language/Presentation Concerns
- Generally well-written.
- Some abstract sentences are excessively long (>60 words).
- "Ensuring zero ground-truth leakage" is repeated too often.

### 13. Limitations That Should Be Expanded
- **NEEDS_EXPANSION:** Contention model simplicity — what RTOS phenomena are not captured?
- **NEEDS_EXPANSION:** Single-domain evaluation limits generalizability.
- **ADEQUATE:** Host timing limitations are well-documented.

### 14. Specific Required Revisions
1. Expand Related Work to include NestDNN, anytime prediction, recent adaptive inference (2023-2026).
2. Add a paragraph on why 100% deadline compliance is trivially achieved.
3. Reframe "68.4% compute reduction" as model-selection reduction, not per-model optimization.
4. Add variance estimates from at least 3 different random seeds.

### 15. Final Recommendation
**BORDERLINE**

---

## Reviewer B — Machine Learning / TinyML Expert

### 1. Overall Assessment
The paper addresses a relevant problem but the ML contribution is thin. The three models are pre-trained and fixed; the "runtime" is a lookup table mapping (workload, deadline) to one of three models. The ML aspects are inherited from prior work and not contributed here.

### 2. Major Strengths
- Relevant problem of dynamic model selection under resource constraints.
- Clear formalization of scheduling policies with explicit mathematical definitions.
- Evidence tiering is a valuable methodological contribution.
- Ablation studies demonstrate component contributions.

### 3. Major Concerns
- **The runtime is a deterministic lookup table.** No learning, no adaptation from history, no uncertainty-aware scheduling.
- **Only 3 models in the registry.** The decision space is trivially small.
- **Accuracy differences are negligible.** The 71.6%-75.2% range (3.6 pp span) questions the practical value of switching.
- **No comparison with any learned scheduling baseline** (RL-based selectors, bandit algorithms).

### 4. Minor Concerns
- BALANCED model (F1=0.756) exceeds HIGH_FIDELITY (F1=0.739), making the naming misleading.
- Host latencies of 0.82-0.86 us are within measurement noise at this scale.

### 5. Novelty Assessment
- Dynamic model selection for TinyML: **INCREMENTAL** (NestDNN, anytime prediction)
- Policy-based scheduling: **INCREMENTAL** (simple threshold rules)
- Macro F1 improvement via model switching: **NOVEL_EMPIRICAL_CHARACTERIZATION** (interesting but minor)

### 6. SOTA/Related-Work Assessment
**CANNOT_BE_ESTABLISHED** — No benchmark against prior dynamic selection methods.

### 7-14. [Consistent with above analysis]

### 15. Final Recommendation
**WEAK_REJECT**

---

## Reviewer C — Domain / Application Expert (Automotive)

### 1. Overall Assessment
The automotive framing is appropriate but surface-level. No engagement with ISO 26262, real ECU architectures, or real driving conditions.

### 2. Major Strengths
- Physical benchmark dataset rather than synthetic data.
- 4-class fault taxonomy is reasonable for proof-of-concept.

### 3. Major Concerns
- **No reference to automotive safety standards.** ISO 26262 and ASIL levels are fundamental.
- **No real ECU deployment.** AUTOSAR, CAN-bus timing, OSEK/VDX RTOS constraints are ignored.
- **Steady-state dynamometer data only.** No transient driving conditions.
- **75% accuracy is inadequate for production automotive diagnostics.**

### 4. Novelty Assessment
- Domain application: **INCREMENTAL**

### 15. Final Recommendation
**BORDERLINE**

---

## Reviewer D — Methods / Reproducibility Expert

### 1. Overall Assessment
Good software engineering practices: deterministic reproduction, open-source, fixed seeds, explicit evidence tiering, audited non-leakage. However, single-seed without repetition limits confidence.

### 2. Major Strengths
- Evidence tiering framework is a genuinely useful contribution.
- Non-leakage auditing is rigorous.
- Deterministic reproduction with single command is exemplary.

### 3. Major Concerns
- Single random seed without repetition.
- No formal verification of scheduler correctness beyond code auditing.
- No cross-validation or bootstrap confidence intervals.

### 15. Final Recommendation
**WEAK_ACCEPT**

---

## Novelty Challenge

### What is already known?
1. **Dynamic model selection** — NestDNN (Fang et al., MobiSys 2018) dynamically selects among model variants based on resources.
2. **QoS-aware scheduling** — Decades of real-time systems literature (Liu & Layland 1973, Lu et al. 2002).
3. **Model compression Pareto analysis** — MCUNet, TinyNAS, Once-for-All.
4. **Trace-driven simulation** — Standard embedded systems methodology.

### Strongest Prior-Art Objection
"The paper combines well-known adaptive inference with well-known QoS scheduling in a TinyML context. NestDNN (2018) already demonstrated dynamic variant selection for resource-constrained devices."

### Defensible?
**Partially.** The specific combination — non-leaking scheduling with verified Pareto models and evidence tiering — is competent systems integration. But novelty is incremental, not fundamental.

---

## SOTA Challenge

**CANNOT_BE_ESTABLISHED** — No external adaptive inference baseline comparison. The 68.4% reduction is relative to its own highest-compute model, not prior methods.

---

## Experimental Validation Challenge

| Suggested Experiment | Classification |
|---|---|
| Physical ESP32 deployment with real timing | STRONGLY_RECOMMENDED |
| Comparison with NestDNN or learned selector | STRONGLY_RECOMMENDED |
| Evaluation on a second dataset/domain | STRONGLY_RECOMMENDED |
| Multiple random seeds with variance | ESSENTIAL_BEFORE_SUBMISSION |
| Larger model registry (>3 models) | OPTIONAL_FUTURE_WORK |

---

## Rejection Simulation

### Most Likely Rejection Reason
"No hardware validation. For IEEE TC, trace-driven simulation alone with synthetic contention is insufficient."
- **Fix:** Add basic ESP32 timing measurements.

### Second Most Likely
"Incremental novelty. Dynamic model selection is well-established (NestDNN 2018, BranchyNet 2016)."
- **Fix:** Add learned scheduling baseline. Reframe as empirical systems study.

### Third Most Likely
"Single dataset, single domain, single seed."
- **Fix:** Add second dataset, report variance across 3+ seeds.

---

## Meta-Review (Area Chair)

### Consensus Strengths
Responsible evidence tiering, systematic evaluation, good reproducibility.

### Consensus Weaknesses
No hardware validation, simplistic contention, narrow evaluation, incremental novelty.

### Final Meta-Review
**BORDERLINE** — Would likely receive Major Revision at IEEE TC. Responsible methodology is appreciated, but hardware validation and stronger baselines are needed.

---

## Venue Fit
**IEEE Transactions on Computers: BORDERLINE**
Better fits: ACM TECS, IEEE IoT-J, or DATE/DAC conference.

---

## Revision Classification
**Overall: MAJOR_REVISION**

| Issue | Priority |
|---|---|
| Multiple random seeds with variance | CRITICAL |
| Expand Related Work (NestDNN, anytime nets) | HIGH |
| Reframe "68.4% compute reduction" | HIGH |
| Add hardware timing measurements | HIGH |
| Add learned scheduling baseline | MEDIUM |
| Add second dataset | MEDIUM |
