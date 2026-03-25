# Phase 1: Strategy -- Primary Lund Jet Plane Density in Hadronic Z Decays

**Session:** Peter (fixer) | **Analysis:** lund_jet_plane | **Type:** measurement (unfolding)
**Base artifact:** STRATEGY_fabiola_2026-03-25_16-50.md | **Arbiter verdict:** ITERATE (Sally, 2026-03-25)

---

## 1. Summary

This analysis measures the primary Lund jet plane density in hadronic Z decays using archived ALEPH data at sqrt(s) = 91.2 GeV. The Lund jet plane is a two-dimensional representation of the radiation pattern inside jets, constructed by following the Cambridge/Aachen (C/A) declustering sequence and mapping each primary splitting to coordinates (ln 1/Delta_theta, ln k_T/GeV). Each thrust hemisphere is declustered independently, yielding the primary emission chain. The measurement is corrected to charged-particle level using bin-by-bin correction factors derived from PYTHIA 6.1 Monte Carlo, with iterative Bayesian unfolding (IBU) as co-primary method. This constitutes the first full two-dimensional primary Lund jet plane density measurement in e+e- collisions, complementing existing measurements from ATLAS (pp, sqrt(s) = 13 TeV), CMS (pp, sqrt(s) = 13 TeV), ALICE (pp and Pb-Pb), and LHCb (pp, sqrt(s) = 13 TeV, light- and b-quark jets).

The dataset comprises approximately 3.05 million hadronic Z decay events collected by ALEPH during 1992-1995, with 771,597 fully simulated PYTHIA 6.1 Monte Carlo events providing both reconstructed and generator-level information for correction and validation.

---

## 2. Physics Motivation and Observable Definition

### 2.1 Motivation

The Lund jet plane provides a theoretically motivated, two-dimensional representation of the perturbative and non-perturbative structure of QCD radiation within jets. Introduced by Dreyer, Salam, and Soyez (JHEP 12 (2018) 064), the Lund plane maps each emission in the angular-ordered clustering tree to a point in the (ln 1/Delta, ln k_t) plane. In this representation:

- The perturbative region (high k_T) is approximately uniform, with density governed by alpha_s and the colour factor of the emitting parton.
- The non-perturbative region (low k_T) reflects hadronization effects.
- The transition between these regimes is directly visible in the 2D density.

For e+e- collisions at the Z pole, the quark-initiated jets provide a clean environment to study this structure without the complications of underlying event, pile-up, or initial-state radiation present in hadron collisions. The Z pole energy is precisely known (sqrt(s) = 91.2 GeV), and the dijet topology is well-defined. This measurement:

1. Provides the first full two-dimensional e+e- Lund plane measurement, enabling direct comparison with pp results (ATLAS, CMS, ALICE, LHCb) and testing the universality of QCD radiation patterns across collision systems.
2. Offers a clean test of parton shower models (PYTHIA, HERWIG, Sherpa) in a controlled environment.
3. Enables extraction of alpha_s and colour factor information from the plane density in the perturbative region, and comparison with NLL analytical predictions (Lifson, Salam, Soyez, JHEP 10 (2020) 170).
4. Probes hadronization effects in a region where non-perturbative models differ substantially.

The secondary Lund plane (following the softer branch at each declustering) is a natural extension that probes different aspects of the radiation pattern. Its feasibility with this dataset will be assessed; however, it requires separate validation infrastructure (different branch-following, separate correction factors) and is not part of the primary measurement scope.

### 2.2 Observable Definition

**The primary Lund jet plane density** is defined as follows.

**Particle-level definition [A]:** Charged particles (|charge| >= 1) with:
- Momentum p > 200 MeV/c [A] (standard ALEPH threshold; cite: inspire_322679, cds_2876991)
- Lifetime c*tau > 1 cm (i.e., stable particles in the standard HEP definition: pi+/-, K+/-, p/pbar, e+/-, mu+/-)
- Produced in hadronic Z decays at sqrt(s) = 91.2 GeV

**ISR/FSR treatment [D10]:** The particle-level definition includes all final-state charged particles after FSR (photon radiation from final-state charged particles does not remove the radiating particle from the charged-particle collection, but may reduce its momentum). ISR photons are excluded from the particle collection (they are not charged particles). The MC truth level (`tgen` tree) is defined after FSR and after hadronization but before detector simulation, consistent with this definition. The `tgenBefore` tree additionally includes events that fail event-level selection, which is needed for efficiency correction. ISR effects on the event kinematics (small boost from beamstrahlung) are included in the MC simulation and corrected for implicitly by the bin-by-bin factors.

**Phase space:** Full 4pi acceptance (no explicit fiducial cuts at particle level). The detector-level selection removes events with poorly contained geometry (|cos(theta_sphericity)| > 0.82), but the particle-level definition is inclusive.

**Hemisphere definition:** The thrust axis is computed from all charged particles in the event. The event is divided into two hemispheres by the plane perpendicular to the thrust axis passing through the interaction point. Each hemisphere defines one "jet" for the Lund plane construction.

**Cambridge/Aachen declustering [D1]:** Within each hemisphere, charged particles are clustered using the Cambridge/Aachen (C/A) algorithm (generalized e+e- variant using the angular distance d_ij = 2(1 - cos theta_ij), following the definition from Dokshitzer, Leder, Moretti, Webber (JHEP 08 (1997) 001), as implemented in FastJet). The C/A algorithm clusters particles in order of decreasing angular distance, producing an angular-ordered clustering tree.

**Primary Lund plane construction [D2]:** Following the hardest branch at each declustering step. The foundational paper (Dreyer, Salam, Soyez, JHEP 12 (2018) 064, Section 2.1) defines the harder branch as the subjet with larger **transverse momentum p_T with respect to the beam axis**: "labelled such that p_{ta} > p_{tb}, where p_{ti} is the transverse momentum of i with respect to the colliding beams." This definition is native to pp collisions where p_T is the natural ordering variable.

**Hardness variable for e+e- [D13]:** For e+e- collisions at the Z pole, where jets are produced roughly isotropically in the centre-of-mass frame and the beam axis has no preferred role, the ordering variable requires adaptation. **The primary hardness variable for this analysis is p_T with respect to the beam axis** (matching the foundational paper definition), with **energy ordering as a systematic variation**. The rationale:

- p_T ordering preserves direct comparability with pp Lund plane measurements (ATLAS, CMS, ALICE, LHCb), which all use p_T ordering.
- For jets in the forward/backward region (along the beam), p_T ordering and energy ordering differ by factors of order sin(theta_jet). At the Z pole with the thrust-based event selection (thrust > 0.7), the thrust axis is well-separated from the beam, so the difference is expected to be moderate for most of the sample.
- The difference between p_T-ordered and energy-ordered primary chains will be quantified as a systematic variation in Phase 2. If the difference is large, both will be presented as separate measurements.

