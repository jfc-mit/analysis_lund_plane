# Phase 3 Critical Review: Selection

**Reviewer:** Nadia (critical + plot validator) | **Date:** 2026-03-25
**Artifact:** `SELECTION_ingrid_2026-03-25_19-01.md`
**Executor:** Ingrid

---

## 1. Closure Test Assessment

### 1.1 Self-consistency closure: algebraic identity -- correctly identified

The closure test reports chi2/ndf = 1.99e-28, p-value = 1.000, all pulls = 0.
This is the expected algebraic identity: corrected = N_reco * (N_genBefore/N_reco) = N_genBefore.

**Evidence:** `closure_ingrid.json` confirms chi2 = 1.15e-26 over 58 bins, alarm field = `"suspiciously_good_expected_for_algebraic_identity"`. The script `03_closure_test.py` (line 72-76) computes `n_corrected = h2d_reco * correction` where `correction = h2d_genBefore / h2d_reco`, then normalizes by `n_hemi_genBefore`. This is N_genBefore / N_hemi_genBefore, which is exactly rho_truth. The identity is complete and numerically verified to machine precision.

**Assessment:** The executor correctly identifies this as a tautology (artifact Section 4.2, experiment log entry for 2026-03-25 18:48). The real closure test (split-sample) is appropriately deferred to Phase 4 (artifact Section 8.2, item 1). The alarm band chi2/ndf < 0.1 trigger is handled correctly: flagged as suspicious but explained as expected.

**Finding:** No issue. The closure infrastructure is correctly implemented and the deferral is appropriate per `conventions/unfolding.md` quality gate 1 ("For bin-by-bin correction, a split-sample closure is required").

### 1.2 Closure normalization bug (fixed)

The experiment log (2026-03-25 18:48) documents a bug found and fixed: initial implementation normalized corrected density by N_hemi_reco instead of N_hemi_genBefore, producing a constant ratio of 1.343. The fix is verified in `03_closure_test.py` line 76: `rho_corrected = n_corrected / (n_hemi_genBefore * bin_area)`. This is correct.

**Finding (C):** The normalization discussion is clear and the fix is documented. Suggest noting the 1.343 = genBefore/reco hemisphere ratio explicitly in the artifact for traceability.

---

## 2. Convention Coverage (conventions/unfolding.md)

Row-by-row check against `conventions/unfolding.md`:

| Convention requirement | Status | Evidence |
|----------------------|--------|----------|
| Precise particle-level definition | DONE | Strategy Section 2.2: charged particles, p > 200 MeV/c, c*tau > 1 cm, full 4pi |
| Correction procedure passes validation | PARTIAL | Self-consistency passes (tautology); split-sample deferred to Phase 4 |
| Covariance matrix | DEFERRED | Committed in COMMITMENTS.md; Phase 4 deliverable (N >= 500 bootstrap) |
| Alternative method cross-check | DEFERRED | IBU committed as co-primary; Phase 4 deliverable |
| Literature requirement (>=2 references) | DONE | Strategy cites DELPHI (inspire_1661966), ALEPH (cds_388806), ATLAS, CMS |
| Closure test | PARTIAL | Self-consistency only; split-sample + stress tests deferred to Phase 4 |
| Stress test | DEFERRED | Committed in COMMITMENTS.md; graded tilts specified |
| Prior/model dependence | DEFERRED | Phase 4 deliverable |
| Covariance validation (PSD, condition) | DEFERRED | Phase 4 deliverable |
| Data/MC input validation | DONE | Phase 2 produced 9 data/MC comparison plots; Phase 3 produced Lund plane comparisons |

**Finding (B-1): No Thrust_charged event selection.** The strategy (Section 4.1 and Phase 2 recommendation Section 12.1) committed to using `Thrust_charged` for event selection cuts (consistency with charged-particle observable) while using the energy-flow thrust axis (TTheta, TPhi) for hemisphere splitting. The implementation in `01_process_all.py` line 46 uses `arrays["Thrust"] > 0.7` -- this is the energy-flow thrust, not Thrust_charged. The strategy explicitly recommended Thrust_charged for the event selection cut. While the impact is likely small (Phase 2 found 0.15% mean difference), this is a departure from the committed approach without documented justification.

**Finding (B-2): Missing ntpc >= 4 track cut.** The strategy (Section 4.1) specifies `ntpc >= 4` as a track-level cut, citing inspire_322679 ("ensures well-reconstructed tracks"). The implementation in `01_process_all.py` lines 49-54 applies pwflag == 0, pmag > 0.2, |d0| < 2.0, |z0| < 10.0 -- but there is no ntpc cut. The Phase 2 exploration also does not mention this branch. The ntpc branch may not exist in the archived data, but this omission should be explicitly documented. If the branch is absent, the impact should be assessed (the `aftercut` pre-selection may already enforce this via passesNTrkMin). COMMITMENTS.md lists "vary ntpc from 3 to 5" as a systematic variation, which cannot be evaluated if the branch is unavailable.

