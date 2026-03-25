# Constructive Review: Phase 1 Strategy

**Reviewer:** Dolores (constructive) | **Artifact:** `STRATEGY_fabiola_2026-03-25_16-50.md`
**Date:** 2026-03-25

---

## Summary assessment

This is a well-structured strategy for the first measurement of the primary Lund jet plane density in e+e- collisions. The observable definition is precise, the systematic plan is thorough, and the self-critique round caught several real issues. The strategy correctly identifies MC model dependence as the dominant systematic and proposes a sound reweighting procedure to evaluate it. The reference analysis table is well-chosen.

However, several opportunities exist to strengthen the analysis significantly, and a few points require clarification or correction before proceeding. The findings below are organized by the six evaluation axes requested, then collected into the classification summary.

---

## 1. Resolving power

### F1 (B): The perturbative plateau region and its discriminating power are not quantitatively delineated

The strategy states that the perturbative region is "approximately uniform" with density rho_LO ~ alpha_s * C_F / pi ~ 0.050, and that the non-perturbative region shows hadronization effects. However, the strategy does not identify *where* on the Lund plane the transition occurs, or in which region the measurement has the strongest power to discriminate between PYTHIA, HERWIG, and analytical QCD.

For a charged-particle measurement at sqrt(s) = 91.2 GeV, the perturbative region where the density should be approximately flat and governed by alpha_s * C_F / pi is roughly:
- ln(k_T/GeV) > 0 (k_T > 1 GeV, above Lambda_QCD)
- 1 < ln(1/Delta_theta) < 3 (intermediate angles, not contaminated by hemisphere boundary effects at wide angle or collinear cutoff at small angle)

The non-perturbative transition at k_T ~ Lambda_QCD ~ 0.3-1 GeV (ln k_T ~ -1 to 0) is precisely the region where PYTHIA (string) and HERWIG (cluster) hadronization models differ most. The strategy should explicitly identify this strip as the primary region for model discrimination, and the perturbative plateau at higher k_T as the region for alpha_s and colour factor sensitivity.

**Requested action:** Add a subsection (or extend Section 10.2) identifying the expected regions of the Lund plane where (a) perturbative QCD predictions apply and the density probes alpha_s/C_F, (b) hadronization model differences are largest, and (c) the measurement is limited by resolution or statistics. This directly informs the binning optimization in Phase 2.

### F2 (C): Running of alpha_s across the Lund plane deserves more explicit treatment

Section 10.2 mentions that "running of alpha_s across the Lund plane (k_T ranges from ~0.05 GeV to ~55 GeV) will produce a visible tilt that probes the QCD beta function." This is correct and is one of the most interesting physics outcomes of the measurement. The strategy would benefit from an explicit estimate of the expected slope: alpha_s(k_T = 1 GeV) ~ 0.5 vs alpha_s(k_T = 45 GeV) ~ 0.11 produces roughly a factor-5 variation in rho across the plane in the perturbative region. This makes the running effect dramatically visible and should be flagged as a key physics message.

---

## 2. Dominant uncertainties

### F3 (B): MC model dependence reweighting procedure assumes detector response is truth-shape-independent

The MC model dependence evaluation (Section 7.2) reweights PYTHIA 6.1 gen-level to match PYTHIA 8 or HERWIG 7 truth-level shapes, then derives new correction factors. The strategy states: "only the gen-level shape changes; the detector response (reco/gen migration) is held fixed from the original PYTHIA 6.1 simulation."

This is a standard and acceptable procedure, but it carries an implicit assumption that the detector response (migration matrix) is independent of the true particle-level distribution. This is approximately true when migrations are small and the response is locally linear, but breaks down when the truth-level reweighting is large (which it will be in the non-perturbative region, precisely where model dependence matters most). Large reweighting factors also inflate statistical uncertainties on the reweighted correction factors.

Evidence from ATLAS (Phys. Rev. Lett. 124 (2020) 222002): their MC model systematic reaches 30% in some bins, precisely because the detector response to soft, wide-angle emissions is correlated with the emission pattern itself. For charged-particle tracking at ALEPH, this correlation is much weaker (tracking efficiency is nearly flat above 200 MeV/c), but it is not zero.

