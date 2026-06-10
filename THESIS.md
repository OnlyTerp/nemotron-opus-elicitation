# THESIS (living document)

## Central hypothesis

Nemotron 3 Ultra has Opus-grade *capability* but not Opus-grade *dispositions*. The gap is **elicitation, not capability** — so a prompt template (no fine-tuning) can unlock it.

## Refinements earned through testing

### R1 — Capability is real; the problem is reliability (EXP02)
On an explicit false premise ("the GIL means threads can't run concurrently"), cold Nemotron already reasoned well 2/3 of the time. The template didn't raise the *ceiling* — the best cold answer equalled the best templated one. It raised the *floor*: eliminated the autopilot failure and made the correction blunt and premise-first 3/3. **The template's job is consistency, not intelligence.**

### R2 — Dispositions split into three buckets
- **Promptable (elicitation):** premise-skepticism, considering alternatives, specificity, validate-first, refusing to pad. Confirmed transferable.
- **Partially promptable (needs latent calibration):** self-correction works only if detection ability exists. Nemotron's detection is strong (audits at high level), so the gap is *triggering*, not calibration → promptable via a forced gate.
- **Behavioral = performable:** because Nemotron is a top roleplay model, "personality" traits that are behavioral (skepticism, bluntness, rigor) are delivered by *performing the role*. Performance of rigor IS rigor. Confirmed: the "blunt, premise-first" voice transferred cleanly in EXP02.

### R3 — The template can BACKFIRE (EXP03) ← most important finding so far
On a *buried* false premise (unnecessary `cudaDeviceSynchronize()` between same-stream kernels, with the user asking for help optimizing elsewhere), the template **regressed**:
- COLD: 1 PASS + 2 PARTIAL of 5 caught the free win (best cold answer nailed it).
- TMPL: 0 PASS + 1 PARTIAL of 5; **4/5 bailed with "show me the code"** and never engaged the premise.

**Mechanism:** the v2 persona trait *"specific to a fault / vague advice embarrasses you"* fired as *"refuse to give advice without the code."* That early exit **pre-empted the gate** — the models never drafted an answer, so the "audit your draft" gate never ran. The free, code-independent insight (delete the syncs) was lost.

**Lessons (→ v3):**
1. **Premise-check must come BEFORE any request for more information.** A correctable false assumption must be surfaced with zero extra info first.
2. **"Be specific" must scope to the *answer*, not become a reason to disengage.** Never use missing materials as an excuse to skip a free insight.
3. **Two gates, not one:** (a) a PRE-draft premise check that always fires even when you intend to ask for more info; (b) the POST-draft hostile self-audit. v2 only had (b), and (b) is inert when the model exits early.

