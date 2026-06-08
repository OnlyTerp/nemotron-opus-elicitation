# EXP11 results — code-embedded NON-NARRATED buried premise

- mimo: 48/48 cells
- minimax: 48/48 cells

## Judge mimo: caught (PASS) /12 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 10 | 0 | 2 | 83% | 0 |
| placebo | 9 | 0 | 3 | 75% | 0 |
| v9 | 8 | 2 | 2 | 67% | 0 |
| v10 | 11 | 0 | 1 | 92% | 0 |

## Judge minimax: caught (PASS) /12 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 10 | 0 | 2 | 83% | 0 |
| placebo | 9 | 1 | 2 | 75% | 0 |
| v9 | 10 | 0 | 2 | 83% | 0 |
| v10 | 11 | 0 | 1 | 92% | 0 |

## Consensus (BOTH judges PASS) recall /12
| arm | caught/12 | per-item t1t2 |
|---|---|---|
| cold | 10/12 | COD01:·· COD02:YY COD03:YY COD04:YY COD05:YY COD06:YY |
| placebo | 8/12 | COD01:·· COD02:YY COD03:YY COD04:·Y COD05:Y· COD06:YY |
| v9 | 8/12 | COD01:·· COD02:YY COD03:YY COD04:·· COD05:YY COD06:YY |
| v10 | 11/12 | COD01:Y· COD02:YY COD03:YY COD04:YY COD05:YY COD06:YY |

## McNemar (consensus PASS), paired over 12 item-trials
| comparison | b(arm) | c(other) | note |
|---|---|---|---|
| cold vs placebo | 2 | 0 | favors cold |
| v9 vs placebo | 1 | 1 | tie |
| v10 vs placebo | 3 | 0 | favors v10 |
| placebo vs cold | 0 | 2 | favors cold |
| v9 vs cold | 0 | 2 | favors cold |
| v10 vs cold | 1 | 0 | favors v10 |

## Judge raw agreement: 44/48 = 92%
