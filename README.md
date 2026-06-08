# Nemotron × Opus Elicitation

**Goal:** Get Opus-4.8-grade *reasoning, reliability, and personality* out of **Nemotron 3 Ultra** through prompting alone — **no fine-tuning**.

## The core bet — and what 15 experiments actually showed

**Original hypothesis:** Nemotron has Opus-grade capability; what it lacks are *dispositions* (premise-questioning, self-audit, validate-first honesty, dense reasoning). Install those via an explicit GATE template (premise-check + hostile self-audit) and you elicit Opus-like behavior. "It was always there, just hidden."

**What the controlled experiments (EXP09-15) actually found — read this first, it overturns the original framing:**

1. **The active ingredient is the PERSONA, not the gates.** A length-matched "warm, specific, validate-first senior expert" prompt with **none** of the explicit premise-check/self-audit machinery beats the bare model on every axis — and **ties or beats every gated template** on five held-out blind batteries. The elaborate GATE scaffolding this project was built around adds ~0 over a good persona, and its bluntness mildly *hurts* the validate-first voice.
2. **The single most reliable, replicated effect: persona fixes the bare model's VOICE.** Cold Nemotron, asked "I think X, check me?", opens "No/Not quite" and corrects without acknowledging what's right (EXP14: cold 1/4 on VOICE). Any warm persona repairs this (4/4). This is the real, shippable win.
3. **Capability ceiling is real.** The hardest logic-trace bugs (a `range(len-k)` off-by-one, a floor-division average) are missed by *every* arm. Prompting moves the floor and the middle, not the ceiling.
4. **The engineered-template trajectory was still real progress:** v7/v8 (labeled gates → process-narration + repetition degeneration) → **v9** (de-labeled, 0 degeneration) → **v10** (validate-first, fixes VOICE) → **v11** (lean, drops the verbose gate paragraphs, matches v10 at ~60% the length). Each step fixed a *measured* defect.
5. **The persona is multi-turn durable** (EXP15): it survives 8 turns of real conversation without decaying to cold's blunt reflex.

**Bottom line:** the shippable artifact is a **lean warm-expert persona** (`templates/v11_lean_synthesis.md`), not the gate machinery. The "elicitation not capability" thesis holds — but the lever is *persona inhabitation*, which Nemotron (a top roleplay model) performs, not an explicit reasoning-scaffold.

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
- ✅ EXP05 (false-positive pilot): v3 FPR **0/8** on premise-clean tasks — no gross over-skepticism; recall 2/2. (n small; 2 mild issues: over-refusal, audit-theater.)
- ✅ EXP06 (v5/v6 calibrated templates): triage fixed over-refusal but **systematically regressed recall** (CUDA 0/4) — precision & recall are coupled through the SOUND-default. Neither dominates.
- ✅ EXP07 (**v7 = v3 + one "deliver corrected work" clause**): **CUDA recall 3/3 + SHA-256 over-refusal fixed + clean** — minimal change beat the redesigns.
- ✅ EXP08 (**v8 = v7 + Opus-personality/GPT-rigor voice layer**): personality delivered (validate-first, dense, decisive); CUDA recall **5/6** (~parity with v7); one ~1/6 degeneration tail to watch.
- ➡️ **Two candidates:** `templates/v7_v3_plus_deliver.md` (max-reliability core) and `templates/v8_voice_layer.md` (push-past-parity: feels like Opus, reasons structured+decisive). External confirmatory decides on macro-success + degeneration rate.

### Headline result (EXP03, blind-confirmed)
On the exact buried-premise trap that broke v2, same model:

| Arm | PASS | PARTIAL | FAIL |
|-----|------|---------|------|
| COLD | 1 | 2 | 2 |
| TMPL v2 | 0 | 1 | 4 |
| **TMPL v3** | **4** | 0 | 1 |

The lever was **ordering** (premise-check before any "show me the code"), not "more reasoning." Capability was always there; the template makes it fire reliably.
