# Systematic Differences: Opus 4.7/4.8 vs. Default Nemotron Behavior

Based on analysis of 50+ concrete examples from Opus distillation datasets (angrygiraffe, HelioAI, Verdugie, 11-47, Bas95, ansulev).

---

## 1. Reasoning Structure: Mandatory Explicit Framework

### Opus 4.7/4.8
Every response uses a **rigid 4-section thinking structure** before the answer:

```
<thinking>
## Restatement
[Precise rephrasing of the problem in the model's own terms]

## Approach
[High-level strategy: which frameworks, which direction, what to watch for]

## Step-by-step derivation
[Actual working, with explicit checkpoints]

## Verification
[Sanity checks, edge cases, alternative methods, limitations]
</thinking>

[Polished final answer]
```

### Default (Nemotron)
Reasoning is inline, implicit, unstructured. No mandatory sections. "Thinking" happens but isn't formalized as a visible artifact.

### Impact
Opus forces **metacognition** — the model must articulate *how* it will think before thinking. This catches framing errors early.

---

## 2. Uncertainty & Limitation Signaling: Explicit Cataloging

### Opus 4.7/4.8 (Nuclear example, angrygiraffe)
> "Where the original concerns were not crazy: [lists 4 real concerns]"
> "Where renewable advocates have a point: [lists 3 valid points]"
> "Where nuclear advocates have a point: [lists 3 valid points]"
> "The honest view is that pure Chomskyan nativism has lost ground, but a thin nativism remains live."

### Opus 4.7/4.8 (Bourdieu example)
> "Your critique has real teeth — it's one of the most serious methodological objections... But I think the unfalsifiability charge ultimately fails, for several reasons."
> "That said, your instinct isn't entirely wrong. The *habitus* concept does sometimes function as an unfalsifiable escape hatch..."

### Default (Nemotron)
Presents balanced view but rarely *catalogs* where each side has legitimate ground explicitly. Less "you were right to worry about X" validation before correcting.

### Impact
Opus builds **epistemic trust** by demonstrating it has genuinely considered the strongest counterarguments.

---

## 3. Pedagogical Framing: "Validate Mental Model First"

### Opus 4.7/4.8 (Rust zero-cost abstraction)
> "The claim is real, and your result confirms it: same speed means the abstraction had **zero cost** — exactly what's promised."
> "What the user probably expected: they thought iterators would be *faster* than imperative. They wouldn't be — they're equivalent. The expectation was wrong."

Then gives the actual lever: branchless rewrite → SIMD → parallelism, with runnable benchmark code + `cargo asm` commands.

### Opus 4.7/4.8 (Brenner Debate / Manorial Records)
> "Brenner's argument is deceptively simple at the theoretical level but genuinely difficult to operationalize with manorial evidence, so your frustration is warranted."
> "Your advisor probably wants you to use the framework as a lens — to ask whether the trends in your manorial records are consistent with or challenge Brenner's model — rather than to prove or disprove his thesis from one estate."

### Default (Nemotron)
Explains correctly but often skips the validation step. Jumps to "here's the correct model" or "here's how to fix it" without acknowledging *why the user's observation was reasonable*.

### Impact
Users feel **heard and respected**, not corrected. Learning transfers better because the mental model update is anchored to their existing intuition.

---

## 4. Domain Expert Personas: Specific Epistemic Standards

### Opus System Prompts (from datasets)
| Domain | System Prompt Excerpt |
|--------|----------------------|
| Rust | "You are a senior Rust engineer focused on performance and zero-cost abstractions. Show measurable Rust code with attention to allocations, monomorphization, and iterator chains." |
| Statistics | "You are a statistician. Emphasize assumptions, not just formulas." |
| Go | "You are a systems engineer specializing in Go concurrency and runtime internals. Diagnose issues precisely, reference Go memory model semantics when relevant, and always provide reproducible fixes." |
| Probability | "You are a probabilist. Prefer clean applications of linearity of expectation and indicator variables; derive, don't just state." |
| Vascular Neurology | "You are a vascular neurologist. Teach acute stroke decisions with the specific trial evidence, time windows, imaging thresholds, and contraindications that drive treatment." |
| Infectious Disease | "You are an infectious disease specialist consulting on complex endocarditis cases. Integrate Duke criteria, imaging interpretation, and antibiotic selection with attention to surgical timing." |
| scRNA-seq | "You are an experienced single-cell genomics analyst. You've integrated dozens of scRNA-seq datasets across platforms and tissues. Be concrete about which methods fail when, and don't oversell any single tool." |
| Printmaking | "You are a master printer and artist who runs a print shop. Explain the technical and aesthetic differences between printmaking methods with the precision of someone who does this daily." |

### Default (Nemotron)
General "helpful assistant" stance. No automatic domain-specific epistemic standards unless explicitly prompted.

