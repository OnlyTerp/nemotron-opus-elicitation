# EXP16 — Cross-model transfer: does the persona effect exist on Qwen-35B?

## Goal
The whole campaign's robust finding is "a warm-expert persona fixes Nemotron's cold VOICE (1/4 → 4/4)." Is that a general fact about LLMs, or specific to Nemotron's baseline? Run v11 vs cold on a DIFFERENT base model — **Qwen3.6-35B-A3B** (local, RTX 4090) — on the discriminating subset: VOICE×2, PREM×2, LOGIC×2, 2 trials, blind, same 2 non-Nemotron judges.

## Result — consensus (BOTH PASS) /12 on Qwen-35B
| arm | total | VOICE | PREM | LOGIC |
|---|---|---|---|---|
| cold | 11/12 | 3/4 | 4/4 | 4/4 |
| v11 | 11/12 | 3/4 | 4/4 | 4/4 |

**Identical.** On Qwen, the persona prompt made **zero difference** on every axis.

## Why — this is the key scoping finding of the whole project

**Qwen's bare model is already validate-first.** Cold Qwen, on the closure "check me" probe, opens *"Your understanding is close but incomplete…"* and *"You're partway there, but…"* — it acknowledges the right part before correcting, unprompted. That is exactly the behavior the persona was installed to produce on Nemotron. Qwen doesn't have Nemotron-cold's flat-"No" reflex, so **there is nothing for the persona to repair.**

Contrast the same VOICE probe across models, COLD (no persona):
- **Nemotron cold (EXP14):** opens "No"/"Not quite", corrects without validating → VOICE 1/4.
- **Qwen cold (EXP16):** opens "You're partway there, but…", validates then corrects → VOICE 3/4.

The persona lifted Nemotron from 1/4 to ~4/4. It can't lift Qwen because Qwen starts at 3/4 already.

## What this means for the central thesis

1. **The "persona fixes VOICE" effect is real but MODEL-SPECIFIC.** It's not a universal LLM law — it's the repair of a *particular deficiency in Nemotron's default disposition* (cold, blunt, correction-first on "check me"). A model whose baseline is already warm (Qwen) gets no benefit because it has no deficit.
2. **This sharpens, not weakens, the "elicitation gap" thesis.** The whole bet was "Nemotron has the capability but not the disposition." EXP16 confirms the *disposition gap is the thing being closed*: where a model already has the disposition (Qwen), the prompt is a no-op; where it doesn't (Nemotron), the prompt closes it. The prompt supplies a missing disposition, it doesn't add capability — exactly the thesis.
3. **PREM and LOGIC transfer trivially because both models already do them** (4/4 both arms, both models). Consistent with the campaign-wide finding that premise/bug-catching is mostly baseline capability, lightly moved by prompting.
4. **Practical implication:** a persona prompt's value depends on the target model's baseline. Audit the bare model first; only invest in persona engineering for the dispositions it actually lacks. For Nemotron that's VOICE/validate-first warmth; for Qwen it's already handled.

## Caveats
- n small (6 items × 2 trials × 2 arms = 24 gens). Single Qwen variant (35B-A3B MoE, Q-quant, local). VOICE n=4/arm is the headline and it's a tie at 3/4 — the *direction* (no persona benefit on Qwen) is clear, the exact rate is noisy.
- One MX02 trial graded PARTIAL for both cold and v11 (both judges agreed) — the recursion probe's "validate-first" bar is strict; neither arm consistently cleared it on Qwen, again showing no persona separation.

## Campaign-level conclusion this enables
The deliverable is not "a magic Opus prompt." It is: **identify the specific disposition your base model lacks, and supply exactly that with a lean persona.** For Nemotron 3 Ultra the lacking disposition is warm validate-first VOICE (+ slight premise-first nudge), and `templates/v11_lean_synthesis.md` supplies it. For a model like Qwen that already has it, skip the persona — it's a no-op. That is the honest, generalizable result.
