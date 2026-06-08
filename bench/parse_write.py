#!/usr/bin/env python3
"""Parse <<<BEGIN id>>> ... <<<END id>>> blocks from raw files and write each to
code_outputs/<id>.txt ONLY if the content's topic matches the item (anti cross-wire guard).
Usage: python3 parse_write.py raw_g2.txt [more_raw...]"""
import re, sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
O=ROOT/"code_outputs"
from validate_code import classify  # reuse anchors

def main(files):
    wrote=0; rejected=[]
    for fp in files:
        txt=pathlib.Path(fp).read_text()
        for m in re.finditer(r"<<<BEGIN\s+(\w+)>>>\s*(.*?)\s*<<<END\s+\1>>>", txt, re.S):
            cid=m.group(1); body=m.group(2).strip()
            mm=re.match(r"(\w+)__(COD\d\d)__(t\d)", cid)
            if not mm:
                rejected.append((cid,"bad id")); continue
            item=mm.group(2)
            best,score,hits=classify(body)
            if best!=item and hits.get(item,0)==0:
                rejected.append((cid, f"content looks like {best}, not {item}")); continue
            (O/f"{cid}.txt").write_text(body+"\n"); wrote+=1
    print(f"wrote {wrote}; rejected {len(rejected)}")
    for cid,why in rejected: print("  REJECT",cid,why)

if __name__=="__main__":
    main(sys.argv[1:] or ["raw_g2.txt"])
