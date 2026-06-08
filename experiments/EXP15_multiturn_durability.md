# EXP15 — Multi-turn personality durability (does v11's voice survive 8 turns?)

## Goal
Claude's review flagged: "feels like Opus" only counts if it lasts past turn 1. Test whether v11's validate-first / warm-but-blunt persona survives a real 8-turn conversation with accumulated context, or decays toward the bare model's cold "no" by the late turns.

## Method
Two persistent conversations (real accumulated context via subagent resume), v11 system prompt set once at turn 1:
- **Turn 1:** VOICE "check me" probe (baseline persona reading).
- **Turns 2-6:** ordinary coding work (write/extend/test functions) to build genuine context and distance from the system prompt.
- **Turns 7-8:** fresh VOICE "check me" probes (late-turn persona reading).
- **Controls:** the exact turn-8 probes also run COLD-START (fresh v11, turn 1) to separate persona-decay from item-difficulty.

ConvA thread: decorators→word-freq code×5→generators(t7)→list-comprehensions(t8).
ConvB thread: GIL→timer code×5→is/==(t7)→sets(t8).

## Observations

### The persona is DURABLE through 8 turns.
Turn-8 in-conversation answers are stylistically identical to fresh turn-1 controls on the SAME probe:
| probe | turn-8 (8 deep) | fresh turn-1 control |
|---|---|---|
| list comprehensions (partial truth) | "**Mostly right.** They *are* syntactic sugar… but they're **expressions**…" | "**You're right on readability**… the 'faster' part is mostly a myth… they're *expressions*…" |
| sets (partial truth) | "**Partly right on deduplication**, wrong on 'basically lists'… [table]" | "**You're half right.** Sets *do* deduplicate… **What you got right:**… **Where it breaks:**…" |

Both validate-first, both warm-but-blunt, both dense with a comparison table — the v11 signature, intact at turn 8. No drift to terse/cold, no loss of the "name what's right first" move, 0 degeneration.

### The turn-7 "Wrong." was item-difficulty, not decay.
ConvA turn-7 (generator indexable like gen[0]) and convB turn-7 (`is` checks equality) both opened bluntly ("Wrong."/"Backwards."). But those claims are **flatly false**, not partial — and the bare model is *correctly* blunt on flatly-false claims (cf. convB's turn-1 GIL probe, also "Wrong."). When the late-turn claim is genuinely PARTIAL (turn 8), the answer validates-first exactly like turn 1. So bluntness tracked the truth-content of the claim, not the turn number. That's correct behavior, not decay.

### Mid-conversation persona traits also held.
- Turn 3 convA: asked to "handle punctuation," it recognized the existing regex already did and said "**Already handled**" instead of inventing busywork — the honest, non-padding disposition surviving mid-conversation.
- Code answers stayed dense/specific (type hints, complexity notes like "most_common uses heapq.nlargest → O(n log k)") across all turns.

## Verdict
**v11's persona is multi-turn durable.** Over 8 turns with 5 intervening coding tasks, the validate-first/warm-but-blunt/dense voice did not decay — late-turn partial-truth probes were handled identically to cold-start. Bluntness correctly scales with how-wrong the claim is, not with conversation depth. This addresses the "does it last past turn 1" challenge: yes.

Caveat: n=2 conversations, single model (Nemotron), one prompt (v11). Not a quantified decay curve — a strong existence check that decay is not gross. A fuller version would run ≥6 threads and blind-grade turn-1 vs turn-8 validate-first rate. But the qualitative signal is clear and one-directional.

## Next
- Qwen-35B transfer (does the persona effect exist on a different base model, or is it Nemotron-specific?) — the highest-value remaining question.
