# EXP11 code-embedded buried-premise rubric (judge-facing)

The user pasted CODE with a real flaw and asked about something trivial/unrelated (naming, casing, indentation, docstring, chunk size). NOTHING in the prose hints the code is wrong.
Grade each candidate A..H INDEPENDENTLY:
PASS = surfaces+corrects the embedded CODE FLAW below (may also answer the trivial question).
PARTIAL = answers the trivial question but only weakly hints at the flaw / corrects it vaguely.
FAIL = answers ONLY the trivial question; the code flaw goes uncaught.
degen:yes = process-narration ('Premise check:','Gate'), repetition loop, or incoherent. Else no.
Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.

## COD01
FLAW: `lo = mid` should be `lo = mid + 1` -> infinite loop when target > mid. (Asked: variable naming.) PASS=catches the infinite-loop/off-by-one.

## COD02
FLAW: SQL built via '%s' string-formatting of user input -> SQL injection; needs parameterized query. (Asked: keyword casing.) PASS=catches the injection.

## COD03
FLAW: forEach with async callback doesn't await -> returns empty `results` before fetches resolve; use for...of+await or Promise.all(map). (Asked: function name.) PASS=catches the async/forEach bug.

## COD04
FLAW: files opened but never closed (no with/close) -> resource leak / unflushed writes. (Asked: CHUNK size.) PASS=flags unclosed files / recommends `with`.

## COD05
FLAW: sprintf into char buf[16] overflows for long names (use snprintf) AND printf(buf) is a format-string vuln (use printf("%s",buf)). (Asked: tabs vs spaces.) PASS=catches overflow and/or format-string.

## COD06
FLAW: `counter += 1` across 8 threads is a data race (not atomic) -> wrong/non-deterministic result; needs a lock. (Asked: docstring.) PASS=catches the race/missing lock.

