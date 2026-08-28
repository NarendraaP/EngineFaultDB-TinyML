# Phase 17C — Workload and Contention Model Audit: Paper 1

**Manuscript:** QoS-Aware Multi-Fidelity Runtime for TinyML Inference under Dynamic Workload Contention  
**Target Venue:** IEEE Transactions on Computers (TC) / ACM TECS / IEEE IoT-J  
**Date:** August 28, 2026  

---

## 1. Executive Summary

This report performs a comprehensive audit of the workload contention and deadline modeling infrastructure implemented in `phase5/simulator/trace_simulator.py` and evaluated across the 80-configuration experiment in Paper 1. 

**Core Findings:**
1. **Mathematical Nature:** Contention is modeled via deterministic multiplier scaling with stochastic Gaussian jitter, representing simulated execution delays on an x86_64 host CPU. It is **trace-driven host simulation**, NOT physical RTOS task preemption or hardware bus contention.
2. **Scale Disparity:** Single-sample inference latency for sub-400 MAC models is sub-microsecond to tens of microseconds ($0.82$--$41.25\,\mu\text{s}$), whereas execution deadlines were configured in milliseconds ($5$--$100\,\text{ms}$). As a result, deadline compliance is trivially $100.0\%$ across all 80 configurations.
3. **Reframing Required:** The paper must transparently disclose this scale disparity, repositioning deadline compliance as a feasibility boundary check while focusing the primary contribution on **workload-aware model switching, theoretical compute reduction ($68.4\%$), and accuracy preservation**.

---

## 2. Actual Code Implementation Audit

### 2.1 Workload Regime Specifications (`phase5/simulator/trace_simulator.py`, lines 48–69)

```python
WORKLOAD_PROFILES = {
    WorkloadLevel.LOW: WorkloadProfile(
        name="LOW", level=WorkloadLevel.LOW,
        latency_multiplier=1.0, jitter_std=0.1,
        description="Minimal host CPU contention; baseline latency"
    ),
    WorkloadLevel.MEDIUM: WorkloadProfile(
        name="MEDIUM", level=WorkloadLevel.MEDIUM,
        latency_multiplier=1.5, jitter_std=0.3,
        description="Moderate host CPU contention"
    ),
    WorkloadLevel.HIGH: WorkloadProfile(
        name="HIGH", level=WorkloadLevel.HIGH,
        latency_multiplier=3.0, jitter_std=0.8,
        description="Heavy host CPU contention"
    ),
    WorkloadLevel.BURST: WorkloadProfile(
        name="BURST", level=WorkloadLevel.BURST,
        latency_multiplier=5.0, jitter_std=2.0,
        description="Burst host CPU contention with high jitter"
    ),
}
```

### 2.2 Synthetic Latency Sequence Generation (lines 72–83)
```python
def generate_workload_sequence(n_samples: int, profile: WorkloadProfile,
                                seed: int = RANDOM_SEED) -> np.ndarray:
    rng = np.random.RandomState(seed)
    base = np.full(n_samples, profile.latency_multiplier)
    jitter = rng.normal(0, profile.jitter_std, n_samples)
    return np.maximum(base + jitter, 1.0)
```

### 2.3 Simulated Latency vs. Configured Deadlines across all 80 Configurations

| Workload Level | Nominal Multiplier | Simulated Mean Latency (Table II) | Simulated P95 Latency (Table II) | Smallest Deadline ($D=5\,\text{ms}$) | Largest Deadline ($D=100\,\text{ms}$) | Margin of Compliance |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **LOW** | $1.0\times$ | $4.88$--$5.32\,\mu\text{s}$ | $7.81$--$8.60\,\mu\text{s}$ | $5,000\,\mu\text{s}$ | $100,000\,\mu\text{s}$ | $>580\times$ headroom |
| **MEDIUM** | $1.5\times$ | $6.61$--$7.09\,\mu\text{s}$ | $8.87$--$10.43\,\mu\text{s}$ | $5,000\,\mu\text{s}$ | $100,000\,\mu\text{s}$ | $>475\times$ headroom |
| **HIGH** | $3.0\times$ | $13.02$--$14.28\,\mu\text{s}$ | $18.91$--$22.09\,\mu\text{s}$ | $5,000\,\mu\text{s}$ | $100,000\,\mu\text{s}$ | $>225\times$ headroom |
| **BURST** | $5.0\times$ | $21.32$--$23.98\,\mu\text{s}$ | $35.27$--$41.25\,\mu\text{s}$ | $5,000\,\mu\text{s}$ | $100,000\,\mu\text{s}$ | $>120\times$ headroom |

---

## 3. Critical Systems Insights & Reviewer Vulnerabilities

### 1. What the Workload Model Approximates:
- Simulates macroscopic CPU throttling and execution delays induced by external background processes.
- Evaluates the state-machine logic of the QoS scheduler under changing operational conditions.
- Verifies that the scheduler does not enter high-frequency switching oscillations (at most 1 switch per continuous workload regime).

### 2. What the Workload Model Cannot Represent:
- **Physical RTOS Task Preemption:** Does not model FreeRTOS context switching, tick interrupts, or priority inversions.
- **Hardware Bus and Memory Contention:** Does not model DMA transfers, SPI/I2C sensor read delays, or Flash cache misses.
- **Microcontroller Microarchitectural Stalls:** Does not capture pipeline flushes on ARM Cortex-M or Xtensa LX6/LX7 cores.

### 3. Why 100% Deadline Compliance is Trivially Achieved:
Because sub-400 MAC models execute in sub-microseconds on modern CPUs, multiplying execution time by $5\times$ only yields $\approx 24\,\mu\text{s}$. A deadline of $5\,\text{ms}$ ($5,000\,\mu\text{s}$) is $200\times$ larger than the worst-case simulated execution time. Therefore, claiming "100% deadline compliance" as a breakthrough is misleading to embedded systems reviewers.

---

## 4. Specific Manuscript Corrections Required

1. **Abstract:**
   - Remove any implication that achieving 100% deadline compliance is a novel algorithmic triumph.
   - Frame the primary contribution around **workload-aware model switching, theoretical arithmetic compute reduction ($68.4\%$), and class-balance preservation (macro F1 $0.7563$)**.
2. **Section VII (Workload and Deadline Model):**
   - Explicitly state: *"Workload contention is modeled via synthetic multiplicative latency scaling and Gaussian jitter to evaluate scheduler state transitions under controlled load. These parameters represent trace-driven simulation parameters rather than bare-metal RTOS preemption measurements."*
   - Add explicit scale discussion: *"Because single-sample inference latency for sub-400 MAC models on host hardware is on the order of microseconds ($<50\,\mu\text{s}$), all evaluated configurations trivially satisfy millisecond-scale deadlines ($5$--$100\,\text{ms}$). We evaluate deadline compliance primarily as a sanity and feasibility check, focusing our primary systems analysis on active arithmetic reduction and diagnostic fidelity."*
3. **Section XI (Limitations):**
   - Expand Limitation 1 to explicitly discuss the scale disparity between microsecond execution and millisecond deadlines, and identify real-time micro-benchmarking on microcontrollers as required future work.
