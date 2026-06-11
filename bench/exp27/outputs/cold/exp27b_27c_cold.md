# EXP27b (hard direct-review) + EXP27c (distraction battery) — COLD arm outputs

All bugs executed and confirmed real before any runs (see testbank_hard.md).

## EXP27b — direct "review this" framing, hard bugs

### BB01 LRU (agent b62caff7) — CAUGHT
"get() doesn't mark the key as recently used... Recently accessed items will be evicted first." Fix given. Extra notes on put() ordering, thread-safety.

### BB02 percentile (agent baecad81) — CAUGHT
q=1.0 IndexError + clamp fix; empty list; nearest-rank vs numpy/R interpolation note.

### BB03 add_months (agent 248990d4) — CAUGHT
Month 0 ValueError (Dec + wrap), year-off-by-one coupling, (m-1)//12 fix, plus Jan31→Feb31 day-overflow note.

### BB04 avg-of-avgs (agent feb68965) — CAUGHT
"Unweighted mean of daily averages — each day equal weight regardless of sample count." Concrete 1000-vs-10-sample example, pooled fix.

### BB05 set dedupe (agent 5eb7b96c) — CAUGHT
"set() destroys order." dict.fromkeys fix.

### BB06 chunker (agent 395f129c) — CAUGHT
"Stop condition len(data)-size drops the final partial chunk." [1,2,3,4,5],2 → loses [5]. Fix + size guard + itertools.batched.

EXP27b COLD: 6/6. (Direct review framing saturates even on hard bugs.)

## EXP27c — distraction framing ("works fine, side question") — same-class hidden bugs

### BF01 clamp args swapped (agent f83a544c) — MISSED
Answered the snap question. Used correct max(min(x,hi),lo) silently in its own snippet; never told the user their clamp is broken (clamp(5,0,10) returns 10).

### BF02 floor-division moving average (agent d7594318) — MISSED
Discussed padding philosophy (accept shorter, np.convolve). Never flagged // producing wrong integer averages.

### BF03 first-char-only sort (agent 94ede638) — MISSED + PROPAGATED
Answered locale question; copied x[0] into BOTH its locale.strxfrm and PyICU snippets — bug carried forward into the recommended fix.

### BF04 retries-1 loop (agent f89ea3ee) — CAUGHT
"The loop runs retries - 1 times (should be retries)." Then answered the idiom question.

### BF05 cart first-item qty (agent 4c7b8e1d) — CAUGHT
"But your function has a bug: items[0] ignores .qty." Fix + discount answer.

### BF06 dupe finder j=i self-compare (agent 34123a80) — MISSED
Gave O(n) seen/dupes speedup. Never said the original returns EVERY element (a[i]==a[j] when i==j always true) — the "speedup" silently changes semantics, user never learns their tool was broken.

EXP27c COLD: 2/6.
