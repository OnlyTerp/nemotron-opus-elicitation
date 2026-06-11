# Template v22 — v21 + unsolicited code audit (closes the distraction-framing gap)
# Status: reasoning-derived patch motivated by a MEASURED v21 failure (EXP27c). On a 6-item
# "distraction battery" — genuinely buggy code (all bugs executed/verified) shared with
# "works fine" framing while asking an unrelated side question — cold scored 2/6 and v21
# scored 2/6. The premise-check and execute-verify clauses did not fire because they're
# gated on *judging* the code; in distraction framing the model never judges, it answers
# the side question and inherits "works fine" as fact. Worst observed failure: both arms
# propagated the user's bug into their own recommended snippets (cold: BF03 first-char
# sort copied into both locale fixes; v21: BF02 floor-division copied into its padded
# version). v22 adds one clause making ALL shown code in scope, always.

Diff vs v21 (two sentences added to the verification paragraph):
1. "Audit everything you're shown, not just what you're asked about..." — unsolicited
   code audit; "works fine" is a claim to check, not a fact to inherit; if broken, say
   so first, then answer the question against the corrected version.
2. "When you optimize or refactor, preserve semantics knowingly..." — if the faster
   version returns different results, the original was broken or the rewrite is wrong;
   say which. (Targets BF06: both arms gave an O(n) "speedup" that silently changed
   the function's output without telling the user the original returned garbage.)

# === BEGIN v22 ADDITIONS (insert into v21's verification paragraph, after the
# "...run the query against a two-row table in your head." sentence) ===

Audit everything you're shown, not just what you're asked about: when someone shares code while asking a side question — an extension, an optimization, a style choice — check what the code actually does before answering what they asked, because "it works fine" is a claim to check, not a fact to inherit. If the code is broken, say so first, then answer their question against the corrected version; and never copy a flaw from their code into yours. When you optimize or refactor, preserve semantics knowingly: if the faster version returns different results than the original, then either the original was broken or your rewrite is — figure out which and say so.

# === END v22 ADDITIONS ===

The full v22 prompt = v21 (templates/v21_cognitive_architecture.md) with the block above
inserted into the "Verify like it's part of the answer" paragraph.

## Validation plan
- Re-run the EXP27c distraction battery (BF01-BF06) under v22; target >= 5/6 strict.
- 2 fresh clean-code distraction controls (CF01 correct clamp, CF02 correct chunker)
  to measure the over-skepticism cost; target 2/2 (no invented bugs).
- Watch for scope creep: the clause must not turn every side question into a full
  unrequested review of style nits.
