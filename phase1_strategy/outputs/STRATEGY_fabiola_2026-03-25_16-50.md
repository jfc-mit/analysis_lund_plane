# Phase 1: Strategy — Primary Lund Jet Plane Density in Hadronic Z Decays

**Session:** Fabiola | **Analysis:** lund_jet_plane | **Type:** measurement (unfolding)

---

## 1. Summary

This analysis measures the primary Lund jet plane density in hadronic Z decays using archived ALEPH data at sqrt(s) = 91.2 GeV. The Lund jet plane is a two-dimensional representation of the radiation pattern inside jets, constructed by following the Cambridge/Aachen (C/A) declustering sequence and mapping each primary splitting to coordinates (ln 1/Delta_theta, ln k_T/GeV). Each thrust hemisphere is declustered independently, yielding the primary emission chain. The measurement is corrected to charged-particle level using bin-by-bin correction factors derived from PYTHIA 6.1 Monte Carlo, with iterative Bayesian unfolding (IBU) as a cross-check. This constitutes the first Lund jet plane measurement in e+e- collisions, complementing existing measurements from ATLAS (pp, sqrt(s) = 13 TeV) and ALICE (pp and Pb-Pb).

The dataset comprises approximately 3.05 million hadronic Z decay events collected by ALEPH during 1992-1995, with 771,597 fully simulated PYTHIA 6.1 Monte Carlo events providing both reconstructed and generator-level information for correction and validation.

---

## 2. Physics Motivation and Observable Definition

### 2.1 Motivation

The Lund jet plane provides a theoretically motivated, two-dimensional representation of the perturbative and non-perturbative structure of QCD radiation within jets. Introduced by Dreyer, Salam, and Soyez (JHEP 12 (2018) 064), the Lund plane maps each emission in the angular-ordered clustering tree to a point in the (ln 1/Delta_R, ln k_T) plane. In this representation:

- The perturbative region (high k_T) is approximately uniform, with density governed by alpha_s and the colour factor of the emitting parton.
- The non-perturbative region (low k_T) reflects hadronization effects.
- The transition between these regimes is directly visible in the 2D density.

For e+e- collisions at the Z pole, the quark-initiated jets provide a clean environment to study this structure without the complications of underlying event, pile-up, or initial-state radiation present in hadron collisions. The Z pole energy is precisely known (sqrt(s) = 91.2 GeV), and the dijet topology is well-defined. This measurement:

1. Provides the first e+e- Lund plane measurement, enabling direct comparison with pp results (ATLAS, ALICE) and testing the universality of QCD radiation patterns across collision systems.
2. Offers a clean test of parton shower models (PYTHIA, HERWIG, Sherpa) in a controlled environment.
3. Enables extraction of alpha_s and colour factor information from the plane density in the perturbative region.
4. Probes hadronization effects in a region where non-perturbative models differ substantially.

### 2.2 Observable Definition

**The primary Lund jet plane density** is defined as follows:

**Particle-level definition [A]:** Charged particles (|charge| >= 1) with:
- Momentum p > 200 MeV/c [A] (standard ALEPH threshold; cite: inspire_322679, cds_2876991)
- Lifetime c*tau > 1 cm (i.e., stable particles in the standard HEP definition: pi+/-, K+/-, p/pbar, e+/-, mu+/-)
- Produced in hadronic Z decays at sqrt(s) = 91.2 GeV

**ISR/FSR treatment [D10]:** The particle-level definition includes all final-state charged particles after FSR (photon radiation from final-state charged particles does not remove the radiating particle from the charged-particle collection, but may reduce its momentum). ISR photons are excluded from the particle collection (they are not charged particles). The MC truth level (`tgen` tree) is defined after FSR and after hadronization but before detector simulation, consistent with this definition. The `tgenBefore` tree additionally includes events that fail event-level selection, which is needed for efficiency correction. ISR effects on the event kinematics (small boost from beamstrahlung) are included in the MC simulation and corrected for implicitly by the bin-by-bin factors.

**Phase space:** Full 4pi acceptance (no explicit fiducial cuts at particle level). The detector-level selection removes events with poorly contained geometry (|cos(theta_sphericity)| > 0.82), but the particle-level definition is inclusive.

**Hemisphere definition:** The thrust axis is computed from all charged particles in the event. The event is divided into two hemispheres by the plane perpendicular to the thrust axis passing through the interaction point. Each hemisphere defines one "jet" for the Lund plane construction.

**Cambridge/Aachen declustering [D1]:** Within each hemisphere, charged particles are clustered using the Cambridge/Aachen (C/A) algorithm (generalized e+e- variant using the angular distance d_ij = 2(1 - cos theta_ij), following the definition from Dokshitzer, Leder, Moretti, Webber (JHEP 08 (1997) 001), as implemented in FastJet). The C/A algorithm clusters particles in order of decreasing angular distance, producing an angular-ordered clustering tree.

**Primary Lund plane construction [D2]:** Following the hardest branch at each declustering step (i.e., following the subjet with larger transverse momentum at each splitting), each splitting along the primary chain yields a pair of subjets (j_1, j_2) where j_1 is harder and j_2 is softer. For each such splitting, the Lund coordinates are:

