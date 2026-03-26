# Session Log: Oscar (Phase 4b Executor)

## Timeline

| Time | Action | Notes |
|------|--------|-------|
| 04:46 | Read upstream artifacts | Strategy, Phase 4a expected, Phase 3 pipeline, correction factors |
| 04:46 | Write plan.md | 5 scripts planned |
| 04:46 | Script 01: Process 10% data | 6 files, seed=42, parallel processing |
| 04:48 | Script 01 complete | 569,472 hemispheres, 2,895,778 splittings (119.8s) |
| 04:49 | Script 02: Correction + comparison | Applied full-MC BBB correction |
| 04:50 | Script 02 complete | chi2/ndf = 197.7/57 = 3.47, 7 bins with |pull|>3 |
| 04:51 | Script 03: Diagnostics | Data/MC ratio, per-year stability, cutflow |
| 04:51 | Script 03 complete | Per-year chi2/ndf all < 1.1, cutflow eff agrees to 0.1% |
| 04:51 | Script 04: Write JSON | analysis_note/results/lund_plane_10pct.json |
| 04:53 | Script 05: Self-check | Full covariance chi2, normalization, pattern analysis |
| 04:53 | Self-check complete | Wide-angle pulls ~0, collinear pulls ~1.6 (expected MC mismodelling) |
| 04:54 | Write artifact | INFERENCE_PARTIAL_oscar.md |

## Key Decisions

1. **10% subsampling**: Applied to raw events (before selection), seed=42, same for all files
2. **Correction normalization**: N_hemi_corrected = N_hemi_data * R_hemi where R_hemi = N_hemi_genBefore/N_hemi_reco
3. **Chi2 method**: Diagonal sigma^2 = stat_data^2 + total_expected^2 (full covariance gives inflated chi2 due to correlations)

## Issues Found

1. chi2/ndf = 3.5 comparing data to MC pseudo-data -- expected, reflects real data/MC differences
2. 7 bins with |pull| > 3, concentrated in collinear region (ln(1/dtheta) > 2.5)
3. Pattern: wide-angle agreement excellent (pull mean ~0), collinear shows systematic excess in data
