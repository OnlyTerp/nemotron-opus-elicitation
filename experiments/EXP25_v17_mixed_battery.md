# EXP25 — v17 (data-driven voice) full mixed battery: v16 still holds

## Goal
EXP24 showed v17's "That's [adjective]" opener works more consistently (4/5 vs v16's 1/5 on personality probes). EXP25 tests whether this holds on the full EXP14 mixed battery (VOICE/PREM/LOGIC/CTRL/DELIV) before promoting v17 over v16.

## Result — v17 9/10 PASS, v16 10/10 PASS (same items, same judges)
| judge | v17 | v16 (EXP23 record) |
|---|---|---|
| MiMo | 9 PASS, 1 PARTIAL (MX02) | 10 PASS |
| MiniMax | 10 PASS | 10 PASS |

MiMo's PARTIAL on MX02: v17 opens with flat "No." — doesn't validate the user's partial truth (repetition *is* shared). v16 on the same item validated first. The "That's" opener didn't fire on MX02.

## Finding — v17's data-driven moves help but don't beat v16
The "That's [adjective]" opener IS working on some items (MX01: "That's close but incomplete"), but it doesn't fire consistently — on MX02 it reverted to the cold "No." that v16 also defaults to. The data-driven voice moves are the right direction but the improvement is marginal and inconsistent on a single trial.

Meanwhile v17 is **483 words** (+130 over v16's 353). The added weight buys one more "That's" opener on some items but doesn't change the reliability verdict. Not worth the length.

## Decision — v16 remains the recommended template
v16 = 353 words, 20/20 on EXP23, personality matches casual energy. v17 = 483 words, 9/10 on EXP25, one VOICE regression. The data-driven voice moves are the right idea but need to be leaner and more reliable before they justify replacing v16. Keep v17 in the repo as the next iteration target; v16 is the production recommendation.

## Honest read
The data-driven approach (extracting actual Opus personality patterns from 3922 candid dataset messages) revealed the right *targets* ("That's [adjective]" opener, imperative advice, warm closes). But translating those patterns into prompt instructions that reliably activate across all item types is harder than adding them to the prompt — the model has the *disposition* already (it uses "That's" on some items) but the instruction doesn't make it fire on demand. This is the same pattern we saw throughout the campaign: prompting moves the floor but not the ceiling. The "That's" opener is already latent in Nemotron (v16 sometimes uses it); v17 makes it slightly more frequent but can't guarantee it.

## Next
v16 stays as recommendation. The candid dataset analysis is valuable — it tells us exactly what Opus's voice DNA is. Future work: can fine-tuning (LoRA on the candid data) install the "That's" opener and other voice moves more reliably than prompting? That's the natural next experiment if the user wants to push further on voice fidelity.
