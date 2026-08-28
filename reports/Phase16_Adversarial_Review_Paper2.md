# Comprehensive Adversarial Peer Review Report
**Manuscript**: Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML
**Target Venue**: ACM TODAES

## Reviewer A: Systems/Embedded Perspective
1. **Overall assessment**: The paper presents a solid engineering benchmark comparing multiple model compression techniques for an ultra-low-resource automotive application. However, it lacks fundamental systems novelty and primarily observes known artifacts of the standard TFLite Micro implementation rather than proposing new architectural or systemic solutions.
2. **Major strengths**: 
   - Strict adherence to sub-4KB and sub-400 MAC constraints, pushing the envelope of what is considered TinyML.
   - Good empirical demonstration of the disconnect between theoretical sparsity and actual serialized storage in FlatBuffers.
   - Comprehensive multi-objective profiling (accuracy, size, MACs, latency).
3. **Major concerns**: 
   - The finding that unstructured pruning doesn't reduce dense FlatBuffer size is well-known to systems engineers using TFLite Micro; it is a limitation of the software framework, not a scientific discovery.
   - Latency measurements on an x86_64 host are almost meaningless for MCU deployments. Cache hierarchies and superscalar architectures on x86 obscure the actual memory-bound nature of MCU inference.
   - Does not propose any custom sparse kernel or FlatBuffer schema optimization to solve the identified pruning issue.
4. **Minor concerns**:
   - The term "Theoretical Active MACs" is heavily used but hardware execution often pads loops for SIMD, making this metric overly theoretical.
   - Distillation models (Student A/B) are manually defined rather than searched, leaving the optimality of the topology questionable.
5. **Novelty assessment**: INCREMENTAL.
6. **SOTA/related-work assessment**: NOT_SOTA (relies on standard off-the-shelf tools).
7. **Experimental adequacy**: Weak. Evaluating embedded performance on an x86_64 CPU is a critical flaw.
8. **Methodological rigor**: High regarding dataset splits, low regarding hardware profiling.
9. **Statistical/evaluation concerns**: Using a single dataset (EngineFaultDB) limits the generalizability of the Pareto frontier.
10. **Reproducibility concerns**: Low. The authors promise full code release.
11. **Content/depth concerns**: Lacks depth in addressing the root cause of the storage inefficiency and proposing a fix.
12. **Language/presentation concerns**: Promotional language like "authoritative verification protocols" and "remarkable fidelity" should be toned down.
13. **Limitations that should be expanded**: The lack of physical MCU deployment must be explicitly stated as a critical limitation.
14. **Specific required revisions**: Must deploy to at least one Cortex-M or Xtensa MCU to measure actual cycle counts and energy.
15. **Final recommendation**: WEAK_REJECT.

## Reviewer B: ML/TinyML Perspective
1. **Overall assessment**: The authors methodically benchmark PTQ, pruning, and KD on a 4-class MLP. While the empirical rigor is appreciated, the machine learning techniques used are highly standard, and the resulting insights are largely expected for this scale of models.
2. **Major strengths**:
   - Clear ablation of floating-point vs FULL_INT8 quantization.
   - Excellent visualization of the 4D Pareto frontier.
   - Strong emphasis on preventing data leakage.
3. **Major concerns**:
   - The MLP baseline is extremely shallow (14->16->8->4). At this scale (412 parameters), the concept of "over-parameterized teacher" for KD is borderline nonsensical. 
   - 75% unstructured pruning on a 412-parameter model is a toy experiment. Structured pruning (e.g., removing neurons/channels) is standard practice for TinyML, yet only unstructured magnitude pruning was evaluated.
   - Feature reduction drops only 2 highly collinear features out of 14, which barely tests the paradigm.
4. **Minor concerns**:
   - The KD loss uses a fixed temperature (T=3.0) and alpha (0.5) without ablation.
   - Why only compare Student A and B? A systematic Neural Architecture Search (NAS) would be more appropriate for finding Pareto-optimal topologies.
