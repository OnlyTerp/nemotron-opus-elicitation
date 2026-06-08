# Nemotron × Opus Elicitation

**Goal:** Get Opus-4.8-grade *reasoning, reliability, and personality* out of **Nemotron 3 Ultra** through prompting alone — **no fine-tuning**.

## The core bet

Nemotron 3 Ultra already has the raw capability to reason at Opus's level. What it lacks is not intelligence — it's the *dispositions* that make Opus effective:

- questioning premises before acting,
- self-auditing to catch its own errors,
- honesty (including with itself),
- dense, token-efficient reasoning,
- a consistent, durable thinking style.

The hypothesis: these are **elicitation gaps, not capability gaps**. A good enough prompt template unlocks them. "It was always there, just hidden."

## What's in here

| Path | What |
|------|------|
| `THESIS.md` | The evolving central hypothesis + what each experiment taught us |
| `templates/v2_persona_gate.md` | **Current** template: persona-inhabitation + a forced self-audit gate |
| `templates/v1_checklist_DEPRECATED.md` | First attempt (rigid checklist) — kept as a cautionary example |
| `findings/opus_vs_default_differences.md` | 12 systematic Opus-vs-default behavioral differences (from dataset analysis) |
| `findings/dataset_provenance.md` | Which HuggingFace "Opus" datasets are real vs synthetic garbage |
| `experiments/EXP0*.md` | Each test: design, hypothesis, raw results, scoring, honest caveats |
| `experiments/raw/` | Unedited subagent outputs |

## Method

Every claim here is tested against the **live Nemotron 3 Ultra** (via `run_subagent --profile nemotron-ultra`), comparing two arms:
- **COLD** — Nemotron with no added prompt (true baseline).
- **TMPL** — Nemotron with the v2 template prepended.

We measure *behavioral* differences (does it challenge a false premise, catch an error, etc.), run multiple trials per arm to expose variance, and — from EXP03 on — grade **blind** with a neutral judge to remove author bias.

## Methodology rules (operating discipline)
1. **Cap both arms at ≤180 words** per response. Keeps the test fair (length isn't a confound) AND prevents runaway / repetition-loop generations. (EXP04 cold runs degenerated into garbage when uncapped.)
2. **Short timeouts; abandon runaways fast.** Never block-wait on a single agent that's run away — drop it.
3. **Don't over-spawn.** Smallest n that's informative; scale up only when a result is close.
4. **Blind-grade** when a result favors the author's hypothesis or is close.

## Status (living)

- ✅ Documented Opus's distinctive reasoning behaviors
- ✅ Built v2 template (persona + gate)
- ✅ EXP01 (flagrant bad data): both arms caught it; template avoided an overclaim
- ✅ EXP02 (obvious false premise, n=3): same ceiling; **template raised the floor** + transferred bluntness
- ✅ EXP03 (buried false premise CUDA, n=5/arm, blind-graded): **v2 regressed (0/5)**, **v3 fixed it and beat cold (4/5 vs 1/5)**
- ✅ EXP04 (generalization, buried premise HTTP/UDP, n=6): **v3 6/6 vs cold 0/5** — v3 generalizes, not overfit. Bonus: cold degenerated into garbage loops chasing the wrong path.
- ➡️ **Current best template: `templates/v3_premise_first.md`**

### Headline result (EXP03, blind-confirmed)
On the exact buried-premise trap that broke v2, same model:

| Arm | PASS | PARTIAL | FAIL |
|-----|------|---------|------|
| COLD | 1 | 2 | 2 |
| TMPL v2 | 0 | 1 | 4 |
| **TMPL v3** | **4** | 0 | 1 |

The lever was **ordering** (premise-check before any "show me the code"), not "more reasoning." Capability was always there; the template makes it fire reliably.
