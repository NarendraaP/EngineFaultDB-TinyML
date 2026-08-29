# Submission Cover Letter

**To:** Editor-in-Chief  
*ACM Transactions on Embedded Computing Systems (TECS)*  
Association for Computing Machinery  

**Date:** August 29, 2026  

**Subject:** Submission of Research Article: *"On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers"*  

Dear Editor-in-Chief and Editorial Board Members,

I am pleased to submit our original full-length research manuscript entitled **"On-Device Characterization and Latency Profiling of Ultra-Low-Resource INT8 TinyML Models on ESP32 Microcontrollers"** for consideration for publication as a regular research article in *ACM Transactions on Embedded Computing Systems (TECS)*.

### Research Context and Contribution
Deploying deep learning models on resource-constrained 32-bit microcontrollers (TinyML) is crucial for real-time edge intelligence. However, while vision and audio models ($>100\,\text{KB}$, $10\text{--}300\,\text{ms}$) have been widely studied, ultra-compact tabular diagnostic networks ($<4\,\text{KB}$ Flash, sub-$100\,\si{\micro\second}$ execution latency) remain significantly under-characterized on commercial silicon. Furthermore, existing host-side simulations fail to capture the low-level instruction bottlenecks and cache dynamics of embedded RISC cores.

In this work, we present a comprehensive physical on-device characterization of four verified `FULL_INT8` Multi-Layer Perceptron (MLP) models deployed on physical Espressif ESP32-D0WD-V3 microcontroller silicon (dual-core Xtensa LX6 @ 240 MHz, 4 MB Flash, 320 KB SRAM). Utilizing a zero-I/O in-RAM hardware timer benchmarking protocol across 24,000 measured single-sample inferences, we establish:
1. **Monotonic Parameter Scaling:** Isolated on-device execution latency scales strictly monotonically with parameter count ($R^2 = 0.963$) from $64.55\,\si{\micro\second}$ (176 params) to $89.90\,\si{\micro\second}$ (412 params).
2. **Physical Distillation Gains:** Structural knowledge distillation delivers an observed $28.20\%$ physical execution latency reduction on silicon relative to the uncompressed baseline.
3. **Quantification of the Host Translation Gap:** Host x86_64 profiling underestimates physical microcontroller execution latency by $62.87\times$ to $76.77\times$, unmasking sub-microsecond rank inversions where host superscalar caching obscures true integer ALU scaling.
4. **Memory Subsystem & Heap Determinism:** TensorFlow Lite for Microcontrollers commits exactly $916\,\text{Bytes}$ of static tensor arena memory with zero dynamic heap allocations and zero memory leakage across $25,200$ consecutive invocations.
5. **Cyber-Physical Edge Deployment Model:** We present a dual-core FreeRTOS partitioning architecture isolating sensor I/O on Core 0 while executing deterministic TinyML inference bursts on Core 1 under $5\text{--}100\,\text{ms}$ deadlines with $97.96\%\text{--}99.90\%$ feasibility headroom.

### Author Confirmation & Open Reproducibility
* This manuscript is original, has not been published previously, and is not currently under consideration for publication elsewhere.
* All authors have approved the manuscript and agree with its submission to *ACM TECS*.
* All experimental firmware code, PlatformIO configuration files, compiled TFLite FlatBuffers, C-byte array headers, Python analysis scripts, and raw serial logs are open-source and publicly accessible in our repository.

Thank you for your time and consideration of our work.

Sincerely,  

**Narendra Satish**  
Corresponding Author  
E-mail: narendresh.p@gmail.com  
GitHub: https://github.com/NarendraaP/EngineFaultDB-TinyML  
