# EXP20 — Does verify-by-substitution generalize the capability lever to NON-code reasoning?

## Goal
EXP17-19 found execute-verify lifts the CODE-correctness ceiling. Does the same disposition ("put your answer back into the problem's constraints and check it") lift NON-code reasoning? Test on word problems with a seductive-but-wrong intuitive answer (CRT-style), where back-substitution reveals the error — the non-code analog of "run the code." Arms: cold, v13, v14 (= v13 + reasoning-verify clause). 2 trials, auto-graded against verified ground truth.

## Bank
8 traps (bat&ball $0.05; widgets 5min; lily pad 47; fresh laptop/case $20; fresh painters 8h; inclusion-exclusion 3; percentage 20%-then-20% = lower 4%; snail 8 days) + 2 easy controls. All ground truths verified by execution.

## Result — auto-graded, deterministic
| arm | TRAP recall /16 | CONTROL /4 |
|---|---|---|
| cold | **16/16** | 4/4 |
| v13 | **16/16** | 4/4 |
| v14 | **16/16** | 4/4 |

**Dead-flat null result.** Every arm aced every trap and every control.

## Finding — there's no reasoning deficit here to lift
Unlike code (where cold was 2/10 on silent bugs), Nemotron **already solves classic CRT/word-problem traps perfectly cold** — including the fresh-parameterized variants ($540 laptop/case, 40 painters) that rule out memorization. Cold's full answers even **spontaneously back-substitute**: *"The ball costs $0.05. If the ball is $0.05, the bat is $1.05 (which is $1.00 more), and together they total $1.10."* The verify-by-substitution disposition v14 adds is already present in the base model for this task class.

## Why this is the RIGHT null result (and consistent with the whole campaign)
The campaign's through-line: **prompting only helps where the base model has a genuine disposition deficit.**
- Code correctness (EXP17): real deficit (cold eyeballs code, misses silent bugs) → execute-verify lifts it 2→10.
- CRT reasoning (EXP20): NO deficit (cold already verifies arithmetic by reflex) → reasoning-verify is a no-op.
- Just as the persona was a no-op on Qwen (EXP16, no VOICE deficit), reasoning-verify is a no-op on Nemotron's math reflex (EXP20, no reasoning deficit).

**The lever only fires where the gap is.** This sharpens, not weakens, the thesis: capability prompting = supplying a missing disposition; supply one the model already has and you get nothing.

## Decision on v14
**Do NOT promote v14 over v13.** The reasoning-verify clause adds length (+38 words) for zero measured benefit on the task class it targets, and adding always-on clauses that don't pay their way risks diluting attention (the lesson of the over-engineered gate templates). v13 remains the recommendation. Keep v14 in the repo as the documented negative result.

## Honest caveats
- These traps, while fresh-parameterized, are still *standard genres* (CRT, work-rate, inclusion-exclusion, percentage, snail-in-well). A harder bank — multi-step constraint-satisfaction where the wrong answer is only caught by checking a non-obvious condition — might still reveal a deficit. EXP20 shows reasoning-verify doesn't help on *common* reflexively-checkable traps; it doesn't prove no reasoning lever exists anywhere. But on the obvious candidate class, the answer is a clean no.
- Single model, n=2; but with 16/16 across all three arms the ceiling/floor are both saturated — more trials won't move a unanimous result.
