# Physics Review: Phase 1 Strategy -- Primary Lund Jet Plane Density

**Reviewer:** Albert (PI / physics referee)
**Artifact:** `STRATEGY_fabiola_2026-03-25_16-50.md`
**Date:** 2026-03-25

---

## Overall Assessment

This is a well-structured strategy for a genuinely novel measurement -- the
first Lund jet plane density in e+e- collisions.  The physics motivation is
sound, the data inventory is thorough, and the systematic plan is more
complete than most first drafts.  However, there are several issues ranging
from an incorrect formula for the leading-order density to an incomplete
reference analysis table that must be resolved before proceeding.

**Verdict: ITERATE** -- resolve the (A) findings before advancing.

---

## Findings

### F1. (A) Leading-order density formula is wrong by a factor of 2

**Strategy Section 10.2** states:

> rho_LO = (alpha_s * C_F) / pi ~ 0.050

The foundational paper (Dreyer, Salam, Soyez, JHEP 12 (2018) 064, Eq. 2.6)
gives the leading-order density in the limit Delta << 1 and z_bar << 1 as:

> rho ~ 2 * alpha_s(k_t) * C_F / pi

The factor of 2 arises from the z-dependent splitting function
p_qq(z) = (1 + (1-z)^2)/z evaluated at small z_bar, where the symmetry
of the splitting function contributes a factor of 2.  The strategy's
numerical estimate should therefore be ~0.100, not ~0.050.

This is a blocking error because the leading-order benchmark is used to
validate the measurement in the perturbative region.  A factor-of-2
discrepancy between data and the "expected" LO value would be incorrectly
flagged as a problem, or worse, the analysis would be tuned to match a
wrong target.

**Action required:** Correct the LO formula to include the factor of 2.
Propagate this to the numerical estimate.

---

### F2. (A) "Harder subjet" definition disagrees with the foundational paper

**Strategy Section 5.2** defines the harder subjet as:

> "the one with larger energy E (standard choice for e+e- Lund plane,
> where energy is the natural hardness variable; this differs from pp
> where pT is used)"

The foundational paper (Dreyer, Salam, Soyez, Section 2.1, step 1) defines
the labeling `p_a > p_b` such that `p_{ta} > p_{tb}`, where `p_t` is the
transverse momentum **with respect to the colliding beams**.  The primary
chain follows the harder branch `p_a` at each step.  In pp collisions, beam-
axis pT is the standard variable, and ATLAS/ALICE/CMS all follow this
convention.

For e+e- collisions, there is no published Lund plane measurement to set
precedent, so the strategy must make a deliberate, documented choice.
Using energy rather than pT is a defensible alternative for e+e- (the
thrust axis, not the beam, is the natural reference direction, and in the
collinear limit E and pT coincide).  **However, the strategy claims this
is the "standard choice" without citation, which is misleading -- there is
no standard for e+e- Lund planes because none has been measured.**

More importantly, if the measurement uses energy ordering while the
theoretical predictions (Eq. 2.5-2.6 of Dreyer et al.) and all pp
measurements use pT ordering, the comparison is not apples-to-apples.  In
the wide-angle region (small ln 1/Delta_theta), energy ordering and pT
ordering can assign different particles to the primary chain, producing
measurably different densities.

**Action required:** (1) Remove the false claim of "standard choice."
(2) Explicitly discuss the pT-vs-energy ordering ambiguity.  (3) Commit
to one as primary and implement the other as a cross-check [D].
(4) Quantify the expected difference in Phase 2 (compare the two orderings
at MC truth level).  I would recommend pT ordering as the primary to
maximize comparability with the theoretical framework and the pp
measurements, with energy ordering as the systematic variation.

---

### F3. (A) Coordinate definitions are inconsistent with the foundational paper

The strategy defines (Section 2.2):

> Delta_theta = arccos(p_hat_1 . p_hat_2)
> k_T = |p_2| * sin(Delta_theta)

The foundational paper (Eq. 2.1a) defines:

> Delta = Delta_{ab}  (rapidity-azimuth distance)
> k_t = p_{tb} * Delta_{ab}

These are **different quantities**.  For the pp case, Delta_R is the
standard rapidity-azimuth distance.  For e+e-, the natural adaptation
uses the 3D opening angle theta (as the strategy proposes), but the
k_T definition then becomes `k_t = p_2 * sin(theta)`, not
`k_t = p_2 * Delta_theta`.  For small angles, `sin(theta) ~ theta`,
so both agree in the collinear limit.  But at wide angles (which are
kinematically accessible for Z-pole hemispheres), `sin(theta)` and
`theta` differ significantly -- for theta = 1 radian, the difference
is ~16%.

The strategy's definition `k_T = |p_2| * sin(Delta_theta)` is actually
the more physically motivated choice for e+e- (it is the true transverse
momentum component), and it agrees with the Dreyer et al. definition in
the collinear limit.  But the strategy must:

