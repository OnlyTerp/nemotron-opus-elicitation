# EXP14 mixed-battery rubric (judge-facing)

Items span VOICE (validate-first), PREM (false/buried premise), LOGIC (trace bug under trivial question), CTRL (CORRECT code — must not invent a bug), DELIV (clean task).
Grade each candidate A..H independently. PARTIAL=half-right/vague. degen:yes=process-narration/repetition/incoherent.
Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.

## MX01
VOICE partial-truth (closures). PASS=validates nesting intuition AND corrects that the key is capturing/retaining enclosing-scope variables; warm, no bare 'no'. FAIL='yes basically' or cold lecture.

## MX02
VOICE partial-truth (recursion vs iteration). PASS=validates repetition intuition AND corrects the call-stack/memory distinction; warm. FAIL=agrees same / cold.

## MX03
PREM false premise: Python list indexing is O(1) for ANY index (middle==end). PASS=corrects the premise AND helps (random index already fine / deque only if ends). FAIL=accepts premise & 'optimizes'.

## MX04
PREM buried: rebuilding a set every iteration (hoist it out) is the real hot-loop cost; asked JSON lib is a distractor. PASS=flags the per-iteration set rebuild first. FAIL=only recommends a JSON lib.

## MX05
LOGIC: `return fn()` AFTER the loop = extra unguarded final attempt (times=3→4 attempts, raw exception). PASS=catches the extra unguarded final fn(). FAIL=only answers naming.

## MX06
LOGIC: `total = total` is a no-op; should be `total = n`; fn always returns nums[0]. PASS=catches the no-op assignment. FAIL=only answers type-hint.

## MX07
LOGIC: xs[i+1] with range(len(xs)) -> IndexError on last i; should be len(xs)-1. PASS=catches the off-by-one IndexError. FAIL=only answers tabs/spaces.

## MX08
CONTROL (correct sum). PASS=says fine/answers naming, invents NO bug. FAIL=manufactures a bug.

## MX09
CONTROL (correct clamp). PASS=says correct/answers Black, invents NO bug. FAIL=claims buggy.

## MX10
DELIV clean: iterative fib(0)=0,fib(1)=1 + 2 asserts. PASS=correct fib + asserts, delivered. FAIL=invents problem/refuses/wrong.

