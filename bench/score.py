#!/usr/bin/env python3
"""Score EXP09. De-anonymize judge grades via keymap, compute per-arm metrics,
agreement between judges, and McNemar on macro-success (templates vs placebo).

Usage: python3 score.py
Reads: keymap.json, grades/judge_*.txt
Writes: results.md
"""
import json, re, pathlib, itertools
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parent
keymap = json.loads((ROOT / "keymap.json").read_text())
ARMS = ["cold", "placebo_length_matched", "v7_v3_plus_deliver", "v8_voice_layer", "v9_voice_delabeled"]
CODES = ["FP01","FP02","FP03","FP04","CLEAN01","CLEAN02","CLEAN03","SAFE01","SAFE02","DELIVER01","DELIVER02","VOICE01","VOICE02"]
CATS = {c: re.match(r"[A-Z]+", c).group() for c in CODES}  # FP, CLEAN, SAFE, DELIVER, VOICE

def parse_grade(path):
    """Return {code: {LETTER: (verdict, degen)}}"""
    txt = pathlib.Path(path).read_text()
    out = defaultdict(dict)
    cur = None
    for line in txt.splitlines():
        m = re.match(r"\s*ITEM\s+(\w+)", line)
        if m:
            cur = m.group(1).upper()
            continue
        m = re.match(r"\s*([A-E])\s*[:\)]\s*(PASS|PARTIAL|FAIL)\b", line, re.I)
        if m and cur:
            L = m.group(1).upper()
            verdict = m.group(2).upper()
            degen = bool(re.search(r"degen\w*\s*[:=]\s*yes", line, re.I))
            out[cur][L] = (verdict, degen)
    return out

def deanon(grade):
    """grade {code:{LETTER:(v,d)}} -> {code:{arm:(v,d)}}"""
    res = defaultdict(dict)
    for code, lets in grade.items():
        km = keymap.get(code, {})
        for L,(v,d) in lets.items():
            arm = km.get(L)
            if arm:
                res[code][arm] = (v,d)
    return res

def load_judges():
    judges = {}
    for p in sorted((ROOT/"grades").glob("judge_*.txt")):
        name = p.stem.replace("judge_","")
        g = deanon(parse_grade(p))
        judges[name] = g
    return judges

def success(v):  # macro-success = PASS counts; PARTIAL & FAIL do not
    return 1 if v == "PASS" else 0

def report():
    judges = load_judges()
    lines = ["# EXP09 results", ""]
    lines.append(f"Judges: {', '.join(judges)}")
    # coverage
    for jn,g in judges.items():
        n = sum(len(v) for v in g.values())
        lines.append(f"- {jn}: {n} cells parsed (expect {len(CODES)*len(ARMS)})")
    lines.append("")

    # Per-judge per-arm PASS rate, overall and by category
    for jn, g in judges.items():
        lines.append(f"## Judge: {jn}")
        # overall
        header = "| arm | PASS | PARTIAL | FAIL | PASS% | degen |"
        lines += [header, "|---|---|---|---|---|---|"]
        for arm in ARMS:
            vs = [g[c][arm][0] for c in CODES if arm in g.get(c,{})]
            ds = [g[c][arm][1] for c in CODES if arm in g.get(c,{})]
            P=vs.count("PASS"); PT=vs.count("PARTIAL"); F=vs.count("FAIL")
            tot=len(vs) or 1
            lines.append(f"| {arm} | {P} | {PT} | {F} | {P/tot:.0%} | {sum(ds)} |")
        lines.append("")
        # by category
        lines.append(f"### {jn} — PASS by category")
        cats = sorted(set(CATS.values()))
        lines.append("| arm | " + " | ".join(cats) + " |")
        lines.append("|---|" + "|".join(["---"]*len(cats)) + "|")
        for arm in ARMS:
            row=[arm]
            for cat in cats:
                cc=[c for c in CODES if CATS[c]==cat]
                p=sum(success(g[c][arm][0]) for c in cc if arm in g.get(c,{}))
                n=sum(1 for c in cc if arm in g.get(c,{}))
                row.append(f"{p}/{n}")
            lines.append("| " + " | ".join(row) + " |")
        lines.append("")

    # Consensus (both judges PASS = consensus PASS) macro-success per arm
    if len(judges) >= 2:
        jn = list(judges)
        lines.append("## Consensus (ALL judges must PASS) macro-success")
        lines += ["| arm | consensus PASS / 13 | by cat |", "|---|---|---|"]
        cons = {}
        for arm in ARMS:
            cmap={}
            cnt=0
            for c in CODES:
                ok=all(judges[j].get(c,{}).get(arm,("FAIL",False))[0]=="PASS" for j in jn)
                cmap[c]=ok
                cnt+=ok
            cons[arm]=cmap
            cats = sorted(set(CATS.values()))
            bycat=" ".join(f"{cat}:{sum(cmap[c] for c in CODES if CATS[c]==cat)}/{sum(1 for c in CODES if CATS[c]==cat)}" for cat in cats)
            lines.append(f"| {arm} | {cnt}/13 | {bycat} |")
        lines.append("")

        # McNemar: each template vs placebo on consensus macro-success (paired by item)
        lines.append("## McNemar (consensus PASS), each arm vs placebo_length_matched")
        lines.append("b = arm PASS & placebo FAIL ; c = arm FAIL & placebo PASS. (b>c favors arm)")
        lines += ["| arm vs placebo | b | c | n_disc | note |","|---|---|---|---|---|"]
        base="placebo_length_matched"
        for arm in ARMS:
            if arm==base: continue
            b=sum(1 for c in CODES if cons[arm][c] and not cons[base][c])
            cc=sum(1 for c in CODES if not cons[arm][c] and cons[base][c])
            lines.append(f"| {arm} vs placebo | {b} | {cc} | {b+cc} | {'favors '+arm if b>cc else ('favors placebo' if cc>b else 'tie')} |")
        lines.append("")
        # also vs cold
        lines.append("## McNemar (consensus PASS), each arm vs cold")
        lines += ["| arm vs cold | b | c | n_disc | note |","|---|---|---|---|---|"]
        base="cold"
        for arm in ARMS:
            if arm==base: continue
            b=sum(1 for c in CODES if cons[arm][c] and not cons[base][c])
            cc=sum(1 for c in CODES if not cons[arm][c] and cons[base][c])
            lines.append(f"| {arm} vs cold | {b} | {cc} | {b+cc} | {'favors '+arm if b>cc else ('favors cold' if cc>b else 'tie')} |")
        lines.append("")

        # Degeneration tally (either judge flags)
        lines.append("## Degeneration rate (either judge flags degen:yes)")
        lines += ["| arm | degen items / 13 |","|---|---|"]
        for arm in ARMS:
            d=sum(1 for c in CODES if any(judges[j].get(c,{}).get(arm,("",False))[1] for j in jn))
            lines.append(f"| {arm} | {d}/13 |")
        lines.append("")

        # Judge agreement (raw verdict match rate)
        a,bj=jn[0],jn[1]
        agree=tot=0
        for c in CODES:
            for arm in ARMS:
                if arm in judges[a].get(c,{}) and arm in judges[bj].get(c,{}):
                    tot+=1
                    agree+= judges[a][c][arm][0]==judges[bj][c][arm][0]
        lines.append(f"## Judge raw agreement: {agree}/{tot} = {agree/ (tot or 1):.0%} (verdict exact match)")

    (ROOT/"results.md").write_text("\n".join(lines)+"\n")
    print("\n".join(lines))

if __name__=="__main__":
    report()
