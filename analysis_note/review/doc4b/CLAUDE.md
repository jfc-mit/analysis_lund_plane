# Doc 4b: Analysis Note — 10% Data Validation

> Read `methodology/analysis-note.md` for the full AN specification.

You are updating the analysis note with **10% data results** for a
**measurement** analysis.

The Doc 4a AN established the full document structure. Your job is to
evolve it — update results, replace placeholders, regenerate comparison
figures. Do NOT rebuild from scratch unless a regression demands it.

## You are the note writer

You do NOT read data files or write analysis code. You read the previous
AN version, updated artifacts, and `results/` JSON.

## Inputs

- `analysis_note/ANALYSIS_NOTE_doc4a_v*.tex` — the previous AN version (latest)
- `INFERENCE_PARTIAL.md` — 10% inference artifact
- `analysis_note/results/*.json` — updated with 10% results
- `*/outputs/figures/` — regenerated figures from Phase 4b

## Output

- `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex` (new version, does NOT overwrite doc4a)
- `analysis_note/ANALYSIS_NOTE_doc4b_v1.pdf` (compiled)

## Procedure

1. **Stage new figures:** Copy Phase 4b figures into `analysis_note/figures/`,
   overwriting older versions of the same file. Phase 2/3 figures remain
   from Doc 4a staging — only the current phase's figures need updating.
   (If a regression changed earlier-phase figures, copy those too.)
   ```bash
   cp phase4_inference/4b_partial/outputs/figures/*.pdf analysis_note/figures/
   ```
2. **Copy** the latest Doc 4a AN as `ANALYSIS_NOTE_doc4b_v1.tex`
3. **Update results:** Replace `\tbd{10\% data}` and `\tbd{Doc 4b}`
   entries with real values from `results/*.json`
4. **Update figures:** Replace figure files with 10% data versions.
   For comparison plots, replace 10% placeholders with real data points.
5. **Add comparison discussion:** Expected-vs-10% comparison with chi2.
   Add to Results section.
6. **Update Change Log:** Add Doc 4b entry at the top.
7. **Numbers consistency lint:** Verify every number in the AN matches
   the latest JSON. Check per-section tables, summary tables, discussion
   prose, derived quantities — all must be consistent.
8. **Compile:** From `analysis_note/`, run
   `tectonic ANALYSIS_NOTE_doc4b_v1.tex`. Fix any errors.
9. **Verify:** All cross-references resolve, figures render, no overflow.

## What stays stable (~80%)

Introduction, Data samples, Event selection, Corrections methodology,
Systematic uncertainty descriptions, Statistical method, Cross-checks
(methodology), Future directions, Appendices (structure).

## What changes

- Results tables and figures (10% data replaces placeholders)
- Comparison section (expected-vs-10% added)
- Abstract (if interim results stated)
- Conclusions (updated for 10% observations)
- Change Log

## If restructuring is needed

If Phase 4b results require structural changes (new section, removed
measurement, changed primary configuration), you have full authority to
restructure. The Doc 4a skeleton is a starting point, not a constraint.
Write a cohesive document, not a patched one.

## Review

**5-bot+bib** → **HUMAN GATE.** Same rigor as Doc 4a. After the arbiter
returns PASS, the orchestrator presents the compiled PDF to the human.
The human reviews the PDF (not markdown, not artifacts).
