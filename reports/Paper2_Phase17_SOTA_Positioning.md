# Phase 17A — SOTA and Related Work Positioning: Paper 2

**Manuscript:** Empirical Pareto Frontier of Model Compression Paradigms for Ultra-Low-Resource TinyML  
**Target Venue:** ACM Transactions on Design Automation of Electronic Systems (TODAES) / IEEE TCAD  
**Date:** August 28, 2026  

---

## 1. Executive Summary

This report performs a comprehensive comparative analysis of Paper 2 against the 2020–2026 TinyML and embedded model compression literature. We survey the 8 closest benchmark and methodology studies, examine their evaluation regimes, and establish the precise scientific classification and contribution boundary of Paper 2.

**Scientific Classification:** **STRONG_EMPIRICAL_BENCHMARK / NOVEL_EMPIRICAL_CHARACTERIZATION**  
**Central Positioning:** An empirical, multi-objective characterization of 12 serialized TFLite deployment artifacts under ultra-low memory budgets (<4 KB, <400 MACs), providing exact structural evidence of the decoupling between fine-grained computational sparsity and on-disk FlatBuffer serialization.

---

## 2. Comparative Matrix: 8 Closest Prior Works (2020–2026)

| Prior Work | Primary Venues / Year | Evaluated Datasets | Model Families | Evaluated Compression Paradigms | Evaluated Metrics | Evaluated Hardware | Storage Metric | Compute Metric | Actual Serialized Binary Inspected? | Primary Distinction from Paper 2 |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **MLPerf Tiny** (Banbury et al.~\cite{banbury2021benchmarking}) | IEEE Micro 2021 | VWW, KWS, CIFAR-10, Anomaly | ResNet-8, DS-CNN, MobileNet, FC-AE | Standard INT8 PTQ | Acc, Latency, Energy | Cortex-M4/M7, ESP32, etc. | Flash Footprint | MACs | Yes (Submission Binaries) | Standardized multi-hardware benchmark; does not explore multi-paradigm Pareto frontiers (pruning vs. KD vs. feature reduction) on identical baselines. |
| **MCUNet / MCUNetV2** (Lin et al.~\cite{lin2020mcunet,lin2021mcunetv2}) | NeurIPS 2020 / 2021 | ImageNet, VWW, Speech Commands | TinyNAS MobileNet-style CNNs | NAS + Memory-Aware Quantization | Top-1 Acc, SRAM Peak, Flash | STM32F7, STM32H7 | Flash (KB) | MACs | Yes (Custom TinyEngine) | Joint NAS + engine optimization for vision (>256 KB Flash); does not target sub-4 KB tabular sensor diagnostic regimes. |
| **MuNAS** (Liberis et al.~\cite{liberis2021munas}) | ACM TECS 2021 | CIFAR-10, HAR, Audio | Tiny CNNs / MLPs | Multi-Objective NAS (Memory, Energy) | Acc, SRAM, Energy | Cortex-M0+, Cortex-M4 | Flash / SRAM | Cycle count | Yes | Explores NAS search spaces for microcontrollers; does not isolate individual compression paradigm interactions (PTQ vs. pruning vs. KD). |
| **Blalock et al. Pruning Survey**~\cite{blalock2020state} | MLSys 2020 | ImageNet, CIFAR-10 | ResNet-50, VGG, MobileNet | Magnitude, Structural, Dynamic Pruning | Top-1 Acc, Sparsity % | x86, GPU | Theoretical Parameters | Theoretical FLOPs | No (In-Memory PyTorch / TF tensors) | Critical meta-study exposing reproducibility gaps in pruning literature; theoretical focus, not serialized FlatBuffer edge deployment. |
| **Gholami et al. Quantization Survey**~\cite{gholami2022survey} | IEEE Proc. 2022 | ImageNet, Language | Diverse Deep Nets | Uniform/Non-uniform PTQ, QAT | Accuracy vs. Bitwidth | GPU, Edge TPU, FPGA | Parameter bits | Bit-Operations (BOPs) | No (Theoretical survey) | Comprehensive theoretical survey of quantization algorithms; does not provide empirical Pareto frontiers for sub-4 KB TinyML artifacts. |
| **MicroNets Challenge** (Banbury et al.~\cite{banbury2021micronets}) | MLSys / NeurIPS 2021 | ImageNet, WMT, LibriSpeech | Transformer, MobileNet, EfficientNet | Extreme Pruning, Quantization, KD | Accuracy vs. Storage/Compute score | Cloud / Edge accelerators | Parameter count | Multi-Add ops | No (Score-based competition) | Evaluates extreme compression for edge accelerators (>1 MB); does not inspect low-level MCU FlatBuffer artifacts. |
| **Polino et al. Distillation + Quantization**~\cite{polino2018model} | ICLR 2018 | CIFAR-10, ImageNet | ResNet, VGG | Quantized Distillation | Accuracy, Bitwidth | x86 / GPU | Model bits | Arithmetic ops | No (Framework tensors) | Theoretical algorithm for quantized distillation; does not evaluate standard TFLite Micro runtime serialization constraints. |
| **Paper 2 (This Work)** | ACM TODAES 2026 | EngineFaultDB (55,998 samples) | Sub-4 KB MLPs (14f, 12f, Student A/B) | INT8 PTQ, Feature Reduction, Unstructured Pruning, Structural KD | Test Acc, Binary Size, Active MACs, Host Latency | Serialized TFLite on x86 host (empirical) | **Exact On-Disk .tflite Bytes** | **Verified Active MACs** | **YES (Low-Level FlatBuffer Graph & Tensor Inspection)** | **Exposes the exact FlatBuffer serialization behavior across all 4 paradigms under strict <4 KB budgets, proving structural KD out-compresses unstructured pruning on disk.** |

