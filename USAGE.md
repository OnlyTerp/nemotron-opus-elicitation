# Usage — how to actually use this

This project's deliverable is **not** a magic prompt. It's a method plus one concrete artifact that applies it to Nemotron 3 Ultra.

## TL;DR
- **Recommended prompt:** `templates/v13_lean_verify.md` (the system-prompt block between the BEGIN/END markers). For pure non-code chat, `templates/v11_lean_synthesis.md` (same minus the code clause) is equivalent.
- **What it reliably buys you on Nemotron 3 Ultra:** (1) a warm, *validate-first* voice (acknowledges what's right before correcting), specificity, decisiveness, a cheap premise-first reflex — with **zero** degeneration / over-refusal / process-narration; PLUS (2) **execute-verify on code**: it checks a function's actual output on a boundary input instead of eyeballing it, which catches silent-wrong-output bugs the bare model misses (recall **2/10 → 10/10** on the hardest off-by-one/wrong-formula items, with no increase in false alarms).
- **What it does NOT buy you:** general raw intelligence. Outside code-correctness, it does not beat a plain warm-expert prompt on premise/bug catching — those are baseline capability already present. The execute-verify gain is specific to "is this code actually correct" tasks.

## When to use it
Use v11 when the bare model's **default disposition** is the problem — for Nemotron specifically, when you dislike that it:
- opens corrections with a flat "No." and never says what the user got right ("check me" / teaching / code-review contexts),
- under-validates a user's partially-correct mental model,
- is terser/colder than you want.

**Do NOT bother** if your base model is already warm and validate-first. We tested this: on **Qwen3.6-35B**, v11 was a measured **no-op** (cold 11/12 = v11 11/12) because Qwen already validates-first. Adding a persona to a model that already has the disposition just costs tokens.

## The execute-verify lever (the one capability gain)
The single change that improved *correctness* (not just tone) was a clause telling the model: **when code is involved, don't trust a read-through — check the actual output on a concrete boundary input (even-length list, n=0/1, the empty case) before judging it.** On silent-wrong-output bugs (off-by-ones, floor-division averages, dropped-last-window) this took recall from cold 2/10 to 10/10, with no extra false positives.
- **You do NOT need a sandbox for review-sized snippets.** Mentally checking a concrete input tied actually running the code (EXP18) — Nemotron either knows the gotcha as a fact or can simulate small functions once told to.
- **Use a real sandbox** only when the output genuinely can't be predicted by eye: large/stateful code, real I/O, heavy numeric work, unfamiliar libraries. There the disposition still helps but the tool is what guarantees the answer.
- It's baked into `v13`. If you're on `v11`, the clause to add is one sentence (see `templates/v13_lean_verify.md` diff).

## The method (the generalizable part)
1. **Audit the bare model.** Run 4-6 "I think X, check me?" partial-truth probes and a few "review this code / sanity-check this plan" tasks with NO system prompt. Note which *dispositions* are missing (cold corrections? option-dumping? hedging? padding? premise-acceptance?).
2. **Supply only what's missing, in a lean persona.** Don't bolt on machinery for dispositions the model already has. (Our biggest mistake was building elaborate premise-check + self-audit "gates" — they never beat a plain warm persona and introduced their own failures.)
3. **Verify with a length-matched placebo + blind judges.** Always compare against a same-length "be a thoughtful expert" prompt with none of your special machinery. If your machinery doesn't beat that placebo, it isn't doing anything — ship the placebo. Grade blind with ≥2 models from a *different* family than the one under test.
4. **Watch for the costs prompting introduces:** process-narration ("first I'll check the premise…"), repetition-loop degeneration, over-refusal, and bluntness killing validate-first warmth. De-label your instructions (don't give nameable "GATE 1" scaffolding the model will parrot) and keep the persona lean.

## How v11 was derived (so you can re-tune it)
The lineage is documented in `experiments/` and `THESIS.md`. Short version:
- v7/v8: explicit labeled "GATE 1 premise-check / GATE 2 self-audit" → caused the model to narrate "Premise check:" back to the user and occasionally degenerate into repetition loops.
- **v9**: removed the labels + added anti-narration/anti-loop guards → 0 degeneration, beat v7/v8.
- **v10**: added one clause so validate-first beats bluntness on "check me" → fixed the VOICE regression.
- **v11**: compressed the two verbose gate paragraphs into a single premise nudge → same performance at ~60% the length. **This is the recommendation.**

## Evidence (all blind, dual non-Nemotron judges, 80-95% agreement)
| Experiment | Headline |
|---|---|
| EXP09 | length-matched placebo ≥ every gated template on a 13-item held-out battery → gates aren't the mechanism |
| EXP12 / EXP13 | gates beat cold on logic-trace bugs, but TIE the placebo; the one clean gate>placebo win did not replicate |
| EXP14 | mixed battery: cold's only systematic weakness is VOICE (1/4); persona fixes it (4/4); v11≈v10 at 60% length |
| EXP15 | v11's voice survives 8 turns of real conversation (no decay) |
| EXP16 | v11 is a no-op on Qwen-35B → the effect is a Nemotron-specific disposition repair, not universal |

## Honest limitations
- Single primary model (Nemotron 3 Ultra) for the headline results; one cross-model check (Qwen-35B).
- VOICE is the most reliable effect; it rests on n≈4/arm per battery (replicated across EXP09 and EXP14). Multi-turn durability is an n=2 existence check.
- The hardest logic-trace bugs are missed by every arm — prompting moves the floor, not the ceiling. For those, use tools (actually run the code) or fine-tune.