1. Acknowledge that this is an **adaptation** of the pp definition to
   e+e-, not a direct transcription.
2. State explicitly that `sin(theta)` is used rather than `theta` in the
   k_T definition.
3. Note that comparisons with pp measurements (ATLAS, ALICE, CMS) are
   only strictly valid in the collinear region (large ln 1/Delta_theta).

This matters because the whole point of comparing e+e- with pp is to test
universality, and the coordinate mapping must be transparent.

**Action required:** Rewrite Section 2.2 and 5.3 to clearly define the
e+e- coordinate adaptation, distinguish it from the pp convention, and
document the regime of validity for cross-collider comparisons.

---

### F4. (B) Reference analysis table is incomplete -- misses CMS (2024), ATLAS top (2024), LHCb (2025)

The strategy references only ATLAS (2020), ALICE (2024), and DELPHI.
Since the strategy was written, several additional Lund plane measurements
have been published:

- **CMS**, JHEP 05 (2024) 116 -- primary Lund plane density in pp at
  13 TeV, AK8 jets with pT > 700 GeV, charged-particle tracks.  This is
  directly comparable to ATLAS and uses iterative Bayesian unfolding.
- **ATLAS**, arXiv:2407.10879 (2024) -- Lund plane in top quark and W
  boson hadronic decays.  This is particularly relevant because it
  measures the Lund plane for color-singlet initiated jets (W -> qq),
  which is closer to the e+e- environment than inclusive QCD jets.
- **LHCb**, Phys. Rev. D (2025), arXiv:2505.23530 -- Lund plane for
  light- and beauty-quark jets, first observation of dead-cone effect
  in beauty jets via the Lund plane.

The ATLAS top/W measurement is especially relevant: it provides the
closest existing analog to the e+e- measurement (color-singlet decay
to quarks).  The LHCb measurement demonstrates that the Lund plane can
resolve quark-flavor effects (dead cone), which is relevant to the
b-quark contamination systematic at the Z pole.

**Action required:** Update the reference table to include CMS (2024),
ATLAS top (2024), and LHCb (2025).  Extract their systematic programs.
Discuss implications of the ATLAS top result for the e+e- measurement.

---

### F5. (B) Bin-by-bin correction as primary method is questionable given the state of the art

The strategy designates bin-by-bin correction as the primary method [D8]
and IBU as a cross-check [D9].  The justification cites:

1. LEP-era precedent (ALEPH subjet, DELPHI splitting)
2. Excellent ALEPH resolution
3. High-dimensional response matrix concerns

Points 1 and 3 are weak.  LEP-era precedent reflects the tools available
in the 1990s, not what is best practice.  The 100x100 response matrix
concern is overstated -- all four modern Lund plane measurements (ATLAS,
ALICE, CMS, LHCb) successfully perform 2D iterative unfolding, and the
ALICE measurement with similar or lower statistics than the available
ALEPH MC succeeded with IBU.

Point 2 (excellent resolution) is the only substantive argument.  If the
response matrix is truly near-diagonal, then bin-by-bin and IBU should
agree to high precision, making the choice immaterial.  But if they
disagree, **the IBU result is more trustworthy** because it accounts for
off-diagonal migration.

The current framing puts the burden of proof on the wrong method:
disagreement between bin-by-bin and IBU would be attributed to "model
bias" in the bin-by-bin method, yet the strategy calls bin-by-bin
"primary."  A reviewer of the eventual paper would ask: "If you know IBU
is more correct, why isn't it your primary result?"

**Action required:** Either (a) promote IBU to the primary method with
bin-by-bin as the cross-check (matching all modern measurements), or
(b) commit to presenting both on equal footing and adopting whichever
shows better closure/stress test performance.  The current asymmetric
framing (bin-by-bin primary, IBU cross-check) is not well motivated
for a 2026 measurement.

---

### F6. (B) Momentum resolution value appears incorrect

**Strategy Section 6.1** states:

> sigma_p/p^2 ~ 0.6 x 10^-3 (GeV/c)^-1

The ALEPH EEC thesis (inspire_322679, Section "The ALEPH detector")
quotes the TPC momentum resolution as:

> Delta p/p^2 = 1.2 x 10^-3 (GeV/c)^-1

The value 0.6 x 10^-3 appears to be the combined TPC+ITC+VDET resolution
from later ALEPH papers, which benefits from the silicon vertex detector
and inner tracking chamber providing additional lever arm.  However, for
the archived open data, it is not guaranteed that the ITC and VDET hits
are included in all track fits (this depends on the reconstruction version
used to produce the archived ntuples).

Using the wrong resolution by a factor of 2 could underestimate the
momentum smearing systematic and the off-diagonal migration in the
response matrix.