5. **Novelty assessment**: NOVEL_EMPIRICAL_CHARACTERIZATION.
6. **SOTA/related-work assessment**: COMPETITIVE.
7. **Experimental adequacy**: Sufficient for the scope, but limited by the simplicity of the architecture.
8. **Methodological rigor**: Good adherence to standard practices.
9. **Statistical/evaluation concerns**: None major, metrics are sound.
10. **Reproducibility concerns**: Minimal, the FlatBuffer focus ensures portability.
11. **Content/depth concerns**: Needs a deeper dive into why unstructured pruning was chosen over structured pruning for an MCU context.
12. **Language/presentation concerns**: "Dark knowledge" is an exaggeration for a 412-parameter teacher.
13. **Limitations that should be expanded**: The scope of model topologies evaluated is too narrow to generalize claims about pruning vs KD.
14. **Specific required revisions**: Include structured pruning baselines. Ablate KD hyperparameters.
15. **Final recommendation**: BORDERLINE.

## Reviewer C: Domain/Application Perspective
1. **Overall assessment**: An interesting application of edge AI for engine fault diagnostics. However, the paper treats the physical signals purely as tabular data, abstracting away the time-series nature of continuous combustion telemetry.
2. **Major strengths**:
   - Use of a physically grounded dataset (EngineFaultDB) rather than synthetic benchmarks.
   - Clear operational classes corresponding to real engine faults.
   - Identification of physically redundant signals (AFR vs Lambda).
3. **Major concerns**:
   - Engine telemetry is inherently temporal. Using a static MLP that looks at single instances ignores temporal dynamics, vibration harmonics, and engine load phases.
   - The overall accuracy (~75%) seems insufficient for a production automotive system where false positives could trigger unnecessary maintenance or limp-home modes.
   - No discussion of varying engine RPMs and loads; dynamometer steady-state data does not reflect transient on-road behavior.
4. **Minor concerns**:
   - Is a sub-4KB model strictly necessary for this application? Modern automotive ECUs have megabytes of flash.
   - Missing domain context on the sampling rate of the sensors.
5. **Novelty assessment**: NOVEL_DOMAIN_APPLICATION.
6. **SOTA/related-work assessment**: SOTA_WITHIN_DEFINED_SCOPE.
7. **Experimental adequacy**: Weak due to the reliance on steady-state dynamometer data.
8. **Methodological rigor**: Treating time-series as tabular data is a methodological shortcut.
9. **Statistical/evaluation concerns**: F1 scores around 0.75 indicate severe misclassifications in some fault classes.
10. **Reproducibility concerns**: Good, data is public.
11. **Content/depth concerns**: Needs an explanation of why temporal models (LSTMs, 1D-CNNs) were completely ignored.
12. **Language/presentation concerns**: Clear and readable.
13. **Limitations that should be expanded**: Must explicitly address the steady-state nature of the dataset and the lack of temporal modeling.
14. **Specific required revisions**: Justify the use of an MLP over temporal architectures. Provide a confusion matrix to show which faults are being confused.
15. **Final recommendation**: WEAK_REJECT.

## Reviewer D: Methods/Reproducibility Perspective
1. **Overall assessment**: The paper shines in its commitment to deterministic evaluation and artifact-driven profiling. It serves as a highly reproducible benchmark, though it acts more like a technical report than a novel scientific paper.
2. **Major strengths**:
   - Explicit detailing of random seeds and split strategies.
   - Verification of exactly 0 float32 tensors in the INT8 graphs.
   - Complete tracking of exact byte sizes and MAC counts.
3. **Major concerns**:
   - Host latency measurements using `time.perf_counter_ns()` on x86 for a TinyML paper are completely invalid and misleading.
   - The paper claims to be an "Empirical Pareto Frontier" but 12 hand-picked models do not constitute a true frontier; it is merely a scatter plot of limited configurations.
   - "Authoritative verification protocols" is an empty buzzword.
4. **Minor concerns**:
   - The difference between 3920 B and 3892 B is 28 bytes of metadata, which is trivial but heavily emphasized.
   - Figures 1 and 2 are somewhat sparse with only 12 data points.
