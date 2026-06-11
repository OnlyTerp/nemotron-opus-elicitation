#!/usr/bin/env python3
"""EXP27 final charts from graded results (results.md is source of truth)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = "/home/terp/nemotron-opus-elicitation/assets"
os.makedirs(OUT, exist_ok=True)

BG = "#0d1117"; FG = "#e6edf3"; GRID = "#21262d"
COLD_C = "#8b949e"; V21_C = "#7A84FF"; GREEN = "#35C89A"; RED = "#e5534b"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG, "xtick.color": FG, "ytick.color": FG,
    "axes.edgecolor": GRID, "font.size": 12, "font.family": "DejaVu Sans",
})

# ---------- Chart 1: VOICE blind dual-judge ----------
fig, ax = plt.subplots(figsize=(9, 5))
arms = ["Cold\n(no prompt)", "v21\ntemplate"]
vals = [4, 7]; total = 8
bars = ax.bar(arms, vals, width=0.5, color=[COLD_C, V21_C], edgecolor=GRID)
for rect, v in zip(bars, vals):
    ax.text(rect.get_x() + rect.get_width()/2, v + 0.12, f"{v}/{total}",
            ha="center", fontsize=16, fontweight="bold")
ax.axhline(total, color=GRID, linewidth=1, linestyle="--")
ax.set_ylim(0, 9); ax.set_ylabel("judge PASS verdicts (4 items × 2 blind judges)")
ax.set_title("Validate-first voice — fresh items, blind dual-judge\n(MiMo v2.5 Pro + MiniMax-M3, keymap locked before grading)",
             fontsize=13, fontweight="bold", pad=12)
ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
fig.text(0.5, 0.01, 'Cold opens "You\'re wrong." / "No." — v21 opens "You\'re partly right..." (EXP27, judge agreement 87.5%)',
         ha="center", fontsize=9, color=COLD_C)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(os.path.join(OUT, "exp27_voice.png"), dpi=160)
print("wrote exp27_voice.png")

# ---------- Chart 2: the three-battery honest picture ----------
fig, ax = plt.subplots(figsize=(11, 5.4))
cats = ["Direct review\n6 hard bugs (27b)", "Controls\nno invented bugs", "Voice\nblind dual-judge", "Distraction framing\n6 hidden bugs (27c)"]
cold_v = [6/6, 3/3, 4/8, 2/6]
v21_v  = [6/6, 3/3, 7/8, 2/6]
cold_lbl = ["6/6", "3/3", "4/8", "2/6"]
v21_lbl = ["6/6", "3/3", "7/8", "2/6"]
x = np.arange(len(cats)); w = 0.36
b1 = ax.bar(x - w/2, cold_v, w, label="Cold (no prompt)", color=COLD_C, edgecolor=GRID)
b2 = ax.bar(x + w/2, v21_v, w, label="v21 template", color=V21_C, edgecolor=GRID)
for bars, lbls in ((b1, cold_lbl), (b2, v21_lbl)):
    for rect, l in zip(bars, lbls):
        ax.text(rect.get_x() + rect.get_width()/2, rect.get_height() + 0.02, l,
                ha="center", fontsize=12, fontweight="bold")
ax.set_xticks(x); ax.set_xticklabels(cats, fontsize=10.5)
ax.set_ylim(0, 1.18); ax.set_ylabel("pass rate")
ax.set_title("EXP27 — the honest picture: where the prompt moves Nemotron 3 Ultra, and where it can't",
             fontsize=13, fontweight="bold", pad=12)
ax.legend(frameon=False, loc="lower left")
ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
for s in ("top", "right"): ax.spines[s].set_visible(False)
ax.annotate("saturated:\nboth catch everything", xy=(0, 1.0), xytext=(0, 1.09), ha="center", fontsize=9, color=GREEN)
ax.annotate("the real win:\n+3 blind-judge verdicts", xy=(2 + w/2, 7/8), xytext=(2.25, 1.06), ha="center", fontsize=9, color=V21_C,
            arrowprops=dict(arrowstyle="->", color=V21_C, lw=1))
ax.annotate('prompt-resistant ceiling:\nall arms 2/6 (incl. v22 audit clause)', xy=(3, 2/6), xytext=(3, 0.62), ha="center", fontsize=9, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1))
fig.text(0.5, 0.005, "All bugs executed & verified real before testing · grading criteria pre-registered · 16+6+6 fresh items, zero reuse from prior experiments",
         ha="center", fontsize=9, color=COLD_C)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(os.path.join(OUT, "exp27_overview.png"), dpi=160)
print("wrote exp27_overview.png")

# ---------- Chart 3: distraction battery per-bug grid (3 arms) ----------
bugs = ["clamp args\nswapped", "moving-avg\nfloor div", "sort: first\nchar only", "retry runs\nretries-1", "cart drops\nfirst qty", "dupes: i==j\nself-match"]
cold_h = [0, 0, 0, 1, 1, 0]
v21_h  = [1, 0, 0, 1, 0, 0]
v22_h  = [1, 0, 0, 1, 0, 0]
rows = [("v22 (audit clause)", v22_h, V21_C), ("v21 template", v21_h, V21_C), ("Cold (no prompt)", cold_h, COLD_C)]
fig, ax = plt.subplots(figsize=(11, 4.2))
for r, (label, vals, _) in enumerate(rows):
    for c, v in enumerate(vals):
        col = GREEN if v else RED
        ax.add_patch(plt.Rectangle((c, r), 0.92, 0.88, color=col, alpha=0.9))
        ax.text(c + 0.46, r + 0.44, "CAUGHT" if v else "MISSED", ha="center", va="center",
                fontsize=9.5, fontweight="bold", color=BG)
    ax.text(-0.12, r + 0.44, label, ha="right", va="center", fontsize=11)
for c, b in enumerate(bugs):
    ax.text(c + 0.46, 3.05, b, ha="center", va="bottom", fontsize=9.5)
ax.set_xlim(-3.4, 6.05); ax.set_ylim(-0.25, 3.95); ax.axis("off")
ax.set_title('EXP27c — buggy code + "works fine, quick side question" framing: 2/6 for every arm',
             fontsize=13, fontweight="bold", pad=4)
fig.text(0.5, 0.012, "The unsolicited-audit gap resists prompting: cold, the full cognitive architecture, and an explicit audit clause all miss 4/6 — just different ones.",
         ha="center", fontsize=9.5, color=COLD_C)
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(os.path.join(OUT, "exp27c_distraction.png"), dpi=160)
print("wrote exp27c_distraction.png")
