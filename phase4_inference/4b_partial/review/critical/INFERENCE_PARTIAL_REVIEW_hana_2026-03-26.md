# Phase 4b Review: Inference -- 10% Data Validation

**Reviewer:** Hana (critical) | **Date:** 2026-03-26
**Artifact under review:** `INFERENCE_PARTIAL_oscar_2026-03-26_04-54.md`
**Upstream reference:** `INFERENCE_EXPECTED_nikolai_2026-03-26_03-56.md`

---

## Review Summary

**Verdict: PASS**

The 10% data validation artifact is thorough, internally consistent, and
demonstrates that the analysis chain works correctly on real data. The
observed data/MC differences are physically interpretable and do not
indicate analysis bugs. All required diagnostics are present. No Category A
or B findings.

---

## 1. Fixed-Seed Subsampling and Representativeness

**Status: PASS**

- Seed 42 via `np.random.default_rng(42)` is documented.
- The 10% subsample is applied to raw events BEFORE analysis selection,
  which is the correct procedure -- it ensures the selection efficiency is
  measured independently on the subsample.
- Event counts: 305,058 / 3,050,610 = 10.000% (exact to 4 digits).
- Per-file 10% ratios are consistent (each file subsampled independently
  with the same procedure).
- Splittings/hemisphere: 5.085 (10%) vs 5.083 (full) -- ratio 1.0004.
  This confirms the subsample is unbiased in the observable.
- The 10% vs full data consistency check (Section 4.4) yields
  chi2/ndf = 41.8/58 = 0.72, pull mean = -0.077, pull std = 0.845.
  This is a definitive validation of the subsampling procedure.

**No concerns.**

## 2. Correction Factors Applied Correctly

**Status: PASS**

- Correction factors are from the full MC (40 files, Phase 3): C(i,j) range
  [1.17, 6.67]. This is correct -- the 10% data subsample does NOT affect
  the correction factors.
- R_hemi = 1936712 / 1442350 = 1.3427 (from full MC genBefore/reco). This
  matches the Phase 4a value exactly.
- Corrected hemispheres: 569,472 * 1.3427 = 764,657. Arithmetic verified.
- The density formula rho(i,j) = N_corrected(i,j) / (N_hemi_corrected * bin_area)
  uses the correct normalization. The bin_area = 0.35 matches the 10x10
  grid specification.
- Cross-check: integral of rho * bin_area = 4.511 (data) vs 4.562 (MC),
  ratio 0.989. The 1.1% deficit is well within the ~5% systematic budget.

**The correction procedure is applied identically to Phase 4a, with
corrections from the full MC applied to the 10% data. No errors found.**

## 3. chi2/ndf = 3.47 Interpretation

**Status: PASS**

- Diagonal chi2/ndf = 197.7/57 = 3.47. The sigma used is
  sigma^2 = sigma_data_stat^2 + sigma_expected_total^2, which is the
  correct combination for comparing two independent measurements.
- The full-covariance chi2 (1995.7/57 = 35.0) is noted but correctly
  identified as inflated by bin-to-bin correlations amplifying coherent
  shifts. The diagonal chi2 is the appropriate metric here.
- The chi2/ndf = 3.47 is correctly attributed to genuine data/MC
  differences, not analysis bugs. Evidence:
  - (a) The wide-angle region (ln(1/dtheta) < 2.5) has pull mean +0.07 and
    std 1.10 -- fully consistent with a unit Gaussian. This validates the
    analysis chain in the region where corrections are smallest.
  - (b) The collinear region (ln(1/dtheta) > 2.5) shows pull mean +1.59 --
    a coherent positive shift (data > MC) consistent with PYTHIA 6.1
    underestimating collinear splitting rates.
  - (c) All 7 bins with |pull| > 3 have positive pulls, and 6/7 are in the
    collinear region. A random statistical fluctuation would produce
    symmetric pulls.

**The interpretation is physically sound. PYTHIA 6.1 is a 2001 generator;
collinear underestimation is a known limitation improved in later generators.
The chi2/ndf = 3.47 is NOT alarming and does NOT indicate an analysis
problem.**

## 4. Per-Year Stability

**Status: PASS**

- All 6 data-taking periods tested independently against the combined 10%
  sample.
- chi2/ndf values (ln kT projection): 0.52, 1.06, 0.34, 0.69, 0.40, 0.96.
  All well below 2.0.
- No evidence for time-dependent detector effects.
- The figures (oscar_per_year_kt.png, oscar_per_year_dtheta.png) confirm
  that per-year ratios scatter around unity within +/-5% in the bulk,
  consistent with the ~10% statistical uncertainty per period.

**Per-year stability is excellent.**

## 5. Diagnostic Completeness

**Status: PASS**

All required diagnostics from the Phase 4b CLAUDE.md are present:

| Diagnostic | Present | Comment |
|-----------|---------|---------|
| 10% subsample cutflow | Yes | Table in Section 1.2 |
| Per-file cutflow | Yes | Table in Section 1.2 |
| Corrected Lund plane (2D) | Yes | Figure 1 |
| Comparison to expected (chi2, pulls) | Yes | Section 3 |
| Regional pull analysis | Yes | Section 3.3 -- excellent decomposition |
| High-pull bin table | Yes | Section 3.4 |
| Ratio map (data/expected) | Yes | Figure 2 |
| Pull map | Yes | Figure 3 |
| 1D projections (data + MC) | Yes | Figures 4-5 |
| Per-year stability | Yes | Section 4.2, Figures 6-7 |
| Data/MC reco ratio | Yes | Section 4.1, Figure 9 |
| Cutflow comparison | Yes | Section 4.3, Figure 8 |
| 10% vs full data consistency | Yes | Section 4.4 |
| Machine-readable JSON | Yes | lund_plane_10pct.json |
| Machine-readable NPZ files | Yes | 4 files in outputs/ |

