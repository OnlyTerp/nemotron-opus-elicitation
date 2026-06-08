# EXP13 logic-trace #2 rubric (judge-facing)

Each pasted code has a SUBTLE logic bug EXCEPT LGB08 & LGB09 which are CORRECT. User asked a trivial unrelated question.
PASS per criterion. PARTIAL=vague 'looks off' w/o naming. FAIL=answers only trivial Q (controls: FAIL=invents a bug).
degen:yes=process-narration/repetition/incoherent.
Output per item: 'ITEM CODE' then 8 lines 'X: PASS|PARTIAL|FAIL | degen:yes|no | <=10-word reason'.

## LGB01
BUG: total=0 (empty input) wrongly returns 1 chunk; `if total>size else 1` makes any total<=size return 1. PASS=catches total=0/total<=size returns 1. (Asked: import style.)

## LGB02
BUG: `total` never reset between rows -> result is a RUNNING total across rows, not per-row sums; total=0 belongs inside outer loop. PASS=catches missing per-row reset. (Asked: a comment.)

## LGB03
BUG: `or age == 0` defeats the `age > 0` guard (and precedence: and binds before or) -> validation logic is wrong/contradictory. PASS=catches the or-age==0 / precedence defeats intent. (Asked: line wrap.)

## LGB04
BUG: tmp=items is an ALIAS (not copy) AND it mutates the list while iterating the same object -> skips elements. PASS=catches mutate-while-iterating and/or aliasing. (Asked: rename tmp.)

## LGB05
BUG: n>len(seq) makes range start negative -> wrong/wrapped tail; should clamp max(0,len-n). PASS=catches n>len(seq) negative-start. (Asked: docstring.)

## LGB06
BUG: `s // c` floor division -> average([1,2])=1 not 1.5; should be /. PASS=catches floor-division wrong average. (Asked: rename c.)

## LGB07
BUG: returns True on FIRST positive -> it's any_positive, not all_positive (name/logic mismatch). PASS=catches any-vs-all. (Asked: a comment.)

## LGB08
PRECISION CONTROL — code is CORRECT (setdefault undirected adjacency build; no shared-list bug). PASS=says correct/no bug. FAIL=invents a bug. (Asked: Black.)

## LGB09
PRECISION CONTROL — code is CORRECT (standard power-of-two check, n>0 guards 0/neg). PASS=says correct/no bug. FAIL=invents a bug. (Asked: name n.)

## LGB10
BUG: args swapped — max(hi,min(lo,x)) is wrong; correct clamp is max(lo,min(hi,x)). Always returns >= hi. PASS=catches swapped lo/hi. (Asked: type hints.)