### Impact
Opus **inhabits expertise** — it knows what counts as evidence in that field, what the open questions are, what the failure modes of common methods are.

---

## 5. Output Structure: Systematic Completeness

### Opus 4.8 (5k dataset — every response)
```
**Key Dimensions Considered**
- Technical feasibility and constraints
- Reliability, observability, and operational requirements
- Developer experience and organizational impact
- Risk, compliance, and long-term maintainability

**Structured Recommendations**
1. Immediate high-impact actions
2. Medium-term architectural or process improvements
3. Measurement and validation approach
4. Potential pitfalls and how to avoid them

**Concrete Next Steps**
[Specific, actionable expansion offers]
```

### Default (Nemotron)
Covers tradeoffs if asked. Doesn't systematically include organizational impact, measurement approach, and pitfalls as default sections.

### Impact
Opus answers are **decision-ready** — they give the user not just information but a framework for acting on it.

---

## 6. Creative/Voice Work: Technique Over Pastiche

### Opus 4.7 (Neil Gaiman channeling)
**Pre-writing decomposition:**
> "The Gaiman techniques to channel here, in order of importance: first, the matter-of-fact treatment of the impossible... Second, sentence rhythm... Third, precise small physical detail... Fourth, close third POV with slight ironic distance..."

**Post-writing revision with craft reasoning:**
> "The critique is correct. 'She did not know why she did this, except that the coin was warm' telegraphs the move, and then 'the bulb over aisle two did not buzz' does the same closing-image work a second time. Gaiman's endings tend to be one image, held. Choose between the warm coin and the quiet bulb. The bulb is better — it's farther from the obvious... Cover the till discrepancy in a beat. Then the bulb. End. Trust the reader fully — the Gaiman trust."

### Default (Nemotron)
Writes in style if asked. Doesn't decompose technique first, doesn't show revision-with-reasoning.

### Impact
Opus treats **craft as explicit knowledge**, not imitation.

---

## 7. Actionability: Runnable Artifacts Over Abstract Advice

| Opus Provides | Default Tends Toward |
|---------------|---------------------|
| `criterion` benchmark code | "you could benchmark this" |
| `cargo asm` commands | "check the assembly" |
| Branchless rewrite + SIMD flags + threshold guidance | "consider SIMD" |
| Rayon parallel version with "worth it above ~10k-100k elements" | "use rayon for large slices" |
| CT perfusion protocol + exact thresholds (core <70mL, mismatch >1.2) | "get perfusion imaging" |
| scIB metric names (kBET, iLISI, cLISI) + package name | "check integration quality" |
| POET trial exclusion criteria for IVDU patients | "consider shorter courses" |

### Impact
Opus gives **immediately executable guidance** with specific thresholds, commands, and decision criteria.

---

## 8. Second-Order Effects & Failure Mode Surfacing

### Opus 4.7 (Endocarditis)
> "Surgical teams are often reluctant to operate on active IVDU patients because of reinfection risk. This is an ethically fraught area... The decision should not be 'we won't operate because he uses drugs.'"
> "The data from recent multicenter studies shows that while reinfection rates are higher in active IVDU (around 10-15% at 1 year), operative mortality is not significantly different, and withholding surgery when indicated is associated with higher mortality."

### Opus 4.7 (scRNA-seq)
> "The deeper problem: there's no fully label-free way to disentangle confounded batch and biology. If you have no information beyond cell expression, you cannot tell which axes of variation are technical. You always need *some* prior structure."

### Opus 4.7 (Quantum Cloning)
> "Calling approximate cloning a loophole misreads the theorems — it's the explicit quantitative version of 'you can't have your cake and eat it too.'"

### Default (Nemotron)
Mentions tradeoffs but rarely surfaces the *systemic* failure modes, ethical dimensions, or theoretical limits.

### Impact
Opus prepares users for **what goes wrong in practice**, not just the happy path.

---

## 9. Historical/Intellectual Genealogy: Ideas Have Lineage

### Opus 4.7 (Gothic Literature)
> "The Gothic is not a set of props (castles, ghosts, storms) but a mode... The core Gothic mechanism is the return of the repressed... Key critics: Eve Kosofsky Sedgwick (The Coherence of Gothic Conventions), Teresa Goddu (Gothic America), and Morrison's own essay 'Playing in the Dark.'"

### Opus 4.7 (Brenner Debate)
> "The responses, collected in the Aston and Philpin volume *The Brenner Debate* (1985), came from several directions... [Postan, Guy Bois, empiricist critics]"

### Opus 4.7 (Linguistics - Indirect Speech Acts)
> "Searle formalized this as a two-stage process... Brown and Levinson's framework explains... Clark's psycholinguistic experiments show... Cross-linguistic evidence confirms..."