This replaces the previous unverified claim that energy ordering is the "standard choice for e+e-." No such standard exists in the literature; the foundational paper uses p_T ordering throughout.

For each splitting along the primary chain, the pair of subjets (j_1, j_2) is identified where j_1 is the harder subjet (larger p_T w.r.t. beam) and j_2 is the softer. The Lund coordinates are:

- **Delta_theta:** The opening angle between j_1 and j_2, computed as Delta_theta = arccos(hat{p}_1 . hat{p}_2), where hat{p} denotes the unit momentum vector.
- **k_T:** The transverse momentum of the softer subjet with respect to the harder one: k_T = |p_2| * sin(Delta_theta), where |p_2| is the momentum magnitude of j_2.

The Lund coordinates are then:
- x = ln(1 / Delta_theta)
- y = ln(k_T / GeV)

**Coordinate adaptation from pp (e+e- vs pp distinction):** The foundational paper (Dreyer, Salam, Soyez 2018) defines coordinates for pp collisions using rapidity-azimuth distance:

- pp definition: Delta = Delta_{ab} = sqrt((y_a - y_b)^2 + (phi_a - phi_b)^2), and k_t = p_{tb} * Delta_{ab} (Eq. 2.1a).
- e+e- definition (this analysis): Delta_theta = arccos(hat{p}_1 . hat{p}_2) (full opening angle), and k_T = |p_2| * sin(Delta_theta).

The key difference is the use of **sin(Delta_theta)** in the e+e- k_T definition versus the small-angle approximation **Delta** used in pp. For small angles (Delta_theta << 1), sin(Delta_theta) ~ Delta_theta ~ Delta_R (up to boost corrections), so the two definitions converge in the collinear region (large ln 1/Delta). For wide-angle emissions (Delta_theta ~ 1 rad), sin(Delta_theta) vs Delta_theta differs by up to ~16% (sin(1) = 0.841 vs 1.0). This is the regime where cross-collider comparison requires care.

**Cross-collider validity regime:** Direct bin-by-bin comparison of the e+e- and pp Lund planes is valid in the collinear region (ln 1/Delta > ~1, i.e., Delta < ~0.37 rad), where sin(theta) ~ theta ~ Delta_R. In the wide-angle region (ln 1/Delta < 1), the coordinate mapping introduces ~10-15% distortions, and comparisons should account for this. Additionally, pp jets have contributions from ISR, MPI, and underlying event at large Delta that are absent in e+e-. Quantitative cross-collider comparison should be restricted to the collinear, perturbative region of the plane.

**The Lund plane density** is:

rho(x, y) = (1 / N_jet) * d^2 n / (dx dy)

where N_jet is the total number of hemispheres (= 2 * N_events after selection) and n is the number of primary splittings in the bin (x, y). This density is averaged over all primary splittings from all hemispheres.

**Discrete binned formula:** In practice, the density is computed in finite bins:

rho(i, j) = (1 / N_jet) * n(i, j) / (Delta_x_i * Delta_y_j)

where n(i, j) is the number of primary splittings in bin (i, j), Delta_x_i = x_{i+1} - x_i is the bin width in ln(1/Delta_theta), and Delta_y_j = y_{j+1} - y_j is the bin width in ln(k_T/GeV). For uniform binning with Delta_x = 0.5 and Delta_y = 0.7, each bin has area 0.35.

**Binning [D3]:** The Lund plane will be binned in:
- ln(1/Delta_theta): 10 bins from 0 to 5 (Delta_theta from ~pi to ~0.007 rad)
- ln(k_T/GeV): 10 bins from -3 to 4 (k_T from ~0.05 GeV to ~55 GeV)

**Binning justification and optimization plan:** Uniform binning is adopted as the starting point because resolution studies have not yet been performed and uniform bins provide a model-independent baseline. The ATLAS Lund plane measurement (Phys. Rev. Lett. 124 (2020) 222002) used non-uniform binning optimized for detector resolution and population statistics. The ALICE measurement (JHEP 05 (2024) 116) also used non-uniform binning. The CMS measurement (JHEP 05 (2024) 116, arXiv:2312.16343) used non-uniform binning as well. The ALEPH detector's superior charged-particle resolution compared to hadron-collider calorimetric measurements may justify finer or different binning.

**Phase 2 binning deliverables:**
- [ ] Migration fraction per bin from the response matrix (off-diagonal fraction < 30% target)
- [ ] Resolution vs bin width study: plot sigma(reco - gen) for both Lund coordinates as a function of the coordinate value
- [ ] Bin population study: require >= 100 data entries per bin (minimum) and >= 50 MC entries per bin
- [ ] Evaluate non-uniform binning (coarser at edges of the plane where resolution degrades or statistics are limited)
- [ ] Compare uniform and optimized binning migration matrices side-by-side

Bin edges will be refined during Phase 2 exploration based on these studies.

### 2.3 Relation to Prior Measurements

No prior measurement of the full 2D Lund jet plane density exists in e+e- collisions. The closest prior work:

- **DELPHI jet splitting probability** (inspire_1661966): Measured the modified differential one-jet rate tilde{D}_1(y), which is the 1D projection of the Lund plane along the kT axis (at fixed y_cut). This is the splitting probability density as a function of the jet resolution parameter. The Lund plane generalizes this to 2D.
- **ALEPH subjet multiplicity** (cds_388806, inspire_457159): Measured subjet multiplicity as a function of the Durham resolution parameter y_0, using ~3M hadronic Z decays. This probes the integrated splitting rate, not the differential 2D density.

The novelty of this measurement is the first full two-dimensional primary Lund jet plane density, which provides richer information than any 1D projection.

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

**Pre-selection investigation [Phase 2 deliverable]:** The `aftercut` label indicates pre-applied cuts, but the exact cuts are not documented in the data files. Phase 2 must:
- [ ] Investigate what pre-selection the `aftercut` label encodes by comparing event counts and kinematic distributions against expectations from documented ALEPH selections
- [ ] Verify that the MC has identical pre-cuts applied (compare `passesAll` flag acceptance between data and MC)
- [ ] Determine the scope of `tgenBefore`: does it contain all generated events, or only those passing some generator-level pre-selection? Compare tgenBefore event counts with expected Z -> hadrons cross-section times luminosity

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
3. **Sherpa** [D14]: Dipole shower with Lund string hadronization. Sherpa's e+e- -> hadrons process at the Z pole requires explicit configuration. Feasibility will be assessed in Phase 2 by attempting to generate 10k events. If Sherpa's e+e- process is not available or produces unphysical results, this will be documented and the comparison will proceed with PYTHIA 8 and HERWIG 7 only.

**Analytical predictions:**

