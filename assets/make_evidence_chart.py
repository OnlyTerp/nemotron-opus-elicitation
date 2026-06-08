#!/usr/bin/env python3
"""Render assets/evidence.png — cold (bare Nemotron) vs v16 pass-rates on the
axes where the campaign shows a clean before/after. Numbers trace to the
experiments cited in README.md / THESIS.md.

Run: python3 assets/make_evidence_chart.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# Theme
BG = "#141414"; GRID = "#2E2E2E"; TICK = "#C7D2FE"; TITLE = "#F3F4F6"
LEG = "#D1D5DB"; SUB = "#9CA3AF"
COLD = "#6F8DA6"   # neutral supporting
V16 = "#7A84FF"    # primary series

# (label, cold %, v16 %, experiment)
data = [
    ("Validate-first\nVOICE",            25,  100, "EXP14"),
    ("Silent code-bug\nrecall",          20,  100, "EXP17"),
    ("Clean-code precision\n(no false bugs)", 100, 100, "EXP05/14"),
    ("Mixed battery\noverall",           53,  100, "EXP23"),
    ("Process-narration\n(clean = high)", 85,  100, "EXP09"),
]
labels = [d[0] for d in data]
cold = [d[1] for d in data]
v16 = [d[2] for d in data]
exps = [d[3] for d in data]

x = np.arange(len(labels))
w = 0.38

fig, ax = plt.subplots(figsize=(12, 6))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)

b1 = ax.bar(x - w/2, cold, w, label="cold (bare Nemotron)", color=COLD, edgecolor=BG)
b2 = ax.bar(x + w/2, v16, w, label="v16 (recommended)", color=V16, edgecolor=BG)

for bars in (b1, b2):
    for r in bars:
        h = r.get_height()
        ax.text(r.get_x() + r.get_width()/2, h + 2, f"{int(h)}%",
                ha="center", va="bottom", color=TITLE, fontsize=11, fontweight="bold")

for xi, e in zip(x, exps):
    ax.text(xi, -13, e, ha="center", va="top", color=SUB, fontsize=9)

ax.set_title("Bare Nemotron 3 Ultra vs v16 — pass-rate by axis",
             color=TITLE, fontsize=16, fontweight="bold", pad=16)
ax.set_ylabel("Pass rate (%)", color=TICK, fontsize=12)
ax.set_ylim(0, 130)
ax.set_xticks(x)
ax.set_xticklabels(labels, color=TICK, fontsize=10.5)
ax.tick_params(axis="y", colors=TICK)
ax.tick_params(axis="x", length=0)
for s in ax.spines.values():
    s.set_visible(False)
ax.yaxis.grid(True, color=GRID, linewidth=1)
ax.set_axisbelow(True)

leg = ax.legend(loc="upper center", bbox_to_anchor=(0.5, 0.99), ncol=2,
                frameon=False, fontsize=11, handlelength=1.4, columnspacing=2.2)
for t in leg.get_texts():
    t.set_color(LEG)

fig.text(0.5, 0.005, "Blind dual non-Nemotron judges (MiMo v2.5 Pro + MiniMax-M3), 80–98% agreement",
         ha="center", color=SUB, fontsize=10)

plt.tight_layout()
out = __file__.rsplit("/", 1)[0] + "/evidence.png"
plt.savefig(out, dpi=200, facecolor=BG, bbox_inches="tight")
print("wrote", out)
