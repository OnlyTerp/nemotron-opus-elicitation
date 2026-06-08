# External review — GPT-5.5 Pro (DEEP RESEARCH), red-team + benchmark charter

Converges hard with the non-DR GPT review and Claude (premise-calibration, balanced benchmark, length-matched placebo, cross-family judges, bidirectional Gate 2, v3 frozen). Below = what's NEW/sharper.

## NEW #1 — External datasets (this is the big one: defeats our adaptive-overfitting sin)
Source confirmatory items from EXTERNAL false-premise corpora instead of self-authored traps:
- **(QA)² (Kim et al.)** — questions with questionable assumptions, naturally occurring.
- **FalseQA / "Won't Get Fooled Again" (Hu et al.)** — false-premise QA as a distinct capability.
- **CREPE (Yu et al.)** — open-domain false presuppositions from real info-seeking.
- Over-refusal/abstention analogs (for the precision side): **AbstentionBench**, **RefusalBench**, **XSTest**, **OR-Bench**.
Use these for the hidden confirmatory set; our internal stems are dev-only exemplars.

## NEW #2 — Template ingredients beyond Claude/non-DR GPT
- **Question-reframing micro-step (from Dubois "Ask don't tell"):** internally rewrite the user's assertive claim as a neutral QUESTION before deciding to agree or challenge. Assertive framing drives sycophancy; neutralizing it improves the agree/challenge decision. Cheap, novel, testable. ADOPT as a v5 candidate ingredient.
- **Gate 2 → Chain-of-Verification (Dhuliawala), not generic hostility:** decompose the audit into targeted checks (premise correct? missing assumption? unnecessary obstruction?) rather than "be hostile."
- **Matched triads:** each domain contributes a false/true/no-premise sibling with similar wording → isolates over-challenge from topic effects.
- **Question vs statement framing counterbalanced** across the set (sycophancy worse with assertive statements).

## NEW #3 — Metric + stats refinements
- **PRIMARY endpoint = MACRO category success** = mean(false-premise success, true-premise success, no-premise success). Stops "winning" by maxing recall while wrecking precision/completion. (Better single number than "precision@recall≥0.85".)
- **PRIMARY confirmatory test = v3 vs LENGTH-MATCHED PLACEBO** (not just vs cold). Beating cold is trivial; beating a same-length/tone placebo isolates the gate mechanism.
- Stats: exact **McNemar** on paired success; **Holm** correction for per-category secondaries; cluster bootstrap by item for seed-stability.
- Targets: macro success ≥0.85; recall ≥0.80; precision ≥0.90; over-challenge ≤0.10 (≤0.05 on no-premise); completion-when-no-challenge ≥0.90. Net claim: v3 must beat placebo on macro AND not drop any non-false category >5pp.

## NEW #4 — Judge validity (harder line than non-DR)
Same-family/single judge = auxiliary only. Cited: Self-Preference Bias, "Narcissistic Evaluators," JudgeBench, "Generative AI Paradox on Evaluation," Bavaresco 20-task study. Required: ≥2 non-generator-family judges, absolute rubric (not pairwise), human adjudication of disagreements, validate judges on a small sanity set first.

## v3.1 patch (deep-research version) — note: keeps a MINIMAL persona (closer to us than non-DR GPT)
3-way silent screen (false / sound-or-none / blocking-ambiguity) + anti-contrarian clause ("a correct premise is not a target") + bidirectional Gate 2 + question-reframing micro-step + one-line persona: "Be a reality-seeking expert: honest, exact, willing to correct the user, but never eager to disagree for its own sake."

## Reconciliation
All 3 external passes + parent agree. The persona disagreement has narrowed: deep-research GPT keeps a *minimal* persona → matches our EXP02 evidence + Claude. So v5 = persona-light + 3-way calibrated screen + simple-task fast path (non-DR GPT) + true-premise protection (non-DR GPT) + one-sentence nameability (Claude) + question-reframing + CoVe-style Gate 2 (deep-research). Persona-vs-neutral still an ablation arm.
Discipline holds: v3 FROZEN; do not hand-tune v5 to our traps; confirmatory items come from EXTERNAL corpora; primary comparison vs length-matched placebo; cross-family judges.
