# Paper 5 — Phase 19A Target Venue & Title Audit Report

> **Manuscript Topic:** On-Device Physical Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers  
> **Audited Venues:** IEEE ESL, ACM TECS, IEEE IoT-J, IEEE TCAD, ACM LCTES, TinyML Symposium, MLSys  
> **Recommended Venue:** *IEEE Embedded Systems Letters (ESL)* / *ACM Transactions on Embedded Computing Systems (TECS)*  

---

## 1. Comprehensive Venue Suitability Audit

We audited 7 prominent venues spanning embedded systems, edge AI, design automation, and machine learning systems:

```
+---------------------------------------------------------------------------------------------------------+
| VENUE                                 | SCOPE & CRITERIA                      | CLASSIFICATION | RATIONALE                              |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| IEEE Embedded Systems Letters (ESL)   | 4-page concise letters on embedded    | EXCELLENT_FIT  | Perfect match for a tightly focused,   |
|                                       | hardware, MCU benchmarks, and TinyML  |                | high-rigor empirical hardware study    |
|                                       | measurements with fast turnaround.    |                | with N=24,000 physical measurements.   |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| ACM Transactions on Embedded          | Full journal articles on embedded     | GOOD_FIT       | Strong fit for a comprehensive         |
| Computing Systems (TECS)              | architectures, runtimes, and TinyML   |                | characterization with detailed memory  |
|                                       | characterizations.                    |                | and host-to-silicon translation.       |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| TinyML Research Symposium             | Specialized annual symposium on       | EXCELLENT_FIT  | Direct target audience of TinyML       |
|                                       | ultra-low-power machine learning.     |                | researchers, hardware engineers, and   |
|                                       |                                       |                | runtime developers.                    |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| IEEE Internet of Things Journal       | Broad IoT systems, networking, and    | GOOD_FIT /     | High prestige, but typically expects   |
| (IEEE IoT-J)                          | applications.                         | BORDERLINE     | full end-to-end IoT cloud/mesh context |
|                                       |                                       |                | rather than standalone MCU profiling.  |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| ACM SIGPLAN / SIGBED LCTES            | Languages, compilers, and tools for   | GOOD_FIT       | Excellent venue for embedded artifact  |
|                                       | embedded systems.                     | (Conf. Track)  | execution and memory layout analysis.  |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| IEEE Transactions on CAD (TCAD)       | EDA, high-level synthesis, and VLSI   | BORDERLINE     | Less focused on software deployment;   |
|                                       | circuit design.                       |                | expects custom silicon or HLS tools.   |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
| MLSys (Conference on ML & Systems)    | Large-scale ML systems and distributed| POOR_FIT       | Focuses primarily on cloud/datacenter  |
|                                       | training/serving architectures.       |                | scale or massive vision architectures. |
+---------------------------------------+---------------------------------------+----------------+----------------------------------------+
```

---

## 2. Primary Recommendation & Publishing Strategy

1. **Primary Target: *IEEE Embedded Systems Letters (ESL)***  
   - **Format:** 4-page IEEE double-column format.
   - **Why ESL is the Optimal Choice:**  
     ESL prioritizes concise, novel, and rigorously measured empirical results on commercial microcontroller hardware. Paper 5's $N=24,000$ measurement suite, host-to-silicon divergence analysis, and memory arena deconstruction fit naturally into ESL's 4-page structure without fluff.
2. **Alternative Target: *ACM Transactions on Embedded Computing Systems (TECS)***  
   - **Format:** Regular full-length journal article ($10\text{--}14$ pages).
   - **When to Use:** If expanded with deeper compiler flag evaluations or comparative cross-toolchain profiling.

---

## 3. Title Audit and Final Selection

We evaluated four candidate title formulations:

```
+---------------------------------------------------------------------------------------------------------+
| CANDIDATE TITLE                                               | SCIENTIFIC ACCURACY | PROMOTION/HYPE | VERDICT  |
+---------------------------------------------------------------+---------------------+----------------+----------+
| 1. "Physical Characterization of Ultra-Low-Resource INT8      | Moderate            | Low            | Generic  |
|    TinyML Models on ESP32 Microcontrollers"                   |                     |                |          |
+---------------------------------------------------------------+---------------------+----------------+----------+
| 2. "From TFLite Artifact to Microcontroller: Physical         | High                | Low            | Strong   |
|    Benchmarking of Ultra-Low-Resource INT8 TinyML Models"     |                     |                |          |
+---------------------------------------------------------------+---------------------+----------------+----------+
| 3. "On-Device Characterization and Latency Profiling of       | Exceptionally High  | Zero (Pure)    | SELECTED |
|    Ultra-Low-Resource INT8 TinyML Models on ESP32-D0WD-V3"    |                     |                | (Best)   |
+---------------------------------------------------------------+---------------------+----------------+----------+
| 4. "SOTA Real-Time TinyML Deployment and Energy Benchmarking  | Misleading (False   | High (Severe)  | REJECTED |
|    Guarantees on ESP32 Silicon"                               | WCET/Energy claims) |                | (Violates|
|                                                               |                     |                | Ethics)  |
+---------------------------------------------------------------+---------------------+----------------+----------+
```

### Selected Authoritative Title:
> **"On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers"**  
> *(Sub-title / Running Header: Empirical Benchmarking, Host-to-Silicon Divergence, and Memory Layout on Xtensa LX6)*
