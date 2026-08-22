#!/usr/bin/env python3
"""
EngineFaultDB — Complete Dataset Audit Analysis
================================================
Generates:
  - Dataset_Audit_Report.md   (full markdown report)
  - correlation_heatmap.png
  - class_distribution.png

All statistics are measured directly from the data — nothing assumed.
"""

import os
import sys
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Fix Windows encoding
sys.stdout.reconfigure(encoding="utf-8")

# ── Paths ────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CSV_PATH   = os.path.join(BASE_DIR, "EngineFaultDB_Final.csv")
OUT_DIR    = BASE_DIR                      # save outputs beside the CSV
REPORT     = os.path.join(OUT_DIR, "Dataset_Audit_Report.md")
HEATMAP    = os.path.join(OUT_DIR, "correlation_heatmap.png")
CLASS_PLOT = os.path.join(OUT_DIR, "class_distribution.png")

# ── 1. Load ──────────────────────────────────────────────────────────────
df = pd.read_csv(CSV_PATH)
print(f"Loaded {CSV_PATH}  →  {df.shape[0]:,} rows × {df.shape[1]} columns")

# ── 2. Basic facts ───────────────────────────────────────────────────────
n_rows, n_cols = df.shape
col_names      = list(df.columns)
dtypes_info    = df.dtypes.astype(str).to_dict()
missing_total  = int(df.isnull().sum().sum())
missing_per_col = df.isnull().sum().to_dict()
dup_rows       = int(df.duplicated().sum())
file_size_bytes = os.path.getsize(CSV_PATH)
file_size_mb    = file_size_bytes / (1024 * 1024)

# ── 3. Class distribution ───────────────────────────────────────────────
class_col = "Fault"
class_counts   = df[class_col].value_counts().sort_index()
class_pct      = df[class_col].value_counts(normalize=True).sort_index() * 100

# ── 4. Descriptive statistics ────────────────────────────────────────────
desc = df.describe().T           # transpose for readability
desc["range"] = desc["max"] - desc["min"]
desc["cv"]    = (desc["std"] / desc["mean"]).replace([np.inf, -np.inf], np.nan)

# ── 5. Constant / near-constant columns ─────────────────────────────────
nunique       = df.nunique()
constant_cols = nunique[nunique == 1].index.tolist()
near_constant = nunique[nunique <= 2].index.tolist()

# ── 6. Correlation matrix (numeric only) ────────────────────────────────
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
corr_matrix  = df[numeric_cols].corr()

# ── 7. High correlations (|r| >= 0.90, excluding self) ──────────────────
high_corr_pairs = []
for i in range(len(corr_matrix.columns)):
    for j in range(i + 1, len(corr_matrix.columns)):
        r = corr_matrix.iloc[i, j]
        if abs(r) >= 0.90:
            high_corr_pairs.append(
                (corr_matrix.columns[i], corr_matrix.columns[j], round(r, 4))
            )

# ── 8. Potential data-quality issues ─────────────────────────────────────
quality_issues = []
if missing_total > 0:
    quality_issues.append(f"Missing values found: {missing_total} total.")
if dup_rows > 0:
    quality_issues.append(f"Duplicate rows found: {dup_rows}.")
if constant_cols:
    quality_issues.append(f"Constant columns (zero variance): {constant_cols}")
if high_corr_pairs:
    quality_issues.append(
        f"{len(high_corr_pairs)} feature pair(s) with |r| ≥ 0.90 "
        "(potential multicollinearity)."
    )
# Check for class imbalance (max/min ratio > 2)
imbalance_ratio = class_counts.max() / class_counts.min()
if imbalance_ratio > 2:
    quality_issues.append(
        f"Mild class imbalance: largest/smallest class ratio = "
        f"{imbalance_ratio:.2f}."
    )
# Check for negative values where they shouldn't be
for c in numeric_cols:
    if (df[c] < 0).any():
        quality_issues.append(f"Column '{c}' contains negative values.")
# Check for zeros that might be placeholders
zero_cols = []
for c in numeric_cols:
    zero_frac = (df[c] == 0).sum() / len(df)
    if 0 < zero_frac < 1 and zero_frac > 0.25:
        zero_cols.append((c, f"{zero_frac*100:.1f}%"))
if zero_cols:
    quality_issues.append(
        f"Columns with >25% zero values (possible placeholders): "
        + ", ".join(f"{c} ({pct})" for c, pct in zero_cols)
    )

if not quality_issues:
    quality_issues.append("No significant data-quality issues detected.")


# ═══════════════════════════════════════════════════════════════════════
# VISUALISATIONS
# ═══════════════════════════════════════════════════════════════════════

