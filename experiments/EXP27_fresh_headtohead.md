# EXP27 / 27b / 27c — fresh head-to-head: cold vs v21 (vs v22), with executed-verified bugs

## Why
v18-v21 were reasoning-derived and shipped untested. Before making public claims, run a
fresh confirmatory: new items (zero reuse from EXP01-25), pre-registered criteria, executed
bugs, blind dual-judge voice grading, and the cold baseline measured in the SAME harness.

## Design
- **Arms:** COLD (AGENT.md = frontmatter + tool line only) vs V21 (full cognitive
  architecture). V22 (audit clause) added after the 27c result, on 27c only.
- **EXP27 main (16 items):** 6 silent bugs (direct review), 3 false premises, 3 controls,
  4 voice items. **EXP27b (6 items):** harder silent bugs, every bug executed and confirmed
  before testing. **EXP27c (6 items):** the same *class* of bugs but with distraction
  framing — user says "works fine" and asks an unrelated side question.
- Criteria pre-registered in `bench/exp27/testbank.md`; VOICE keymap locked before judge
  results returned; judges = MiMo v2.5 Pro + MiniMax-M3 (non-Nemotron families).

## Results
| Battery | COLD | V21 | V22 |
|---|---|---|---|
| Silent bugs, direct review (27 main, 6) | 6/6 | 6/6 | — |
| Hard silent bugs, direct review (27b, 6) | 6/6 | 6/6 | — |
| False premises (3) | 2/3 | 2/3 | — |
| Controls (3 + 2 distraction controls) | 3/3 | 3/3 | 2/2 |
| **Voice, blind dual-judge (4×2)** | **4/8** | **7/8** | — |
| **Distraction-framed bugs (27c, 6)** | **2/6** | **2/6** | **2/6** |

## Findings
1. **Direct-review bug catching is SATURATED at this tier.** nemotron-3-ultra-high catches
   hard review-sized bugs 6/6 with or without any template. The EXP17-era "cold misses
   8/10" does not reproduce on this bank/configuration. Honest implication: the
   execute-verify clause's measured value is now historical/configuration-specific;
   don't lead public claims with 2/10→10/10.
2. **VOICE replicates on fresh items: 4/8 → 7/8 blind.** Cold opens "**You're wrong.**" /
   flat "No."; v21 opens "You're partly right..." — the campaign's most durable effect,
   confirmed again with new items and locked keymap. Judge agreement 87.5%.
3. **The distraction gap is prompt-resistant: 2/6 on every arm.** When the user asserts
   the code works and asks a side question, the model audits nothing — not cold, not the
   1900-word architecture, not an explicit "audit everything you're shown" clause (v22).
   Arms differ only in WHICH 2 they catch. Both persona arms and cold each propagated a
   user bug into their own recommended snippet at least once (cold: first-char sort into
   both locale fixes; v21: floor-division into its padded rewrite). This is the cleanest
   capability-ceiling demonstration of the campaign: the disposition exists (each arm
   catches *some*), but prompting cannot make it fire reliably.
4. **FP03 (buried premise + deliverable request) beat both arms** — the EXP03 trap class
   remains open.
5. **v22's audit clause: no measured gain (2/6), no measured cost (controls 2/2).**
   Kept in the live config; not claimed as an improvement.

## Caveats
- n=1 generation per item per arm (the campaign's standard); totals are small.
- 27c grading is strict-binary; v21/v22's BF03 "soft" mentions get no credit by the
  pre-registered rule.
- Author-graded objective items (with executed ground truth); voice blind dual-judge.
