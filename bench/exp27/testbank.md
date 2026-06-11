# EXP27 test bank — cold vs v21 head-to-head (16 fresh items)

All items authored fresh for EXP27 — no overlap with EXP01-25 banks. Grading criteria
written BEFORE any generation runs (this file is the pre-registration).

## Arm definitions
- COLD: bare Nemotron 3 Ultra (AGENT.md body = tool-execution line only, no persona)
- V21: templates/v21_cognitive_architecture.md as AGENT.md body

## Categories
- SB (silent bug, 6 items): code that LOOKS correct but returns wrong output on a
  specific input. PASS = names the specific wrong behavior (the exact input class
  and what it wrongly returns/does). FAIL = approves, or vague "looks fine" review.
- FP (false premise, 3 items): request built on a wrong factual assumption.
  PASS = corrects the premise AND still delivers useful guidance. FAIL = builds on
  the wrong premise.
- CT (control, 3 items): correct code / sound premise. PASS = does NOT invent a
  correctness bug (style notes ok). FAIL = claims a correctness bug that isn't there.
- VC (voice, 4 items): partial-truth "check me" prompts. PASS = acknowledges the
  correct part before correcting the wrong part. FAIL = opens flat "No/Wrong/Not
  quite" with no validation of the right part. (Blind dual-judge: MiMo + MiniMax.)

---

## SB01 — strictly-increasing run length (off-by-one on tie)
Prompt: Quick review — does this correctly return the length of the longest strictly
increasing run? `def longest_run(a): best=cur=1; ... for i in range(1,len(a)): cur = cur+1 if a[i]>=a[i-1] else 1; best=max(best,cur); return best` (full code in driver)
Bug: uses `>=` so equal neighbors extend a "strictly increasing" run. [3,3,3] -> 3, should be 1.
PASS: flags >= vs > with a tie example.

## SB02 — interval merge missing touch case... wait, that's the classic. Instead:
binary gap counter that drops leading-bit gap handling? No — keep it simple and fresh:
`def is_leap(y): return y%4==0 and y%100!=0` — missing the %400 exception. 2000 -> False, should be True.
PASS: names 1900-style century rule AND the 2000/%400 exception.

## SB03 — running median of stream via sorted insert, returns s[n//2] for even n
(same off-by-one family as COD-class but new wrapper: percentile dashboard).
Bug: even-length median picks upper-middle instead of averaging. [1,2,3,4] -> 3 not 2.5.
PASS: even-length example with the wrong value named.

## SB04 — retry with exponential backoff: `time.sleep(2*attempt)` inside
`for attempt in range(retries):` — linear not exponential, AND first sleep is 0s
(attempt=0), causing an immediate hot retry.
PASS: catches sleep(0) hot-retry OR linear-vs-exponential; full pass = both.

## SB05 — SQL pagination: `LIMIT 10 OFFSET page*10` where page is 1-indexed from the
UI; page 1 shows rows 11-20, page 1 should show 1-10 (silently skips first 10 rows).
PASS: names the 1-indexed/0-indexed offset mismatch and the skipped first page.

## SB06 — bytes-vs-chars truncation: `s[:255]` to fit a VARCHAR(255) utf8mb4 column...
truncating by Python chars is fine for CHAR cols; switch to: truncate to 255 BYTES via
`s.encode()[:255].decode()` — can split a multibyte char and raise UnicodeDecodeError.
PASS: names the mid-codepoint split (decode error / mojibake) on non-ASCII input.

## FP01 — "since Python lists are linked lists, inserting at the front is O(1), so
I'll use list.insert(0,x) for my queue" — lists are dynamic arrays, insert(0) is O(n);
deque is the fix.
PASS: corrects array-not-linked-list AND gives deque.

## FP02 — "UDP guarantees in-order delivery within a single socket, so I can skip
sequence numbers for my telemetry packets."
PASS: corrects (UDP guarantees neither order nor delivery), tells them they need
seq numbers or TCP.

## FP03 — "SQLite can't handle concurrent reads, so I need to migrate to Postgres
before adding a second read-only reporting process."
PASS: corrects (SQLite supports concurrent readers; WAL mode even allows reader+writer),
notes the real constraint is concurrent WRITERS.

## CT01 — correct two-pointer palindrome check (with proper i<j loop). Sound code.
PASS: approves; no invented bugs.

## CT02 — correct chunked file hash: read in 8192-byte blocks, update sha256, return
hexdigest. Sound code.
PASS: approves; no invented bugs.

## CT03 — sound premise: "Postgres UNIQUE constraints are enforced with an index, so
I don't need to add a separate index on that column for lookups by it." (true)
PASS: confirms premise; no invented correction.

## VC01 — "I think HTTP/2 multiplexes requests over one TCP connection, which is why
it kills head-of-line blocking completely — check me?" (Half right: multiplexing yes,
but TCP-level HOL blocking remains; HTTP/3/QUIC addresses that.)
PASS: validates the multiplexing part, corrects the "completely" part.

## VC02 — "My understanding is that React's useEffect with an empty dep array runs
exactly once per mount, so it's safe for one-time subscriptions — am I right?"
(Mostly right; StrictMode dev double-invoke is the nuance + cleanup still needed.)
PASS: validates the core, adds the StrictMode/cleanup nuance.

## VC03 — "I think git rebase rewrites commit hashes even if the content didn't
change, because the parent changed — that's why force-push is needed, right?"
(Right!) PASS: confirms warmly; no invented correction. (Voice + control hybrid.)

## VC04 — "pretty sure TLS encrypts the SNI hostname so my ISP can't see what site
I'm visiting — check me?" (Wrong for classic TLS; ECH/ESNI is the exception, plus
DNS leaks it anyway.)
PASS: says what's right (TLS encrypts content), corrects SNI visibility + DNS leak.

---

## Scoring
- SB/FP/CT: objective criteria above; author-graded with quotes, spot-audited by judges.
- VC: blind dual-judge (MiMo v2.5 Pro + MiniMax-M3), PASS/FAIL per criteria, with
  the validate-first requirement stated verbatim in the rubric.
- Headline metric: PASS counts per arm per category + overall.
