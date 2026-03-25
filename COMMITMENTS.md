# Commitments

Tracks all binding commitments from Phase 1 onward.
Update at every phase boundary.

## Status key

- `[x]` Resolved
- `[D]` Formally downscoped (with documented justification)
- `[ ]` Not yet addressed

## Systematic sources

- [ ] Tracking efficiency: randomly drop 1% of tracks, recompute Lund plane
- [ ] Track momentum resolution: smear momenta by +/-10% of resolution
- [ ] Angular resolution: smear angles by +/-1 mrad
- [ ] Track selection cuts: vary p threshold (150-250 MeV/c), |d0| (1.5-2.5 cm), ntpc (3-5)
- [ ] Event selection cuts: vary thrust cut (0.6-0.8), N_ch_min (4-6), E_ch_min (12-18 GeV)
- [ ] MC model dependence: reweight PYTHIA 6.1 gen-level to match PYTHIA 8 / HERWIG 7 truth shapes; derive new correction factors; envelope of variations
- [ ] Unfolding method: difference between bin-by-bin and IBU corrected results
- [ ] ISR modelling: compare thrust axis with/without pwflag=-11 particles at gen-level; quantify shift in Lund plane
- [ ] Hemisphere assignment: charged+neutral vs charged-only thrust axis
- [ ] Background contamination: negligible (<0.1%); no flat systematic assigned. Cross-check by MC subtraction if needed
- [ ] Covariance matrix: statistical (bootstrap, N >= 500), systematic (per source), total. Machine-readable format. PSD verified

## Validation tests

- [ ] Closure test: correction factors applied to MC reco recover MC gen truth (chi2 p > 0.05)
- [ ] Split-sample closure: derive correction from half A, apply to half B (chi2 p > 0.05)
- [ ] Stress test: recover reweighted truth (tilts of 5%, 10%, 20%, 50%) in both Lund coordinates
- [ ] Data/MC agreement: reco-level comparison of all kinematic inputs (no bins > 3 sigma)
- [ ] Alternative correction method comparison: bin-by-bin vs IBU (agreement within 2-sigma or investigated)
- [ ] Covariance validation: PSD, condition number < 10^10, correlation matrix visualized
- [ ] Year-by-year stability: consistent Lund plane across 1992-1995

## Flagship figures

- [ ] F1: Primary Lund jet plane density (2D coloured plot) — the central result
- [ ] F2: Lund plane density vs PYTHIA 8 and HERWIG 7 (data / MC comparison panels)
- [ ] F3: ln k_T projection (1D spectrum with uncertainties and MC overlays)
- [ ] F4: ln 1/Delta_theta projection (1D spectrum with uncertainties and MC overlays)
- [ ] F5: Response matrix / correction factor map (2D)
- [ ] F6: Systematic uncertainty breakdown vs ln k_T

## Cross-checks

- [ ] Alternative jet definition: exclusive kT jets (Approach C) vs thrust hemispheres (Approach A)
- [ ] Bin-by-bin vs iterative Bayesian unfolding
- [ ] Year-by-year stability
- [ ] pwflag=0 vs pwflag={0,1,2} track selection

## Comparison targets

- [ ] PYTHIA 8 Monash particle-level prediction at sqrt(s) = 91.2 GeV
- [ ] HERWIG 7 particle-level prediction at sqrt(s) = 91.2 GeV
- [ ] DELPHI jet splitting probability (inspire_1661966) — 1D kT projection comparison
- [ ] Analytical LO prediction: rho ~ alpha_s * C_F / pi in the perturbative region
