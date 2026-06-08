#!/usr/bin/env python3
"""Create per-(arm,chunk) driver instruction files for generation subagents.
Chunks interleave categories so the model must discriminate (challenge FP, not CLEAN) in one context.
"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent
DRV = ROOT / "drivers"; DRV.mkdir(exist_ok=True)
PROMPTS = ROOT / "prompts"; OUT = ROOT / "outputs"

ARMS = ["cold", "placebo_length_matched", "v7_v3_plus_deliver", "v8_voice_layer", "v9_voice_delabeled"]
CHUNKS = {
    "A": ["FP01", "CLEAN01", "SAFE01", "DELIVER01", "VOICE01"],
    "B": ["FP02", "CLEAN02", "SAFE02", "DELIVER02", "VOICE02"],
    "C": ["FP03", "CLEAN03", "FP04"],
}

manifest = []
for arm in ARMS:
    for ch, codes in CHUNKS.items():
        lines = [
            "You are a generation worker. Process each task file below INDEPENDENTLY — treat each as a brand-new, unrelated request with a clean slate; do NOT let one answer influence another.",
            "For EACH task file:",
            "  1. Read the file with your read tool.",
            "  2. It contains [SYSTEM ROLE INSTRUCTIONS] (maybe empty), a [USER MESSAGE], and output rules.",
            "  3. Fully adopt the system role instructions, then answer the USER MESSAGE per the output rules (<=180 words).",
            "  4. Write ONLY your answer (no preamble, no commentary) to the given OUTPUT path with your write tool.",
            "Do all tasks. Report 'DONE <n>' when finished.",
            "",
            "TASKS:",
        ]
        for i, code in enumerate(codes, 1):
            pf = PROMPTS / f"{arm}__{code}.txt"
            of = OUT / f"{arm}__{code}.txt"
            lines.append(f"{i}. READ: {pf}")
            lines.append(f"   WRITE-ANSWER-TO: {of}")
        (DRV / f"{arm}__{ch}.txt").write_text("\n".join(lines) + "\n")
        manifest.append(f"{arm}__{ch}")

print("\n".join(manifest))
print(f"\n{len(manifest)} driver files in {DRV}")
