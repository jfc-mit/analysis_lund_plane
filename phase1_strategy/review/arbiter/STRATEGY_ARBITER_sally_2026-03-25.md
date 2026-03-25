# Arbiter Adjudication: Phase 1 Strategy -- Lund Jet Plane Density

**Arbiter:** Sally | **Date:** 2026-03-25
**Artifact:** `phase1_strategy/outputs/STRATEGY_fabiola_2026-03-25_16-50.md`
**Reviews adjudicated:**
- Physics: Albert (13 findings: 3A, 7B, 3C)
- Critical: Andrzej (16 findings: 4A, 7B, 5C)
- Constructive: Dolores (18 findings: 1A, 9B, 8C)

---

## 1. Structured Adjudication Table

Each row adjudicates one finding or group of correlated findings.
Final category reflects the arbiter's independent assessment after
cross-checking against the strategy artifact.

### 1.1 Multi-Reviewer Findings

| # | Finding | Sources | Their Categories | Final Category | Rationale |
|---|---------|---------|-----------------|----------------|-----------|
| 1 | **LO density formula wrong by factor 2** | Albert F1 | A | **A** | Albert is correct. The Dreyer/Salam/Soyez Eq. 2.6 gives rho ~ 2*alpha_s*C_F/pi in the soft, collinear limit, arising from the p_qq(z) = (1+(1-z)^2)/z splitting function. The strategy writes rho_LO = alpha_s*C_F/pi and estimates 0.050; the correct value is ~0.100. This is a factor-2 error in the benchmarking formula that would cause misinterpretation during Phase 4 validation. Blocking. |
| 2 | **Observable definition / hardness variable not verified against foundational paper** | Albert F2, Andrzej A1 | A, A | **A** | Both reviewers converge: the strategy claims energy ordering is the "standard choice for e+e-" without citation, and no evidence exists that the Dreyer/Salam/Soyez paper was actually retrieved and compared term-by-term. The foundational paper defines the harder branch by p_T; the e+e- adaptation to energy ordering is a defensible physics choice but must be explicitly justified, not asserted as standard. The methodology (03-phases.md) explicitly requires term-by-term verification against the cited paper. This is a blocking process failure and a physics ambiguity that affects every downstream phase. Albert's recommendation (p_T primary, energy as systematic variation) is sound. |
| 3 | **Coordinate definitions: e+e- adaptation from pp not transparent** | Albert F3, Andrzej A1 (partial) | A, A (within A1) | **A** | The strategy defines k_T = |p_2|*sin(Delta_theta), which is physically motivated and correct. However, it does not distinguish this from the pp definition (k_t = p_{tb}*Delta_{ab}) or discuss the regime where the two diverge. At wide angles (theta ~ 1 rad), sin(theta) vs theta differs by ~16%. Since the measurement's value proposition includes cross-collider comparison, the coordinate mapping must be explicit. Blocking because it affects the interpretation of every bin in the wide-angle region. |
| 4 | **Uniform binning not physics-motivated** | Andrzej A2 | A | **B** | Andrzej elevates this to A, citing ATLAS/ALICE non-uniform binning and the methodology requirement for physics-motivated bin widths. I accept the substance but downgrade to B. Reason: (a) the strategy explicitly commits to refining binning in Phase 2, (b) uniform binning is a valid starting point when resolution studies have not yet been performed, and (c) the Phase 2 exploration is the natural place to determine optimal binning from data/MC. However, the strategy must provide a physics-motivated *justification* for why uniform is the starting point (or adopt non-uniform), cite the ATLAS/ALICE binning choices, and commit to specific Phase 2 deliverables for bin optimization (migration fractions, resolution vs bin width). The current bare deferral to Phase 2 without any justification is insufficient. |
| 5 | **Missing heavy flavour systematic** | Albert F7, Andrzej A3, Dolores F7 | B, A, B | **A** | All three reviewers flag this. The Z pole has 21.5% bb-bar and 17.2% cc-bar fractions. The dead-cone effect produces measurably different Lund plane densities for b-quark jets (confirmed by LHCb 2025). The DELPHI splitting analysis explicitly separated quark flavours. The strategy lists no systematic for flavour composition -- not in the systematic table, not in COMMITMENTS.md. I elevate to A because: (i) 22% of the sample has different physics from the remaining 78%, (ii) the correction factors from PYTHIA 6.1 assume the SM flavour mix but the sensitivity is not assessed, and (iii) the omission was caught by all three reviewers independently. The fix is straightforward (reweight MC to vary b-fraction by +/-2%, or split by MC flavour tag). |
| 6 | **Hemisphere assignment violates observable-redefinition convention** | Andrzej B2, Dolores F16 | B, B | **B** | Both reviewers correctly identify that changing the thrust axis from charged-only to energy-flow changes WHAT is measured, violating conventions/unfolding.md lines 136-150. The particle-level definition (Section 2.2) specifies the thrust axis from "all charged particles," so the energy-flow comparison is a cross-check with a different observable, not a systematic. The fix is well-specified: reclassify to cross-check, replace with a thrust-axis resolution systematic (smear and measure hemisphere migration). |
| 7 | **MC reweighting limitation not acknowledged** | Andrzej B3, Dolores F3 | B, B | **B** | Both reviewers note the same limitation: reweighting changes gen-level shapes but holds the detector response fixed, which is approximately correct only when the response is locally linear and reweighting factors are moderate. The strategy states this as a feature ("only the gen-level shape changes") when it is a limitation. Required fix: acknowledge the limitation, add a diagnostic (check that reweighting factors do not exceed ~3x in any bin, verify reco-level shape migrates as expected). |
| 8 | **F5 conflates correction factors with response matrix** | Albert F12, Dolores F9 | C, A | **B** | Albert calls this C (mislabeling), Dolores calls it A (distinct objects requiring separate figures). I assess B. The correction factor C(i,j) is a per-bin scalar; the response matrix R(i,j) is a 100x100 migration probability matrix. These are fundamentally different objects. A journal referee would require both if IBU is presented as a cross-check. The fix is simple: rename F5 to "correction factors," add the response matrix to the additional figures list. Not blocking (the figures are not produced until Phase 4), but must be fixed in the strategy. |
| 9 | **NLL predictions not cited** | Albert F13, Dolores F12 | C, B | **B** | Albert suggests citing Lifson/Salam/Soyez (JHEP 10 (2020) 170); Dolores elevates to B. I concur with B. The NLL Lund plane density predictions exist, are directly relevant, and transform the measurement from a generator-tuning exercise into a quantitative QCD test. The strategy should cite this work and commit to investigating whether numerical predictions are available. This is a <30 min fix (add citation + commitment). |
| 10 | **Secondary Lund plane as maximality gap** | Dolores F6 | B | **C** | Dolores argues the secondary plane should be flagged as a natural extension. I downgrade to C. For Phase 1, the primary plane is the correct focus. The secondary plane requires additional validation infrastructure (different branch-following, separate correction factors, potentially different systematic behavior). Flagging it as a Phase 4 extension is sufficient. However, the strategy should note its existence and feasibility in one sentence. |

