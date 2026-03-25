# Phase 4a: Inference — Expected Results

> Read `methodology/03-phases.md` → "Phase 4a" for full requirements.
> Read `methodology/appendix-plotting.md` for figure standards.
> Read `conventions/fitting.md` for fit diagnostics and interpretation.

You are computing **expected results** for a **measurement** analysis.
Data access: **MC/Asimov pseudo-data only. No real data.**

**Start in plan mode.** Produce a plan before writing any code.

## Output artifacts

- `outputs/INFERENCE_EXPECTED.md` — inference artifact with expected results
- `analysis_note/results/*.json` — machine-readable results (see below)
- `outputs/figures/*.pdf` — all analysis and result figures

## What this phase does

- Evaluate experimental + theory systematics as rate/shape variations
- Build statistical model or correction chain
- Produce expected results on Asimov/MC pseudo-data (never real data)
- Closure tests, stress tests, validation tests
- Full covariance matrix (stat + per-syst + total)
- Comparison to theory predictions using full covariance
- Per-systematic impact figures (bin-dependent shifts)
- Operating point stability scan

## Machine-readable outputs (mandatory)

Write all numerical results to `analysis_note/results/` as JSON:
- Fitted parameters with uncertainties
- Per-systematic shifts (bin edges + up/down shifts)
- Covariance matrices (stat, syst, total)
- Validation test results (chi2, ndf, p-value, passes)

Organize into separate files by category (e.g., `parameters.json`,
`systematics.json`, `covariance.json`, `validation.json`). The note
writer discovers files by reading the directory — use descriptive
filenames. These JSON files are the single source of truth for the
note writer; it reads numbers from here, not from prose artifacts.

## Key requirements

- Every systematic variation justified by a measurement or published
  uncertainty (no arbitrary "±50%" without citation)
- No flat borrowed systematics (unless documented: subdominant + infeasible
  to propagate + cited measurement)
- Independent closure test (not the same MC used for corrections)
- Systematic completeness table vs conventions + reference analyses
- Per-systematic documentation: physical origin, evaluation method,
  numerical impact, interpretation
- Phase 1 traceability: every committed source implemented or [D] downscoped
- Update `COMMITMENTS.md` at phase boundary

## Applicable conventions

- `conventions/unfolding.md` — for unfolded measurements
- `conventions/extraction.md` — for extraction/counting measurements

The technique selected in Phase 1 determines which file applies.
Read the "When this applies" section of each to confirm.

## Review

**1-bot + plot validator** [blocking] — critical reviewer checks inference
correctness (fits converge, code correct, no shortcuts, systematics
non-trivial). Plot validator checks all figures. Must PASS before Doc 4a
begins.
