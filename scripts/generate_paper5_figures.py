import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Output directories
out_dirs = [
    'papers/Paper5_ESP32_Deployment/figures',
    'papers/Paper5_ESP32_Deployment/submission/figures'
]
for d in out_dirs:
    os.makedirs(d, exist_ok=True)

# Set high-quality styling
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Helvetica', 'Arial', 'DejaVu Sans'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 9,
    'figure.titlesize': 13,
    'figure.dpi': 300
})

# -------------------------------------------------------------
# Figure 1: Physical Deployment & Benchmarking Pipeline
# -------------------------------------------------------------
fig, ax = plt.subplots(figsize=(7.4, 3.2), dpi=300)
ax.axis('off')
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)

# 4 Main Cards
cards = [
    ('1. FULL_INT8 Models', '4 MLP Artifacts\n176 to 412 params\n0 float32 tensors', 0.02, '#1A73E8', '#E8F0FE'),
    ('2. C-Byte Headers', 'Static Arrays (.h)\nROM Embedding\nSub-4 KB Footprint', 0.27, '#137333', '#E6F4EA'),
    ('3. ESP32 Silicon', 'Xtensa LX6 Core\n240 MHz Clock\n320 KB Static SRAM', 0.52, '#B06000', '#FEF7E0'),
    ('4. Zero-I/O Bench', 'In-RAM Timer Loop\nesp_timer_get_time\nN = 24,000 Trials', 0.77, '#C5221F', '#FCE8E6')
]

w, h = 0.21, 0.60
y_base = 0.32

for title, body, x, border, bg in cards:
    # Main card body (pad=0 ensures exact width w and height h without expansion)
    card_bg = patches.FancyBboxPatch((x, y_base), w, h, boxstyle='round,pad=0,rounding_size=0.02',
                                    facecolor=bg, edgecolor=border, linewidth=2.0)
    ax.add_patch(card_bg)
    # Header box
    header_h = 0.16
    header = patches.FancyBboxPatch((x, y_base + h - header_h), w, header_h,
                                   boxstyle='round,pad=0,rounding_size=0.02',
                                   facecolor=border, edgecolor=border, linewidth=1.0)
    ax.add_patch(header)
    # Header text
    ax.text(x + w/2, y_base + h - header_h/2, title, ha='center', va='center',
            fontsize=9.5, fontweight='bold', color='#FFFFFF')
    # Body text
    ax.text(x + w/2, y_base + (h - header_h)/2, body, ha='center', va='center',
            fontsize=8.5, fontweight='bold', color='#1A1A1A', linespacing=1.3)

# Connecting arrows
arrow_style = dict(arrowstyle='-|>', color='#202124', lw=2.2, mutation_scale=16)
for x_start in [0.23, 0.48, 0.73]:
    ax.annotate('', xy=(x_start + 0.04, y_base + h/2), xytext=(x_start, y_base + h/2),
                arrowprops=arrow_style)

# Bottom badges
badges = [
    ('Disk-Verified\nFlatBuffers', 0.02, '#1A73E8', '#E8F0FE'),
    ('Flash Partition\n1.25 MB Allocation', 0.27, '#137333', '#E6F4EA'),
    ('Bare-Metal TFLM\n916 B Tensor Arena', 0.52, '#B06000', '#FEF7E0'),
    ('Zero UART Delays\n0 B Dynamic Heap', 0.77, '#C5221F', '#FCE8E6')
]

bh = 0.20
for text, x, border, bg in badges:
    badge = patches.FancyBboxPatch((x, 0.05), w, bh, boxstyle='round,pad=0,rounding_size=0.015',
                                  facecolor=bg, edgecolor=border, linewidth=1.4)
    ax.add_patch(badge)
    ax.text(x + w/2, 0.05 + bh/2, text, ha='center', va='center',
            fontsize=8.0, fontweight='bold', color=border, linespacing=1.2)