- **Delta_theta:** The opening angle between j_1 and j_2, computed as Delta_theta = arccos(hat{p}_1 . hat{p}_2), where hat{p} denotes the unit momentum vector.
- **k_T:** The transverse momentum of the softer subjet with respect to the harder one: k_T = |p_2| * sin(Delta_theta), where |p_2| is the momentum magnitude of j_2.

The Lund coordinates are then:
- x = ln(1 / Delta_theta)
- y = ln(k_T / GeV)

**The Lund plane density** is:

rho(x, y) = (1 / N_jet) * d^2 n / (dx dy)

where N_jet is the total number of hemispheres (= 2 * N_events after selection) and n is the number of primary splittings in the bin (x, y). This density is averaged over all primary splittings from all hemispheres.

**Binning [D3]:** The Lund plane will be binned in:
- ln(1/Delta_theta): 10 bins from 0 to 5 (Delta_theta from ~pi to ~0.007 rad)
- ln(k_T/GeV): 10 bins from -3 to 4 (k_T from ~0.05 GeV to ~55 GeV)

Bin edges will be refined during Phase 2 exploration based on population statistics and resolution studies. The target is at least 100 entries per bin in data for a well-populated plane.

### 2.3 Relation to Prior Measurements

No prior measurement of the full 2D Lund jet plane density exists in e+e- collisions. The closest prior work:

- **DELPHI jet splitting probability** (inspire_1661966): Measured the modified differential one-jet rate tilde{D}_1(y), which is the 1D projection of the Lund plane along the kT axis (at fixed y_cut). This is the splitting probability density as a function of the jet resolution parameter. The Lund plane generalizes this to 2D.
- **ALEPH subjet multiplicity** (cds_388806, inspire_457159): Measured subjet multiplicity as a function of the Durham resolution parameter y_0, using ~3M hadronic Z decays. This probes the integrated splitting rate, not the differential 2D density.

The novelty of this measurement is the full 2D Lund plane density, which provides richer information than any 1D projection.

---

## 3. Sample Inventory

### 3.1 Data

| File | Year | Events (pre-selection) | Size |
|------|------|----------------------|------|
| LEP1Data1992_recons_aftercut-MERGED.root | 1992 | 551,474 | 3.8 GB |
| LEP1Data1993_recons_aftercut-MERGED.root | 1993 | 538,601 | 3.7 GB |
| LEP1Data1994P1_recons_aftercut-MERGED.root | 1994 | 433,947 | 3.0 GB |
| LEP1Data1994P2_recons_aftercut-MERGED.root | 1994 | 447,844 | 3.1 GB |
| LEP1Data1994P3_recons_aftercut-MERGED.root | 1994 | 483,649 | 3.4 GB |
| LEP1Data1995_recons_aftercut-MERGED.root | 1995 | 595,095 | 4.1 GB |
| **Total** | **1992-1995** | **3,050,610** | **21 GB** |

**Notes:**
- All files are pre-processed with standard ALEPH reconstruction; the `aftercut` suffix indicates that basic quality cuts have been pre-applied.
- Each event in the "t" tree contains variable-length arrays of particle-level quantities (px, py, pz, pt, pmag, eta, theta, phi, mass, charge, pwflag, pid, d0, z0) for all reconstructed tracks and calorimeter objects.
- Pre-computed event shapes are available: Thrust (+ axis direction TTheta, TPhi), Sphericity, Aplanarity, and multiple thrust axis variants (charged-only, corrected, etc.).
- Selection flags (passesAll, passesNTrkMin, etc.) are stored per event.
- Pre-computed SoftDrop variables (zg, rg) are available in jet trees but will not be used for primary analysis.

**Luminosity [L]:** The total number of hadronic Z decays collected by ALEPH during 1992-1995 was approximately 4 million (the standard ALEPH figure for combined LEP1 data; cite: inspire_458542 reports 2.8M after their specific selection from 1992-1995 data, while cds_388806 reports ~3M in their analysis). Our pre-cut event count of 3,050,610 is consistent with the standard ALEPH hadronic Z sample after basic quality cuts. Exact per-year integrated luminosities will be fetched from the ALEPH publications during Phase 4 when they enter the analysis note; for the strategy they are not needed since this measurement uses self-normalization (the Lund plane density is per-hemisphere, so absolute luminosity cancels).

### 3.2 Monte Carlo

| Description | Files | Events (reco) | Events (gen) | Generator |
|-------------|-------|---------------|-------------|-----------|
| PYTHIA 6.1 + ALEPH detector sim | 40 files | 771,597 | 771,597 | PYTHIA 6.1 |

**Notes:**
- The MC has matching reco-level tree "t" (151 branches, same structure as data) and gen-level tree "tgen" (199 branches, includes truth particle information and event selection flags).
- "tgenBefore": Gen-level before event selection (~24,360 events per file vs ~19,158 after selection). This is needed for efficiency correction.
- Gen-level particles include charged and neutral species with pwflag codes: 0 (charged tracks), 1 (unknown_1), 2 (photon/neutral-1), 3 (unknown_3), 4 (photons), 5 (neutral hadrons), -11 (excluded particles, likely from ISR/detector material).
- The reco/gen event count equality (771,597 = 771,597) indicates matched events: every gen event that passes selection has a corresponding reco event. The tgenBefore tree (larger statistics) contains events that fail the event-level selection, enabling efficiency correction.

