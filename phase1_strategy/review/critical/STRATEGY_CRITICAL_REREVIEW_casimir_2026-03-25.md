# Critical Re-Review: Phase 1 Strategy -- Lund Jet Plane Density

**Reviewer:** Casimir (re-review) | **Date:** 2026-03-25
**Artifact:** `phase1_strategy/outputs/STRATEGY_peter_2026-03-25_17-17.md`
**Arbiter verdict under review:** `STRATEGY_ARBITER_sally_2026-03-25.md` (5A, 16B)
**Fixer session:** Peter, 2026-03-25

---

## 1. Finding-by-Finding Verification

### 1.1 Category A Findings (5)

| # | Finding | Status | Notes |
|---|---------|--------|-------|
| 1 | LO formula wrong by factor 2 | **RESOLVED** | Corrected throughout: Section 10.2 now reads rho_LO = 2 * alpha_s(k_T) * C_F / pi, numerical estimate ~0.100 all-particle and ~0.067 charged-particle. The derivation explicitly cites Eq. 2.6 and explains the factor of 2 from the splitting function. Propagated to Section 3.3, F3 description, and COMMITMENTS.md comparison targets. No residual instances of the old value (0.050) found in the artifact. |
| 2 | Hardness variable not verified against foundational paper | **RESOLVED** | Section 2.2 now explicitly quotes Dreyer/Salam/Soyez 2018 Section 2.1 definition ("labelled such that p_{ta} > p_{tb}"). p_T ordering adopted as primary [D13]. Energy ordering designated as systematic variation. The "standard choice for e+e-" claim is removed and replaced with the explicit statement: "No such standard exists in the literature." The retrieval log (Section 14.3) documents the web search that retrieved the foundational paper. Sections 5.2 and 6.1 are consistent with p_T ordering. |
| 3 | Coordinate adaptation from pp not transparent | **RESOLVED** | Section 2.2 now contains a term-by-term comparison of pp and e+e- coordinate definitions, including quantitative estimates of the sin(Delta_theta) vs Delta_theta divergence (16% at 1 rad). Section 5.3 provides a parallel comparison table. The cross-collider validity regime is stated explicitly (collinear region only, ln 1/Delta > ~1). The treatment is thorough and correct. |
| 4 | Uniform binning not justified (arbiter downgraded to B, but tracked in A list by priority) | **RESOLVED** | Section 2.2 now cites ATLAS, CMS, and ALICE non-uniform binning as context, justifies uniform as a resolution-study-free starting point, and commits to five specific Phase 2 binning deliverables (migration fraction per bin, resolution vs bin width, bin population, non-uniform evaluation, side-by-side comparison). COMMITMENTS.md contains a matching Phase 2 deliverable line. The justification is adequate: uniform is defensible as a baseline provided Phase 2 delivers the optimization study. |
| 5 | Missing heavy flavour systematic | **RESOLVED** | Added to the systematic table (Section 7.2) with specific evaluation method (reweight MC b-fraction by +/-2%), citing the PDG R_b value and the LHCb 2025 dead-cone evidence. The expected magnitude (1-5%, largest in collinear region) is physics-motivated. Present in COMMITMENTS.md. The LHCb reference is also added to the reference table (Section 8.5). |

**Category A verdict: All 5 findings properly resolved.**

### 1.2 Category B Findings (16)

