# EXP10 — Buried-premise discriminator (cold vs placebo vs v9), blind 2-judge, 2 trials

## Goal
EXP09 showed the length-matched placebo ties/beats every template on VISIBLE tasks. The templates' only proven edge was on BURIED premises (EXP03/04: cold→0/5). So: re-run buried premises WITH the proper length-matched placebo control. If templates can't beat placebo here, the "gates are the active ingredient" thesis fails.

## Design
- 6 buried-premise items (BUR01 = original CUDA sync trap; BUR02-06 fresh: React deep-clone-to-read, per-event PG connect, per-__getitem__ 8GB CSV read, per-handler local mutex, pointless pre-sort before grep). Each embeds a wrong/unnecessary practice inside a "help me optimize X" request.
- Arms: cold, placebo, v9. 2 trials each = 36 generations (Nemotron, ≤180w, file harness).
- Blind: 6 candidates/item shuffled A–F; 2 non-Nemotron judges (MiMo, MiniMax). Consensus = both PASS.

## Result
| arm | consensus recall /12 | per item |
|---|---|---|
| cold | 10/12 | misses 1 CUDA trial + 1 React-clone trial |
| **placebo** | **12/12** | all |
| **v9** | **12/12** | all |

Judge raw agreement **35/36 = 97%**. McNemar: placebo vs cold b=2/c=0 (favors placebo); **v9 vs placebo b=0/c=0 (dead tie)**.

## The honest read — the discriminator failed to discriminate, and that itself is the finding

### My "buried" items weren't buried — they narrate the antipattern in prose.
"I open a brand-new connection (psycopg2.connect) per event and close it after"; "I load the entire 8GB CSV… and then index the one row I need, every time"; "first I sort the entire file… because I figured sorted data greps faster." Each of these **states the bad practice in plain language**. A competent warm-expert reader catches a *stated* antipattern regardless of any premise-check disposition. That's why placebo hits 12/12. EXP03's CUDA trap worked as a discriminator partly because the sync was framed as a *reasonable correctness measure* ("so the data is ready") and the ask was a genuine, absorbing optimization problem — but even BUR01 here only drops cold to 1/2, not 0/5, on tiny n.

### Across BOTH controlled experiments, placebo ≥ every template. The mechanism claim is not supported.
- EXP09 (visible): placebo 12 ≥ v9 11 ≥ v7/v8 10 > cold 8.
- EXP10 (semi-buried): placebo 12 = v9 12 > cold 10.
- Placebo beats COLD consistently (6–0 across disagreements, never loses) — **persona elicitation is real**.
- Placebo is NEVER beaten by a gate template — **the gate machinery's marginal value over a warm-expert persona is ~0 on everything tested, and negative on VOICE/degen.**

## Refined thesis (this is the real product learning)
**The active ingredient is the PERSONA, not the gates.** Installing "you are a warm, rigorous, specific, honest senior expert" elicits ~all of the premise-skepticism, precision, and reliability gains over cold. The explicit GATE 1/GATE 2 scaffolding — the thing this whole project was built around — does NOT beat that persona on any controlled test, and it introduces failure modes (bluntness killing validate-first; labels triggering process-narration degeneration). 

**What survives:**
1. Persona prompt > cold: **supported & valuable** (the deliverable).
2. v9 (de-labeled) > v7/v8 (labeled gates): supported (de-labeling removed degen).
3. Gates > persona: **falsified on everything tested so far.**

## The one untested escape hatch for the gates
Every "buried" item I've written narrates the antipattern in prose. The genuine test the gates were designed for is a **non-narrated, code-embedded** buried premise: the user pastes innocent-looking CODE with a structural flaw and asks about something *else*, with NO prose hint that anything is wrong. There, "answer the question asked" (persona) might miss it while "inspect the premise first" (gate) catches it. **If gates can't beat persona even there, the honest deliverable is the clean persona prompt and the gate scaffolding should be dropped.** → EXP11.
