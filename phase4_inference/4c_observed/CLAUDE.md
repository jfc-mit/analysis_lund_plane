# Phase 4c: Inference — Full Data

> Read `methodology/03-phases.md` → "Phase 4c" for full requirements.

You are producing **final results on the full dataset** for a
**measurement** analysis.
Data access: **Full dataset.** Only after human approval at the Doc 4b gate.

## Output artifacts

- `outputs/INFERENCE_OBSERVED.md` — inference artifact with full results
- `analysis_note/results/*.json` — updated with full data results
- `outputs/figures/*.pdf` — final result figures

## What this phase does

- Run full analysis chain on complete dataset
- Compare to BOTH 10% and expected results
- Re-evaluate systematics on full data (not just transferred from MC)
- Investigate anomalies (large NP pulls, poor GoF, pathologies)
- Configuration selection with GoF check
- Fit triviality gate (chi2 = 0 is an alarm, not a result)
- Viability check on all reported measurements
- Competitiveness assessment for multi-observable analyses
- Final machine-readable results in JSON

## Key requirements

- Compare to both 10% and expected: flag >2-sigma disagreement
- Re-evaluate systematics on full data where possible
- GoF of primary configuration: chi2/ndf < 3 (p > 0.01)
- Fit boundary check (no parameters at boundaries)
- Fit triviality gate (chi2 = 0 → investigate circularity)
- Viability: total uncertainty < 50% of central value
- Update `COMMITMENTS.md` — all lines should be [x] or [D]

## Applicable conventions

- `conventions/unfolding.md` — for unfolded measurements
- `conventions/extraction.md` — for extraction/counting measurements

The technique selected in Phase 1 determines which file applies.
Read the "When this applies" section of each to confirm.

## Review

**1-bot + plot validator** [blocking] — critical reviewer checks full
results, GoF, pathologies, comparison to expected/10%. Must PASS before
Doc 4c begins.
