# Phase 4b Plan — 10% Data Inference

**Session:** Oscar | **Date:** 2026-03-26

## Overview

First look at REAL DATA. Process 10% of data (fixed seed 42), apply full MC
correction factors, compare to Phase 4a expected results.

## Upstream artifacts

| Artifact | Path | Key contents |
|----------|------|-------------|
| Strategy | `phase1_strategy/outputs/STRATEGY_peter_2026-03-25_17-17.md` | Observable definition, binning, systematics plan |
| Phase 3 pipeline | `phase3_selection/src/01_process_all.py` | Event selection, Lund declustering |
| Correction factors | `phase3_selection/outputs/correction_ingrid.npz` | C = N_genBefore / N_reco, full MC (40 files) |
| Expected results | `phase4_inference/4a_expected/outputs/expected_results_felix.npz` | MC pseudo-data corrected Lund plane |
| Covariance | `phase4_inference/4a_expected/outputs/covariance_felix.npz` | stat + syst covariance from bootstrap |
| Expected JSON | `analysis_note/results/lund_plane_expected.json` | Machine-readable expected density |
| Phase 3 cutflow | `phase3_selection/outputs/cutflow_ingrid.json` | Full data cutflow for comparison |

## Key numbers from upstream

- Full data: 3,050,610 events -> 2,846,194 after selection -> 5,692,388 hemispheres
- Expected 10%: ~285k events selected, ~569k hemispheres
- MC reco: 1,442,350 hemispheres; MC genBefore: 1,936,712 hemispheres
- Correction factors: 10x10 grid, range [1.17, 6.67], 58 populated bins
- Binning: ln(1/Delta_theta) in [0,5] x 10, ln(k_T/GeV) in [-3,4] x 10

## Scripts to write

### Script 1: `01_process_10pct_data.py`
Process 10% of real data with fixed seed 42:
- For each data file: generate random event indices with `np.random.default_rng(42)`
- Select exactly 10% of events (before analysis selection)
- Apply identical event/track selection as Phase 3
- Build Lund plane from 10% subsample
- Save per-file histograms for per-year stability check
- Save cutflow per file
- Output: `outputs/data_10pct_lund_oscar.npz`, `outputs/data_10pct_per_year_oscar.npz`

### Script 2: `02_correct_and_compare.py`
Apply corrections and compare to expected:
- Load 10% data Lund plane
- Load full-MC correction factors from Phase 3
- Apply bin-by-bin correction: rho = (N_data_10pct * C) / (N_hemi_10pct * bin_area)
  Wait -- this is WRONG. The correction is C = N_genBefore / N_reco. So:
  corrected_counts = N_data_10pct * C
  Then normalize: rho = corrected_counts / (N_hemi_corrected * bin_area)
  where N_hemi_corrected = N_hemi_data_10pct * (N_hemi_genBefore / N_hemi_reco)
  OR equivalently: rho = corrected_counts / (N_hemi_genBefore_scale * bin_area)

  Actually, the cleanest formulation is:
  rho(i,j) = [N_data(i,j) * C(i,j)] / [N_hemi_data * (N_hemi_genBefore/N_hemi_reco) * bin_area]

  But wait -- looking at the Phase 4a expected artifact:
  "rho(i,j) = (N_reco * C) / (N_hemi_genBefore * bin_area)"
  The denominator uses N_hemi_genBefore. For data, we should use:
  rho(i,j) = [N_data(i,j) * C(i,j)] / [N_hemi_data * R_hemi * bin_area]
  where R_hemi = N_hemi_genBefore / N_hemi_reco is the hemisphere efficiency correction.

  This needs care. I'll follow exactly what Phase 3/4a did.

- Compare to expected: compute pull = (data_10pct - expected) / sigma
- Compute chi2 using covariance from Phase 4a (scaled for 10% statistics)
- Generate ratio plots

### Script 3: `03_diagnostics.py`
Diagnostic comparisons:
- Data (10%) vs MC reco: 2D Lund plane ratio
- 1D projections (ln k_T, ln 1/Delta_theta) with data points + MC band
- Per-year consistency: compare Lund plane from each data year
- Cutflow: 10% data vs MC (efficiency agreement)

### Script 4: `04_write_json.py`
Write machine-readable outputs:
- `analysis_note/results/lund_plane_10pct.json`

## Figures to produce

1. Corrected 10% data Lund plane (2D colz)
2. 10% data vs expected comparison (2D ratio)
3. Pull map (data - expected) / sigma
4. 1D projection in ln(k_T) with data points + MC overlay
5. 1D projection in ln(1/Delta_theta) with data points + MC overlay
6. Per-year stability (1D projections per year, overlaid)
7. Cutflow comparison (10% data vs MC scaled)
8. Data/MC reco ratio (2D, before correction)

## Execution order

1. Script 1 (processing) -- long, ~3 min with 10% data and parallel processing
2. Script 2 (correction + comparison) -- fast
3. Script 3 (diagnostics) -- fast
4. Script 4 (JSON output) -- fast
5. Write artifact

## Timing estimate

- 10% of ~3M events = ~305k events, 6 files
- Phase 3 processed 6 data files in ~35s each -> 10% should be ~3.5s each
- Total processing: < 1 minute
- Plotting and comparison: < 1 minute
- Total: ~5 minutes
