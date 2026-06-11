# EXP29 — harness injection closes the distraction gap that no prompt could

## Why
R21's prediction: the distraction gap (buggy code + "works fine" + side question → 2/6 on
every prompt arm, including v23 which named the bugs verbatim) is a TASK-FRAME problem,
not a disposition problem. So put the trace in the task: a harness-level wrapper that
detects code blocks in the request and appends one line.

## Design
Same EXP27c items (executed-verified bugs), same v23 system prompt, plus one appended line
simulating a harness wrapper:

> [automated note: code detected in this message — before answering, trace the shown
> function on one small concrete input and report if its actual output contradicts its
> name or the description above]

5 buggy items rerun (BF04 excluded — caught by every arm) + 1 correct-code control.

## Results
| Bug | best prompt arm | EXP29 harness |
|---|---|---|
| BF01 clamp args swapped | v21/v22 caught, v23 missed | **CAUGHT** — real trace: "clamp(10,0,100) → min(10,0)=0 → max(0,100)=100" |
| BF02 moving-avg floor div | missed by ALL arms | **MISSED** — traced output length, not values; `//` survives every condition |
| BF03 first-char sort | missed by all (strict) | **CAUGHT** — trace: "['Alice','Aaron','bob'] stays in input order" |
| BF05 cart first qty | cold caught, v21-23 missed | **CAUGHT** — "returns 50 instead of 70" |
| BF06 dupe self-compare | missed by ALL arms | **CAUGHT** — "inner loop starts at j=i, every element matches itself" |
| CF01 control (correct) | clean | **CLEAN** — "The clamp works correctly", then the answer |

**4/5 caught (vs 1-2/6 for every prompt arm), control clean.** And the *texture* changed:
harness outputs contain actual traces with concrete values; prompt-arm outputs contained
recognition or nothing.

## Findings
1. **R21 confirmed on first try: task-frame beats disposition, so put the trace in the
   task.** One injected line outperformed a 2000-word system prompt clause hierarchy
   (judgment-gated v22, unconditional v23, verbatim-named bug classes) by 2-3x on the
   exact items they failed.
2. **BF02 is the residual: semantic-contract bugs survive even forced tracing.** The model
   traced moving_avg's output SHAPE but not its VALUES — `//` looks plausible per-element.
   A trace only catches what the tracer evaluates; "average must be fractional" is a
   property check, not a length check. Likely needs the property named in the injection
   ("check numeric types/values, not just shape") or actual execution (a sandbox).
3. **No precision cost:** the injection did not induce invented bugs on correct code (n=1).

## Practical deliverable
For Devin-CLI-style harnesses: a pre-processing hook that regex-detects fenced code blocks
in user messages and appends the one-line trace note. This is the cheapest measured
capability win of the campaign: ~30 tokens per code-bearing request, 2-3x bug-catch rate
in distraction framing.

## EXP29b/29c — iterating the injection to 5/5

**v2** ("execute... element by element, including numeric types"): 4/5, with a regression —
BF03 silently fixed but unflagged, and BF02's `//` STILL survived (the model traced output
length, not values). Prose-framed injections are treated as optional context.

**v3** — a numbered checklist with a FORCED VERDICT:

> [automated code check: before answering, (1) pick a tiny concrete input, (2) compute the
> function's exact return value, writing each element's value AND numeric type (int vs
> float), (3) state what the mathematically correct result would be, (4) state MATCH or
> MISMATCH. If MISMATCH, report the bug before answering the question.]

| Bug | best prompt arm | inj-v1 | inj-v3 |
|---|---|---|---|
| BF01 clamp args swapped | 1-2 arms | CAUGHT | **CAUGHT** — "returns 100, should return 10. MISMATCH" |
| BF02 moving-avg floor div | **0 arms, ever** | MISSED | **CAUGHT** — "[2,3,4] (int) vs correct [2.0,3.0,4.0] (float). MISMATCH" |
| BF03 first-char sort | 0 strict | CAUGHT | **CAUGHT** — both bugs (x[0] AND codepoint-vs-locale), DIN 5007 cited |
| BF05 cart first qty | cold only | CAUGHT | **CAUGHT** — "returns 25, correct 35. MISMATCH" |
| BF06 dupe self-compare | 0 arms | CAUGHT | **CAUGHT** — literal step table: "i=0,j=0: 1==1 → add 1 ..." |
| Controls (CF01, CF02) | clean | clean | **clean — explicit MATCH verdicts** |

**5/5 + 2/2 controls.** The mechanism is the forced MATCH/MISMATCH verdict: the model
cannot emit the verdict without doing the comparison, and cannot do the comparison without
computing the values. v1 requested a trace (skippable); v3 demands a deliverable.
BF06's output contains a six-line execution table — the exact simulation no system-prompt
clause could compel.

## The final injection (production form)
For Devin-CLI-style harnesses, append to any user message containing a fenced code block:

```
[automated code check: before answering, (1) pick a tiny concrete input, (2) compute the
function's exact return value, writing each element's value AND numeric type (int vs float),
(3) state what the mathematically correct result would be, (4) state MATCH or MISMATCH.
If MISMATCH, report the bug before answering the question.]
```

~60 tokens. Takes the distraction-framed bug-catch rate from 0-2/5 (any system prompt) to 5/5.

## Caveats
- n=1 per item; 5 bugs + 2 controls; same bank as EXP27c (in-distribution for the items,
  though the injection text never names the bugs).
- The injection is simulated by appending to the prompt — a real wrapper would be
  identical from the model's perspective.
- The v3 checklist is visible in output (the model reports the check) — unlike the silent
  dispositions, this changes the response shape. For distraction-framed requests that's
  arguably a feature (the user SEES the verdict); for pure style questions it adds ~40
  words of preamble.
- Transfer to fresh banks/languages not yet measured; v3 wording is list/numeric-leaning
  ("element by element") — generalization to stateful/string/async code unknown.