**Requested action:** Acknowledge this assumption explicitly in the strategy. Add a sentence stating that if the truth-level reweighting factors exceed some threshold (e.g., a factor of 3 in any bin), the procedure will be cross-checked by verifying that the reco-level shape also migrates as expected under reweighting. This is a diagnostic, not an additional systematic -- it validates the reweighting procedure itself.

### F4 (B): The 1% tracking efficiency drop needs a clearer connection to the data

The strategy justifies the 1% random track drop as "conservative" relative to the 0.7% TPC hit variation measured in cds_2876991. However, the systematic evaluation conventions (methodology/06-review.md Section 6.3, question 4) explicitly ask: "Is any systematic evaluated on MC when a data-based evaluation exists and gives a smaller value?"

The 0.7% number from cds_2876991 is itself measured from data (TPC hit variation). The 1% used in the strategy is an MC-evaluated inflation of that data measurement. This is acceptable provided: (a) the 1% is documented as a conservative envelope on the data measurement, not as an independent MC-only estimate, and (b) the strategy commits to checking whether a data-driven tracking efficiency evaluation (e.g., from track reconstruction efficiency in overlapping TPC/ITC regions) could reduce this systematic. The ALEPH detector had redundant tracking in the ITC-TPC overlap region -- this was exploited in other ALEPH analyses.

**Requested action:** State explicitly that 1% is a conservative envelope on the data-measured 0.7%, and note that a data-driven tracking efficiency cross-check using detector redundancy (ITC-TPC overlap) will be investigated in Phase 2/3 if this systematic turns out to be significant.

### F5 (C): Event selection systematic variations could be better motivated

The thrust cut variation (0.6-0.8) and N_ch_min variation (4-6) are reasonable, but the ranges appear chosen symmetrically around the nominal values without explicit motivation. Why 0.6 and not 0.5? Why not 0.9? The range should be motivated either by (a) the range over which published ALEPH analyses have used these cuts, or (b) the range over which data/MC agreement holds. Phase 2 can determine this, but the strategy should flag the intent.

---

## 3. Information recovery

### F6 (B): The secondary Lund plane is not discussed

The strategy measures only the *primary* Lund plane (following the harder subjet at each declustering step). The secondary Lund plane -- constructed by following the softer branch at one or more steps -- carries complementary information about secondary emissions and is more sensitive to colour coherence effects. Dreyer, Salam, and Soyez (JHEP 12 (2018) 064) discuss this explicitly.

For a first measurement, focusing on the primary plane is correct. However, the strategy should at minimum:
(a) Note that the secondary plane is accessible with the same data and declustering infrastructure, requiring only a different branch-following choice in the code.
(b) Flag it as a natural extension in Phase 4 or as a "maximality check" item -- the orchestrator protocol requires checking for feasible work the agent did not do.

The secondary Lund plane is not a different analysis; it is a few additional lines of code on top of the primary measurement infrastructure. Not mentioning it at all risks the maximality check flagging it later.

**Requested action:** Add a brief subsection (e.g., 2.4 "Extensions: Secondary Lund Plane") noting that the secondary plane is accessible and will be evaluated for feasibility during Phase 2 exploration. If statistics and correction quality permit, it should be included as an additional result.

### F7 (B): Quark/gluon separation via heavy flavour tagging is not considered

The ALEPH data at the Z pole contains a significant fraction of Z -> bb-bar events (~21.7% of hadronic Z decays). The archived data includes impact parameter information (d0, z0 branches), and the ALEPH b-tagging capability is well-established (cf. inspire_433342, the ALEPH quark-gluon jet study in the corpus, which uses lifetime tagging on the same data format). The DELPHI splitting analysis (inspire_1661966) explicitly separated quark and gluon jets using b-tagging.

Measuring the Lund plane separately for light-quark-enriched and b-quark-enriched hemispheres would:
- Test whether the colour factor sensitivity (rho ~ alpha_s * C_F / pi for quarks vs alpha_s * C_A / pi for gluons) is visible in the data
- Provide a direct connection to the DELPHI splitting ratio measurement (inspire_1661966: CA = 2.8 +/- 0.8 * CF from the splitting ratio)
- Double the physics content of the paper