4. **LO QCD prediction** (Dreyer, Salam, Soyez, JHEP 12 (2018) 064, Eq. 2.6): rho_LO = 2 * alpha_s(k_T) * C_F / pi in the soft-collinear limit. See Section 10.2.
5. **NLL QCD prediction** (Lifson, Salam, Soyez, JHEP 10 (2020) 170): All-order single-logarithmic calculation of the primary Lund plane density, achieving 5-7% precision at high k_T. This paper provides numerical predictions for pp jets; applicability to e+e- (quark-initiated jets, no ISR/MPI contributions) will be investigated. The NLL prediction includes running coupling, collinear splitting function effects, and soft large-angle logarithms. If numerical predictions for quark jets are available (or extractable from the published results), they will be overlaid on the measurement — transforming this from a generator-tuning exercise into a quantitative test of perturbative QCD.

These particle-level predictions will be overlaid on the corrected data. The difference between generators (particularly PYTHIA vs HERWIG) probes hadronization model dependence, which is expected to be the dominant systematic in the soft k_T region.

### 3.4 Published Comparison Data

**DELPHI splitting probability (inspire_1661966):** The DELPHI measurement of the modified differential 2-jet rate provides a 1D projection related to the Lund plane. Representative data points will be extracted from HEPData (if available) or digitized from the published figures. **Caveat:** The DELPHI observable uses the Durham kT algorithm with specific y_cut values, not C/A declustering of hemispheres. The comparison is approximate and requires coordinate transformation (y_cut -> k_T at fixed sqrt(s)). The ln k_T projection of our measurement can be qualitatively compared after accounting for the different jet definition.

**ATLAS Lund plane (Phys. Rev. Lett. 124 (2020) 222002):** HEPData record ins1845479. Representative data points for the 2D density and 1D projections will be extracted. **Caveat:** ATLAS measures anti-kT R=0.4 jets with p_T > 675 GeV in pp at 13 TeV, using all particles (charged + neutral). The different collision system, jet definition, energy scale, and particle content mean comparison is qualitative only — useful for validating the general structure (flat perturbative plateau, non-perturbative rise) but not for bin-by-bin agreement. Cross-collider comparison is meaningful only in the collinear, perturbative region (see Section 2.2).

**CMS Lund plane (JHEP 05 (2024) 116, arXiv:2312.16343):** HEPData record available. Measures charged-particle Lund plane for anti-kT R=0.4 and R=0.8 jets with p_T > 700 GeV in pp at 13 TeV. The charged-particle definition makes this the closest pp comparison to our measurement.

---

## 4. Event Selection Approach

### 4.1 Approach A (Baseline): Standard Cut-Based Selection

Following established ALEPH hadronic event selection (cds_2876991, inspire_322679, inspire_430544):

**Track-level cuts:**
- Momentum: p > 200 MeV/c [A] (quality cut; below this, ALEPH TPC resolution degrades -- inspire_322679)
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
2. **Event quality is one-dimensional.** The relevant event quality criterion is whether the thrust hemispheres are well-defined -- this is captured almost entirely by the thrust value and hemisphere multiplicity, which are single-variable cuts.
3. **No discriminating variables beyond what cuts already use.** The candidate MVA inputs (thrust, sphericity, N_ch, missing p, cos(theta_sph)) are the same variables used in the cut-based selection. An MVA would merely remap these into a single score, offering marginal improvement over the already-high-purity selection.

**Alternative second approach [D7]:** Instead of MVA vs cuts (which would be two parametric variants of the same method), the two qualitatively different selection approaches will be:

- **Approach A:** Hemisphere-based selection using the thrust axis (standard approach described above)
- **Approach C:** Exclusive kT-jet-based selection. Cluster the full event with the kT (Durham) algorithm requiring exactly 2 jets. The y_cut parameter will be determined in Phase 2 by scanning the 2-jet rate R_2(y_cut) in data and MC, and selecting the y_cut value where R_2 ~ 80-85% (this is the standard LEP approach for Durham jet studies, cf. inspire_1661966). The 2-jet rate is a smooth, monotonically decreasing function of y_cut, so the choice is well-defined and can be cross-checked between data and MC. Use these 2 jets instead of thrust hemispheres. This provides a qualitatively different jet definition (algorithmic jets vs geometric hemispheres) and serves as a powerful cross-check of the observable definition.

**Note on limited independence at high thrust:** At high thrust (T > 0.7), thrust hemispheres and Durham 2-jets agree on >90% of particle assignments. The qualitative difference is in the treatment of soft, wide-angle particles near the hemisphere boundary. The comparison is most informative for events near the thrust cut boundary (T ~ 0.7) where jet definitions diverge most.

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
2. Identify the harder subjet: the one with larger transverse momentum p_T with respect to the beam axis [D13] (following Dreyer, Salam, Soyez 2018, Section 2.1, which defines "labelled such that p_{ta} > p_{tb}"). This is the primary ordering variable. Energy ordering is evaluated as a systematic variation.
3. Record the splitting: (Delta_theta, k_T) as defined in Section 2.2
4. Follow the harder subjet to the next splitting
5. Continue until the harder subjet has no further substructure (i.e., it is a single particle)

This primary chain captures the sequence of hardest emissions, analogous to the leading-log parton shower evolution.

### 5.3 Coordinate System: e+e- vs pp

The foundational Lund plane paper (Dreyer, Salam, Soyez 2018) is written for pp collisions. The coordinate definitions differ between pp and e+e-:

**pp definition (Dreyer, Salam, Soyez 2018, Eq. 2.1a):**
- Angular distance: Delta = Delta_{ab} = sqrt((y_a - y_b)^2 + (phi_a - phi_b)^2) (rapidity-azimuth)
- Transverse momentum: k_t = p_{tb} * Delta_{ab}
- Lund coordinates: (ln 1/Delta, ln k_t)

**e+e- definition (this analysis):**
- Angular distance: Delta_theta = arccos(hat{p}_1 . hat{p}_2) (full 3D opening angle, in radians)
- Transverse momentum: k_T = |p_2| * sin(Delta_theta)
- Lund coordinates: (ln 1/Delta_theta, ln k_T)

**Key differences:**
1. **sin(Delta_theta) vs Delta_theta:** The e+e- k_T uses sin(Delta_theta), not the small-angle approximation Delta_theta. For Delta_theta < 0.3 rad, sin(theta)/theta > 0.985 (< 1.5% difference). For Delta_theta = 1 rad, sin(1)/1 = 0.841 (16% difference). This matters for the wide-angle region of the Lund plane (ln 1/Delta_theta < 1).
2. **3D angle vs rapidity-azimuth:** The e+e- opening angle is a true 3D angle, not a rapidity-azimuth distance. For central jets in pp, Delta_R ~ Delta_theta. For forward jets, the mapping depends on the jet rapidity.
3. **No ISR/MPI/UE:** The e+e- Lund plane has no contributions from initial-state radiation, multi-parton interactions, or underlying event at large angles. The large-Delta region in e+e- is purely final-state QCD radiation.

