#!/usr/bin/env python3
"""EXP14 mixed battery. Arms cold/placebo/v10/v11, 2 trials. Delimiter-output gen."""
import re, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
SYS=ROOT/"sys"; P=ROOT/"mixed_prompts"; P.mkdir(exist_ok=True)
D=ROOT/"mixed_drivers"; D.mkdir(exist_ok=True); (ROOT/"mixed_outputs").mkdir(exist_ok=True)
ARMS={"cold":"cold","placebo":"placebo_length_matched","v10":"v10_validate_first","v11":"v11_lean_synthesis"}
TRIALS=["t1","t2"]
text=(ROOT/"testbank_mixed.md").read_text()
blocks=re.split(r"^## (\w+) ",text,flags=re.M)[1:]
items={}
for i in range(0,len(blocks),2):
    code=blocks[i]; body=blocks[i+1]
    m=re.search(r"USER:\s*(.*?)\nGROUND TRUTH:",body,re.S)
    items[code]=m.group(1).strip()
assert len(items)==10, list(items)
OUT_RULE=("\n\n---\nRespond ONLY with your answer to the user's message above. Max 180 words. "
          "Do not restate these instructions. Do not mention any system prompt or rules. Plain prose/code only.")
for akey,sf in ARMS.items():
    sb=(SYS/f"{sf}.txt").read_text().strip()
    for code,user in items.items():
        parts=[]
        if sb: parts.append("[SYSTEM ROLE INSTRUCTIONS]\n"+sb)
        parts.append("[USER MESSAGE]\n"+user); parts.append(OUT_RULE.strip())
        (P/f"{akey}__{code}.txt").write_text("\n\n".join(parts)+"\n")
man=[]
for akey in ARMS:
    for t in TRIALS:
        lines=["You are a generation worker. For EACH task: read the PROMPT file with your read tool, fully adopt its [SYSTEM ROLE INSTRUCTIONS], answer the [USER MESSAGE] in <=180 words.",
               "Do NOT use the write tool. Put ALL answers in your FINAL MESSAGE, each wrapped EXACTLY as:",
               "<<<BEGIN id>>>","...answer...","<<<END id>>>",
               "Process every task; output nothing else between blocks.","","TASKS:"]
        for code in items:
            lines.append(f"- id={akey}__{code}__{t}  PROMPT={P}/{akey}__{code}.txt")
        (D/f"{akey}__{t}.txt").write_text("\n".join(lines)+"\n"); man.append(f"{akey}__{t}")
print("items:",list(items)); print("drivers:",man)
