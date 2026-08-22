# Reproducibility Guide: Paper 4 (Independent TinyML Verification Framework)

This submission package contains the complete source code, LaTeX manuscript, figures, and reproducibility instructions for:
**"An Independent Verification Framework for Reproducible TinyML Evaluation"**

## 1. Verification Dimensions (D1-D7)
The verification protocol formalizes testing across seven core dimensions:
1. D1: Data Isolation & Normalization Purity
2. D2: Serialized Binary Integrity
3. D3: Quantization Graph Inspection (Zero-Float Verification)
4. D4: Sparsity vs. Storage Accounting
5. D5: Theoretical vs. Active MAC Profiling
6. D6: Timing Protocol Auditing
7. D7: Runtime Routing Non-Leakage

## 2. Reproduction Workflow
To execute the complete independent verification suite:
```bash
python scripts/phase4_5_verification.py
```
Verification logs and resolved discrepancy tables:
- results/tinyml_model_profile_verified.csv
- reports/Phase14_Claim_Evidence_Matrix.md

## 3. Scope & Limitations
- Audits software artifacts, serialized binaries, and host traces. Physical MCU timing and hardware power profiling represent complementary hardware validation layers.
