# Comprehensive Adversarial Peer Review Report
**Manuscript**: Hierarchical Multi-Fidelity Inference for Resource-Constrained Engine Fault Diagnosis
**Target Venue**: IEEE TII

## Reviewer A: Systems/Embedded Perspective
1. **Overall assessment**: The paper proposes an asymmetric cascade (Decision Tree -> MLP) to reduce average computational load in edge diagnosis. The system-level intuition is sound, leveraging the extreme class imbalance of real-world operations, but the evaluation relies entirely on theoretical MAC reductions rather than actual hardware profiling.
2. **Major strengths**:
   - Practical alignment with real-world operating priors (engines are mostly healthy).
   - Clever use of an ultra-fast DT for the gating function (0 MACs, high anomaly recall).
   - Strict separation of validation data for threshold calibration.
3. **Major concerns**:
   - Theoretical MACs are a poor proxy for energy and latency in pipelined or parallel architectures. A branching DT structure often causes pipeline stalls and cache misses, which might offset the MAC savings.
   - The assumption that waking up a deeper neural network on demand is cost-free is false. Powering up SRAM banks and loading weights from Flash for Mode B incurs significant latency and energy penalties (the "wake-up tax").
   - 282 MACs vs 384 MACs is computationally trivial on modern ECUs. The overhead of the switching logic might consume more energy than the 100 MACs saved.
4. **Minor concerns**:
   - Baseline C (LR cascade) was dismissed quickly, but an LR might map better to SIMD hardware than a deeply branched DT.
   - The memory footprint holds both Mode A and Mode B concurrently; the paper doesn't heavily analyze the SRAM implications.
5. **Novelty assessment**: NOVEL_SYSTEM_INTEGRATION.
6. **SOTA/related-work assessment**: COMPETITIVE.
7. **Experimental adequacy**: Weak on the systems side (no MCU deployment).
8. **Methodological rigor**: Good statistical rigor, poor hardware realization.
9. **Statistical/evaluation concerns**: The MAC calculation assumes linear energy scaling, which is fundamentally incorrect for MCUs.
10. **Reproducibility concerns**: Low.
11. **Content/depth concerns**: Missing an analysis of the power state machine required to actually realize these savings.
12. **Language/presentation concerns**: "Astounding 89.8% reduction" is promotional and theoretical.
13. **Limitations that should be expanded**: The gap between MACs and actual joules/seconds on hardware.
14. **Specific required revisions**: Provide an analytical or empirical model of the switching overhead and memory loading costs between Mode A and Mode B.
15. **Final recommendation**: WEAK_REJECT.

## Reviewer B: ML/TinyML Perspective
1. **Overall assessment**: A clean, well-executed application of cascaded classification to an automotive dataset. The machine learning pipeline is robust, and the threshold tuning strategy is mathematically sound. However, the models themselves are extremely basic.
2. **Major strengths**:
   - Excellent use of PR-AUC to evaluate the heavily imbalanced anomaly detection task.
   - Rigorous threshold calibration ($\theta^*$) on the validation set preventing test leakage.
   - The DT d=5 achieves highly impressive screening metrics (99.6% recall).
3. **Major concerns**:
   - The overall accuracy of Mode B is only ~75%, heavily struggling with Class 2 and Class 3 (F1 ~0.50). Building a sophisticated cascade on top of a fundamentally weak base classifier seems premature.
   - Cascading an MLP after a DT is a known technique (e.g., in boosting). The ML contribution here is highly applied, not fundamentally novel.
   - Is it possible that a slightly larger DT or Random Forest could simply solve the whole problem (multi-class) with high efficiency, rendering the MLP Mode B unnecessary?
4. **Minor concerns**:
   - The confidence thresholding uses simple posterior probabilities from the DT. DT probabilities are notoriously uncalibrated. Did the authors apply Platt scaling or Isotonic regression?
   - The dataset scaling (MinMaxScaler) is applied globally? The text says fitted strictly on training data, which is correct.
