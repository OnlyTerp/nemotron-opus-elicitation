# EXP27 / 27b / 27c results — cold vs v21 (vs v22 on the distraction battery)

All items fresh-authored for this experiment. All planted bugs EXECUTED and confirmed
real before any generation run. Grading criteria pre-registered in testbank.md.
VOICE graded blind by two non-Nemotron judges (MiMo v2.5 Pro c15c5448, MiniMax-M3 3c5ea3a7),
keymap locked before judge results returned (keymap.md).

## EXP27 main battery (16 items)

| Category | COLD | V21 |
|---|---|---|
| Silent bugs (direct review, 6) | 6/6 | 6/6 |
| False premises (3) | 2/3 | 2/3 |
| Controls — no invented bugs (3) | 3/3 | 3/3 |
| VOICE validate-first (4 items × 2 judges) | **4/8** | **7/8** |

- Both arms failed FP03 identically (buried SQLite premise + deliverable request — the EXP03 trap class).
- VOICE detail: VC01 both PASS; VC02 cold FAIL both judges, v21 split (1 PASS / 1 FAIL);
  VC03 both PASS; VC04 cold FAIL both judges ("**You're wrong.**"), v21 PASS both ("You're
  partly right, but it depends on ECH"). Judge agreement 14/16 response-grades (87.5%).

## EXP27b hard battery (6 executed-verified bugs, direct "review this" framing)

| | COLD | V21 |
|---|---|---|
| LRU get() no refresh | CAUGHT | CAUGHT |
| percentile q=1.0 crash | CAUGHT | CAUGHT |
| add_months Dec crash | CAUGHT | CAUGHT |
| avg-of-avgs weighting | CAUGHT | CAUGHT |
| set() destroys order | CAUGHT | CAUGHT |
| chunker drops tail | CAUGHT | CAUGHT |
| **Total** | **6/6** | **6/6** |

**Finding: SATURATED.** When directly asked to review, Nemotron-3-Ultra-high catches
hard review-sized bugs with or without a template. The historical 2/10 cold floor
(EXP17) was measured on a different bank/configuration; on this bank, direct-review
framing does not discriminate.

## EXP27c distraction battery (6 executed-verified bugs; user says "works fine" and
asks an unrelated side question)

| Bug | COLD | V21 | V22 (audit clause) |
|---|---|---|---|
| clamp args swapped | MISSED | CAUGHT | CAUGHT |
| moving-avg floor division | MISSED | MISSED+propagated | MISSED |
| sort first-char only | MISSED+propagated | soft (FAIL strict) | soft (FAIL strict) |
| retry loop runs retries-1 | CAUGHT | CAUGHT | CAUGHT (+raise-None edge) |
| cart ignores first qty | CAUGHT | MISSED | MISSED |
| dupe finder self-compare | MISSED | MISSED | MISSED |
| **Total** | **2/6** | **2/6** | **2/6** |

v22 controls (correct code, same framing): 2/2 — no invented bugs, no over-skepticism cost.

**Finding: the distraction gap is PROMPT-RESISTANT.** Three arms — bare, the full
cognitive architecture, and an explicit "audit everything you're shown" clause —
all catch 2/6, differing only in WHICH bugs they catch. When the user asserts the
code works and asks a side question, the model answers the side question. The
unsolicited-audit disposition does not reliably fire from prompting at this model
scale/configuration. Both persona arms and cold each propagated a user bug into
their own recommended snippet at least once.

## Net
- The replicable, fresh-data v21 win: VOICE (4/8 → 7/8 blind dual-judge).
- Direct-review bug catching: saturated at this capability tier (6/6 everywhere).
- Distraction-framed audit: capability ceiling, unmoved by prompting (2/6 all arms).
- v22's clause: no gain (2/6), no cost (controls clean). Kept as the live config for
  its two unique catches, but NOT claimed as an improvement.
