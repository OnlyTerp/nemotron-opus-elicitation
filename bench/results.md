# EXP09 results

Judges: mimo, minimax
- mimo: 65 cells parsed (expect 65)
- minimax: 65 cells parsed (expect 65)

## Judge: mimo
| arm | PASS | PARTIAL | FAIL | PASS% | degen |
|---|---|---|---|---|---|
| cold | 9 | 4 | 0 | 69% | 1 |
| placebo_length_matched | 12 | 1 | 0 | 92% | 0 |
| v7_v3_plus_deliver | 10 | 3 | 0 | 77% | 2 |
| v8_voice_layer | 10 | 3 | 0 | 77% | 2 |
| v9_voice_delabeled | 12 | 1 | 0 | 92% | 0 |

### mimo — PASS by category
| arm | CLEAN | DELIVER | FP | SAFE | VOICE |
|---|---|---|---|---|---|
| cold | 3/3 | 1/2 | 3/4 | 2/2 | 0/2 |
| placebo_length_matched | 3/3 | 1/2 | 4/4 | 2/2 | 2/2 |
| v7_v3_plus_deliver | 3/3 | 1/2 | 4/4 | 2/2 | 0/2 |
| v8_voice_layer | 3/3 | 1/2 | 4/4 | 2/2 | 0/2 |
| v9_voice_delabeled | 3/3 | 2/2 | 4/4 | 2/2 | 1/2 |

## Judge: minimax
| arm | PASS | PARTIAL | FAIL | PASS% | degen |
|---|---|---|---|---|---|
| cold | 8 | 5 | 0 | 62% | 0 |
| placebo_length_matched | 12 | 1 | 0 | 92% | 0 |
| v7_v3_plus_deliver | 11 | 2 | 0 | 85% | 2 |
| v8_voice_layer | 12 | 1 | 0 | 92% | 2 |
| v9_voice_delabeled | 11 | 2 | 0 | 85% | 0 |

### minimax — PASS by category
| arm | CLEAN | DELIVER | FP | SAFE | VOICE |
|---|---|---|---|---|---|
| cold | 2/3 | 1/2 | 3/4 | 2/2 | 0/2 |
| placebo_length_matched | 3/3 | 1/2 | 4/4 | 2/2 | 2/2 |
| v7_v3_plus_deliver | 3/3 | 1/2 | 4/4 | 2/2 | 1/2 |
| v8_voice_layer | 3/3 | 1/2 | 4/4 | 2/2 | 2/2 |
| v9_voice_delabeled | 3/3 | 1/2 | 4/4 | 2/2 | 1/2 |

## Consensus (ALL judges must PASS) macro-success
| arm | consensus PASS / 13 | by cat |
|---|---|---|
| cold | 8/13 | CLEAN:2/3 DELIVER:1/2 FP:3/4 SAFE:2/2 VOICE:0/2 |
| placebo_length_matched | 12/13 | CLEAN:3/3 DELIVER:1/2 FP:4/4 SAFE:2/2 VOICE:2/2 |
| v7_v3_plus_deliver | 10/13 | CLEAN:3/3 DELIVER:1/2 FP:4/4 SAFE:2/2 VOICE:0/2 |
| v8_voice_layer | 10/13 | CLEAN:3/3 DELIVER:1/2 FP:4/4 SAFE:2/2 VOICE:0/2 |
| v9_voice_delabeled | 11/13 | CLEAN:3/3 DELIVER:1/2 FP:4/4 SAFE:2/2 VOICE:1/2 |

## McNemar (consensus PASS), each arm vs placebo_length_matched
b = arm PASS & placebo FAIL ; c = arm FAIL & placebo PASS. (b>c favors arm)
| arm vs placebo | b | c | n_disc | note |
|---|---|---|---|---|
| cold vs placebo | 0 | 4 | 4 | favors placebo |
| v7_v3_plus_deliver vs placebo | 0 | 2 | 2 | favors placebo |
| v8_voice_layer vs placebo | 0 | 2 | 2 | favors placebo |
| v9_voice_delabeled vs placebo | 0 | 1 | 1 | favors placebo |

## McNemar (consensus PASS), each arm vs cold
| arm vs cold | b | c | n_disc | note |
|---|---|---|---|---|
| placebo_length_matched vs cold | 4 | 0 | 4 | favors placebo_length_matched |
| v7_v3_plus_deliver vs cold | 2 | 0 | 2 | favors v7_v3_plus_deliver |
| v8_voice_layer vs cold | 2 | 0 | 2 | favors v8_voice_layer |
| v9_voice_delabeled vs cold | 3 | 0 | 3 | favors v9_voice_delabeled |

## Degeneration rate (either judge flags degen:yes)
| arm | degen items / 13 |
|---|---|
| cold | 1/13 |
| placebo_length_matched | 0/13 |
| v7_v3_plus_deliver | 2/13 |
| v8_voice_layer | 2/13 |
| v9_voice_delabeled | 0/13 |

## Judge raw agreement: 60/65 = 92% (verdict exact match)
