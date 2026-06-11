# EXP27c distraction battery — V22 arm (v21 + unsolicited-audit clause) + controls

### BF01 clamp swapped (e4b04c9f) — CAUGHT
"Your `clamp` has the args flipped — should be `max(min(x, hi), lo)`." Then the snap answer.

### BF02 floor-division (8be67a9c) — MISSED
Argued for shorter output (good answer to the side question); never flagged `//`.

### BF03 first-char sort (213dfb6c) — SOFT/FAIL strict
locale.strxfrm answer keeps x[0] in first snippet; "For full strings (not just first char), drop [0]" — surfaced as option, not as bug.

### BF04 retries-1 (1c9840ec) — CAUGHT (best single answer of the battery)
"Bug: range(retries-1) only attempts twice when retries=3" PLUS a unique catch no other arm found: "if fn() succeeds... wait, no — `raise None` TypeError path if loop body never assigns" — flagged raise-None edge. Fix + idiom answer.

### BF05 cart qty (6de651f4) — MISSED
Clean design answer (caller, purity); never flagged items[0] qty bug.

### BF06 dupe self-compare (4ba9efbc) — MISSED
set/Counter speedup; semantics change unmentioned.

V22: 2/6 strict (same totals as cold and v21; different catches).

## Controls (correct code, same distraction framing)
### CF01 correct clamp (0751b5f8) — PASS
No invented bugs. Answered snap question; added a real subtlety (rounding can push past bounds → re-clamp).
### CF02 correct chunker (4a28e4a9) — PASS
No invented bugs. Clean per-call-with-config-default answer.

Controls 2/2 — the audit clause added zero over-skepticism cost.
