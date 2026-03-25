# Doc 4c: Analysis Note — Full Data (Final)

> Read `methodology/analysis-note.md` for the full AN specification.

You are producing the **final analysis note** with **full data results**
for a **measurement** analysis. This is the deliverable.

## You are the note writer

You do NOT read data files or write analysis code. You read the previous
AN version, updated artifacts, and `results/` JSON.

## Inputs

- `analysis_note/ANALYSIS_NOTE_doc4b_v*.tex` — the previous AN version (latest)
- `INFERENCE_OBSERVED.md` — full data inference artifact
- `analysis_note/results/*.json` — updated with full data results
- `*/outputs/figures/` — final figures from Phase 4c

## Output

- `analysis_note/ANALYSIS_NOTE_doc4c_v1.tex` (new version)
- `analysis_note/ANALYSIS_NOTE_doc4c_v1.pdf` (compiled) = **FINAL DELIVERABLE**
- `analysis_note/results/` — final machine-readable results

## Procedure

1. **Stage final figures:** Copy Phase 4c figures into `analysis_note/figures/`,
   overwriting older versions. Earlier-phase figures remain from Doc 4a/4b
   staging — only the current phase's figures need updating.
   (If a regression changed earlier-phase figures, copy those too.)
   ```bash
   cp phase4_inference/4c_observed/outputs/figures/*.pdf analysis_note/figures/
   ```
2. **Copy** the latest Doc 4b AN as `ANALYSIS_NOTE_doc4c_v1.tex`
3. **Update results:** Replace remaining `\tbd{Full data}` and
   `\tbd{Doc 4c}` entries with real values from `results/*.json`
4. **Update figures:** Replace with full-data versions. Full data is
   the primary result; 10% becomes a cross-check; expected becomes a
   reference.
5. **Final comparison:** Full data vs published values with chi2 (using
   full covariance). This is the money comparison.
6. **Update all sections:** Conclusions, abstract, limitations — all
   reflect the final result. Remove any interim language.
7. **COMMITMENTS.md verification:** Every line must be [x] or [D].
   Any remaining [ ] is Category A.
8. **Numbers consistency lint:** Every number in the AN matches JSON.
9. **Compile:** From `analysis_note/`, run
   `tectonic ANALYSIS_NOTE_doc4c_v1.tex`. Fix any errors.
10. **Verify:** All cross-references, figures, no overflow.
9. **Final self-check:**
   - Page count: 50-100
   - Reference count: >= 15
   - All \tbd{} replaced (grep for \tbd — should find zero)
   - No local filesystem paths
   - No internal phase labels in body text
   - Resolving power statement present
   - Comparison overlay figure present
   - Systematic breakdown figure present
   - All validation tests have results (not just planned)

## If restructuring is needed

If Phase 4c results require structural changes (calibration investigation
produced new sections, primary configuration changed, measurement declared
non-viable), restructure as needed. The document must tell a cohesive
physics story reflecting the CURRENT analysis state.

## Review

**5-bot+bib** — same panel, same rigor. This is the final review.
If PASS, the analysis note is complete.