| # | Finding | Status | Notes |
|---|---------|--------|-------|
| 6 | Hemisphere assignment violates conventions (observable redefinition) | **RESOLVED** | Section 7.3 explicitly reclassifies hemisphere assignment (charged+neutral vs charged-only thrust axis) from systematic to cross-check, citing conventions/unfolding.md lines 136-150. Thrust-axis resolution systematic (smear momenta, measure hemisphere migration) added to Section 7.2 as the replacement. COMMITMENTS.md cross-checks section lists hemisphere assignment as a cross-check. COMMITMENTS.md systematic sources section lists thrust-axis resolution as a systematic. Consistent. |
| 7 | MC reweighting limitation not acknowledged | **RESOLVED** | The MC model dependence entry in Section 7.2 now includes an explicit "Limitation acknowledged" paragraph and a diagnostic: if reweighting factors exceed 3x, the linear-response assumption is flagged and verified by comparing predicted vs actual reco-level distributions. COMMITMENTS.md validation tests include the reweighting diagnostic. |
| 40 | Double-counting model dependence / unfolding method systematics | **RESOLVED** | New Section 6.2 discusses orthogonality: model dependence probes truth-shape sensitivity while unfolding method probes inversion-procedure sensitivity. The envelope rule is stated: if cross-terms exceed the quadrature sum, the larger envelope is taken. This is a sound approach. COMMITMENTS.md unfolding method entry references Section 6.2. |
| 41 | Efficiency correction formula ambiguous (tgen vs tgenBefore) | **RESOLVED** | Section 6.1 now explicitly defines C(i,j) = N_gen_before(i,j) / N_reco(i,j) using tgenBefore (pre-selection), with a clear explanation of how this folds event-level efficiency into the bin-by-bin factor. Section 6.3 further elaborates and gives the separate IBU efficiency formula: epsilon(i,j) = N_gen(i,j) / N_gen_before(i,j). The formulas are internally consistent and avoid double-counting. |
| 8 | F5 conflates correction factors with response matrix | **RESOLVED** | F5 is renamed "Correction factor map (2D)" in Section 9. The response matrix is listed separately under "Additional figures (not flagship, but required)." The two objects are clearly distinguished. |
| 9 | NLL predictions not cited | **RESOLVED** | Lifson/Salam/Soyez (JHEP 10 (2020) 170) is cited in Sections 2.1, 3.3, and the new Section 10.3. The commitment to investigate numerical predictions for e+e- is documented. COMMITMENTS.md comparison targets include the NLL prediction entry. |
| 11 | Reference table missing CMS (2024), ATLAS top/W (2024), LHCb (2025) | **RESOLVED** | Sections 8.2 (CMS), 8.4 (ATLAS top/W), and 8.5 (LHCb) are added with systematic program details. The ATLAS top/W entry correctly identifies the W -> qq Lund plane as the closest pp analog to Z -> qq (colour-singlet quark radiation). The LHCb entry links to finding #5 (dead-cone). |
| 12 | Published comparison data not extracted | **RESOLVED** | Section 3.4 documents extraction plans for DELPHI, ATLAS, and CMS HEPData with explicit caveats (different jet definitions, coordinate transformations, approximate comparisons). COMMITMENTS.md comparison targets include DELPHI, ATLAS, and CMS HEPData entries. The caveats are specific and correct (Durham vs C/A, pp vs e+e-, all-particle vs charged). |
| 14 | Aftercut pre-selection not investigated | **RESOLVED** | Section 3.1 contains three specific Phase 2 investigation items: (a) determine what "aftercut" encodes, (b) verify MC has identical pre-cuts, (c) determine tgenBefore scope. COMMITMENTS.md Phase 2 deliverables includes the aftercut investigation. |
| 15 | Bin-by-bin as primary method weakly motivated | **RESOLVED** | Section 6.1 now frames bin-by-bin and IBU as co-primary methods. The method parity assessment (Section 8.7) explicitly acknowledges that all four modern measurements use IBU. The result selection criterion is stated: whichever passes stress tests better, with IBU as default if both pass equivalently. This is a sound resolution. |
| 16 | Momentum resolution possibly wrong by factor 2 | **RESOLVED** | Section 7.2 (Track momentum resolution entry) now discusses both TPC-only (sigma_p/p^2 ~ 1.2e-3) and combined TPC+ITC+VDET (~ 0.6e-3) resolutions. A Phase 2 diagnostic is committed: check impact parameter resolution (sigma_d0 ~ 25 um for combined vs ~150 um for TPC-only) to determine which detectors contribute to archived tracks. COMMITMENTS.md Phase 2 deliverables includes momentum resolution verification. |
| 17 | Neutral-particle contamination in thrust axis | **RESOLVED** | Section 7.2 includes a "Neutral thrust axis" entry documenting the issue. Notes that the archived data contains multiple thrust variants (Thrust, ThrustCharged, ThrustCorrected). Phase 2 investigation committed to determine the source and handle consistently. COMMITMENTS.md Phase 2 deliverables and systematic sources both reference this. |
| 19 | Stress test tilt axes/form unspecified | **RESOLVED** | Section 7.1 (Stress test row) and Section 12.1 (Stress test entry) now specify: tilts applied independently in ln(1/Delta_theta), ln(k_T), and as a 2D correlated product tilt w(x,y) = w_x(x) * w_y(y). Functional form: w(x) = 1 + epsilon * (x - x_mean) / (x_max - x_mean). Epsilon values: 0.05, 0.10, 0.20, 0.50. COMMITMENTS.md validation test entry matches. This is precisely what was requested. |
| 21 | Response matrix definition for IBU non-standard | **RESOLVED** | Section 6.1 (Method B: IBU) now defines R(i,j -> k,l) as a proper migration probability matrix with each row summing to <= 1 (deficit = efficiency loss). The matching strategy is bin-level population [D12], avoiding the 1:1 object matching pitfall. This is mathematically correct. |
| 23 | Tracking efficiency 1% drop not properly cited | **RESOLVED** | Section 7.2 (Tracking efficiency entry) now cites ALEPH NIM A 360 (1995) 481-506, Table 3. Per-track efficiency ~98.5% for isolated tracks with p > 200 MeV/c. The 0.7% from TPC hit variation (cds_2876991) is correctly identified as the systematic uncertainty on the efficiency, not the inefficiency itself. The 1% drop is justified as ~1 sigma above the measured ~1.5% per-track inefficiency. COMMITMENTS.md matches. |
| 26 | "First e+e-" claim needs "full 2D" qualification | **RESOLVED** | The summary (Section 1), Section 2.3, and cross-references consistently use "first full two-dimensional primary Lund jet plane density." No unqualified "first" claims remain. |

