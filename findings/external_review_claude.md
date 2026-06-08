# External review — Claude Opus (extended thinking), deep-research charter

Charter: introspection + template architecture (disposition taxonomy, v3 critique, v4, multi-turn durability). Claude correctly declined to run a web "research job" and reasoned directly — good premise-check on its own task.

## Headline contributions
1. **Independently flagged the over-skepticism / false-positive gap as the #1 issue** — the same hole the parent agent predicted GPT would find. Two independent arrivals = strong signal it's real. Our EXP02-04 only ever used tasks that CONTAIN a false premise, so v3's precision (false-positive rate on premise-clean tasks) is unmeasured.
2. **Three-way GATE 1 triage** (Broken / Sound-but-underspecified / Sound) with "Sound → just do it" as an explicit success state — the proposed fix for v3's unconditional premise-hunt.
3. **One-sentence nameability test**: "if you can't say which assumption is wrong and why in one sentence, it isn't Broken — proceed." Cheap, concrete precision filter.
4. **"Default to Sound"** sets the prior correctly.
5. **GATE 2 audits both directions** — also catches over-correction/padding (precision backstop).
6. **"No false balance AND no false certainty"** added to honesty clause.
7. Disposition taxonomy w/ promptability + risk; honest that **taste (choosing among valid options) is the irreducible weak point** of the elicitation thesis.
8. Multi-turn durability: drift = contextual dilution + user-mirroring; fix = compressed per-turn re-trigger (~30 tok); 10-turn stress test with turn-1-vs-turn-10 delta and embedded over-skepticism controls (turns 2 & 9).

## Disposition taxonomy (verbatim summary)
| Trait | Promptability | Best lever | Main risk |
|---|---|---|---|
| Premise-skepticism | High | Bounded decision step | Over-firing (false positives) |
| Validate-first | High | Flat rule | ~None |
| Hostile self-audit | High if forced | Perspective-swap | Doesn't fire unprompted |
| Density | Medium | Persona/voice, never "be concise" | Clumsy phrasing kills info |
| Honest bluntness | Medium | Pair w/ "no false certainty" | Manufactured contrarianism |
| Knowing when to stop | Medium | Persona | Padding creeps back |
| Taste | Low | Nudge only | Irreducible inconsistency |

## Do-not-challenge list (over-skepticism guardrail)
1. Pure execution requests (premise irrelevant). 2. User already shows tradeoff awareness. 3. Stylistic/subjective/preference calls. 4. Flaw is real but irrelevant to the goal (subtlest). 5. Would need investigation to know it's wrong (violates "zero extra info"). 6. "Mild smell" but no nameable flaw → treat Sound. 7. Emergencies/debugging-in-progress → lead with the fix.

## Flagged uncertainties (Claude's own)
- Can't measure v3's FP rate from its seat — it's inference; the control set confirms/kills it.
- Per-turn re-trigger's exact form (system vs prepend, length) untested.
- Taste is the weakest point; no prompt fully fixes it.
- All reasoning from the Opus family + priors; Nemotron quirks may break specific phrasings — treat v4 as the next A/B hypothesis, not final.

## Parent-agent critique to carry forward (NOT from Claude)
**v4's biggest untested risk = recall/precision tradeoff.** The "Sound → just do it" branch is structurally the SAME kind of escape hatch that made v2 regress (v2's "be specific" → "demand code" exit). v4 could under-fire and regress toward cold on EXP03/04-style buried premises. So v4 must be tested for BOTH: (a) does it keep ~v3's catch-rate on buried-but-real premises, and (b) does it get a low false-positive rate on premise-clean tasks. Measuring only one is the trap.
Also test a **"v4-lite"**: added triage complexity may dilute Nemotron's compliance vs v3's simpler premise-first rule. Simplicity has value.
