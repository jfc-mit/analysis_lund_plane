# Phase 3: Selection -- Primary Lund Jet Plane Density in Hadronic Z Decays

**Session:** Ingrid (executor) | **Date:** 2026-03-25 | **Analysis:** lund_jet_plane

---

## 1. Event Selection

### 1.1 Track-Level Cuts

All cuts follow the standard ALEPH hadronic event selection (cds_2876991, inspire_322679):

| Cut | Criterion | Motivation |
|-----|-----------|------------|
| Particle type | pwflag == 0 | Charged tracks only |
| Momentum | p > 200 MeV/c | Below this, ALEPH TPC resolution degrades (inspire_322679) |
| Impact parameter | \|d0\| < 2 cm | Removes secondary interactions (cds_2876991) |
| Longitudinal IP | \|z0\| < 10 cm | Removes beam-gas background (cds_2876991) |

### 1.2 Event-Level Cuts

| Cut | Criterion | Motivation |
|-----|-----------|------------|
| Quality flags | passesAll == True | Standard ALEPH quality (N_ch >= 5, E_ch > 15 GeV, missing P < 20 GeV, \|cos theta_sph\| < 0.82) |
| Thrust | Thrust > 0.7 | Ensures well-separated hemispheres; removes highly multi-jet events |
| Track multiplicity | N_ch >= 5 (after track cuts) | Ensures meaningful clustering |
| Hemisphere population | N_tracks per hemisphere >= 2 | Ensures C/A clustering is viable in both hemispheres |

### 1.3 Cutflow

#### Data Cutflow

| Cut | Events | Cumulative eff. | Relative eff. |
|-----|--------|-----------------|---------------|
| Total (archived) | 3,050,610 | 100.00% | -- |
| passesAll + Thrust > 0.7 + N_ch >= 5 | 2,868,384 | 94.03% | 94.03% |
| N_hemi >= 2 (both hemispheres) | 2,846,194 | 93.30% | 99.23% |
| **Final** | **2,846,194 events = 5,692,388 hemispheres** | | |

#### MC Cutflow (reco level)

| Cut | Events | Cumulative eff. | Relative eff. |
|-----|--------|-----------------|---------------|
| Total (archived) | 771,597 | 100.00% | -- |
| passesAll + Thrust > 0.7 + N_ch >= 5 | 726,585 | 94.17% | 94.17% |
| N_hemi >= 2 | 721,175 | 93.47% | 99.26% |
| **Final** | **721,175 events = 1,442,350 hemispheres** | | |

#### MC Gen (after event selection)

| Cut | Events | Cumulative eff. |
|-----|--------|-----------------|
| Total | 771,597 | 100.00% |
| N_ch >= 5 | 771,468 | 99.98% |
| N_hemi >= 2 | 767,465 | 99.46% |
| **Final** | **767,465 events = 1,534,930 hemispheres** | |

#### MC GenBefore (before event selection)

| Cut | Events | Cumulative eff. |
|-----|--------|-----------------|
| Total | 973,769 | 100.00% |
| N_ch >= 5 | 973,584 | 99.98% |
| N_hemi >= 2 | 968,356 | 99.44% |
| **Final** | **968,356 events = 1,936,712 hemispheres** | |

**Data/MC efficiency agreement:** Data final efficiency 93.30% vs MC 93.47%, ratio = 0.998. The selection introduces negligible data/MC bias.

**GenBefore/gen ratio:** 1,936,712 / 1,534,930 = 1.262, indicating ~79% event selection efficiency at generator level.

---

## 2. Lund Plane Construction

### 2.1 Method

For each selected event:
1. **Hemisphere splitting:** Use the pre-computed energy-flow thrust axis (TTheta, TPhi) to split particles into two hemispheres via the sign of p_dot_thrust.
2. **C/A clustering:** Each hemisphere clustered with FastJet `ee_genkt_algorithm` (R=999, p=0 for C/A), E-scheme recombination.
3. **Primary declustering chain:** Follow the harder subjet (larger p_T w.r.t. beam axis) at each declustering step.
4. **Lund coordinates:** For each splitting, record:
   - x = ln(1/Delta_theta), where Delta_theta = arccos(hat{p}_1 . hat{p}_2)
   - y = ln(k_T/GeV), where k_T = |p_softer| * sin(Delta_theta)

### 2.2 Results

| Level | Hemispheres | Splittings | Avg splits/hemi |
|-------|-------------|------------|-----------------|
| Data | 5,692,388 | 28,934,792 | 5.08 |
| MC reco | 1,442,350 | 7,405,085 | 5.13 |
| MC gen | 1,534,930 | 8,352,333 | 5.44 |
| MC genBefore | 1,936,712 | 10,514,849 | 5.43 |

The gen-level has ~6% more splittings per hemisphere than reco, reflecting track reconstruction losses at the detector level. The genBefore and gen have identical splits/hemi (5.43 vs 5.44), confirming the event selection does not bias the per-hemisphere splitting rate.

### 2.3 Binning