# ── Correlation heatmap ──────────────────────────────────────────────────
plt.figure(figsize=(14, 11))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(
    corr_matrix,
    mask=mask,
    annot=True,
    fmt=".2f",
    cmap="RdBu_r",
    center=0,
    linewidths=0.5,
    square=True,
    cbar_kws={"shrink": 0.8, "label": "Pearson r"},
    annot_kws={"size": 8},
)
plt.title("EngineFaultDB — Feature Correlation Matrix", fontsize=15, pad=15)
plt.tight_layout()
plt.savefig(HEATMAP, dpi=200)
plt.close()
print(f"Saved  {HEATMAP}")

# ── Class distribution bar chart ─────────────────────────────────────────
fig, ax = plt.subplots(figsize=(8, 5))
colors = sns.color_palette("Set2", n_colors=len(class_counts))
bars = ax.bar(
    [f"Fault {int(k)}" for k in class_counts.index],
    class_counts.values,
    color=colors,
    edgecolor="black",
    linewidth=0.6,
)
for bar, pct in zip(bars, class_pct.values):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 200,
        f"{bar.get_height():,}\n({pct:.2f}%)",
        ha="center",
        va="bottom",
        fontsize=10,
    )
ax.set_xlabel("Fault Type", fontsize=12)
ax.set_ylabel("Count", fontsize=12)
ax.set_title("EngineFaultDB — Class Distribution", fontsize=14, pad=12)
ax.set_ylim(0, class_counts.max() * 1.18)
ax.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig(CLASS_PLOT, dpi=200)
plt.close()
print(f"Saved  {CLASS_PLOT}")


# ═══════════════════════════════════════════════════════════════════════
# MARKDOWN REPORT
# ═══════════════════════════════════════════════════════════════════════

def md_table(df_table):
    """Convert a DataFrame to a markdown table string."""
    lines = []
    headers = [""] + list(df_table.columns) if df_table.index.name or True else list(df_table.columns)
    # Use index as first column
    header_line = "| " + " | ".join(str(h) for h in ["Feature"] + list(df_table.columns)) + " |"
    sep_line    = "| " + " | ".join(["---"] * (len(df_table.columns) + 1)) + " |"
    lines.append(header_line)
    lines.append(sep_line)
    for idx, row in df_table.iterrows():
        vals = [str(idx)] + [f"{v:.4f}" if isinstance(v, float) else str(v) for v in row]
        lines.append("| " + " | ".join(vals) + " |")
    return "\n".join(lines)


