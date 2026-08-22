# Submission Cover Letter

**To:** Editor-in-Chief  
*IEEE Transactions on Computers*  
IEEE Computer Society  

**Date:** August 22, 2026  
**Manuscript Title:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention  
**Author(s):** Antigravity Research Team  
**Article Type:** Regular Research Paper  

Dear Editor-in-Chief and Editorial Board Members,

We are pleased to submit our original research manuscript entitled **\"QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention\"** for publication consideration in *IEEE Transactions on Computers*.

### Research Problem & Motivation
Deploying deep learning directly on resource-constrained microcontrollers (TinyML) is increasingly challenging in real-time embedded systems where CPU availability fluctuates dynamically due to interrupt service routines, peripheral I/O bursts, and concurrent RTOS threads. Conventional TinyML deployments execute a single static neural network model regardless of transient CPU contention, inevitably leading to missed real-time deadlines during workload spikes or suboptimal accuracy during idle periods.

### Key Contributions & Major Empirical Findings
1. **Dynamic Multi-Fidelity Runtime:** We develop a trace-driven, ground-truth-independent runtime that dynamically switches between verified Pareto-optimal model representations based on deadline headroom and estimated CPU contention.
2. **Deterministic Empirical Trace Evaluation:** Evaluating the runtime across 80 systematic configurations (5 deadlines $\times$ 4 synthetic workload levels $\times$ 4 QoS policies) over 11,200 held-out test frames demonstrates that our runtime achieves up to a **68.4% reduction in theoretical active arithmetic operations (MACs)** under high contention ($ vs. $ MACs) while preserving diagnostic macro F1 (.7563$).
3. **Rigorous Methodological Isolation:** We prove that model switching operates strictly on runtime operational telemetry without accessing ground-truth labels, preventing decision leakage.

### Venue Fit & Originality Declaration
*IEEE Transactions on Computers* is the premier venue for pioneering research at the intersection of computer architecture, real-time systems, and embedded computing. Our manuscript directly addresses real-time deadline management and runtime trade-offs for edge machine learning architectures.

This manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere. All experimental code, models, and simulation pipelines are open-sourced in our public repository.

Thank you for your time and editorial consideration.

Sincerely,  
**Antigravity Research Team**  
*QoS-Aware TinyML Research Platform*  
