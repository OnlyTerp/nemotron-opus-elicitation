# EXP20 REASONING-VERIFY bank — non-code word problems checkable by back-substitution

The test of whether "verify your answer against the problem's constraints" generalizes the capability lever beyond code. Each problem has a SEDUCTIVE wrong answer (the fast intuitive one) and a correct answer that back-substitution into the stated constraints confirms. No code — pure arithmetic/logic reasoning. The model is NOT asked to verify; the template arm's disposition is what should trigger it.

Success (PASS) = states the correct answer (back-sub-consistent). FAIL = the seductive wrong answer. PARTIAL = sets up correctly but arithmetic slip to a third value.

---

## RZ01 (bat and ball — classic CRT)
USER: A bat and a ball cost $1.10 in total. The bat costs $1.00 more than the ball. How much does the ball cost? Give just the amount.
SEDUCTIVE WRONG: $0.10. CORRECT: $0.05 (ball 0.05, bat 1.05, diff 1.00, total 1.10). Back-sub: 0.10 ball → bat 1.10 → total 1.20 ≠ 1.10, so 0.10 is wrong. PASS=$0.05.

## RZ02 (widgets — CRT)
USER: If 5 machines take 5 minutes to make 5 widgets, how long do 100 machines take to make 100 widgets? Answer in minutes.
SEDUCTIVE WRONG: 100. CORRECT: 5 (each machine makes 1 widget in 5 min; 100 machines make 100 in 5). PASS=5.

## RZ03 (lily pad — CRT)
USER: A patch of lily pads doubles in size every day. It takes 48 days to cover the whole lake. How many days to cover half the lake?
SEDUCTIVE WRONG: 24. CORRECT: 47 (doubles each day, so half the day before full). PASS=47.

## RZ04 (fresh-parameterized bat/ball — not the famous numbers)
USER: A laptop and a case cost $540 in total. The laptop costs $500 more than the case. How much does the case cost? Just the amount.
SEDUCTIVE WRONG: $40. CORRECT: $20 (case 20, laptop 520, diff 500, total 540). Back-sub: 40 → laptop 540 → total 580 ≠ 540. PASS=$20.

## RZ05 (fresh widgets parameterization)
USER: If 8 painters paint 8 fences in 8 hours, how many hours for 40 painters to paint 40 fences?
SEDUCTIVE WRONG: 40. CORRECT: 8. PASS=8.

## RZ06 (overlapping sets — seductive subtract)
USER: In a class of 30, 18 play soccer and 15 play basketball. Every student plays at least one. How many play both?
SEDUCTIVE WRONG: 3 (or "can't tell"). CORRECT: 18+15-30 = 3. Actually back-sub: both=3 → only-soccer 15, only-basket 12, both 3 → total 30 ✓. PASS=3. (Here seductive and correct coincide via inclusion-exclusion; FAIL = says can't determine, or wrong number.)

## RZ07 (percentage trap)
USER: A shirt is discounted 20%, then the sale price is increased by 20%. Is the final price higher than, lower than, or equal to the original? By what percent?
SEDUCTIVE WRONG: equal. CORRECT: lower, by 4% (×0.8×1.2 = 0.96). Back-sub with $100: 100→80→96. PASS=lower by 4%.

## RZ08 (compound days off-by-one)
USER: A snail climbs 3 ft up a well each day and slips 2 ft back each night. The well is 10 ft deep. How many days to climb out?
SEDUCTIVE WRONG: 10. CORRECT: 8 (net 1 ft/day, but on day 8 it climbs from 7 to 10 and is out before slipping). Back-sub: end of day 7 at 7 ft; day 8 climbs 3 → 10, out. PASS=8.

## RZ09 (CLEAN/easy control — no trap, just arithmetic)
USER: A book costs $12 and you buy 3 of them. What's the total? Just the amount.
TRUTH: $36, no trap. PASS=$36. (Control: verify shouldn't break easy correct answers.)

## RZ10 (CLEAN control — straightforward)
USER: A train travels 60 miles in 1 hour. At the same speed, how far in 2.5 hours? Just the distance.
TRUTH: 150 miles, no trap. PASS=150 miles. (Control.)