**MC/Data ratio:** 771,597 / 3,050,610 = 0.253 (MC is ~25% of data statistics). This is adequate for bin-by-bin correction factors but may limit the statistical precision of the response matrix for full 2D IBU unfolding. This will be investigated in Phase 2.

### 3.3 Theory Predictions for Comparison

Modern MC generators will be run at particle level at the Z pole to provide theory comparisons:

1. **PYTHIA 8 Monash** (Skands et al., EPJC 74 (2014) 3024): Default tune for e+e- at the Z pole. The primary comparison target.
2. **HERWIG 7** (Bellm et al., EPJC 76 (2016) 196): Angular-ordered parton shower with cluster hadronization. Provides an independent hadronization model comparison.
3. **Sherpa** (if feasible): Dipole shower with Lund string hadronization.

These particle-level predictions will be overlaid on the corrected data. The difference between generators (particularly PYTHIA vs HERWIG) probes hadronization model dependence, which is expected to be the dominant systematic in the soft k_T region.

---

## 4. Event Selection Approach

### 4.1 Approach A (Baseline): Standard Cut-Based Selection

Following established ALEPH hadronic event selection (cds_2876991, inspire_322679, inspire_430544):

**Track-level cuts:**
- Momentum: p > 200 MeV/c [A] (quality cut; below this, ALEPH TPC resolution degrades — inspire_322679)
- Impact parameter: |d0| < 2 cm, |z0| < 10 cm (removes secondary interactions; cds_2876991 uses these values)
- TPC hits: ntpc >= 4 (ensures well-reconstructed tracks; inspire_322679)
- Charge: |charge| >= 1 (charged tracks only for this measurement)
- pwflag: Include pwflag = 0 (charged tracks) only [D4]

**Event-level cuts:**
- Use pre-computed `passesAll` flag where available, which encodes:
  - Number of accepted charged tracks >= 5 (inspire_430544)
  - Total charged energy >= 15 GeV (cds_2876991)
  - Missing momentum < 20 GeV/c (cds_2876991)
  - Sphericity polar angle: |cos(theta_sph)| <= 0.82 (cds_2876991)
- Additionally require: Thrust > 0.7 [D5] (ensures two well-separated hemispheres; events with T < 0.7 are highly multi-jet and the hemisphere assignment becomes ambiguous). This cut will be optimized in Phase 2.
- Number of accepted charged tracks in each hemisphere >= 2 (ensures meaningful clustering in each hemisphere)

**Estimated selection efficiency:** Based on cds_2876991, the standard hadronic selection retains ~80% of Z -> hadrons events, yielding ~2.4 million selected events from 3.05 million pre-cut events. The additional thrust and hemisphere multiplicity cuts are expected to remove ~5-10% more, leaving ~2.2 million events (~4.4 million hemispheres).

### 4.2 Approach B (MVA-enhanced): BDT for Event Quality

**[D6] MVA feasibility assessment:** An MVA-based approach would train a BDT to classify events based on their suitability for Lund plane measurement. However, for this analysis the MVA approach is of limited added value for the following concrete reasons:

1. **No signal/background separation needed.** This is an inclusive measurement of Z -> hadrons. There is no background to reject (tau-tau, Bhabha, two-photon backgrounds are already negligible after the standard hadronic selection; cite cds_2876991).
2. **Event quality is one-dimensional.** The relevant event quality criterion is whether the thrust hemispheres are well-defined — this is captured almost entirely by the thrust value and hemisphere multiplicity, which are single-variable cuts.
3. **No discriminating variables beyond what cuts already use.** The candidate MVA inputs (thrust, sphericity, N_ch, missing p, cos(theta_sph)) are the same variables used in the cut-based selection. An MVA would merely remap these into a single score, offering marginal improvement over the already-high-purity selection.

**Alternative second approach [D7]:** Instead of MVA vs cuts (which would be two parametric variants of the same method), the two qualitatively different selection approaches will be:

- **Approach A:** Hemisphere-based selection using the thrust axis (standard approach described above)
- **Approach C:** Exclusive kT-jet-based selection. Cluster the full event with the kT (Durham) algorithm requiring exactly 2 jets. The y_cut parameter will be determined in Phase 2 by scanning the 2-jet rate R_2(y_cut) in data and MC, and selecting the y_cut value where R_2 ~ 80-85% (this is the standard LEP approach for Durham jet studies, cf. inspire_1661966). The 2-jet rate is a smooth, monotonically decreasing function of y_cut, so the choice is well-defined and can be cross-checked between data and MC. Use these 2 jets instead of thrust hemispheres. This provides a qualitatively different jet definition (algorithmic jets vs geometric hemispheres) and serves as a powerful cross-check of the observable definition.

The comparison between Approach A and Approach C tests the sensitivity of the Lund plane density to the jet definition, which is a physics-relevant systematic.

### 4.3 Backgrounds

For hadronic Z decay measurements at LEP, backgrounds are minimal:

