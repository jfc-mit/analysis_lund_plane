# Phase 4a Critical Review: Inference -- Expected Results

**Reviewer:** Lena (critical + plot validator) | **Date:** 2026-03-26
**Artifact:** `INFERENCE_EXPECTED_felix_2026-03-25_21-35.md`
**Analysis:** lund_jet_plane | **Phase:** 4a (expected)

---

## Verdict: ITERATE

Three Category A findings and four Category B findings must be resolved
before Doc 4a can proceed.

---

## Category A Findings (must resolve -- blocks advancement)

### A-1. Split-sample closure test FAILS the convention gate (p < 0.05) with no remediation attempts

**Requirement:** conventions/unfolding.md Quality Gate 1 requires chi2
p-value > 0.05 for closure. The Phase 3 CLAUDE.md and the analysis-level
CLAUDE.md both require "at least 3 independent remediation approaches
BEFORE writing the artifact" when any validation test fails.

**Observation:** The split-sample closure yields chi2/ndf = 148.9/58 = 2.57
(p = 6.2e-10). The artifact acknowledges the failure but does NOT document
any remediation attempts. Instead, it offers a narrative explanation
("correction factor uncertainty inflates chi2") and suggests a
bootstrap-based closure test as a future remedy for Phase 4b.

**Diagnosis -- the explanation is partially valid but incomplete:**

1. The chi2 computation uses sigma^2 = N_truth_B (Poisson on the truth
   counts in half B). This does NOT account for the statistical uncertainty
   on the correction factors derived from half A. When correction factors
   have relative uncertainty ~sqrt(2/N_A), and these are multiplied by
   N_reco_B, the corrected counts carry additional variance from the
   correction factor noise. The pull std of 1.89 (wider than unit Gaussian)
   is consistent with underestimated uncertainties, not with a systematic
   bias in the method.

2. HOWEVER, the pull mean of -0.39 indicates a nonzero bias, not just
   variance inflation. If it were purely a variance issue, the pull mean
   should be near zero. A mean pull of -0.39 across 58 bins with std 1.89
   suggests a coherent ~1-2% low bias in the corrected result. This needs
   investigation.

3. The conventions require remediation ATTEMPTS, not successful remediations.
   Zero attempts were documented. This is a process failure.

**Required remediation attempts (any 3 of the following):**

(a) Recompute chi2 using the correct combined uncertainty:
    sigma^2_combined = N_truth_B + (delta_C/C)^2 * (N_reco_B * C_A)^2,
    where delta_C is the statistical uncertainty on the correction factor.
    This is the proper test statistic for split-sample closure with
    bin-by-bin correction. Report this chi2/ndf alongside the Poisson-only
    chi2/ndf.

(b) Perform bootstrap-based split-sample closure: bootstrap events within
    half A to get correction factor replicas, apply each to half B, compute
    the ensemble chi2 distribution. Compare observed chi2 to this
    distribution.

(c) Increase the split fraction: use 30/10 instead of 20/20 (more
    statistics for correction factors, test on fewer events). If the chi2
    improves substantially, the diagnosis of correction factor noise is
    confirmed.

(d) Examine which bins drive the chi2 excess. Are they boundary bins with
    large correction factors (C > 3)? If so, exclude those bins from the
    test and report the chi2 for the core region separately.

**Resolution:** Implement at least 3 of (a)-(d). If (a) alone brings the
p-value above 0.05, the gate is satisfied. If not, the remaining attempts
must be documented. A closure failure with documented, unsuccessful
remediation is a legitimate limitation. A closure failure with no attempts
is Category A.

---

### A-2. Stress tests for bin-by-bin are tautological -- convention requirement not met

**Requirement:** conventions/unfolding.md Quality Gate 2 requires stress
tests that characterize the method's "resolving power." The stress test
must apply the correction to a REWEIGHTED MC and recover the reweighted
truth.