**Action required:** (1) Verify which tracking detectors contribute to the
archived track reconstruction (check whether ITC/VDET hits are used).
(2) Cite the correct resolution for the relevant tracking configuration.
(3) Use the verified resolution for the momentum smearing systematic.

---

### F7. (B) No b-quark systematic considered

At the Z pole, approximately 22% of hadronic decays produce b-quark pairs.
B-hadrons have displaced decay vertices (c*tau ~ 500 um for B mesons), and
the b-quark Lund plane density differs from light-quark density due to:

1. The dead-cone effect (suppressed collinear radiation for massive quarks)
2. B-hadron decay products reconstructed as prompt tracks, contaminating
   the primary declustering chain
3. Different fragmentation hardness (b quarks carry larger fraction of
   hemisphere energy)

The LHCb measurement (2025) explicitly demonstrates that the Lund plane
has resolving power for b-quark vs. light-quark jets.  At the Z pole,
with 22% b-fraction, this is not a negligible effect.

The strategy lists no systematic for flavor composition.  The correction
factors from PYTHIA 6.1 implicitly include the Standard Model flavor mix,
but the sensitivity to the b-fraction should be evaluated.

**Action required:** Add a systematic for b-quark flavor composition.
Evaluate by reweighting the MC to vary the b-fraction (e.g., +/-2%
absolute, reflecting the precision of R_b measurements at LEP).
Alternatively, split the Lund plane by MC flavor tag and quantify the
b-quark contribution to each bin.

---

### F8. (B) Missing systematic for neutral-particle contamination

The strategy measures charged particles only but reconstructs the thrust
axis from charged tracks.  However, the archived ALEPH data may include
energy-flow objects (charged + neutral) for the thrust computation --
the corpus passage from cds_2876991 states "the event sphericity polar
angle [...] as determined by energy-flow objects."

If the thrust axis in the archived data is computed from energy-flow
objects but the Lund plane uses only charged tracks, there is a mismatch:
the hemisphere assignment depends on neutrals but the Lund plane does not.
This is a potential source of bias, especially for events with energetic
neutral pions carrying significant transverse momentum.

The strategy mentions "Compare thrust axis from charged+neutral (energy
flow) vs charged-only" under hemisphere assignment (Section 7.2), which
is good, but it should be elevated to a proper systematic with a
quantitative evaluation plan.

**Action required:** Clarify whether the pre-computed thrust in the
archived data uses all particles or charged-only.  If energy-flow, then
either (a) recompute thrust from charged tracks only for consistency, or
(b) include the thrust-definition mismatch as a systematic variation.

---

### F9. (B) The Lund plane density normalization needs the bin-width denominator

**Strategy Section 2.2** defines:

> rho(x, y) = (1 / N_jet) * d^2 n / (dx dy)

This is correct as a continuous density.  But in practice, the discrete
binned version must divide by the bin widths:

> rho(x_i, y_j) = (1 / N_jet) * N_splittings(i,j) / (Delta_x * Delta_y)

where Delta_x and Delta_y are the bin widths in ln(1/Delta_theta) and
ln(k_T/GeV) respectively.  With the proposed 10x10 binning, Delta_x = 0.5
and Delta_y = 0.7.  This is standard, but the strategy should state
the discrete formula explicitly to avoid ambiguity during implementation.
With non-uniform bin widths (which may arise from Phase 2 optimization),
getting this wrong would silently distort the density.

**Action required:** Write out the explicit discrete binned formula,
including bin widths.

---

### F10. (B) Stress test reweighting procedure is underspecified

**Strategy Section 12.1** proposes:

> "Reweight MC truth by tilts of 5%, 10%, 20%, 50%."

But it does not specify **what** is tilted.  A tilt in ln(k_T)?  In
ln(1/Delta_theta)?  A 2D tilt?  The direction and functional form of the
tilt matter because they test different failure modes.  A tilt in k_T
tests sensitivity to the k_T spectrum shape (which affects the correction
factors through MC model dependence), while a tilt in angle tests the
angular response.

The conventions/unfolding.md likely requires graded tilts in both
projection axes.  The strategy mentions "graded tilt functions" in both
Lund coordinates (Section 7.1) but the validation table (Section 12.1)
just says "tilts of 5%, 10%, 20%, 50%" without specifying the axis.

**Action required:** Specify that stress tests will apply tilts
independently in both Lund coordinates (ln k_T and ln 1/Delta_theta),
plus a 2D correlated tilt (e.g., along the diagonal).  State the
functional form (linear tilt, i.e., w(x) = 1 + epsilon * (x - x_mean)
or similar).

---

### F11. (C) The Thrust > 0.7 cut is aggressive and potentially biases the Lund plane