### 1.2 Single-Reviewer Findings

| # | Finding | Source | Their Category | Final Category | Rationale |
|---|---------|--------|---------------|----------------|-----------|
| 11 | **Reference table missing CMS (2024), ATLAS-top (2024), LHCb (2025)** | Albert F4 | B | **B** | Valid. Three additional Lund plane measurements have been published since the strategy was drafted. The ATLAS top/W measurement is especially relevant (color-singlet -> qq, closest analog to e+e-). The LHCb measurement demonstrates dead-cone sensitivity in the Lund plane (relevant to finding #5). The strategy must update the reference table and extract systematic programs. |
| 12 | **Published comparison data not extracted** | Andrzej A4 | A | **B** | Andrzej calls this A, citing the methodology requirement to extract published numerical results. I assess B. The methodology says "Extract published numerical results [...] and record them in the strategy artifact." No DELPHI or ATLAS HEPData values are extracted. However, this is a documentation gap, not a physics error. The DELPHI splitting probability is a 1D projection that requires coordinate transformation before comparison, and ATLAS is pp with different jet definitions. The comparison is approximate. Required: extract representative data points from DELPHI (HEPData or digitized) and ATLAS (HEPData), note the caveats, record in strategy. |
| 13 | **Quark/gluon separation via b-tagging** | Dolores F7 | B | **C** | Dolores proposes measuring the Lund plane separately for light-quark-enriched and b-quark-enriched hemispheres using impact parameter tagging. This would double the physics content. However, it is a scope expansion that goes beyond the primary measurement. The b-tagging capability of the archived data and the correction procedure for a flavour-tagged measurement require significant investigation. I classify as C: note the opportunity in the strategy and flag for feasibility study in Phase 2. The primary measurement must work first. |
| 14 | **"aftercut" pre-selection not investigated** | Andrzej B7 | B | **B** | Valid. The data files are labeled "aftercut" but the strategy does not document what cuts were pre-applied, whether they bias the Lund plane, or whether MC has identical pre-cuts. The tgenBefore tree scope is also ambiguous (all generated events, or only those passing some pre-selection?). This directly affects the efficiency correction. Required: add an explicit Phase 2 deliverable to investigate and document the pre-selection. |
| 15 | **Bin-by-bin as primary method weakly motivated** | Albert F5 | B | **B** | Albert argues that the current framing (bin-by-bin primary, IBU cross-check) puts the burden of proof on the wrong method. The four modern Lund plane measurements all use IBU. The only substantive argument for bin-by-bin (excellent resolution) implies the choice is immaterial. I accept as B: the strategy should either promote IBU to co-primary status or commit to presenting whichever method passes stress tests better. The asymmetric framing is not well justified for a 2026 measurement. |
| 16 | **Momentum resolution value possibly wrong by factor 2** | Albert F6 | B | **B** | Albert notes that sigma_p/p^2 ~ 0.6e-3 is the combined TPC+ITC+VDET resolution, while TPC-only is 1.2e-3. For archived data, it is unclear which tracking detectors contribute. Using the wrong resolution by 2x underestimates momentum smearing. Required: verify which detectors contribute to the archived track reconstruction and cite the correct resolution. |
| 17 | **Neutral-particle contamination in thrust axis** | Albert F8 | B | **B** | The archived data may compute thrust from energy-flow objects (charged+neutral). If so, the thrust axis definition at detector level includes neutrals while the Lund plane uses only charged tracks. This is related to finding #6 but distinct: it concerns what the archived data already contains, not what the analyst chooses. Required: determine the thrust axis source in the archived data and handle consistently. |
| 18 | **Binned density formula with explicit bin widths not stated** | Albert F9 | B | **C** | The continuous formula is correct. The discrete binning formula (dividing by Delta_x * Delta_y) is standard and will be implemented in code. Writing it out explicitly is good practice but not physics-critical. Downgrade to C: add the explicit discrete formula. |
| 19 | **Stress test tilt axes/form unspecified** | Albert F10 | B | **B** | Valid. "Tilts of 5%, 10%, 20%, 50%" without specifying what is tilted (ln k_T? angle? 2D?) is incomplete. The conventions require graded tilts. Required: specify tilts independently in both Lund coordinates plus a 2D correlated tilt, and state the functional form. |
| 20 | **Selection approaches limited independence** | Andrzej B1 | B | **C** | At high thrust (>0.7), thrust hemispheres and Durham 2-jets agree on >90% of particle assignments. The "qualitative difference" is in the soft, wide-angle particles. This is a valid observation but the Phase 1 requirement (two approaches, MVA infeasibility documented) IS met. The characterization should be tempered. Downgrade to C: add a sentence acknowledging the limited independence at high thrust. |
| 21 | **Response matrix definition for IBU non-standard** | Andrzej B4 | B | **B** | The strategy's definition of R(i,j) conflates event-level and splitting-level information. For IBU, the response matrix must be a proper migration probability matrix (each row sums to <=1). The bin-level approach is a specific choice that must be validated. Required: clarify the IBU response matrix definition and ensure it satisfies the mathematical requirements. |
| 22 | **No methodology diagram planned** | Andrzej B5 | B | **C** | A Lund plane construction diagram would be helpful but is a documentation item for the analysis note, not a strategy-blocking finding. The figures are produced in Phase 4 / Doc phases. Downgrade to C: add a methodology diagram to the additional figures list. |
| 23 | **Tracking efficiency 1% drop not properly cited** | Andrzej B6, Dolores F4 | B, B | **B** | Both note the circular reasoning: 0.7% is the systematic on tracking efficiency, not the inefficiency itself. The 1% drop should be justified as a specific multiple of the measured inefficiency from the ALEPH detector paper. Required: cite the actual per-track efficiency and justify the 1% drop rate. |
| 24 | **Perturbative/non-perturbative region not delineated** | Dolores F1 | B | **C** | Dolores requests explicit identification of which Lund plane regions are perturbative, non-perturbative, and resolution-limited. This is a useful addition to the physics motivation but not strategy-blocking. Phase 2 exploration will determine this quantitatively. Downgrade to C. |
| 25 | **No flagship figure with analytical LO overlay** | Dolores F10 | B | **C** | Dolores notes that no flagship figure shows the LO analytical prediction overlaid on data. This is a valid presentation suggestion, but the figure content is defined at strategy level and produced at Doc phases. The strategy already identifies the LO comparison in Section 10.2 and lists projection figures (F3, F4). Downgrade to C: modify F3 description to include LO overlay. |
| 26 | **"First e+e-" claim needs "full 2D" qualification** | Dolores F14 | B | **B** | Valid. The DELPHI splitting probability is a 1D Lund plane projection. The novelty claim should consistently say "first full two-dimensional primary Lund jet plane density." Imprecise framing that a journal referee would flag. |
| 27 | **Thrust > 0.7 cut potentially biases Lund plane** | Albert F11 | C | **C** | Valid suggestion. Multi-jet events (T < 0.7) have different Lund plane densities. The systematic variation (thrust 0.6-0.8) partially covers this. The suggestion to present with and without the cut is reasonable. Accept as C. |
| 28 | **LO prediction needs charged-particle correction** | Andrzej C1 | C | **C** | Valid. The LO formula is for all-particle emissions; the charged-particle density is lower by ~60-70%. This correction should be noted alongside the LO estimate. Accept as C. Note this compounds with finding #1 (factor-2 error). |
| 29 | **Sherpa "if feasible" is not a commitment** | Andrzej C2, Dolores F13 | C, C | **C** | Both reviewers note this. Either commit or document why infeasible. Accept as C. |
| 30 | **Control observable (thrust)** | Andrzej C3 | C | **C** | Adding a well-known observable as end-to-end validation would be powerful. Accept as C suggestion. |
| 31 | **Modern methodology search not documented** | Andrzej C4 | C | **C** | The retrieval log shows modern references came from training knowledge, not actual search. Accept as C: document the search queries. |
| 32 | **Phase 2 binning deliverables should be explicit** | Andrzej C5 | C | folded into #4 | Absorbed into finding #4. |
| 33 | **Running alpha_s slope estimate** | Dolores F2 | C | **C** | Accept as C suggestion. |
| 34 | **Event selection systematic ranges not motivated** | Dolores F5 | C | **C** | Accept as C. |
| 35 | **Three-jet gluon Lund plane** | Dolores F8 | C | **C** | Accept as C (future extension). |
| 36 | **Data/MC ratio format for F2** | Dolores F11 | C | **C** | Accept as C. |
| 37 | **MC stat uncertainty per bin not estimated** | Dolores F15 | C | **C** | Accept as C. |
| 38 | **Lowest ln(k_T) bins below detector sensitivity** | Dolores F17 | C | **C** | Accept as C: Phase 2 deliverable to evaluate. |
| 39 | **Explicit normalization formula** | Dolores F18 | C | **C** | Accept as C. |

### 1.3 Findings Missed by All Reviewers

| # | Finding | Category | Rationale |
|---|---------|----------|-----------|
| 40 | **Double-counting of model dependence and unfolding method systematics.** The systematic table lists both "MC model dependence" (reweighting) and "Unfolding method" (bin-by-bin vs IBU difference). If IBU uses the same PYTHIA 6.1 response matrix, these two sources share the same underlying model dependence and are not independent. The total uncertainty envelope would double-count the same effect. | **B** | Andrzej's conventions audit (bottom of his review) mentions this as a "gap" but does not assign it a finding ID or category. No reviewer formally raised it. The strategy must discuss how these two systematic sources will be kept orthogonal. |
| 41 | **The correction factor formula (Section 6.1) is ambiguous about whether N_gen uses tgen or tgenBefore.** The strategy defines C(i,j) = N_gen(i,j) / N_reco(i,j), but does not specify whether N_gen counts splittings from events in tgen (post-selection) or tgenBefore (pre-selection). If tgen, the correction factors do not include event-level efficiency. If tgenBefore, they include efficiency but the denominator (reco splittings) only comes from selected events. The efficiency correction (Section 6.3) says it is "folded into" C(i,j), but the formula does not show this. | **B** | This ambiguity could lead to either missing the efficiency correction or double-counting it. The formula must be made explicit: either C(i,j) = N_gen_before(i,j) / N_reco(i,j) for a combined correction, or separate efficiency and resolution corrections must be defined. |

---

## 2. Reviewer Diagnostic

### 2.1 Albert (Physics)

**Coverage:** Excellent. Caught the factor-2 LO error (unique among reviewers), the hardness variable ambiguity, the coordinate convention mismatch, and the missing b-quark systematic. Also identified three incomplete reference analyses. The physics knowledge is deep and specific.

**Severity calibration:** Well-calibrated. Three genuine A findings, all verified. B findings are substantive. C suggestions are constructive.

**Blind spots:** Did not check conventions/unfolding.md compliance (observable-redefinition pitfall). Did not flag the aftercut pre-selection issue. Did not notice the double-counting potential for model dependence and unfolding systematics.

**Overall:** Strongest on foundational physics. This review alone would catch the most dangerous errors.

### 2.2 Andrzej (Critical)

**Coverage:** Very thorough. Identified 16 findings spanning observable definition, binning, systematics, conventions compliance, COMMITMENTS audit, and decision label audit. The conventions coverage audit and reference analysis parity check are particularly valuable.

**Severity calibration:** Slightly aggressive. A2 (binning) elevated to A when B is more appropriate (Phase 2 can resolve). A4 (published data extraction) elevated to A; the methodology does require extraction, but the absence is a documentation gap rather than a physics error. Other assessments are well-calibrated.

**Blind spots:** Did not catch the factor-2 LO error. Did not identify the momentum resolution ambiguity (TPC-only vs combined). Did not flag the neutral-particle thrust axis issue.

**Overall:** Strongest on process compliance and conventions. The conventions audit table is the most useful single artifact in any review.

### 2.3 Dolores (Constructive)

**Coverage:** Broad. 18 findings spanning all six evaluation axes. The information recovery suggestions (secondary plane, quark/gluon separation) add genuine physics value. The figure conflation finding (F9) is well-argued.

**Severity calibration:** Generally appropriate for the constructive role. Only one A finding (F9, figure conflation), which I assessed as B. The B findings are a mix of genuine issues (F3, F12, F16) and scope-expansion suggestions (F6, F7) that I downgraded.

**Blind spots:** Did not catch the factor-2 LO error. Did not flag the binning justification gap. Did not identify the aftercut pre-selection issue or the momentum resolution ambiguity.

**Overall:** Strongest on maximality and presentation. The constructive frame surfaces opportunities the other reviewers miss.

### 2.4 Cross-Reviewer Coverage Matrix

| Topic | Albert | Andrzej | Dolores | Covered? |
|-------|--------|---------|---------|----------|
| LO formula error | F1 (A) | -- | -- | 1/3 |
| Hardness variable | F2 (A) | A1 (A) | -- | 2/3 |
| Coordinate convention | F3 (A) | A1 (partial) | -- | 2/3 |
| Binning justification | -- | A2 (A) | -- | 1/3 |
| Heavy flavour | F7 (B) | A3 (A) | F7 (B) | 3/3 |
| Observable redef. | -- | B2 (B) | F16 (B) | 2/3 |
| MC reweighting limit | -- | B3 (B) | F3 (B) | 2/3 |
| Correction/response conflation | F12 (C) | -- | F9 (A) | 2/3 |
| NLL predictions | F13 (C) | -- | F12 (B) | 2/3 |
| Reference table gaps | F4 (B) | -- | -- | 1/3 |
| Published data extraction | -- | A4 (A) | -- | 1/3 |
| Aftercut pre-selection | -- | B7 (B) | -- | 1/3 |
| Momentum resolution | F6 (B) | -- | -- | 1/3 |
| Neutral thrust axis | F8 (B) | -- | -- | 1/3 |
| Secondary plane | -- | -- | F6 (B) | 1/3 |
| Double-counting syst. | -- | (audit note) | -- | 0/3 |
| Efficiency formula ambiguity | -- | -- | -- | 0/3 |

**Assessment:** The three reviews have good complementarity. No single reviewer would have caught all the important issues. The physics reviewer is uniquely positioned for formula-level errors; the critical reviewer for process compliance; the constructive reviewer for scope and presentation.

---

## 3. Verdict

**ITERATE.**

### 3.1 Justification

The strategy is fundamentally sound -- the measurement is well-motivated, the data inventory is thorough, and the overall structure is above average for a first-draft strategy. However, the review panel has identified 5 Category A findings and 13 Category B findings that must be resolved before the strategy can pass.

The Category A findings are particularly concerning because they affect the observable definition and benchmarking formula -- the foundational elements that every downstream phase depends on:

1. The LO formula is wrong by a factor of 2 (finding #1)
2. The hardness variable is asserted as "standard" without verification (finding #2)
3. The coordinate adaptation from pp is not transparent (finding #3)
4. A systematic affecting 22% of the sample is entirely missing (finding #5)

These are not cosmetic issues. If the fixer writes code using energy ordering and calibrates against rho ~ 0.050, every closure test and validation comparison in Phases 2-4 will be biased. The observable definition must be nailed down now.

### 3.2 Category A Findings (Must Resolve)

These block advancement. The fixer must address all 5.

| Priority | # | Finding | Action Required |
|----------|---|---------|-----------------|
| 1 | 1 | LO formula wrong by factor 2 | Correct to rho ~ 2*alpha_s*C_F/pi. Propagate numerical estimate (~0.100 for all-particle; note charged-particle correction). |
| 2 | 2 | Hardness variable not verified | Retrieve Dreyer/Salam/Soyez paper (web/arXiv). Compare term-by-term. Document differences. Commit to p_T ordering as primary (matching theory/pp) with energy ordering as systematic variation, or justify the alternative with explicit citation. Remove "standard choice" claim. |
| 3 | 3 | Coordinate adaptation not transparent | Rewrite Sections 2.2 and 5.3 to: (a) distinguish e+e- definition from pp, (b) state that sin(theta) is used in k_T, (c) note regime of validity for cross-collider comparisons. |
| 4 | 5 | Missing heavy flavour systematic | Add to systematic table and COMMITMENTS.md. Evaluation: reweight MC b-fraction by +/-2% (R_b precision), or split MC by flavour tag and quantify b-quark contribution per bin. |
| 5 | 4 | Uniform binning not justified | Cite ATLAS/ALICE binning. Justify uniform as starting point (or adopt non-uniform). Add Phase 2 deliverables: migration fraction per bin, resolution vs bin width, bin population study. |

### 3.3 Category B Findings (Must Fix Before PASS)

These weaken the analysis and must be resolved. The fixer should address all 13 in the same iteration.

| Priority | # | Finding | Action Required |
|----------|---|---------|-----------------|
| 1 | 6 | Hemisphere assignment violates conventions | Reclassify from systematic to cross-check. Add thrust-axis resolution systematic (smear momenta, measure hemisphere migration). Update COMMITMENTS.md. |
| 2 | 7 | MC reweighting limitation not acknowledged | Acknowledge limitation. Add diagnostic: if reweighting factors > 3x, verify reco-level shape migration. |
| 3 | 40 | Double-counting model dependence / unfolding method | Discuss how MC model dependence and unfolding method systematics will be kept orthogonal. |
| 4 | 41 | Efficiency correction formula ambiguous | Clarify whether C(i,j) uses tgen or tgenBefore. Write explicit formula showing efficiency folding. |
| 5 | 8 | F5 conflates correction factors / response matrix | Rename F5 to "correction factor map." Add response matrix to additional figures. |
| 6 | 9 | NLL predictions not cited | Cite Lifson/Salam/Soyez (JHEP 10 (2020) 170). Commit to investigating numerical predictions for e+e-. |
| 7 | 11 | Reference table incomplete | Add CMS (2024), ATLAS top/W (2024), LHCb (2025). Extract systematic programs. Discuss ATLAS top relevance for e+e-. |
| 8 | 12 | Published comparison data not extracted | Extract representative data points from DELPHI (HEPData/digitized) and ATLAS (HEPData). Record in strategy with caveats. Add COMMITMENTS.md entry. |
| 9 | 14 | Aftercut pre-selection not investigated | Add Phase 2 deliverable: investigate and document pre-cuts, verify MC has identical pre-cuts, determine tgenBefore scope. |
| 10 | 15 | Bin-by-bin primary weakly motivated | Either promote IBU to co-primary or commit to presenting whichever passes stress tests better. Acknowledge that all modern measurements use IBU. |
| 11 | 16 | Momentum resolution possibly wrong by 2x | Verify which tracking detectors (TPC-only vs TPC+ITC+VDET) contribute to archived tracks. Cite correct resolution. |
| 12 | 17 | Neutral thrust axis not addressed | Determine whether archived data thrust uses energy-flow or charged-only. Handle consistently (recompute if needed, or include as systematic). |
| 13 | 19 | Stress test tilts unspecified | Specify tilts independently in both Lund coordinates + 2D correlated tilt. State functional form (e.g., w(x) = 1 + epsilon*(x - x_mean)). |
| 14 | 21 | IBU response matrix definition non-standard | Clarify as proper migration probability matrix (rows sum to <=1). Validate bin-population approach. |
| 15 | 23 | Tracking efficiency 1% not properly cited | Cite actual ALEPH per-track efficiency from detector paper. Justify 1% as specific multiple of measured inefficiency uncertainty. |
| 16 | 26 | "First" claim needs "full 2D" qualification | Consistently use "first full two-dimensional primary Lund jet plane density" throughout. |

### 3.4 Category C Findings (Apply Before Commit)

These are suggestions. Apply as many as practical before final commit. No re-review needed.

Findings #10, #13, #18, #20, #22, #24, #25, #27, #28, #29, #30, #31, #33, #34, #35, #36, #37, #38, #39.

Key C items to prioritize:
- #28: Note charged-particle correction to LO prediction (compounds with A finding #1)
- #10: Add one sentence noting secondary Lund plane feasibility
- #18: Write out explicit discrete binned formula
- #22: Add methodology diagram to additional figures
- #25: Add LO overlay to F3 description
- #29: Commit to Sherpa or document infeasibility concretely

---

## 4. COMMITMENTS.md Update Requirements

The fixer must add the following to COMMITMENTS.md:

- [ ] Heavy flavour composition systematic (b-quark mass effect)
- [ ] Published comparison data extraction (DELPHI HEPData + ATLAS HEPData)
- [ ] Thrust-axis resolution systematic (replacing hemisphere assignment as systematic)
- [ ] NLL prediction comparison (Lifson/Salam/Soyez 2020)
- [ ] Phase 2 binning optimization deliverables (migration fraction, resolution study)
- [ ] Phase 2 aftercut pre-selection investigation

The existing "Hemisphere assignment" line should be reclassified as a cross-check.

---

## 5. Process Notes

- The strategy executor (Fabiola) produced a well-structured artifact that covers all required elements. The self-critique round caught several issues but missed the factor-2 formula error and the hardness variable ambiguity.
- The retrieval log shows no evidence that the foundational paper (Dreyer/Salam/Soyez) was actually fetched and compared. This is the specific failure mode the methodology guards against.
- The 4-bot review panel worked effectively: good complementarity, minimal redundancy, three genuinely different perspectives.
- The iteration count is 0. The arbiter expects one fix iteration to resolve all A and B findings, provided the fixer systematically addresses the prioritized list above.
