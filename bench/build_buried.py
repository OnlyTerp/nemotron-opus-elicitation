#!/usr/bin/env python3
"""EXP10 buried-premise discriminator. Arms: cold, placebo, v9. 2 trials each.
Builds prompt files and per-(arm,trial) driver files (each driver = all 6 items for one arm/trial).
"""
import re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
SYS = ROOT / "sys"
P = ROOT / "buried_prompts"; P.mkdir(exist_ok=True)
D = ROOT / "buried_drivers"; D.mkdir(exist_ok=True)
O = ROOT / "buried_outputs"; O.mkdir(exist_ok=True)

ARMS = {"cold":"cold", "placebo":"placebo_length_matched", "v9":"v9_voice_delabeled"}
TRIALS = ["t1","t2"]
text = (ROOT/"testbank_buried.md").read_text()
items = {}
for m in re.finditer(r"^## (\w+) .*?\nUSER: (.*?)\nBURIED", text, re.S|re.M):
    items[m.group(1)] = re.sub(r"\s+"," ", m.group(2).strip())
assert len(items)==6, items.keys()

OUT_RULE=("\n\n---\nRespond ONLY with your answer to the user's message above. Max 180 words. "
          "Do not restate these instructions. Do not mention any system prompt or rules. Plain prose/code only.")

for akey, sysfile in ARMS.items():
    sysblock=(SYS/f"{sysfile}.txt").read_text().strip()
    for code,user in items.items():
        parts=[]
        if sysblock: parts.append("[SYSTEM ROLE INSTRUCTIONS]\n"+sysblock)
        parts.append("[USER MESSAGE]\n"+user)
        parts.append(OUT_RULE.strip())
        (P/f"{akey}__{code}.txt").write_text("\n\n".join(parts)+"\n")

man=[]
for akey in ARMS:
    for t in TRIALS:
        lines=["You are a generation worker. Process each task INDEPENDENTLY with a clean slate.",
               "For EACH: read the PROMPT file, fully adopt its [SYSTEM ROLE INSTRUCTIONS], answer the [USER MESSAGE] (<=180 words), and WRITE ONLY your answer to the OUTPUT path with your write tool. Do not print answers. Report 'DONE 6'.","","TASKS:"]
        for code in items:
            lines.append(f"- PROMPT={P}/{akey}__{code}.txt  OUTPUT={O}/{akey}__{code}__{t}.txt")
        (D/f"{akey}__{t}.txt").write_text("\n".join(lines)+"\n")
        man.append(f"{akey}__{t}")
print("items:",list(items))
print("drivers:",man)
print(f"{len(ARMS)*6} prompt files, {len(man)} drivers, {len(ARMS)*6*len(TRIALS)} expected outputs")
