# Dataset provenance — which "Opus" HF datasets are real signal vs noise

We mined several HuggingFace datasets claiming to capture Opus reasoning. **Most are community-uploaded synthetic data, not authentic Anthropic outputs.** Treat all as unverified. Quality varies enormously.

## Verdict table

| Dataset | What it actually is | Usable? |
|---|---|---|
| `11-47/claude_opus_4.8_max_thinking_5k_v2` | **Templated filler.** 5k entries, identical skeleton ("Key Dimensions Considered" / "Structured Recommendations") with the task string swapped in. The "assistant" turns contain NO actual reasoning or answers — just the *shape* of an answer. | ❌ **Garbage.** Do not extract patterns from it. We accidentally over-weighted its rigid skeleton in template v1. |
| `angrygiraffe/*` (nuclear, nativism, Bourdieu threads) | Higher-quality multi-turn reasoning; validate-first, cataloged uncertainty, names scholars. Possibly real Claude, possibly good synthetic. | ✅ Good *behavioral* signal (not ground truth) |
| `HelioAI/Claude-Opus-4.x-DeepReason` | Long-form reasoning traces (multilingual incl. Russian). Viewer broken (malformed JSON). | ⚠️ Mixed; hard to verify |
| `Verdugie/opus-4.6-training-catalog`, `opus-candid-training-data` | Conversational/personality + STEM pedagogy framing | ⚠️ Synthetic-looking; use cautiously |
| `ansulev/Opus-4.7-Reasoning-CoT-4800x`, `Bas95/reasoning-distill-claude-opus-4-7-max` | CoT traces with extended-thinking framing | ⚠️ Unverified |

## The lesson (cost us a template version)
The rigid section skeleton in template **v1** came disproportionately from the WORST dataset (`11-47`). The genuinely good examples (Rust zero-cost, Bourdieu, endocarditis, scRNA-seq) do NOT use a fixed skeleton — their structure follows the problem. **Behavioral patterns (validate-first, specificity, premise-skepticism, failure-mode surfacing) are the real signal; fixed output templates are noise.**

## Practical guidance
- Do NOT train/prompt toward a fixed section format.
- If we ever want real traces: capture them ourselves via the Claude API with extended thinking, or use vetted open CoT datasets (OpenThoughts, R1 distills) — not HF "opus" uploads.
- Every dataset here is a *hypothesis generator*, validated only by live A/B tests against Nemotron (see `experiments/`).