---

## 3. Selection Approach Comparison

### 3.1 Two approaches tried: PASS

- **Approach A (primary):** Thrust hemispheres + C/A declustering, p_T-ordered
- **Approach C (cross-check):** Exclusive kT (Durham) 2-jets + C/A declustering

**Evidence:** `approach_comparison_ingrid.json` reports 200,000 events processed, ratio mean = 0.999, std = 0.010, chi2/ndf = 10.56/57 = 0.185. This is quantitative, uses adequate statistics, and the two approaches are qualitatively different (thrust hemispheres vs kT jet clustering).

### 3.2 Quantitative comparison: PASS

The chi2/ndf of 0.185 indicates the approaches are statistically equivalent for Thrust > 0.7 events. The artifact provides a clear justification for choosing Approach A: the two approaches assign particles nearly identically for two-jet topologies.

**Finding (C-1):** The approach comparison uses only data events. A comparison at MC gen-level would verify the approaches agree where detector effects are absent, strengthening the claim. Not blocking.

### 3.3 chi2/ndf suspiciously low?

The chi2/ndf = 0.185 with 57 dof implies p-value ~ 1.0 (the approaches are too similar). This is expected given the Thrust > 0.7 cut selects clean two-jet events where hemisphere and kT jet definitions converge. The approaches become qualitatively different only for multi-jet topologies (Thrust < 0.7), which are excluded. This is physically reasonable and not an alarm.

---

## 4. Data Completeness

### 4.1 All data files processed: PASS

**Evidence:** Artifact Section 8.3 reports "6 data + 40 MC = 46" files processed. Phase 2 inventory lists 6 data files totaling 3,050,610 events. Artifact cutflow (Section 1.3) reports 3,050,610 total data events. All years (1992-1995) are included.

### 4.2 All MC files processed: PASS

**Evidence:** 40 MC files processed. Phase 2 reports 771,597 MC reco events; artifact cutflow reports 771,597 MC total events. All MC is used.

### 4.3 GenBefore sample: PASS

**Evidence:** 973,769 genBefore events (artifact Section 1.3), matching Phase 2 inventory (973,769). The genBefore/gen ratio of 1.262 is consistent across phases.

---

## 5. Correction Infrastructure

### 5.1 Correction factors

**Evidence from `correction_summary_ingrid.json`:**
- Mean: 1.680, median: 1.468
- Range: [1.166, 6.667]
- 4 bins with C > 2 (kinematic boundaries)
- 0 bins with C < 0.5

The median of ~1.47 is consistent with the event selection efficiency correction (~1/0.79 = 1.27) plus detector effects. The maximum of 6.67 is at kinematic boundaries where statistics are poor. The convention guideline of 0.8-5x is slightly exceeded in 1 bin (C = 6.67).

**Finding (B-3): One correction factor exceeds 5x.** The artifact reports max C = 6.667, exceeding the plausible range guideline of 0.8-5x from the review focus. This single bin is at a kinematic boundary with poor statistics (likely the highest ln(k_T) or most collinear bin). The bin should be identified and its statistical uncertainty quantified. If the bin has fewer than ~10 reco entries, the correction factor is statistically meaningless. Consider masking this bin or noting it explicitly in the Phase 4 handoff.

### 5.2 Efficiency map

**Evidence:** Mean efficiency = 0.731, min = 0.000, max = 0.900. The mean is consistent with the ~79% event selection efficiency. The min of 0.000 indicates bins where gen-level events exist in genBefore but not in gen (after selection). These bins are at kinematic boundaries.

**Finding (C-2):** The efficiency minimum of exactly 0.000 suggests at least one bin has zero gen entries but non-zero genBefore entries. These bins contribute to the correction factor but have zero efficiency. Verify this is confined to depopulated boundary bins and not a physics region.

### 5.3 Diagonal fraction

**Evidence:** Mean = 0.836, 57/58 populated bins above 0.50. The `conventions/unfolding.md` Phase 3 CLAUDE.md states "If < 50%, reassess the binning/method." Only 1/58 bins is below 0.50.

**Finding:** PASS. The diagonal fraction comfortably exceeds the 50% threshold. Bin-by-bin correction is well-motivated.