5. **Novelty assessment**: INCREMENTAL.
6. **SOTA/related-work assessment**: COMPETITIVE.
7. **Experimental adequacy**: Sufficient for the claims made.
8. **Methodological rigor**: High.
9. **Statistical/evaluation concerns**: The baseline multi-class accuracy is too low to be considered solved.
10. **Reproducibility concerns**: Minimal.
11. **Content/depth concerns**: Missing a comparison against a pure DT/RF multi-class baseline.
12. **Language/presentation concerns**: Clear and precise.
13. **Limitations that should be expanded**: Discuss the poor performance on Classes 2 and 3 and how the cascade might behave if Mode B was a stronger model.
14. **Specific required revisions**: Add a multi-class Decision Tree and Random Forest baseline. Address probability calibration for the DT.
15. **Final recommendation**: BORDERLINE.

## Reviewer C: Domain/Application Perspective
1. **Overall assessment**: The paper accurately identifies a critical domain constraint: automotive telemetry is mostly nominal, and continuous deep inference wastes resources. The framing around the "monolithic inefficiency" is excellent for TII.
2. **Major strengths**:
   - Domain-aware cost modeling taking into account the prior probability of faults (P(Normal) = 0.90).
   - Clear identification of thermodynamic and mechanical redundancies in the feature set.
   - High anomaly recall (99.98%), which is critical for safety systems.
3. **Major concerns**:
   - As in Paper 2, treating continuous combustion dynamics as static tabular data is a severe limitation for a real ECU application. 
   - A 90% healthy assumption is realistic for a lifespan, but during a drive cycle, faults are persistent. If a misfire occurs, it stays misfiring. The cascade will just trigger Mode B continuously, degenerating to the monolithic baseline exactly when the system is under stress.
   - The assumption of a "continuous multi-sensor diagnostic stream" ignores the CAN bus sampling rates and ECU task scheduling (typically 10ms to 100ms loops). 
4. **Minor concerns**:
   - The cost of false positives (triggering Mode B needlessly) vs false negatives (missing a fault) is not quantified in domain terms (e.g., dollars, emissions).
   - No consideration of sensor degradation over time.
5. **Novelty assessment**: NOVEL_DOMAIN_APPLICATION.
6. **SOTA/related-work assessment**: SOTA_WITHIN_DEFINED_SCOPE.
7. **Experimental adequacy**: Lacking temporal domain validation.
8. **Methodological rigor**: Good.
9. **Statistical/evaluation concerns**: The independent sample assumption violates the physical reality of continuous engine operation.
10. **Reproducibility concerns**: Low.
11. **Content/depth concerns**: Must address the temporal persistence of faults.
12. **Language/presentation concerns**: Well written.
13. **Limitations that should be expanded**: Transients, dynamic loads, and fault persistence.
14. **Specific required revisions**: Model a simulated "drive cycle" with contiguous blocks of nominal and faulty data to show how the trigger rate behaves over time.
15. **Final recommendation**: WEAK_ACCEPT.

## Reviewer D: Methods/Reproducibility Perspective
1. **Overall assessment**: The empirical evaluation is tightly controlled and highly transparent. The analysis of the gating threshold's sensitivity is particularly well executed.
2. **Major strengths**:
   - Superb data hygiene (strict isolation of validation set for thresholding).
   - The cost model (Eq 2) is clearly defined and empirically validated.
   - All code and artifacts are claimed to be available.
3. **Major concerns**:
   - The paper overstates its contribution as a "genuinely new diagnostic method". It is an application of standard early-exit/cascading logic to a specific dataset.
   - The reduction from 384 MACs to 282.8 MACs is mathematically correct but practically irrelevant. These numbers are so small that the overhead of the Python/C++ wrapper calling the models likely dwarfs the inference itself.
4. **Minor concerns**:
   - Figure 1a and 1b x-axes should be explicitly linked.
   - Baseline B (Mode A only) has 41.76% accuracy, which is just the binary classification performance mapped to multi-class. It's a bit of a strawman baseline.
