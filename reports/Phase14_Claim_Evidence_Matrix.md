# Phase 14: Comprehensive Claim-to-Evidence Matrix & Contribution Rewriting
**Audit Date:** August 22, 2026  
**Auditor:** Antigravity Research Grade Audit Engine (ScholarMaster Protocol)  
**Strict Mandate:** Verify every major claim against concrete implementation and experimental artifacts; map literature counterexamples; provide exact conservative replacement wording.  

---

## 1. Paper 1: Claim-to-Evidence Matrix

| Claim | Manuscript Location | Implementation Evidence | Experimental Evidence | Literature Counterexample | Verdict | Required Action & Replacement Phrasing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Claim 1.1:** *Multi-fidelity runtime achieves up to 68.4% compute reduction.* | Abstract, Sec. V.C | phase5/runtime/qos_runtime.py (Mode mapping) | 	inyml_model_profile_verified.csv (HIGH: 304 MACs, BALANCED: 96 MACs) | Early-exit CNNs achieve variable compute but require deep branch graphs. | SUPPORTED-BUT-NARROW | **Refine:** Explicitly state *\"up to 68.4% reduction in theoretical active arithmetic operations (MACs) per frame relative to the high-fidelity baseline.\"* |
| **Claim 1.2:** *Maintains >99% deadline compliance under high contention.* | Abstract, Sec. V.B | QoSScheduler.select_model() logic | phase5_policy_comparison.csv (\%$ compliance under BURST at \,\mu\text{s}$) | Static scheduling misses deadlines when execution times spike. | SUPPORTED | **Retain:** Supported by 80-configuration grid data. |
| **Claim 1.3:** *Scheduler operates with zero ground-truth label leakage.* | Sec. III.B, Sec. VIII | select_model() inputs: deadline, workload, measured latency | Verified in Phase5_Software_Runtime_Audit.md (Check 1) | Many academic cascades tune selection thresholds on test data. | SUPPORTED | **Retain:** Code architecture strictly separates routing telemetry from ground truth. |

---

## 2. Paper 2: Claim-to-Evidence Matrix

| Claim | Manuscript Location | Implementation Evidence | Experimental Evidence | Literature Counterexample | Verdict | Required Action & Replacement Phrasing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Claim 2.1:** *Exactly 6 of 12 candidate models are Pareto-optimal across 4 objectives.* | Abstract, Sec. IV.D, Table II | scripts/phase4_5_verification.py | 	inyml_model_profile_verified.csv (4D non-domination computation) | 2D Pareto frontiers (Accuracy vs. Size) miss active MAC trade-offs. | SUPPORTED | **Retain:** Formally proven across Accuracy, Size, MACs, and Latency. |
| **Claim 2.2:** *Magnitude pruning yields zero serialized storage compression in standard TFLite FlatBuffers.* | Sec. IV.B, Sec. V.A | Byte-level parser erify_tflite_structure() | File sizes: ,920\,\text{B}$ across \%, 50\%, 75\%$ sparsity vs. ,892\,\text{B}$ unpruned | Literature frequently equates weight sparsity with file compression. | SUPPORTED | **Retain:** Major empirical insight exposing dense tensor buffer storage of zeros. |
| **Claim 2.3:** *Knowledge distillation achieves true structural compression.* | Sec. IV.C, Sec. V | Student models student_a_8_4 and student_b_16_4 | Student A: ,976\,\text{B}$ ($-23.5\%$), $ MACs ($-58.3\%$) | Distillation is standard, but structural compression for sub-KB FlatBuffers is verified. | SUPPORTED | **Retain:** Direct empirical proof of Flash footprint reduction. |

---

## 3. Paper 3: Claim-to-Evidence Matrix

| Claim | Manuscript Location | Implementation Evidence | Experimental Evidence | Literature Counterexample | Verdict | Required Action & Replacement Phrasing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Claim 3.1:** *Hierarchical gating achieves 26.36% compute reduction on test set and 89.8% on nominal streams.* | Abstract, Sec. V.C, Table III | Mode A DT ($ MACs) + Mode B MLP ($ MACs) | qos_threshold_sweep_test.csv ( = 0.7364$ at $\theta^* = 0.05$) | Monolithic deep diagnostic models execute \%$ of layers on all samples. | SUPPORTED-BUT-NARROW | **Refine:** Explicitly distinguish the .36\%$ empirical test-set reduction from the .8\%$ projected reduction on \%$ nominal operational telemetry. |
| **Claim 3.2:** *Maintains 99.98% anomaly detection recall.* | Abstract, Sec. V.A | Mode A Decision Tree =5$ screening | Test evaluation: $\text{FNR} = 0.000250$ ($ missed anomalies out of ,000$) | Aggressive binary screeners often leak anomalies into the nominal pool. | SUPPORTED | **Retain:** Validated on 11,200 physical test records. |
| **Claim 3.3:** *Gating threshold calibration on validation data generalizes without leakage.* | Sec. V.D | Isolated sweep on qos_threshold_sweep_val.csv | Val Acc: .51\%$ vs. Test Acc: .64\%$; Val FNR: .000188$ vs. Test FNR: .000250$ | Tuning thresholds per test set creates optimistic evaluation bias ($+1.8\%$). | SUPPORTED | **Retain:** Proven across validation and held-out test splits. |

---

## 4. Paper 4: Claim-to-Evidence Matrix

| Claim | Manuscript Location | Implementation Evidence | Experimental Evidence | Literature Counterexample | Verdict | Required Action & Replacement Phrasing |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Claim 4.1:** *The 7-dimensional verification framework uncovered 20 empirical discrepancies across 6 failure modes.* | Abstract, Sec. IV, Table II | 7 verification scripts in scripts/ & eports/ | Full discrepancy audit log in Phase4_5_Independent_Verification.md | Standard Python model.evaluate() missed 19 of the 20 low-level discrepancies. | SUPPORTED | **Retain:** Fully documented with exact line numbers and corrective patches. |
| **Claim 4.2:** *Test-set threshold selection introduces an optimistic accuracy bias of +1.80%.* | Abstract, Sec. V, Table III | Controlled leakage experiment script | Comparative validation sweep vs. test sweep | Ad-hoc threshold tuning is widespread in edge IoT literature. | SUPPORTED | **Retain:** Empirically demonstrated and mathematically quantified. |
| **Claim 4.3:** *The 7-D taxonomy provides a universal verification framework for all TinyML.* | Sec. I, Sec. II | Formal predicate definitions (-D_7$) | Case study conducted on 12 tabular diagnostic TFLite models | Framework demonstrated on tabular models; vision/audio pipelines have different operator sets. | SUPPORTED-BUT-NARROW | **Refine:** Replace "universal framework" with *\"an empirical verification protocol demonstrated on an end-to-end TinyML case study and extensible to general Edge AI pipelines.\"* |