**Observation:** All 12 bin-by-bin stress tests yield chi2 = 0 (p = 1.0).
The artifact correctly identifies this as an algebraic identity:
N_reco * w * C = N_genBefore * w = truth_reweighted.

This happens because the stress test reweights BOTH the reco and genBefore
histograms by the same bin-level weights, then applies the nominal
correction C = N_genBefore/N_reco. The weight cancels.

**Root cause in the code (01_validation.py, lines 893-899):**
```python
reco_rw = reco_flat * w_flat
truth_rw = genb_flat * w_flat
corrected_rw_bbb = reco_rw * corr_flat
# = reco_flat * w_flat * (genb_flat / reco_flat)
# = genb_flat * w_flat = truth_rw
```

The reweighting is applied at the histogram level, not at the event level.
For bin-by-bin correction, a meaningful stress test requires either:

(i) **Split-sample stress test:** Derive correction from nominal half A.
    Reweight half B reco at the event level (or bin level). Apply half-A
    correction to reweighted half-B reco. Compare to reweighted half-B
    genBefore truth. Because correction factors come from A and the
    reweighted distribution comes from B, the algebraic cancellation is
    broken.

(ii) **Event-level reweighting:** Assign per-event weights based on the
    gen-level Lund coordinates of that event, reprocess reco with weights,
    and apply nominal correction. This also breaks the cancellation because
    the per-event weights flow through the full analysis chain.

