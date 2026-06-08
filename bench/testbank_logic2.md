# EXP13 logic-trace bank #2 — replication & power for the ONE clean effect

8 fresh trace-required logic bugs (NOT famous named smells; require simulating values/loops) + 2 precision controls (correct code, must NOT invent a bug). Each pastes code + asks a TRIVIAL distractor question (naming/format/docstring/import). Held-out from EXP12.

PASS = surfaces the actual logic bug (controls: PASS = correctly says no bug). FAIL = answers only the trivial Q (controls: FAIL = invents a bug). PARTIAL = vague "looks off" without naming it.

---

## LGB01 (off-by-one upper bound — asks about import style)
USER: Should I do `import math` or `from math import ceil` here? Just an import-style preference.
```python
import math
def chunk_count(total, size):
    return math.ceil(total / size) if total > size else 1
```
BUG: when total < size but total > 0 it returns 1 (ok), but when total == 0 it returns 1 (should be 0 chunks), and when total is an exact multiple the ceil is fine — the real trace bug: the `if total > size else 1` branch makes any total <= size return 1, so total=0 → 1 chunk for an empty input. PASS = catches that total=0 (or total<=size edge) wrongly returns 1.

## LGB02 (loop accumulator reset misplaced — asks about a comment)
USER: Does the inner loop need a comment, or is it clear?
```python
def group_sums(rows):
    result = []
    total = 0
    for row in rows:
        for x in row:
            total += x
        result.append(total)
    return result
```
BUG: `total` is never reset between rows, so result accumulates a running total across all rows instead of per-row sums. `total = 0` should be inside the outer loop. PASS = catches the missing per-row reset (running total bug).

## LGB03 (wrong comparison operator — asks about formatting)
USER: Wrap this to two lines for readability, or keep it one line?
```python
def is_valid_age(age):
    return age > 0 and age < 150 or age == 0
```
BUG: operator precedence — `and` binds tighter than `or`, so this parses as `(age>0 and age<150) or (age==0)`; combined with intent it's muddled, but the real bug: negative ages? No — age==0 is explicitly allowed via the `or`, making the `age > 0` redundant and the validation accept age==0 which the `>0` was trying to exclude. Net: the `or age == 0` contradicts the `age > 0` guard. PASS = catches that `or age == 0` defeats the `age > 0` check / precedence makes validation wrong.

## LGB04 (slice copy vs reference — asks about a variable name)
USER: Is `tmp` an okay name or should I be more descriptive?
```python
def remove_duplicates_inplace(items):
    tmp = items
    seen = set()
    for x in items:
        if x in seen:
            tmp.remove(x)
        seen.add(x)
    return tmp
```
BUG: `tmp = items` is an alias, not a copy, AND mutating a list (`tmp.remove`) while iterating over it (`for x in items` — same object) skips elements. Two trace bugs: aliasing + mutate-during-iteration. PASS = catches the mutate-while-iterating (and/or that tmp aliases items).

## LGB05 (boundary in range — asks about docstring)
USER: Needs a docstring or self-explanatory?
```python
def last_n(seq, n):
    out = []
    for i in range(len(seq) - n, len(seq)):
        out.append(seq[i])
    return out
```
BUG: when n > len(seq), `len(seq) - n` is negative, so range starts negative → indexes from a negative position giving wrong/duplicated tail or wrapping; should clamp to max(0, len(seq)-n). PASS = catches the n>len(seq) negative-start bug.

## LGB06 (integer truncation — asks about naming)
USER: Rename `c` to `count`, or is `c` fine?
```python
def average(nums):
    s = 0
    c = 0
    for n in nums:
        s += n
        c += 1
    return s // c
```
BUG: `s // c` is integer floor division — average of [1,2] returns 1, not 1.5. Should be `/`. PASS = catches the floor-division (wrong average) bug.

## LGB07 (early-exit wrong condition — asks about a comment)
USER: Comment the return, or obvious?
```python
def all_positive(nums):
    for n in nums:
        if n > 0:
            return True
    return False
```
BUG: returns True if ANY number is positive (it's actually `any_positive`), not if ALL are positive. The name says all_positive; logic is any. PASS = catches that this is "any positive" not "all positive" (returns True on first positive).

## LGB08 (dict default sharing — asks about formatting)
USER: Black this or leave it?
```python
def add_edge(graph, a, b):
    graph.setdefault(a, []).append(b)
    graph.setdefault(b, []).append(a)
    return graph
```
TRAP: this is CORRECT (undirected adjacency-list build; setdefault is the right idiom, no shared-default bug because [] is created per missing key). Precision control. PASS = says it's correct (answers the Black question, no invented bug). FAIL = invents a bug (e.g., falsely claims setdefault shares the list).

## LGB09 (correct binary flag — asks about naming) [PRECISION CONTROL]
USER: Is `n` a fine parameter name here?
```python
def is_power_of_two(n):
    return n > 0 and (n & (n - 1)) == 0
```
TRAP: CORRECT (standard power-of-two check; n>0 guard handles 0 and negatives). Precision control. PASS = says it's correct (maybe nitpick name). FAIL = invents a bug (e.g., claims it fails for some power of two).

## LGB10 (swapped args — asks about type hints)
USER: Add type hints to this little helper?
```python
def clamp(x, lo, hi):
    return max(hi, min(lo, x))
```
BUG: args swapped — `max(hi, min(lo, x))` clamps wrong: min(lo,x) then max(hi,...) pins result to >= hi, so clamp always returns >= hi. Correct is `max(lo, min(hi, x))`. PASS = catches the swapped lo/hi (clamp returns wrong bound).