plt.tight_layout()
for d in out_dirs:
    fig.savefig(os.path.join(d, 'physical_pipeline.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# -------------------------------------------------------------
# Figure 2: Mean ESP32 Latency & Percentiles across 4 Models
# -------------------------------------------------------------
models = ['student_a_8_4\n(176 params)', 'student_b_16_4\n(328 params)', 'mlp_12f\n(380 params)', 'mlp_14f\n(412 params)']
means = [64.55, 72.96, 76.77, 89.90]
p95s = [69.00, 83.00, 83.00, 95.00]
p99s = [76.00, 83.00, 90.00, 101.00]
maxs = [77.00, 84.00, 90.00, 102.00]

fig, ax = plt.subplots(figsize=(6.2, 3.8), dpi=300)
x = np.arange(len(models))
width = 0.5

bars = ax.bar(x, means, width, label='Mean Latency', color='#1A73E8', edgecolor='#174EA6', linewidth=1.2, alpha=0.85, zorder=3)

# Scatter indicators for percentiles and max
ax.scatter(x, p95s, color='#E37400', marker='^', s=60, label='P95 Percentile', zorder=5)
ax.scatter(x, p99s, color='#D93025', marker='s', s=55, label='P99 Percentile', zorder=5)
ax.scatter(x, maxs, color='#80868B', marker='x', s=65, label='Empirical Max', zorder=5)

# Value annotations above bars
for i, m in enumerate(means):
    ax.text(i, m + 1.8, f"{m:.2f} $\\mu$s", ha='center', va='bottom', fontsize=8.5, fontweight='bold', color='#174EA6')

ax.set_ylabel('Execution Latency ($\\mu$s)')
ax.set_title('On-Device Latency Distributions on ESP32-D0WD-V3 (240 MHz)', pad=10)
ax.set_xticks(x)
ax.set_xticklabels(models)
ax.set_ylim(0, 120)
ax.grid(True, linestyle='--', alpha=0.4, axis='y', zorder=0)
ax.legend(frameon=True, loc='upper left', framealpha=0.9)

# Annotation for 28.2% speedup
ax.annotate('28.2% Speedup', xy=(0, 64.55), xytext=(0.8, 48),
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2", color="#137333", lw=1.5),
            fontsize=8.5, fontweight='bold', color="#137333",
            bbox=dict(boxstyle="round,pad=0.2", facecolor="#E6F4EA", edgecolor="#137333", alpha=0.9))

plt.tight_layout()
for d in out_dirs:
    fig.savefig(os.path.join(d, 'latency_distributions.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# -------------------------------------------------------------
# Figure 3: Parameter Count vs Physical Latency Correlation
# -------------------------------------------------------------
params = np.array([176, 328, 380, 412])
latencies = np.array([64.55, 72.96, 76.77, 89.90])

fig, ax = plt.subplots(figsize=(5.5, 3.6), dpi=300)

# Linear fit
slope, intercept = np.polyfit(params, latencies, 1)
x_fit = np.linspace(150, 450, 100)
y_fit = slope * x_fit + intercept

# Compute R2
residuals = latencies - (slope * params + intercept)
ss_res = np.sum(residuals**2)
ss_tot = np.sum((latencies - np.mean(latencies))**2)
r2 = 1 - (ss_res / ss_tot)

ax.plot(x_fit, y_fit, color='#1A73E8', linestyle='--', label=f'Linear Fit ($R^2 = {r2:.3f}$)', lw=1.5, zorder=2)
ax.scatter(params, latencies, color='#D93025', s=80, edgecolor='#A50E0E', label='Measured Models (N=6,000/model)', zorder=4)

# Labels on points
labels = ['student_a', 'student_b', 'mlp_12f', 'mlp_14f']
for i, txt in enumerate(labels):
    offset_y = 2.5 if i != 1 else -4.5
    offset_x = 0 if i != 2 else -15
    ax.annotate(f"{txt}\n({latencies[i]:.2f} $\\mu$s)", (params[i], latencies[i]),
                xytext=(params[i] + offset_x, latencies[i] + offset_y),
                fontsize=8, ha='center', color='#202124')

ax.set_xlabel('Model Parameter Count')
ax.set_ylabel('Mean On-Device Latency ($\\mu$s)')
ax.set_title('Parameter Count vs. Physical Inference Latency', pad=10)
ax.set_xlim(140, 450)
ax.set_ylim(55, 105)
ax.grid(True, linestyle='--', alpha=0.4)
ax.legend(frameon=True, loc='upper left', framealpha=0.9)

plt.tight_layout()
for d in out_dirs:
    fig.savefig(os.path.join(d, 'params_vs_latency.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

# -------------------------------------------------------------
# Figure 4: Host x86 vs ESP32 Latency Comparison
# -------------------------------------------------------------
host_lats = [1.02, 0.98, 1.00, 1.43]
ratios = [63.28, 74.45, 76.77, 62.87]

fig, ax1 = plt.subplots(figsize=(6.2, 3.8), dpi=300)

x = np.arange(len(models))
w = 0.35

ax1.set_ylabel('Inference Latency ($\\mu$s)', color='#1A73E8')
rects1 = ax1.bar(x - w/2, means, w, label='ESP32 Physical Latency', color='#1A73E8', edgecolor='#174EA6', alpha=0.85)
rects2 = ax1.bar(x + w/2, host_lats, w, label='Host x86_64 Latency', color='#34A853', edgecolor='#137333', alpha=0.85)
ax1.tick_params(axis='y', labelcolor='#1A73E8')
ax1.set_ylim(0, 110)

ax2 = ax1.twinx()
ax2.set_ylabel('Host-to-ESP32 Slowdown Ratio', color='#D93025')
line1 = ax2.plot(x, ratios, color='#D93025', marker='o', lw=1.8, markersize=7, label='Slowdown Ratio ($\\times$)')
ax2.tick_params(axis='y', labelcolor='#D93025')
ax2.set_ylim(40, 95)

# Value annotations for ratios
for i, r in enumerate(ratios):
    ax2.annotate(f"{r:.1f}$\\times$", (x[i], r), xytext=(x[i], r + 2.5),
                 fontsize=8.5, ha='center', color='#A50E0E', fontweight='bold')

ax1.set_xticks(x)
ax1.set_xticklabels(models)
ax1.set_title('Host x86_64 vs. ESP32 Physical Execution Comparison', pad=10)

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left', framealpha=0.9)

plt.tight_layout()
for d in out_dirs:
    fig.savefig(os.path.join(d, 'host_vs_esp32.png'), dpi=300, bbox_inches='tight')
plt.close(fig)

print("All 4 publication figures generated successfully in both directories.")