**Finding (B-4): Diagonal fraction is approximate, not computed from event-level matching.** The `02_correction_infrastructure.py` script (lines 121-127) computes the diagonal fraction as `min(N_gen, N_reco) / max(N_gen, N_reco)` per bin, which is a population-level proxy. It is NOT the true diagonal fraction (fraction of splittings that remain in the same bin between reco and gen levels). The true diagonal fraction requires event-by-event matching, which is noted in the code comments (line 107-108: "For the full IBU response, we need matched reco/gen Lund plane entries"). The script acknowledges this limitation (line 121: "True diagonal fraction requires event-level matching (done in 02b)") but no `02b` script exists. The approximate method will overestimate the diagonal fraction when gen and reco have similar total populations but different per-splitting migration patterns. The Phase 2 migration study (14% average) provides a more reliable estimate from event-matched data. The aggregate-level approximation should be explicitly flagged as approximate in the artifact (it is flagged in the figure label: "Diagonal fraction (approximate)").

---

## 6. Observable Definition Check

### 6.1 Lund plane construction

Checking the implementation in `01_process_all.py` against the strategy definition:

| Definition element | Strategy (Section 2.2) | Implementation | Match? |
|-------------------|----------------------|----------------|--------|
| Hemisphere splitting | Thrust axis (TTheta, TPhi) | `split_hemispheres()` uses TTheta, TPhi | YES |
| C/A clustering | `ee_genkt_algorithm`, R=999, p=0 | Line 135: `ee_genkt_algorithm, 999.0, 0.0` | YES |
| Hardness variable | p_T w.r.t. beam | Lines 153-155: `pt1 = sqrt(px^2 + py^2)` | YES |
| Delta_theta | `arccos(hat_p1 . hat_p2)` | Line 169: `np.arccos(cos_theta)` | YES |
| k_T | `|p_softer| * sin(Delta_theta)` | Line 174: `norm2 * np.sin(delta_theta)` | YES |
| Lund coordinates | ln(1/Delta_theta), ln(k_T) | Lines 176-177 | YES |
| E-scheme recombination | Implicit in ee_genkt | FastJet default for ee_genkt | YES |

**Finding:** The observable definition matches the strategy term-by-term. The p_T ordering, sin(Delta_theta) in k_T, and arccos formula are all correctly implemented.

### 6.2 Particle mass assumption

**Finding (B-5): Pion mass used for all charged tracks.** The code (`01_process_all.py` line 40, `01a_prototype.py` line 27) assigns M_PI = 0.13957 GeV to all particles when computing energy: `energy = sqrt(pmag^2 + M_PI^2)`. This is a standard simplification for charged-particle analyses (the majority of charged particles are pions), but the strategy does not specify this mass assumption. For C/A clustering (angular ordering), the mass enters through the energy in E-scheme recombination. The impact is small for light hadrons but may affect the clustering sequence for heavier particles (kaons, protons). This should be documented as a choice and its impact assessed. The mass branch exists in the data (Phase 2 reports mass values 0-3.81 GeV), so the actual particle mass could be used instead.

---

## 7. COMMITMENTS.md Check

Phase 3-relevant commitments:

| Commitment | Status | Notes |
|-----------|--------|-------|
| Closure test (p > 0.05) | PARTIAL | Self-consistency only; split-sample in Phase 4 |
| Data/MC agreement (no bins > 3 sigma) | CONTEXTUAL | 34 bins > 3 sigma in 2D, but this is expected at 5.7M hemispheres. 1D ratios within 5-10%. Gate PASS |
| Alternative correction (bin-by-bin vs IBU) | DEFERRED | IBU infrastructure started (efficiency map computed); full IBU in Phase 4 |
| Alternative jet definition cross-check | DONE | Approach A vs C comparison completed |
| Year-by-year stability | NOT DONE | Phase 2 found year-to-year consistency in <Thrust> and <N_ch>. Full Lund plane stability not checked in Phase 3 |
| Neutral thrust axis investigation | DONE | Phase 2 determined: Thrust is energy-flow, Thrust_charged is charged-only |
| Binning optimization | DONE | 10x10 uniform adopted per Phase 2 migration study |
| p_T vs energy ordering | DONE | Phase 2 quantified; p_T adopted as primary |
| Track selection cut systematic | DEFERRED | Phase 4 (varies p, d0, ntpc) |
| Event selection cut systematic | DEFERRED | Phase 4 (varies thrust, N_ch) |

**Finding (B-6): The Thrust event selection cut uses energy-flow Thrust, not Thrust_charged.** This is the same as finding B-1 but from the COMMITMENTS.md perspective. The strategy committed to using Thrust_charged for event selection (Phase 2 recommendation, Section 12.1). The executor used `Thrust` (energy-flow) without documenting the deviation. This should either be corrected to use Thrust_charged, or the deviation should be explicitly justified (e.g., the passesAll flag already encodes the event selection using a thrust variant, and adding a separate charged thrust cut is redundant).

---

## 8. Additional Findings

