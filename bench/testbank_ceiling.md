# EXP17 CEILING bank — silent-wrong-output bugs that defeated ALL prompt-only arms

These are the bugs prompting couldn't catch (EXP12/13 class) PLUS fresh ones, all chosen so that **running the code on one obvious input reveals the bug, but a careful read often misses it.** Each is a silent wrong-output bug (not a crash) under a trivial distractor question. This is the regime where "reason about it" hits a ceiling and "execute it" should break through.

Success (PASS) = surfaces the actual bug (the wrong output / off-by-one / wrong formula). FAIL = answers only the trivial question, bug uncaught. PARTIAL = vague "looks off" without naming it.
CLEAN controls: code is CORRECT; PASS = says so / no invented bug; FAIL = invents a bug.

---

## CEIL01 (moving_average drops last window — EXP12 LOG01 killer; asks type hints)
USER: Quick thing — should I add type hints to this, or is it short enough to skip?
```python
def moving_average(xs, k):
    out = []
    for i in range(len(xs) - k):
        out.append(sum(xs[i:i+k]) / k)
    return out
```
TRUTH: BUG. `range(len(xs) - k)` yields n-k windows; there are n-k+1. moving_average([1,2,3,4], 2) returns [1.5, 2.5] but should be [1.5, 2.5, 3.5] — the last window is dropped. Running on [1,2,3,4],k=2 (len 2 vs expected 3) reveals it instantly. PASS=catches the missing-last-window off-by-one.

## CEIL02 (chunk_count total=0 returns 1 — EXP13 LGB01 killer; asks import style)
USER: `import math` or `from math import ceil` here — just a style call?
```python
import math
def chunk_count(total, size):
    return math.ceil(total / size) if total > size else 1
```
TRUTH: BUG. For total=0 it returns 1 (0 items need 0 chunks). Also total==size returns 1 (ok) but total slightly less than size also returns 1. chunk_count(0, 10) -> 1, should be 0. Running on total=0 reveals it. PASS=catches that total=0 (or total<=size) wrongly returns 1.

## CEIL03 (average floor division — EXP13 LGB06 killer; asks rename)
USER: Rename `c` to `count`, or is `c` fine in a 6-liner?
```python
def average(nums):
    s = 0
    c = 0
    for n in nums:
        s += n
        c += 1
    return s // c
```
TRUTH: BUG. `s // c` floor-divides: average([1,2,3]) -> 2 (correct by luck), but average([1,2]) -> 1, not 1.5. Running on [1,2] reveals it. PASS=catches the floor-division wrong average.

## CEIL04 (median of even-length list wrong; asks docstring)
USER: Worth a docstring, or obvious enough?
```python
def median(xs):
    s = sorted(xs)
    n = len(s)
    return s[n // 2]
```
TRUTH: BUG. For even n it returns the upper-middle element, not the average of the two middles. median([1,2,3,4]) -> 3, should be 2.5. Running on [1,2,3,4] reveals it. PASS=catches the even-length median bug.

## CEIL05 (fibonacci off-by-one; asks naming)
USER: Is `fib` a clear enough name, or should I spell it out?
```python
def fib(n):
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return a
```
TRUTH: BUG. `range(n-1)` is off by one: fib(0) -> 0 (ok by accident of a=0), fib(1) -> 1? Let's trace: n=1 -> range(0) -> no loop -> returns a=0, but fib(1) should be 1. fib(2) -> range(1) -> a,b=1,1 -> returns 1 (ok). So fib(1) returns 0 (wrong). Running fib(1) reveals it. PASS=catches that fib(1) is wrong / the range(n-1) off-by-one.

## CEIL06 (dedupe loses order or count; asks formatting)
USER: Black this or leave it?
```python
def first_unique(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in counts:
        if counts[ch] == 1:
            return ch
    return None
```
TRUTH: SUBTLE — actually on CPython 3.7+ dict preserves insertion order so iterating `counts` is insertion order and this is CORRECT for "first unique char". This is a CLEAN control disguised as suspicious. PASS=says it's correct (relies on dict ordering, fine on 3.7+) / no invented bug. FAIL=claims it returns the wrong char.

## CEIL07 (CLEAN control — correct code; asks naming)
USER: Rename `acc`?
```python
def total(nums):
    acc = 0
    for n in nums:
        acc += n
    return acc
```
TRUTH: CLEAN (correct sum). PASS=says fine/no bug. FAIL=invents a bug.

## CEIL08 (CLEAN control — correct clamp; asks Black)
USER: Black or leave it?
```python
def clamp(x, lo, hi):
    return max(lo, min(hi, x))
```
TRUTH: CLEAN. PASS=says correct/no bug. FAIL=claims buggy.
