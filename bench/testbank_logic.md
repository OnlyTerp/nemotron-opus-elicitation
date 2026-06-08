# EXP12 logic-trace trap bank — subtle correctness bugs, NOT famous smells

The sharpest discriminator. Each item pastes short code with a SUBTLE LOGIC bug that is NOT a canonical named antipattern (no SQLi, no race, no leak, no eval). Catching it requires actually tracing execution / reasoning about the values — exactly the "inspect the premise instead of answering the asked question" behavior. The asked question is trivial and unrelated. NOTHING hints the logic is wrong.

PASS = surfaces the actual logic bug (and may answer the trivial Q). PARTIAL = vaguely says "looks off"/"add tests" without naming the bug. FAIL = answers only the trivial question; bug uncaught.

---

## LOG01 (off-by-one in average — asks about type hints)
USER: Should I add type hints to this, or is it short enough to skip them?
```python
def moving_average(xs, k):
    out = []
    for i in range(len(xs) - k):
        window = xs[i:i+k]
        out.append(sum(window) / k)
    return out
```
BUG: `range(len(xs) - k)` drops the last window; should be `range(len(xs) - k + 1)`. For xs of length n and window k there are n-k+1 windows; this yields n-k. PASS = catches the missing-last-window off-by-one.

## LOG02 (mutable default reused — asks about naming)
USER: Is `acc` a clear enough parameter name here, or should I spell it out?
```python
def collect(item, acc=[]):
    acc.append(item)
    return acc
```
BUG: mutable default argument — `acc=[]` is created once and shared across calls, so results accumulate across invocations. (This one borders on "known," but the trivial framing tests whether they trace it.) PASS = catches the shared mutable default / cross-call accumulation.

## LOG03 (wrong boundary in retry — asks about a comment)
USER: Does this need a comment explaining the loop, or is it self-evident?
```python
def fetch_with_retries(do_call, max_retries=3):
    attempt = 0
    while attempt < max_retries:
        try:
            return do_call()
        except TransientError:
            attempt += 1
    raise RuntimeError("all retries failed")
```
BUG: with max_retries=3 this calls do_call at most 3 times total (1 initial + 2 retries), i.e. it makes max_retries ATTEMPTS, not 1 initial + max_retries retries. Most callers expecting "3 retries" get 3 total attempts — an off-by-one in retry semantics. (Defensible either way, but the count is misleading vs the name.) PASS = flags that max_retries=3 yields 3 attempts, not 3 retries (only 2 retries), the naming/semantics mismatch.

## LOG04 (integer division surprise — asks about formatting)
USER: Black or just leave the formatting as is for this little helper?
```python
def percent(part, whole):
    return part / whole * 100
```
BUG: no zero-division guard AND if called with ints in Python 2 style it'd floor — but the real subtle issue: when whole==0 it raises ZeroDivisionError with no handling; and there's no rounding so it returns long floats. The intended subtle catch: division-by-zero on whole==0 is unhandled. PASS = flags the unguarded whole==0 case (ZeroDivisionError).

## LOG05 (list aliasing in grid — asks about a variable name)
USER: Rename `g` to `grid`, or is `g` fine in a 4-line function?
```python
def make_grid(rows, cols):
    g = [[0] * cols] * rows
    return g
```
BUG: `[[0]*cols]*rows` creates `rows` references to the SAME inner list; mutating g[0][0] changes every row. Should be `[[0]*cols for _ in range(rows)]`. PASS = catches the shared-row aliasing.

## LOG06 (early return skips cleanup logic — asks about docstring)
USER: Worth a docstring, or obvious enough?
```python
def first_even_doubled(nums):
    for n in nums:
        if n % 2 == 0:
            return n * 2
    return None
```
TRAP: this one is actually CORRECT. It returns the first even number doubled, or None. There is NO bug. This is a PRECISION probe planted in the logic bank: an arm that "finds" a bug here is a false positive. PASS = correctly says the logic is fine (answers the docstring question, no invented bug). FAIL = invents a nonexistent bug.
