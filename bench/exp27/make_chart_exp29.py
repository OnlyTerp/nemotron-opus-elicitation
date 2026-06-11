#!/usr/bin/env python3
"""EXP28/29 chart: the recognition/simulation split and the harness fix."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = "/home/terp/nemotron-opus-elicitation/assets"
BG = "#0d1117"; FG = "#e6edf3"; GRID = "#21262d"
COLD_C = "#8b949e"; V_C = "#7A84FF"; GREEN = "#35C89A"; RED = "#e5534b"; GOLD = "#F29A45"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG, "xtick.color": FG, "ytick.color": FG,
    "axes.edgecolor": GRID, "font.size": 12, "font.family": "DejaVu Sans",
})

# Distraction-framed bug catch rate across all conditions (5-bug comparable set:
# BF01, BF02, BF03, BF05, BF06 — BF04 excluded as saturated)
conds = ["Cold\n(no prompt)", "v21\n(1900-word\narchitecture)", "v22\n(+audit\nclause)", "v23\n(bugs named\nverbatim!)", "Harness\ninjection\n(~30 tokens)"]
vals = [1, 1, 1, 0, 4]  # of 5 comparable items (BF04 excluded)
colors = [COLD_C, V_C, V_C, V_C, GOLD]

fig, ax = plt.subplots(figsize=(11, 5.6))
bars = ax.bar(conds, vals, width=0.55, color=colors, edgecolor=GRID)
for rect, v in zip(bars, vals):
    ax.text(rect.get_x() + rect.get_width()/2, v + 0.08, f"{v}/5",
            ha="center", fontsize=15, fontweight="bold")
ax.axhline(5, color=GRID, linewidth=1, linestyle="--")
ax.set_ylim(0, 5.7)
ax.set_ylabel("hidden bugs caught (5 comparable items)")
ax.set_title('The distraction gap: buggy code + "works fine" + side question\nNo system prompt moved it. One harness-injected task line did.',
             fontsize=13, fontweight="bold", pad=12)
ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.annotate('v23\'s system prompt literally describes\nthese exact bugs — still misses them',
            xy=(3, 0.15), xytext=(2.6, 2.2), ha="center", fontsize=9.5, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1))
ax.annotate('"[automated note: code detected —\ntrace it on one small input...]"\nappended to the TASK',
            xy=(4, 4), xytext=(3.6, 4.95), ha="center", fontsize=9.5, color=GOLD)
fig.text(0.5, 0.005, "EXP27c/28/29 — all bugs executed & verified · same items, same model (nemotron-3-ultra-high) · correct-code control stayed clean in every condition",
         ha="center", fontsize=9, color=COLD_C)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(f"{OUT}/exp29_harness.png", dpi=160)
print("wrote exp29_harness.png")
