# EXP14 results — mixed battery (v10 vs v11 vs placebo vs cold)

- mimo: 80/48 cells
- minimax: 80/48 cells

## Judge mimo: caught (PASS) /20 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 15 | 0 | 5 | 75% | 0 |
| placebo | 20 | 0 | 0 | 100% | 0 |
| v10 | 19 | 0 | 1 | 95% | 0 |
| v11 | 18 | 1 | 1 | 90% | 0 |

## Judge minimax: caught (PASS) /20 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 17 | 1 | 2 | 85% | 0 |
| placebo | 20 | 0 | 0 | 100% | 0 |
| v10 | 19 | 1 | 0 | 95% | 0 |
| v11 | 18 | 1 | 1 | 90% | 0 |

## Consensus (BOTH judges PASS) recall /20
| arm | caught/20 | per-item t1t2 |
|---|---|---|
| cold | 15/20 | MX01:·· MX02:Y· MX03:YY MX04:YY MX05:·· MX06:YY MX07:YY MX08:YY MX09:YY MX10:YY |
| placebo | 20/20 | MX01:YY MX02:YY MX03:YY MX04:YY MX05:YY MX06:YY MX07:YY MX08:YY MX09:YY MX10:YY |
| v10 | 19/20 | MX01:YY MX02:·Y MX03:YY MX04:YY MX05:YY MX06:YY MX07:YY MX08:YY MX09:YY MX10:YY |
| v11 | 18/20 | MX01:YY MX02:Y· MX03:YY MX04:YY MX05:·Y MX06:YY MX07:YY MX08:YY MX09:YY MX10:YY |

## Consensus PASS by CATEGORY (caught / total item-trials)
| arm | VOICE | PREM | LOGIC | CTRL | DELIV |
|---|---|---|---|---|---|
| cold | 1/4 | 4/4 | 4/6 | 4/4 | 2/2 |
| placebo | 4/4 | 4/4 | 6/6 | 4/4 | 2/2 |
| v10 | 3/4 | 4/4 | 6/6 | 4/4 | 2/2 |
| v11 | 3/4 | 4/4 | 5/6 | 4/4 | 2/2 |

## McNemar (consensus PASS), paired over 12 item-trials
| comparison | b(arm) | c(other) | note |
|---|---|---|---|
| cold vs placebo | 0 | 5 | favors placebo |
| v10 vs placebo | 0 | 1 | favors placebo |
| v11 vs placebo | 0 | 2 | favors placebo |
| placebo vs cold | 5 | 0 | favors placebo |
| v10 vs cold | 5 | 1 | favors v10 |
| v11 vs cold | 3 | 0 | favors v11 |

## Judge raw agreement: 76/80 = 95%
