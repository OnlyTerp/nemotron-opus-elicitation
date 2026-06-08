#!/usr/bin/env python3
import re, json, pathlib
from collections import defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
keymap=json.loads((ROOT/"hard_keymap.json").read_text())
ARMS=["cold","v12","v12tool"]
CODES=[f"HARD0{n}" for n in range(1,9)]; BUG=CODES[:6]; CTRL=CODES[6:]; TRIALS=["t1","t2"]
def parse(p):
    out=defaultdict(dict);cur=None
    for line in pathlib.Path(p).read_text().splitlines():
        m=re.match(r"\s*(?:ITEM\s+)?(HARD\d\d)\b",line)
        if m: cur=m.group(1);continue
        m=re.match(r"\s*([A-F])\s*[:\)]\s*(PASS|PARTIAL|FAIL)\b",line,re.I)
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
    for ch in ["h1","h2"]:
        p=ROOT/"grades"/f"{j}_hard_{ch}.txt"
        if p.exists():
            for c,d in parse(p).items(): g[c]=d
    return deanon(g)
J={j:load(j) for j in ["mimo","minimax"]}
def cons(c,tag): return all(J[jj].get(c,{}).get(tag,("FAIL",False))[0]=="PASS" for jj in J)
L=["# EXP18 results — HARD bank (does the SANDBOX beat mental execution?)",""]
for jn,g in J.items(): L.append(f"- {jn}: {sum(len(v) for v in g.values())}/48 cells")
L.append("")
L.append("## Consensus (BOTH judges PASS)")
L+=["| arm | BUG recall /12 | CONTROL precision /4 | per-bug (t1t2) |","|---|---|---|---|"]
for a in ARMS:
    bug=sum(1 for c in BUG for t in TRIALS if cons(c,f"{a}__{t}"))
    ctrl=sum(1 for c in CTRL for t in TRIALS if cons(c,f"{a}__{t}"))
    detail=" ".join(f"{c[4:]}:{''.join('Y' if cons(c,f'{a}__{t}') else '.' for t in TRIALS)}" for c in BUG)
    L.append(f"| {a} | {bug}/12 | {ctrl}/4 | {detail} |")
L.append("")
# the key comparison: v12tool vs v12 on HARD02 (float) and overall
def mc(arm,base,items):
    b=cc=0
    for c in items:
        for t in TRIALS:
            x=cons(c,f"{arm}__{t}");y=cons(c,f"{base}__{t}");b+=x and not y;cc+=y and not x
    return b,cc
L.append("## McNemar: does v12tool (sandbox) beat v12 (mental)?")
b,cc=mc("v12tool","v12",BUG); L.append(f"- v12tool vs v12 on ALL bug items: b={b} c={cc} -> {'sandbox wins' if b>cc else ('mental wins' if cc>b else 'TIE')}")
b,cc=mc("v12tool","v12",["HARD02"]); L.append(f"- v12tool vs v12 on HARD02 (float rounding, the predicted sandbox win): b={b} c={cc}")
b,cc=mc("v12","cold",BUG); L.append(f"- v12 vs cold on bug items: b={b} c={cc}")
L.append("")
a,bj=list(J);ag=tot=0
for c in CODES:
    for a2 in ARMS:
        for t in TRIALS:
            tag=f"{a2}__{t}"
            if tag in J[a].get(c,{}) and tag in J[bj].get(c,{}):
                tot+=1; ag+= J[a][c][tag][0]==J[bj][c][tag][0]
L.append(f"## Judge raw agreement: {ag}/{tot} = {ag/(tot or 1):.0%}")
(ROOT/"results_hard.md").write_text("\n".join(L)+"\n")
print("\n".join(L))