**Cross-collider comparison validity:** The e+e- and pp Lund planes are directly comparable (bin-by-bin) only in the collinear, perturbative region where sin(theta) ~ theta ~ Delta_R and ISR/MPI contributions are negligible. For quantitative cross-collider comparison, the coordinate transformation must be applied explicitly. See Section 2.2 for the validity regime.

---

## 6. Correction Strategy

### 6.1 Co-Primary Methods: Bin-by-Bin Correction and IBU [D8, D9]

Both bin-by-bin correction and iterative Bayesian unfolding are adopted as co-primary methods. The final result will be presented using whichever method passes all stress tests; if both pass, the method with smaller total uncertainty will be primary. This acknowledges that all four modern Lund plane measurements (ATLAS 2020, ALICE 2024, CMS 2024, LHCb 2025) use iterative unfolding, while LEP-era analyses (DELPHI, ALEPH) used bin-by-bin correction.

**Method A: Bin-by-bin correction.** For each bin (i,j) of the 2D Lund plane:

C(i,j) = N_gen_before(i,j) / N_reco(i,j)

where N_gen_before(i,j) is the number of primary splittings at generator level **from all events in tgenBefore** (i.e., before event-level selection) in that bin, and N_reco(i,j) is the number of primary splittings at reconstructed level from selected events. This combined correction factor simultaneously accounts for:
- Detector resolution and track reconstruction effects (migration between bins)
- Event-level selection efficiency (~79%)
- Track-level reconstruction efficiency

By using tgenBefore (pre-selection) in the numerator and reco (post-selection) in the denominator, the efficiency correction is explicitly folded into C(i,j). This avoids double-counting that would arise from a separate efficiency correction.

**Justification for bin-by-bin as co-primary [D8]:**

1. **The ALEPH tracking resolution is excellent for charged particles.** The momentum resolution of the ALEPH TPC+ITC+VDET combined tracking is sigma_p/p^2 ~ 0.6 x 10^-3 (GeV/c)^-1, and the angular resolution is ~1 mrad (see Section 7.2 for resolution discussion). This means the migration between neighbouring bins is expected to be small -- the response matrix should be close to diagonal.
2. **Published LEP analyses used multiplicative correction.** The ALEPH subjet analysis (cds_388806) used bin-by-bin correction. The DELPHI jet splitting analysis (inspire_1661966) also used correction factors.
3. **MC statistics may limit IBU precision.** With 10x10 = 100 bins, the response matrix has 10,000 elements. The available MC statistics (771k events) may be marginal for some bins.

**Method B: Iterative Bayesian Unfolding (IBU).** The 2D IBU will be implemented as the co-primary method:

1. Construct the response matrix R(i,j -> k,l) from MC, where (i,j) is the true-level bin and (k,l) is the reco-level bin. **R is a proper migration probability matrix:** each element R(i,j -> k,l) = N(true in bin (i,j) AND reco in bin (k,l)) / N(true in bin (i,j)). Each row sums to <= 1 (the deficit from 1 accounts for events that are generated but not reconstructed, i.e., efficiency losses). This is the standard definition required for IBU to converge correctly.
2. Apply IBU with 4 iterations (standard starting point; optimize via closure tests).
3. The prior for the first iteration is the reco-level distribution.

The number of IBU iterations will be determined by the trade-off between bias (too few iterations) and variance (too many), assessed via closure and stress tests.

**Response matrix matching strategy [D12]:** The Lund plane has variable multiplicity per event: each hemisphere yields a variable-length primary declustering chain (typically 3-8 splittings). The response matrix maps (gen-level bin) -> (reco-level bin) for individual splittings, NOT for individual hemispheres. The matching strategy is **bin-level, not object-level**: for each MC event, all gen-level primary splittings are histogrammed into their true bins and all reco-level primary splittings into their reco bins. This avoids the pitfall identified in conventions/unfolding.md: attempting to match "1st reco splitting to 1st gen splitting" would produce an artificially poor response because the declustering chain order is sensitive to soft radiation.

### 6.2 Orthogonality of Model Dependence and Unfolding Method Systematics

The systematic table (Section 7.2) lists both "MC model dependence" (reweighting) and "Unfolding method" (bin-by-bin vs IBU difference). These two sources share the same underlying MC (PYTHIA 6.1) and are not fully independent. To avoid double-counting:

- **MC model dependence** is evaluated by reweighting the gen-level truth and re-deriving correction factors. This tests sensitivity to the assumed truth shape while holding the detector response fixed.
- **Unfolding method** is evaluated as the difference between bin-by-bin and IBU applied to the same (nominal) MC. This tests sensitivity to the mathematical correction procedure while holding the truth model fixed.

The two are approximately orthogonal because model dependence probes the truth-shape sensitivity while unfolding method probes the inversion-procedure sensitivity. However, if the IBU result with reweighted MC differs from the bin-by-bin result with reweighted MC by more than the quadrature sum of the individual systematics, the larger envelope will be taken as the combined model+method systematic (i.e., the systematics will not be added in quadrature).

### 6.3 Efficiency Correction

The Lund plane density requires correction for:

1. **Event-level efficiency:** Events lost due to event selection. Estimated from MC using tgenBefore (pre-selection) vs tgen (post-selection): approximately 19,158/24,360 ~ 79% per file.
2. **Track-level efficiency:** Charged particles lost due to track quality cuts. Estimated from MC as the ratio of gen-level particles passing particle-level cuts to reco-level particles passing track cuts.
3. **Hemisphere assignment migration:** Events where the thrust axis is misreconstructed, causing particles to be assigned to the wrong hemisphere. Assessed from MC.

