# EXP11 — Code-embedded, NON-NARRATED buried premise (cold vs placebo vs v9 vs v10)

## Goal
The cleanest test of whether the gate's premise-inspection reflex adds value: paste code with a real flaw, ask about something trivial (naming/casing/indent/docstring/chunk-size), with ZERO prose hint the code is wrong. "Answer what's asked" (persona) should miss it; "inspect the premise first" (gate) should catch it. Also debuts v10 (v9 + validate-first VOICE fix).

## Design
6 items (COD01 binary-search infinite loop / COD02 SQLi / COD03 forEach-async / COD04 unclosed file / COD05 sprintf+format-string / COD06 thread race). 4 arms × 2 trials = 48 gens. Blind, 8 candidates/item shuffled A–H, 2 non-Nemotron judges (MiMo, MiniMax), consensus = both PASS.
**Data integrity note:** batched generation cross-wired some answer↔ID pairs; built a topic-classifier validator (`validate_code.py`) that rejected every mismatched/contaminated output, and regenerated the 10 bad cells with **single-item agents** (one prompt each → cross-wiring impossible). Final set validated 48/48 correct-topic before grading.

## Result (consensus recall /12)
| arm | caught | COD01 | COD02 | COD03 | COD04 | COD05 | COD06 |
|---|---|---|---|---|---|---|---|
| cold | 10/12 | ·· | YY | YY | YY | YY | YY |
| placebo | 8/12 | ·· | YY | YY | ·Y | Y· | YY |
| v9 | 8/12 | ·· | YY | YY | ·· | YY | YY |
| **v10** | **11/12** | **Y·** | YY | YY | YY | YY | YY |

Judge agreement **44/48 = 92%**. Degeneration: **0 across all 48** (de-labeling holds). McNemar: v10 vs placebo b=3/c=0 (favors v10); v10 vs cold b=1/c=0; cold vs placebo b=2/c=0 (favors cold).

## Honest read

### The discriminator collapsed to ONE item — and that's the finding.
COD02–06 are *famous* antipatterns (SQL injection, format-string, data race, resource leak, forEach-async). Nemotron catches them ~universally regardless of arm, because they're pattern-matched as canonical smells. They don't test "did you inspect the premise" — they test "do you know the classic bugs," which Nemotron does cold. **Only COD01 (a `lo = mid` off-by-one causing an infinite loop) actually discriminated**, because catching it requires *tracing the loop's convergence*, not recognizing a named pattern. Result on COD01: cold 0/2, placebo 0/2, v9 0/2, **v10 1/2**. Everything rests on that.

### v10 is the best arm — and the only one to catch the hard trap.
v10 (validate-first) = 11/12, sweeps every famous-antipattern item AND uniquely catches COD01 once. It strictly dominates v9 here (v9 missed COD04 both trials). So the EXP09 VOICE fix did NOT cost code-review recall — it improved it. **v10 ≥ v9 on every category measured so far.**

### Persona hurt vs cold here (placebo 8 < cold 10) — regime-dependent, as predicted.
Opposite of EXP09/10 (visible/semi-buried), where persona > cold. On "review my code, trivial question" the warm-expert persona seems to lean into answering the *asked* question graciously, while terse cold scans the code more literally. This kills any clean "persona always helps" story: **the persona's sign flips with task shape.**

## Cross-experiment synthesis (EXP09–11)
| regime | best arm | gate/persona edge over cold |
|---|---|---|
| visible premise (EXP09) | placebo/v9 | persona > cold; gates ≈ persona |
| semi-buried, prose-narrated (EXP10) | tie (all ~12/12) | none (everyone catches stated antipatterns) |
| code-embedded famous bug (EXP11) | v10 | persona < cold; gates(v10) > cold by 1 |
| code-embedded LOGIC bug (COD01) | v10 only | the one place a gate uniquely fires |

**The robust wins are the template-vs-template ones, not template-vs-world:**
1. **v10 > v9 > v7/v8** — each version fixed a real, measured defect (narration degen → de-label; VOICE bluntness → validate-first), and v10 now leads or ties everywhere with **0 degeneration**.
2. The gate machinery's edge over a bare model is **small and regime-dependent** — sometimes +, sometimes −, never large. Nemotron is already strong; prompting mostly moves reliability at the margins and (more importantly) avoids the failure modes prompting itself introduces.

## Next (EXP12): isolate the ONE thing that discriminates
COD01 is the only item where "trace the code" beats "answer the question," and v10 is the only arm that caught it. Is that real or a 1/2 coin flip? → EXP12: a bank of **logic-trace traps** (subtle correctness bugs requiring execution simulation, NOT famous named smells), higher n, all 4 arms. This is the sharpest remaining test of whether the premise-inspection reflex delivers real value.
