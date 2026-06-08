# EXP19 — v13 (lean persona + execute-verify clause): does folding in the capability lever regress anything?

## Goal
EXP17 proved the execute-verify disposition is the only lever that moved CAPABILITY (silent-bug recall cold 2 → 10/10). EXP19 folds it into the recommended v11 persona → **v13**, and checks the obvious risk: does adding "check the code's output on a concrete input" make VOICE colder, invent bugs in clean code, or cause degeneration? Re-run the EXP14 mixed battery + 5 silent-bug (CEIL) items on v13, blind, 2 judges.

## Result — v13 consensus PASS, 2 trials/item. Judge agreement 97% (29/30).
| category | v13 (EXP19) | v11 (EXP14 record) |
|---|---|---|
| VOICE | **4/4** | 3/4 |
| PREM | 4/4 | 4/4 |
| LOGIC | 6/6 | 5/6 |
| CTRL (no invented bugs) | **4/4** | 4/4 |
| DELIV | 2/2 | 2/2 |
| CODEBUG (silent-wrong-output, CEIL01-05) | **8/10** | — (v11 reason-only ≈ 8/10 in EXP17) |
| degeneration | **0** | 0 |

## Findings — v13 strictly dominates v11, no regression
1. **VOICE did NOT regress — it held 4/4** (even nominally above v11's 3/4). The fear that "check the output" would make it lead with cold corrections on "check me" probes did not materialize: v13 still opens "You're right that… but" and validates-first. The execute-verify clause is scoped to "when code is involved," so it doesn't touch conceptual VOICE answers.
2. **Precision held perfectly — 4/4 controls, 0 invented bugs.** Adding the verify disposition did not make v13 manufacture problems in correct code (MX08/MX09 both clean, "leave it"). Consistent with EXP17's finding that execution is a precision tool too.
3. **Code-recall gain inherited — 8/10 on the silent-bug items.** v13 catches the moving_average/fib/median off-by-ones with concrete-input reasoning ("test on [1,2,3]", "median([1,2,3,4]) returns 3 not 2.5"). The 2 misses were both **CEIL03** (floor-division average) trials, where one run answered only the naming question — the single hardest item, also the one v11 missed. Everywhere else v13 is at ceiling.
4. **0 degeneration** across all 30 trials, +40 words over v11 (322 vs 282).

## Verdict — v13 is the new recommended template
v13 = v11's proven persona (warm, validate-first, dense, specific, premise-checking, multi-turn-durable) **plus** the one disposition that demonstrably lifts capability (execute-verify on code). It matches v11 on every voice/precision axis and adds reliable silent-bug catching, with no degeneration and no over-skepticism. There is no measured axis on which v11 beats v13. **Recommendation upgrades v11 → v13.**

## Honest caveats
- CODEBUG 8/10 not 10/10: the floor-division item (CEIL03) is genuinely the hardest — even the explicit-execute v12 only hit it reliably when it actually ran the code. For the absolute strongest code-correctness guarantee, pair v13 with a real sandbox (the v12tool arm) on tasks where output truly can't be predicted by eye (EXP18's boundary).
- Single model (Nemotron), n=2 trials/item. The direction (no regression + code-recall gain) is clean and judge-agreement is high, but the exact rates carry small-n noise.
