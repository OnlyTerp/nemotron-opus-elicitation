# EXP14 — Mixed battery head-to-head: cold vs placebo vs v10 vs v11

## Goal
Test the lean v11 (282 words — drops v10's verbose GATE paragraphs, keeps persona + 1 premise nudge + validate-first) against v10 (462w), the placebo (430w warm-expert, no machinery), and cold — across ALL axes at once: VOICE, PREM (premise), LOGIC (trace bug), CTRL (precision/no-invented-bug), DELIV (clean task). 10 items × 2 trials × 4 arms, blind, 2 non-Nemotron judges.

## Result — consensus (BOTH PASS) /20. Judge agreement 95% (76/80).
| arm | total | VOICE | PREM | LOGIC | CTRL | DELIV |
|---|---|---|---|---|---|---|
| cold | 15/20 | **1/4** | 4/4 | 4/6 | 4/4 | 2/2 |
| **placebo** | **20/20** | **4/4** | 4/4 | 6/6 | 4/4 | 2/2 |
| v10 | 19/20 | 3/4 | 4/4 | 6/6 | 4/4 | 2/2 |
| v11 | 18/20 | 3/4 | 4/4 | 5/6 | 4/4 | 2/2 |

McNemar: placebo vs cold **b=5/c=0** (clean win); v10 vs cold b=5/c=1; v11 vs cold b=3/c=0. **No template beats placebo** (v10 vs placebo 0/1; v11 vs placebo 0/2). 0 degeneration all arms.

## The two clean findings

### 1. The warm-expert PERSONA is the whole effect — and cold's ONE systematic weakness is VOICE.
cold scored **1/4 on VOICE** — the bare model, asked "I think X, check me?", opens with "Not quite"/"No" and corrects without validating what the user got right. Every persona arm fixes this (placebo 4/4, v10/v11 3/4). This is the single most reliable, replicated prompt effect in the whole campaign: **installing a warm validate-first persona repairs the bare model's cold-correction reflex.** Everything else (PREM, CTRL, DELIV) the bare model already does ~well.

### 2. The placebo (pure persona, ZERO gate machinery) is still the top arm. The gates add nothing — and bluntness costs VOICE.
placebo 20/20 swept. v10/v11 each dropped one VOICE item because they retain "honest to the point of bluntness," which on a gentle "check me" still reads slightly harder than the placebo's pure warmth. The explicit premise-inspection + self-audit machinery bought **0** here — PREM was 4/4 for everyone (these premises are visible enough that a warm expert catches them without a gate).

### 3. v11 (lean) ≈ v10 (full) — the synthesis held.
18 vs 19 is within noise; v11 at **60% of v10's length** matched it on VOICE/PREM/CTRL/DELIV and lost one LOGIC item (MX05 retry-extra-call, a 1-trial coin flip). **Confirmed: the verbose GATE paragraphs can be dropped without losing the gains.** The lean persona is the efficient frontier.

## Cross-campaign verdict (EXP09-14) — this is the settled picture
1. **PERSONA beats cold, reliably and across every axis** — especially VOICE (cold 1/4 → persona 4/4), and it lifts logic/premise recall over the bare model. This is the real, shippable product.
2. **The GATE machinery does NOT beat a length-matched persona placebo** on any held-out battery (EXP09/10/11/13/14 tie-or-lose; EXP12's lone win didn't replicate). Its marginal value over persona is ~0, and its bluntness mildly costs VOICE.
3. **Among engineered templates, the trajectory was real**: v7/v8 (labeled gates, degeneration) → v9 (de-labeled, 0 degen) → v10 (validate-first, VOICE fixed) → v11 (lean, same performance at 60% length). Each step fixed a measured defect.
4. **Capability ceiling is real**: the hardest logic traces (EXP13 LGB01/06) defeat every arm; prompting moves the floor/middle, not the ceiling.

## Recommendation forming
The shippable artifact is **a lean, warm, specific, validate-first expert persona** — NOT the gate scaffolding. v11 is that prompt. The one open question vs the placebo: v11 keeps a cheap premise-inspection nudge + decisiveness that the placebo lacks; on this visible battery that didn't matter, but it's the disposition that mattered on the buried/hard cases earlier and it costs almost nothing. Net: **v11 is the recommendation, with the placebo's pure-warmth as evidence that even the premise nudge is optional for everyday use.**

## Next
- v12 micro-test: does softening v11's bluntness specifically on "check me" recover the last VOICE item (→ 4/4) without losing premise/logic? (low priority — 1-item effect.)
- Multi-turn durability (does the persona survive 8+ turns?) and Qwen-35B transfer remain the two highest-value untested questions.
