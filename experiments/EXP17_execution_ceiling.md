# EXP17 — Does execution-verification break the prompt-only capability ceiling? YES.

## Goal
EXP12/13 found a hard ceiling: silent-wrong-output bugs (off-by-ones, wrong formulas) under a trivial distractor question were missed by cold, placebo, and every prompt template ~uniformly, because catching them requires *running the code on a concrete input*, not reading it. EXP17 attacks that ceiling directly with an **execute-verify** disposition.

## Design
8-item CEILING bank: 5 silent-wrong-output bugs (the EXP12/13 killers — moving_average drops last window, chunk_count(0)→1, average floor-division, even-length median, fib off-by-one) + 3 CORRECT controls (precision: must NOT invent a bug). Each under a trivial question (type hints / import style / rename / docstring / Black). 4 arms × 2 trials, blind, 2 non-Nemotron judges:
- **cold** — bare model, reason only.
- **v11** — recommended persona, reason only.
- **v12** — v11 + "before concluding, mentally EXECUTE on a concrete input (even-length list, n=0/1) and check the actual output." NO tool.
- **v12tool** — same prompt, but the agent ACTUALLY runs the code via a Python sandbox.

## Result — consensus (BOTH judges PASS). Judge agreement 98% (63/64).
| arm | BUG recall /10 | CONTROL precision /6 |
|---|---|---|
| cold | **2/10** | 6/6 |
| v11 (persona, reason-only) | **8/10** | 6/6 |
| v12 (execute-verify, mental) | **10/10** | 6/6 |
| v12tool (actually runs code) | **10/10** | 6/6 |

McNemar (BUG items, consensus): v11 vs cold **b=6/c=0**; v12 vs v11 **b=2/c=0**; v12 vs cold **b=8/c=0**; **v12tool vs v12 = 0/0 (tie).** 0 degeneration.

## Findings — the ceiling is real, and TWO things lift it

### 1. The execute-verify DISPOSITION cracks the ceiling (cold 2 → v12 10/10).
The exact bugs that defeated every arm in EXP12/13 are now caught essentially perfectly. The instruction "don't trust a read-through; run it on a concrete input that would expose an off-by-one (even-length list, n=0/1) and check the actual output" converts the model's strong-but-unfocused capability into a reliable catch. This is the **first lever in the whole project that lifted the capability ceiling**, not just the disposition floor.

### 2. The SANDBOX adds nothing over mental execution here (v12 = v12tool = 10/10).
This is the surprising, important part. Actually running the code tied mentally tracing it. Why: these are tiny pure functions where Nemotron's *simulation* of `moving_average([1,2,3,4],2)` is accurate once it's prompted to actually do the trace. **The lever is the disposition to evaluate on a concrete input, not the tool.** (Caveat: for larger/stateful/library-heavy code the sandbox should pull ahead — mental execution will break down where real execution won't. This bank is the regime where the disposition alone suffices.)

### 3. v11 (persona, reason-only) is already 8/10 — much better than EXP12/13 implied.
EXP12/13 showed gates≈placebo missing these bugs. But here the *recommended* persona catches 8/10 reason-only. The difference: v11's "specific to a fault, name the number" disposition plus the fresh framing pulls more catches than the earlier templates did. The 2 it missed (fib off-by-one once, moving_average once) are exactly where v12's explicit "trace it" instruction closes the gap. So the ladder is real: **cold 2 → persona 8 → persona+execute-verify 10.**

### 4. Zero precision cost. All arms 6/6 on controls.
Critically, the verification disposition did NOT cause over-skepticism — no arm invented a bug in the 3 correct functions. v12tool's runs even *self-corrected*: one agent initially expected the wrong answer on the first-unique-char control, ran it, saw its expectation was wrong, and reported the code as correct. **Execution is a precision tool as much as a recall tool** — it confirms correctness, it doesn't manufacture problems.

## Implication for the product
The recommendation upgrades. For **code review / correctness tasks specifically**, fold the execute-verify clause into the persona: "don't judge code by reading it — evaluate it on a concrete boundary input and check the actual output." That single disposition took silent-bug recall from 2/10 (cold) to 10/10, with no precision cost and no sandbox required. This is the highest-impact single change found in the entire campaign — it's the one that moved *capability*, not just voice.

## Next (EXP18-19)
- Confirm the sandbox pulls ahead where mental execution should fail: a bank of larger/stateful functions (mutation, accumulation across calls, library behavior) — there v12tool should beat v12.
- Fold execute-verify into v11 → **v13 production template**; re-run the EXP14 mixed battery to confirm VOICE/clean/degeneration don't regress when the code-verify clause is added.