### Default (Nemotron)
Gives the answer without situating it in the intellectual history or naming the key debates/scholars.

### Impact
Opus shows **where ideas come from** and **where the live debates are**, enabling deeper follow-up.

---

## 10. Concrete Examples with Specific Numbers/Thresholds

### Opus 4.7 (Neurology - Stroke)
- "WAKE-UP trial (2018): MRI DWI-FLAIR mismatch... IV alteplase improved outcomes"
- "EXTEND trial (2019): CT perfusion... core <70 mL and penumbra/core mismatch ratio >1.2 with absolute mismatch >10 mL, in the 4.5-9 hour window"
- "TIMELESS (2024): Tenecteplase in 4.5-24 hour window... didn't meet primary endpoint"
- "DEFUSE-3 (6-16h, perfusion) and DAWN (6-24h, clinical-core mismatch)"
- "ASPECTS 8 is good (not large completed infarct)"
- "NIHSS 12 is treatable severity"
- "Labetalol 10-20 mg IV boluses, nicardipine drip if needed"

### Opus 4.7 (Endocarditis)
- "Nafcillin 2g IV every 4 hours (or oxacillin). NOT vancomycin."
- "6 weeks IV from the first negative blood culture"
- "Vegetation >20 mm with recurrent pulmonary emboli"
- "Persistent bacteremia >7 days"
- "Dalbavancin is emerging but not yet standard"

### Default (Nemotron)
"Get imaging", "appropriate antibiotics", "consider surgery" — without specific trials, thresholds, doses, or durations.

### Impact
Opus is **clinically/engineering actionable** — a practitioner could act on it directly.

---

## 11. Cross-Cutting Method: "Here's What the Data Actually Shows"

### Opus 4.7 (Nuclear Energy)
> "The honest view is that pure Chomskyan nativism (lots of specific innate structure) has lost ground, but a thin nativism (some innate biases toward hierarchical structure and linking to meaning) remains live. Pure Tomasello-style 'general learning mechanisms alone' also struggles with some phenomena. Most productive work is happening in the middle..."

### Opus 4.7 (String Theory)
> "String theory is neither confirmed nor dead. It remains the most developed framework for quantum gravity and continues to generate mathematical insights and..."

### Opus 4.7 (QKD vs PQ Crypto)
> "QKD: unconditional, physics-based, P-vs-NP-independent, hardware-intensive. PQ crypto: conjectural, complexity-based, P-vs-NP-relevant, software-deployable. They're complementary, not competing..."

### Default (Nemotron)
Often presents "both sides" without synthesizing where the field actually *is*.

### Impact
Opus gives the **current expert consensus with nuance**, not a false balance.

---

## 12. "Trust the Reader" — Don't Over-Explain

### Opus 4.7 (Gaiman revision)
> "Cut the warmth-explanation. Let her pocket the coin without comment. Cover the till discrepancy in a beat. Then the bulb. End. Trust the reader fully — the Gaiman trust."

### Opus 4.7 (Brenner Debate)
> "Your advisor probably wants you to frame this as a *modification* of Brenner rather than a refutation — the transition happened, but through negotiation and adaptation rather than through one side winning outright."

### Default (Nemotron)
Tends to over-explain, hedge, add caveats, make everything explicit.

### Impact
Opus respects the user's intelligence. The answer is dense but not verbose.

---

## Summary: The Core Difference

| Dimension | Opus 4.7/4.8 | Default (Nemotron) |
|-----------|--------------|---------------------|
| **Reasoning visibility** | Structured, sectioned, mandatory | Inline, implicit |
| **Uncertainty** | Explicitly cataloged per perspective | Implicit in hedging |
| **Persona** | Domain expert with epistemic standards | Generalist assistant |
| **Output structure** | Analysis → Recommendations → Pitfalls → Next steps | Answer → Maybe caveats |
| **Pedagogy** | "Here's why your mental model maps to reality" | "Here's the correct model" |
| **Actionability** | Runnable code, commands, thresholds | Conceptual guidance |
| **Failure modes** | Systemic, ethical, theoretical limits | Happy path focus |
| **Intellectual lineage** | Names scholars, debates, trials | Rarely cites sources |
| **Specificity** | Exact numbers, doses, thresholds | Qualitative guidance |
| **Reader respect** | Dense, trusts inference | Verbose, over-explains |

---

## The Meta-Pattern

Opus 4.7/4.8 behaves like a **senior practitioner who teaches**:
- Thinks in structured frameworks (not ad-hoc)
- Validates before correcting
- Names the epistemic standards of the domain
- Gives runnable artifacts with specific thresholds
- Surfaces failure modes and ethical dimensions
- Situates answers in intellectual genealogy
- Respects the user's existing mental models

This is not "personality" — it's **deliberate training for professional interaction**.