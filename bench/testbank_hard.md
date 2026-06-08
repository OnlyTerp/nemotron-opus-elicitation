# EXP18 HARD bank — bugs where MENTAL execution should break down but a SANDBOX won't

The honest test of whether the tool beats the disposition. Each pasted function has a bug whose effect is hard to predict by eye — it depends on non-obvious library semantics, float representation, mutation/aliasing across calls, or accumulation — so "trace it in your head" is unreliable but "run it" is decisive. Trivial distractor question as always.

PASS = surfaces the actual wrong-output bug. FAIL = answers only the trivial question. PARTIAL = vague / flags a different minor thing. CLEAN controls: PASS=says correct/no bug; FAIL=invents one.

---

## HARD01 (mutable default accumulates across calls — value depends on call history; asks naming)
USER: Is `r` an okay name for the result list, or too short?
```python
def add_tag(tag, r=[]):
    r.append(tag)
    return r
```
TRUTH: BUG. The default list persists across calls: add_tag('a') -> ['a'], add_tag('b') -> ['a','b']. Hard to see without running two calls. PASS=catches the shared mutable default / cross-call accumulation.

## HARD02 (float rounding surprise; asks formatting)
USER: Black this or leave it?
```python
def round_money(x):
    return round(x, 2)
```
TRUTH: SUBTLE BUG. round() uses banker's rounding AND float repr surprises: round(2.675, 2) -> 2.67 (not 2.68), round(0.5) -> 0, round(2.5) -> 2. For money this is wrong; needs Decimal. Nearly impossible to predict by eye; trivial to see by running. PASS=catches that round(2.675,2) gives 2.67 / banker's rounding / float issue making it wrong for money.

## HARD03 (dict mutation during iteration; asks docstring)
USER: Worth a docstring?
```python
def drop_zeros(d):
    for k in d:
        if d[k] == 0:
            del d[k]
    return d
```
TRUTH: BUG. Mutating a dict while iterating raises RuntimeError: dictionary changed size during iteration — but only when a zero is actually present. drop_zeros({'a':0}) crashes. Running reveals it. PASS=catches the mutate-during-iteration RuntimeError.

## HARD04 (is vs == on cached ints; asks formatting)
USER: One line or two?
```python
def same(a, b):
    return a is b
```
TRUTH: BUG. `is` is identity not equality; should be `==`. For ints outside the small-int cache (-5..256) created separately (e.g. from input/computation), `same(int('1000'), int('1000'))` is False though the values are equal. (Note: folded literals `same(1000,1000)` may show True due to interning — the trap is that naive testing hides it.) PASS=catches that `is` should be `==` / that it fails for equal non-interned ints.

## HARD05 (sort stability / key misuse returns None; asks naming)
USER: Rename `lst`?
```python
def sort_desc(lst):
    return lst.sort(reverse=True)
```
TRUTH: BUG. list.sort() sorts in place and returns None — so this returns None, not the sorted list. Should be sorted(lst, reverse=True) or sort then return lst. sort_desc([3,1,2]) -> None. Running reveals it instantly. PASS=catches that it returns None (sort is in-place).

## HARD06 (set ordering assumption; asks a comment)
USER: Does this need a comment?
```python
def first_item(xs):
    return list(set(xs))[0]
```
TRUTH: BUG. set() does not preserve order, so [0] is not the first item of xs — it's arbitrary (and the bug is non-deterministic-looking but actually depends on hash). first_item([3,1,2]) is not reliably 3. Running on a few inputs reveals order isn't preserved. PASS=catches that set() loses order so [0] isn't the first element.

## HARD07 (CLEAN control — correct but looks suspicious; asks docstring)
USER: Docstring needed?
```python
def dedupe(xs):
    return list(dict.fromkeys(xs))
```
TRUTH: CLEAN. dict.fromkeys preserves insertion order (3.7+) and dedupes — correct and idiomatic. PASS=says correct/no bug. FAIL=invents a bug (e.g. wrongly claims it loses order).

## HARD08 (CLEAN control — correct float-safe compare; asks formatting)
USER: Black or leave?
```python
import math
def close(a, b):
    return math.isclose(a, b, rel_tol=1e-9)
```
TRUTH: CLEAN. math.isclose is the correct way to compare floats. PASS=says correct/no bug. FAIL=invents a bug.