This is feasible: tag one hemisphere as b-enriched using the impact parameter information already in the data, measure the Lund plane in the *opposite* hemisphere (which is then enriched in light quarks by anti-tagging). The infrastructure for this is the same as the inclusive measurement plus a b-tag cut.

**Requested action:** Add a discussion of quark-flavour-separated Lund plane measurements as a feasibility study for Phase 2. If the b-tagging efficiency and purity are sufficient (which the ALEPH quark-gluon literature strongly suggests), commit to this as an additional measurement. If the b-tagging capability of the archived data is insufficient, document why with evidence.

### F8 (C): Three-jet events and the gluon Lund plane

Beyond two-hemisphere (dijet) events, three-jet events (selected by requiring three jets at a suitable y_cut) provide direct access to gluon-jet Lund planes. The gluon jet is identified as the jet not containing a b-tagged particle in bb-bar events. While this requires significantly more selection infrastructure and introduces purity issues, it is worth noting as a future extension. The ALEPH subjet analysis (cds_388806) and the colour factor measurement (inspire_537303) both exploit three-jet topologies from the same data.

---

## 4. Presentation and flagship figures

### F9 (A): F5 is labelled "Response matrix" but actually shows correction factors

The strategy states F5 is the "Response matrix / correction factor map (2D)." These are different objects. The correction factor C(i,j) = N_gen(i,j) / N_reco(i,j) is a 2D map that is inherently diagonal-structured (one number per bin). The response matrix R(i,j) for the IBU cross-check is a 100x100 matrix mapping true bins to reco bins, which is an intrinsically different visualization.

A journal referee would require *both* if IBU is used as a cross-check:
- The correction factor map (2D, one panel) for the primary method
- The response matrix (2D, one panel) for the cross-check, demonstrating the near-diagonal structure that justifies bin-by-bin correction

These cannot be conflated into one figure.

**Requested action:** Split F5 into two figures: F5a (bin-by-bin correction factor map) and F5b (2D response matrix for IBU). Alternatively, keep F5 as the correction factor map and add the response matrix to the "additional figures" list, with a note that it provides the key validation of the bin-by-bin assumption.

### F10 (B): Missing figure: analytical LO overlay on the 2D plane or 1D projection

The theory comparison plan (Section 10.2) discusses the analytical LO prediction rho_LO = alpha_s * C_F / pi but none of the flagship figures show this comparison. The most impactful figure in the paper would overlay the measured 1D k_T projection (F3) with the analytical prediction -- showing the transition from the perturbative plateau to the non-perturbative rise. This is the "money plot" that demonstrates the measurement's physics content.

**Requested action:** Either modify F3 to include the analytical LO line (with the alpha_s running effect) as an overlay, or add a dedicated flagship figure F7 for the theory comparison. This figure would show the measured ln(k_T) projection with (a) PYTHIA 8, (b) HERWIG 7, and (c) the LO analytical prediction overlaid, clearly delineating the perturbative and non-perturbative regimes.

### F11 (C): Consider a data/MC ratio presentation for F2

F2 (Lund plane vs PYTHIA 8 and HERWIG 7) is described as "three panels" or "2D ratio plots." The most informative presentation would be: (top) the data Lund plane, (middle) data/PYTHIA 8 ratio, (bottom) data/HERWIG 7 ratio. The ratio presentation immediately reveals where the generators succeed and fail. The ATLAS Lund plane paper used exactly this format and it is highly effective.

---

## 5. Theory comparison strategy

### F12 (B): NLL predictions for the Lund plane density exist and should be cited

The strategy mentions "NLL resummation" in passing (Section 10.2) but does not cite any specific NLL or NNLL calculation. The state of the art for analytical Lund plane predictions includes:

- Dreyer, Salam, Soyez, JHEP 12 (2018) 064 -- the original paper defining the Lund plane and deriving the LO density. This is cited.
- Lifson, Salam, Soyez, JHEP 10 (2020) 170 -- NLL resummation for the Lund jet plane density, providing the first beyond-LO analytical prediction for the 1D projections.
- Herren, Lifson, Marzani, Salam, Soyez -- further NNLL work extending these predictions.