with open(REPORT, "w", encoding="utf-8") as f:
    f.write("# EngineFaultDB — Dataset Audit Report\n\n")
    f.write(f"**Generated:** Measured directly from `EngineFaultDB_Final.csv`\n\n")
    f.write("---\n\n")

    # ── 1. Repository & File Overview ────────────────────────────────────
    f.write("## 1. Repository & File Overview\n\n")
    f.write("| Item | Value |\n")
    f.write("| --- | --- |\n")
    f.write("| Repository | [Leo-Thomas/EngineFaultDB](https://github.com/Leo-Thomas/EngineFaultDB) |\n")
    f.write("| License | GNU General Public License v3.0 (GPLv3) |\n")
    f.write(f"| Dataset file | `EngineFaultDB_Final.csv` |\n")
    f.write(f"| File size | {file_size_mb:.2f} MB ({file_size_bytes:,} bytes) |\n")
    f.write("| Other files | `README.md`, `LICENSE` |\n")
    f.write(f"| Repository structure | Flat (3 files, no subdirectories) |\n")
    f.write("\n")

    # ── 2. Dataset Shape ─────────────────────────────────────────────────
    f.write("## 2. Dataset Shape\n\n")
    f.write(f"| Metric | Value |\n")
    f.write(f"| --- | --- |\n")
    f.write(f"| Rows | {n_rows:,} |\n")
    f.write(f"| Columns | {n_cols} |\n")
    f.write(f"| Total cells | {n_rows * n_cols:,} |\n")
    f.write("\n")

    # ── 3. Column Names & Data Types ─────────────────────────────────────
    f.write("## 3. Column Names & Data Types\n\n")
    f.write("| # | Column | Dtype | Non-Null Count | Unique Values |\n")
    f.write("| --- | --- | --- | --- | --- |\n")
    for i, c in enumerate(col_names):
        nn = int(df[c].notna().sum())
        uq = int(df[c].nunique())
        f.write(f"| {i+1} | `{c}` | {dtypes_info[c]} | {nn:,} | {uq:,} |\n")
    f.write("\n")

    # ── 4. Missing Values ────────────────────────────────────────────────
    f.write("## 4. Missing Values\n\n")
    f.write(f"**Total missing cells:** {missing_total:,}\n\n")
    if missing_total > 0:
        f.write("| Column | Missing | % |\n")
        f.write("| --- | --- | --- |\n")
        for c, v in missing_per_col.items():
            if v > 0:
                f.write(f"| `{c}` | {v:,} | {v/n_rows*100:.2f}% |\n")
    else:
        f.write("No missing values in any column.\n")
    f.write("\n")

    # ── 5. Duplicate Rows ────────────────────────────────────────────────
    f.write("## 5. Duplicate Rows\n\n")
    f.write(f"| Metric | Value |\n")
    f.write(f"| --- | --- |\n")
    f.write(f"| Exact duplicate rows | {dup_rows:,} |\n")
    f.write(f"| Duplicate % | {dup_rows/n_rows*100:.2f}% |\n")
    f.write("\n")

    # ── 6. Class Distribution ────────────────────────────────────────────
    f.write("## 6. Class Distribution (Target: `Fault`)\n\n")
    f.write("| Fault Type | Count | Percentage |\n")
    f.write("| --- | --- | --- |\n")
    for k in class_counts.index:
        f.write(f"| {int(k)} | {class_counts[k]:,} | {class_pct[k]:.2f}% |\n")
    f.write(f"| **Total** | **{n_rows:,}** | **100%** |\n")
    f.write(f"\n> Class imbalance ratio (max / min): **{imbalance_ratio:.2f}**\n\n")
    f.write("![Class Distribution](class_distribution.png)\n\n")

    # ── 7. Descriptive Statistics ────────────────────────────────────────
    f.write("## 7. Descriptive Statistics\n\n")
    stat_df = desc[["count", "mean", "std", "min", "25%", "50%", "75%", "max", "range", "cv"]].copy()
    stat_df.columns = ["Count", "Mean", "Std", "Min", "25%", "Median", "75%", "Max", "Range", "CV"]
    f.write(md_table(stat_df.round(4)))
    f.write("\n\n")

    # ── 8. Feature Ranges ────────────────────────────────────────────────
    f.write("## 8. Feature Ranges\n\n")
    f.write("| Feature | Min | Max | Range |\n")
    f.write("| --- | --- | --- | --- |\n")
    for c in numeric_cols:
        mn = df[c].min()
        mx = df[c].max()
        rng = mx - mn
        f.write(f"| `{c}` | {mn:.4f} | {mx:.4f} | {rng:.4f} |\n")
    f.write("\n")

    # ── 9. Constant / Near-Constant Columns ──────────────────────────────
    f.write("## 9. Constant / Near-Constant Columns\n\n")
    if constant_cols:
        f.write(f"**Constant columns (1 unique value):** {', '.join(f'`{c}`' for c in constant_cols)}\n\n")
    else:
        f.write("No constant columns detected.\n\n")
    if near_constant and near_constant != constant_cols:
        f.write(f"**Near-constant (≤ 2 unique):** {', '.join(f'`{c}`' for c in near_constant)}\n\n")

    # ── 10. Correlation Matrix ───────────────────────────────────────────
    f.write("## 10. Correlation Matrix\n\n")
    f.write("![Correlation Heatmap](correlation_heatmap.png)\n\n")
    if high_corr_pairs:
        f.write("### Highly Correlated Feature Pairs (|r| ≥ 0.90)\n\n")
        f.write("| Feature A | Feature B | Pearson r |\n")
        f.write("| --- | --- | --- |\n")
        for a, b, r in sorted(high_corr_pairs, key=lambda x: -abs(x[2])):
            f.write(f"| `{a}` | `{b}` | {r:.4f} |\n")
        f.write("\n")
    else:
        f.write("No feature pairs with |r| ≥ 0.90.\n\n")

    # ── 11. Data Quality Issues ──────────────────────────────────────────
    f.write("## 11. Potential Data-Quality Issues\n\n")
    for issue in quality_issues:
        f.write(f"- {issue}\n")
    f.write("\n")

    # ── 12. Reproducibility — Python Code ────────────────────────────────
    f.write("## 12. Reproducibility\n\n")
    f.write("The complete Python script used to generate this report is saved as "
            "`audit_analysis.py` alongside the dataset.  Key dependencies:\n\n")
    f.write("```\n")
    f.write("Python 3.13+\n")
    f.write("pandas, numpy, matplotlib, seaborn\n")
    f.write("```\n\n")
    f.write("Run:\n\n")
    f.write("```bash\n")
    f.write("python audit_analysis.py\n")
    f.write("```\n\n")

    f.write("---\n")
    f.write("*End of report.*\n")

print(f"Saved  {REPORT}")
print("\n✅  Audit complete.")