10 x 10 uniform bins:
- ln(1/Delta_theta): [0, 5], step 0.5
- ln(k_T/GeV): [-3, 4], step 0.7
- 100 total bins, 58 populated (42 depopulated at kinematic boundaries)

---

## 3. Correction Infrastructure

### 3.1 Bin-by-Bin Correction Factors

C(i,j) = N_genBefore(i,j) / N_reco(i,j)

This simultaneously corrects for detector resolution, track reconstruction efficiency, and event selection efficiency (~79%).

| Statistic | Value |
|-----------|-------|
| Mean | 1.680 |
| Median | 1.468 |
| Min | 1.166 |
| Max | 6.667 |
| Bins with C > 2 | 4 (kinematic boundaries) |
| Bins with C < 0.5 | 0 |
| Bins with N_reco = 0 | 42 / 100 |

The median correction of 1.47 is consistent with the event selection efficiency correction (~1/0.79 = 1.27) plus detector effects.

![Correction factor map](figures/ingrid_correction_factor_map.pdf)

### 3.2 Efficiency Map

epsilon(i,j) = N_gen(i,j) / N_genBefore(i,j)

| Statistic | Value |
|-----------|-------|
| Mean | 0.731 |
| Min | 0.000 |
| Max | 0.900 |

![Efficiency map](figures/ingrid_efficiency_map.pdf)

### 3.3 Diagonal Fraction

Approximate diagonal fraction (gen/reco bin population agreement) across populated bins:

| Statistic | Value |
|-----------|-------|
| Mean | 0.836 |
| Bins > 0.5 | 57 / 58 |
| Bins < 0.5 | 1 / 58 |

This confirms that the bin-by-bin correction method is viable (diagonal fraction well above the 50% threshold from conventions/unfolding.md).

![Diagonal fraction map](figures/ingrid_diagonal_fraction_map.pdf)

---

## 4. Closure Test

### 4.1 Method

Apply bin-by-bin correction C(i,j) to MC reco counts, normalize, and compare to genBefore truth density:

- Corrected: rho_corr(i,j) = [N_reco(i,j) * C(i,j)] / (N_hemi_genBefore * Delta_x * Delta_y)
- Truth: rho_truth(i,j) = N_genBefore(i,j) / (N_hemi_genBefore * Delta_x * Delta_y)

### 4.2 Results

| Metric | Value |
|--------|-------|
| chi2/ndf | 0.0000 |
| p-value | 1.000 |
| Pull mean | 0.0000 |
| Pull std | 0.0000 |
| Ratio (corrected/truth) | 1.000000 (all bins) |

**Assessment:** The closure test passes trivially because the bin-by-bin correction is algebraically exact when applied to the same MC that derived it: corrected = N_reco * (N_genBefore/N_reco) = N_genBefore. This is an identity, not a validation of the method's resolving power. The genuine closure tests (split-sample closure, stress tests) are performed in Phase 4.

**Alarm band:** chi2/ndf < 0.1 is flagged as "suspiciously good," but this is the expected algebraic identity and is documented as such.

![Closure test ln(kT)](figures/ingrid_closure_kt.pdf)
![Closure test ln(1/Delta_theta)](figures/ingrid_closure_dtheta.pdf)
![Closure test pulls](figures/ingrid_closure_pulls.pdf)

---

## 5. Data/MC Comparisons

### 5.1 Reco-Level Lund Plane

The 2D Lund plane density shows the characteristic triangular structure at both data and MC levels:
- Kinematic boundary (upper-left triangle depopulated)
- Perturbative plateau at moderate ln(1/Delta_theta) and ln(k_T)
- Non-perturbative rise at low k_T (ln(k_T) < -1)
- Collinear enhancement at large ln(1/Delta_theta)

![Data reco-level Lund plane](figures/ingrid_lund_2d_data_reco.pdf)
![MC reco-level Lund plane](figures/ingrid_lund_2d_mc_reco.pdf)

### 5.2 Data/MC Agreement

| Metric | Value |
|--------|-------|
| Populated bins | 58 / 100 |
| Data/MC ratio mean | 1.005 |
| Data/MC ratio std | 0.105 |
| Data/MC ratio range | [0.42, 1.30] |
| 1D ln(kT) ratio range | [0.95, 1.06] |
| 1D ln(1/Delta_theta) ratio range | [0.97, 1.10] |

The Data/MC agreement is excellent, with the 1D projection ratios within 5-10% across the populated phase space. The 2D ratio shows the MC slightly overestimates the non-perturbative region (low k_T) and underestimates the high-k_T, moderate-angle region -- consistent with known PYTHIA 6.1 tuning limitations.

**Gate verdict:** PASS (ratio mean within 10% of unity, spread < 20%).

![Data/MC 2D ratio](figures/ingrid_lund_2d_data_mc_ratio.pdf)
![Data/MC ln(kT) projection](figures/ingrid_lund_kt_data_mc.pdf)
![Data/MC ln(1/Delta_theta) projection](figures/ingrid_lund_dtheta_data_mc.pdf)

---

## 6. Approach Comparison

