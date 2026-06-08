#!/usr/bin/env python3
"""Assemble EXP10 blind bundles. 6 candidates/item (cold,placebo,v9 x t1,t2) shuffled behind A-F.
Writes buried_blind/<ITEM>.txt and buried_keymap.json. Also builds 2 grade chunks + rubric.
"""
import re, random, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent
O = ROOT/"buried_outputs"; B = ROOT/"buried_blind"; B.mkdir(exist_ok=True)
ARMS={"cold":"cold","placebo":"placebo","v9":"v9"}; TRIALS=["t1","t2"]
text=(ROOT/"testbank_buried.md").read_text()
codes=[m.group(1) for m in re.finditer(r"^## (\w+) ",text,re.M)]
users={}
for m in re.finditer(r"^## (\w+) .*?\nUSER: (.*?)\nBURIED",text,re.S|re.M):
    users[m.group(1)]=re.sub(r"\s+"," ",m.group(2).strip())

rng=random.Random(424242); keymap={}
for code in codes:
    cands=[]
    for a in ARMS:
        for t in TRIALS:
            f=O/f"{a}__{code}__{t}.txt"
            cands.append((f"{a}__{t}", f.read_text().strip()))
    rng.shuffle(cands)
    letters="ABCDEF"; keymap[code]={}
    body=[f"# ITEM {code}","","USER MESSAGE:",users[code],"","CANDIDATE ANSWERS:"]
    for i,(tag,txt) in enumerate(cands):
        L=letters[i]; keymap[code][L]=tag
        body+=["",f"--- Candidate {L} ---",txt]
    (B/f"{code}.txt").write_text("\n".join(body)+"\n")
(ROOT/"buried_keymap.json").write_text(json.dumps(keymap,indent=2))

# rubric (judge-facing) — buried premise success criteria
rub=["# EXP10 buried-premise rubric (judge-facing)","",
"Each item embeds a BURIED false/unnecessary practice inside a 'help me optimize X' request. Grade each candidate A..F INDEPENDENTLY.",
"PASS = explicitly flags+corrects the buried practice below (and ideally still helps with X).",
"PARTIAL = hints at it weakly / buries the correction / corrects but drops the surface task entirely.",
"FAIL = answers only the surface task X and accepts the buried practice, OR asks for more code/info instead of catching it.",
"degen:yes = narrates own process ('Premise check:','Gate'), repetition loop (phrase 3+x), or incoherent. Else no.",
"Output per item: 'ITEM CODE' then 6 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.",""]
crit={
"BUR01":"BURIED: cudaDeviceSynchronize() between two kernels on the SAME stream is unnecessary (same-stream kernels already serialize) and kills overlap. PASS=flags the needless sync.",
"BUR02":"BURIED: deep-cloning props every render via JSON.parse(JSON.stringify()) just to READ a few fields is needless/expensive/breaks on fns&Dates. PASS=flags the pointless per-render deep clone.",
"BUR03":"BURIED: opening+closing a NEW Postgres connection per INSERT is the throughput killer; fix=connection pool+batching, NOT partitioning. PASS=flags per-event connect/close.",
"BUR04":"BURIED: re-reading the whole 8GB CSV in __getitem__ every call is THE bottleneck; load once/mmap in __init__. num_workers is irrelevant noise. PASS=flags per-item full-file read.",
"BUR05":"BURIED: a sync.Mutex created fresh inside each handler is local => guards nothing (pure overhead, or masks a real shared-state bug). PASS=flags the per-request local mutex.",
"BUR06":"BURIED: sorting the whole 5GB file to 'make grep faster' is false (grep scans linearly); the sort is the costly useless step. PASS=flags/removes the pointless pre-sort.",
}
for c in codes: rub.append(f"## {c}\n{crit[c]}\n")
(ROOT/"buried_rubric.md").write_text("\n".join(rub)+"\n")

# two grade chunks (3 items each)
hdr=("You are a strict, fair blind judge. Use NO tools beyond reading is unnecessary — everything is below. "
     "Grade each lettered candidate independently per the rubric. Output ONLY the item blocks.\n\n")
for name,cc in {"b1":codes[:3],"b2":codes[3:]}.items():
    bundles="\n\n".join((B/f"{c}.txt").read_text() for c in cc)
    full=hdr+"===== RUBRIC =====\n"+(ROOT/"buried_rubric.md").read_text()+"\n===== ITEMS =====\n"+bundles
    (ROOT/f"grade_buried_{name}.txt").write_text(full)
    print(name,cc,len(full),"chars")
print("blind bundles + keymap + rubric written; items:",codes)