---

## 3. Addressing the Core Reviewer Questions

### Question 1: "Why is this more than a carefully executed engineering benchmark?"

**Reviewer Objection:**  
*"The paper simply runs standard TensorFlow Model Optimization Toolkit (TF-MOT) tutorials on a tabular dataset and plots the results. Where is the scientific research contribution?"*

**Scientifically Defensible Answer:**
1. **First-of-Its-Kind Multi-Paradigm Artifact Characterization under <4 KB Budgets:**  
   Most compression studies evaluate a single paradigm in isolation (e.g., pruning *or* quantization *or* distillation) and typically on vision benchmarks with megabytes of memory. Paper 2 is one of the few empirical studies to evaluate all four paradigms simultaneously on an identical, verified baseline constrained to the extreme edge regime ($<4$\,KB Flash, $<400$ MACs).
2. **Empirical Demystification of FlatBuffer Serialization Mechanics:**  
   A pervasive assumption in theoretical ML is that $75\%$ weight pruning yields a $75\%$ reduction in storage. Paper 2 empirically deconstructs this assumption by inspecting the actual FlatBuffer binaries, demonstrating that fine-grained unstructured sparsity in standard TFLite retains dense 2D arrays, resulting in an actual $+28$\,Byte metadata penalty ($3,920$\,B vs. $3,892$\,B). 
3. **Actionable Pareto Guidance for Edge Engineers:**  
   By mapping the exact 3D Pareto frontier across deterministic deployment axes (Accuracy, On-Disk Size, Active Arithmetic Ops), Paper 2 provides rigorous empirical proof that:
   - Structural Knowledge Distillation is the non-dominated paradigm when **Flash storage** is the primary bottleneck ($2,976$\,B, a $23.5\%$ reduction).
   - Unstructured Magnitude Pruning is the non-dominated paradigm when **ALU compute cycles** are the primary bottleneck ($96$ active MACs, a $75\%$ reduction).
   - Full INT8 Quantization is non-dominated when **pure integer arithmetic** is required (0 float32 tensors).

### Question 2: "Is the Paper SOTA?"

**Assessment: NOT_SOTA (and SOTA should NOT be claimed).**  
Paper 2 does not propose a new compression algorithm that beats SOTA algorithms on ImageNet or CIFAR-10. It is a **rigorous empirical characterization and artifact benchmark** that evaluates existing standard compression techniques on ultra-low-resource embedded binaries. Claiming "SOTA" would trigger immediate reviewer hostility. Reframing the paper explicitly as an **Empirical Characterization and Pareto Benchmark** makes the contribution transparent, rigorous, and respected.

---

## 4. Literature Comparison Framing for Revised Section III

The revised Related Work (Section III) should be structured into four targeted subsections:
1. **Quantization and Pure-Integer Edge Execution:** Contrast theoretical bitwidth reduction~\cite{gholami2022survey} with verified `FULL_INT8` execution graph requirements in TFLite Micro~\cite{david2021tensorflow}.
2. **Weight Sparsity vs. Embedded Serialization Formats:** Contrast theoretical pruning literature~\cite{han2016deep,blalock2020state} with embedded flatbuffer dense storage realities.
3. **Structural Distillation for Extreme-Edge Topologies:** Discuss how distillation enables true topological compression~\cite{hinton2015distilling,gou2021knowledge} compared to fine-grained pruning.
4. **Multi-Objective Edge AI Benchmarks:** Position the work alongside MLPerf Tiny~\cite{banbury2021benchmarking} and MuNAS~\cite{liberis2021munas}, emphasizing the specific focus on sub-4 KB multi-sensor diagnostics.