**Finding (B-7): genBefore hemisphere splitting uses energy-flow TTheta/TPhi.** In `01_process_all.py` line 101 (`split_hemispheres`), the hemisphere splitting uses TTheta and TPhi from whatever tree is being processed. For the `tgenBefore` tree, this means the pre-computed gen-level thrust axis is used. Phase 2 confirmed that gen-level trees have their own thrust computation. This is correct for the particle-level definition. However, the gen-level thrust axis computation may differ from the reco-level one (charged+neutral vs charged-only), and this is a source of systematic uncertainty that should be noted.

**Finding (C-3): Data/MC ratio panel y-axis label.** The closure test figures (Figures 9-10) use the ratio panel label "Data / MC" even though the comparison is "Corrected MC reco" vs "MC gen truth." The label should read "Corrected / Truth" or similar. This is cosmetic but potentially confusing.

**Finding (C-4): Pull distribution figure size.** Figure 11 (closure pulls) visually appears narrower than the other figures despite using figsize=(10,10). This may be an artifact of the content (sparse histogram concentrated in one bin). Not a plotting violation but could benefit from adjusting the x-axis range or bin count.

**Finding (B-8): Approach C uses data only, no MC correction factors.** The approach comparison (script `04_approach_comparison.py`) compares reco-level densities only. To serve as a meaningful systematic cross-check in Phase 4, Approach C will need its own correction infrastructure (correction factors derived from MC processed with Approach C). The artifact notes this as a Phase 4 deliverable (Section 8.2) but does not produce any Approach C MC histograms. This is acceptable for Phase 3 but should be flagged as a Phase 4 requirement.

**Finding (C-5): Correction factor map colorbar range.** The correction factor map (Figure 6) uses vmin=0.5, vmax=3.0, but the actual range is [1.17, 6.67]. The bins with C > 3.0 are clipped to the colorbar maximum, losing visual information at the kinematic boundaries. This is a reasonable default (the bulk is in [1.0, 3.0]) but the clipped bins should be noted.

---

## 9. Summary of Findings

### Category A (must resolve)
None.

### Category B (should address)

| # | Finding | Impact |
|---|---------|--------|
| B-1 | Thrust event selection uses energy-flow `Thrust`, not `Thrust_charged` as committed in strategy | Deviates from Phase 1 commitment without justification; impact likely small but must be documented |
| B-2 | Missing ntpc >= 4 track cut from strategy; branch availability not documented | May affect track quality; cannot evaluate committed ntpc systematic variation |
| B-3 | One correction factor exceeds 5x (C = 6.67); bin not identified | Statistical reliability of this bin is questionable |
| B-4 | Diagonal fraction is approximate (aggregate-level), not event-matched | Overestimates true diagonal fraction; acknowledged in figure label but not in artifact text |
| B-5 | Pion mass assumed for all charged tracks without documentation | Standard simplification but undocumented; actual mass branch available |
| B-6 | = B-1 from COMMITMENTS perspective | Phase 1 commitment deviation |
| B-7 | genBefore hemisphere splitting uses gen-level thrust axis; consistency with reco-level not explicitly verified | Potential systematic source |
| B-8 | Approach C has no MC correction infrastructure for Phase 4 | Blocks Approach C systematic evaluation unless built in Phase 4 |

### Category C (suggestions)

| # | Finding |
|---|---------|
| C-1 | Approach comparison could include gen-level comparison |
| C-2 | Efficiency = 0.000 bins should be enumerated |
| C-3 | Closure ratio panel label says "Data / MC" instead of "Corrected / Truth" |
| C-4 | Pull distribution looks narrow despite 10x10 figsize |
| C-5 | Correction factor colorbar clips bins with C > 3.0 |

---

## 10. Verdict

**PASS**

The Phase 3 artifact demonstrates a competent, complete execution of the Lund jet plane selection and correction infrastructure. All data and MC files are processed. The observable definition matches the strategy term-by-term. Two qualitatively different selection approaches are compared quantitatively. The closure test correctly identifies the algebraic identity and appropriately defers split-sample closure to Phase 4. The correction factors are physically plausible and the diagonal fraction supports the bin-by-bin method.

The Category B findings are real but none are blocking:
- B-1/B-6 (Thrust vs Thrust_charged) has negligible impact (0.15% difference per Phase 2) and can be addressed as a systematic variation in Phase 4.
- B-2 (ntpc) may be pre-applied by the aftercut selection; should be documented.
- B-3 (max C = 6.67) affects one kinematic boundary bin.
- B-4 (approximate diagonal fraction) is conservatively biased.
- B-5 (pion mass) is standard practice.
- B-7 and B-8 are Phase 4 preparation items.

All B items should be addressed before the Phase 4 handoff, but none require re-running the Phase 3 processing. They can be resolved with documentation additions and flagging for Phase 4.