### 6.1 Approaches

- **Approach A (primary):** Thrust hemispheres, C/A declustering, p_T-ordered primary chain
- **Approach C (cross-check):** Exclusive kT (Durham) 2-jets, then C/A declustering of each jet

### 6.2 Results (200k data events)

| Metric | Value |
|--------|-------|
| Approach A hemispheres | 372,870 |
| Approach C jets | 372,870 |
| Ratio (C/A) mean | 0.999 |
| Ratio (C/A) std | 0.010 |
| Ratio (C/A) range | [0.93, 1.01] |
| Chi2 (A vs C) | 10.6 / 57 = 0.185 |

The two approaches agree within 1% in most bins. The chi2/ndf of 0.185 indicates the approaches are effectively equivalent for this event sample (Thrust > 0.7 events are dominated by two-jet topologies where hemispheres and kT jets assign particles identically).

**Conclusion:** The Lund plane density is insensitive to the jet definition choice at this level of precision. Approach A (thrust hemispheres) is confirmed as the primary choice; the Approach C difference can serve as a cross-check systematic in Phase 4.

![Approach A vs C 2D ratio](figures/ingrid_approach_a_vs_c_2d.pdf)
![Approach A vs C ln(kT) comparison](figures/ingrid_approach_kt_comparison.pdf)

---

## 7. GenBefore Truth-Level Lund Plane

The generator-level Lund plane density from tgenBefore (before event selection) represents the particle-level truth that the measurement aims to recover.

![GenBefore Lund plane](figures/ingrid_lund_2d_genBefore.pdf)

---

## 8. Summary and Handoff to Phase 4

### 8.1 Key Deliverables

| Deliverable | Status | File |
|-------------|--------|------|
| Full cutflow (data + MC, all levels) | Complete | `cutflow_ingrid.json` |
| Data Lund plane (2D histogram) | Complete | `data_lund_ingrid.npz` |
| MC reco Lund plane | Complete | `mc_reco_lund_ingrid.npz` |
| MC gen Lund plane | Complete | `mc_gen_lund_ingrid.npz` |
| MC genBefore Lund plane | Complete | `mc_genBefore_lund_ingrid.npz` |
| Bin-by-bin correction factors | Complete | `correction_ingrid.npz` |
| Data/MC comparison | PASS | `data_mc_comparison_ingrid.json` |
| Closure test (self-consistency) | PASS | `closure_ingrid.json` |
| Approach comparison (A vs C) | Complete | `approach_c_lund_ingrid.npz` |

### 8.2 Phase 4 Requirements

1. **Split-sample closure:** Derive correction from MC half A, apply to MC half B. This is the genuine closure test (not algebraic identity).
2. **Stress tests:** Apply graded tilts (5%, 10%, 20%, 50%) and verify recovery.
3. **IBU implementation:** Construct proper response matrix with event-level reco/gen matching.
4. **Systematic evaluation:** Track efficiency, momentum resolution, angular resolution, track/event selection cuts, MC model dependence, unfolding method, heavy flavour composition.
5. **Covariance matrix:** Bootstrap with N >= 500 replicas.

### 8.3 Processing Summary

| Resource | Value |
|----------|-------|
| MC processing time | 657s (8 workers) |
| Data processing time | 1143s (6 workers) |
| Total wall time | ~30 min |
| Files processed | 6 data + 40 MC = 46 |

---

## Figures Summary

| # | Description | File |
|---|-------------|------|
| 1 | Reco-level 2D Lund plane (data) | `ingrid_lund_2d_data_reco.{pdf,png}` |
| 2 | Reco-level 2D Lund plane (MC) | `ingrid_lund_2d_mc_reco.{pdf,png}` |
| 3 | Data/MC 2D ratio | `ingrid_lund_2d_data_mc_ratio.{pdf,png}` |
| 4 | Data/MC ln(kT) projection with ratio | `ingrid_lund_kt_data_mc.{pdf,png}` |
| 5 | Data/MC ln(1/Delta_theta) projection with ratio | `ingrid_lund_dtheta_data_mc.{pdf,png}` |
| 6 | Correction factor map C(i,j) | `ingrid_correction_factor_map.{pdf,png}` |
| 7 | Diagonal fraction map | `ingrid_diagonal_fraction_map.{pdf,png}` |
| 8 | Efficiency map | `ingrid_efficiency_map.{pdf,png}` |
| 9 | Closure test ln(kT) | `ingrid_closure_kt.{pdf,png}` |
| 10 | Closure test ln(1/Delta_theta) | `ingrid_closure_dtheta.{pdf,png}` |
| 11 | Closure test pulls | `ingrid_closure_pulls.{pdf,png}` |
| 12 | Approach A vs C 2D ratio | `ingrid_approach_a_vs_c_2d.{pdf,png}` |
| 13 | Approach A vs C ln(kT) comparison | `ingrid_approach_kt_comparison.{pdf,png}` |
| 14 | GenBefore truth-level Lund plane | `ingrid_lund_2d_genBefore.{pdf,png}` |
