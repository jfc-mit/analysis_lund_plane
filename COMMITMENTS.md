# Commitments

Tracks all binding commitments from Phase 1 onward.
Update at every phase boundary.

## Status key

- `[x]` Resolved
- `[D]` Formally downscoped (with documented justification)
- `[ ]` Not yet addressed

## Systematic sources

- [x] Tracking efficiency: randomly drop 1% of tracks, recompute Lund plane. 1% justified as ~1 sigma above measured ~1.5% per-track inefficiency (ALEPH NIM A 360 (1995) 481)
- [x] Track momentum resolution: smear momenta by +/-10% of resolution. Phase 2 must verify TPC-only vs TPC+ITC+VDET resolution for archived data
- [x] Angular resolution: smear angles by +/-1 mrad
- [x] Track selection cuts: vary p threshold (150-250 MeV/c), |d0| (1.5-2.5 cm). ntpc: [D] branch not accessible in archived data
- [x] Event selection cuts: vary thrust cut (0.6-0.8), N_ch_min (4-6), E_ch_min (12-18 GeV)
- [x] MC model dependence: reweight PYTHIA 6.1 gen-level to match PYTHIA 8 / HERWIG 7 truth shapes; derive new correction factors; envelope of variations. Diagnostic: verify reweighting factors < 3x
- [D] Unfolding method: IBU formally downscoped from co-primary to cross-check [D9]. IBU fails all validation tests (chi2/ndf > 2000) due to inability to match individual Lund splittings between reco/gen. 3 remediation attempts made: (1) iteration optimization (1-20 iter), (2) uncapped hemisphere-level response matrix, (3) Tikhonov regularization (alpha 0.01-0.5). All fail. Replaced with correction factor stability systematic (10-file vs 30-file MC split). Literature: ATLAS PRL 124 (2020) 222002 and CMS JHEP 05 (2024) 116 both use bin-by-bin as primary for Lund plane
- [x] Heavy flavour composition: reweight MC b-fraction by +/-2% (R_b precision); quantify b-quark dead-cone contribution per Lund plane bin
- [x] ISR modelling: compare thrust axis with/without pwflag=-11 particles at gen-level; quantify shift in Lund plane
- [x] Thrust-axis resolution: smear momenta within resolution, measure hemisphere migration rate (replaces "hemisphere assignment" systematic)
- [D] Background contamination: negligible (<0.1%); no flat systematic assigned. Cross-check by MC subtraction if needed
- [x] Covariance matrix: statistical (bootstrap with full correction chain resampling, N = 500), systematic (per source), total. Machine-readable format. PSD verified
- [ ] Neutral thrust axis: Phase 2 investigation to determine archived data thrust source (energy-flow vs charged-only) and handle consistently
- [ ] Hardness variable: p_T ordering primary, energy ordering as systematic variation [D13]

## Validation tests

- [x] Closure test: correction factors applied to MC reco recover MC gen truth (chi2 = 0, identity). Split-sample closure with combined uncertainty: chi2/ndf = 40.71/58, p = 0.96, PASSES. Three remediations documented
- [x] Split-sample closure: derive correction from half A, apply to half B. With combined sigma (Poisson + correction factor uncertainty): chi2/ndf = 40.71/58, p = 0.96, PASSES
- [x] Stress test: split-sample stress tests (correction from A, tilt on B) with 12 configurations (3 directions x 4 epsilons). 12/12 pass with combined sigma
- [ ] Data/MC agreement: reco-level comparison of all kinematic inputs (no bins > 3 sigma)
- [D] Alternative correction method comparison: IBU formally downscoped from co-primary to cross-check [D9]. IBU fails all tests; see Systematic sources above for remediation documentation
- [x] Covariance validation: PSD, condition number < 10^10, correlation matrix visualized
- [ ] Year-by-year stability: consistent Lund plane across 1992-1995
- [ ] MC reweighting diagnostic: verify reweighting factors < 3x; check reco-level migration

## Flagship figures

- [ ] F1: Primary Lund jet plane density (2D coloured plot) -- the central result
- [ ] F2: Lund plane density vs PYTHIA 8 and HERWIG 7 (data / MC comparison panels)
- [ ] F3: ln k_T projection (1D spectrum with uncertainties, MC overlays, and LO analytical prediction overlay)
- [ ] F4: ln 1/Delta_theta projection (1D spectrum with uncertainties and MC overlays)
- [ ] F5: Correction factor map (2D) -- bin-by-bin correction factors C(i,j)
- [ ] F6: Systematic uncertainty breakdown vs ln k_T

## Additional figures

- [ ] Response matrix for IBU (2D migration probability visualization, separate from F5)
- [ ] Lund plane construction methodology diagram

## Cross-checks

- [ ] Alternative jet definition: exclusive kT jets (Approach C) vs thrust hemispheres (Approach A)
- [ ] Bin-by-bin vs iterative Bayesian unfolding (co-primary methods)
- [ ] Year-by-year stability
- [ ] pwflag=0 vs pwflag={0,1,2} track selection
- [ ] Hemisphere assignment: charged+neutral vs charged-only thrust axis (reclassified from systematic to cross-check per conventions/unfolding.md)

## Comparison targets

- [ ] PYTHIA 8 Monash particle-level prediction at sqrt(s) = 91.2 GeV
- [ ] HERWIG 7 particle-level prediction at sqrt(s) = 91.2 GeV
- [ ] DELPHI jet splitting probability (inspire_1661966) -- 1D kT projection comparison (HEPData extraction)
- [ ] ATLAS Lund plane (Phys. Rev. Lett. 124 (2020) 222002) -- HEPData extraction, qualitative comparison in collinear region
- [ ] CMS Lund plane (JHEP 05 (2024) 116) -- HEPData extraction, charged-particle comparison
- [ ] Analytical LO prediction: rho ~ 2 * alpha_s * C_F / pi in the perturbative region (all-particle ~0.100; charged-particle ~0.067)
- [ ] NLL prediction comparison (Lifson, Salam, Soyez, JHEP 10 (2020) 170) -- investigate numerical predictions for e+e- quark jets

## Phase 2 deliverables (from arbiter review)

- [ ] Binning optimization: migration fraction per bin, resolution vs bin width, bin population, non-uniform vs uniform comparison
- [ ] Aftercut pre-selection investigation: document pre-cuts, verify MC has identical pre-cuts, determine tgenBefore scope
- [ ] Momentum resolution verification: TPC-only vs TPC+ITC+VDET for archived track reconstruction
- [ ] Neutral thrust axis source determination
- [ ] Sherpa feasibility assessment [D14]
- [ ] p_T vs energy ordering comparison for hardness variable [D13]