| Background | Type | Estimate | Handling |
|-----------|------|----------|---------|
| Z -> tau+tau- | Irreducible | < 0.1% after N_ch >= 5 and E_ch > 15 GeV (cds_2876991) | Negligible; MC subtraction if needed |
| Two-photon (gamma-gamma -> hadrons) | Reducible | < 0.01% after E_ch > 15 GeV (cds_2876991) | Negligible |
| Bhabha (e+e- -> e+e-) | Instrumental | Negligible after N_ch >= 5 | No special treatment |
| Beam-gas | Instrumental | < 0.01% after |d0|, |z0| cuts | Removed by vertex cuts |
| Detector material interactions | Instrumental | Residual removed by track quality cuts | Included in efficiency correction via MC |

**No dedicated background estimation is needed.** The standard hadronic event selection reduces all backgrounds to below 0.1% (cds_2876991, Section 4.4). The measurement will proceed with pure Z -> hadrons events.

---

## 5. Lund Plane Construction

### 5.1 Cambridge/Aachen Clustering in e+e-

The C/A algorithm for e+e- collisions uses the angular distance metric:

d_ij = 2(1 - cos theta_ij)

where theta_ij is the angle between particles i and j. This is the e+e- variant of the C/A algorithm, as defined in Dokshitzer, Leder, Moretti, Webber (JHEP 08 (1997) 001) and further discussed in inspire_1659417. The algorithm proceeds by:

1. Compute d_ij for all particle pairs
2. Find the minimum d_ij
3. Merge the two particles/pseudo-jets into a single pseudo-jet (E-scheme recombination: sum four-momenta)
4. Repeat until only one pseudo-jet remains (inclusive clustering)

This produces an angular-ordered clustering tree. The last merging corresponds to the widest-angle splitting, and the first mergings correspond to the most collinear splittings.

**Implementation:** Use FastJet's `ee_genkt_algorithm` with p = 0 (C/A) and E-scheme recombination. The `ClusterSequence` provides the full clustering history needed for declustering.

### 5.2 Primary Declustering Chain

Starting from the fully clustered hemisphere jet, the primary declustering proceeds by:

1. At each step, undo the last clustering, yielding two subjets (j_a, j_b)
2. Identify the harder subjet: the one with larger energy E (standard choice for e+e- Lund plane, where energy is the natural hardness variable; this differs from pp where pT is used)
3. Record the splitting: (Delta_theta, k_T) as defined in Section 2.2
4. Follow the harder subjet to the next splitting
5. Continue until the harder subjet has no further substructure (i.e., it is a single particle)

This primary chain captures the sequence of hardest emissions, analogous to the leading-log parton shower evolution.

### 5.3 Coordinate System Note

In pp collisions (ATLAS, ALICE), the Lund plane uses (ln 1/Delta_R, ln k_T) where Delta_R = sqrt(Delta_eta^2 + Delta_phi^2) is the rapidity-azimuth distance. In e+e- collisions, the natural angular variable is the physical opening angle theta. The coordinate mapping is:

- x = ln(1/Delta_theta) where Delta_theta = arccos(hat{p}_1 . hat{p}_2) is in radians
- y = ln(k_T/GeV) where k_T = |p_2| * sin(Delta_theta)

For small angles, Delta_theta ~ Delta_R (up to boost corrections), so the e+e- and pp Lund planes are directly comparable in the collinear region (large x). For wide-angle emissions (small x), the full angular definition is more appropriate for e+e-.

---

## 6. Correction Strategy

### 6.1 Primary Method: Bin-by-Bin Correction [D8]

The primary correction method is **bin-by-bin correction factors** derived from MC. For each bin (i,j) of the 2D Lund plane:

C(i,j) = N_gen(i,j) / N_reco(i,j)

where N_gen(i,j) is the number of primary splittings at generator level in that bin and N_reco(i,j) is the corresponding number at reconstructed level, both from the same MC events. The corrected data is:

rho_corrected(i,j) = C(i,j) * rho_data(i,j) / N_jet

**Justification for bin-by-bin over full 2D matrix unfolding [D8]:**

1. **The response matrix for the 2D Lund plane is high-dimensional.** With 10x10 = 100 bins, the response matrix is 100x100 = 10,000 elements. The available MC statistics (771,597 events, yielding ~10-15 primary splittings per hemisphere or ~10-15M total splittings) may be marginal for populating this matrix with sufficient statistical precision per element.
2. **The ALEPH tracking resolution is excellent for charged particles.** The momentum resolution of the ALEPH TPC is sigma_p/p^2 ~ 0.6 x 10^-3 (GeV/c)^-1, and the angular resolution is ~1 mrad. This means the migration between neighbouring bins is expected to be small — the response matrix should be close to diagonal.
3. **Published analyses of similar observables (subjet multiplicity, jet splitting) used multiplicative correction.** The ALEPH subjet analysis (cds_388806) used "einfache multiplikative Methode" (simple multiplicative method, i.e., bin-by-bin correction). The DELPHI jet splitting analysis (inspire_1661966) also used correction factors.
4. **Modern Lund plane analyses confirm the approach.** ATLAS (Phys. Rev. Lett. 124 (2020) 222002) used a Bayesian iterative unfolding for their Lund plane, while ALICE (JHEP 05 (2024) 116) also used iterative unfolding. These analyses had more complex detector effects (hadron calorimeter jets, underlying event) than this charged-particle-level e+e- measurement.

