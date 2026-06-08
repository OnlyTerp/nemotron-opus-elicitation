#!/usr/bin/env python3
"""Score EXP17 ceiling. 4 arms (cold,v11,v12,v12tool) x 8 items x 2 trials, 2 judges.
BUGGY items CEIL01-05 = recall; CONTROL items CEIL06-08 = precision (PASS=no invented bug)."""
import re, json, pathlib
from collections import defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
keymap=json.loads((ROOT/"ceil_keymap.json").read_text())
ARMS=["cold","v11","v12","v12tool"]
CODES=[f"CEIL0{n}" for n in range(1,9)]; BUG=CODES[:5]; CTRL=CODES[5:]; TRIALS=["t1","t2"]
def parse(p):
    out=defaultdict(dict);cur=None
    for line in pathlib.Path(p).read_text().splitlines():
        m=re.match(r"\s*(?:ITEM\s+)?(CEIL\d\d)\b",line)
        if m: cur=m.group(1);continue
        m=re.match(r"\s*([A-H])\s*[:\)]\s*(PASS|PARTIAL|FAIL)\b",line,re.I)
        if m and cur: out[cur][m.group(1).upper()]=(m.group(2).upper(), bool(re.search(r"degen\w*\s*[:=]\s*yes",line,re.I)))
    return out
def deanon(g):
    r=defaultdict(dict)
    for c,l in g.items():
        for L,v in l.items():
            t=keymap.get(c,{}).get(L)
            if t: r[c][t]=v
    return r
def load(j):
    g={}
    for ch in ["p1","p2"]:
        p=ROOT/"grades"/f"{j}_ceil_{ch}.txt"
        if p.exists():
            for c,d in parse(p).items(): g[c]=d
    return deanon(g)
J={j:load(j) for j in ["mimo","minimax"]}
def cons(c,tag): return all(J[jj].get(c,{}).get(tag,("FAIL",False))[0]=="PASS" for jj in J)
L=["# EXP17 results — CEILING (does execution break the prompt-only ceiling?)",""]
for jn,g in J.items(): L.append(f"- {jn}: {sum(len(v) for v in g.values())}/64 cells")
L.append("")
L.append("## Consensus (BOTH judges PASS)")
L+=["| arm | BUG recall /10 | CONTROL precision /6 | per-bug-item (t1t2) |","|---|---|---|---|"]
for a in ARMS:
    bug=sum(1 for c in BUG for t in TRIALS if cons(c,f"{a}__{t}"))
    ctrl=sum(1 for c in CTRL for t in TRIALS if cons(c,f"{a}__{t}"))
    detail=" ".join(f"{c[4:]}:{''.join('Y' if cons(c,f'{a}__{t}') else '·' for t in TRIALS)}" for c in BUG)
    L.append(f"| {a} | {bug}/10 | {ctrl}/6 | {detail} |")
L.append("")
# per-judge recall too (less strict)
for jn,g in J.items():
    L.append(f"### Judge {jn}: BUG PASS /10 per arm")
    row=[]
    for a in ARMS:
        p=sum(1 for c in BUG for t in TRIALS if g.get(c,{}).get(f"{a}__{t}",("",0))[0]=="PASS")
        row.append(f"{a}:{p}/10")
    L.append("- "+" | ".join(row))
L.append("")
# McNemar v12tool vs v11, v12 vs v11, v11 vs cold on BUG items
def mc(arm,base):
    b=cc=0
    for c in BUG:
        for t in TRIALS:
            x=cons(c,f"{arm}__{t}");y=cons(c,f"{base}__{t}");b+=x and not y;cc+=y and not x
    return b,cc
L.append("## McNemar on BUG items (consensus)")
L+=["| comparison | b(arm wins) | c | note |","|---|---|---|---|"]
for arm,base in [("v11","cold"),("v12","v11"),("v12tool","v11"),("v12tool","v12"),("v12","cold"),("v12tool","cold")]:
    b,cc=mc(arm,base); L.append(f"| {arm} vs {base} | {b} | {cc} | {'favors '+arm if b>cc else ('favors '+base if cc>b else 'tie')} |")
L.append("")
a,bj=list(J);ag=tot=0
for c in CODES:
    for a2 in ARMS:
        for t in TRIALS:
            tag=f"{a2}__{t}"
            if tag in J[a].get(c,{}) and tag in J[bj].get(c,{}):
                tot+=1; ag+= J[a][c][tag][0]==J[bj][c][tag][0]
L.append(f"## Judge raw agreement: {ag}/{tot} = {ag/(tot or 1):.0%}")
(ROOT/"results_ceil.md").write_text("\n".join(L)+"\n")
print("\n".join(L))
