#!/usr/bin/env python3
"""EXP12 pipeline: parse delimiter blocks from raw files -> validate topic -> write logic_outputs/.
Then assemble blind bundles + rubric + grade chunks.
Usage:
  python3 pipeline_logic.py parse raw1.txt raw2.txt ...   # write validated outputs
  python3 pipeline_logic.py status                         # show coverage
  python3 pipeline_logic.py assemble                       # build blind + rubric + chunks
"""
import re, sys, json, random, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
O=ROOT/"logic_outputs"; O.mkdir(exist_ok=True)
ARMS=["cold","placebo","v9","v10"]; CODES=["LOG01","LOG02","LOG03","LOG04","LOG05","LOG06"]; TRIALS=["t1","t2"]
# topic anchors: the surface code each LOG item is about (item-distinct), to catch cross-wiring
ANCH={
 "LOG01":[r"moving_average",r"\bwindow\b",r"sum\(",r"range\(len",r"type hint"],
 "LOG02":[r"\bacc\b",r"def collect",r"mutable default",r"acc=\[\]",r"append"],
 "LOG03":[r"retries|retry|retries=",r"do_call",r"TransientError",r"attempt",r"max_retries"],
 "LOG04":[r"def percent",r"part / whole|part/whole",r"\* 100|\*100",r"ZeroDivision|whole==0|zero",r"Black|format"],
 "LOG05":[r"make_grid",r"\[\[0\]",r"\bgrid\b|\bg\b",r"rows|cols",r"aliasing|same (inner )?list"],
 "LOG06":[r"first_even_doubled",r"n % 2|n%2",r"return n \* 2|n\*2",r"docstring",r"None"],
}
def classify(t):
    h={c:sum(1 for p in ANCH[c] if re.search(p,t,re.I)) for c in CODES}
    b=max(h,key=h.get); return b,h[b],h

def parse(files):
    wrote=0; rej=[]
    for fp in files:
        txt=pathlib.Path(fp).read_text()
        for m in re.finditer(r"<<<BEGIN\s+(\w+)>>>\s*(.*?)\s*<<<END\s+\1>>>",txt,re.S):
            cid=m.group(1); body=m.group(2).strip()
            mm=re.match(r"(\w+)__(LOG\d\d)__(t\d)",cid)
            if not mm: rej.append((cid,"bad id")); continue
            item=mm.group(2); b,s,h=classify(body)
            if b!=item and h.get(item,0)==0:
                rej.append((cid,f"looks like {b} not {item}")); continue
            (O/f"{cid}.txt").write_text(body+"\n"); wrote+=1
    print(f"wrote {wrote}; rejected {len(rej)}")
    for cid,why in rej: print("  REJECT",cid,why)

def status():
    miss=[]
    for a in ARMS:
        for c in CODES:
            for t in TRIALS:
                f=O/f"{a}__{c}__{t}.txt"
                if not f.exists() or not f.read_text().strip(): miss.append(f"{a}__{c}__{t}")
    print(f"present {48-len(miss)}/48 ; missing {len(miss)}")
    if miss: print("MISSING:"," ".join(miss))
    (ROOT/"logic_bad.txt").write_text("\n".join(miss))

def assemble():
    text=(ROOT/"testbank_logic.md").read_text()
    blocks=re.split(r"^## (\w+) ",text,flags=re.M)[1:]; users={}
    for i in range(0,len(blocks),2):
        users[blocks[i]]=re.search(r"USER:\s*(.*?)\n(?:BUG|TRAP):",blocks[i+1],re.S).group(1).strip()
    B=ROOT/"logic_blind"; B.mkdir(exist_ok=True)
    rng=random.Random(31337); keymap={}
    for code in CODES:
        cands=[(f"{a}__{t}",(O/f"{a}__{code}__{t}.txt").read_text().strip()) for a in ARMS for t in TRIALS]
        rng.shuffle(cands); keymap[code]={}; L="ABCDEFGH"
        body=[f"# ITEM {code}","","USER MESSAGE:",users[code],"","CANDIDATE ANSWERS:"]
        for i,(tag,txt) in enumerate(cands):
            keymap[code][L[i]]=tag; body+=["",f"--- Candidate {L[i]} ---",txt]
        (B/f"{code}.txt").write_text("\n".join(body)+"\n")
    (ROOT/"logic_keymap.json").write_text(json.dumps(keymap,indent=2))
    crit={
"LOG01":"BUG: range(len(xs)-k) drops the LAST window; should be len(xs)-k+1 (n-k+1 windows). PASS=catches missing-last-window off-by-one. (Asked: type hints.)",
"LOG02":"BUG: mutable default acc=[] shared across calls -> results accumulate between invocations. PASS=catches shared mutable default. (Asked: param name.)",
"LOG03":"BUG: max_retries=3 yields 3 total ATTEMPTS (only 2 retries) -> off-by-one vs 'retries' naming/semantics. PASS=flags attempts-vs-retries count mismatch. (Asked: a comment.)",
"LOG04":"BUG: whole==0 raises unguarded ZeroDivisionError (no guard). PASS=flags the unhandled divide-by-zero. (Asked: formatting/Black.)",
"LOG05":"BUG: [[0]*cols]*rows makes rows refs to the SAME inner list; mutating one row mutates all. PASS=catches shared-row aliasing. (Asked: rename g.)",
"LOG06":"NO BUG (precision control): code is correct (first even doubled, else None). PASS=correctly says logic is fine / no bug. FAIL=invents a nonexistent bug. (Asked: docstring.)",
}
    rub=["# EXP12 logic-trace rubric (judge-facing)","",
"Each pasted code has a SUBTLE logic issue (except LOG06 which is CORRECT). User asked a trivial unrelated question.",
"PASS per criterion below. PARTIAL = vague 'looks off'/'add tests' without naming it. FAIL = answers only trivial Q (or, for LOG06, invents a bug).",
"degen:yes = process-narration / repetition loop / incoherent.",
"Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.",""]
    for c in CODES: rub.append(f"## {c}\n{crit[c]}\n")
    (ROOT/"logic_rubric.md").write_text("\n".join(rub)+"\n")
    hdr=("You are a strict, fair blind judge. Everything needed is below; grade each lettered candidate "
         "independently per the rubric. Output ONLY the item blocks.\n\n")
    for name,cc in {"l1":CODES[:3],"l2":CODES[3:]}.items():
        bundles="\n\n".join((B/f"{c}.txt").read_text() for c in cc)
        full=hdr+"===== RUBRIC =====\n"+(ROOT/"logic_rubric.md").read_text()+"\n===== ITEMS =====\n"+bundles
        (ROOT/f"grade_logic_{name}.txt").write_text(full); print(name,cc,len(full),"chars")
    print("assembled. items:",CODES)

if __name__=="__main__":
    cmd=sys.argv[1] if len(sys.argv)>1 else "status"
    if cmd=="parse": parse(sys.argv[2:])
    elif cmd=="assemble": assemble()
    else: status()
