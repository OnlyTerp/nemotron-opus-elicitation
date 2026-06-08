#!/usr/bin/env python3
"""EXP13 pipeline: parse delimiter blocks -> validate topic -> write logic2_outputs/. Then assemble blind + rubric + chunks.
Usage: parse <raw...> | status | assemble"""
import re, sys, json, random, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
O=ROOT/"logic2_outputs"; O.mkdir(exist_ok=True)
ARMS=["cold","placebo","v9","v10"]; CODES=[f"LGB{n:02d}" for n in range(1,11)]; TRIALS=["t1","t2"]
ANCH={
 "LGB01":[r"chunk_count",r"math\.ceil|ceil",r"total",r"\bsize\b",r"import"],
 "LGB02":[r"group_sums",r"\btotal\b",r"reset",r"per-row|running total",r"result\.append"],
 "LGB03":[r"is_valid_age",r"\bage\b",r"precedence|and .*or|or age",r"150",r"two lines|one line"],
 "LGB04":[r"remove_duplicates",r"\btmp\b",r"alias|same object|reference",r"iterat|while.*remov|mutat",r"seen"],
 "LGB05":[r"last_n",r"\bseq\b",r"range\(len",r"negative|n >|clamp|max\(0",r"docstring"],
 "LGB06":[r"def average",r"//|floor|integer divis",r"\bs\b.*\bc\b|s // c",r"1\.5",r"count|rename"],
 "LGB07":[r"all_positive",r"any|first positive|returns True",r"\bn > 0\b|n>0",r"comment",r"\bALL\b|\bany\b"],
 "LGB08":[r"add_edge",r"setdefault",r"graph",r"adjacency|undirected|correct",r"Black"],
 "LGB09":[r"is_power_of_two",r"n & |n-1|n & \(n",r"power of two|correct",r"\bn\b",r"name"],
 "LGB10":[r"\bclamp\b",r"max\(|min\(",r"\blo\b|\bhi\b|swap",r"type hint",r"bound"],
}
def classify(t):
    h={c:sum(1 for p in ANCH[c] if re.search(p,t,re.I)) for c in CODES}
    b=max(h,key=h.get); return b,h[b],h
def parse(files):
    wrote=0;rej=[]
    for fp in files:
        for m in re.finditer(r"<<<BEGIN\s+(\w+)>>>\s*(.*?)\s*<<<END\s+\1>>>",pathlib.Path(fp).read_text(),re.S):
            cid=m.group(1);body=m.group(2).strip()
            mm=re.match(r"(\w+)__(LGB\d\d)__(t\d)",cid)
            if not mm: rej.append((cid,"bad id"));continue
            item=mm.group(2);b,s,h=classify(body)
            if b!=item and h.get(item,0)==0: rej.append((cid,f"looks like {b} not {item}"));continue
            (O/f"{cid}.txt").write_text(body+"\n");wrote+=1
    print(f"wrote {wrote}; rejected {len(rej)}")
    for cid,why in rej: print("  REJECT",cid,why)
def status():
    miss=[f"{a}__{c}__{t}" for a in ARMS for c in CODES for t in TRIALS if not (O/f"{a}__{c}__{t}.txt").exists() or not (O/f"{a}__{c}__{t}.txt").read_text().strip()]
    print(f"present {80-len(miss)}/80 ; missing {len(miss)}")
    if miss: print("MISSING:"," ".join(miss))
    (ROOT/"logic2_bad.txt").write_text("\n".join(miss))
