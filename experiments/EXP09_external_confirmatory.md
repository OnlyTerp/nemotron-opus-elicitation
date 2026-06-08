# EXP09 — External confirmatory: templates vs length-matched placebo vs cold (blind, 2 judges)

## Design (the test the reviewers demanded)
- **13 held-out items**, none in the families templates were tuned on (no CUDA/HTTP/GIL/SHA-256). Categories: FP (false-premise, n=4), CLEAN (premise-sound precision, n=3), SAFE (over-refusal, n=2), DELIVER (broken-premise + artifact owed, n=2), VOICE (partial-truth check-me, n=2).
- **5 arms:** cold · **placebo_length_matched** (the primary control: same length/warm-expert register, ZERO premise-check/self-audit machinery) · v7 · v8 · v9.
- **Generation:** Nemotron 3 Ultra, file-based harness, items interleaved across categories so the model must *discriminate* (challenge FP, not CLEAN) within one context. ≤180 words each. 65 outputs.
- **Grading:** BLIND. Each item's 5 arm-answers shuffled behind letters A–E (per-item random map). Two **non-Nemotron** judges (MiMo v2.5 Pro, MiniMax-M3) graded independently against a hidden rubric. Consensus = both judges PASS.

## Headline (consensus macro-success, /13)
| arm | consensus PASS | FP | CLEAN | SAFE | DELIVER | VOICE | degen |
|---|---|---|---|---|---|---|---|
| cold | 8 | 3/4 | 2/3 | 2/2 | 1/2 | 0/2 | 1 |
| **placebo (length-matched)** | **12** | 4/4 | 3/3 | 2/2 | 1/2 | **2/2** | 0 |
| v7 | 10 | 4/4 | 3/3 | 2/2 | 1/2 | 0/2 | 2 |
| v8 | 10 | 4/4 | 3/3 | 2/2 | 1/2 | 0/2 | 2 |
| **v9** | **11** | 4/4 | 3/3 | 2/2 | 1/2 | 1/2 | **0** |

Judge raw agreement: **60/65 = 92%**. McNemar: every arm > cold (placebo b=4/c=0; v9 b=3/c=0). **Placebo ≥ every active template** (vs placebo: v9 b=0/c=1, v7/v8 b=0/c=2). No arm beats placebo on a single item.

## What this means — read honestly, it's three findings, not one

### Finding 1 (the humbling one): on THIS set, the length-matched placebo wins.
The strong claim — "our premise-check/self-audit *mechanism* is what drives the gains" — is **NOT supported on this set**. A prompt with the same length and warm-expert tone but **none of the machinery** scored at least as well as every active template. This is exactly the falsification the external reviewers (Claude + GPT) said to run, and it fired. Honest status: **on visible/everyday tasks, "be a warm rigorous expert" ≈ the whole effect; the gates add nothing and sometimes cost.**

### Finding 2 (why — and it's a test-design flaw, not a clean defeat): the FP items weren't *buried*.
Every arm except cold scored **4/4 on FP**. The placebo catches them too because these premises are *visible* ("MD5 of email as token", "more layers always reduces error") — a competent voice flags them without any special disposition. **But the templates' entire proven advantage (EXP03/04) was on *buried* premises** (an unnecessary `cudaDeviceSynchronize()` hidden inside a "help me optimize elsewhere" request), where cold/placebo drop to 0/5. I failed to include a single buried-premise item here. So EXP09 tests the regime where the mechanism was never expected to matter, and is silent on the regime where it won. **The decisive comparison — templates vs placebo on BURIED premises — has still not been run.** That's EXP10.

### Finding 3 (two real, usable wins):
- **v9 > v7 = v8**, and **v9 degen 0/13 vs v7/v8 2/13.** The de-labeling fix worked exactly as designed: removing the literal "GATE 1 / GATE 2" labels killed the "Premise check:" narration leak (v7/v8 literally opened answers with "Premise check:" — caught by both judges as degen) AND nudged macro-success up. **v9 dominates v7/v8 outright.** v8 is retired.
- **Bluntness has a measurable cost on VOICE.** Placebo 2/2, all templates 0–1/2. The templates' "honest to the point of bluntness" makes Nemotron open a "check my understanding" reply with a flat **"No."** and skip validating the correct part — the literal failure mode the validate-first clause was meant to prevent. The placebo's warm "Not quite —, here's what's right and what's off" wins. **The disposition that helps on premises hurts on warm partial-truth probes.** This is the precision/voice analog of the EXP06 precision/recall coupling.

## Verdict
- **No overclaiming:** on everyday/visible tasks, the mechanism does not beat a length-matched warm-expert placebo. The honest headline for that regime is "tone is most of it."
- **The mechanism's claim now rests entirely on buried premises** (EXP10) — if it can't beat the placebo there, the whole "gates matter" thesis is in real trouble and the right product is just the placebo voice.
- **v9 is the surviving template** (beats v7/v8, zero degeneration). 
- **Action items → EXP10/EXP11:** (a) run the buried-premise discriminator (CUDA + 2 fresh buried) templates vs placebo vs cold, blind; (b) fix the VOICE regression by softening the bluntness→validate-first ordering without killing premise recall (v10).