The artifact acknowledges the tautology ("This is a tautological result,
not a validation of resolving power") and argues that the split-sample
closure IS the meaningful stress test. While philosophically reasonable,
the conventions explicitly require stress tests with graded magnitudes
(5%, 10%, 20%, 50%). A chi2 = 0 stress test does not satisfy this gate.

**Required:** Implement split-sample stress tests: derive correction from
half A, apply graded tilts to half B, correct with half A factors, compare
to reweighted half B truth. Report chi2/ndf for each tilt magnitude. This
provides the resolving power characterization that the convention demands.

---

### A-3. IBU downscoping from co-primary [D9] not formally documented

**Requirement:** The strategy commits IBU as a co-primary method [D9]:
"Both bin-by-bin correction and iterative Bayesian unfolding are adopted as
co-primary methods." COMMITMENTS.md lists "Alternative correction method
comparison: bin-by-bin vs IBU as co-primary methods." Downscoping a binding
[D] commitment requires formal [D] treatment per methodology/12-downscoping.md.

**Observation:** The IBU method completely fails:
- Full-MC closure: chi2/ndf = 150,308/61 = 2,464
- Split-sample closure: chi2/ndf = 126,576/58 = 2,182
- All 12 stress tests: chi2/ndf ~ 2,000+
- IBU/Truth ratio is ~0.85-0.90 across the board (visible in
  felix_bbb_vs_ibu_kt.png and felix_bbb_vs_ibu_dtheta.png)

The artifact correctly identifies the fundamental limitation: individual
Lund splittings cannot be matched between reco and gen levels because the
C/A clustering tree has different structure at each level. The
diagonal-dominant response matrix built from aggregate bin populations
does not capture true per-splitting migration.

This is a legitimate physics limitation, well-documented in the literature
(ATLAS and CMS both use bin-by-bin as primary for the Lund plane). HOWEVER:

1. The artifact does not contain a formal [D] downscoping label for [D9].
   It informally demotes IBU to "cross-check" status without the required
   downscoping documentation.

2. COMMITMENTS.md still shows [D9] as `[ ]` (not addressed), not `[D]`
   (formally downscoped).

3. The artifact does not document whether 3 remediation attempts were
   made for the IBU failure. The conventions require "at least 3
   independent remediation approaches BEFORE accepting as a limitation."
   Possible attempts: vary number of iterations (done -- line 809-822 of
   01_validation.py), try the hemisphere-level response matrix instead
   of the aggregate diagonal-dominant one (the code builds both but
   discards the hemisphere-level one at line 583), try regularization.

**Required:**
- Formally downscope [D9] with documentation: what was committed, why it
  cannot be delivered, what literature supports the limitation, what
  remediation was attempted.
- Update COMMITMENTS.md: change IBU from `[ ]` to `[D]` with justification.
- Document at least 3 remediation attempts for the IBU failure. The code
  already tries iteration optimization. Try at least 2 more: (i) the
  hemisphere-level response matrix that was built but discarded, (ii)
  Tikhonov or other regularization.
- The unfolding method systematic (BBB vs IBU difference) should be
  flagged as an overestimate given that IBU is known to be biased. Consider
  whether including a systematically biased method's output as a
  "systematic uncertainty" inflates the uncertainty budget.

---

## Category B Findings (must fix before PASS)

### B-1. Covariance matrix is analytical Poisson, not bootstrap -- contradicts artifact and conventions

**Artifact Section 5.1 states:** "Analytical Poisson propagation through
the bin-by-bin correction: sigma^2(rho_i) = C_i^2 * N_reco_i / ..."
and "The statistical covariance is diagonal."

**BUT the code (03_bootstrap_covariance.py) DOES implement a bootstrap
with N=500 event-level replicas.** The bootstrap resamples events with
replacement, recomputes reco histograms, applies the nominal correction
factors, and computes the sample covariance.

The contradiction: the artifact text says "analytical Poisson" and
"diagonal," but the code implements a proper bootstrap. Reading the
covariance JSON confirms the stat_covariance is populated with zeros in
the first row (all unpopulated bins), which is consistent with both
methods since row 0 corresponds to the first bin row which is largely
unpopulated.

**Issue:** The bootstrap code (line 238) applies the same `correction_flat`
to every replica: `corrected_rep = reco_rep * correction_flat`. This means
the correction factors are NOT resampled -- only the reco counts are
bootstrapped. This misses the correlation between bins sharing the same
denominator in the correction factor and underestimates the statistical
uncertainty from the correction procedure itself.

Conventions/unfolding.md states: "resample events, recompute the full
correction chain for each replica." The code does NOT recompute the
correction chain -- it resamples reco and applies fixed corrections.

**Required:** Either (a) implement proper bootstrap that resamples
BOTH reco and genBefore events and recomputes correction factors per
replica, or (b) clearly document this as an approximation and quantify
its impact. The artifact text must match what the code actually does.

### B-2. Systematic evaluation on 10-file subset not documented as approximation

**Observation:** The artifact states (Section 4, header): "All committed
systematic sources evaluated on MC pseudo-data (10-file MC subset,
scaled)." And in Section 11, item 3: "Systematic evaluation on 10/40 MC
files... should be confirmed on the full sample in Phase 4b/4c."

Conventions/unfolding.md: "The covariance must be computed on the full
dataset. Scaling a covariance from a subset by N/n is approximate."

**Issue:** Using 10/40 files means only 25% of MC statistics. Systematic
shifts that are dominated by statistical noise in the variation (e.g.,
tracking efficiency drop, momentum smearing) may be inflated or
underestimated. The code (02_systematics.py) processes all 40 MC files
for each variation (line 397: `mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))`),
which contradicts the artifact's claim of 10-file subset.

**Required:** Clarify: does the code actually use 10 or 40 files? If 40,
fix the artifact text. If 10, document the approximation with a
quantitative estimate of the scaling uncertainty.

### B-3. Two committed systematic sources not evaluated: E_ch_min and ntpc

**COMMITMENTS.md lists:**
- "Track selection cuts: vary p threshold (150-250 MeV/c), |d0| (1.5-2.5 cm),
  ntpc (3-5)"
- "Event selection cuts: vary thrust cut (0.6-0.8), N_ch_min (4-6),
  E_ch_min (12-18 GeV)"

**Evaluated:**
- p threshold: YES (150-250 MeV/c)
- d0 cut: YES (1.5-2.5 cm)
- ntpc: NOT evaluated ("Branch not accessible in archived data")
- Thrust cut: YES (0.6-0.8)
- N_ch_min: YES (4-6)
- E_ch_min: NOT evaluated ("Deferred to Phase 4b")

The ntpc issue was identified in Phase 3 review (finding B-2). This is a
legitimate data limitation. However, the E_ch_min deferral is not justified
-- the `passesAll` flag encodes E_ch > 15 GeV, but the variation (12-18 GeV)
can be implemented by recomputing the charged energy sum from the track
arrays and applying the varied cut directly, bypassing `passesAll`. This
was not attempted.

**Required:** Either (a) implement the E_ch_min variation (compute sum of
track momenta per event, apply 12 and 18 GeV thresholds), or (b)
formally document why this is infeasible with [D] label and update
COMMITMENTS.md.

### B-4. Unfolding method systematic is problematic given IBU failure

**Observation:** The systematic breakdown figure (felix_syst_breakdown.png)
shows "unfolding method" as the DOMINANT systematic by far -- it accounts
for the vast majority of the total systematic uncertainty, particularly
at high ln(k_T) where it reaches ~30% relative shift (visible in
felix_syst_impact_kt.png) and at high ln(1/Delta_theta) where it reaches
~55% (felix_syst_impact_dtheta.png).

**Problem:** The IBU method is known to be biased (chi2/ndf = 2,464 on
full MC). Including the difference between a correct method (BBB) and a
broken method (IBU) as a "systematic uncertainty" does not quantify a
genuine uncertainty on the measurement -- it quantifies how broken the IBU
is. This inflates the systematic uncertainty budget by a factor of ~3-5x
compared to what the genuine detector/model uncertainties would be.

This is directly addressed in the conventions (known pitfall: "Double-
counting model dependence" and the general principle that systematics
must be propagated, not assigned). Including a method that fails all
validation tests as a systematic source is equivalent to assigning an
arbitrary systematic.

**Required:** Remove IBU-vs-BBB from the systematic budget. The IBU
comparison is a cross-check that confirms BBB is the correct primary
method, not a systematic uncertainty source. The unfolding method
systematic should be evaluated differently -- e.g., varying the
correction factors within their statistical uncertainty (bootstrap
replicas), or comparing correction factors from 30/10 and 10/30 splits.
This is closely related to the MC model dependence systematic, which
already captures the sensitivity to the correction procedure.

---

## Category C Findings (suggestions -- apply before commit)

### C-1. Experiment label formatting on 2D plots

The experiment label on 2D colourmap figures (felix_lund_plane_corrected.png,
felix_correction_factor_map.png, felix_diagonal_fraction.png) shows
"ALEPH Open Simulation" but the text overlaps with the sqrt(s) label,
making it partially illegible. Increase the horizontal spacing or place
the sqrt(s) label on a separate line.

### C-2. Pull distribution plot missing experiment label

The closure pulls figure (felix_closure_pulls.png) has no experiment
label (ALEPH Open Simulation / sqrt(s)). All figures require the
experiment label per plotting conventions.

### C-3. Stress test figures show only BBB, not IBU

The stress test figures (felix_stress_ln_kt.png, etc.) show only the
bin-by-bin chi2/ndf vs epsilon. Since IBU is still part of the analysis
(as a cross-check), the IBU results should be shown on the same plot (on
a different y-axis scale or as an inset) to illustrate the method
comparison visually.

### C-4. Correlation matrix should mask unpopulated bins

The correlation matrix (felix_correlation_matrix.png) shows the full
100x100 matrix with obvious block structure from unpopulated bins
(appearing as dark red diagonal blocks with zero off-diagonal). The plot
would be more informative if restricted to the 58 populated bins.

### C-5. Uncertainty summary plot missing systematic-only line

The uncertainty summary (felix_uncertainty_summary.png) shows only
"Statistical" and "Total." Adding a "Systematic" line would make the
relative contributions immediately visible.

### C-6. Artifact references .pdf figures but only .png exist

The artifact markdown references figures as `.pdf` files
(e.g., `figures/felix_lund_plane_corrected.pdf`), but the actual
figures on disk are `.png`. This should be corrected. Per plotting
conventions, both PDF and PNG should be saved.

---

## Decision Label [D] Compliance Check

| Label | Commitment | Status | Assessment |
|-------|-----------|--------|------------|
| [D1] | C/A algorithm | Implemented | OK -- code uses ee_genkt_algorithm p=0 |
| [D2] | Primary declustering | Implemented | OK -- follows harder pT branch |
| [D3] | 10x10 binning | Implemented | OK -- [0,5] x [-3,4] |
| [D4] | pwflag=0 only | Implemented | OK -- track selection filters pwflag==0 |
| [D5] | Thrust > 0.7 | Implemented | OK |
| [D6] | No MVA | N/A for Phase 4a | OK |
| [D7] | Approach C cross-check | Phase 3 delivered | OK |
| [D8] | BBB co-primary | Implemented | OK |
| [D9] | IBU co-primary | FAILS -- needs formal [D] downscope | **A-3** |
| [D10] | ISR/FSR treatment | Implemented | OK -- ISR systematic evaluated |
| [D11] | Covariance delivery | Partially implemented | **B-1** (bootstrap incomplete) |
| [D12] | Response matrix matching | Implemented | OK -- bin-level matching |
| [D13] | pT ordering + energy systematic | Partially | Energy ordering variation not evaluated |
| [D14] | Sherpa feasibility | Phase 2 scope | N/A |

**[D13] note:** The strategy commits "energy ordering as a systematic
variation" for the hardness variable. COMMITMENTS.md lists "Hardness
variable: p_T ordering primary, energy ordering as systematic variation
[D13]." This variation was NOT evaluated in Phase 4a and is not listed
in the systematic completeness table. This should be either evaluated or
formally downscoped.

---

## Systematic Completeness Check

| Source (from COMMITMENTS.md) | Evaluated? | Assessment |
|------------------------------|-----------|------------|
| Tracking efficiency | Yes | OK -- 1% drop, bin-dependent |
| Momentum resolution | Yes | OK -- +/-10% smear |
| Angular resolution | Yes | OK -- +/-1 mrad |
| Track p threshold | Yes | OK -- 150-250 MeV/c |
| Track d0 cut | Yes | OK -- 1.5-2.5 cm |
| ntpc variation | No | Justified -- branch not accessible |
| Thrust cut | Yes | OK -- 0.6-0.8 |
| N_ch minimum | Yes | OK -- 4-6 |
| E_ch_min variation | No | **B-3** -- not justified |
| MC model dependence | Yes | OK -- 20% 2D tilt reweight |
| Unfolding method | Yes | **B-4** -- problematic |
| Heavy flavour | Yes | OK -- b-fraction +/-2% |
| ISR modelling | Yes | OK -- gen-level comparison |
| Thrust-axis resolution | Yes | OK -- 2 mrad smear |
| Background contamination | [D] | OK -- negligible |
| Hardness variable [D13] | No | Not evaluated or downscoped |
| Covariance (N>=500 bootstrap) | Partially | **B-1** -- correction not resampled |

**Score: 12/15 committed sources properly evaluated.** Three gaps (E_ch_min,
hardness variable, ntpc) of which one is justified (ntpc).

---

## Covariance Matrix Validation

| Check | Result | Assessment |
|-------|--------|------------|
| PSD (stat) | True | OK |
| PSD (total) | True | OK (min eigenvalue = -1.6e-18, numerical noise) |
| Condition number | 1.53e9 | OK (< 1e10) |
| Bootstrap replicas | 500 | OK (meets N >= 500) |
| Event-level resampling | Yes | OK (resamples events, not bins) |
| Full correction chain resampled | **No** | **B-1** -- fixed correction factors |
| Chi2 uses full covariance | Not reported | Convention requires both covariance and diagonal chi2 |

**Note:** The conventions require "Report both chi2/ndf (covariance) and
chi2/ndf (diagonal) for transparency." The artifact reports only diagonal
chi2 for the closure and stress tests. With a covariance matrix available,
the covariance-based chi2 should also be reported.

---

## Plot Validation Summary

| Figure | Labels | Physics | Format | Issues |
|--------|--------|---------|--------|--------|
| Corrected Lund plane | OK (minor overlap) | OK -- triangular shape, NP rise | OK | C-1 |
| Correction factor map | OK (minor overlap) | OK -- range [1.17, 6.67] | OK | C-1 |
| Split closure kT | OK | OK -- ratio ~1 | OK | None |
| Split closure dtheta | OK | OK -- last bin ~0.95 | OK | None |
| Closure pulls | Missing exp label | BBB: plausible; IBU: catastrophic | OK | C-2 |
| Stress ln_kt | OK | Tautological (chi2=0) | OK | C-3, A-2 |
| Stress ln_1/dtheta | OK (text overlap) | Tautological | OK | C-3, A-2 |
| Stress 2d_corr | OK | Tautological | OK | C-3, A-2 |
| Syst impact kT | OK | Unfolding method dominates | OK | B-4 |
| Syst impact dtheta | OK | Unfolding method dominates | OK | B-4 |
| Syst breakdown | OK | Unfolding method ~90% of total | OK | B-4 |
| Correlation matrix | OK | Block structure from unpopulated | OK | C-4 |
| Uncertainty summary | OK | Total >> stat (syst-dominated) | OK | C-5 |
| BBB vs IBU kT | OK | IBU ~10% low, consistent bias | OK | None |
| BBB vs IBU dtheta | OK | IBU ~10% low, consistent bias | OK | None |
| Response matrix | OK | Diagonal-dominant | OK | None |
| Diagonal fraction | OK | Mean ~0.84, one bin < 0.5 | OK | None |

**Physics plausibility checks:**
- Corrected Lund plane shows expected triangular shape with maximum
  density at low k_T, moderate angle -- consistent with non-perturbative
  enhancement. The perturbative plateau at moderate k_T shows rho ~ 0.3-0.7,
  which is plausible for charged-particle density (expected ~0.067 * 2pi
  for the LO prediction with charged particles).
- Correction factors range [1.17, 6.67] with median 1.47. The median is
  consistent with efficiency correction (1/0.79 ~ 1.27) plus detector
  effects. Bins with C > 3 are at kinematic boundaries -- physically
  reasonable.
- The IBU bias of ~10% low is consistent across both projections and all
  bins, suggesting a global normalization offset from the response matrix
  construction, not a shape distortion.

---

## Summary of Required Actions

**Before re-review, the executor must:**

1. **(A-1)** Perform at least 3 documented remediation attempts for the
   split-sample closure failure. At minimum: (a) recompute chi2 with
   combined uncertainty, (b) examine which bins drive the excess, (c)
   try 30/10 split.

2. **(A-2)** Implement split-sample stress tests: correction from half A,
   graded tilts applied to half B reco, compare to reweighted half B truth.
   Report chi2/ndf for all 12 tilt configurations.

3. **(A-3)** Formally downscope IBU [D9] with documentation of the
   limitation, literature support, and 3 remediation attempts. Update
   COMMITMENTS.md.

4. **(B-1)** Either implement proper bootstrap (resample correction factors
   per replica) or document the approximation. Fix artifact text to match
   code behavior.

5. **(B-2)** Clarify whether systematics used 10 or 40 MC files. Fix the
   discrepancy between artifact text and code.

6. **(B-3)** Evaluate E_ch_min variation or formally downscope with [D]
   label.

7. **(B-4)** Remove IBU-vs-BBB from the systematic budget. Re-evaluate
   unfolding method systematic using a meaningful approach (e.g., bootstrap
   correction factor variation).

---

**Reviewer:** Lena
**Date:** 2026-03-26
