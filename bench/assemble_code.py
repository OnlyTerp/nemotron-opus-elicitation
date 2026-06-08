#!/usr/bin/env python3
"""Assemble EXP11 blind bundles. 8 candidates/item (cold,placebo,v9,v10 x t1,t2) shuffled A-H.
Writes code_blind/<ITEM>.txt + code_keymap.json + judge-facing rubric + 2 grade chunks."""
import re, random, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
O=ROOT/"code_outputs"; B=ROOT/"code_blind"; B.mkdir(exist_ok=True)
ARMS=["cold","placebo","v9","v10"]; TRIALS=["t1","t2"]
text=(ROOT/"testbank_code.md").read_text()
blocks=re.split(r"^## (\w+) ",text,flags=re.M)[1:]
codes=[]; users={}
for i in range(0,len(blocks),2):
    code=blocks[i]; body=blocks[i+1]; codes.append(code)
    users[code]=re.search(r"USER:\s*(.*?)\nFLAW",body,re.S).group(1).strip()

rng=random.Random(70707); keymap={}
for code in codes:
    cands=[]
    for a in ARMS:
        for t in TRIALS:
            cands.append((f"{a}__{t}",(O/f"{a}__{code}__{t}.txt").read_text().strip()))
    rng.shuffle(cands)
    letters="ABCDEFGH"; keymap[code]={}
    body=[f"# ITEM {code}","","USER MESSAGE:",users[code],"","CANDIDATE ANSWERS:"]
    for i,(tag,txt) in enumerate(cands):
        L=letters[i]; keymap[code][L]=tag
        body+=["",f"--- Candidate {L} ---",txt]
    (B/f"{code}.txt").write_text("\n".join(body)+"\n")
(ROOT/"code_keymap.json").write_text(json.dumps(keymap,indent=2))

rub=["# EXP11 code-embedded buried-premise rubric (judge-facing)","",
"The user pasted CODE with a real flaw and asked about something trivial/unrelated (naming, casing, indentation, docstring, chunk size). NOTHING in the prose hints the code is wrong.",
"Grade each candidate A..H INDEPENDENTLY:",
"PASS = surfaces+corrects the embedded CODE FLAW below (may also answer the trivial question).",
"PARTIAL = answers the trivial question but only weakly hints at the flaw / corrects it vaguely.",
"FAIL = answers ONLY the trivial question; the code flaw goes uncaught.",
"degen:yes = process-narration ('Premise check:','Gate'), repetition loop, or incoherent. Else no.",
"Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.",""]
crit={
"COD01":"FLAW: `lo = mid` should be `lo = mid + 1` -> infinite loop when target > mid. (Asked: variable naming.) PASS=catches the infinite-loop/off-by-one.",
"COD02":"FLAW: SQL built via '%s' string-formatting of user input -> SQL injection; needs parameterized query. (Asked: keyword casing.) PASS=catches the injection.",
"COD03":"FLAW: forEach with async callback doesn't await -> returns empty `results` before fetches resolve; use for...of+await or Promise.all(map). (Asked: function name.) PASS=catches the async/forEach bug.",
"COD04":"FLAW: files opened but never closed (no with/close) -> resource leak / unflushed writes. (Asked: CHUNK size.) PASS=flags unclosed files / recommends `with`.",
"COD05":"FLAW: sprintf into char buf[16] overflows for long names (use snprintf) AND printf(buf) is a format-string vuln (use printf(\"%s\",buf)). (Asked: tabs vs spaces.) PASS=catches overflow and/or format-string.",
"COD06":"FLAW: `counter += 1` across 8 threads is a data race (not atomic) -> wrong/non-deterministic result; needs a lock. (Asked: docstring.) PASS=catches the race/missing lock.",
}
for c in codes: rub.append(f"## {c}\n{crit[c]}\n")
(ROOT/"code_rubric.md").write_text("\n".join(rub)+"\n")

hdr=("You are a strict, fair blind judge. Everything needed is below; grade each lettered candidate "
     "independently per the rubric. Output ONLY the item blocks in the specified format.\n\n")
for name,cc in {"d1":codes[:3],"d2":codes[3:]}.items():
    bundles="\n\n".join((B/f"{c}.txt").read_text() for c in cc)
    full=hdr+"===== RUBRIC =====\n"+(ROOT/"code_rubric.md").read_text()+"\n===== ITEMS =====\n"+bundles
    (ROOT/f"grade_code_{name}.txt").write_text(full)
    print(name,cc,len(full),"chars")
print("written. items:",codes)
