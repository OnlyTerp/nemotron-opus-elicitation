# Nemotron × Opus Elicitation

**Goal:** Get Opus-4.8-grade *reasoning, reliability, and personality* out of **Nemotron 3 Ultra** through prompting alone — **no fine-tuning**.

## The core bet — and what 15 experiments actually showed

**Original hypothesis:** Nemotron has Opus-grade capability; what it lacks are *dispositions* (premise-questioning, self-audit, validate-first honesty, dense reasoning). Install those via an explicit GATE template (premise-check + hostile self-audit) and you elicit Opus-like behavior. "It was always there, just hidden."

**What the controlled experiments (EXP09-15) actually found — read this first, it overturns the original framing:**

1. **The active ingredient is the PERSONA, not the gates.** A length-matched "warm, specific, validate-first senior expert" prompt with **none** of the explicit premise-check/self-audit machinery beats the bare model on every axis — and **ties or beats every gated template** on five held-out blind batteries. The elaborate GATE scaffolding this project was built around adds ~0 over a good persona, and its bluntness mildly *hurts* the validate-first voice.
2. **The single most reliable, replicated effect: persona fixes the bare model's VOICE.** Cold Nemotron, asked "I think X, check me?", opens "No/Not quite" and corrects without acknowledging what's right (EXP14: cold 1/4 on VOICE). Any warm persona repairs this (4/4). This is the real, shippable win.
3. **Capability ceiling is real for *persona* prompts — but breakable with execute-verify.** The hardest silent-wrong-output bugs (a `range(len-k)` off-by-one, a floor-division average) are missed by every *voice/persona* arm (cold 2/10). The execute-verify clause (point 6) is the one thing that cracked them (→10/10).
4. **The engineered-template trajectory was still real progress:** v7/v8 (labeled gates → process-narration + repetition degeneration) → **v9** (de-labeled, 0 degeneration) → **v10** (validate-first, fixes VOICE) → **v11** (lean, drops the verbose gate paragraphs, matches v10 at ~60% the length). Each step fixed a *measured* defect.
5. **The persona is multi-turn durable** (EXP15): it survives 8 turns of real conversation without decaying to cold's blunt reflex.
6. **One lever moved actual CAPABILITY, not just voice** (EXP17-19): an **execute-verify** clause ("don't trust a read-through — check the code's output on a concrete boundary input") took silent-wrong-output-bug recall from **cold 2/10 → 10/10**, with zero precision cost and zero degeneration. A real sandbox added nothing over *mental* execution on review-sized code (EXP18) — the lever is the disposition, not the tool. Folded into the persona, this gives the final template **`v13_lean_verify.md`**.

7. **Register calibration makes it feel human** (EXP22-23): adding "match the user's register and energy — professional when they're professional, casual when they're casual" gave v16 the personality to say "Hell yeah" and "Nope" naturally, while scoring a perfect 20/20 on the reliability battery (v13 was 29/30). Zero regressions on any axis.

**Bottom line:** the shippable artifact is **`templates/v16_personality_calibrate.md`** — a 353-word lean persona that supplies three active levers: *validate-first voice* (fixes Nemotron's cold bluntness), *execute-verify on code* (lifts silent-bug recall from 2/10 to 10/10), and *register calibration* (matches the user's energy naturally). All three are dispositions the model could always perform; the prompt just makes them fire reliably. No gates, no scaffolding, no over-engineering — just the dispositions Nemotron was missing.

## What's in here

| Path | What |
|------|------|
| `USAGE.md` | **Start here to use it.** The recommended prompt + the "audit then supply" method |
| `THESIS.md` | The full hypothesis arc (R1→R12) + what each experiment taught us |
| `templates/v11_lean_synthesis.md` | ⭐ **RECOMMENDED** prompt (lean warm-expert persona) |
| `templates/v7..v10_*.md` | Superseded predecessors, kept for history (each header says why) |
| `templates/v1_checklist_DEPRECATED.md` | First attempt (rigid checklist) — cautionary example |
| `bench/` | The EXP09-16 harness: testbanks, file-based generation, blind assembler, scorers, raw outputs, grades |
| `experiments/EXP*.md` | Each test: design, hypothesis, raw results, scoring, honest caveats |
| `findings/` | Dataset provenance + early external reviews |