**Category B verdict: All 16 findings properly resolved.**

### 1.3 Category C Findings Applied

The fixer applied 6 Category C findings (as documented in the fixer log). These are not blocking but I verify their correctness:

| # | Finding | Status | Notes |
|---|---------|--------|-------|
| 28 | Charged-particle correction to LO | Correctly applied | Section 10.2 discusses the ~2/3 charged fraction, estimates rho_charged ~ 0.067. The caveat about fragmentation-model dependence is noted. |
| 10 | Secondary Lund plane | Correctly applied | One sentence in Section 2.1 notes secondary plane feasibility and scope limitations. |
| 18 | Discrete binned formula | Correctly applied | Section 2.2 includes explicit formula rho(i,j) = (1/N_jet) * n(i,j) / (Delta_x_i * Delta_y_j). |
| 22 | Methodology diagram | Correctly applied | Listed in additional figures. |
| 25 | LO overlay on F3 | Correctly applied | F3 description in Section 9 includes "LO analytical prediction rho_LO = 2 * alpha_s(k_T) * C_F / pi (corrected for charged-particle fraction, see Section 10.2) as a reference line." |
| 29 | Sherpa commitment | Correctly applied | Concrete plan: attempt 10k events in Phase 2 [D14], document if infeasible. |

---

## 2. COMMITMENTS.md Consistency Check

The arbiter (Section 4) required six specific additions to COMMITMENTS.md. Verification against the current file:

