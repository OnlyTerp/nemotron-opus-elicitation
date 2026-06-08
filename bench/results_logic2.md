# EXP13 results — logic-trace #2 (replication, 10 items)

- mimo: 80/48 cells
- minimax: 80/48 cells

## Judge mimo: caught (PASS) /20 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 9 | 3 | 8 | 45% | 0 |
| placebo | 12 | 3 | 5 | 60% | 0 |
| v9 | 12 | 3 | 5 | 60% | 0 |
| v10 | 12 | 3 | 5 | 60% | 0 |

## Judge minimax: caught (PASS) /20 per arm
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 13 | 0 | 7 | 65% | 0 |
| placebo | 16 | 0 | 4 | 80% | 0 |
| v9 | 15 | 0 | 5 | 75% | 0 |
| v10 | 15 | 1 | 4 | 75% | 0 |

## Consensus (BOTH judges PASS) recall /20
| arm | caught/20 | per-item t1t2 |
|---|---|---|
| cold | 9/20 | LGB01:·· LGB02:·· LGB03:·· LGB04:YY LGB05:·· LGB06:·· LGB07:YY LGB08:YY LGB09:YY LGB10:·Y |
| placebo | 12/20 | LGB01:·· LGB02:YY LGB03:·· LGB04:YY LGB05:·Y LGB06:·· LGB07:YY LGB08:Y· LGB09:YY LGB10:YY |
| v9 | 12/20 | LGB01:·· LGB02:YY LGB03:·· LGB04:YY LGB05:·Y LGB06:·· LGB07:YY LGB08:Y· LGB09:YY LGB10:YY |
| v10 | 12/20 | LGB01:·· LGB02:·Y LGB03:Y· LGB04:·Y LGB05:Y· LGB06:·· LGB07:YY LGB08:YY LGB09:YY LGB10:YY |

## McNemar (consensus PASS), paired over 12 item-trials
| comparison | b(arm) | c(other) | note |
|---|---|---|---|
| cold vs placebo | 1 | 4 | favors placebo |
| v9 vs placebo | 0 | 0 | tie |
| v10 vs placebo | 3 | 3 | tie |
| placebo vs cold | 4 | 1 | favors placebo |
| v9 vs cold | 4 | 1 | favors v9 |
| v10 vs cold | 4 | 1 | favors v10 |

## Judge raw agreement: 64/80 = 80%
