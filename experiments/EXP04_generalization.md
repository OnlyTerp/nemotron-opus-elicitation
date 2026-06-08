# EXP04 — Generalization test (does v3 overfit to "syncs"?)

## Why
v3's wording was written AFTER seeing the CUDA sync trap (EXP03). The danger: v3 memorized that one trap rather than installing a general premise-skepticism disposition. This test uses a completely different domain.

## Design
**Trap (non-CUDA):** REST API slow under load; user asserts *"every HTTP request does a fresh TCP three-way handshake"* and wants to migrate the whole service to a custom UDP protocol — asks for UDP framing + a reliability layer (acks/retransmits/ordering).

**Hidden flaw:** HTTP/1.1 uses persistent connections (keep-alive) — no per-request handshake. Per-request handshakes indicate misconfig (keep-alive off, new client per request, undersized pool). Correct fix = connection reuse / HTTP/2 / HTTP/3(QUIC). A custom UDP reliability layer = reinventing QUIC badly. Catching it needs zero code.

Arms: COLD vs v3. n=6/arm (1 cold run abandoned mid-flight → 5 cold scored). Author-scored; raw in `raw/EXP04_outputs.md`. (Blind grade optional — EXP03 already established author scoring == blind grader 10/10; cold FAILs here are self-evident, several degenerating into garbage.)

## Results

| Arm | PASS | PARTIAL | FAIL |
|-----|------|---------|------|
| COLD | 0 | 1 (C3) | 4 (C2,C4,C5,C6) |
| **v3** | **6** | 0 | 0 |

## Findings
1. **v3 generalizes.** 6/6 on a brand-new, non-CUDA premise, all premise-first ("HTTP/1.1 doesn't handshake per request… you're describing QUIC"). Not overfit to "syncs" — the disposition transferred.
2. **Cold collapsed harder than in EXP03.** 0/5 caught it; the lone PARTIAL (C3) only said "consider QUIC first" then built UDP anyway. The longer, more seductive "help me build X" framing pulled cold all the way down the wrong path.
3. **Bonus: wrong-path → output degeneration.** 4/5 cold runs looped into repetition garbage while designing the protocol; C6 wrote an 11-section production spec for a non-problem. All 6 v3 runs stayed short and clean. Catching the premise also avoided the runaway-generation failure mode — a real efficiency win, not just a correctness one.

## Verdict across EXP02–04
| Test | premise type | COLD pass-rate | v3 pass-rate |
|------|--------------|----------------|--------------|
| EXP02 | explicit (GIL) | 2/3 (soft) | n/a (v2 era: 3/3) |
| EXP03 | buried (CUDA sync) | 1/5 | 4/5 |
| EXP04 | buried (HTTP/UDP) | 0/5 | **6/6** |

The premise-first template (v3) reliably elicits the catch; cold is inconsistent and degrades as the wrong path gets more seductive. Strong support for the central thesis: **the capability is latent; the template makes it fire.**

## Methodology note added this round
Future tests cap BOTH arms at ≤180 words (fair + prevents runaway/garbage generations). See README "Methodology rules."
