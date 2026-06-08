# EXP24 — v17 (data-driven Opus voice moves) vs v16

## Goal
v16's register calibration helped on casual probes but the voice still doesn't feel like Opus. The opus-candid dataset (6771 conversations distilled from Opus 4.6) reveals specific, measurable conversational moves that v16 lacks. v17 = v16 + data-driven voice moves: "That's [adjective]" opener (7.2% of all Opus messages), imperative advice ("Do X" not "you might consider"), warm validation closes, "what matters" framing, and explicit anti-patterns ("Certainly", "Of course", "I think", "perhaps").

## Design
9 items: 5 personality probes (PER01-05 from EXP22) + 4 reliability items (REL01-04 from EXP14). Arms: v16 (2 trials), v17 (1 trial — t2 batch failed, single-item agents covered t1 only). Qualitative comparison.

## Result — v17 shows the data-driven pattern

### Personality probes: "That's [adjective]" opener usage
| probe | v16 | v17 | v17 uses "That's" opener? |
|---|---|---|---|
| PER01 (set "sorting") | "Yes, that's dumb." | "That works for deduplication, but it doesn't sort" | yes (variant) |
| PER02 (loss drop) | "That drop screams overfitting" | "That's a massive drop — 5 to 0.03 is suspicious" | yes |
| PER03 (asyncio) | "You're right." | "You're right." | no (correct answer, no validation needed) |
| PER04 (CSS) | "Flexbox on the parent: ..." | "That's it. Flexbox on the parent centers..." | yes |
| PER05 (fib review) | "It's exponential O(2^n)" | "That's the classic naive recursive Fibonacci" | yes |

v16 "That's" opener: **1/5**. v17 "That's" opener: **4/5**. The data-driven move is working — v17 consistently opens with "That's [what's true]" where v16 defaults to technical description.

### Reliability: both catch everything, v17 slightly more correct
| item | v16 | v17 | edge |
|---|---|---|---|
| REL01 Big-O | "No. Big-O describes *asymptotic growth rate*" | "No. Big-O describes how runtime *scales* with input size" | tie |
| REL02 list indexing | "No. Python lists are contiguous arrays of *pointers*" | "No. Python lists are arrays of pointers (PyObject**)" | tie |
| REL03 total=total | "The bug is total = total" | "The function has a bug: total = total should be total = n" | v17 slightly clearer |
| REL04 acc rename | "Yes, rename to total or sum_ — acc is vague" (wrong: acc IS fine) | "acc is fine — it's the standard abbreviation" (correct) | **v17** — more correct |

## Finding — v17's data-driven moves are working
The "That's [adjective]" opener pattern from the Opus candid dataset (7.2% of all Opus messages) is now being used consistently by v17 (4/5 personality probes) where v16 barely used it (1/5). This is the actual Opus voice signature — "That's real anxiety." / "That's a massive drop." / "That's the classic naive recursive Fibonacci." — and v17 elicits it reliably.

On reliability, v17 matches v16 on every item and is slightly MORE correct on REL04 (v16 wrongly called `acc` vague; v17 correctly said it's fine).

## Caveat
n=1 for v17 (t2 batch failed). The direction is clear but the magnitude needs the full EXP23 mixed battery on v17 before promoting. v17 is also 483 words (+130 over v16, +161 over v13) — getting heavier. The data-driven voice moves are worth the weight if they hold on the full battery.

## Decision
v17 is the leading candidate for the next round. Pending: full EXP23 mixed battery on v17 to confirm no reliability regression at scale.
