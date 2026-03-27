# Commitments

Tracks all binding commitments from Phase 1 onward.
Update at every phase boundary.

## Status key

- `[x]` Resolved
- `[D]` Formally downscoped (with documented justification)
- `[ ]` Not yet addressed

## Systematic sources

- [x] Tracking efficiency: randomly drop 1% of tracks, recompute Lund plane. 1% justified as ~1 sigma above measured ~1.5% per-track inefficiency (ALEPH NIM A 360 (1995) 481)
- [x] Track momentum resolution: smear momenta by +/-10% of resolution. Phase 2 verified TPC+ITC combined resolution
- [x] Angular resolution: smear angles by +/-1 mrad
- [x] Track selection cuts: vary p threshold (150-250 MeV/c), |d0| (1.5-2.5 cm). ntpc: [D] branch not accessible in archived data
- [x] Event selection cuts: vary thrust cut (0.6-0.8), N_ch_min (4-6), E_ch_min (12-18 GeV)
- [x] MC model dependence: reweight PYTHIA 6.1 gen-level; derive new correction factors; envelope of variations
- [D] Unfolding method: IBU formally downscoped from co-primary to cross-check [D9]. 3 remediation attempts documented, all fail. Replaced with correction factor stability systematic
- [x] Heavy flavour composition: reweight MC b-fraction by +/-2%
- [x] ISR modelling: compare thrust axis with/without pwflag=-11 particles at gen-level
- [x] Thrust-axis resolution: smear momenta within resolution, measure hemisphere migration rate
- [D] Background contamination: negligible (<0.1%); no flat systematic assigned
- [x] Covariance matrix: statistical (bootstrap N=500), systematic (per source), total. PSD verified
- [x] Neutral thrust axis: Phase 2 determined archived data uses energy-flow thrust. Charged-only thrust available as cross-check
- [x] Hardness variable: p_T ordering primary [D13], energy ordering compared at MC truth level (<5% difference in core)

## Validation tests

- [x] Closure test: chi2 = 0 (identity). Split-sample with combined sigma: chi2/ndf = 40.71/58, p = 0.96
- [x] Split-sample closure: chi2/ndf = 40.71/58, p = 0.96, PASSES
- [x] Stress test: 12/12 split-sample configurations pass with combined sigma
- [x] Data/MC agreement: reco-level Lund plane ratio mean 1.005, std 0.055
- [D] Alternative correction method: IBU downscoped [D9]; see Systematic sources
- [x] Covariance validation: PSD verified, condition number < 10^10
- [x] Year-by-year stability: all 6 periods chi2/ndf < 1.3 (full data)
- [x] MC reweighting diagnostic: reweighting factors < 3x verified

## Flagship figures

- [x] F1: Primary Lund jet plane density (2D) -- emeric_lund_plane_full_corrected.pdf
- [D] F2: Lund plane vs PYTHIA 8 / HERWIG 7 -- deferred to future (standalone generators not run; noted in Future Directions)
- [x] F3: ln k_T projection (1D with uncertainties) -- emeric_1d_kt_projection.pdf
- [x] F4: ln 1/Delta_theta projection (1D) -- emeric_1d_dtheta_projection.pdf
- [x] F5: Correction factor map (2D) -- ingrid_correction_factor_map.pdf
- [x] F6: Systematic uncertainty breakdown -- nikolai_syst_breakdown.pdf

## Additional figures

- [x] Response matrix for IBU (2D) -- felix_response_matrix.pdf
- [D] Methodology diagram -- not produced; analysis flow described in text

## Cross-checks

- [x] Alternative jet definition: Approach A vs C, chi2/ndf = 0.185
- [D] Bin-by-bin vs IBU: IBU downscoped [D9]
- [x] Year-by-year stability: all periods consistent
- [D] pwflag=0 vs pwflag={0,1,2}: not evaluated; documented in limitations
- [x] Hemisphere assignment: charged+neutral vs charged-only thrust axis (reclassified as cross-check)

## Comparison targets

- [D] PYTHIA 8 Monash: standalone generation not performed; noted in Future Directions
- [D] HERWIG 7: standalone generation not performed; noted in Future Directions
- [D] DELPHI jet splitting: qualitative comparison noted; quantitative extraction requires coordinate transformation
- [D] ATLAS Lund plane HEPData: qualitative comparison (pp vs e+e- jet definitions differ)
- [D] CMS Lund plane HEPData: same caveat as ATLAS
- [x] Analytical LO prediction: rho_LO^charged ~ 0.067, consistent with perturbative plateau
- [D] NLL prediction: requires input from theory authors for e+e- quark jets; noted in Future Directions

## Phase 2 deliverables

- [x] Binning optimization: migration fraction, bin population studied; 10x10 uniform validated; 15x15 viable for future
- [x] Aftercut pre-selection: passesNTrkMin pre-applied; tgenBefore confirmed as full pre-selection sample
- [x] Momentum resolution: TPC+ITC combined tracking confirmed (sigma_p/p^2 ~ 0.8-1.0e-3)
- [x] Neutral thrust axis: energy-flow thrust in archived data confirmed
- [D] Sherpa feasibility [D14]: not attempted; noted in Future Directions
- [x] p_T vs energy ordering [D13]: compared at MC truth level, <5% difference in perturbative core
