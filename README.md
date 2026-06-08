# nemotron-opus-elicitation

**Make Nemotron 3 Ultra warm, honest, and reliable — without fine-tuning.**

Nemotron 3 Ultra is a powerful model with a personality problem. By default it:
- Opens corrections with a flat **"No."** and never says what you got right
- Misses subtle code bugs (off-by-ones, wrong formulas) because it eyeballs instead of checking
- Sometimes narrates its own reasoning process ("Premise check: ... Gate 1 ...")
- Misses silent wrong-output bugs in functions that *look* correct

This repo contains **v16** — a 353-word system prompt that fixes all four, proven across 25 controlled experiments with blind dual-judge grading. It makes Nemotron say "Hell yeah" when you're excited, catch silent code bugs the bare model misses, and validate what you got right before correcting what you got wrong.

## Quick start

Copy the system prompt from [`templates/v16_personality_calibrate.md`](templates/v16_personality_calibrate.md) — the text between `=== BEGIN` and `=== END` — and paste it into your Devin CLI's `~/.config/devin/agents/nemotron-ultra/AGENT.md` (or wherever your Nemotron agent's system prompt lives).

That's it. 353 words. No tools, no scaffolding, no fine-tuning.

## What it actually does

| Problem | Before (cold) | After (v16) | Evidence |
|---|---|---|---|
| Flat "No." on "check me" prompts | Opens with "No." / "Not quite" | "That's close but incomplete..." / "That's real anxiety." | EXP14: cold 1/4 → v16 4/4 VOICE |
| Silent code bugs (off-by-ones, wrong formulas) | Misses 8/10 | Catches 10/10 | EXP17: cold 2/10 → 10/10 |
| Process narration ("Premise check:", repetition loops) | 2/13 items | 0/13 | EXP08-09 |
| Personality (matches user energy) | Flat professional | "Hell yeah", "Nope", "Done" | EXP22-23 |
| Over-skepticism (inventing bugs in correct code) | 0/6 false positives | 0/6 | EXP05, EXP14 |

## How it works

The prompt installs three dispositions Nemotron already *has* but doesn't reliably *use*:

1. **Validate-first voice** — when someone says "check me" and is partly right, acknowledge what's correct before fixing what's wrong. (Nemotron's default: skip straight to correction.)

2. **Execute-verify on code** — before judging code correct, check its output on a concrete boundary input (even-length list, n=0/1, the empty case). (Nemotron's default: eyeball it.)

3. **Register calibration** — match the user's energy. Professional when they're professional, casual when they're casual. (Nemotron's default: stay in professional mode regardless.)

All three are dispositions the model already performs — the prompt just makes them fire reliably.

## Template lineage

| Version | What changed | Key result |
|---|---|---|
| v7/v8 | Labeled "GATE 1/GATE 2" scaffolding | Caused process-narration + repetition loops |
| v9 | Removed labels | 0 degeneration, beat v7/v8 |
| v10 | Added validate-first clause | Fixed VOICE regression |
| v11 | Compressed gates to one lean persona | Same performance at 60% length |
| v13 | Added execute-verify on code | Lifted silent-bug recall from 2/10 to 10/10 |
| v16 | Added register calibration | 20/20 on mixed battery, personality matches energy |
| v17 | Added data-driven Opus voice moves | 9/10 (1 VOICE regression), not adopted |

## Is this model-specific?

Yes. The effect is a **Nemotron-specific disposition repair**, not a universal prompt trick. On Qwen 3.6 35B (already warm/validate-first by default), v16 was a measured no-op — because there's no deficit to fix. The method — audit the base model for what it lacks, supply exactly that — is general. The specific prompt is tuned to Nemotron's gaps.

## What it doesn't do

- **Make Nemotron smarter.** It doesn't lift the capability ceiling. The hardest logic bugs defeat every prompt variant equally.
- **Guarantee every response.** It raises the floor and makes failures rarer, but prompting has a ceiling. For the hardest code-correctness cases, a real code execution sandbox beats even the best prompt.
- **Replace fine-tuning.** The Opus-candid dataset (7K conversations) is included in `opus-datasets/` for anyone who wants to fine-tune. Prompting installs the dispositions; fine-tuning would install them more reliably.

## Repo structure

| Path | What |
|---|---|
| `templates/v16_personality_calibrate.md` | **The prompt.** 353 words. Copy the text between BEGIN/END. |
| `USAGE.md` | How to use it, when it helps, when it doesn't, the "audit then supply" method |
| `THESIS.md` | The full research arc (15 refinements, 25 experiments) for the curious |
| `experiments/` | Each experiment: design, results, honest caveats |
| `bench/` | Test banks, generation harness, blind grading infrastructure |
| `opus-datasets/` | Opus-candid personality data (7K conversations) for fine-tuning |
| `findings/` | Early external reviews, dataset provenance |

## Running the experiments

Everything is reproducible. The bench harness uses Nemotron via Devin's `run_subagent` (profile `nemotron-ultra`), file-based generation with a topic-validator to prevent cross-wiring, and blind grading by two non-Nemotron judges (MiMo v2.5 Pro + MiniMax-M3).

```
# Generate (cold arm, mixed battery)
cd bench && python3 build_mixed.py

# Grade blind
# (dispatches to judges via run_subagent, writes to grades/)

# Score
python3 score_mixed.py
```

## License

MIT. The Opus-candid dataset has its own license from the original authors.

## Acknowledgments

Built on [Devin](https://devin.ai) CLI. Nemotron 3 Ultra via Blackbox AI. Judging by MiMo v2.5 Pro (Xiaomi) and MiniMax-M3. The Opus-candid dataset was originally created by [Verdugie](https://huggingface.co/Verdugie/opus-candid-training-data).