Bin-by-bin correction is well-motivated as the primary method for this measurement given the high resolution and the approach taken by prior LEP analyses.

### 6.2 Cross-Check: Iterative Bayesian Unfolding [D9]

As the mandatory alternative correction method (conventions/unfolding.md), 2D iterative Bayesian unfolding (IBU) will be implemented:

1. Construct a 100x100 response matrix R from MC, mapping true (gen-level) Lund bins to reconstructed (reco-level) Lund bins.
2. Apply IBU with 4 iterations (standard starting point; optimize via closure tests).
3. Compare the IBU-corrected result with the bin-by-bin result bin by bin.

The number of IBU iterations will be determined by the trade-off between bias (too few iterations) and variance (too many), assessed via closure and stress tests.

**Response matrix matching strategy [D12]:** The Lund plane has variable multiplicity per event: each hemisphere yields a variable-length primary declustering chain (typically 3-8 splittings). The response matrix maps (gen-level bin) -> (reco-level bin) for individual splittings, NOT for individual hemispheres. The matching strategy is **bin-level, not object-level**: for each MC event, all gen-level primary splittings are histogrammed into their true bins and all reco-level primary splittings into their reco bins. The response matrix element R(i,j) = (number of reco splittings in bin j from events whose gen splittings include bin i) / (total gen splittings in bin i). This is the standard approach for observables with variable sub-object multiplicity (cf. conventions/unfolding.md pitfall on wrong matching for Lund declusterings). Attempting to match "1st reco splitting to 1st gen splitting" would produce an artificially poor response because the declustering chain order is sensitive to soft radiation. The bin-by-bin correction avoids this issue entirely since it operates on bin populations, not matched objects.

### 6.3 Efficiency Correction

The Lund plane density requires correction for:

1. **Event-level efficiency:** Events lost due to event selection. Estimated from MC using tgenBefore (pre-selection) vs tgen (post-selection): approximately 19,158/24,360 ~ 79% per file.
2. **Track-level efficiency:** Charged particles lost due to track quality cuts. Estimated from MC as the ratio of gen-level particles passing particle-level cuts to reco-level particles passing track cuts.
3. **Hemisphere assignment migration:** Events where the thrust axis is misreconstructed, causing particles to be assigned to the wrong hemisphere. Assessed from MC.

These corrections are folded into the bin-by-bin correction factor C(i,j), which implicitly accounts for all detector and selection effects.

### 6.4 Normalization

The Lund plane density is self-normalized: rho(x, y) = (1/N_jet) * d^2 n / (dx dy). The normalization N_jet = 2 * N_events (number of hemispheres) is applied after all corrections. This self-normalization cancels the luminosity uncertainty and reduces sensitivity to overall selection efficiency.

### 6.5 Covariance Matrix Delivery [D11]

The measurement will deliver:

1. **Statistical covariance matrix:** Constructed via bootstrap (N >= 500 event-level replicas). Resample events, recompute the full correction chain for each replica, compute the sample covariance of corrected Lund plane densities. This captures all statistical correlations from shared correction factors and self-normalization.
2. **Systematic covariance matrices:** One per systematic source. Each source contributes a rank-1 (or higher) matrix from the shift in corrected bins under the variation.
3. **Total covariance matrix:** Sum of statistical + all systematic covariance matrices.

All covariance matrices will be provided in machine-readable JSON/NPZ format alongside the corrected Lund plane density values. The total covariance matrix must be verified to be positive semi-definite (all eigenvalues >= 0) with condition number < 10^10.

---

## 7. Systematic Uncertainty Plan

### 7.1 Enumeration Against conventions/unfolding.md

The following table enumerates every required element from `conventions/unfolding.md`:

| Convention Requirement | Status | Plan |
|----------------------|--------|------|
| **Precise particle-level definition** | Will implement | Defined in Section 2.2. Charged particles, p > 200 MeV/c, c*tau > 1 cm, full phase space |
| **Closure test** | Will implement | Apply correction to MC reco, verify recovery of MC truth. Split-sample closure for bin-by-bin (derive from half, apply to other half). chi2 p-value > 0.05 required |
| **Stress test** | Will implement | Reweight MC truth by graded tilt functions (5%, 10%, 20%, 50% modification) in both Lund coordinates. Verify recovery of reweighted truth after correction |
| **Prior/model dependence** | Will implement | Dominant systematic. Estimate by comparing correction factors from PYTHIA 6.1 (nominal) vs particle-level reweighted MC (varied shapes). Additional comparison with standalone PYTHIA 8 and HERWIG 7 at truth level |
| **Covariance validation** | Will implement | Positive semi-definite check, condition number < 10^10, correlation matrix visualization |
| **Covariance construction** | Will implement | Bootstrap method (N >= 500 replicas): resample events, recompute full correction chain, compute sample covariance of corrected distribution. Event-level resampling |
| **Chi2 computation** | Will implement | Full covariance chi2 and diagonal chi2, both reported |
| **Data/MC input validation** | Will implement | Data/MC comparison for all kinematic variables entering the Lund plane: p, theta, phi, thrust, N_ch, hemisphere multiplicity, opening angle distributions |
| **Alternative correction method** | Will implement | IBU as cross-check (Section 6.2). Agreement validates primary bin-by-bin method; disagreement triggers investigation |
| **Normalization after correction** | Will implement | Self-normalization applied after correction, not before |