5. **Novelty assessment**: INCREMENTAL.
6. **SOTA/related-work assessment**: CANNOT_BE_ESTABLISHED (it's a benchmark of known methods).
7. **Experimental adequacy**: Strong in metrics, weak in hardware execution.
8. **Methodological rigor**: Host timing is a severe flaw.
9. **Statistical/evaluation concerns**: Generalization beyond EngineFaultDB is unproven.
10. **Reproducibility concerns**: Excellent. The specific claims are highly verifiable.
11. **Content/depth concerns**: Stop presenting framework metadata overhead as a scientific finding.
12. **Language/presentation concerns**: Hyperbolic language around standard procedures.
13. **Limitations that should be expanded**: The host latency limitation must be elevated to a central caveat.
14. **Specific required revisions**: Remove the x86 host latency from the Pareto frontier analysis entirely, or replace it with actual MCU timings.
15. **Final recommendation**: BORDERLINE.

---

## NOVELTY CHALLENGE
**What would a knowledgeable reviewer say is already known?** It is common knowledge that unstructured pruning in TFLite does not yield size reductions without specialized sparse formats, and that INT8 PTQ preserves accuracy well for MLPs. 
**Strongest prior-art objection:** The paper essentially runs standard TF-MOT tutorials on a specific tabular dataset.
**Is the contribution defensible?** Only as a highly rigorous, open-source engineering benchmark for a specific domain, but not as a novel methodology.

## SOTA CHALLENGE
**SOTA at what exact task, under what constraints?** Sub-4KB tabular classification on EngineFaultDB.
**Does it hold up?** Yes, within its very narrow constraints, but it doesn't establish a new SOTA technique, only measures existing ones.

## EXPERIMENTAL VALIDATION CHALLENGE
**Is evidence broad enough?** No. Only one dataset, one model class (MLP), and zero actual hardware deployments.
**Classify suggested experiments:**
- Real MCU deployment (Cortex-M4/M0): ESSENTIAL_BEFORE_SUBMISSION
- Structured pruning comparison: STRONGLY_RECOMMENDED
- Additional dataset: OPTIONAL_FUTURE_WORK

## HEADER/SECTION REVIEW
- **Abstract**: OVERSTATED (claims empirical host latency is a relevant Pareto objective for TinyML).
- **Introduction**: MOSTLY_JUSTIFIED.
- **Methodology**: FULLY_JUSTIFIED.
- **Results**: THIN (only 12 models evaluated).
- **Discussion**: OVERSTATED (drawing broad architectural implications from a 412-parameter model).

## REJECTION SIMULATION
**Top 3 most likely rejection reasons + minimum change:**
1. *Irrelevant Latency Metric (x86 profiling for TinyML)*. Change: Deploy to a physical Arduino Nano 33 BLE or Raspberry Pi Pico and measure microseconds.
2. *Lack of Novelty in Sparsity Findings*. Change: Implement a custom flatbuffer schema or sparse kernel to show how the 75% sparsity CAN be leveraged.
3. *Toy Model Size*. Change: Scale the baseline up slightly to allow for meaningful structured pruning, or evaluate on a time-series model (CNN/LSTM).

## META-REVIEW
**As area chair, determine:** UNLIKELY_SURVIVE (for a premier journal like TODAES, the lack of actual embedded hardware validation and the reliance on a single toy MLP is fatal).

## VENUE FIT
**Target**: ACM TODAES
**Fit**: POOR_FIT. TODAES expects deep architectural/systems design, novel hardware-software co-design, or significant CAD methodologies. This is an applied benchmarking paper, better suited for a specialized workshop or an application-focused journal.

## LIMITATIONS REVIEW
**Host Latency vs. MCU Timing**: CRITICAL (this invalidates a quarter of the Pareto frontier).
**Sparse Kernel Acceleration**: ADEQUATE.
**Model Topology Scope**: NEEDS_EXPANSION (needs to admit that MLPs are weak for time-series).

## LANGUAGE REVIEW
- **Promotional wording**: "authoritative verification protocols", "remarkable fidelity", "pure integer execution graphs".
- **Vague statements**: "dark knowledge" for a tiny network.
- **Unsupported emphasis**: Hyping the +28B metadata size increase as a major "structural insight".
