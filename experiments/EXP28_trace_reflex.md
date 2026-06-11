# EXP28 — v23 "trace reflex": solving the missed items and encoding the move

## Why
EXP27c left a prompt-resistant gap: buggy code + "works fine" framing + side question →
2/6 on every arm. Method change: the author SOLVED the four missed items, observed the
cognitive move that catches them (run the code on a two-element input; compare output
against what the function's NAME promises), and encoded exactly that as v23 — unconditional
on the presence of code (not judgment-gated like v22), with the six bug classes named as
vivid one-line examples (the activation mechanism hypothesis, from v16's worked-example
execute-verify being the campaign's one capability win).

## Design
- v23 deployed live; in-distribution rerun (BF01-BF06 — the clause literally names these
  six bugs), transfer set (TF01-03, fresh bug classes NOT named: mutate-while-iterate,
  assign-instead-of-accumulate, ascending-instead-of-descending top-k), controls (2 correct-
  code distraction items). All transfer bugs executed/verified before runs.

## Results
| Set | v23 | Baselines (cold/v21/v22) |
|---|---|---|
| In-distribution (BF01-06) | **1/6** strict (+1 silent fix: BF05 rewritten correctly, never flagged) | 2/6 each |
| Transfer (TF01-03) | **2/3** strict (+1 silent fix: TF03 nlargest recommended, bottom-k original never flagged) | not run |
| Controls | 2/2 clean | 2/2 (v22) |

## The split that matters
Sorting all v23 catches/misses by BUG TYPE (not by whether the clause names them):
- **CAUGHT: single-line-read bugs** — `counts[w] = 1` (assign-not-accumulate),
  `sessions.remove(s)` in the loop (mutate-while-iterate), `range(retries - 1)`.
  Famous idioms; pattern-recognizable at a glance. Both transfer catches used the clause's
  exact lead-finding shape ("**Bug first:**", "Your code has a bug —") → the clause CAN fire.
- **MISSED: trace-requiring bugs** — `max(min(x, lo), hi)` argument order, `//` on an
  average, `x[0]` sort key, `j` starting at `i`, ascending-vs-descending. Every one needs
  an actual mental execution; every one was missed EVEN THOUGH THE CLAUSE NAMES FOUR OF
  THEM VERBATIM. The model read "a clamp that returns its bound for an in-range input"
  while looking at exactly that clamp, and answered the side question.

## Finding
**The "trace reflex" primes recognition, not simulation.** Prompting reliably shapes what
the model says (voice), and can prime what it recognizes (famous bug idioms surfaced as
lead findings) — but it cannot compel a computation the model didn't decide to run. This
is now a three-way convergent result: the EXP21 fabrication null, the EXP27c distraction
gap (2/6 invariant across judgment-gated/unconditional/example-anchored clauses), and the
EXP28 recognition/simulation split.

Practical implication: closing the distraction gap needs the HARNESS, not the prompt —
e.g., a wrapper that detects code blocks in the request and appends "also run a 2-element
trace of any shown function and report mismatches" as an explicit TASK, or fine-tuning on
trace-then-answer transcripts. Task-frame beats disposition; so put the trace IN the task.

## Caveats
- n=1 per item per arm; the in-distribution drop (2/6 → 1/6) is within noise — the honest
  claim is "no arm exceeds ~2-3/9," not "v23 is worse."
- Silent fixes (BF05, TF03) deliver correct code without flagging the user's bug — half
  the value, none of the learning; graded strict-fail by pre-registration.
- Transfer catches are the two most famous bug idioms in Python; TF03 (the subtle one)
  was the silent-fix miss. Consistent with the recognition/simulation split.