**Explicit formula:** These corrections are folded into the bin-by-bin correction factor C(i,j) = N_gen_before(i,j) / N_reco(i,j) as defined in Section 6.1, which uses tgenBefore (pre-selection) in the numerator. This automatically includes the event-level efficiency. For IBU, efficiency is applied as a separate multiplicative factor after unfolding: rho_corrected = rho_unfolded / epsilon(i,j), where epsilon(i,j) = N_gen(i,j) / N_gen_before(i,j) is the per-bin event selection efficiency.

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
| **Stress test** | Will implement | Reweight MC truth by graded tilt functions (5%, 10%, 20%, 50% modification) in both Lund coordinates independently and as a 2D correlated tilt. Verify recovery of reweighted truth after correction. Tilt functional form: w(x) = 1 + epsilon * (x - x_mean) / (x_max - x_mean), applied independently in ln(1/Delta_theta), in ln(k_T), and as a 2D product tilt w(x,y) = w_x(x) * w_y(y). The epsilon values are 0.05, 0.10, 0.20, 0.50 |
| **Prior/model dependence** | Will implement | Dominant systematic. Estimate by comparing correction factors from PYTHIA 6.1 (nominal) vs particle-level reweighted MC (varied shapes). Additional comparison with standalone PYTHIA 8 and HERWIG 7 at truth level |
| **Covariance validation** | Will implement | Positive semi-definite check, condition number < 10^10, correlation matrix visualization |
| **Covariance construction** | Will implement | Bootstrap method (N >= 500 replicas): resample events, recompute full correction chain, compute sample covariance of corrected distribution. Event-level resampling |
| **Chi2 computation** | Will implement | Full covariance chi2 and diagonal chi2, both reported |
| **Data/MC input validation** | Will implement | Data/MC comparison for all kinematic variables entering the Lund plane: p, theta, phi, thrust, N_ch, hemisphere multiplicity, opening angle distributions |
| **Alternative correction method** | Will implement | IBU as co-primary method (Section 6.1). Agreement validates methods; disagreement triggers investigation |
| **Normalization after correction** | Will implement | Self-normalization applied after correction, not before |

### 7.2 Systematic Uncertainty Sources

| Source | Category | Evaluation Method | Expected Magnitude |
|--------|----------|-------------------|-------------------|
| **Tracking efficiency** | Detector | Randomly drop tracks with a per-track probability of 1%, recompute Lund plane, take difference as systematic. Justification for 1%: The ALEPH TPC per-track efficiency is ~98.5% for isolated tracks with p > 200 MeV/c in the barrel region (ALEPH Collaboration, "Performance of the ALEPH detector at LEP," NIM A 360 (1995) 481-506, Table 3). The 0.7% uncertainty from TPC hit requirement variation (cds_2876991, varying ntpc from 4 to 7) is the systematic uncertainty on the efficiency, not the inefficiency itself. The 1% random drop is chosen as approximately 1 sigma above the measured ~1.5% per-track inefficiency, providing a conservative systematic envelope. The effect on the Lund plane is evaluated by rerunning the full analysis chain (clustering, declustering, correction) on the modified track collection | 1-3% (largest at low k_T where soft tracks dominate) |
| **Track momentum resolution** | Detector | Smear track momenta by +/-10% of the resolution. **Resolution note:** The ALEPH tracking system consists of TPC, ITC (Inner Tracking Chamber), and VDET (vertex detector). The combined TPC+ITC+VDET resolution is sigma_p/p^2 ~ 0.6 x 10^-3 (GeV/c)^-1. TPC-only resolution is ~1.2 x 10^-3 (GeV/c)^-1. For the archived data, the reconstruction likely uses the combined tracking (standard ALEPH reconstruction). **Phase 2 must verify** which detectors contribute to the archived track reconstruction by examining the track parameter distributions (impact parameter resolution is a diagnostic: sigma_d0 ~ 25 um for combined vs ~150 um for TPC-only). The systematic will use the verified resolution value | < 1% (ALEPH tracking resolution is excellent) |
| **Angular resolution** | Detector | Smear track angles by +/-1 mrad (ALEPH angular resolution). Effect on Delta_theta | < 0.5% (angular resolution is sub-mrad) |
| **Track selection cuts** | Selection | Vary p threshold from 150 to 250 MeV/c; vary |d0| from 1.5 to 2.5 cm; vary ntpc from 3 to 5. Envelope of variations | 1-5% (largest at phase space boundaries) |
| **Event selection cuts** | Selection | Vary thrust cut from 0.6 to 0.8; vary N_ch_min from 4 to 6; vary E_ch_min from 12 to 18 GeV. Evaluate effect on corrected result | 1-3% |
| **MC model dependence** [dominant] | Correction | Reweight PYTHIA 6.1 gen-level Lund plane to match standalone PYTHIA 8 Monash truth-level shape (2D bin-by-bin reweighting of gen events). Derive new correction factors from the reweighted MC and correct data. The difference between the nominally corrected and reweighted-corrected Lund plane is the MC model systematic. Repeat with HERWIG 7 target shape. Take the envelope of the two reweighting variations as the systematic. **Limitation acknowledged:** Reweighting changes the gen-level shape but holds the detector response fixed, which is approximately correct only when the response is locally linear and the reweighting factors are moderate. **Diagnostic:** If reweighting factors exceed 3x in any bin, the linear-response assumption is suspect. In that case, verify that the reco-level shape migrates as expected (compare reweighted gen -> predicted reco via response matrix vs actual reco-level reweighted distribution). Flag bins where the diagnostic fails | 5-20% (largest in non-perturbative region, k_T < 1 GeV) |
| **Unfolding method** | Correction | Difference between bin-by-bin and IBU corrected results. See Section 6.2 for orthogonality discussion with MC model dependence | 1-5% (indicator of model bias if large) |
| **Heavy flavour composition** | Physics | The Z pole produces bb-bar pairs (R_b = 0.2163 +/- 0.0007, PDG) and cc-bar pairs (R_c = 0.172 +/- 0.003, PDG). The b-quark mass (m_b ~ 4.2 GeV) creates a dead-cone effect (suppression of collinear radiation at angles theta < m_b/E_b), producing measurably different Lund plane densities for b-quark jets (demonstrated by LHCb, Phys. Rev. D 112 (2025) 072015). With ~22% of hemispheres containing b-quarks, this is a significant fraction of the sample with different physics. **Evaluation:** Reweight the MC b-fraction by +/-2% (corresponding to the R_b uncertainty) and re-derive correction factors. Additionally, split the MC sample by generator-level flavour tag (b vs light) and quantify the b-quark contribution per Lund plane bin. This provides both the systematic uncertainty from the b-fraction and a characterization of the dead-cone signature | 1-5% (largest in the collinear region where dead-cone effect is strongest) |
| **ISR modelling** | Physics | [L] Cannot toggle ISR in archived PYTHIA 6.1 MC. Instead, assess ISR impact using the MC gen-level information: compare the thrust axis computed from all gen-level charged particles vs the thrust axis excluding pwflag=-11 particles (ISR/material). The shift in hemisphere assignment and Lund plane coordinates quantifies the ISR effect. Additionally, the tgenBefore tree includes ISR photon information that can be used to characterize the ISR energy spectrum. The ISR energy at the Z pole is small (typically < 1 GeV per event) and the effect on the Lund plane is expected to be negligible | < 1% (ISR is a small correction at the Z pole; beamstrahlung energy loss ~0.1% of sqrt(s)) |
| **Background contamination** | Physics | Not applicable -- backgrounds are < 0.1% after selection (cds_2876991). No dedicated systematic assigned; the contamination is orders of magnitude below any other uncertainty source. If needed as a cross-check, subtract estimated tau/two-photon contamination from data and compare corrected Lund plane with and without subtraction | Negligible (< 0.1%, well below statistical precision in any bin) |
| **Thrust-axis resolution** | Detector | The thrust axis reconstruction has finite resolution from track momentum smearing. Evaluate by smearing track momenta within their resolution and recomputing the thrust axis, then measuring the hemisphere migration rate (fraction of particles that change hemisphere assignment). This directly quantifies the detector effect on the hemisphere definition without changing the observable definition. Replaces the previous "hemisphere assignment" systematic (see Section 7.3) | 1-3% (largest for particles near the hemisphere boundary) |
| **Neutral thrust axis** | Observable definition | **Phase 2 investigation required:** Determine whether the archived data's pre-computed thrust (Thrust, TTheta, TPhi branches) was computed from energy-flow objects (charged + neutral) or from charged tracks only. The data files contain multiple thrust variants (Thrust, ThrustCharged, ThrustCorrected). If the standard Thrust uses energy-flow, the detector-level thrust axis includes neutrals while the Lund plane uses only charged tracks. This inconsistency must be resolved: either use the charged-only thrust axis at detector level (recompute if necessary), or include the neutral-thrust vs charged-thrust difference as a systematic. Phase 2 will determine the archived data thrust source and handle consistently | To be determined |
| **Hardness variable** | Observable definition | Difference between p_T-ordered and energy-ordered primary chains (see Section 2.2, [D13]) | To be determined in Phase 2; cross-check, not a systematic |
| **Jet definition** | Observable definition | Compare Approach A (thrust hemispheres) vs Approach C (kT jets). The difference characterizes sensitivity to jet definition | Cross-check, not a systematic (different observable definitions) |