The strategy proposes Thrust > 0.7 [D5] to ensure "well-separated
hemispheres."  The typical thrust distribution at the Z pole peaks around
0.85-0.90, with a tail extending to ~0.6 for multi-jet events.  A cut at
0.7 removes roughly 5-10% of events.

The concern is that multi-jet events (T < 0.7) have different Lund plane
densities than dijet events (high T) -- they have more wide-angle hard
radiation.  Removing them biases the measurement toward a more
"perturbative-looking" Lund plane.  This is a physics choice, not a
quality requirement: the hemisphere definition is valid down to T ~ 0.5
(each hemisphere still contains well-defined particles).

At minimum, the systematic evaluation of varying the thrust cut from 0.6
to 0.8 (proposed in Section 7.2) must cover a range that includes "no
thrust cut" as a limiting case.  If the measurement is sensitive to the
thrust cut, the particle-level definition should include a truth-level
thrust requirement, making the measurement explicitly for "dijet-like
events" rather than "all hadronic Z decays."

**Action required (suggestion):** Consider presenting the measurement
both with and without the thrust cut (or with a very loose cut like
T > 0.55) as a sensitivity study.  If a thrust cut is retained, include
it in the particle-level definition.

---

### F12. (C) Flagship figure F5 description is misleading

The strategy describes F5 as the "Response matrix (2D)" but then says it
will display "the bin-by-bin correction factor C(i,j)."  The correction
factor is NOT the response matrix -- it is the ratio of truth to reco
bin populations.  The actual response matrix is the 100x100 migration
matrix used for IBU.  If the plot shows C(i,j), it should be labeled
"correction factors" not "response matrix."

For a Lund plane paper, the actual flagship should show the migration
matrix (or at least its diagonal purity/stability) to demonstrate that
off-diagonal migration is small, justifying the bin-by-bin approach.

**Action required (suggestion):** Rename F5 to "Bin-by-bin correction
factors."  Add a separate figure showing the response matrix purity
(fraction of events reconstructed in the same bin as generated) as a 2D
map.  This directly supports the correction method choice.

---

### F13. (C) Theory comparison could include NLL analytical predictions

Section 10.2 mentions that "Comparisons with analytical calculations
(Dreyer, Salam, Soyez) will be pursued if published numerical predictions
are available."  This is passive.  The Dreyer et al. paper provides the
LO formula explicitly, and NLL corrections have been computed (see
Lifson, Salam, Soyez, JHEP 10 (2020) 170 for the NLL Lund plane
density).  For e+e- at the Z pole with known center-of-mass energy, the
analytical predictions are among the cleanest available in QCD.

**Action required (suggestion):** Commit to overlaying the LO and (if
available) NLL analytical predictions on the corrected data in the
perturbative region.  This turns the measurement into a quantitative
test of perturbative QCD, not just a generator-tuning exercise.

---

## Summary Table

| ID | Severity | Section | Finding |
|----|----------|---------|---------|
| F1 | **(A)** | 10.2 | LO density formula wrong by factor 2 |
| F2 | **(A)** | 5.2, 2.2 | "Harder subjet" definition ambiguous, falsely claimed as standard |
| F3 | **(A)** | 2.2, 5.3 | Coordinate definitions not clearly distinguished from pp convention |
| F4 | **(B)** | 8 | Reference table misses CMS (2024), ATLAS top (2024), LHCb (2025) |
| F5 | **(B)** | 6.1, 6.2 | Bin-by-bin as primary method weakly motivated vs modern IBU |
| F6 | **(B)** | 6.1 | Momentum resolution value possibly wrong by factor 2 |
| F7 | **(B)** | 7.2 | No b-quark systematic (22% of Z decays) |
| F8 | **(B)** | 7.2 | Thrust axis neutral-particle contamination not addressed |
| F9 | **(B)** | 2.2 | Binned density formula with bin widths not explicitly stated |
| F10 | **(B)** | 12.1 | Stress test tilt axes and functional form unspecified |
| F11 | **(C)** | 4.1 | Thrust > 0.7 cut potentially biases Lund plane; consider looser cut |
| F12 | **(C)** | 9 | F5 labeled "response matrix" but shows correction factors |
| F13 | **(C)** | 10.2 | Analytical NLL predictions should be a commitment, not optional |

---

## Verdict

**ITERATE.**  Three Category A findings (F1, F2, F3) must be resolved.
Six Category B findings should be addressed to bring the strategy to the
standard expected for a first measurement.  The Category C items are
suggestions that would strengthen the analysis but do not block
advancement.

The strategy is fundamentally sound -- the measurement is well motivated,
the data are adequate, and the systematic plan is more complete than many
published analyses at this stage.  But the observable definition must be
nailed down precisely (F2, F3) and the LO benchmark must be correct (F1)
before any code is written.  These are not cosmetic issues; they affect
every downstream phase.
