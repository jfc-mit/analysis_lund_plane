# Fixer Session: Katya — 27 March 2026

## Objective
Final round of figure and content fixes for the Lund jet plane analysis note (Doc 4b).

## Issues Addressed

### A. Multi-panel matplotlib violations (split into separate figs)

1. **nikolai_closure_pulls** (Fig 9): Replaced 1x2 multi-panel (BBB+IBU jammed together) with standalone `nikolai_closure_pulls_bbb.pdf` — single (10,10) figure with Poisson-only and combined-uncertainty pull histograms plus N(0,1) overlay.

2. **hugo_reco_gen_1d_comparison** (Fig 24): Split 1x2 side-by-side into `hugo_reco_gen_dtheta.pdf` and `hugo_reco_gen_kt.pdf` — each as standalone (10,10) figures. Required re-processing MC files (5 files x 4000 events) with fastjet clustering to regenerate the reco/gen splittings.

3. **felix_closure_pulls** (Fig 36 in appendix): Split 1x2 into `felix_closure_pulls_bbb.pdf` and `felix_closure_pulls_ibu.pdf` — each standalone. The correlation matrix that was paired with it became a standalone figure (Fig 37).

### B. Experiment label fixes

4. **oscar 2D plots** (pull map, ratio, data/MC reco ratio, 10pct Lund plane): The original labels had "ALEPH" overlapping with "10% subsample, sqrt(s) = 91.2 GeV" because `set_aspect("equal")` made the axes too narrow for CMS-style large-font labels. Fixed by:
   - Removing `set_aspect("equal")` — justified because ln(1/dtheta) and ln(kT/GeV) are different physical quantities with different ranges, so equal aspect is not required
   - Using `llabel="Open Data (10%)"` with `rlabel=r"$\sqrt{s} = 91.2$ GeV"`
   - Moving chi2/ndf to a text annotation box in the lower-right of the pull map

5. **oscar_per_year** stability plots: Shortened `llabel` from "Open Data (10%, per year)" to "Open Data (10%)".

6. **oscar_lund_plane_10pct_corrected**: Same label fix as other 2D plots.

### C. LaTeX composition fixes

7. Updated figure references in the .tex to use the split single-panel figures:
   - `nikolai_closure_pulls.pdf` → `nikolai_closure_pulls_bbb.pdf`
   - `hugo_reco_gen_1d_comparison.pdf` → side-by-side `hugo_reco_gen_dtheta.pdf` + `hugo_reco_gen_kt.pdf`
   - `felix_closure_pulls.pdf` + `felix_correlation_matrix.pdf` → separate figures for BBB pulls, IBU pulls, and correlation matrix
   - `hugo_correction_factor_preview.pdf` made standalone (was paired with the old multi-panel reco/gen figure)

8. Fixed broken cross-reference: `\ref{sec:syst-mc-model}` → `\ref{sec:syst-model}` (was rendering as "Section ??").

### D. Content expansion

9. **Section 8.2 (1D projections)**: Expanded from 3-sentence stub to full discussion including:
   - Projection formulae
   - Physics interpretation of the ln(kT) projection (hadronization peak, perturbative tail, DGLAP suppression)
   - Physics interpretation of the ln(1/dtheta) projection (phase-space boundary, tracking resolution limit)
   - Quantitative data/MC agreement assessment
   - LO QCD benchmark comparison

10. **Section 8.3 (Reco-level 2D)**: Expanded from 2-sentence stub to full discussion including:
    - Description of all four panels in Figure 22
    - Quantitative data/MC ratio (mean 1.005, std 0.105)
    - genBefore truth plane interpretation
    - Detector effects discussion (angular resolution, momentum smearing)
    - Connection to closure test validation

11. **Section 8.4 (Uncertainty breakdown)**: Expanded from figure-only stub to full discussion including:
    - Statistical uncertainty behavior across the Lund plane
    - Systematic uncertainty hierarchy (MC model dependence dominant, tracking efficiency second)
    - Total uncertainty range (1-8% relative)
    - Systematic-to-statistical ratio (2:1 in bulk)
    - Connection to future directions (alternative generator MC)

## Output Files

- `analysis_note/fix_figs_katya.py` — figure fix script (v2, with all 8 fixes)
- `analysis_note/ANALYSIS_NOTE_doc4b_v7.tex` — updated LaTeX source
- `analysis_note/ANALYSIS_NOTE_doc4b_v7.pdf` — compiled PDF (44 pages, up from 39)
- Regenerated figures in `analysis_note/figures/`:
  - `nikolai_closure_pulls_bbb.{pdf,png}`
  - `hugo_reco_gen_dtheta.{pdf,png}`
  - `hugo_reco_gen_kt.{pdf,png}`
  - `felix_closure_pulls_bbb.{pdf,png}`
  - `felix_closure_pulls_ibu.{pdf,png}`
  - `oscar_pull_map_10pct.{pdf,png}`
  - `oscar_ratio_10pct_vs_expected.{pdf,png}`
  - `oscar_data_mc_reco_ratio_2d.{pdf,png}`
  - `oscar_lund_plane_10pct_corrected.{pdf,png}`
  - `oscar_per_year_kt.{pdf,png}`
  - `oscar_per_year_dtheta.{pdf,png}`

## Verification

All figures verified by visual inspection of PNGs:
- No label overlaps on any figure
- All single-panel figures use (10,10) figsize
- All 2D colorbars use make_square_add_cbar
- All experiment labels follow the convention (ALEPH + Open Data/Open Simulation + sqrt(s))
- chi2/ndf on pull map is a text annotation, not in the label
- PDF compiles cleanly (only standard overfull hbox warnings)