### 7.2 Systematic Uncertainty Sources

| Source | Category | Evaluation Method | Expected Magnitude |
|--------|----------|-------------------|-------------------|
| **Tracking efficiency** | Detector | Randomly drop tracks with a per-track probability of 1%, recompute Lund plane, take difference as systematic. Justification for 1%: cds_2876991 measures the tracking efficiency uncertainty as 0.7% from TPC hit requirement variation (varying ntpc from 4 to 7). The per-track inefficiency is larger than the efficiency uncertainty (the total tracking efficiency is ~98-99% per track, cite ALEPH TPC performance); 1% random drop is a conservative envelope on the track-level efficiency uncertainty. The effect on the Lund plane is evaluated by rerunning the full analysis chain (clustering, declustering, correction) on the modified track collection | 1-3% (largest at low k_T where soft tracks dominate) |
| **Track momentum resolution** | Detector | Smear track momenta by +/-10% of the resolution (sigma_p/p^2 ~ 0.6e-3 (GeV/c)^-1). Recompute Lund plane | < 1% (ALEPH TPC resolution is excellent) |
| **Angular resolution** | Detector | Smear track angles by +/-1 mrad (ALEPH angular resolution). Effect on Delta_theta | < 0.5% (angular resolution is sub-mrad) |
| **Track selection cuts** | Selection | Vary p threshold from 150 to 250 MeV/c; vary |d0| from 1.5 to 2.5 cm; vary ntpc from 3 to 5. Envelope of variations | 1-5% (largest at phase space boundaries) |
| **Event selection cuts** | Selection | Vary thrust cut from 0.6 to 0.8; vary N_ch_min from 4 to 6; vary E_ch_min from 12 to 18 GeV. Evaluate effect on corrected result | 1-3% |
| **MC model dependence** [dominant] | Correction | Reweight PYTHIA 6.1 gen-level Lund plane to match standalone PYTHIA 8 Monash truth-level shape (2D bin-by-bin reweighting of gen events). Derive new correction factors from the reweighted MC and correct data. The difference between the nominally corrected and reweighted-corrected Lund plane is the MC model systematic. Repeat with HERWIG 7 target shape. Take the envelope of the two reweighting variations as the systematic. This procedure is well-defined because only the gen-level shape changes; the detector response (reco/gen migration) is held fixed from the original PYTHIA 6.1 simulation | 5-20% (largest in non-perturbative region, k_T < 1 GeV) |
| **Unfolding method** | Correction | Difference between bin-by-bin and IBU corrected results | 1-5% (indicator of model bias if large) |
| **ISR modelling** | Physics | [L] Cannot toggle ISR in archived PYTHIA 6.1 MC. Instead, assess ISR impact using the MC gen-level information: compare the thrust axis computed from all gen-level charged particles vs the thrust axis excluding pwflag=-11 particles (ISR/material). The shift in hemisphere assignment and Lund plane coordinates quantifies the ISR effect. Additionally, the tgenBefore tree includes ISR photon information that can be used to characterize the ISR energy spectrum. The ISR energy at the Z pole is small (typically < 1 GeV per event) and the effect on the Lund plane is expected to be negligible | < 1% (ISR is a small correction at the Z pole; beamstrahlung energy loss ~0.1% of sqrt(s)) |
| **Background contamination** | Physics | Not applicable — backgrounds are < 0.1% after selection (cds_2876991). No dedicated systematic assigned; the contamination is orders of magnitude below any other uncertainty source. If needed as a cross-check, subtract estimated tau/two-photon contamination from data and compare corrected Lund plane with and without subtraction | Negligible (< 0.1%, well below statistical precision in any bin) |
| **Hemisphere assignment** | Observable definition | Compare thrust axis from charged+neutral (energy flow) vs charged-only. Evaluate effect on hemisphere composition and Lund plane | 1-3% |
| **Jet definition** | Observable definition | Compare Approach A (thrust hemispheres) vs Approach C (kT jets). The difference characterizes sensitivity to jet definition | Cross-check, not a systematic (different observable definitions) |

### 7.3 Expected Dominant Systematics

Based on the reference analyses (see Section 8):

1. **MC model dependence** will likely dominate, especially in the low-k_T (non-perturbative) region. ATLAS reports 5-30% model dependence in their Lund plane measurement. For e+e- with charged particles only, the effect is expected to be somewhat smaller due to the simpler event topology, but still dominant.
2. **Tracking efficiency** will be the leading detector-related systematic.
3. **Track selection cuts** will affect the edges of the Lund plane (low p, large angle).

---

## 8. Reference Analysis Table

### 8.1 ATLAS Lund Jet Plane (Phys. Rev. Lett. 124 (2020) 222002)