### 7.3 Reclassification: Hemisphere Assignment

The previous strategy listed "Hemisphere assignment: charged+neutral vs charged-only thrust axis" as a systematic uncertainty. Per conventions/unfolding.md (lines 136-150, "Observable redefinition is not a systematic"), changing the thrust axis from charged-only to energy-flow changes WHAT is measured -- it is a different observable with a different particle-level definition. **This is reclassified as a cross-check**, not a systematic. The detector-level systematic on hemisphere assignment is captured by the new "Thrust-axis resolution" systematic (smear momenta, measure migration), which varies the detector response while keeping the particle-level definition fixed.

### 7.4 Expected Dominant Systematics

Based on the reference analyses (see Section 8):

1. **MC model dependence** will likely dominate, especially in the low-k_T (non-perturbative) region. ATLAS reports 5-30% model dependence in their Lund plane measurement. For e+e- with charged particles only, the effect is expected to be somewhat smaller due to the simpler event topology, but still dominant.
2. **Heavy flavour composition** will be important in the collinear region where the b-quark dead-cone effect is largest.
3. **Tracking efficiency** will be the leading detector-related systematic.
4. **Track selection cuts** will affect the edges of the Lund plane (low p, large angle).

---

## 8. Reference Analysis Table

### 8.1 ATLAS Lund Jet Plane (Phys. Rev. Lett. 124 (2020) 222002)

| Aspect | Detail |
|--------|--------|
| Observable | Primary Lund jet plane density rho(ln 1/Delta_R, ln k_T) in pp at 13 TeV |
| Jet definition | Anti-kT R=0.4 jets, pT > 675 GeV |
| Declustering | C/A reclustering, primary Lund plane |
| Hardness variable | p_T w.r.t. beam (standard Dreyer/Salam/Soyez definition) |
| Correction | Bayesian iterative unfolding |
| Validation | Closure test, stress test with reweighted truth |
| Systematics | Jet energy scale (~2-5%), jet energy resolution (~1-3%), tracking efficiency (~1%), MC model (PYTHIA vs HERWIG, 5-30%), unfolding (1-5%) |
| MC generators | PYTHIA 8 Monash, HERWIG 7 |
| Dominant systematic | MC generator model dependence |
| Binning | Non-uniform |

### 8.2 CMS Lund Jet Plane (JHEP 05 (2024) 116, arXiv:2312.16343)

| Aspect | Detail |
|--------|--------|
| Observable | Primary Lund jet plane density in pp at 13 TeV, charged particles |
| Jet definition | Anti-kT R=0.4 and R=0.8 jets, pT > 700 GeV, |y| < 1.7 |
| Declustering | C/A reclustering, primary Lund plane |
| Hardness variable | p_T w.r.t. beam |
| Correction | Iterative unfolding |
| Validation | Closure test, stress tests |
| Systematics | Tracking efficiency, MC model dependence, unfolding regularization |
| MC generators | PYTHIA 8, HERWIG 7 |
| Dominant systematic | MC model dependence |
| Binning | Non-uniform |
| HEPData | Available (record 146031) |

### 8.3 ALICE Lund Plane (JHEP 05 (2024) 116)

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
| Binning | Non-uniform |

### 8.4 ATLAS Lund Plane in Top/W Jets (arXiv:2407.10879, EPJC 2025)

| Aspect | Detail |
|--------|--------|
| Observable | Lund jet plane density in hadronic decays of top quarks and W bosons, pp at 13 TeV |
| Jet definition | Anti-kT R=1.0, pT > 350 GeV, charged particles |
| Declustering | C/A reclustering |
| Correction | Iterative unfolding |
| Key finding | W-boson jets (colour singlet -> qq) are the closest analog to e+e- Z -> qq. All MC predictions are incompatible with the W-jet measurement. This suggests the Lund plane is a sensitive discriminator of QCD radiation patterns |
| Relevance | The W -> qq Lund plane probes colour-singlet quark radiation, directly analogous to Z -> qq. Comparison of our Z-pole measurement with the ATLAS W-jet result (after accounting for energy scale and boost effects) tests universality of quark fragmentation |

### 8.5 LHCb Lund Plane for Light and Beauty Jets (Phys. Rev. D 112 (2025) 072015, arXiv:2505.23530)

| Aspect | Detail |
|--------|--------|
| Observable | Lund jet plane density for light-quark-enriched and b-quark jets, pp at 13 TeV |
| Jet definition | Anti-kT charged-particle jets |
| Key finding | First direct observation of the dead-cone effect in beauty-quark jets in the collinear region of the Lund plane |
| Relevance | Demonstrates that the Lund plane is sensitive to heavy flavour effects. Directly motivates our heavy flavour composition systematic (Section 7.2). At the Z pole with 22% bb-bar, the dead-cone effect will produce a measurable modification in the collinear region |

### 8.6 DELPHI Jet Splitting (inspire_1661966)

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

### 8.7 Method Parity Assessment