## Method

Every claim is tested against the **live Nemotron 3 Ultra** (`run_subagent --profile nemotron-ultra`). From EXP09 on, the protocol hardened to address the exact biases the early work had:
- **Length-matched placebo** (same warm-expert register, ZERO gate machinery) as the *primary* control — not just COLD. This is what revealed the gates weren't the active ingredient.
- **Held-out test banks** authored fresh per experiment (no tuning on them).
- **Blind grading by TWO non-Nemotron judges** (MiMo v2.5 Pro + MiniMax-M3) — answers shuffled behind random letters; consensus = both PASS; McNemar on paired item-trials. Judge agreement ran 80-100%.
- **File-based generation harness** with a topic-validator that rejects/quarantines any answer↔item cross-wiring, plus single-item regeneration for reliability.

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
- ✅ EXP08 (**v8 = v7 + voice layer**): personality delivered; but labeled gates left a ~1/6 degeneration tail.
- ✅ **EXP09 (held-out confirmatory, blind 2-judge, length-matched placebo): OVERTURNED the mechanism claim.** placebo 12/13 ≥ v9 11 ≥ v7/v8 10 > cold 8. No gated template beat the placebo. Sub-wins: v9 (de-labeled) 0/13 degen beats v7/v8; bluntness costs VOICE.
- ✅ EXP10-11 (buried / code-embedded premises): famous antipatterns caught ~universally; gates didn't separate from placebo (only an isolated logic bug did, once).
- ✅ EXP12 (logic-trace traps): **the one clean gate win** — v9 8/12 > cold=placebo 5/12 (100% agree). ✅ EXP13 (replication, 10 items): **did NOT replicate** — gates tie placebo (12/20 each) > cold 9.
- ✅ **EXP14 (mixed head-to-head, 95% agree): placebo 20/20 > v10 19 > v11 18 > cold 15.** Cold's ONE systematic weakness is VOICE (1/4); persona fixes it (4/4). **v11 (lean, 60% length) ≈ v10.**
- ✅ EXP15 (multi-turn): v11 persona **survives 8 turns**, no decay.
- ✅ EXP16 (Qwen-35B transfer): v11 is a **no-op** (11/12 = cold) — the effect is a Nemotron-specific disposition repair, not universal.
- ✅ **EXP17 (execute-verify breaks the capability ceiling):** silent-wrong-output bugs cold **2/10 → v12 10/10**, 0 precision cost, 98% agree.
- ✅ EXP18 (sandbox vs mental): real sandbox **ties** mental execution (12/12 = 12/12) on review-sized code — the lever is the disposition, not the tool.
- ✅ **EXP19 (v13 = v11 + execute-verify):** VOICE 4/4, CTRL 4/4, 0 degen, + silent-bug recall 8/10. v13 dominates v11.
- ✅ **EXP22-23 (v16 = v13 + register calibration):** 20/20 on mixed battery (100% agree), personality matches casual energy ("Hell yeah", "Nope", "Done"), zero regressions. **v16 strictly dominates v13.**
- ⭐ **Final recommendation: `templates/v16_personality_calibrate.md`** — 353 words, three active levers, no gates. See `USAGE.md`.

### Headline result (EXP14, blind 2-judge, 95% agreement)
The whole campaign in one table — consensus PASS by category, /4 unless noted:

| Arm | VOICE | PREM | LOGIC/6 | CTRL | DELIV/2 | total/20 |
|-----|-------|------|---------|------|---------|----------|
| COLD | **1/4** | 4/4 | 4/6 | 4/4 | 2/2 | 15 |
| placebo (persona, no gates) | 4/4 | 4/4 | 6/6 | 4/4 | 2/2 | **20** |
| v10 (full gates) | 3/4 | 4/4 | 6/6 | 4/4 | 2/2 | 19 |
| **v11 (lean, recommended)** | 3/4 | 4/4 | 5/6 | 4/4 | 2/2 | 18 |

The lever turned out to be **persona, not the gate mechanism** — and its biggest, most reliable effect is repairing the bare model's cold VOICE. Capability (PREM/LOGIC/CTRL/DELIV) was already there; the persona supplies the missing *disposition*.
