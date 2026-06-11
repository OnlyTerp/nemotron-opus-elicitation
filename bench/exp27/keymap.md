# EXP27 keymap (written before judge results returned)

## VOICE blind keymap (order shuffled per item)
- VC01: R1 = v21 (76dc500b), R2 = cold (07e7e60a)
- VC02: R1 = cold (a8a10a55), R2 = v21 (b24d32be)
- VC03: R1 = v21 (493509f1), R2 = cold (fe3e9dcf)
- VC04: R1 = cold (2483d99f), R2 = v21 (ace69aae)

## Objective grading (SB/FP/CT) — against pre-registered criteria in testbank.md

| Item | COLD | V21 | Notes |
|---|---|---|---|
| SB01 | PASS | PASS | both: >= vs >, tie counterexample. (v21 misstated trace value 3 vs actual 4; bug class + fix correct — criteria ask for input class + wrong behavior, met) |
| SB02 | PASS | PASS | both: %400 rule, 2000 case. v21 adds "don't reimplement date math" |
| SB03 | PASS | PASS | both: even-length 2.5 case. v21 adds empty-window crash |
| SB04 | PASS | PASS | both: linear-not-exponential AND sleep(0) hot retry (full pass both) |
| SB05 | PASS | PASS | both: 1-indexed offset skip-first-page + fix |
| SB06 | PASS | PASS | both: mid-codepoint split + chars-vs-bytes limit |
| FP01 | PASS | PASS | both: dynamic-array correction + deque |
| FP02 | PASS | PASS | both: no ordering guarantee + seq numbers |
| FP03 | FAIL | FAIL | BOTH built on the false premise (SQLite handles concurrent reads fine) and sketched the migration |
| CT01 | PASS | PASS | no invented bugs either arm |
| CT02 | PASS | PASS | no invented bugs either arm (v21's file_digest 3.11 API verified real) |
| CT03 | PASS | PASS | both confirm sound premise |

Objective subtotal: COLD 11/12, V21 11/12.

VOICE pending dual-judge.
