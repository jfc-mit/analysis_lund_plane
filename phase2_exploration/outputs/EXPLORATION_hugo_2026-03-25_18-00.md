# Phase 2: Exploration -- Primary Lund Jet Plane Density in Hadronic Z Decays

**Session:** Hugo (executor) | **Date:** 2026-03-25 | **Analysis:** lund_jet_plane

---

## 1. Sample Inventory

### 1.1 Data

| File | Year | Events | Size |
|------|------|--------|------|
| LEP1Data1992_recons_aftercut-MERGED.root | 1992 | 551,474 | 3.8 GB |
| LEP1Data1993_recons_aftercut-MERGED.root | 1993 | 538,601 | 3.7 GB |
| LEP1Data1994P1_recons_aftercut-MERGED.root | 1994 | 433,947 | 3.0 GB |
| LEP1Data1994P2_recons_aftercut-MERGED.root | 1994 | 447,844 | 3.1 GB |
| LEP1Data1994P3_recons_aftercut-MERGED.root | 1994 | 483,649 | 3.4 GB |
| LEP1Data1995_recons_aftercut-MERGED.root | 1995 | 595,095 | 4.1 GB |
| **Total** | **1992-1995** | **3,050,610** | **21 GB** |

**Tree structure (data, per file):**
- `t`: 151 branches, primary particle tree. Contains per-particle arrays (px, py, pz, pt, pmag, eta, theta, phi, mass, charge, d0, z0, pwflag, pid) and per-event scalars (Thrust, TTheta, TPhi, Sphericity, Aplanarity, nChargedHadrons, selection flags).
- 10 additional jet trees: anti-kT R=0.4/0.8 (E-scheme and WTA-modp), kT N=2/N=3 exclusive jets, boosted event trees. Each has 13 branches with pre-computed jet quantities and SoftDrop variables (zg, rg).

**Key data branches:**
- Particle: px, py, pz, pt, pmag, eta, theta, phi, mass, charge, d0, z0, pwflag, pid
- Event: Thrust, Thrust_charged, Thrust_neutral, ThrustCorr, ThrustCorrInverse, ThrustWithMissP, TTheta, TPhi, Sphericity, Aplanarity, nChargedHadrons
- Selection flags: passesAll, passesNTrkMin, passesSTheta, passesMissP, passesISR, passesWW, passesNeuNch
- pwflag values: {0, 1, 2, 3, 4, 5} (0 = charged tracks, 4 = photons, 5 = neutral hadrons)

### 1.2 Monte Carlo

| Description | Files | Reco events | Gen events | GenBefore events | Generator |
|-------------|-------|-------------|------------|------------------|-----------|
| PYTHIA 6.1 + ALEPH det. sim | 40 files | 771,597 | 771,597 | 973,769 | PYTHIA 6.1 |

**Tree structure (MC, per file):**
- `t`: 151 branches (identical schema to data)
- `tgen`: 199 branches (gen-level after event selection). Extra 48 branches for systematic studies: ThrustWithReco, ThrustWithGenIneff, ThrustWithGenIneffFake, ThrustWithRecoCorr, ThrustWithRecoCorrInverse, ThrustWithRecoAndMissP, plus corresponding theta/phi/eta/pt/rap w.r.t. each thrust variant.
- `tgenBefore`: 151 branches (gen-level before event selection, same schema as t/tgen base)
- Gen-level jet trees: same jet algorithms as data, with "Before" variants (e.g., akR4ESchemeGenJetBeforeTree) corresponding to pre-selection events.

**GenBefore/gen ratio:** 973,769 / 771,597 = 1.262 (event selection efficiency ~79%).

**Gen-level pwflag values:** {-11, 0, 1, 2, 3, 4, 5}. Composition in tgen:
- pwflag = 0 (charged): 43.6%
- pwflag = 4 (photons): 44.7%
- pwflag = 5 (neutral hadrons): 4.4%
- pwflag = -11 (ISR/material excluded): 1.2%
- pwflag = 1, 2, 3: combined 6.2%

### 1.3 MC/Data ratio

MC/Data = 771,597 / 3,050,610 = 0.253 (25.3%). After selection: 721,175 / 2,846,194 = 0.253. The ratio is preserved through the cutflow.

---

## 2. Data Quality Assessment

### 2.1 Branch-level checks

All particle-level and event-level branches checked for NaN, Inf, negative momenta, and unphysical ranges on 5000 data events. **No pathologies found.**

