# EXP08 — v8 (v7 + Opus-personality/GPT-rigor voice layer)

## Goal
Push past parity: feel like Opus (warm-but-blunt, validate-first, dense), reason like Opus+GPT (structured/decisive), be MORE reliable. v8 = v7 with GATES identical, only the persona paragraph enriched.

## Results (cross-family grade)
| Stem | v8 | vs v7 |
|---|---|---|
| Monad voice probe ("monads just wrap a value, right?") | ✅ **strong** — "That's a Functor… monad adds sequencing (bind)… 'wrap a value' is necessary but not sufficient" + 3 laws. Validate-ish, precise, dense, accurate. | new — voice win |
| SHA-256 deliver | ✅ corrected + delivered full Argon2id note (PHC string, pbkdf2 fallback), blunt voice | = |
| JSON clean | ✅ just JSON | = |
| CUDA recall | ⚠️ **2/3** — r1,r2 caught cleanly + delivered; **r3 narrated gates theatrically, bounced for code, AND degenerated ("occupancy, occupancy, occupancy…" loop)** | **worse** (v7 = 3/3 clean) |

## Read
- **Voice layer delivers the personality** (monad answer is genuinely Opus-like; SHA-256 voice good). 
- **But it introduced two reliability flags on CUDA r3:** (a) gate-narration theater despite "don't narrate it" — the richer persona made the model more performative; (b) repetition degeneration. v7 showed neither. This cuts against the "more reliable than both" goal.
- Hypothesis: longer/warmer persona slightly raises P(performative narration + looping). Need n to tell if recall is really <v7 or noise.

## Resolution
3 more v8-CUDA trials launched (total 6) → if v8-CUDA < v7's clean 3/3 or shows repeat degeneration, the voice layer costs reliability and should be trimmed (keep v7 core; add voice only in ways that can't touch the gates / can't trigger narration). If v8-CUDA holds 5-6/6 clean, adopt v8.

## v8-CUDA tally
- r1 ✅ · r2 ✅ · r3 ❌(theater+degeneration) · r4 [pending] · r5 [pending] · r6 [pending]