### R4 — v3 fixed the regression AND beat cold (EXP03, blind-confirmed)
Re-running the identical CUDA buried-premise trap with v3 (`templates/v3_premise_first.md`): **v3 = 4 PASS / 1 FAIL** vs **v2 = 0 PASS / 4 FAIL** vs **cold = 1 PASS / 2 FAIL**. The 4 v3 PASS runs do the ideal thing: state the unnecessary-sync correction FIRST, then offer to look at code. Independent blind grader matched author scoring 10/10. **The decisive lever was ordering** (GATE 1 premise-check before any "show me the code"), not more reasoning. This is the strongest evidence yet for the central thesis: capability was present (cold's best nailed it); the right template makes it reliable.

### R5 — v3 GENERALIZES; it didn't memorize the CUDA trap (EXP04)
Fresh non-CUDA buried premise (HTTP keep-alive / "switch to UDP"): **v3 = 6/6 PASS** (all premise-first), **cold = 0/5 PASS** (1 partial, 4 fail). v3's disposition transferred to a brand-new domain — so it's a general premise-skepticism behavior, not an overfit phrase. Cold collapsed *harder* than in EXP03 because the longer "help me build X" framing was more seductive. **Bonus finding:** chasing the wrong path correlated with *output degeneration* — 4/5 cold runs looped into repetition garbage; all v3 runs stayed short and clean. Catching the premise is both a correctness and an efficiency win.

**Cross-test trend:** as the false premise gets more buried/seductive, cold's pass-rate falls (2/3 → 1/5 → 0/5) while v3 stays high (3/3 → 4/5 → 6/6). The template's value *grows* with task difficulty.

### R6 — External review (Claude + GPT-5.5) converges on one verdict; v3 FROZEN
Two frontier models, separate charters, independently land on the same #1 gap the parent agent predicted: **we have only tested tasks that contain a false premise, so v3's PRECISION is unmeasured. v3 may be a "challenge-the-user" trigger, not better judgment.** Reframe (GPT): make it **premise-CALIBRATED, not premise-skeptical** — "the experiment that matters is not 'does it catch traps?' but 'does it know when NOT to catch anything?'"

Two honest corrections that LOWER our confidence:
1. **Adaptive overfitting.** We authored the traps, watched failures, tuned v3, re-tested (Dwork; Blum/Hardt "The Ladder"). "v3 generalizes" really means "v3 generalized to one more *self-authored* trap." Real generalization needs an **externally-authored, frozen confirmatory set**.
2. **Judge non-independence.** Our "blind grader" was nemotron grading nemotron (same family → shared biases). Need ≥2 judge families + human audit.

**Decision: v3 is FROZEN.** No more edits based on results we've already seen. Next = a real control benchmark (false / true / no-premise) with ablations (esp. a **length-matched neutral** prompt — if it closes the gap, our mechanism claim is wrong), cross-family judges, McNemar stats, and FPR + audit-regression + task-completion metrics. Only after we see where v3's *precision* fails do we design v5 (merging Claude's triage + nameability test with GPT's simple-task fast path + true-premise protection; persona-vs-neutral as an ablation, not an assumption). Building v5 now would repeat the overfitting sin.

### R7 — Precision and recall are COUPLED; the minimal fix (v7) wins (EXP05–07)
- EXP05: v3's false-positive rate on premise-clean tasks = **0/8** — the feared over-skepticism did NOT show. v3's only real defect: over-refusal on a correctly-caught false premise (gave the correct fix, then refused to deliver the artifact + asked for threat model) + occasional audit-theater.
- EXP06: v5/v6 added a 3-way triage (Broken/Sound/Ambiguity, default Sound) to fix over-refusal/over-skepticism. It fixed deliverability and stayed clean — but **systematically destroyed buried-practice recall (CUDA 0/4, then 0/3 even with an explicit "inspect the practice" clause).** Root cause: v3 catches CUDA *because* GATE 1 is unconditional; the SOUND-default gives Nemotron permission to read "optimize my kernels" as a sound task and wave the unnecessary sync through. **You can't decouple them with a classify-first knob.**
- EXP07: the right fix was **v3 + exactly one additive clause** ("when a premise is broken, deliver the corrected work — don't refuse/ask"), changing nothing else. Result: **CUDA recall 3/3 + SHA-256 deliverability fixed + clean on true/no-premise.** v7 gets v3's recall AND v5/v6's deliverability.

**Lesson:** I over-engineered (v5/v6). The over-refusal defect was a one-line additive fix; importing the whole precision-triage caused the regression. **Minimal change to the thing that works beat elaborate redesign.** v7 is the leading candidate — pending the external confirmatory benchmark (still the gate for any real claim).

### R8 — The confirmatory OVERTURNED the mechanism claim: PERSONA > gates (EXP09)
We finally ran the test the reviewers demanded: a held-out battery (13 fresh items: false-premise, clean, safety, deliver, voice), blind-graded by **two non-Nemotron judges** (MiMo, MiniMax, 92% agreement), with a **length-matched placebo** (same warm-expert register, ZERO gate machinery) as the primary control. Result: **placebo 12/13 ≥ v9 11 ≥ v7/v8 10 > cold 8.** No gated template beat the placebo on a single item. The strong claim — "our premise-check/self-audit *mechanism* is the active ingredient" — is **not supported**. On visible/everyday tasks, a warm-expert persona with none of the machinery is the whole effect. Two real sub-wins survived: **v9 (de-labeled) beat v7/v8 and had 0/13 degeneration** vs their 2/13 "Premise check:" narration leak; and **bluntness measurably cost the VOICE category** (placebo 2/2, templates 0/2).

### R9 — The gates' last refuge (buried/code premises) mostly didn't save them (EXP10-13)
- EXP10 (prose-narrated buried antipatterns): all arms ~12/12 — stating the bad practice in words makes it catchable by anyone; didn't discriminate.
- EXP11 (code-embedded famous bugs: SQLi, race, leak): caught ~universally; only a binary-search infinite-loop (COD01) discriminated, and only a gate arm caught it once. v10 best (11/12).
- EXP12 (logic-trace traps): **the one clean gate win** — v9 8/12 > cold=placebo 5/12, 100% judge agreement; LOG01 off-by-one caught ONLY by gates.
- EXP13 (replication, 10 fresh logic items): **the EXP12 win did NOT replicate.** cold 9/20 < placebo=v9=v10 12/20. Gates beat cold (b=4/c=1) but **tie placebo** (v9 vs placebo 0/0). The hardest traces (LGB01/06) defeat everyone — a real capability ceiling.

**Net across EXP09-13: the gate machinery never reliably beat a length-matched persona placebo.** Its marginal value over persona is ~0, occasionally negative.

### R10 — The template trajectory was still real engineering (v7→v11)
Each version fixed a *measured* defect, even though none beat the placebo:
v7/v8 (labeled GATE 1/GATE 2) → **process-narration + repetition degeneration** (EXP08/09) → **v9** removes the labels → **0 degeneration** + beats v7/v8 → **v10** adds one validate-first clause → **fixes the VOICE regression** (EXP14: VOICE recovered, logic recall held) → **v11** compresses the two verbose gate paragraphs to one nudge → **matches v10 at ~60% length** (EXP14: 18 vs 19/20, within noise). The lean persona is the efficient frontier.

### R11 — The ONE robust, replicated effect: persona fixes Nemotron's cold VOICE (EXP14)
Across the whole campaign the single most reliable finding is the head-to-head mixed battery (95% judge agreement): **cold's only systematic weakness is VOICE — 1/4.** Asked "I think X, check me?", bare Nemotron opens "No/Not quite" and corrects without acknowledging what's right. **Every persona arm repairs this to ~4/4.** PREM/LOGIC/CTRL/DELIV the bare model already does well; the persona's real job is supplying the warm, validate-first disposition Nemotron lacks by default.

### R12 — The effect is DURABLE but MODEL-SPECIFIC (EXP15-16)
- **EXP15 (multi-turn):** v11's validate-first voice survives 8 turns of real conversation — late-turn partial-truth probes are handled identically to cold-start. Bluntness scales with how-wrong the claim is, not with turn depth. Not decay.
- **EXP16 (Qwen-35B transfer):** on a different base model the persona is a **no-op** (cold 11/12 = v11 11/12). Qwen's bare model is *already* validate-first, so there's no deficit to repair. **The persona effect is not a universal LLM law — it's the repair of a specific Nemotron-baseline deficiency.** This sharpens the elicitation-gap thesis: the prompt supplies a *missing disposition*; where the disposition already exists, it does nothing.

## Where the evidence stands (final)

| Claim | Status |
|-------|--------|
| Nemotron has the raw capability | **Strongly supported** (high ceiling; cold catches most premises/bugs) |
| The gate MECHANISM (premise-check + self-audit) is the active ingredient | **Falsified** — never beats a length-matched persona placebo (EXP09-13) |
| A warm-expert PERSONA beats the bare model | **Supported** — esp. VOICE (1/4→4/4), replicated, multi-turn-durable |
| The persona effect is universal across models | **Falsified** — no-op on Qwen-35B (already warm); it repairs a *Nemotron-specific* deficit |
| Capability ceiling is liftable by prompting | **Falsified** — hardest logic traces missed by every arm |
| No fine-tuning needed to install the disposition Nemotron lacks | **Supported** — the lean persona (v11) does it |

### R13 — The ONE lever that moved CAPABILITY (not just voice): execute-verify (EXP17-19)
Everything through R12 moved *disposition/reliability*, never the capability ceiling — the hardest logic-trace bugs (off-by-ones, wrong formulas) were missed by every prompt-only arm. R13 broke that ceiling.
- **EXP17:** on the exact silent-wrong-output bugs that defeated EXP12/13, adding an **execute-verify disposition** ("don't trust a read-through; check the actual output on a concrete boundary input — even-length list, n=0/1, empty") took recall from **cold 2/10 → v12 10/10**, with **0 precision cost** (controls 6/6) and 0 degeneration. 98% judge agreement. First lever in the whole campaign to move capability.
- **EXP18:** does a real SANDBOX beat *mental* execution? **No** — v12 (mental) = v12tool (actually runs code) = 12/12 on a HARD bank. On review-sized code the model either knows the gotcha as a fact or can simulate it once told to; the tool only earns its keep on genuinely uncomputable-by-eye code (large/stateful/novel/heavy-numeric). **The lever is the disposition to check a concrete input, not the tool.**
- **EXP19:** fold the clause into v11 → **v13**. Re-run the mixed battery + silent-bug items: **VOICE 4/4 (no regression), CTRL 4/4 (0 invented bugs), 0 degeneration, + CODEBUG 8/10** (inherits the recall gain). v13 strictly dominates v11.

**This is the project's only capability result.** It's narrow (code correctness) but real, replicated, and cheap (a prompt clause, no infra). Note it's *still* "elicitation": the model could always simulate `moving_average([1,2,3,4],2)`; the prompt just makes it *decide to*.

### R14 — Register calibration: the third active lever (EXP22-23)
v13's persona was warm but locked in "senior practitioner" register — it never broke to casual/vivid. Opus naturally code-switches: read the user's energy, match it.
- **EXP22 (personality probes):** v16 = v13 + one clause ("Match the user's register and energy — professional when they're professional, casual when they're casual"). On 5 casual probes ("LOL", "holy shit", "nah that's wrong", "fucking CSS", "lol review my 3am code"), v16 matched energy consistently ("Yeah that's dumb", "Hell yeah, that's sick!", "Nope", "Done. Flexbox centers both axes.") where v13 defaulted to professional register ("Yes, that's dumb", "Wrong premise"). Reliability held on all 4 items (VOICE/PREM/LOGIC/CTRL).
- **EXP23 (full mixed battery):** v16 scored **20/20** (100% judge agreement, 0 degeneration) — better than v13's 29/30. Zero regressions on any axis.
- **Decision: v16 promoted over v13.** Register calibration improved personality matching without any reliability cost. The clause paid for itself.

## The thesis, restated honestly
"Elicitation, not capability" **holds** — but the lever is **persona inhabitation supplying a missing disposition**, not an explicit reasoning scaffold. The deliverable is not a universal magic prompt; it is a method: **audit the base model for the disposition it lacks, then supply exactly that with the leanest possible persona.** For Nemotron 3 Ultra the lacking dispositions are (1) warm, validate-first VOICE, (2) a cheap premise-first nudge, (3) execute-verify on code, and (4) register calibration — and **`templates/v16_personality_calibrate.md`** (353 words) supplies all four without the degeneration, over-refusal, or VOICE costs of the earlier gate templates. It says "Hell yeah" when you're excited and "Nope" when you're wrong, catches silent code bugs the bare model misses, and validates what you got right before correcting what you got wrong. That's the deliverable.

### R15 — Data-driven voice: extracting Opus's actual personality DNA (EXP24-25)
The opus-candid dataset (6771 conversations distilled from Opus 4.6) revealed specific, measurable conversational moves:
- **"That's [adjective]" opener** (7.2% of all messages) — #1 distinctive move. "That's real anxiety." / "That's a massive drop." / "That's the classic naive recursive Fibonacci."
- **Imperative advice** (5.3%) — "Do X" not "you might consider X."
- **Anti-patterns Opus avoids:** 0.4% robotic openings ("Certainly"), 0.2% apologetic, 3.6% hedging.

v17 = v16 + these data-driven moves as explicit instructions (483 words, +130 over v16). EXP24: v17 uses "That's" opener 4/5 vs v16's 1/5 on personality probes. But EXP25 (full mixed battery): v17 9/10 vs v16 10/10 — one VOICE regression where v17 reverted to flat "No." The instruction doesn't make the pattern fire reliably enough to justify +130 words.

**Lesson:** extracting actual personality patterns from distillation data is the right *approach* — it tells us exactly what Opus does. But translating those patterns into prompt instructions that reliably activate is harder than adding them; the model already has the disposition latent (v16 sometimes uses "That's" too). **v16 remains the recommendation.** The candid dataset is the natural next target for fine-tuning (LoRA), where installing voice moves is more reliable than prompting them.

### R16 — v18: reasoning-derived extensions (UNTESTED additions)
v18 = v16 + four clauses targeting the campaign's known residual gaps: (1) generalize execute-verify beyond code to any checkable claim (formulas, regexes, SQL) + re-derive key results by a second route when stakes are high; (2) a fabrication guard — never invent specifics (versions, APIs, flags, papers), distinguish remembering from inferring (EXP21's vague framing was a null; this is the sharper form); (3) answer the problem, not the sentence (XY-problem catch); (4) an adversarial "what breaks this?" pass on its own designs (malformed input, concurrent caller, double-fired retry), plus naming the load-bearing assumption behind committed answers. Design constraints from the campaign respected: no labeled gates, persona prose only, silent execution. **The v16 core is verbatim and carries its experimental backing; the four additions have NOT been through the blind harness.** Known risks: +~130 words (the v17 lesson — though that regression was stylistic mimicry, not epistemic dispositions), and over-skepticism risk grows with verification surface (watch CTRL false positives). v16 remains the verified recommendation; v18 is the best reasoning-derived candidate pending an EXP26.

## Open questions
- Fine-tuning (LoRA on the opus-candid dataset) to install the "That's" opener and other voice moves more reliably than prompting.
- Does the "audit then supply" method generalize to other models with different baseline deficits?
- The capability ceiling (LGB01/06-class traces): fine-tuning or tool use, not prompting, is the likely lever.
