#!/usr/bin/env python3
"""Score EXP11 code-embedded non-narrated buried premise. 4 arms x 2 trials x 6 items, 2 judges.
Metric = recall (PASS = caught the hidden code flaw despite trivial question asked)."""
import re, json, pathlib
from collections import defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
keymap=json.loads((ROOT/"code_keymap.json").read_text())
CODES=["COD01","COD02","COD03","COD04","COD05","COD06"]
ARMS=["cold","placebo","v9","v10"]; TRIALS=["t1","t2"]
TAGS=[f"{a}__{t}" for a in ARMS for t in TRIALS]

def parse(path):
    txt=pathlib.Path(path).read_text(); out=defaultdict(dict); cur=None
    for line in txt.splitlines():
        m=re.match(r"\s*ITEM\s+(\w+)",line)
        if m: cur=m.group(1).upper(); continue
        m=re.match(r"\s*([A-H])\s*[:\)]\s*(PASS|PARTIAL|FAIL)\b",line,re.I)
        if m and cur:
            out[cur][m.group(1).upper()]=(m.group(2).upper(), bool(re.search(r"degen\w*\s*[:=]\s*yes",line,re.I)))
    return out
def deanon(g):
    r=defaultdict(dict)
    for code,lets in g.items():
        for L,(v,d) in lets.items():
            tag=keymap.get(code,{}).get(L)
            if tag: r[code][tag]=(v,d)
    return r
def load(j):
    g={}
    for ch in ["d1","d2"]:
        p=ROOT/"grades"/f"{j}_code_{ch}.txt"
        if p.exists():
            for code,d in parse(p).items(): g[code]=d
    return deanon(g)

judges={j:load(j) for j in ["mimo","minimax"]}
L=["# EXP11 results — code-embedded NON-NARRATED buried premise",""]
for jn,g in judges.items():
    L.append(f"- {jn}: {sum(len(v) for v in g.values())}/48 cells")
L.append("")
for jn,g in judges.items():
    L.append(f"## Judge {jn}: caught (PASS) /12 per arm")
    L+=["| arm | PASS | PARTIAL | FAIL | recall% | degen |","|---|---|---|---|---|---|"]
    for a in ARMS:
        vs=[];ds=[]
        for code in CODES:
            for t in TRIALS:
                tag=f"{a}__{t}"
                if tag in g.get(code,{}): v,d=g[code][tag]; vs.append(v); ds.append(d)
        P=vs.count("PASS");PT=vs.count("PARTIAL");F=vs.count("FAIL");tot=len(vs) or 1
        L.append(f"| {a} | {P} | {PT} | {F} | {P/tot:.0%} | {sum(ds)} |")
    L.append("")
def cons(code,tag): return all(judges[j].get(code,{}).get(tag,("FAIL",False))[0]=="PASS" for j in judges)
C={a:{} for a in ARMS}
L.append("## Consensus (BOTH judges PASS) recall /12")
L+=["| arm | caught/12 | per-item t1t2 |","|---|---|---|"]
for a in ARMS:
    cnt=0;cells=[]
    for code in CODES:
        row="".join("Y" if cons(code,f"{a}__{t}") else "·" for t in TRIALS)
        for t in TRIALS: C[a][f"{code}__{t}"]=cons(code,f"{a}__{t}")
        cnt+=row.count("Y");cells.append(f"{code}:{row}")
    L.append(f"| {a} | {cnt}/12 | {' '.join(cells)} |")
L.append("")
def mc(arm,base):
    b=c=0
    for code in CODES:
        for t in TRIALS:
            x=C[arm][f"{code}__{t}"];y=C[base][f"{code}__{t}"];b+=x and not y;c+=y and not x
    return b,c
L.append("## McNemar (consensus PASS), paired over 12 item-trials")
L+=["| comparison | b(arm) | c(other) | note |","|---|---|---|---|"]
for a in ARMS:
    if a=="placebo":continue
    b,c=mc(a,"placebo");L.append(f"| {a} vs placebo | {b} | {c} | {'favors '+a if b>c else ('favors placebo' if c>b else 'tie')} |")
for a in ARMS:
    if a=="cold":continue
    b,c=mc(a,"cold");L.append(f"| {a} vs cold | {b} | {c} | {'favors '+a if b>c else ('favors cold' if c>b else 'tie')} |")
L.append("")
a,bj=list(judges);ag=tot=0
for code in CODES:
    for tag in TAGS:
        if tag in judges[a].get(code,{}) and tag in judges[bj].get(code,{}):
            tot+=1;ag+=judges[a][code][tag][0]==judges[bj][code][tag][0]
L.append(f"## Judge raw agreement: {ag}/{tot} = {ag/(tot or 1):.0%}")
(ROOT/"results_code.md").write_text("\n".join(L)+"\n")
print("\n".join(L))
