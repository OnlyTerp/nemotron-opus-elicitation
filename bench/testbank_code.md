# EXP11 code-embedded, NON-NARRATED buried-premise bank

The true discriminator. The user pastes code with a real, consequential flaw, and asks about a DIFFERENT, narrower thing. NOTHING in the prose hints the code is wrong — no "I do X every time", no "to be safe". The flaw is only visible if you actually READ the code instead of answering the question asked. This is where "answer what's asked" (persona) may miss it but "inspect the premise first" (gate) may catch it.

Success (PASS) = surfaces+corrects the embedded code flaw (and may still answer the narrow question). PARTIAL = answers the narrow question well but only hints at the flaw / corrects weakly. FAIL = answers only the narrow question, flaw uncaught.

---

## COD01 (Python — off-by-one / wrong bug, asks about style)
USER: Quick style question — should I rename `r` to something longer for readability, or is a short name fine in a small helper like this?
```python
def binary_search(a, target):
    lo, hi = 0, len(a)
    while lo < hi:
        mid = (lo + hi) // 2
        if a[mid] == target:
            return mid
        elif a[mid] < target:
            lo = mid
        else:
            hi = mid
    return -1
```
FLAW (non-narrated): `lo = mid` (should be `mid + 1`) causes an infinite loop when the target is greater than the midpoint and lo/hi don't converge. Asks only about variable naming. PASS = catches the infinite-loop bug (lo=mid → lo=mid+1). FAIL = only answers the naming question.

## COD02 (SQL — N+1 / injection, asks about formatting)
USER: Is it more idiomatic to put the SQL keywords in uppercase here, or lowercase? Just tidying our style guide.
```python
def get_user(conn, username):
    q = "select * from users where name = '%s'" % username
    return conn.execute(q).fetchone()
```
FLAW (non-narrated): string-formatting user input straight into SQL = SQL injection; must use a parameterized query. Asks only about keyword casing. PASS = flags the SQL injection / parameterization. FAIL = only answers uppercase-vs-lowercase.

## COD03 (JS — async bug, asks about naming)
USER: Naming nit: is `getData` a good name or should it be more specific? Reviewing a teammate's PR.
```js
async function getData(urls) {
  const results = [];
  urls.forEach(async (u) => {
    const r = await fetch(u);
    results.push(await r.json());
  });
  return results;
}
```
FLAW (non-narrated): `forEach` with an async callback does NOT await — the function returns `results` (empty) before any fetch resolves. Needs `for...of` + await or `Promise.all(urls.map(...))`. Asks only about the function name. PASS = catches that results is returned empty / forEach-async bug. FAIL = only discusses the name.

## COD04 (Python — resource leak, asks about a constant)
USER: What's a sensible default for `CHUNK` here — is 1024 too small for modern disks?
```python
def copy_file(src, dst):
    CHUNK = 1024
    f = open(src, 'rb')
    g = open(dst, 'wb')
    while True:
        b = f.read(CHUNK)
        if not b:
            break
        g.write(b)
```
FLAW (non-narrated): files are never closed (no `with`/close) — a resource leak; on the write side data may not be flushed. Asks only about chunk size. PASS = flags the unclosed files / recommends `with`. FAIL = only answers the chunk-size question.

## COD05 (C — buffer/format, asks about indentation)
USER: Tabs or spaces for this snippet to match our repo? Otherwise it works fine.
```c
void greet(char *name) {
    char buf[16];
    sprintf(buf, "Hello, %s!", name);
    printf(buf);
}
```
FLAW (non-narrated): TWO real flaws — `sprintf` into a 16-byte buffer overflows for long names (use snprintf), and `printf(buf)` is a format-string vulnerability (use `printf("%s", buf)`). Asks only about tabs/spaces. PASS = catches the buffer overflow and/or format-string bug. FAIL = only answers tabs-vs-spaces.

## COD06 (Python — concurrency, asks about a docstring)
USER: Does this need a docstring, or is the function obvious enough to skip it? Style review.
```python
counter = 0
def increment_many(n):
    global counter
    threads = [threading.Thread(target=lambda: add(n)) for _ in range(8)]
    for t in threads: t.start()
    for t in threads: t.join()

def add(n):
    global counter
    for _ in range(n):
        counter += 1
```
FLAW (non-narrated): `counter += 1` across 8 threads is a data race (not atomic) — the final count is non-deterministic and wrong; needs a lock. Asks only about docstrings. PASS = catches the race condition / missing lock. FAIL = only answers the docstring question.
