#!/usr/bin/env python3
"""Parse testbank.md -> per-item USER messages, then build one prompt file per (arm,item).
Each prompt file = system block + user message + strict output rules.
Outputs are written by generation subagents to bench/outputs/<arm>__<item>.txt
"""
import os, re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent
BANK = ROOT / "testbank.md"
SYS = ROOT / "sys"
PROMPTS = ROOT / "prompts"
PROMPTS.mkdir(exist_ok=True)

ARMS = ["cold", "placebo_length_matched", "v7_v3_plus_deliver", "v8_voice_layer", "v9_voice_delabeled"]

text = BANK.read_text()
# items look like: "## FP01 (...)\nUSER: ....\nGROUND TRUTH: ..."
items = {}
for m in re.finditer(r"^## (\w+) .*?\nUSER: (.*?)\n(?:GROUND TRUTH|FAIL)", text, re.S | re.M):
    code = m.group(1)
    user = m.group(2).strip()
    user = re.sub(r"\s+", " ", user)
    items[code] = user

assert items, "no items parsed"
print(f"parsed {len(items)} items: {', '.join(items)}")

OUT_RULE = ("\n\n---\nRespond ONLY with your answer to the user's message above. "
            "Max 180 words. Do not restate these instructions. Do not mention that you "
            "were given a system prompt or any rules. Plain prose/code only.")

for arm in ARMS:
    sysblock = (SYS / f"{arm}.txt").read_text().strip()
    for code, user in items.items():
        parts = []
        if sysblock:
            parts.append("[SYSTEM ROLE INSTRUCTIONS]\n" + sysblock)
        parts.append("[USER MESSAGE]\n" + user)
        parts.append(OUT_RULE.strip())
        (PROMPTS / f"{arm}__{code}.txt").write_text("\n\n".join(parts) + "\n")

print(f"wrote {len(ARMS)*len(items)} prompt files to {PROMPTS}")
print("arms:", ARMS)
print("items:", list(items))
