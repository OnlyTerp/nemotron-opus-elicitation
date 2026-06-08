#!/usr/bin/env python3
"""Score EXP10 buried-premise discriminator. 3 arms x 2 trials x 6 items, 2 judges.
Metric = recall (PASS = caught the buried practice). Reports per-arm caught/12 (6 items x 2 trials),
consensus (both judges PASS), per-item breakdown, and McNemar-style arm-vs-placebo / arm-vs-cold."""
import re, json, pathlib
from collections import defaultdict
ROOT=pathlib.Path(__file__).resolve().parent
keymap=json.loads((ROOT/"buried_keymap.json").read_text())
CODES=["BUR01","BUR02","BUR03","BUR04","BUR05","BUR06"]
ARMS=["cold","placebo","v9"]; TRIALS=["t1","t2"]
TAGS=[f"{a}__{t}" for a in ARMS for t in TRIALS]

def parse(path):
    txt=pathlib.Path(path).read_text(); out=defaultdict(dict); cur=None
    for line in txt.splitlines():
        m=re.match(r"\s*ITEM\s+(\w+)",line)
        if m: cur=m.group(1).upper(); continue
        m=re.match(r"\s*([A-F])\s*[:\)]\s*(PASS|PARTIAL|FAIL)\b",line,re.I)
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

def load(judge):
    g={}
    for ch in ["b1","b2"]:
        p=ROOT/"grades"/f"{judge}_buried_{ch}.txt"
        if p.exists():
            for code,d in parse(p).items(): g[code]=d
    return deanon(g)

judges={j:load(j) for j in ["mimo","minimax"]}
lines=["# EXP10 results — buried-premise discriminator",""]
for jn,g in judges.items():
    n=sum(len(v) for v in g.values())
    lines.append(f"- {jn}: {n}/36 cells parsed")
lines.append("")

# per-judge per-arm recall (PASS counts over 12 = 6 items x 2 trials)
for jn,g in judges.items():
    lines.append(f"## Judge {jn}: caught (PASS) per arm /12")
    lines+= ["| arm | PASS | PARTIAL | FAIL | recall% | degen |","|---|---|---|---|---|---|"]
    for a in ARMS:
        vs=[]; ds=[]
        for code in CODES:
            for t in TRIALS:
                tag=f"{a}__{t}"
                if tag in g.get(code,{}):
                    v,d=g[code][tag]; vs.append(v); ds.append(d)
        P=vs.count("PASS");PT=vs.count("PARTIAL");F=vs.count("FAIL");tot=len(vs) or 1
        lines.append(f"| {a} | {P} | {PT} | {F} | {P/tot:.0%} | {sum(ds)} |")
    lines.append("")

# consensus (both judges PASS) per arm/item/trial
def cons_pass(code,tag):
    return all(judges[j].get(code,{}).get(tag,("FAIL",False))[0]=="PASS" for j in judges)
lines.append("## Consensus (BOTH judges PASS) recall /12")
lines+=["| arm | caught/12 | per-item (t1,t2) |","|---|---|---|"]
cons={a:{} for a in ARMS}
for a in ARMS:
    cnt=0; cells=[]
    for code in CODES:
        row=[]
        for t in TRIALS:
            ok=cons_pass(code,f"{a}__{t}"); cons[a][f"{code}__{t}"]=ok; cnt+=ok
            row.append("Y" if ok else "·")
        cells.append(f"{code}:{''.join(row)}")
    lines.append(f"| {a} | {cnt}/12 | {' '.join(cells)} |")
lines.append("")

# McNemar arm vs placebo and vs cold (paired over 12 item-trials)
def mcnemar(arm,base):
    b=c=0
    for code in CODES:
        for t in TRIALS:
            x=cons[arm][f"{code}__{t}"]; y=cons[base][f"{code}__{t}"]
            b+= x and not y; c+= y and not x
    return b,c
lines.append("## McNemar (consensus PASS), paired over 12 item-trials")
lines+=["| comparison | b (arm wins) | c (other wins) | note |","|---|---|---|---|"]
for a in ARMS:
    if a=="placebo": continue
    b,c=mcnemar(a,"placebo")
    lines.append(f"| {a} vs placebo | {b} | {c} | {'favors '+a if b>c else ('favors placebo' if c>b else 'tie')} |")
for a in ARMS:
    if a=="cold": continue
    b,c=mcnemar(a,"cold")
    lines.append(f"| {a} vs cold | {b} | {c} | {'favors '+a if b>c else ('favors cold' if c>b else 'tie')} |")
lines.append("")

# judge agreement
a,bj=list(judges)
ag=tot=0
for code in CODES:
    for tag in TAGS:
        if tag in judges[a].get(code,{}) and tag in judges[bj].get(code,{}):
            tot+=1; ag+= judges[a][code][tag][0]==judges[bj][code][tag][0]
lines.append(f"## Judge raw agreement: {ag}/{tot} = {ag/(tot or 1):.0%}")
(ROOT/"results_buried.md").write_text("\n".join(lines)+"\n")
print("\n".join(lines))