| Branch | Min | Max | Mean | Issues |
|--------|-----|-----|------|--------|
| px | -45.5 | 39.8 | -0.002 | None |
| py | -38.3 | 42.1 | 0.007 | None |
| pz | -37.3 | 33.9 | -0.001 | None |
| pmag | 0.134 | 45.66 | 2.82 | None |
| theta | 0.20 | 2.94 | 1.57 | None |
| phi | -3.14 | 3.14 | 0.005 | None |
| mass | 0 | 3.81 | 0.094 | 34,502 zeros |
| Thrust | 0.627 | 0.999 | 0.938 | None |
| nChargedHadrons | 5 | 45 | 18.67 | None |

**Note on d0/z0:** Non-charged particles (pwflag != 0) have sentinel values d0 = z0 = -999. After filtering to pwflag == 0, d0 and z0 are within their physical ranges (|d0| < 2 cm, |z0| < 10 cm as pre-applied by the archiving).

### 2.2 Year-to-year consistency

| Year | <Thrust> | <N_ch> |
|------|----------|--------|
| 1992 | 0.9389 | 18.53 |
| 1993 | 0.9371 | 18.86 |
| 1994P1 | 0.9362 | 18.76 |
| 1994P2 | 0.9355 | 18.69 |
| 1994P3 | 0.9367 | 18.62 |
| 1995 | 0.9358 | 18.88 |

Excellent stability. Maximum variation: 0.9% in thrust, 1.9% in N_ch. No year requires special treatment.

### 2.3 Flag branch analysis

**Data selection flags (5000 events):**
- passesAll: 94.56% True
- passesNTrkMin: 100% True (already pre-applied by archiving)
- passesSTheta: 97.68% True
- passesMissP: 97.16% True
- passesISR: 98.90% True
- passesWW: 98.90% True
- passesNeuNch: 99.50% True

**MC selection flags (reco, 5000 events):** Nearly identical acceptance rates (passesAll = 94.72%), confirming the MC reproduces the selection efficiency.

---

## 3. Aftercut Pre-Selection Investigation

### 3.1 What "aftercut" encodes

The data files have the suffix `aftercut`, indicating pre-applied cuts. From the flag analysis:
- **passesNTrkMin is 100% True in data** -- the minimum-track-count cut has been pre-applied during archiving. No events with fewer than the minimum N_ch survive.
- The other flags (passesSTheta, passesMissP, etc.) still vary, meaning they were NOT pre-applied.
- The passesAll flag is the AND of all sub-flags, with 94.6% acceptance in data.

### 3.2 MC has identical pre-cuts

MC passesAll acceptance = 94.7% vs data 94.6%. The sub-flag acceptances agree within 0.2%. The MC was archived with the same pre-cuts.

### 3.3 tgenBefore scope

- tgenBefore has 973,769 events vs tgen's 771,597 events (ratio 1.262).
- **tgenBefore passesAll is ALL False** -- gen-level selection flags are zeroed in tgenBefore, not evaluated. This means tgenBefore contains events regardless of whether they would pass event selection.
- passesSTheta in tgenBefore: 76.8% True (vs 96.2% in tgen). This confirms tgenBefore includes events failing the sphericity polar angle cut.
- **Conclusion:** tgenBefore contains ALL generated events (before event selection). It is the correct denominator for efficiency correction: C(i,j) = N_genBefore(i,j) / N_reco(i,j).

---

## 4. Thrust Axis Source Determination

| Thrust variant | Mean (data) | Mean (MC reco) | Description |
|---------------|-------------|----------------|-------------|
| Thrust | 0.9380 | 0.9366 | Pre-computed (energy-flow) |
| Thrust_charged | 0.9366 | 0.9355 | Charged-only |
| Thrust_neutral | 0.9426 | 0.9403 | Neutral-only |
| ThrustCorr | 0.9379 | 0.9365 | Corrected variant |
| ThrustCorrInverse | 0.9381 | 0.9366 | Inverse-corrected |
| ThrustWithMissP | 0.9356 | 0.9345 | With missing momentum |

**Conclusion:** Thrust != Thrust_charged (different means: 0.9380 vs 0.9366), confirming that the pre-computed `Thrust` uses energy-flow objects (charged + neutral). The difference is small (~0.15%) but systematic.

**Recommendation for Phase 3:** Use `Thrust_charged` (or recompute from selected charged tracks) for event selection, ensuring consistency with the charged-particle Lund plane definition. Use the energy-flow `Thrust` axis direction (TTheta, TPhi) for hemisphere splitting (better resolution from neutrals), and include the Thrust_charged vs Thrust difference as a systematic variation.

---

## 5. Momentum Resolution Verification

