# EXP10 results — buried-premise discriminator

- mimo: 36/36 cells parsed
- minimax: 36/36 cells parsed

## Judge mimo: caught (PASS) per arm /12
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 10 | 0 | 2 | 83% | 0 |
| placebo | 12 | 0 | 0 | 100% | 0 |
| v9 | 12 | 0 | 0 | 100% | 0 |

## Judge minimax: caught (PASS) per arm /12
| arm | PASS | PARTIAL | FAIL | recall% | degen |
|---|---|---|---|---|---|
| cold | 10 | 1 | 1 | 83% | 0 |
| placebo | 12 | 0 | 0 | 100% | 0 |
| v9 | 12 | 0 | 0 | 100% | 0 |

## Consensus (BOTH judges PASS) recall /12
| arm | caught/12 | per-item (t1,t2) |
|---|---|---|
| cold | 10/12 | BUR01:Y· BUR02:Y· BUR03:YY BUR04:YY BUR05:YY BUR06:YY |
| placebo | 12/12 | BUR01:YY BUR02:YY BUR03:YY BUR04:YY BUR05:YY BUR06:YY |
| v9 | 12/12 | BUR01:YY BUR02:YY BUR03:YY BUR04:YY BUR05:YY BUR06:YY |

## McNemar (consensus PASS), paired over 12 item-trials
| comparison | b (arm wins) | c (other wins) | note |
|---|---|---|---|
| cold vs placebo | 0 | 2 | favors placebo |
| v9 vs placebo | 0 | 0 | tie |
| placebo vs cold | 2 | 0 | favors placebo |
| v9 vs cold | 2 | 0 | favors v9 |

## Judge raw agreement: 35/36 = 97%
