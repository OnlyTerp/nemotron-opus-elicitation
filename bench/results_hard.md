# EXP18 results — HARD bank (does the SANDBOX beat mental execution?)

- mimo: 48/48 cells | minimax: 48/48 cells | judge agreement 45/48 = 94%

## Consensus (BOTH judges PASS)
| arm | BUG recall /12 | CONTROL precision /4 | per-bug (t1t2) |
|---|---|---|---|
| cold | 8/12 | 4/4 | 01:YY 02:.Y 03:.Y 04:.. 05:YY 06:YY |
| v12 (mental execute-verify) | **12/12** | 4/4 | all caught |
| v12tool (real sandbox) | **12/12** | 4/4 | all caught |

## The key question — answered, and it's a NEGATIVE for "the tool helps"
- **v12tool vs v12 on all bug items: b=0, c=0 → exact TIE.** Even on HARD02 (banker's-rounding `round(2.675,2)=2.67`), the predicted sandbox win, mental v12 already nailed it (it *knows* the banker's-rounding fact without running it).
- **v12 vs cold: b=4, c=0** — the execute-verify disposition again beats bare model.
- Controls 4/4 all arms — no over-skepticism, no invented bugs.

## Honest read
EXP18 was designed to find where the SANDBOX finally pulls ahead of mental tracing — bugs depending on non-obvious library/float/aliasing semantics. It did NOT find it. Two reasons:
1. **Most "hard" Python bugs are FAMOUS** (mutable default, `is`-identity, sort-returns-None, dict-mutation-during-iteration, set-unordered). Nemotron recognizes them by name on sight — cold got 8/12 — so neither mental nor real execution is needed.
2. **For the one genuinely compute-dependent item (float rounding), Nemotron already KNOWS the gotcha fact** ("round uses banker's rounding, 2.675→2.67") as declarative knowledge, so mental v12 stated the exact wrong value without running it.

**Conclusion across EXP17+18: the lever is the execute-verify DISPOSITION, not the sandbox.** On small, famous, or fact-backed code, "decide to check the output on a concrete input" is sufficient whether or not you actually run it. The sandbox would only pull ahead on code whose output Nemotron genuinely cannot predict — large/stateful/novel logic, real I/O, heavy numeric computation — which this bank (and most short code-review snippets) does not contain. That's a real boundary, not a win for tools on everyday review tasks.

**Product implication:** fold the execute-verify *disposition* into the template (cheap, no infra). Reserve the actual sandbox for genuinely uncomputable-by-eye tasks; for short code review it buys nothing over the disposition.