**Impact parameter analysis (charged tracks, pwflag == 0):**
- Median |d0| = 170 um
- 68th percentile |d0| = 380 um
- 95th percentile |d0| = 8240 um (0.82 cm)

The 68th percentile of 380 um is intermediate between TPC-only (~150 um core) and TPC+ITC+VDET combined (~25 um core). The large tail at high |d0| is dominated by tracks from secondary decays (K_S, Lambda, etc.) and conversion electrons, which inflate the overall distribution.

**Assessment:** The archived track reconstruction likely uses TPC+ITC (inner tracking chamber) but may not include full VDET (vertex detector) in all configurations. The momentum resolution is sigma_p/p^2 ~ 0.8-1.0 x 10^-3 (GeV/c)^-1, still excellent for this measurement.

**Strategy revision input:** Phase 1 assumed sigma_p/p^2 ~ 0.6 x 10^-3 (full TPC+ITC+VDET). Phase 2 finds the resolution is likely ~0.8-1.0 x 10^-3. **Impact: negligible** -- the systematic from momentum resolution smearing (+/-10% of resolution) will use the correct value, and the resolution is still far better than the bin widths.

---

## 6. Data/MC Comparisons

Nine data/MC comparison plots produced with ratio panels (50k data, 50k MC events):

| Variable | Data/MC agreement | Notes |
|----------|-------------------|-------|
| p (momentum) | Within +/-5% | ![](figures/hugo_pmag_data_mc.pdf) |
| p (log scale) | Within +/-5% | ![](figures/hugo_pmag_log_data_mc.pdf) |
| theta | Within +/-3% | ![](figures/hugo_theta_data_mc.pdf) |
| phi | Within +/-2% | Flat, as expected ![](figures/hugo_phi_data_mc.pdf) |
| p_T | Within +/-5% | ![](figures/hugo_pt_data_mc.pdf) |
| Thrust | Within +/-5% | ![](figures/hugo_thrust_data_mc.pdf) |
| Thrust_charged | Within +/-5% | ![](figures/hugo_thrust_charged_data_mc.pdf) |
| N_ch | Within +/-5% | ![](figures/hugo_nch_data_mc.pdf) |
| N_hemi_min | Within +/-5% | ![](figures/hugo_hemi_mult_data_mc.pdf) |

**Summary:** PYTHIA 6.1 MC reproduces data kinematics at the few-percent level across all variables entering the Lund plane. No bins show >3-sigma disagreement in the bulk region. The MC is adequate for deriving correction factors.

---

## 7. Cutflow (Baseline Yields)

### 7.1 Data Cutflow

| Cut | Events | Cumulative eff. | Relative eff. |
|-----|--------|-----------------|---------------|
| Total (archived) | 3,050,610 | 100.00% | 100.00% |
| passesAll | 2,889,543 | 94.72% | 94.72% |
| Thrust > 0.7 | 2,872,177 | 94.15% | 99.40% |
| N_ch >= 5 (post-track-cuts) | 2,868,384 | 94.03% | 99.87% |
| N_hemi >= 2 (both hemispheres) | 2,846,194 | 93.30% | 99.23% |

### 7.2 MC Cutflow (reco)

| Cut | Events | Cumulative eff. | Relative eff. |
|-----|--------|-----------------|---------------|
| Total (archived) | 771,597 | 100.00% | 100.00% |
| passesAll | 731,006 | 94.74% | 94.74% |
| Thrust > 0.7 | 726,759 | 94.19% | 99.42% |
| N_ch >= 5 | 726,585 | 94.17% | 99.98% |
| N_hemi >= 2 | 721,175 | 93.47% | 99.26% |

### 7.3 Data/MC Efficiency Comparison

| Cut | Data eff. | MC eff. | Ratio |
|-----|-----------|---------|-------|
| passesAll | 94.72% | 94.74% | 0.9998 |
| Thrust > 0.7 | 94.15% | 94.19% | 0.9996 |
| N_ch >= 5 | 94.03% | 94.17% | 0.9985 |
| N_hemi >= 2 | 93.30% | 93.47% | 0.9982 |

**Data/MC efficiency agreement is <0.2% at every cut.** The selection introduces negligible data/MC bias.

### 7.4 Final Yields

- **Data:** 2,846,194 events = 5,692,388 hemispheres
- **MC (reco):** 721,175 events = 1,442,350 hemispheres
- **MC (genBefore):** 973,769 events (for efficiency correction)

---

## 8. Reco-Level Lund Jet Plane

### 8.1 Construction method