All four modern Lund plane measurements (ATLAS 2020, CMS 2024, ALICE 2024, LHCb 2025) used iterative Bayesian unfolding. LEP-era analyses (DELPHI, ALEPH) used bin-by-bin correction. For this measurement:

- **Co-primary: bin-by-bin correction AND IBU** -- acknowledging the modern consensus while leveraging the excellent ALEPH resolution.
- **The result will be presented using whichever method passes stress tests better.** If both pass equivalently, the IBU result will be primary (matching modern practice), with bin-by-bin as the cross-check.
- **Method parity is satisfied:** both approaches are implemented, and any significant disagreement will be investigated and resolved.

---

## 9. Flagship Figures

The following ~6 flagship figures will represent the measurement:

1. **F1: The primary Lund jet plane density (2D coloured density plot).** The central result: rho(ln 1/Delta_theta, ln k_T) as a 2D histogram with colour scale. This is the signature plot of the analysis.

2. **F2: Lund plane density compared to PYTHIA 8 and HERWIG 7.** Three panels (or 2D ratio plots): data, PYTHIA 8, HERWIG 7 predictions. Shows model agreement/disagreement across the plane.

3. **F3: Projections onto ln k_T (1D spectrum).** The Lund plane integrated over ln 1/Delta_theta, yielding the k_T spectrum of primary emissions. Includes data points with systematic uncertainty bands, MC generator overlays, and the LO analytical prediction rho_LO = 2 * alpha_s(k_T) * C_F / pi (corrected for charged-particle fraction, see Section 10.2) as a reference line. This is the most direct comparison with the DELPHI splitting probability result.

4. **F4: Projections onto ln 1/Delta_theta (1D spectrum).** The Lund plane integrated over ln k_T, yielding the angular spectrum of primary emissions.

5. **F5: Correction factor map (2D).** The bin-by-bin correction factor C(i,j) displayed as a 2D coloured plot. Illustrates the detector response and validates the near-diagonal structure assumed by bin-by-bin correction.

6. **F6: Systematic uncertainty breakdown.** A stacked/overlaid display of the leading systematic contributions (MC model, heavy flavour, tracking, selection) as a function of ln k_T (integrated over angle), showing which regions are statistics-limited vs systematics-limited.

**Additional figures (not flagship, but required):**
- Response matrix R(i,j -> k,l) for the IBU method (2D visualization, separate from F5)
- Data/MC comparison of input kinematic variables (p, theta, N_ch, thrust)
- Closure test result (corrected MC reco vs MC truth)
- Stress test results (recovery of tilted truth)
- Alternative correction method comparison (bin-by-bin vs IBU)
- Year-by-year stability check
- Approach A vs Approach C comparison
- Lund plane construction methodology diagram: schematic showing the declustering procedure, coordinate definition, and relationship between the clustering tree and the Lund plane points

---

## 10. Theory Comparisons

### 10.1 MC Generator Predictions

Three modern MC generators will be run at particle level (e+e- -> hadrons at sqrt(s) = 91.2 GeV) to produce theory predictions:

1. **PYTHIA 8.3 Monash tune** -- default string fragmentation
2. **HERWIG 7.3** -- angular-ordered shower + cluster hadronization
3. **Sherpa 2.2** [D14] -- dipole shower + Lund string. Feasibility to be assessed in Phase 2 (see Section 3.3)

These will be run at generator level only (no detector simulation) with the same particle-level cuts as the measurement definition. Each generator will produce O(10^6) events at the Z pole (estimated runtime ~30 min per generator).

### 10.2 Analytical Predictions

The Lund plane density in the perturbative region has a known analytical form at leading order (Dreyer, Salam, Soyez, JHEP 12 (2018) 064, Eq. 2.5-2.6). In the soft-collinear limit (Delta << 1, z_bar << 1), the z_bar-dependent factor in Eq. 2.5 evaluates to 2 (from the integral of the splitting function p_{gq}(z) = (1+(1-z)^2)/z, which gives a factor 2 in the z -> 0 limit), yielding:

**rho_LO = 2 * alpha_s(k_T) * C_F / pi** (Eq. 2.6)

For quark-initiated jets (as at the Z pole), C_F = 4/3. With alpha_s(M_Z) ~ 0.118 (to be fetched from PDG at Phase 4), the expected all-particle density is:

rho_LO ~ 2 * 0.118 * (4/3) / pi ~ 0.100

**Charged-particle correction:** The LO formula describes all-particle emissions (quarks and gluons fragmenting into all hadron species). The measurement uses only charged particles. The charged-particle fraction of hadrons is approximately 2/3 (from isospin: pi+, pi-, pi0 are produced in roughly equal numbers, and pi0 -> gamma gamma is neutral). The charged-particle Lund plane density is therefore expected to be:

rho_LO,charged ~ 0.67 * rho_LO ~ 0.067

This is an approximate correction; the actual charged fraction depends on the fragmentation model and the k_T scale. The LO overlay on F3 will show both the all-particle and charged-particle-corrected predictions.

**Running of alpha_s:** Across the Lund plane, k_T ranges from ~0.05 GeV to ~55 GeV. The running of alpha_s from alpha_s(1 GeV) ~ 0.5 to alpha_s(50 GeV) ~ 0.13 produces a visible tilt that probes the QCD beta function.

### 10.3 NLL Predictions

Lifson, Salam, and Soyez (JHEP 10 (2020) 170, arXiv:2007.06578) provide an all-order single-logarithmic calculation of the primary Lund plane density, including running coupling, collinear splitting function effects, and soft large-angle logarithms. Their calculation achieves 5-7% precision at high k_T and ~20% at the lower edge of the perturbative region.

The published numerical predictions are for pp jets. For quark-initiated jets in e+e- (where the quark colour factor C_F = 4/3 is unambiguous and there are no ISR/MPI contaminations), the NLL predictions should be directly applicable in the perturbative region after appropriate coordinate mapping.

**Commitment:** Investigate whether numerical NLL predictions for e+e- quark jets are available (contact authors or check supplementary material). If available, overlay on the measurement. If not, compare the shape of the k_T dependence at fixed Delta with the NLL prediction (the running-coupling slope is a theory-data comparison that does not require absolute normalization).

---

## 11. Open Issues and Constraints

### 11.1 Constraints [A]

- **[A1]** Particle-level definition uses p > 200 MeV/c threshold, set by ALEPH TPC resolution. Cannot lower without degraded momentum measurement.
- **[A2]** MC is PYTHIA 6.1 only (single generator for detector-level correction). No alternative fully simulated MC is available. This means MC model dependence for the correction factors cannot be directly evaluated by comparing two generators at detector level -- it must be assessed via reweighting or truth-level comparisons.
- **[A3]** MC statistics (~772k events) are ~25% of data statistics. This limits the precision of correction factors in sparsely populated Lund plane bins.

