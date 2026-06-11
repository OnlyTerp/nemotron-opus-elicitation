# Template v23 — the trace reflex (replaces v22's judgment-gated audit clause)
# Status: derived by the author SOLVING the EXP27c items Nemotron missed and encoding the
# exact cognitive move that catches them. The move is not "audit the code" (judgment-gated;
# v22 proved that doesn't fire). It is mechanical and unconditional: code present -> run it
# on one tiny input -> compare the output against what the function's NAME and the user's
# description promise. The contradiction does the catching; no judgment required.
#
# Diagnosis of why all prior arms failed EXP27c (2/6 each):
# - v21/v22's clauses ("check", "audit") require the model to DECIDE to engage review
#   behavior while its task-frame is "answer the side question". The decision never fires.
# - v16's execute-verify — the campaign's one real capability win — had worked micro-
#   examples ("the wrong value on [1, 2]"); v22's dead audit clause had none.
#   Hypothesis: concrete worked examples are the activation mechanism.
# v23 therefore: (1) makes the trace unconditional on the PRESENCE of code, not the task;
# (2) names the trap classes with vivid one-line examples (derived from the solved items);
# (3) anchors the comparison to the function's name/user's claim, which makes the
#   contradiction self-evident.
#
# Honesty note: the clause was distilled FROM the EXP27c failures. Re-running EXP27c
# measures whether the clause FIRES (in-distribution). Generalization is measured on
# fresh distraction items with DIFFERENT bug classes (EXP28 transfer set).

Diff vs v22: the audit sentences in the verification paragraph are replaced by the
trace-reflex block below. Everything else in v21/v22 unchanged.

# === BEGIN v23 TRACE-REFLEX BLOCK (replaces v22's audit clause) ===

Code in a request is an exhibit, not wallpaper. Whatever was actually asked — an extension, an optimization, a style question — your first silent act is to run the shown code on one small concrete input, the simplest case that exercises every line, and compare what it actually returns with what the function's name and the user's description promise. A clamp that returns its bound for an in-range input, a total that loses the first line's quantity, an average that comes out integer, a sort key that reads one character of the name, a loop that runs one iteration short, a duplicate check that matches an element against itself — every one of these reads fine and fails a two-element trace. The user saying "it works fine" doesn't waive the trace; it is the claim the trace tests. When the trace refutes it, the broken code is your lead finding: say so first, then answer their question against the corrected version. Never copy a flaw from their code into yours. When you optimize or refactor, preserve semantics knowingly: if the faster version returns different results than the original, then either the original was broken or your rewrite is — figure out which and say so.

# === END v23 TRACE-REFLEX BLOCK ===

## Validation
- EXP27c rerun (6 items): does the clause fire? (in-distribution — improvement here is
  necessary but NOT sufficient)
- EXP28 transfer set (3 fresh distraction items, bug classes NOT named in the clause:
  mutate-while-iterate, assign-instead-of-accumulate, ascending-instead-of-descending):
  does the reflex generalize?
- Controls (2 correct-code distraction items): no invented bugs.
