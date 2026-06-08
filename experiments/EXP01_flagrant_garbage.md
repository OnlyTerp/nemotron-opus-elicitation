# EXP01 — Flagrant bad data (dataset audit)

## Design
Give Nemotron a 4-entry sample of `11-47/claude_opus_4.8_max_thinking_5k_v2` (templated filler: identical skeleton across entries, scenario text swapped, entries 2&3 have the same prompt) and ask: is this good source material for learning how Opus reasons?

Arms: COLD (no template) vs TMPL (v2). 1 trial each.

## Result
**Both rejected it.** The repetition was flagrant enough that cold caught it unaided. So the test did NOT cleanly discriminate on the binary "catches garbage."

## The real signal (quality, not binary)
- COLD overreached: asserted *"Opus 4.8 does not exist… appears fabricated"* — an unbacked claim from stale knowledge (it's wrong; 4.8 exists). Exactly the "didn't check my own premise" error.
- TMPL stayed disciplined: confined itself to what the sample proves — *"the repetition alone falsifies the claim"* — and invoked the gate explicitly. No overclaim.

## Conclusion
Inconclusive on the headline, but the template improved **epistemic discipline** (no overclaim) even when both reached the same verdict. Test was too easy → motivated EXP02/03 with subtler premises. Also confirmed `11-47` is garbage (see `findings/dataset_provenance.md`).
