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

## Caveats
- n=1 per item; 5+1 items; same bank as EXP27c (in-distribution for the items, though the
  injection text never names the bugs).
- The injection is simulated by appending to the prompt — a real wrapper would be
  identical from the model's perspective.
- BF04 not rerun (saturated). Transfer of the injection to fresh banks not yet measured.