If numerical predictions from the NLL calculations of Lifson, Salam, Soyez (2020) are available (they may have been published as supplemental material or in the JHEP auxiliary files), comparing the e+e- Lund plane measurement with NLL QCD predictions would be a major physics result -- far more interesting than comparison with MC generators alone. Even if numerical predictions are not immediately available for the e+e- case (the calculations were done for pp), the analytical framework is the same and the authors may provide predictions upon request.

**Requested action:** Add a citation to the NLL Lund plane work (Lifson, Salam, Soyez, JHEP 10 (2020) 170) and commit to investigating whether numerical predictions for e+e- are available. If they are, the comparison with NLL QCD replaces MC generators as the primary physics message of the paper. If they are not, document this limitation and note that the measurement provides data for future analytical comparisons.

### F13 (C): Sherpa feasibility should be assessed early

Section 10.1 lists Sherpa 2.2 as a theory comparison "(if feasible)." The hedging is understandable, but Sherpa 3.x is the current release, and e+e- event generation at the Z pole is a basic Sherpa capability. The strategy should commit to a concrete feasibility check in Phase 2 (attempting `pixi add sherpa` or running a standalone Sherpa generation) rather than leaving it as indefinitely conditional. A third generator comparison (string vs cluster vs dipole+string) significantly strengthens the model dependence evaluation.

---

## 6. Honest framing

### F14 (B): The "first e+e- Lund plane measurement" claim needs careful framing

The strategy repeatedly emphasizes novelty: "the first Lund jet plane measurement in e+e- collisions." While technically accurate for the full 2D primary Lund plane, the DELPHI splitting probability measurement (inspire_1661966) already measured what is effectively a 1D projection of the Lund plane. The strategy acknowledges this in Section 2.3 but the framing elsewhere could be read as over-claiming.

A journal referee would insist on careful phrasing. The honest framing is: "This is the first measurement of the full two-dimensional primary Lund jet plane density in e+e- collisions. One-dimensional projections related to jet splitting probabilities have been measured previously by DELPHI [cite]."

**Requested action:** Ensure the novelty claim is always qualified as "full two-dimensional" throughout the strategy and future artifacts. This is not a physics error, but imprecise framing that a referee would flag.

### F15 (C): MC statistics limitation is acknowledged but its impact is not quantified

Constraint [A3] notes that MC is ~25% of data statistics, which "limits the precision of correction factors in sparsely populated Lund plane bins." The strategy does not estimate which bins will be statistics-limited in the MC. With 771k events yielding ~10-15 primary splittings per hemisphere, the total MC splitting count is ~10-15M, distributed over 100 bins -- an average of 100k-150k per bin, but with large variation. Corner bins (large angle + high k_T, or small angle + low k_T) will have orders of magnitude fewer entries and the correction factors there may have O(10%) statistical uncertainty from MC alone.

A rough estimate of the MC statistical uncertainty per bin would help calibrate expectations. This can be deferred to Phase 2 exploration, but the strategy should flag it explicitly as a Phase 2 deliverable.

---

## Additional findings

### F16 (B): Hemisphere assignment systematic is categorized as "observable definition" -- this is confusing

Section 7.2 lists "Hemisphere assignment: Compare thrust axis from charged+neutral (energy flow) vs charged-only" as an "Observable definition" category systematic. But per conventions/unfolding.md, "Observable redefinition is not a systematic" -- changing the thrust axis definition changes what is measured. If the measurement uses a charged-particle thrust axis, then switching to an energy-flow thrust axis changes the observable, and the difference is not a systematic uncertainty on the original observable.

The strategy should either:
(a) Define the measurement as using the charged-particle thrust axis and remove the energy-flow comparison from the systematic table (keep it as a cross-check only), or
(b) Define the measurement as using the energy-flow thrust axis (which may be better since the data has calorimeter information) and evaluate the systematic by varying the calorimeter energy scale.

Currently the strategy is ambiguous on which thrust axis defines the measurement. The particle-level definition (Section 2.2) says "the thrust axis is computed from all charged particles" -- so the charged-particle thrust IS the definition, and the energy-flow comparison is a cross-check, not a systematic.