### 11.2 Limitations [L]

- **[L1]** Only charged particles are measured. The neutral-particle Lund plane would require calorimeter-based measurements with worse resolution. This is a measurement choice, not a limitation, but the result is a charged-particle Lund plane, not an all-particle one.
- **[L2]** The PYTHIA 6.1 MC may not accurately model all features of the Lund plane, particularly in the non-perturbative region. Standalone PYTHIA 8 and HERWIG 7 at truth level partially address this via model comparison, but the correction itself depends on PYTHIA 6.1.

### 11.3 Decisions [D]

- **[D1]** Cambridge/Aachen algorithm for declustering (angular-ordered; required for Lund plane definition)
- **[D2]** Primary declustering chain (follow the harder subjet)
- **[D3]** Binning: 10x10 in (ln 1/Delta_theta, ln k_T), range [0,5] x [-3,4]. To be refined in Phase 2 (see binning deliverables in Section 2.2).
- **[D4]** Use pwflag = 0 particles only (charged tracks). Cross-check with pwflag = {0,1,2}.
- **[D5]** Thrust > 0.7 cut for well-defined hemispheres. Optimize in Phase 2.
- **[D6]** No MVA for event selection (justified: no signal/background separation needed, one-dimensional event quality, negligible backgrounds).
- **[D7]** Second selection approach: exclusive kT-jet-based (Approach C) instead of MVA.
- **[D8]** Bin-by-bin correction as co-primary method. Justified by ALEPH resolution and LEP precedent.
- **[D9]** IBU as co-primary method. Matching modern ATLAS/CMS/ALICE/LHCb methodology.
- **[D10]** ISR/FSR treatment: include all final-state charged particles after FSR; ISR photons excluded.
- **[D11]** Covariance matrix delivery: statistical (bootstrap N >= 500) + systematic + total. Machine-readable format.
- **[D12]** Response matrix matching: bin-level population matching (not object-level 1:1 matching) for variable-multiplicity Lund declusterings.
- **[D13]** Hardness variable: p_T w.r.t. beam (primary), energy ordering (systematic variation). Verified against Dreyer/Salam/Soyez 2018.
- **[D14]** Sherpa: assess feasibility in Phase 2. If infeasible, document why and proceed with PYTHIA 8 + HERWIG 7 only.

---

## 12. Validation

### 12.1 Validation Plan

| Test | Description | Pass Criterion |
|------|------------|----------------|
| Closure test | Apply correction factors to MC reco, compare with MC gen truth | chi2/ndf ~ 1, p-value > 0.05 |
| Split-sample closure | Derive correction from MC half A, apply to MC half B | chi2/ndf ~ 1, p-value > 0.05 |
| Stress test | Reweight MC truth by tilts of 5%, 10%, 20%, 50% independently in ln(1/Delta_theta), ln(k_T), and 2D correlated. Functional form: w(x) = 1 + epsilon*(x - x_mean)/(x_max - x_mean). Correct reweighted reco, compare with reweighted truth | Recovery within statistical + systematic uncertainty for tilts up to 20% |
| Alternative method | Compare bin-by-bin vs IBU | Agreement within 2-sigma per bin, or disagreement investigated |
| Data/MC agreement | Compare data and MC at reco level for all kinematic inputs | No bins with data/MC > 3 sigma for key variables |
| Year-by-year stability | Compute Lund plane for each data year separately | Consistent within statistical uncertainties |
| Approach A vs C | Compare thrust hemispheres vs kT jets | Characterize systematic from jet definition |
| Covariance PSD | Check all eigenvalues >= 0, condition number < 10^10 | Pass/fail |
| MC reweighting diagnostic | Verify reweighting factors < 3x; check reco-level migration | Factors < 3x in all bins, or bins flagged |

### 12.2 Comparison Targets

The primary comparison targets are the modern MC generators at particle level, the LO analytical prediction (rho = 2*alpha_s*C_F/pi), and the NLL prediction (Lifson/Salam/Soyez 2020) if numerical values are available. The 1D k_T projection can be compared with the DELPHI jet splitting probability (inspire_1661966), after accounting for the different jet definition (Durham vs hemisphere C/A declustering). The general structure (flat perturbative plateau, non-perturbative rise) can be compared with ATLAS and CMS pp Lund plane results in the collinear region.

---

## 13. Code Reference

Scripts written during Phase 1 (data exploration):
- `phase1_strategy/src/check_data_structure.py` -- Reads one data and one MC file, prints tree/branch structure
- `phase1_strategy/src/count_events.py` -- Counts events in all data and MC files
- `phase1_strategy/src/check_branches.py` -- Full branch inventory, pwflag distributions, event shape variables

All scripts run via `pixi run py <script>`.

---

## 14. Retrieval Log

### 14.1 LEP Corpus Queries (Phase 1)
1. `search_lep_corpus("Lund jet plane e+e- measurement")` -- Found DELPHI splitting probability
2. `search_lep_corpus("ALEPH hadronic event selection track cuts")` -- Found cds_2876991, inspire_322679
3. `search_lep_corpus("subjet multiplicity ALEPH Durham")` -- Found cds_388806, inspire_457159
4. `search_lep_corpus("ALEPH EEC systematic uncertainties")` -- Found inspire_322679
5. `search_lep_corpus("jet structure correction factors LEP")` -- Found DELPHI, ALEPH methods
6. `search_lep_corpus("ALEPH tracking efficiency TPC resolution")` -- Found detector performance info

### 14.2 Paper Drilldowns
- `get_paper("cds_2876991")` -- ALEPH QGP search with same archived data
- `get_paper("inspire_1661966")` -- DELPHI jet splitting probability
- `get_paper("cds_388806")` -- ALEPH quark/gluon subjet multiplicity

### 14.3 Web Search (Fixer, Peter, 2026-03-25)
- **Dreyer/Salam/Soyez 2018:** Retrieved arXiv:1807.04758, verified Eq. 2.1 (p_T ordering), Eq. 2.6 (rho = 2*alpha_s*C_F/pi). Confirmed hardness variable is p_T w.r.t. beam, not energy.
- **Lifson/Salam/Soyez 2020:** Retrieved arXiv:2007.06578. NLL Lund plane density calculation, 5-7% precision at high k_T.
- **CMS Lund plane 2024:** JHEP 05 (2024) 116, arXiv:2312.16343. Charged-particle Lund plane in pp at 13 TeV. HEPData available.
- **ATLAS top/W Lund plane 2024:** arXiv:2407.10879, EPJC 2025. First Lund plane in top/W jets. W-jet = colour-singlet qq, closest analog to Z -> qq.
- **LHCb Lund plane 2025:** Phys. Rev. D 112 (2025) 072015, arXiv:2505.23530. First dead-cone observation in Lund plane for b-quark jets.