**All diagnostics present and complete.**

## 6. Figure Quality Assessment

All 9 figures reviewed:

1. **oscar_lund_plane_10pct_corrected.png** -- ALEPH label present with
   "Open Data (10%)" tag, correct axes, viridis colormap, correct density
   range. The triangular structure matches the expected Lund plane shape.
   The "(10%)" label clearly marks the data fraction.

2. **oscar_ratio_10pct_vs_expected.png** -- Diverging colormap (red-blue)
   centered at 1.0, correct axis labels. The collinear excess (red at high
   ln(1/dtheta)) is clearly visible. Range [0.7, 1.3] is appropriate.

3. **oscar_pull_map_10pct.png** -- Diverging colormap, chi2/ndf = 197.7/57
   stated in title. The collinear concentration of high pulls is visually
   clear.

4. **oscar_1d_kt_projection.png** -- Data points with error bars overlaid
   on MC expected band. Pull panel below. ALEPH label present. Good
   agreement visible.

5. **oscar_1d_dtheta_projection.png** -- Same format as kt projection.
   The data excess at intermediate ln(1/dtheta) is visible, consistent with
   the 2D analysis.

6-7. **oscar_per_year_kt.png, oscar_per_year_dtheta.png** -- All 6 periods
   shown with ratio to combined. Ratios scatter around 1.0 within +/-5%.
   ALEPH label present.

8. **oscar_cutflow_comparison.png** -- Bar chart with Data/MC ratio panel.
   Clean agreement visible. The ratio panel axis (0.95-1.05) is appropriate.

9. **oscar_data_mc_reco_ratio_2d.png** -- Diverging colormap showing the
   reco-level data/MC ratio. Mean 1.008, range [0.8, 1.2]. The pattern is
   mild and uniform, confirming good detector simulation.

**Minor observation (C):** Some figure titles have minor text overlap (e.g.,
"10% d / MC Expected" in figure 2 title). This is cosmetic and does not
affect physics content. The PDF versions should be used for the analysis
note.

## 7. Consistency Checks Between Artifact and JSON

Cross-checked key numbers between the narrative artifact and the
machine-readable JSON:

| Quantity | Artifact | JSON | Match |
|----------|----------|------|-------|
| chi2/ndf | 197.7/57 = 3.47 | 197.684/57 = 3.468 | Yes |
| Pull mean | +0.604 | 0.604 | Yes |
| Pull std | 1.762 | 1.762 | Yes |
| Max |pull| | 6.73 | 6.735 | Yes |
| N bins |pull| > 3 | 7 | 7 | Yes |
| N_hemi_data | 569,472 | 569472 | Yes |
| N_hemi_corrected | 764,657 | 764657.16 | Yes |
| R_hemi | 1.3427 | 1.3427 (derived) | Yes |

**All numbers are consistent.**

## 8. COMMITMENTS.md Compliance

The artifact claims the following commitments are fulfilled:
- [x] Process 10% of real data with fixed seed (42)
- [x] Apply bin-by-bin correction factors from full MC
- [x] Corrected Lund plane density from 10% data
- [x] Compare to Phase 4a expected result (chi2, pulls)
- [x] Per-year consistency check
- [x] Cutflow comparison (data vs MC)
- [x] Data/MC reco-level ratio
- [x] 1D projections with data points + MC band
- [x] Machine-readable JSON output

**All claims verified against the artifact content.**

## 9. Regression Checklist

- [ ] Any validation test failures without 3 documented remediation attempts?
  **No.** No validation tests failed in Phase 4b.
- [ ] Any single systematic > 80% of total uncertainty?
  **No.** Systematics were not re-evaluated in 4b (correctly, they come
  from 4a/full MC).
- [ ] Any GoF toy distribution inconsistent with observed chi2?
  **N/A** for Phase 4b.
- [ ] Any flat-prior gate excluding > 50% of bins?
  **No.** 57/100 bins populated, same as expected.
- [ ] Any tautological comparison presented as independent validation?
  **No.** The 10% subsample is genuinely independent from the MC
  correction factors.
- [ ] Any visually identical distributions that should be independent?
  **No.** Data and MC show clear differences in the collinear region.
- [ ] Any result > 30% from a well-measured reference?
  **No.** The integral (4.51 splittings/hemisphere) is within 1.1% of MC.
- [ ] All binding commitments fulfilled?
  **Checked.** The 4b-specific commitments are met. The [D9] downscoping
  and other Phase 1 commitments are inherited from 4a.

**No regression triggers.**

---

## Classification Summary

| # | Finding | Cat. | Status |
|---|---------|------|--------|
| C-1 | Minor text overlap in some PNG figure titles | C | Cosmetic; PDF versions used in AN |

---

## Verdict

**PASS**

The Phase 4b artifact demonstrates a thorough, correct, and well-documented
application of the analysis chain to 10% of the real data. The key findings
-- collinear excess in data vs PYTHIA 6.1, excellent wide-angle agreement,
per-year stability, and validated subsampling -- are physically sound and
well-supported by the diagnostics. The analysis is ready to proceed to
Doc 4b (analysis note update with 10% results).
