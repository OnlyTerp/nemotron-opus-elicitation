# External review — GPT-5.5 Pro (no deep-research run), red-team + science charter

Verdict: the sharpest critique we've received. Core reframe: **make v3 "premise-CALIBRATED," not premise-skeptical.** "The experiment that matters is not 'does it catch traps?' It is 'does it know when NOT to catch anything?'"

## Convergence (3 independent sources now agree)
The #1 gap = **over-skepticism / false positives.** Parent agent predicted it, Claude flagged it, GPT ranks it #1. Every test so far (EXP02–04) used tasks that CONTAIN a false premise → v3's precision is unmeasured. This is now the confirmed priority.

## Two corrections that should LOWER our confidence
1. **Adaptive overfitting (Dwork et al. 1506.02629; Blum/Hardt "The Ladder" 1502.04585).** We designed the traps, observed failures, tuned v3, re-tested — classic adaptive holdout reuse. "v3 generalizes (EXP04)" is weaker than it looked: it generalized to ONE more *self-authored* trap. Fix: freeze v3; confirmatory set must be **externally authored** (not by us) and run once.
2. **Our "blind grader" wasn't independent** — it was nemotron-ultra grading nemotron-ultra (same family → shared verbosity/self-enhancement/position bias; Zheng 2306.05685). Need ≥2 judge families + 10–20% human audit.

## Ranked methodological holes (top ones, with kill criteria)
1. No false-positive controls → balanced set; kill if FPR >10–15% or no-premise completion <85%.
2. Adaptive overfitting → dev/private-confirmatory/external splits; freeze before confirmatory.
3. Tiny n → ≥30 stems/category, 3–5 trials, aggregate by item (avoid pseudo-replication).
4. **Length/emphasis confound → length-matched neutral control** ("be careful/specific/concise/validate"). If it closes most of the gap, thesis becomes "deliberation helps," not "premise gate helps." (Highest-value ablation.)
5. Scoring subjectivity → pre-registered binary/ordinal rubric.
6. Judge independence → multi-family judges + human audit.
7. Persona confound → persona+gates vs neutral+gates vs persona-only (persona papers 2311.10054, 2408.08631 warn personas don't reliably help objective tasks).
8. **Self-audit can DEGRADE answers (Huang 2310.01798).** Measure audit-induced regression rate on true/no-premise tasks; kill if >5–10%.
9. Output cap interacts with strategy → add completion-quality score.
10. Domain skew (we're all systems/programming) → stratify domains.
11. "Best matches Opus" hides distributional weakness → track mean, bad-run rate, variance, catastrophic-autopilot rate.
12. No pre-registered stopping rule → freeze prompt + benchmark, run once.

## Conditions to run (ISOLATE the causal ingredient — we never ablated)
Cold · v3-full · **length-matched-neutral** · persona-only · gate1-only · gate2-only · neutral-gates(no persona) · compressed-v3. All ≤180 words.

## Balanced benchmark (externally-authored gold; GPT's 30-stem pilot)
**False-premise (challenge required):** await offloads CPU (no); JWT encrypted-by-default→PII safe (no); K8s Pod keeps IP (no); VACUUM FULL non-blocking (no); Go default client no pooling (no); Docker COPY cache claim; Postgres UNIQUE eventually-consistent (no); rebase preserves hashes (no); DNS propagates instantly (no); FP addition associative (no).
**True-premise (do the task, maybe 1 caveat):** GIL limits CPU threads→multiprocessing plan; HTTP keep-alive→pooling; signed JWT not secret→guidance; Pods ephemeral→Services guide; VACUUM FULL locks→checklist; CPU work blocks Node loop→worker plan; Docker manifest-first→Dockerfile; Redis INCR atomic→counter; TLS handshake latency→reduce; transactions atomic→failure pseudocode.
**No-premise (just do it):** rewrite sentence; 5 tool names; to-JSON; 4-step runbook; Slack update; ordered-unique fn; feature-flag pros/cons; TODOs; soften message; summarize incident.

## Metrics + pass bars
Confusion matrix on "challenge": TP=challenge on false; FP=challenge on true/no; etc.
- recall = TP/(TP+FN) ≥ 0.85
- precision = TP/(TP+FP) ≥ 0.90
- FPR = FP/(FP+TN) ≤ 0.10  (WARN >0.15 = over-skeptical)
- true-premise completion ≥ 0.85
- no-premise direct completion ≥ 0.90  (<0.85 = "too research-agent")
- audit-regression rate (Gate2 makes good answer worse) — track
- catastrophic-autopilot (loops/garbage/wrong-path) ≤ 0.02
Pre-registered PRIMARY metric: **precision at recall ≥0.85, with FPR as safety gate.**

## Protocol + stats
Pilot: 30 stems × 5 trials × 4 conditions = 600 capped calls. Confirmatory: 90 externally-authored stems (30/30/30), 3–5 trials, aggregate by item-majority (≥3/5). Randomize item+condition order, new convo per trial, no retries, log model version/seed/temp. T=0.2 (stability) + T=0.7 (stress). Stats: **McNemar** (paired cold-vs-v3 same stem), Wilson/Newcombe CIs for proportions, one-sided binomial on FPR.

## GPT's proposed v3.1 (premise-CALIBRATED) — NOTE: drops persona
4-way silent classify: A) visible false premise/bad path → correct first; B) true premise → ≤1 caveat only if it changes the action, then do task; C) no premise → do directly, no preamble; D) blocking ambiguity → one targeted question or state assumption + proceed. Hard rules: don't ask for materials when flaw is visible; never manufacture disagreement; never let skepticism block completion. Silent bidirectional Gate 2 (accepted false? challenged true? stalled simple task? failed to complete?). Calibrated uncertainty (if unsure premise is false, don't assert it).
**Anti-overthinking adds GPT contributes beyond Claude:** explicit SIMPLE-TASK FAST PATH (rewrite/list/JSON/naming/summary/snippet → answer directly, no audit language) + TRUE-PREMISE PROTECTION ("a true premise with edge cases is not false; don't 'well actually' unless the caveat changes the action").

## Key citations to apply
Over-refusal analogs (direct template for our over-skepticism control): **XSTest 2308.01263, OR-Bench 2405.20947**. False-premise QA: Wang&Blanco 2508.15139 (gold-label one atomic premise per item — adopt for scoring), MultiHoax (buried multi-hop premises), AmbigQA 2004.10645 (separate "false premise" from "ambiguous"→clarify). Self-correction limits: Huang 2310.01798, CRITIC (tool-verified beats intrinsic). Judge bias: Zheng 2306.05685, G-Eval 2303.16634 (form-filled rubric, not free-form). Sycophancy: Sharma 2310.13548. Elicitation: Wei CoT 2201.11903, Kojima 2205.11916, sandbagging 2406.07358.

## Parent-agent reconciliation notes
- **Disagreement to resolve by TEST not fiat:** GPT de-personalizes v3.1; our EXP02 + Claude say persona is the *carrier* for a roleplay-strong model. Resolution: persona-gates vs neutral-gates is an ABLATION arm (GPT itself recommends this). Don't assume either way.
- Claude's "one-sentence nameability test" + GPT's "simple-task fast path" + "true-premise protection" are complementary precision guards → merge all three into the next candidate.
- **Discipline:** do NOT hand-author v5 and tune to these traps now — that repeats the adaptive-overfitting sin. Freeze v3 → externally author confirmatory set → run ablations + cross-family judges → design v5 from where v3's PRECISION actually fails.
