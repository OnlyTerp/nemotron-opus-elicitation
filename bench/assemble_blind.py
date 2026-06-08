#!/usr/bin/env python3
"""Assemble blind grading bundles. For each item, gather all arm outputs,
shuffle them behind letters A.. with a per-item random mapping, write:
  - bench/blind/<ITEM>.txt   (judge-facing: USER + lettered candidates)
  - bench/keymap.json        (ITEM -> {LETTER: arm})
Also reports any missing/empty outputs.
"""
import json, random, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "outputs"; BLIND = ROOT / "blind"; BLIND.mkdir(exist_ok=True)
import re
ARMS = ["cold", "placebo_length_matched", "v7_v3_plus_deliver", "v8_voice_layer", "v9_voice_delabeled"]
# parse user messages from prompts (USER MESSAGE block)
PROMPTS = ROOT / "prompts"
bank = (ROOT / "testbank.md").read_text()
items = [m.group(1) for m in re.finditer(r"^## (\w+) ", bank, re.M)]
users = {}
for code in items:
    pf = (PROMPTS / f"cold__{code}.txt").read_text()
    u = pf.split("[USER MESSAGE]\n",1)[1].split("\n\n---",1)[0].strip()
    users[code] = u

rng = random.Random(20260608)
keymap = {}
missing = []
for code in items:
    cands = []
    for arm in ARMS:
        f = OUT / f"{arm}__{code}.txt"
        if not f.exists() or not f.read_text().strip():
            missing.append(f"{arm}__{code}")
            continue
        cands.append((arm, f.read_text().strip()))
    rng.shuffle(cands)
    letters = "ABCDE"
    keymap[code] = {}
    body = [f"# ITEM {code}", "", "USER MESSAGE:", users[code], "", "CANDIDATE ANSWERS:"]
    for i,(arm,txt) in enumerate(cands):
        L = letters[i]
        keymap[code][L] = arm
        body += ["", f"--- Candidate {L} ---", txt]
    (BLIND / f"{code}.txt").write_text("\n".join(body)+"\n")

(ROOT / "keymap.json").write_text(json.dumps(keymap, indent=2))
print("items:", len(items), "| blind bundles written")
print("MISSING/empty outputs:", missing if missing else "none")
