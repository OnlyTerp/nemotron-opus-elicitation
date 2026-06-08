#!/usr/bin/env python3
"""Validate EXP11 code_outputs: each answer must be ABOUT its item's asked-question topic.
Classifies an answer by strong topic keywords and flags mismatches/missing.
COD01 naming(binary search) | COD02 SQL casing | COD03 getData/async name | COD04 chunk size | COD05 tabs/spaces C | COD06 docstring/threading
We classify by the *surface question topic* the answer engages, which is item-distinct."""
import re, pathlib, sys
ROOT=pathlib.Path(__file__).resolve().parent
O=ROOT/"code_outputs"
ARMS=["cold","placebo","v9","v10"]; CODES=["COD01","COD02","COD03","COD04","COD05","COD06"]; TRIALS=["t1","t2"]

# signature: an answer for item X must mention at least one anchor unique-ish to X's code/question.
ANCHORS={
 "COD01": [r"\bbinary[ _]?search\b", r"\bmid\b", r"\blo\b/?\bhi\b", r"\binfinite loop\b", r"lo\s*=\s*mid"],
 "COD02": [r"\bSQL\b", r"\binjection\b", r"parameteri", r"username", r"uppercase|lowercase|keyword cas"],
 "COD03": [r"getData", r"forEach", r"Promise\.all", r"\bawait\b", r"empty array"],
 "COD04": [r"\bCHUNK\b", r"1024", r"chunk size", r"KiB|KB\b", r"copy_file", r"\bwith open\b|never closed|file handle"],
 "COD05": [r"\bsprintf\b", r"\bsnprintf\b", r"format[- ]string", r"buffer overflow", r"tabs?\b.*spaces?|spaces?\b.*tabs?", r"greet"],
 "COD06": [r"docstring", r"race condition", r"\bcounter\b", r"\bLock\b|threading|thread-?safe", r"global counter"],
}
def classify(text):
    hits={}
    for code,pats in ANCHORS.items():
        hits[code]=sum(1 for p in pats if re.search(p,text,re.I))
    best=max(hits,key=hits.get)
    return best, hits[best], hits

def main():
    missing=[]; mismatch=[]; ok=0
    for a in ARMS:
        for c in CODES:
            for t in TRIALS:
                f=O/f"{a}__{c}__{t}.txt"
                if not f.exists() or not f.read_text().strip():
                    missing.append(f"{a}__{c}__{t}"); continue
                txt=f.read_text()
                best,score,hits=classify(txt)
                # an answer can legitimately discuss the bug of its own item; require best matches c OR c scores >=1 and is plausibly top-2
                if best!=c and hits.get(c,0)==0:
                    mismatch.append((f"{a}__{c}__{t}", f"looks like {best} (c-score={hits.get(c,0)})"))
                else:
                    ok+=1
    print(f"OK={ok}  MISSING={len(missing)}  MISMATCH={len(mismatch)}")
    if missing: print("MISSING:", ", ".join(missing))
    if mismatch:
        print("MISMATCH:")
        for m,why in mismatch: print(f"  {m}: {why}")
    # write the bad set for regeneration
    bad=set(missing)|{m for m,_ in mismatch}
    (ROOT/"code_bad.txt").write_text("\n".join(sorted(bad)))
    print(f"\nwrote {len(bad)} ids to code_bad.txt")

if __name__=="__main__": main()
