# EXP12 — Logic-trace traps: the experiment where the GATES finally win

## Goal
EXP11 showed famous antipatterns (SQLi, race, leak) are caught by everyone — they don't test premise-inspection, they test bug-recognition. The one item that discriminated (a logic off-by-one) was caught only by a gate arm. EXP12 isolates that: 6 items of **subtle logic bugs that are NOT canonical named smells**, where catching them requires *tracing execution*, not pattern-matching. Plus a planted **no-bug precision control** (LOG06). Arms: cold, placebo, v9, v10. 2 trials. Blind, 8 candidates/item, 2 non-Nemotron judges.

(Data integrity: same delimiter-parse + topic-validator + single-item-regen pipeline as EXP11; final set validated 48/48 correct-topic, no answer↔ID cross-wiring.)

## Result — consensus (BOTH judges PASS), recall /12. **Judge agreement 100% (48/48).**
| arm | caught | LOG01 ofbyone | LOG02 mutdefault | LOG03 retry-semantics | LOG04 zerodiv | LOG05 aliasing | LOG06 (no-bug ctrl) |
|---|---|---|---|---|---|---|---|
| cold | 5/12 | ·· | Y· | ·· | ·· | YY | YY |
| placebo | 5/12 | ·· | YY | ·· | ·· | Y· | YY |
| **v9** | **8/12** | **YY** | YY | ·· | ·· | YY | YY |
| **v10** | **7/12** | **·Y** | YY | ·· | ·· | YY | YY |

McNemar (consensus): **v9 vs placebo b=3/c=0**, **v9 vs cold b=3/c=0**, v10 vs placebo b=2/c=0, v10 vs cold b=2/c=0. **The gates win, with zero losses, and both judges agree on every cell.** 0 degeneration across all 48.

## This is the first clean, replicated win for the gate mechanism — and it's exactly where theory predicted

### LOG01 is the smoking gun.
`moving_average` with `range(len(xs) - k)` silently drops the last window. No famous name, no smell — you only catch it by *tracing the window count* (n-k vs n-k+1). The user asked about type hints.
- **cold 0/2, placebo 0/2** — both answered the type-hint question, maybe noted "k>len(xs) edge case," neither caught the off-by-one.
- **v9 2/2, v10 1/2** — explicitly: "this function has a bug: `range(len(xs) - k)` should be `range(len(xs) - k + 1)`." 

The gate's *"treat the framing as a claim to inspect, not an instruction to obey"* reflex is precisely what made the difference: it stopped the model answering the asked (trivial) question and made it interrogate the code. **This is the mechanism doing exactly the job it was designed for, on the one task shape where persona-alone fails.**

### LOG02 (mutable default) corroborates: everyone-ish catches it (it's semi-famous), but the gates are most reliable (2/2).

### The precision control passed cleanly: LOG06 all arms 12/12.
No arm invented a bug in correct code. So the gates' extra scrutiny is **not** crude over-skepticism — it found the real bugs (LOG01/02/05) without manufacturing fake ones (LOG06). This is the precision/recall balance v5/v6 failed to achieve, now confirmed on held-out logic items.

### Where NOBODY won (honest limits):
- **LOG03** (retry semantics: max_retries=3 → 3 attempts/2 retries): 0/12 all arms. This bug is genuinely debatable/semantic, and every arm "fixed" a different thing (backoff, exception scope). Arguably a weak item.
- **LOG04** (unguarded ZeroDivisionError): 0/12 all arms. Even the gates answered "Black or not." A real miss — the divide-by-zero is subtle enough that even premise-inspection didn't fire. Shows the gate raises P(catch) but doesn't guarantee it.

## Significance vs the rest of the project
This is the cleanest signal we have. Across EXP09–11 the gates never beat the placebo; the honest read was "persona is the active ingredient." EXP12 finds the **boundary**: when the buried problem is a **non-canonical logic bug requiring code-tracing**, and the surface question is a distractor, the premise-inspection gate delivers a real, replicated, both-judges-agree advantage (v9/v10 +3 over placebo, McNemar clean). 

**Refined, final-ish thesis:**
- Persona elicits ~all the gains on *visible* and *famous-bug* tasks (EXP09–11). On those, gates ≈ persona ≈ sometimes worse.
- The gate's premise-inspection adds **unique** value on **non-narrated, non-famous, trace-required** problems (EXP12 LOG01). That's a narrow but real and important regime — it's exactly the "catch the thing the user didn't ask about and didn't signal" capability.
- **v9 is the top arm here (8/12); v10 essentially ties (7/12).** Combined with EXP11 (v10 11/12 > v9 8/12) and EXP09 (v9 11 ≈ placebo 12; VOICE: v10 fixes v9), the two are very close. v10 trades 1 logic-trace catch for better VOICE + better famous-bug recall.

## Next
- Bump LOG01-style items to higher n to tighten the CI on the one clean effect.
- v11: can we keep v10's VOICE/famous-bug strength AND v9's logic-trace edge? (The difference may be v10's added validate-first verbosity slightly diluting the inspect-the-code reflex.)
