# EXP12 results — logic-trace traps

- mimo: 48/48 cells
- minimax: 48/48 cells

## Judge mimo: caught (PASS) /12 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 5 | 0 | 7 | 42% | 0 |
| placebo | 5 | 0 | 7 | 42% | 0 |
| v9 | 8 | 0 | 4 | 67% | 0 |
| v10 | 7 | 0 | 5 | 58% | 0 |

## Judge minimax: caught (PASS) /12 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 5 | 0 | 7 | 42% | 0 |
| placebo | 5 | 0 | 7 | 42% | 0 |
| v9 | 8 | 0 | 4 | 67% | 0 |
| v10 | 7 | 0 | 5 | 58% | 0 |

## Consensus (BOTH judges PASS) recall /12
| arm | caught/12 | per-item t1t2 |
|---|---|---|
| cold | 5/12 | LOG01:·· LOG02:Y· LOG03:·· LOG04:·· LOG05:YY LOG06:YY |
| placebo | 5/12 | LOG01:·· LOG02:YY LOG03:·· LOG04:·· LOG05:Y· LOG06:YY |
| v9 | 8/12 | LOG01:YY LOG02:YY LOG03:·· LOG04:·· LOG05:YY LOG06:YY |
| v10 | 7/12 | LOG01:·Y LOG02:YY LOG03:·· LOG04:·· LOG05:YY LOG06:YY |

## McNemar (consensus PASS), paired over 12 item-trials
| comparison | b(arm) | c(other) | note |
|---|---|---|---|
| cold vs placebo | 1 | 1 | tie |
| v9 vs placebo | 3 | 0 | favors v9 |
| v10 vs placebo | 2 | 0 | favors v10 |
| placebo vs cold | 1 | 1 | tie |
| v9 vs cold | 3 | 0 | favors v9 |
| v10 vs cold | 2 | 0 | favors v10 |

## Judge raw agreement: 48/48 = 100%