| Required Addition | Present? | Notes |
|---|---|---|
| Heavy flavour composition systematic | Yes | Line: "Heavy flavour composition: reweight MC b-fraction by +/-2%..." |
| Published comparison data extraction (DELPHI + ATLAS HEPData) | Yes | DELPHI, ATLAS, and CMS listed under Comparison targets |
| Thrust-axis resolution systematic (replacing hemisphere assignment) | Yes | Listed under Systematic sources; hemisphere reclassified under Cross-checks |
| NLL prediction comparison (Lifson/Salam/Soyez 2020) | Yes | Listed under Comparison targets |
| Phase 2 binning optimization deliverables | Yes | Listed under Phase 2 deliverables |
| Phase 2 aftercut pre-selection investigation | Yes | Listed under Phase 2 deliverables |
| Hemisphere assignment reclassified as cross-check | Yes | Listed under Cross-checks with explicit "(reclassified from systematic to cross-check per conventions/unfolding.md)" |

**All arbiter-mandated COMMITMENTS.md updates are present.**

Additional consistency checks:

- **Systematic sources:** 14 entries, all matching strategy Section 7.2. Neutral thrust axis and hardness variable entries present.
- **Validation tests:** 9 entries, all matching strategy Section 12.1. MC reweighting diagnostic present.
- **Flagship figures:** 6 entries (F1-F6), matching strategy Section 9. F5 correctly labeled as "Correction factor map."
- **Additional figures:** Response matrix and methodology diagram present, matching strategy.
- **Cross-checks:** 5 entries, including hemisphere assignment reclassification. Bin-by-bin vs IBU listed as "(co-primary methods)" which is consistent with strategy Section 6.1.
- **Comparison targets:** 7 entries. LO formula correctly states "rho ~ 2 * alpha_s * C_F / pi" with both all-particle (~0.100) and charged-particle (~0.067) estimates.
- **Phase 2 deliverables:** 6 entries covering binning, aftercut, momentum resolution, neutral thrust axis, Sherpa, and hardness variable. All match strategy commitments.

**COMMITMENTS.md is internally consistent with the strategy.**

---

## 3. New Issues Introduced by Fixes

I have examined the fixed strategy for regressions or new problems introduced by the fixer's changes.

### 3.1 Potential Issue: CMS and ALICE reference collision

In Section 8.2 (CMS) and Section 8.3 (ALICE), the citation is listed as "JHEP 05 (2024) 116" for both. This appears to be a citation collision -- CMS and ALICE cannot have published in the same journal volume and page. One of these citations is likely incorrect.

**Assessment: Category C.** This is a bibliographic error that does not affect physics content. The arXiv numbers are distinct (CMS: arXiv:2312.16343 for CMS; ALICE likely has a different arXiv ID). The actual physics content and systematic programs extracted from each reference are correct and clearly refer to different experiments. This should be corrected before the strategy is committed, but does not require re-review.

### 3.2 Potential Issue: Charged-particle fraction estimate

Section 10.2 states the charged-particle fraction is "approximately 2/3 (from isospin: pi+, pi-, pi0 are produced in roughly equal numbers, and pi0 -> gamma gamma is neutral)." This isospin argument gives 2/3 for pions only; when kaons, protons, and other species are included, the charged fraction may differ. The PYTHIA 8 Monash tune at the Z pole gives a charged-particle fraction of approximately 60-65% for the energy-weighted sum entering the Lund plane.

**Assessment: Category C.** The estimate is order-of-magnitude correct and the text explicitly notes it is approximate ("the actual charged fraction depends on the fragmentation model and the k_T scale"). The LO overlay is a qualitative reference line, not a precision prediction. No action needed.

### 3.3 Potential Issue: IBU efficiency formula consistency

Section 6.3 gives the IBU efficiency factor as epsilon(i,j) = N_gen(i,j) / N_gen_before(i,j). This is applied after unfolding: rho_corrected = rho_unfolded / epsilon(i,j). However, the IBU response matrix in Section 6.1 is constructed from matched gen/reco events (implicitly post-selection), meaning events that fail selection are already excluded from the response matrix. The deficit from rows summing to < 1 accounts for reco-level losses (tracking, migration out of acceptance), but not for gen-level event selection losses.

