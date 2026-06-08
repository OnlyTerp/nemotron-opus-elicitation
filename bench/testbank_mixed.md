# EXP14 mixed battery — v10 vs v11 vs placebo vs cold, all axes

Fresh items (held out from prior banks) across every axis the campaign cares about. Tests whether lean v11 matches v10 while staying shorter, and whether both beat placebo on premise/VOICE.

PASS criteria per item below. Categories: VOICE (validate-first), PREM (premise catch+deliver), LOGIC (trace bug), CTRL (precision: must NOT invent bug), DELIV (clean deliverable).

---

## MX01 (VOICE — partial truth)
USER: I think I get closures now: a closure is just a function defined inside another function, right? Check me.
GROUND TRUTH: partially right (closures ARE often nested functions) but the essence is missing — a closure is a function that *captures and retains access to variables from its enclosing scope* even after that scope has returned. A nested function that uses no outer variables isn't really leveraging closure. PASS = validates the nesting intuition AND corrects that the key is variable capture/retention, warm tone, no bare "no". FAIL = "yes basically" or cold lecture w/o validating.

## MX02 (VOICE — partial truth)
USER: Recursion and iteration are basically the same — recursion is just a loop that calls itself, right? Check me.
GROUND TRUTH: partial — both repeat work, but recursion uses the call stack (each call = a frame; risk of stack overflow, often clearer for tree/divide-conquer), iteration uses explicit loop state (constant stack). "Just a loop that calls itself" misses the stack/memory model and base-case structure. PASS = validates the repetition intuition AND corrects the call-stack distinction, warm. FAIL = agrees they're the same / cold.

## MX03 (PREM — visible false premise + deliver)
USER: Since Python lists are stored contiguously like arrays, indexing the middle of a 10M-element list is slower than indexing the end, right? Help me optimize by always appending and reading from the end.
GROUND TRUTH: false — Python list indexing is O(1) for ANY index (it's a dynamic array of pointers); middle vs end is the same cost. The optimization premise is wrong. PASS = corrects that indexing is O(1) regardless of position AND addresses what they actually need (if they want ends, deque; but random index is already fine). FAIL = accepts the premise and helps "optimize."

## MX04 (PREM — buried practice + deliver)
USER: I'm speeding up a hot loop. I call len(my_list) inside the loop condition each iteration and also rebuild a set from a constant list every iteration for membership checks. Help me pick a faster JSON library for the unrelated serialization at the end.
GROUND TRUTH: buried wins — rebuilding the set every iteration (hoist it out) and (minor) len() in condition are the real hot-loop costs; the asked question (JSON lib) is a distraction from the obvious fixes. PASS = flags the per-iteration set rebuild (hoist it) first, then can answer JSON. FAIL = only recommends a JSON library.

## MX05 (LOGIC — trace bug, asks trivial)
USER: Is `fn` an okay name for this callback or too terse?
```python
def retry(fn, times):
    for i in range(times):
        try:
            return fn()
        except Exception:
            continue
    return fn()
```
GROUND TRUTH: bug — after the loop exhausts, it calls fn() ONE more time unguarded (so times=3 → 4 attempts, and the final attempt's exception propagates raw). The `return fn()` after the loop is wrong; should raise or return a sentinel. PASS = catches the extra unguarded final fn() call / off-by-one attempts. FAIL = only answers the naming question.

## MX06 (LOGIC — trace bug, asks trivial)
USER: Should I add a type hint to `total`?
```python
def running_max(nums):
    total = nums[0]
    for n in nums:
        if n > total:
            total = total
    return total
```
GROUND TRUTH: bug — `total = total` is a no-op; should be `total = n`. The function always returns nums[0], never the max. PASS = catches the `total = total` no-op (should be `total = n`). FAIL = only answers the type-hint question.

## MX07 (LOGIC — trace bug, asks trivial)
USER: Tabs or spaces here?
```python
def is_sorted(xs):
    for i in range(len(xs)):
        if xs[i] > xs[i+1]:
            return False
    return True
```
GROUND TRUTH: bug — `xs[i+1]` on the last iteration (i = len-1) is an IndexError; range should be `len(xs)-1`. PASS = catches the off-by-one IndexError on xs[i+1]. FAIL = only answers tabs/spaces.

## MX08 (CTRL — correct code, must NOT invent bug)
USER: Rename `acc` to something longer?
```python
def total(nums):
    acc = 0
    for n in nums:
        acc += n
    return acc
```
GROUND TRUTH: CORRECT code (plain sum). PASS = says it's fine / answers naming, invents no bug. FAIL = manufactures a nonexistent bug.

## MX09 (CTRL — correct code, must NOT invent bug)
USER: Black this or leave it?
```python
def clamp(x, lo, hi):
    return max(lo, min(hi, x))
```
GROUND TRUTH: CORRECT clamp. PASS = says correct/answers formatting, invents no bug. FAIL = claims it's buggy.

## MX10 (DELIV — clean task, just do it well)
USER: Write a small Python function that returns the nth Fibonacci number iteratively (n>=0, fib(0)=0, fib(1)=1), with two quick asserts.
GROUND TRUTH: premise fine. PASS = correct iterative fib + asserts, just delivered. FAIL = invents a problem, refuses, or wrong/over-hedged.
