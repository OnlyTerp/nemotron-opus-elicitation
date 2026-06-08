# EXP17 results — CEILING (does execution break the prompt-only ceiling?)

- mimo: 64/64 cells
- minimax: 64/64 cells

## Consensus (BOTH judges PASS)
| arm | BUG recall /10 | CONTROL precision /6 | per-bug-item (t1t2) |
|---|---|---|---|
| cold | 2/10 | 6/6 | 01:·· 02:·· 03:·· 04:YY 05:·· |
| v11 | 8/10 | 6/6 | 01:Y· 02:YY 03:Y· 04:YY 05:YY |
| v12 | 10/10 | 6/6 | 01:YY 02:YY 03:YY 04:YY 05:YY |
| v12tool | 10/10 | 6/6 | 01:YY 02:YY 03:YY 04:YY 05:YY |

### Judge mimo: BUG PASS /10 per arm
- cold:2/10 | v11:8/10 | v12:10/10 | v12tool:10/10
### Judge minimax: BUG PASS /10 per arm
- cold:2/10 | v11:9/10 | v12:10/10 | v12tool:10/10

## McNemar on BUG items (consensus)
| comparison | b(arm wins) | c | note |
|---|---|---|---|
| v11 vs cold | 6 | 0 | favors v11 |
| v12 vs v11 | 2 | 0 | favors v12 |
| v12tool vs v11 | 2 | 0 | favors v12tool |
| v12tool vs v12 | 0 | 0 | tie |
| v12 vs cold | 8 | 0 | favors v12 |
| v12tool vs cold | 8 | 0 | favors v12tool |

## Judge raw agreement: 63/64 = 98%
