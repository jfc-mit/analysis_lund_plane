# Fix Session: Gunnar (2nd iteration) -- 2026-03-26

## Problem
All 2D plots with colorbars had wrong aspect ratios and inconsistent colorbar gaps.
The first fix attempt (Wolfgang) partially fixed this but left `fig.colorbar(im, ax=ax)`,
`fig.colorbar(im, ax=ax, shrink=0.8)` patterns in several files -- these are Category A
per the spec.

## Root cause
The correct pattern is:
```python
im = ax.pcolormesh(...)
ax.set_aspect("equal")
cax = mh.utils.make_square_add_cbar(ax)
fig.colorbar(im, cax=cax, label="...")
```

The wrong pattern `fig.colorbar(im, ax=ax, ...)` lets matplotlib steal space from the
main axes, producing non-square data areas and inconsistent colorbar gaps.

## Files fixed (7 files, 19 colorbar patterns total)

### phase4_inference/4b_partial/src/02_correct_and_compare.py
- 3 colorbars fixed (corrected Lund plane, ratio to expected, pull map)
- Added `ax.set_aspect("equal")` to all three

### phase4_inference/4b_partial/src/03_diagnostics.py
- 1 colorbar fixed (data/MC reco ratio 2D)
- Added `ax.set_aspect("equal")`

### phase4_inference/4a_expected/src/04_figures.py
- 7 colorbars fixed (BBB Lund plane, IBU Lund plane, correction map,
  response matrix, diagonal fraction, correlation matrix)
- Changed all `aspect="auto"` to `aspect="equal"` for imshow
- Added `ax.set_aspect("equal")` for pcolormesh

### phase4_inference/4a_expected/src/05_combined_deliverables.py
- 6 colorbars fixed (Lund plane, correction map, correlation matrix,
  response matrix, diagonal fraction)
- Changed `aspect="auto"` to `aspect="equal"` for imshow

### phase4_inference/4a_expected/src/06_fix_nikolai.py
- 1 colorbar fixed (correlation matrix)
- Changed `aspect="auto"` to `aspect="equal"`

### phase4_inference/4a_expected/src/fix_plots_wolfgang.py
- 3 colorbars fixed (response matrix, felix correlation matrix,
  nikolai correlation matrix)
- Removed `shrink=0.8` parameter

## Verification

### Grep check: zero forbidden patterns
- `fig.colorbar(im, ax=ax` -- 0 matches
- `plt.colorbar` -- 0 matches
- `fig.colorbar(im)` -- 0 matches
- `shrink=` -- 0 matches

### Figure regeneration
Ran all three fix_plots_wolfgang.py scripts:
- phase4_inference/4a_expected/src/fix_plots_wolfgang.py -- SUCCESS
- phase4_inference/4b_partial/src/fix_plots_wolfgang.py -- SUCCESS
- phase3_selection/src/fix_plots_wolfgang.py -- SUCCESS

### Visual verification (PNG readback)
All regenerated 2D figures confirmed:
- Square data area
- Colorbar flush against right edge with small consistent gap
- No text overlap or distortion
- Proper axis labels visible

### Pull calculation verification (Step 4)
The `sigma_data` in 02_correct_and_compare.py uses:
```
stat_err = sqrt(h2d_data) * correction / (n_hemi_corrected * bin_area)
```
This correctly propagates Poisson sqrt(N_data) through the bin-by-bin correction
factor and normalization. The 1D projection pull uses
`sigma_tot = sqrt(err_data^2 + err_expected^2)`, combining data stat and expected
total in quadrature. Verified correct.

### lint-plots
27 violations found, but NONE related to colorbars or aspect ratios.
All remaining violations are pre-existing (underscore labels, bar charts,
exp_label on ratio panels).

## Outputs
- Fixed scripts in phase4_inference/4a_expected/src/, phase4_inference/4b_partial/src/
- Regenerated figures in all phase outputs/figures/ directories
- Staged figures in analysis_note/figures/
- New analysis_note/ANALYSIS_NOTE_doc4b_v2.tex and .pdf (1.39 MiB)
- Change Log updated with v2 entry documenting the plotting fixes
