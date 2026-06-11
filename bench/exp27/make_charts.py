#!/usr/bin/env python3
"""EXP27/27b chart generation. Data filled from graded results (results.md is source of truth)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "..", "assets")
os.makedirs(OUT, exist_ok=True)

BG = "#0d1117"; FG = "#e6edf3"; GRID = "#21262d"
COLD_C = "#8b949e"; V21_C = "#7A84FF"; ACCENT = "#35C89A"

plt.rcParams.update({
    "figure.facecolor": BG, "axes.facecolor": BG, "savefig.facecolor": BG,
    "text.color": FG, "axes.labelcolor": FG, "xtick.color": FG, "ytick.color": FG,
    "axes.edgecolor": GRID, "font.size": 12, "font.family": "DejaVu Sans",
})

# ---- DATA (filled after grading; see results.md) ----
# EXP27 main battery
main_cats = ["Silent bugs\n(6 items)", "False premises\n(3 items)", "Controls: no\ninvented bugs (3)", "Voice: validate\nfirst (4, blind)"]
cold_main = [6, 2, 3, None]   # voice filled from dual-judge
v21_main  = [6, 2, 3, None]
# Voice from dual-judge consensus (judge agreement noted in results.md)
COLD_VOICE = None  # fill
V21_VOICE = None   # fill

# EXP27b hard battery (6 executed-verified bugs); per-bug catch detail
hard_bugs = ["LRU get()\nno refresh", "percentile\nq=1.0 crash", "add_months\nDec crash", "avg of avgs\nweighting", "set() order\ndestroyed", "chunker\ndrops tail"]
cold_hard = [None]*6  # fill 1/0
v21_hard  = [None]*6  # fill 1/0


def bar_compare(labels, cold_vals, v21_vals, totals, title, fname, judge_note=""):
    x = np.arange(len(labels)); w = 0.36
    fig, ax = plt.subplots(figsize=(10, 5.4))
    b1 = ax.bar(x - w/2, cold_vals, w, label="Cold (no prompt)", color=COLD_C, edgecolor=GRID)
    b2 = ax.bar(x + w/2, v21_vals, w, label="v21 template", color=V21_C, edgecolor=GRID)
    for bars, vals in ((b1, cold_vals), (b2, v21_vals)):
        for rect, v, t in zip(bars, vals, totals):
            ax.text(rect.get_x() + rect.get_width()/2, v + 0.06, f"{v}/{t}",
                    ha="center", va="bottom", fontsize=11, fontweight="bold")
    ax.set_xticks(x); ax.set_xticklabels(labels)
    ax.set_ylim(0, max(totals) + 1.1)
    ax.set_ylabel("items passed")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=14)
    ax.legend(frameon=False, loc="upper right")
    ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    if judge_note:
        fig.text(0.5, 0.005, judge_note, ha="center", fontsize=9, color=COLD_C)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=160)
    print("wrote", fname)


def per_bug_grid(bugs, cold_vals, v21_vals, fname):
    fig, ax = plt.subplots(figsize=(10, 3.4))
    for row, (vals, label, color) in enumerate(
        ((v21_vals, "v21 template", V21_C), (cold_vals, "Cold (no prompt)", COLD_C))):
        for col, v in enumerate(vals):
            c = (ACCENT if v else "#d9534f")
            ax.add_patch(plt.Rectangle((col, row), 0.92, 0.92, color=c, alpha=0.92))
            ax.text(col + 0.46, row + 0.46, "CAUGHT" if v else "MISSED",
                    ha="center", va="center", fontsize=9.5, fontweight="bold", color=BG)
        ax.text(-0.15, row + 0.46, label, ha="right", va="center", fontsize=11.5)
    for col, b in enumerate(bugs):
        ax.text(col + 0.46, 2.12, b, ha="center", va="bottom", fontsize=9.5)
    ax.set_xlim(-3.2, len(bugs)); ax.set_ylim(-0.2, 3.1); ax.axis("off")
    ax.set_title("EXP27b — 6 executed-and-verified silent bugs (review-resistant bank)",
                 fontsize=13, fontweight="bold", pad=2)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=160)
    print("wrote", fname)


if __name__ == "__main__":
    assert COLD_VOICE is not None, "fill grades first"
    cold_main[3] = COLD_VOICE; v21_main[3] = V21_VOICE
    bar_compare(main_cats, cold_main, v21_main, [6, 3, 3, 4],
                "EXP27 — fresh 16-item battery: cold Nemotron 3 Ultra vs v21",
                "exp27_main.png",
                "Voice graded blind by two non-Nemotron judges (MiMo v2.5 Pro + MiniMax-M3); objective items graded against pre-registered criteria")
    per_bug_grid(hard_bugs, cold_hard, v21_hard, "exp27b_hard.png")
