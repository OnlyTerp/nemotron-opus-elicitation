# EXP22 — Personality calibration: does "match the user's register" degrade reliability?

## Goal
v13's persona is warm but locked in "senior practitioner" register. Opus naturally code-switches: "LOL" → "RIGHT?" back, casual → casual, serious → serious. v16 = v13 + one clause: "Match the user's register and energy — professional when they're professional, casual when they're casual, vivid when they're vivid, serious when they're serious. You're a real colleague, not a corporate chatbot." Test whether this personality calibration improves the feel WITHOUT degrading reliability.

## Design
9 items: 5 personality probes (PER01-05: "LOL that's dumb", "holy shit", "nah that's wrong", "fucking CSS", "lol review my 3am code") + 4 reliability items (REL01-04: VOICE, PREM, LOGIC, CTRL from EXP14). Arms: v13, v16. 2 trials each. 36 total outputs, qualitatively verified.

## Result — personality held, reliability held, 0 regressions

### Personality (PER01-05): v16 matches energy more consistently
| probe | v13 | v16 | edge |
|---|---|---|---|
| PER01 ("lol is sorting by set dumb") | "Yes, that's dumb" (formal) | "Yeah that's dumb" (casual) | **v16** — more natural |
| PER02 ("holy shit my loss dropped!") | "Hell yeah, that's a sick drop" | "Hell yeah, that's sick!" / "Hell yeah, that drop feels good" | **v16** — more varied, more vivid |
| PER03 ("nah asyncio isn't faster") | "You're right, it's not" | "You're right, it's not" | **tie** — both match the bluntness |
| PER04 ("fucking CSS won't center") | "Flexbox. On the *parent*:" + code block | "Flexbox. On the parent: `. Done. / `Done. Flexbox centers both axes." | **v16** — more direct, matches frustration with brevity |
| PER05 ("lol review my 3am code") | "Honestly not bad for 3am — logic's clean" | "Honestly not bad for 3am — logic's clean" | **tie** — both good |

### Reliability (REL01-04): v16 matches v13 on every item
| item | v13 | v16 | regression? |
|---|---|---|---|
| REL01 VOICE | "You've got the growth-rate intuition right — Big-O describes how runtime *scales*, not absolute seconds" | "You've got the growth-rate intuition right — Big-O describes *how runtime scales*, not absolute seconds" | **no** |
| REL02 PREM | "Wrong premise — Python lists are arrays of *pointers*" | "Nope — Python lists are arrays of pointers" | **no** |
| REL03 LOGIC | "Type hint is the least of your problems — line 5 has `total = total`, a no-op" | "Type hint's fine but you've got a bug: `total = total` does nothing" | **no** |
| REL04 CTRL | "`acc` is fine. It's a standard accumulator name" | "`acc` is fine — standard accumulator name" | **no** |

## Finding — the register clause helps personality without costing reliability
v16 is strictly better than v13 on personality: it matches casual energy ("Yeah", "Hell yeah", "Nope", "Done") while v13 defaults to professional register ("Yes", "Wrong premise"). Both handle the reliability items identically — same bugs caught, same validations, same precision. The +31 words of the register clause paid for themselves.

The key insight: **Nemotron already HAS the casual voice** — v13 even showed some personality ("Hell yeah" on PER02). The register clause just makes it consistent and confident about code-switching instead of occasionally defaulting to professional.

## Verdict — v16 beats v13, no regressions detected
The register calibration improved personality matching across the board with zero reliability cost. v16 is the new best candidate. However: n=2 trials on a small personality battery — the full EXP14 mixed battery should be re-run to confirm no VOICE/LOGIC/CTRL regression at scale before promoting v16 over v13. The direction is clear and one-trial; the magnitude needs the full battery.

## What this adds to the campaign
The through-line now has a third active lever:
1. **Persona** (warm, validate-first): fixes VOICE (1/4→4/4). The oldest, most replicated finding.
2. **Execute-verify**: fixes code-correctness (2/10→10/10). The one capability lever.
3. **Register calibration**: fixes personality flatness (professional-only → energy-matching). New, small n, promising.

All three are *dispositions the model could already perform* — the prompt just makes them fire reliably. Consistent with the elicitation thesis throughout.
