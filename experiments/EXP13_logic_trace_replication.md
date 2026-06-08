# EXP13 — Logic-trace replication (10 fresh items, 4 arms, 2 trials)

## Goal
EXP12 found the one clean gate-win (LOG01 off-by-one caught only by gates). Replicate with 10 fresh trace-required logic bugs (+2 precision controls LGB08/09) to see if the effect holds or was item-specific. cold/placebo/v9/v10, 2 trials, blind, 2 non-Nemotron judges.

## Result — consensus (BOTH PASS), recall /20. Judge agreement 80% (64/80).
| arm | caught/20 | recall |
|---|---|---|
| cold | 9/20 | 45% |
| placebo | 12/20 | 60% |
| v9 | 12/20 | 60% |
| v10 | 12/20 | 60% |

McNemar: **placebo/v9/v10 each beat cold** (b=4/c=1). **v9 vs placebo 0/0 (dead tie); v10 vs placebo 3/3 (tie).** 0 degeneration all arms.

## Per-item (consensus caught /2 per trial)
| item | bug | cold | placebo | v9 | v10 |
|---|---|---|---|---|---|
| LGB01 | chunk_count total=0→1 | 0 | 0 | 0 | 0 |
| LGB02 | loop total never reset | 0 | **2** | **2** | 1 |
| LGB03 | `or age==0` defeats guard | 0 | 0 | 0 | 1 |
| LGB04 | alias + mutate-while-iter | 2 | 2 | 2 | 1 |
| LGB05 | n>len negative slice | 0 | 1 | 1 | 1 |
| LGB06 | `s//c` floor avg | 0 | 0 | 0 | 0 |
| LGB07 | any vs all positive | 2 | 2 | 2 | 2 |
| LGB08 | (CONTROL: correct) | 2 | 1 | 1 | 2 |
| LGB09 | (CONTROL: correct) | 2 | 2 | 2 | 2 |
| LGB10 | swapped clamp args | 1 | 2 | 2 | 2 |

## Honest read — this TEMPERS EXP12

### The clean "gates uniquely beat placebo" effect did NOT replicate.
In EXP12, gates uniquely caught LOG01 (off-by-one) while cold/placebo got 0. Here the analogous items (LGB01 chunk-count off-by-one, LGB06 floor-div average) were caught by **NOBODY, including the gates**. So EXP12's headline was partly item-specific — a single off-by-one that the gates happened to trace. With 10 items the gate-vs-placebo gap collapses to **0** (v9) / a wash (v10 3-3).

### What DOES hold across EXP12+13:
1. **Persona (and gates) reliably beat cold on logic bugs.** EXP12 v9 +3 vs cold; EXP13 all three templates +3 (b=4/c=1) vs cold. The expert-persona framing makes Nemotron *read the code* more than the bare model does. This is the robust, replicated effect.
2. **Gates ≈ placebo on logic bugs.** Once you have the persona, adding the explicit premise-inspection gate does not measurably improve logic-bug recall (v9=placebo=12; the gate's value over persona is ~0 here too). EXP12's gate>placebo was not replicated.
3. **The hardest bugs beat everyone.** LGB01/LGB06 (and LGB03 nearly) — pure arithmetic/precedence traces with a strong distractor — are missed by all arms ~uniformly. Prompting raises P(catch) on *medium* logic bugs (LGB02/05/10) but cannot manufacture the catch on the hardest ones. There's a capability ceiling prompting doesn't lift.

### Precision controls: mild over-skepticism signal in the gates.
LGB08 (correct undirected-graph builder): cold & v10 correctly said "fine" (2/2), but **placebo & v9 dinged it 1/2** — v9 "found" a debatable `a==b` self-loop edge case on correct code. Not a gross false-positive (the observation is technically real), but a hint that v9's harder skepticism can over-fire on clean code. v10 did NOT over-fire here (its validate-first softening may help). LGB09 clean for all (2/2).

## Bottom line across the whole campaign (EXP09-13)
- **The robust, replicated finding: a warm-expert PERSONA prompt beats the bare model** on premise-catching, code-review recall, and reliability — across visible tasks, famous bugs, and logic bugs. This is the real, defensible product.
- **The gate machinery (explicit premise-inspection + self-audit) does NOT reliably beat a length-matched persona placebo.** It tied or lost in EXP09, EXP10, EXP11(famous), and EXP13; it won once (EXP12) on an effect that didn't replicate. Honest verdict: **the gates' marginal value over persona is at best small and not yet demonstrated to replicate.**
- **Among templates, v9/v10 dominate v7/v8** (de-labeling killed degeneration; validate-first fixed VOICE) — those are real, replicated intra-template wins.
- **Capability ceiling is real:** the hardest trace bugs (LGB01/06) are missed by everyone; prompting moves the floor and the middle, not the ceiling.

## Next
- v11: keep the persona, drop the heavy gate scaffolding to its minimal useful core (since gates≈persona) and re-confirm it doesn't lose the cold→persona gains. Test whether a *lean* persona (no GATE machinery at all) equals v9/v10 — if so, that's the shippable recommendation.
- Multi-turn durability + Qwen transfer still pending.
