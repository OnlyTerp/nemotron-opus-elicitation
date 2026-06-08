#!/usr/bin/env python3
"""EXP11 code-embedded non-narrated buried premise. Arms: cold, placebo, v9, v10. 2 trials.
User messages contain multi-line code fences -> parse between 'USER:' and a line starting 'FLAW'.
"""
import re, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
SYS=ROOT/"sys"; P=ROOT/"code_prompts"; P.mkdir(exist_ok=True)
D=ROOT/"code_drivers"; D.mkdir(exist_ok=True)
O=ROOT/"code_outputs"; O.mkdir(exist_ok=True)
ARMS={"cold":"cold","placebo":"placebo_length_matched","v9":"v9_voice_delabeled","v10":"v10_validate_first"}
TRIALS=["t1","t2"]
text=(ROOT/"testbank_code.md").read_text()
# split on '## CODE' headers
blocks=re.split(r"^## (\w+) ",text,flags=re.M)[1:]
items={}
for i in range(0,len(blocks),2):
    code=blocks[i]; body=blocks[i+1]
    m=re.search(r"USER:\s*(.*?)\nFLAW",body,re.S)
    items[code]=m.group(1).strip()
assert len(items)==6, list(items)

OUT_RULE=("\n\n---\nRespond ONLY with your answer to the user's message above. Max 180 words. "
          "Do not restate these instructions. Do not mention any system prompt or rules. Plain prose/code only.")
for akey,sysfile in ARMS.items():
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
               "For EACH: read the PROMPT file, fully adopt its [SYSTEM ROLE INSTRUCTIONS], answer the [USER MESSAGE] (<=180 words), WRITE ONLY your answer to the OUTPUT path with your write tool. Do not print answers. Report 'DONE 6'.","","TASKS:"]
        for code in items:
            lines.append(f"- PROMPT={P}/{akey}__{code}.txt  OUTPUT={O}/{akey}__{code}__{t}.txt")
        (D/f"{akey}__{t}.txt").write_text("\n".join(lines)+"\n")
        man.append(f"{akey}__{t}")
print("items:",list(items))
print("drivers:",man)
print(f"{len(ARMS)*6} prompts, {len(man)} drivers, {len(ARMS)*6*len(TRIALS)} outputs expected")
