# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Computers*  
IEEE Computer Society  

**Date:** August 28, 2026  
**Manuscript Title:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention  
**Corresponding Author:** Narendra Satish  
**Author Email:** narendresh.p@gmail.com  
**Article Type:** Regular Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit the original research manuscript entitled **"QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention"** for publication consideration in *IEEE Transactions on Computers*.

### Research Problem & Motivation
Deploying deep learning directly on resource-constrained microcontrollers (TinyML) is increasingly challenging in embedded systems where CPU availability fluctuates dynamically due to interrupt service routines, peripheral I/O bursts, and concurrent RTOS threads. Conventional TinyML deployments execute a single static neural network model regardless of transient CPU contention, inevitably leading to execution delays during workload spikes or suboptimal accuracy during idle periods.

### Key Contributions & Major Empirical Findings
1. **Trace-Driven QoS Runtime:** We develop a trace-driven, ground-truth-independent runtime that dynamically switches between verified Pareto-optimal model representations based on deadline headroom and estimated CPU contention.
2. **Empirical Trace Evaluation:** Evaluating the runtime across 80 systematic configurations (5 deadlines $\times$ 4 synthetic workload levels $\times$ 4 QoS policies) over 11,200 held-out test frames demonstrates that our runtime achieves **up to a 68.4\% reduction in theoretical active arithmetic operations (MACs) per inference frame** under high contention (96 vs. 304 MACs) while preserving diagnostic macro F1 ($0.7563$).
3. **Methodological Isolation:** Model switching operates strictly on runtime operational telemetry without accessing ground-truth labels, ensuring zero routing leakage.
4. **Hardware Scope & Boundaries:** All reported latencies are host empirical timings, and active compute savings are quantified in theoretical active MACs. Because single-sample execution latency is in the microsecond range ($<50\,\mu\text{s}$), 100\% deadline compliance is presented as a feasibility baseline relative to millisecond deadlines ($5$--$100$\,ms). Physical microcontroller validation (e.g., on ESP32 silicon under FreeRTOS preemption) is explicitly declared as planned future work.

### Declarations
- **Originality & Dual Submission:** [CONFIRM ORIGINALITY / NO SIMULTANEOUS SUBMISSION - The author confirms this manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere].
- **Reproducibility:** All models, runtime source modules, trace simulation harnesses, and empirical result logs are publicly accessible in our repository.

Thank you for your editorial review and consideration.

Sincerely,  
**Narendra Satish**  
*Email:* narendresh.p@gmail.com  