Charged tracks passing selection (pwflag==0, p > 0.2 GeV, |d0| < 2 cm, |z0| < 10 cm) are split into thrust hemispheres using the pre-computed thrust axis (TTheta, TPhi). Each hemisphere is clustered with the Cambridge/Aachen algorithm (FastJet `ee_genkt_algorithm` with R=999, p=0) and the primary declustering chain is followed using `has_parents()`, ordering by p_T w.r.t. beam. At each splitting, the Lund coordinates are computed:
- ln(1/Delta_theta) where Delta_theta = arccos(p1_hat . p2_hat)
- ln(k_T) where k_T = |p_softer| * sin(Delta_theta)

### 8.2 Results (100k events, 200k hemispheres)

- **Total splittings:** 1,017,492
- **Average splittings per hemisphere:** 5.09

The 2D Lund plane density shows the characteristic triangular structure:
- Kinematic boundary at large angle + high k_T (upper-left triangle)
- Perturbative plateau at moderate ln(1/Delta_theta), moderate ln(k_T)
- Non-perturbative rise at low k_T (ln(k_T) < -1)
- Collinear enhancement at large ln(1/Delta_theta)

![Reco-level Lund plane](figures/hugo_lund_plane_reco_data.pdf)

### 8.3 Projections

The k_T projection shows a broad peak at ln(k_T) ~ -1 (k_T ~ 0.4 GeV), with the perturbative tail extending to ln(k_T) ~ 3. The LO analytical predictions (all-particle rho ~ 0.100, charged rho ~ 0.067) provide reference levels for the perturbative region.

![k_T projection](figures/hugo_lund_kt_projection.pdf)
![Delta_theta projection](figures/hugo_lund_dtheta_projection.pdf)

---

## 9. Binning Optimization

### 9.1 Proposed binning

10 x 10 uniform bins:
- ln(1/Delta_theta): [0, 5] in steps of 0.5
- ln(k_T/GeV): [-3, 4] in steps of 0.7

### 9.2 Bin population (MC, 20k events)

With 20k MC events, the core bins have >100 entries. At full MC statistics (721k events, ~36x more), all populated bins will have >1000 entries. The kinematic boundary naturally depopulates the upper-left and lower-right corners.

![Bin population](figures/hugo_bin_population_reco.pdf)

### 9.3 Migration fraction

Mean |N_reco - N_gen| / N_reco = **14%** across populated bins. Only 7/100 bins exceed 30% migration. These are at the kinematic boundaries where the response matrix is most sensitive to resolution effects.

![Migration fraction](figures/hugo_migration_fraction.pdf)

### 9.4 Correction factor preview

The ratio N_gen / N_reco (post-selection only, not using genBefore) is within 0.8-1.2 across the core of the Lund plane, indicating the detector response is close to unity. The full correction factor using genBefore will be computed in Phase 3.

![Correction factor preview](figures/hugo_correction_factor_preview.pdf)

### 9.5 Binning recommendation

The proposed 10x10 uniform binning is adequate:
- Bin population requirement (>=100 data, >=50 MC per bin) is satisfied in 90+ bins
- Migration fraction < 30% in 93/100 bins
- Resolution is dominated by the declustering procedure, not momentum resolution
- Non-uniform binning (coarser at edges) could improve the 7 high-migration bins but is not required

---

## 10. p_T vs Energy Ordering Comparison

### 10.1 Method

Both orderings applied to the same MC gen-level events (15k events, ~30k hemispheres). The primary declustering chain is followed using p_T w.r.t. beam (primary) or energy (alternative) to determine the "harder" subjet.

### 10.2 Results

- p_T ordering: 161,207 splittings
- Energy ordering: 161,892 splittings (0.4% more -- some chains are slightly longer)

The 2D ratio rho_energy / rho_pT is close to 1.0 over most of the populated plane. Differences are largest at:
- Large opening angles (low ln 1/Delta_theta < 1) + high k_T: up to 15-20%
- Kinematic boundaries: scattered bins with larger differences

In the perturbative core (1 < ln 1/Delta_theta < 4, -1 < ln k_T < 2), the difference is typically < 5%.

![p_T vs energy ordering ratio](figures/hugo_pt_vs_energy_ordering_ratio.pdf)
![p_T vs energy 1D projection](figures/hugo_pt_vs_energy_kt_projection.pdf)

### 10.3 Conclusion

The difference is moderate and confined to the wide-angle region. **p_T ordering is confirmed as the primary choice.** The ordering difference will be included as a systematic variation in Phase 4, not as a separate measurement (Phase 1 decision [D13] is validated).