def assemble():
    text=(ROOT/"testbank_logic2.md").read_text()
    blocks=re.split(r"^## (\w+) ",text,flags=re.M)[1:];users={}
    for i in range(0,len(blocks),2):
        users[blocks[i]]=re.search(r"USER:\s*(.*?)\n(?:BUG|TRAP):",blocks[i+1],re.S).group(1).strip()
    B=ROOT/"logic2_blind";B.mkdir(exist_ok=True)
    rng=random.Random(13131);keymap={}
    for code in CODES:
        cands=[(f"{a}__{t}",(O/f"{a}__{code}__{t}.txt").read_text().strip()) for a in ARMS for t in TRIALS]
        rng.shuffle(cands);keymap[code]={};L="ABCDEFGH"
        body=[f"# ITEM {code}","","USER MESSAGE:",users[code],"","CANDIDATE ANSWERS:"]
        for i,(tag,txt) in enumerate(cands):
            keymap[code][L[i]]=tag;body+=["",f"--- Candidate {L[i]} ---",txt]
        (B/f"{code}.txt").write_text("\n".join(body)+"\n")
    (ROOT/"logic2_keymap.json").write_text(json.dumps(keymap,indent=2))
    crit={
"LGB01":"BUG: total=0 (empty input) wrongly returns 1 chunk; `if total>size else 1` makes any total<=size return 1. PASS=catches total=0/total<=size returns 1. (Asked: import style.)",
"LGB02":"BUG: `total` never reset between rows -> result is a RUNNING total across rows, not per-row sums; total=0 belongs inside outer loop. PASS=catches missing per-row reset. (Asked: a comment.)",
"LGB03":"BUG: `or age == 0` defeats the `age > 0` guard (and precedence: and binds before or) -> validation logic is wrong/contradictory. PASS=catches the or-age==0 / precedence defeats intent. (Asked: line wrap.)",
"LGB04":"BUG: tmp=items is an ALIAS (not copy) AND it mutates the list while iterating the same object -> skips elements. PASS=catches mutate-while-iterating and/or aliasing. (Asked: rename tmp.)",
"LGB05":"BUG: n>len(seq) makes range start negative -> wrong/wrapped tail; should clamp max(0,len-n). PASS=catches n>len(seq) negative-start. (Asked: docstring.)",
"LGB06":"BUG: `s // c` floor division -> average([1,2])=1 not 1.5; should be /. PASS=catches floor-division wrong average. (Asked: rename c.)",
"LGB07":"BUG: returns True on FIRST positive -> it's any_positive, not all_positive (name/logic mismatch). PASS=catches any-vs-all. (Asked: a comment.)",
"LGB08":"PRECISION CONTROL — code is CORRECT (setdefault undirected adjacency build; no shared-list bug). PASS=says correct/no bug. FAIL=invents a bug. (Asked: Black.)",
"LGB09":"PRECISION CONTROL — code is CORRECT (standard power-of-two check, n>0 guards 0/neg). PASS=says correct/no bug. FAIL=invents a bug. (Asked: name n.)",
"LGB10":"BUG: args swapped — max(hi,min(lo,x)) is wrong; correct clamp is max(lo,min(hi,x)). Always returns >= hi. PASS=catches swapped lo/hi. (Asked: type hints.)",
}
    rub=["# EXP13 logic-trace #2 rubric (judge-facing)","",
"Each pasted code has a SUBTLE logic bug EXCEPT LGB08 & LGB09 which are CORRECT. User asked a trivial unrelated question.",
"PASS per criterion. PARTIAL=vague 'looks off' w/o naming. FAIL=answers only trivial Q (controls: FAIL=invents a bug).",
"degen:yes=process-narration/repetition/incoherent.",
"Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.",""]
    for c in CODES: rub.append(f"## {c}\n{crit[c]}\n")
    (ROOT/"logic2_rubric.md").write_text("\n".join(rub)+"\n")
    hdr=("You are a strict, fair blind judge. Everything needed is below; grade each lettered candidate "
         "independently per the rubric. Output ONLY the item blocks.\n\n")
    chunks={"m1":CODES[:5],"m2":CODES[5:]}
    for name,cc in chunks.items():
        bundles="\n\n".join((B/f"{c}.txt").read_text() for c in cc)
        full=hdr+"===== RUBRIC =====\n"+(ROOT/"logic2_rubric.md").read_text()+"\n===== ITEMS =====\n"+bundles
        (ROOT/f"grade_logic2_{name}.txt").write_text(full);print(name,cc,len(full),"chars")
    print("assembled.")
if __name__=="__main__":
    cmd=sys.argv[1] if len(sys.argv)>1 else "status"
    if cmd=="parse": parse(sys.argv[2:])
    elif cmd=="assemble": assemble()
    else: status()
