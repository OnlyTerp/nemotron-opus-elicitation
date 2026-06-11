#!/usr/bin/env python3
"""Viral hero graphic: stock Nemotron vs the full stack (v21 persona + forced-verdict harness check)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import numpy as np

OUT = "/home/terp/nemotron-opus-elicitation/assets/hero_viral.png"
BG = "#0a0e14"; PANEL = "#11161f"; FG = "#e6edf3"; DIM = "#7d8590"; GRID = "#1d2330"
RED = "#f0524b"; GREEN = "#3fcf8e"; PURPLE = "#8b7cff"; GOLD = "#f5a953"

fig = plt.figure(figsize=(16, 9), facecolor=BG)

# ---------- title ----------
fig.text(0.5, 0.945, "We rebuilt Nemotron 3 Ultra's brain with 29 controlled experiments",
         ha="center", fontsize=23, fontweight="bold", color=FG)
fig.text(0.5, 0.895, "same 550B model · zero fine-tuning · blind dual-judge grading · every bug executed & verified real",
         ha="center", fontsize=12.5, color=DIM)

# ---------- left panel: the three measured wins ----------
axL = fig.add_axes((0.045, 0.10, 0.42, 0.72)); axL.set_facecolor(BG); axL.axis("off")
axL.set_xlim(0, 10); axL.set_ylim(0, 10)

rows = [
    ("Warm, validate-first voice", "blind dual-judge, fresh items", 4/8, 7/8, "4/8", "7/8"),
    ("Hidden-bug catch rate", 'buggy code + "works fine" framing', 1/5, 5/5, "1/5", "5/5"),
    ("Silent-bug code review", "EXP17 bank, boundary-input checks", 2/10, 10/10, "2/10", "10/10"),
]
y = 8.6
for title, sub, v0, v1, l0, l1 in rows:
    axL.text(0.1, y + 0.62, title, fontsize=15, fontweight="bold", color=FG)
    axL.text(0.1, y + 0.13, sub, fontsize=10, color=DIM)
    # stock bar
    axL.add_patch(FancyBboxPatch((0.1, y - 0.62), 6.6, 0.46, boxstyle="round,pad=0.02",
                                 fc=GRID, ec="none"))
    axL.add_patch(FancyBboxPatch((0.1, y - 0.62), max(6.6 * v0, 0.3), 0.46, boxstyle="round,pad=0.02",
                                 fc=RED, ec="none"))
    axL.text(6.95, y - 0.40, f"stock  {l0}", fontsize=11.5, color=RED, va="center", fontweight="bold")
    # upgraded bar
    axL.add_patch(FancyBboxPatch((0.1, y - 1.32), 6.6, 0.46, boxstyle="round,pad=0.02",
                                 fc=GRID, ec="none"))
    axL.add_patch(FancyBboxPatch((0.1, y - 1.32), 6.6 * v1, 0.46, boxstyle="round,pad=0.02",
                                 fc=GREEN, ec="none"))
    axL.text(6.95, y - 1.10, f"ours  {l1}", fontsize=11.5, color=GREEN, va="center", fontweight="bold")
    y -= 3.0

# ---------- right panel: the receipts ----------
axR = fig.add_axes((0.50, 0.10, 0.465, 0.72)); axR.set_facecolor(BG); axR.axis("off")
axR.set_xlim(0, 10); axR.set_ylim(0, 10)

def card(ax, x, y, w, h, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                fc=PANEL, ec=color, lw=1.6))

# stock card
card(axR, 0.2, 6.7, 9.4, 2.6, RED)
axR.text(0.55, 8.78, "STOCK", fontsize=11, fontweight="bold", color=RED)
axR.text(0.55, 8.18, 'you: "my code works fine — quick side question?"', fontsize=11.5, color=DIM, style="italic")
axR.text(0.55, 7.58, 'it answers the side question. The broken clamp,', fontsize=12.5, color=FG)
axR.text(0.55, 7.06, 'the wrong median, the off-by-one — all shipped.', fontsize=12.5, color=FG)

# arrow
axR.annotate("", xy=(5.0, 5.6), xytext=(5.0, 6.45),
             arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=3))
axR.text(5.25, 5.95, "persona v21 + 60-token harness check", fontsize=10.5, color=GOLD)

# upgraded card
card(axR, 0.2, 1.6, 9.4, 3.9, GREEN)
axR.text(0.55, 5.06, "OURS", fontsize=11, fontweight="bold", color=GREEN)
axR.text(0.55, 4.42, 'traces your code before answering — every time:', fontsize=12.5, color=FG)
axR.text(0.55, 3.74, 'moving_avg([1,2,3,4], 2) → [1, 2, 3]  (int)', fontsize=12, color=FG, family="monospace")
axR.text(0.55, 3.22, 'correct → [1.5, 2.5, 3.5]  (float)', fontsize=12, color=FG, family="monospace")
axR.text(0.55, 2.62, 'MISMATCH — // truncates your averages', fontsize=12.5, color=RED, family="monospace", fontweight="bold")
axR.text(0.55, 2.0, '...then answers your actual question. "Hell yeah" when', fontsize=11.5, color=DIM)
axR.text(0.55, 1.52, "you're hyped, \"you're partly right\" when you're not.", fontsize=11.5, color=DIM)

# honest footnote + repo
fig.text(0.5, 0.045, "and the honest part: we also found what prompts CAN'T do — full methodology, all 29 experiments, blind grades, charts:",
         ha="center", fontsize=11, color=DIM)
fig.text(0.5, 0.012, "github.com/OnlyTerp/nemotron-opus-elicitation", ha="center",
         fontsize=14.5, color=PURPLE, fontweight="bold", family="monospace")

fig.savefig(OUT, dpi=170, facecolor=BG)
print("wrote", OUT)