**Requested action:** Move the hemisphere assignment comparison from the systematic table to the cross-checks section. Replace it with a thrust-axis resolution systematic: smear the thrust axis direction by the expected resolution (from MC truth-reco comparison) and evaluate the effect on hemisphere assignment and the Lund plane.

### F17 (C): The binning range in ln(k_T) extends below detector sensitivity

The proposed binning extends ln(k_T/GeV) down to -3, corresponding to k_T ~ 0.05 GeV = 50 MeV. With a track momentum threshold of p > 200 MeV/c, the minimum measurable k_T depends on the opening angle: k_T = p * sin(Delta_theta). For the minimum momentum (200 MeV/c) at a moderate angle (Delta_theta ~ 0.5 rad), k_T_min ~ 100 MeV. The lowest bin [-3, -2.3] (k_T = 50-100 MeV) will be populated only by very specific kinematic configurations and may have large correction factors.

Phase 2 exploration should evaluate the bin population and correction factor magnitude in this region and consider truncating the binning range if the correction exceeds, say, a factor of 5. This is a Phase 2 task, but worth flagging.

### F18 (C): Normalization sequence deserves an explicit formula

Section 6.4 states "self-normalization applied after correction, not before" (correctly following the conventions pitfall). However, the explicit formula for the final result is:

rho(i,j) = C(i,j) * N_data_reco(i,j) / (N_jet * Delta_x * Delta_y)

where N_jet = 2 * N_events(selected), and the correction factor C(i,j) already includes efficiency. The strategy should write this out explicitly to avoid ambiguity about whether N_jet is the number of selected events at detector level or after efficiency correction. For a self-normalized observable, N_jet at detector level is correct (the efficiency correction enters through C(i,j)), but this should be stated.

---

## Classification summary

| ID | Category | Title | Section |
|----|----------|-------|---------|
| F1 | B | Perturbative vs non-perturbative region discrimination power not delineated | 1 |
| F2 | C | Running alpha_s slope estimate would strengthen the physics case | 1 |
| F3 | B | MC reweighting assumption (response independent of truth shape) not acknowledged | 2 |
| F4 | B | Tracking efficiency 1% needs clearer data connection and data-driven cross-check | 2 |
| F5 | C | Event selection systematic ranges not explicitly motivated | 2 |
| F6 | B | Secondary Lund plane not discussed (maximality gap) | 3 |
| F7 | B | Quark/gluon separation via b-tagging not considered (major information recovery opportunity) | 3 |
| F8 | C | Three-jet gluon Lund plane noted as extension | 3 |
| F9 | A | F5 conflates correction factors with response matrix -- these are distinct objects requiring separate figures | 4 |
| F10 | B | No flagship figure shows the analytical LO QCD overlay | 4 |
| F11 | C | Data/MC ratio format recommended for F2 | 4 |
| F12 | B | NLL analytical predictions (Lifson, Salam, Soyez 2020) not cited or pursued | 5 |
| F13 | C | Sherpa feasibility should be resolved concretely in Phase 2 | 5 |
| F14 | B | "First" claim needs consistent "full 2D" qualification | 6 |
| F15 | C | MC statistical uncertainty per Lund bin not estimated | 6 |
| F16 | B | Hemisphere assignment: observable redefinition treated as systematic (conflicts with conventions/unfolding.md) | Additional |
| F17 | C | Lowest ln(k_T) bins may be below detector sensitivity | Additional |
| F18 | C | Explicit normalization formula would remove ambiguity | Additional |

**Totals:** 1 Category A, 9 Category B, 8 Category C.

---

## Verdict

The strategy is solid and demonstrates careful thought about the measurement. The single Category A (F9: figure conflation) is straightforward to fix. The Category B items collectively address the concern that the strategy could extract significantly more physics from the data -- particularly the secondary Lund plane (F6), quark/gluon separation (F7), and NLL analytical comparison (F12), which together could transform this from a "first measurement" paper into a paper with genuine QCD insight. The hemisphere assignment systematic mis-categorization (F16) should also be resolved to maintain consistency with conventions/unfolding.md.

None of the findings challenge the overall analysis direction. The observable definition, correction strategy, and validation plan are sound.