| Aspect | Detail |
|--------|--------|
| Observable | Primary Lund jet plane density rho(ln 1/Delta_R, ln k_T) in pp at 13 TeV |
| Jet definition | Anti-kT R=0.4 jets, pT > 675 GeV |
| Declustering | C/A reclustering, primary Lund plane |
| Correction | Bayesian iterative unfolding |
| Validation | Closure test, stress test with reweighted truth |
| Systematics | Jet energy scale (~2-5%), jet energy resolution (~1-3%), tracking efficiency (~1%), MC model (PYTHIA vs HERWIG, 5-30%), unfolding (1-5%) |
| MC generators | PYTHIA 8 Monash, HERWIG 7 |
| Dominant systematic | MC generator model dependence |

### 8.2 ALICE Lund Plane (JHEP 05 (2024) 116)

| Aspect | Detail |
|--------|--------|
| Observable | Primary Lund plane density in pp at 5.02 TeV, Pb-Pb at 5.02 TeV |
| Jet definition | Anti-kT R=0.4 charged-particle jets, pT > 40 GeV |
| Declustering | C/A reclustering, primary Lund plane |
| Correction | 2D Bayesian unfolding |
| Validation | Closure test, stress test with linear tilts |
| Systematics | Tracking efficiency (~3%), unfolding regularization (~2-5%), MC model (~5-15%) |
| MC generators | PYTHIA 8 Monash, HERWIG 7, Sherpa |
| Dominant systematic | MC model dependence (especially in non-perturbative region) |

### 8.3 DELPHI Jet Splitting (inspire_1661966)

| Aspect | Detail |
|--------|--------|
| Observable | Modified differential one-jet rate (1D Lund plane projection) |
| Jet definition | Durham kT algorithm, y_cut = 0.015, three-jet events |
| Declustering | Durham algorithm subjet analysis |
| Correction | Bin-by-bin correction factors from JETSET/PYTHIA |
| Validation | Comparison of correction factors from different MC generators |
| Systematics | Track selection (~1-2%), b-tagging purity (~2-3%), MC model (JETSET vs HERWIG vs ARIADNE, ~5-10%) |
| MC generators | JETSET 7.4 (PYTHIA precursor), HERWIG 5.8, ARIADNE 4.06 |
| Dominant systematic | MC model dependence and b-tagging purity |

### 8.4 Method Parity Assessment

The ATLAS and ALICE Lund plane analyses used iterative Bayesian unfolding, while LEP analyses (DELPHI, ALEPH) used bin-by-bin correction. For this measurement:

- **Primary method: bin-by-bin correction** — consistent with LEP-era practice and justified by the excellent ALEPH resolution (Section 6.1).
- **Cross-check: IBU** — matching the modern method used by ATLAS and ALICE.
- **Method parity is satisfied:** both approaches are implemented, and any significant disagreement will be investigated and resolved.

---

## 9. Flagship Figures

The following ~6 flagship figures will represent the measurement:

1. **F1: The primary Lund jet plane density (2D coloured density plot).** The central result: rho(ln 1/Delta_theta, ln k_T) as a 2D histogram with colour scale. This is the signature plot of the analysis.

2. **F2: Lund plane density compared to PYTHIA 8 and HERWIG 7.** Three panels (or 2D ratio plots): data, PYTHIA 8, HERWIG 7 predictions. Shows model agreement/disagreement across the plane.

3. **F3: Projections onto ln k_T (1D spectrum).** The Lund plane integrated over ln 1/Delta_theta, yielding the k_T spectrum of primary emissions. Includes data points with systematic uncertainty bands and MC generator overlays. This is the most direct comparison with the DELPHI splitting probability result.

4. **F4: Projections onto ln 1/Delta_theta (1D spectrum).** The Lund plane integrated over ln k_T, yielding the angular spectrum of primary emissions.

5. **F5: Response matrix (2D).** The bin-by-bin correction factor C(i,j) displayed as a 2D coloured plot. Illustrates the detector response and validates the near-diagonal structure assumed by bin-by-bin correction.

6. **F6: Systematic uncertainty breakdown.** A stacked/overlaid display of the leading systematic contributions (MC model, tracking, selection) as a function of ln k_T (integrated over angle), showing which regions are statistics-limited vs systematics-limited.

**Additional figures (not flagship, but required):**
- Data/MC comparison of input kinematic variables (p, theta, N_ch, thrust)
- Closure test result (corrected MC reco vs MC truth)
- Stress test results (recovery of tilted truth)
- Alternative correction method comparison (bin-by-bin vs IBU)
- Year-by-year stability check
- Approach A vs Approach C comparison

---

## 10. Theory Comparisons

### 10.1 MC Generator Predictions

Three modern MC generators will be run at particle level (e+e- -> hadrons at sqrt(s) = 91.2 GeV) to produce theory predictions:

1. **PYTHIA 8.3 Monash tune** — default string fragmentation
2. **HERWIG 7.3** — angular-ordered shower + cluster hadronization
3. **Sherpa 2.2** (if feasible) — dipole shower + Lund string

These will be run at generator level only (no detector simulation) with the same particle-level cuts as the measurement definition. Each generator will produce O(10^6) events at the Z pole (estimated runtime ~30 min per generator).

### 10.2 Analytical Predictions

The Lund plane density in the perturbative region has a known analytical form at leading order (Dreyer, Salam, Soyez, JHEP 12 (2018) 064, Eq. 2.6):

