#!/usr/bin/env python3
"""Auto-grade EXP20 reasoning by checking the correct answer appears (and seductive-wrong is rejected)."""
import re, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
O=ROOT/"reason_outputs"
ARMS=["cold","v13","v14"]; CODES=[f"RZ{n:02d}" for n in range(1,11)]; TRIALS=["t1","t2"]
# (correct regex, seductive-wrong regex or None). PASS = correct present AND not ending on seductive.
KEY={
 "RZ01":(r"\$?0\.05\b|5 cents|five cents", r"\$?0\.10\b|10 cents"),
 "RZ02":(r"\b5\b\s*(min|minutes)?", r"\b100\b\s*min"),
 "RZ03":(r"\b47\b", r"\b24\b"),
 "RZ04":(r"\$?20\b", r"\$?40\b"),
 "RZ05":(r"\b8\b\s*(hour|hours|hrs)?", r"\b40\b\s*hour"),
 "RZ06":(r"\b3\b", None),
 "RZ07":(r"lower.*\b4\s*%|\b4\s*%.*lower|0\.96|96\b", r"\bequal\b"),
 "RZ08":(r"\b8\b\s*(day|days)?", r"\b10\b\s*day"),
 "RZ09":(r"\$?36\b", None),
 "RZ10":(r"\b150\b", None),
}
def verdict(code, txt):
    correct, wrong = KEY[code]
    t=txt.lower()
    has_c = re.search(correct, t, re.I) is not None
    has_w = wrong and re.search(wrong, t, re.I) is not None
    # final answer heuristic: last 60 chars
    tail = t[-80:]
    if has_c and not (wrong and re.search(wrong, tail, re.I) and not re.search(correct, tail, re.I)):
        return "PASS"
    if has_w and not has_c:
        return "FAIL"
    return "PARTIAL" if has_c else "FAIL"
def main():
    import collections
    res=collections.defaultdict(lambda:collections.defaultdict(dict))
    miss=[]
    for a in ARMS:
        for c in CODES:
            for t in TRIALS:
                f=O/f"{a}__{c}__{t}.txt"
                if not f.exists() or not f.read_text().strip(): miss.append(f"{a}__{c}__{t}"); continue
                res[a][c][t]=verdict(c, f.read_text())
    print("missing:", miss or "none")
    BUG=CODES[:8]; CTRL=CODES[8:]
    print("\n=== EXP20 auto-graded recall ===")
    print(f"{'arm':6} {'TRAP /16':10} {'CONTROL /4':10}  per-trap")
    for a in ARMS:
        trap=sum(res[a].get(c,{}).get(t)=="PASS" for c in BUG for t in TRIALS)
        ctrl=sum(res[a].get(c,{}).get(t)=="PASS" for c in CTRL for t in TRIALS)
        detail=" ".join(f"{c}:{''.join({'PASS':'Y','PARTIAL':'~','FAIL':'.'}.get(res[a].get(c,{}).get(t,'.'),'?') for t in TRIALS)}" for c in BUG)
        print(f"{a:6} {trap}/16{'':6} {ctrl}/4{'':6}  {detail}")
if __name__=="__main__": main()
