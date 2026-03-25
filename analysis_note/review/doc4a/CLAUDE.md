# Doc 4a: Analysis Note — Expected Results

> Read `methodology/analysis-note.md` for the full AN specification.
> Read `methodology/appendix-plotting.md` for figure standards and compositing.
> Read `methodology/appendix-checklist.md` for the completeness checklist.

You are writing the **complete analysis note** for a **measurement**
analysis using **expected results only** (from Phase 4a).

This is the heavy lift — you are establishing the full document structure,
figure compositing, and rendering quality. Doc 4b/4c will evolve this
document by updating results, not rebuilding it.

## You are the note writer

You do NOT read data files or write analysis code. You read phase
artifacts and `results/` JSON, then write LaTeX prose. You CAN produce
or delegate methodology diagrams (correction chains, analysis flow, etc.).

## Inputs

- All phase artifacts: `STRATEGY.md`, `EXPLORATION.md`, `SELECTION.md`,
  `INFERENCE_EXPECTED.md`
- `analysis_note/results/*.json` — single source of truth for ALL numbers
- `*/outputs/figures/` — all figures from Phases 2-4a
- `conventions/` files — for completeness checks
- `experiment_log.md`
- `COMMITMENTS.md` — verify coverage
- `conventions/an_template.tex` — the LaTeX starting template

## Output

- `analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`
- `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf` (compiled)

## Procedure

### 1. Plan (before writing any LaTeX)

Produce a plan covering:
- Section structure (all 13 required sections)
- Which figures go in which sections (inventory ALL figures from phases)
- Which results tables are needed
- Which systematic sources get their own subsections
- Which figures should be composed (side-by-side, grids)
- Flagship figures (from COMMITMENTS.md) — these go in Results/Comparison
- Missing figures that need to be produced (methodology diagrams, etc.)

### 2. Stage figures

Before writing any LaTeX, copy all figures from phase directories into
`analysis_note/figures/` so LaTeX `\includegraphics{figures/name.pdf}`
resolves correctly:

```bash
mkdir -p analysis_note/figures
cp phase*/outputs/figures/*.pdf analysis_note/figures/ 2>/dev/null
cp phase*/*/outputs/figures/*.pdf analysis_note/figures/ 2>/dev/null
```

If two phases produce a figure with the same name (e.g., Phase 2 and
Phase 4a both have `thrust_data_mc.pdf`), keep the later phase's version
(it supersedes the earlier one).

### 3. Copy template and write

Start from `conventions/an_template.tex`. Copy it to
`analysis_note/ANALYSIS_NOTE_doc4a_v1.tex`. Write each section in order.
**Compile after writing each major section:**

```bash
cd analysis_note && tectonic ANALYSIS_NOTE_doc4a_v1.tex
```

Always compile from the `analysis_note/` directory so relative paths
(`../conventions/preamble.tex`, `../references.bib`, `figures/`) resolve
correctly.

Fix any LaTeX errors immediately — you have the full document in context.

### 4. Numbers from JSON only

Every number in the AN must come from `results/*.json`. Do NOT transcribe
from prose artifacts. When quoting a result, trace it: "this comes from
results/parameters.json, field mz.value."

### 5. Figure compositing

Compose related figures in LaTeX using `\includegraphics` patterns from
the template. Sizing reference:

| Grid | Per-panel size | Use case |
|------|---------------|----------|
| 1x2 pair | `height=0.38\linewidth` | Projection comparisons |
| 2x2 | `height=0.32\linewidth` | Sub-dominant systematics |
| 3-column | `width=0.32\linewidth` | Data/MC surveys |
| Standalone | `height=0.45\linewidth` (default) | Flagship, complex |

Mandatory composites: per-variable surveys (3-column), per-systematic
shifts, per-cut comparisons, nominal + uncertainty pairs. Standalone:
flagship figures, figures with colorbars, figures with >3 legend entries.

### 6. Placeholder conventions

**Tables:** Use `\tbd{description}` for future-phase values:
```latex
$M_Z$ [GeV] & $91.187 \pm 0.004$ & \tbd{10\% data} & \tbd{Full data} \\
```

**Comparison plots:** For measurement-vs-theory/reference comparison
figures, include greyed-out placeholder entries for 10% and full data
where meaningful. NOT all figures — data/MC distributions, systematic
impact plots, closure tests show only current-stage data.

### 7. Self-check before submitting

Count and report these metrics:
1. Total display equations (`\begin{equation}`): target >= 8
2. Total figures referenced: target >= 20
3. Total tables: target >= 5
4. Systematic subsections: must equal sources in budget table
5. Comparison statements with chi2/pull: grep for "consistent" — each
   needs a number in the same paragraph
6. Word count of Corrections section: target >= 500
7. Word count per systematic subsection: target >= 100 each
8. Page count of compiled PDF: target 50-100, under 30 is Category A
9. Reference count: target >= 15 unique citations

### 8. Compile final PDF

From `analysis_note/`, run `tectonic ANALYSIS_NOTE_doc4a_v1.tex` and verify:
- All figures render (no broken placeholders)
- No content overflow
- Cross-references resolve (no "??")
- Citations resolve (no "[?]")
- TOC page numbers match actual pages

## LaTeX conventions

- Cross-references: `\label{fig:name}` / `Figure~\ref{fig:name}`
- Citations: `\cite{key}` with `../references.bib` (path from analysis_note/)
- Math: `$...$` inline, `\begin{equation}...\end{equation}` display
- Use `\mathrm{}` for operator names in equations (e.g., `\mathrm{d}\sigma`)
- Captions: 2-5 sentences, `<What> (<where>) <description/conclusion>`
- No empty sections: every `\section`/`\subsection` has prose before figures

## Quality standards

- **50-100 pages.** Under 30 is Category A.
- Every cut needs a distribution plot
- Every systematic needs an impact figure
- Every cross-check needs a comparison plot
- Every result has context (comparison, interpretation, resolving power)
- The completeness test: a physicist unfamiliar with this analysis can
  reproduce every number from the AN alone

## Review

**5-bot+bib** — physics + critical + constructive + plot validator +
rendering + bibtex → arbiter. This is the heaviest review — it validates
the full AN structure, rendering quality, physics content, and citations.