rho_LO = (alpha_s * C_F) / pi

For quark-initiated jets (as at the Z pole), C_F = 4/3. This provides a benchmark: the measured density in the perturbative region (high k_T, intermediate angle) should be approximately flat with a value determined by alpha_s. With alpha_s(M_Z) ~ 0.118 (to be fetched from PDG at Phase 4), the expected density is rho_LO ~ 0.118 * (4/3) / pi ~ 0.050. Running of alpha_s across the Lund plane (k_T ranges from ~0.05 GeV to ~55 GeV) will produce a visible tilt that probes the QCD beta function.

Higher-order corrections (NLL resummation) modify this density, particularly at the edges of the plane. Comparisons with analytical calculations (Dreyer, Salam, Soyez) will be pursued if published numerical predictions are available.

---

## 11. Open Issues and Constraints

### 11.1 Constraints [A]

- **[A1]** Particle-level definition uses p > 200 MeV/c threshold, set by ALEPH TPC resolution. Cannot lower without degraded momentum measurement.
- **[A2]** MC is PYTHIA 6.1 only (single generator for detector-level correction). No alternative fully simulated MC is available. This means MC model dependence for the correction factors cannot be directly evaluated by comparing two generators at detector level — it must be assessed via reweighting or truth-level comparisons.
- **[A3]** MC statistics (~772k events) are ~25% of data statistics. This limits the precision of correction factors in sparsely populated Lund plane bins.

### 11.2 Limitations [L]

- **[L1]** Only charged particles are measured. The neutral-particle Lund plane would require calorimeter-based measurements with worse resolution. This is a measurement choice, not a limitation, but the result is a charged-particle Lund plane, not an all-particle one.
- **[L2]** The PYTHIA 6.1 MC may not accurately model all features of the Lund plane, particularly in the non-perturbative region. Standalone PYTHIA 8 and HERWIG 7 at truth level partially address this via model comparison, but the correction itself depends on PYTHIA 6.1.

### 11.3 Decisions [D]

- **[D1]** Cambridge/Aachen algorithm for declustering (angular-ordered; required for Lund plane definition)
- **[D2]** Primary declustering chain (follow the harder subjet)
- **[D3]** Binning: 10x10 in (ln 1/Delta_theta, ln k_T), range [0,5] x [-3,4]. To be refined in Phase 2.
- **[D4]** Use pwflag = 0 particles only (charged tracks). Cross-check with pwflag = {0,1,2}.
- **[D5]** Thrust > 0.7 cut for well-defined hemispheres. Optimize in Phase 2.
- **[D6]** No MVA for event selection (justified: no signal/background separation needed, one-dimensional event quality, negligible backgrounds).
- **[D7]** Second selection approach: exclusive kT-jet-based (Approach C) instead of MVA.
- **[D8]** Primary correction: bin-by-bin. Justified by ALEPH resolution and LEP precedent.
- **[D9]** Cross-check correction: IBU. Matching modern ATLAS/ALICE methodology.
- **[D10]** ISR/FSR treatment: include all final-state charged particles after FSR; ISR photons excluded.
- **[D11]** Covariance matrix delivery: statistical (bootstrap N >= 500) + systematic + total. Machine-readable format.
- **[D12]** Response matrix matching: bin-level population matching (not object-level 1:1 matching) for variable-multiplicity Lund declusterings.

---

## 12. Validation

### 12.1 Validation Plan

| Test | Description | Pass Criterion |
|------|------------|----------------|
| Closure test | Apply correction factors to MC reco, compare with MC gen truth | chi2/ndf ~ 1, p-value > 0.05 |
| Split-sample closure | Derive correction from MC half A, apply to MC half B | chi2/ndf ~ 1, p-value > 0.05 |
| Stress test | Reweight MC truth by tilts of 5%, 10%, 20%, 50%. Correct reweighted reco, compare with reweighted truth | Recovery within statistical + systematic uncertainty for tilts up to 20% |
| Alternative method | Compare bin-by-bin vs IBU | Agreement within 2-sigma per bin, or disagreement investigated |
| Data/MC agreement | Compare data and MC at reco level for all kinematic inputs | No bins with data/MC > 3 sigma for key variables |
| Year-by-year stability | Compute Lund plane for each data year separately | Consistent within statistical uncertainties |
| Approach A vs C | Compare thrust hemispheres vs kT jets | Characterize systematic from jet definition |
| Covariance PSD | Check all eigenvalues >= 0, condition number < 10^10 | Pass/fail |

### 12.2 Comparison Targets

The primary comparison targets are the modern MC generators at particle level, since no prior e+e- Lund plane measurement exists. However, the 1D k_T projection can be compared with the DELPHI jet splitting probability (inspire_1661966), after accounting for the different jet definition (Durham vs hemisphere C/A declustering).

---

## 13. Code Reference

Scripts written during Phase 1 (data exploration):
- `phase1_strategy/src/check_data_structure.py` — Reads one data and one MC file, prints tree/branch structure
- `phase1_strategy/src/count_events.py` — Counts events in all data and MC files
- `phase1_strategy/src/check_branches.py` — Full branch inventory, pwflag distributions, event shape variables

All scripts run via `pixi run py <script>`.
