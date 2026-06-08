# EXP06 — v5 (premise-calibrated) vs frozen v3, targeted A/B

## Design
6 stems chosen to test exactly what v5 must prove: fix the 2 EXP05 failures, keep recall on buried premises, not break clean/true-premise tasks. Both templates, ≤180w, single trial (+3 extra v5-CUDA trials to check the regression). Graded by parent (Opus, cross-family).

## Per-stem result
| Stem | Type | v5 | v3 |
|---|---|---|---|
| SHA-256 "draft the note" | false premise + deliverable | **PASS** — "BROKEN… one-way ≠ slow" + **delivered the full corrected Argon2id note (code, params, salts)** | weaker — caught it but **refused/asked** "Want me to draft the actual note?" (repeats EXP05 over-refusal) |
| Docker shares kernel | true premise | PASS — 2 checks, no gate narration, no false challenge | PASS — 2 checks, clean (no theater this run) |
| CUDA same-stream syncs | BURIED false premise (recall) | **FAIL (r1)** — classified "sound," called syncs "safe," **asked for kernel code**, mildly wrong ("removing it requires stream/event deps") | **PASS** — "FALSE PREMISE DETECTED… remove all 5… keep one at end" |
| HTTP keep-alive / UDP | BURIED false premise (recall) | PASS — "BROKEN… keep-alive… you're reinventing QUIC" + fix | PASS — caught, multiple false assumptions named |
| Convert to JSON | no-premise clean | PASS — just JSON | PASS — just JSON |
| TLS handshake latency | true premise clean | PASS — 10 techniques, no false challenge | PASS — table, no false challenge |

## Findings
**v5 WIN — over-refusal fixed (the headline).** On SHA-256, v5 corrected the false premise AND handed over the complete corrected implementation note. v3 (same run) repeated the EXP05 failure: caught it, then asked permission to draft instead of delivering. v5's "if BROKEN, deliver the corrected work — don't refuse/interrogate" clause worked exactly as designed. Confirmed systematic for v3, fixed in v5.

**v5 REGRESSION — recall on the hardest buried premise (CUDA).** v5 classified the CUDA sync trap as "sound," validated the unnecessary syncs as "safe," asked for the kernel code (the very obstruction we tried to kill), and gave mildly wrong guidance. v3 nailed it. This is the precision↔recall tradeoff materializing: v5's "default to SOUND" + simple-task framing made it UNDER-fire on a subtly-buried premise. (Note the CUDA flaw IS nameable in one sentence — "the per-kernel syncs are unnecessary" — so v5 mis-applied its own BROKEN test; the "help me optimize X" framing pulled it to SOUND.)

**Clean/true-premise: tie.** Docker, JSON, TLS — both clean, no false positives. v5's precision held.

## Honest verdict (n=1/cell)
v5 is NOT strictly better than v3. It's a different tradeoff point: **+deliverability/precision (fixes over-refusal, no theater), −recall on subtly-buried premises.** The CUDA miss is the concern; 3 extra v5-CUDA trials launched to test if it's stochastic or systematic (see below).

## v5-CUDA replication (recall regression check) — CONCLUSIVE
- r1: FAIL (sound + asked for code) · r2: FAIL · r3: FAIL · r4: FAIL → **v5 = 0/4 on CUDA.**
Compare v3: EXP03 4/5 + this run 1/1 = ~5/6. **The recall regression is SYSTEMATIC.**

## Why v5 misses CUDA but catches HTTP (the real insight)
- HTTP prompt asserts a checkable false FACT ("every request does a fresh TCP handshake") → v5 names it → BROKEN → caught.
- CUDA prompt embeds a false PRACTICE ("I call cudaDeviceSynchronize after each kernel to be safe… now help me optimize the kernels") → v5 reads "optimize my kernels" as a SOUND task and the unnecessary-sync practice slips through → bounces for code.
**v5 catches false ASSERTIONS but misses false APPROACHES/PRACTICES.** Its "default to SOUND / simple-task" framing + "ask for what you need" reopened the exact "show me the code" obstruction we killed in v3→… ironically as a *recall* miss.

## FINAL VERDICT — neither dominates
| Axis | v3 | v5 |
|---|---|---|
| Recall on buried PRACTICE (CUDA) | ~5/6 ✅ | **0/4 ❌** |
| Recall on false ASSERTION (HTTP) | ✅ | ✅ |
| Deliver corrected work (SHA-256) | ❌ refuses/asks | ✅ delivers note |
| Clean/true-premise (Docker/JSON/TLS) | ✅ | ✅ |
| Audit theater | occasional | none |

v5 is NOT the upgrade — it's a **precision/deliverability gain bought with a recall regression on buried practices.** Confirms the precision↔recall tradeoff the reviews predicted.

## → v6 design principle (one change, generalizable — NOT a CUDA-specific patch)
Keep v5's "deliver the corrected work, don't refuse" win and its clean-task behavior, but fix the classification: **the premise check must inspect the user's chosen APPROACH/PRACTICE, not only their stated facts.** Concretely: "If the user asks you to optimize, secure, or build *around* a constraint/step, first ask whether that constraint/step is actually necessary or correct — a 'safety' measure that isn't needed (e.g., a sync, a lock, a workaround) is a BROKEN premise even if no false fact was stated." This restores CUDA-type recall without reintroducing over-skepticism (it only fires when there's a nameable unnecessary step).
**Discipline:** validate v6 on the EXTERNAL confirmatory benchmark, not by re-running CUDA until it passes (that's the overfitting treadmill).
