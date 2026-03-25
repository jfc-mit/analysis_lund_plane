# Phase 4b: Inference — 10% Data Validation

> Read `methodology/03-phases.md` → "Phase 4b" for full requirements.

You are validating the analysis with **10% of the data** for a
**measurement** analysis.
Data access: **10% data subsample (fixed random seed) + MC normalized to 10% luminosity.**

## Output artifacts

- `outputs/INFERENCE_PARTIAL.md` — inference artifact with 10% results
- `analysis_note/results/*.json` — updated with 10% results
- `outputs/figures/*.pdf` — regenerated result figures with 10% data

## What this phase does

- Run full analysis chain on 10% data subsample
- Compare to Phase 4a expected (overlay, chi2)
- Evaluate GoF, NP pulls, impact ranking on 10% data
- Flag discrepancies with expected results
- Regenerate result figures with 10% data
- For extraction: include diagnostics sensitive to data/MC differences
  (not just the final quantity)

## Key requirements

- 10% data selected with fixed documented random seed
- MC normalized to 10% luminosity
- Compare to Phase 4a expected — should be compatible within
  large uncertainties
- Fix problems BEFORE seeing more data
- Update `analysis_note/results/` JSON with 10% results
- Update `COMMITMENTS.md`

## Applicable conventions

- `conventions/unfolding.md` — for unfolded measurements
- `conventions/extraction.md` — for extraction/counting measurements

The technique selected in Phase 1 determines which file applies.
Read the "When this applies" section of each to confirm.

## Review

**1-bot + plot validator** [blocking] — critical reviewer checks 10%
results for consistency with expected. Plot validator checks all figures.
Must PASS before Doc 4b begins.