5. **Novelty assessment**: INCREMENTAL.
6. **SOTA/related-work assessment**: SOTA_PROVEN (on this specific dataset).
7. **Experimental adequacy**: Strong methodology, limited scope.
8. **Methodological rigor**: Very high.
9. **Statistical/evaluation concerns**: None.
10. **Reproducibility concerns**: None.
11. **Content/depth concerns**: The absolute scale of the compute being saved is too small to matter.
12. **Language/presentation concerns**: Tends to dramatize simple concepts (e.g., "monolithic inefficiency").
13. **Limitations that should be expanded**: The scale of the MACs.
14. **Specific required revisions**: Scale up the Mode B model to something that actually requires optimization (e.g., >100K MACs), otherwise the cascade solves a non-problem.
15. **Final recommendation**: BORDERLINE.

---

## NOVELTY CHALLENGE
**What would a knowledgeable reviewer say is already known?** Cascading a fast, cheap classifier (like a cascade of rejectors) before a heavy classifier is exactly how Viola-Jones worked in 2004. 
**Strongest prior-art objection:** This is just a domain-specific application of the standard BranchyNet/early-exit paradigm.
**Is the contribution defensible?** Yes, because the specific hybridization of a non-linear Decision Tree for anomaly screening gating a deep MLP is well-tailored and rigorously evaluated on an industrial dataset.

## SOTA CHALLENGE
**SOTA at what exact task, under what constraints?** Compute-efficient classification on EngineFaultDB.
**Does it hold up?** Yes, the mathematical demonstration of the savings under 90% nominal priors is compelling.

## EXPERIMENTAL VALIDATION CHALLENGE
**Is evidence broad enough?** No. 
**Classify suggested experiments:**
- Multi-class Decision Tree/Random Forest baseline: ESSENTIAL_BEFORE_SUBMISSION
- Continuous time-series "drive cycle" simulation: STRONGLY_RECOMMENDED
- Physical MCU energy profiling: STRONGLY_RECOMMENDED

## HEADER/SECTION REVIEW
- **Abstract**: MOSTLY_JUSTIFIED.
- **Introduction**: FULLY_JUSTIFIED.
- **Methodology**: FULLY_JUSTIFIED.
- **Results**: FULLY_JUSTIFIED.
- **Discussion**: THIN (needs to address fault persistence and switching overhead).

## REJECTION SIMULATION
**Top 3 most likely rejection reasons + minimum change:**
1. *Trivial scale of the problem*. 384 MACs is essentially free on modern hardware. Change: Either use a much larger baseline model (e.g., 1D-CNN) or demonstrate savings on a deeply constrained ultra-low-power 8-bit micro.
2. *Lack of a pure DT multi-class baseline*. Change: Add a multi-class DT baseline. If a depth-10 DT gets 75% accuracy with 10 compares, the whole hierarchy is moot.
3. *Ignores temporal persistence*. Change: Add a time-series evaluation segment showing contiguous fault states.

## META-REVIEW
**As area chair, determine:** BORDERLINE. The methodology is extremely sound and the writing is clear, but the scale of the neural network (384 MACs) makes the elaborate cascade seem like massive overkill. It requires major revisions to prove the cascade is actually necessary.

## VENUE FIT
**Target**: IEEE TII (Transactions on Industrial Informatics)
**Fit**: BORDERLINE. TII loves cyber-physical systems and industrial AI, so the domain is a perfect fit. However, TII also demands robust, practical implementations. The lack of hardware validation and the use of static tabular data for a dynamic physical system are significant detriments.

## LIMITATIONS REVIEW
**Theoretical Compute vs. Hardware**: CRITICAL.
**Static Sensor Topology**: ADEQUATE.
**Controlled Dynamometer**: NEEDS_EXPANSION (must link to temporal persistence).

## LANGUAGE REVIEW
- **Promotional wording**: "astounding 89.8% reduction", "squandering memory bandwidth" (384 MACs squanders nothing).
- **Vague statements**: None major, metrics are precise.
- **Unsupported emphasis**: The theoretical cost model is presented as a guaranteed hardware saving.
