# Fix Session Log: Wolfgang (2026-03-26)

## Purpose
Address all blocking plotting and prose issues found during human review of the Doc 4b analysis note.

## Issues Fixed

### PLOTTING FIXES

**Issue #1: Data/MC comparison plots (Figs 1-4 in the AN)**
- Changed: data shown as raw counts (events/bin), MC scaled to match data integral
- Changed: lower panel now shows (Data - MC) / sigma_Data (pull-style) instead of Data/MC ratio
- Changed: y-axis label on lower panel is the proper LaTeX fraction
- Fixed: "Axis 0" text suppressed from all ratio panels
- Script: `phase2_exploration/src/fix_data_mc_wolfgang.py`
- Affected figures: `hugo_pmag_data_mc`, `hugo_pmag_log_data_mc`, `hugo_theta_data_mc`, `hugo_phi_data_mc`, `hugo_pt_data_mc`, `hugo_thrust_data_mc`, `hugo_nch_data_mc`, `hugo_hemi_mult_data_mc`, `hugo_thrust_charged_data_mc`

**Issue #2: All 2D Lund plane plots — SQUARE aspect ratio**
- Added `ax.set_aspect("equal")` to all 2D pcolormesh plots
- Used `mh.utils.make_square_add_cbar(ax)` for colorbar placement
- Script: `phase3_selection/src/fix_plots_wolfgang.py` (Phase 3 figures)
- Script: `phase4_inference/4a_expected/src/fix_plots_wolfgang.py` (Phase 4a figures)
- Script: `phase4_inference/4b_partial/src/fix_plots_wolfgang.py` (Phase 4b figures)
- Affected figures: All `ingrid_*` 2D plots, `felix_*` 2D plots, `nikolai_*` 2D plots, `oscar_*` 2D plots

**Issue #3: Closure pull distribution (Fig 9) — completely redone**
- Changed from broken 1x2 subplot layout to separate individual figures
- Each panel is now a clean (10, 10) figure with proper spacing
- Created: `felix_closure_pulls_bbb.pdf` and `felix_closure_pulls_ibu.pdf`
- `felix_closure_pulls.pdf` kept as backward-compatible copy of BBB version
- `nikolai_closure_pulls.pdf` regenerated as clean single figure

**Issue #4: Systematic breakdown (Fig 13) — legend overlap fixed**
- Moved legend to upper left with extended ylim (1.5x) to prevent overlap
- Applied to both `felix_syst_breakdown` and `nikolai_syst_breakdown`

**Issue #5: Systematic impact (Fig 14) — legend overlap fixed**
- Moved legend to lower left with `bbox_to_anchor=(0.0, 0.0)` to avoid overlapping curves
- Applied to both `felix_syst_impact_*` and `nikolai_syst_impact_*`

**Issue #6: Correlation matrix (Fig 18) — square aspect + investigation**
- Set `aspect="equal"` on imshow
- Investigation findings:
  - High off-diagonal correlations are EXPECTED: the dominant MC model-dependence systematic shifts all bins coherently (same sign)
  - This produces a block-diagonal structure in the correlation matrix, which is physically correct
  - Mean off-diagonal correlation ~0.7 among populated bins — driven by the coherent model-dependence shift
  - NOT pathological: this is the standard correlation structure for measurements with dominant common-mode systematics

**Issue #7: 10% data 2D plots (Figs 25-26) — square aspect + label fix**
- Square aspect applied to all 2D 10% data plots
- chi2/ndf annotation moved to text box on the pull map (not crowding the experiment label)

**Issue #8: 1D projections with data (Fig 27) — MC band + legend**
- MC expected shown as filled histogram band (`fill_between` + step outline)
- Three legend entries: "MC Expected (central)", "MC Expected (±1σ)", "Data (10%)"
- All entries now have proper legend labels

**Issue #9: Per-year stability (Fig 28) — clean layout**
- Per-year 1D projections regenerated with clean layout
- "Axis 0" text suppressed from ratio panels

### PROSE FIXES

**Issue #10: Systematic subsections — flowing prose**
- Rewrote all 12 systematic subsections in Section 5.x
- Removed bold **Method:** / **Impact:** / **Interpretation:** label format
- Each subsection now reads as a coherent paragraph describing:
  - Physical origin of the systematic
  - How the variation was performed
  - Numerical impact (max and mean relative shifts)
  - Interpretation and context
- Subsections rewritten: tracking efficiency, momentum resolution, angular resolution, track p threshold, track d0 cut, thrust cut, N_ch minimum, E_ch minimum, thrust-axis resolution, MC model dependence, correction factor stability, heavy flavour, ISR modelling

**Issue #11: Fig 6 caption — factual error corrected**
- OLD: "The correction is close to unity in the densely populated core"
- NEW: "The correction ranges from approximately 1.2 to 3.0, with a median value of 1.47 in the populated region"
- Added explanation: minimum of 1.17 reflects ~79% event selection efficiency (1/0.79 ≈ 1.27) plus detector effects
- Noted that even in the core, correction is typically 1.3-1.5

### BINNING INVESTIGATION

**Issue #12: Finer binning study**
- Script: `phase3_selection/src/binning_study_wolfgang.py`
- Results saved to: `phase3_selection/outputs/binning_study_wolfgang.json`

**Findings:**
- Current 10x10: 59 populated bins (data), 58 (reco), avg 414,686 data entries/populated bin
- Core region (1 < ln(1/Δθ) < 4, -1 < ln(kT) < 3): 30 bins, avg 424,382 data entries/bin
- Mean diagonal fraction at 10x10: 0.84

**15x15 estimate:** ~131 populated bins, avg ~184,000 data entries/bin (core ~189,000)
- VIABLE: far above the 500-entry threshold even in the core
- Estimated migration fraction: ~44% (up from ~16% at 10x10)

**20x20 estimate:** ~232 populated bins, avg ~104,000 data entries/bin (core ~106,000)
- VIABLE in terms of statistics (well above 100 entries per bin)
- Estimated migration fraction: ~58% — this is high but may be acceptable for bin-by-bin correction

**Recommendation:** 15x15 is clearly viable and would provide 2.5x more measured bins while maintaining healthy statistics. 20x20 is also viable in terms of statistics but the higher migration fraction (~58%) would need careful validation of the bin-by-bin correction. A proper study requires reprocessing Phase 3 data at the new binning (the current estimates use approximate scaling from the 10x10 histograms).

**IMPORTANT CAVEAT:** These estimates are from scaling the 10x10 histograms. A proper study requires re-histogramming the raw Lund coordinates at finer binning, which involves reprocessing Phase 3 data.

## Files Modified

### New scripts
- `phase2_exploration/src/fix_data_mc_wolfgang.py`
- `phase3_selection/src/fix_plots_wolfgang.py`
- `phase3_selection/src/binning_study_wolfgang.py`
- `phase4_inference/4a_expected/src/fix_plots_wolfgang.py`
- `phase4_inference/4b_partial/src/fix_plots_wolfgang.py`

### LaTeX source
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex` (prose + caption fixes)

### Regenerated figures (all phases)
- Phase 2: 9 data/MC comparison plots
- Phase 3: 11 Lund plane + correction plots
- Phase 4a: 14 inference + systematic plots (felix + nikolai)
- Phase 4b: 8 10% data plots

### Compiled output
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf` (recompiled)

### Binning study output
- `phase3_selection/outputs/binning_study_wolfgang.json`
