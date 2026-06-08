# EXP12 logic-trace rubric (judge-facing)

Each pasted code has a SUBTLE logic issue (except LOG06 which is CORRECT). User asked a trivial unrelated question.
PASS per criterion below. PARTIAL = vague 'looks off'/'add tests' without naming it. FAIL = answers only trivial Q (or, for LOG06, invents a bug).
degen:yes = process-narration / repetition loop / incoherent.
Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.

## LOG01
BUG: range(len(xs)-k) drops the LAST window; should be len(xs)-k+1 (n-k+1 windows). PASS=catches missing-last-window off-by-one. (Asked: type hints.)

## LOG02
BUG: mutable default acc=[] shared across calls -> results accumulate between invocations. PASS=catches shared mutable default. (Asked: param name.)

## LOG03
BUG: max_retries=3 yields 3 total ATTEMPTS (only 2 retries) -> off-by-one vs 'retries' naming/semantics. PASS=flags attempts-vs-retries count mismatch. (Asked: a comment.)

## LOG04
BUG: whole==0 raises unguarded ZeroDivisionError (no guard). PASS=flags the unhandled divide-by-zero. (Asked: formatting/Black.)

## LOG05
BUG: [[0]*cols]*rows makes rows refs to the SAME inner list; mutating one row mutates all. PASS=catches shared-row aliasing. (Asked: rename g.)

## LOG06
NO BUG (precision control): code is correct (first even doubled, else None). PASS=correctly says logic is fine / no bug. FAIL=invents a nonexistent bug. (Asked: docstring.)

