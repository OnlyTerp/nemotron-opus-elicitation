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

## Where the evidence stands

| Claim | Status |
|-------|--------|
| Nemotron has the raw capability | **Strongly supported** (high ceiling, cold often nails it) |
| Prompting can make good reasoning reliable | **Supported** on explicit premises (EXP02) |
| A single generic template always helps | **Falsified** (EXP03 regression) |
| Template effect depends on task shape | **Supported** — helps on explicit claims, hurts when a "need more info" exit pre-empts the audit |
| No fine-tuning needed | **Still open** — plausible, but only with a template that fixes the R3 ordering bug |

## Open questions / next tests
- Does v3 (premise-first ordering) fix the EXP03 regression? (Re-run EXP03 with v3.)
- Bigger n (>=10/arm) for statistical confidence; report ratios + variance.
- Test the *ceiling*: a premise hard enough that cold rarely catches it — does any template lift it?
- Personality durability under multi-turn pressure (roleplay claim) — not yet tested.