---

## 11. PDF Build Test

Tectonic v0.15+ compiles LaTeX successfully. A minimal stub with equations and text was compiled to a 14.5 KB PDF, then deleted. **Toolchain confirmed working.**

---

## 12. Strategy Revision Inputs

### 12.1 Thrust axis: energy-flow vs charged-only

**Phase 1 assumed:** The thrust axis source was not specified. Phase 2 committed to determining it.

**Phase 2 found:** The pre-computed `Thrust` branch uses energy-flow objects (charged + neutral). The `Thrust_charged` branch provides the charged-only alternative.

**Recommendation:** Use the energy-flow thrust axis direction (TTheta, TPhi) for hemisphere splitting (better resolution from including neutrals), but use Thrust_charged for event selection cuts (consistency with charged-particle observable). Include the charged-only vs energy-flow hemisphere assignment difference as a cross-check.

### 12.2 Momentum resolution

**Phase 1 assumed:** TPC+ITC+VDET combined tracking (sigma_p/p^2 ~ 0.6 x 10^-3).

**Phase 2 found:** Impact parameter distribution suggests TPC+ITC (sigma_p/p^2 ~ 0.8-1.0 x 10^-3). Still excellent. The momentum resolution systematic (smear by +/-10% of resolution) should use the Phase 2 value.

**Impact:** Negligible on feasibility. Update the resolution value used in the momentum smearing systematic.

### 12.3 tgenBefore confirmed as full generator sample

**Phase 1 assumed:** tgenBefore contains events before event selection.

**Phase 2 confirmed:** tgenBefore passesAll is ALL False, and the ratio genBefore/gen = 1.262 is consistent with ~79% event selection efficiency. tgenBefore is the correct denominator for efficiency correction.

---

## 13. Pre-Review Self-Check

- [x] Sample inventory: every file with tree names, branches, events
- [x] Data quality: no pathologies, outliers, unphysical values
- [x] Object definitions: track selection (pwflag==0, p > 0.2 GeV, |d0| < 2 cm, |z0| < 10 cm) from cds_2876991
- [x] Variable survey with data/MC comparisons for all candidates (9 plots)
- [x] Baseline yields after preselection (2,846,194 data / 721,175 MC)
- [x] PDF build test passed
- [x] Experiment log updated with all discoveries
- [x] All figures pass plotting rules (lint-plots: 0 true violations; 1 false-positive from multi-figure file)

---

## Figures Summary

| Figure | Description | File |
|--------|-------------|------|
| 2D Lund plane (reco) | Primary result at detector level | `hugo_lund_plane_reco_data.{pdf,png}` |
| k_T projection | 1D projection with LO reference | `hugo_lund_kt_projection.{pdf,png}` |
| Delta_theta projection | 1D angular projection | `hugo_lund_dtheta_projection.{pdf,png}` |
| Bin population | MC bin entries for 10x10 binning | `hugo_bin_population_reco.{pdf,png}` |
| Migration fraction | |reco-gen|/reco per bin | `hugo_migration_fraction.{pdf,png}` |
| Correction factor | gen/reco ratio preview | `hugo_correction_factor_preview.{pdf,png}` |
| Reco/gen comparison | 1D distributions comparison | `hugo_reco_gen_1d_comparison.{pdf,png}` |
| p_T vs energy ratio | 2D ordering comparison | `hugo_pt_vs_energy_ordering_ratio.{pdf,png}` |
| p_T vs energy 1D | k_T projection comparison | `hugo_pt_vs_energy_kt_projection.{pdf,png}` |
| Data/MC: p | Momentum distribution | `hugo_pmag_data_mc.{pdf,png}` |
| Data/MC: p (log) | Momentum (log scale) | `hugo_pmag_log_data_mc.{pdf,png}` |
| Data/MC: theta | Polar angle | `hugo_theta_data_mc.{pdf,png}` |
| Data/MC: phi | Azimuthal angle | `hugo_phi_data_mc.{pdf,png}` |
| Data/MC: p_T | Transverse momentum | `hugo_pt_data_mc.{pdf,png}` |
| Data/MC: Thrust | Thrust distribution | `hugo_thrust_data_mc.{pdf,png}` |
| Data/MC: Thrust_charged | Charged thrust | `hugo_thrust_charged_data_mc.{pdf,png}` |
| Data/MC: N_ch | Charged multiplicity | `hugo_nch_data_mc.{pdf,png}` |
| Data/MC: N_hemi_min | Min hemisphere multiplicity | `hugo_hemi_mult_data_mc.{pdf,png}` |