The formula chain is: IBU unfolds reco -> gen (post-selection), then epsilon corrects gen (post-selection) -> gen (pre-selection). This is the standard two-step approach and is mathematically correct, provided the response matrix is built from post-selection MC only (tgen matched to t, not tgenBefore). The strategy says the response matrix maps gen -> reco for "individual splittings" using bin-level matching, which implicitly uses post-selection events. The chain is consistent.

**Assessment: No issue.** The two-step IBU approach is correctly formulated. The bin-by-bin approach uses tgenBefore in the numerator to combine both steps. Both yield the same result if the response is locally linear and the efficiency is bin-factorizable. This is sound.

### 3.4 Check: Decision label completeness

The strategy defines 14 decision labels [D1]-[D14]. Each is documented in Section 11.3. The [A] and [L] labels are in Sections 11.1 and 11.2 respectively. No decision is referenced in the text without a corresponding definition.

**Assessment: No issue.**

### 3.5 Check: Internal consistency of bin-by-bin vs IBU framing

The strategy calls both methods "co-primary" (Section 6.1) and states "the result will be presented using whichever method passes stress tests better." COMMITMENTS.md lists "Alternative correction method comparison: bin-by-bin vs IBU as co-primary methods (agreement within 2-sigma or investigated)" under validation tests. This is internally consistent. The Section 8.7 method parity assessment correctly notes that if both pass equivalently, IBU will be primary. No contradiction.

### 3.6 Check: Retrieval log completeness

Section 14.3 documents the fixer's web searches (Dreyer/Salam/Soyez 2018, Lifson/Salam/Soyez 2020, CMS 2024, ATLAS top/W 2024, LHCb 2025). The arbiter's finding #2 required the foundational paper to be "retrieved and compared term-by-term." The retrieval log confirms this was done. The experiment log (fixer section) provides additional detail on the term-by-term comparison.

**Assessment: No issue.**

---

## 4. Overall Assessment

### 4.1 Strengths of the fixed strategy

1. **The foundational physics is now correct.** The LO formula, hardness variable, coordinate definitions, and cross-collider validity regime are all accurately stated and properly cited.

2. **The systematic plan is comprehensive.** Fourteen systematic sources are enumerated, including the previously missing heavy flavour composition. The conventions/unfolding.md enumeration is complete ("Will implement" or "Not applicable" for every entry).

3. **The correction strategy is sound.** The co-primary bin-by-bin + IBU approach is well-motivated, with proper formulas, clear efficiency treatment, and an orthogonality discussion for potential double-counting.

4. **COMMITMENTS.md is complete and consistent.** All arbiter-mandated additions are present. The reclassification of hemisphere assignment from systematic to cross-check is properly executed. Phase 2 deliverables are specific and actionable.

5. **The reference analysis table is thorough.** Six reference analyses spanning ATLAS, CMS, ALICE, LHCb, DELPHI, and ALEPH, with systematic programs extracted and method parity assessed.

### 4.2 Residual minor items (Category C, no re-review needed)

- CMS/ALICE citation collision in Sections 8.2/8.3 (same journal reference for different papers). Fix before commit.
- The charged-particle fraction estimate (2/3) is approximate; the text correctly notes this.

---

## 5. Verdict

**PASS.**

All 5 Category A findings are properly resolved with correct physics content, not just cosmetic patches. All 16 Category B findings are addressed with substantive fixes. No new Category A or Category B issues were introduced by the fixes. COMMITMENTS.md is complete and consistent with the strategy. The strategy is internally coherent and ready to advance to Phase 2.

The single Category C note (CMS/ALICE citation collision) should be corrected before the strategy is committed, but does not require re-review.
