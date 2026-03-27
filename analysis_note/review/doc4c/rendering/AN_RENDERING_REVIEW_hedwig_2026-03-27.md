# Rendering Review: ANALYSIS_NOTE_doc4c_v2

**Reviewer:** Hedwig (rendering reviewer)
**Date:** 2026-03-27
**Document:** `analysis_note/ANALYSIS_NOTE_doc4c_v2.pdf` (48 pages)
**Source:** `analysis_note/ANALYSIS_NOTE_doc4c_v2.tex`

---

## Summary

The document compiles and renders cleanly. The 48-page PDF is well-structured
with a complete table of contents, bibliography (20 references), 45 figures,
29 tables, and 6 appendices. No broken cross-references ("??") or missing
citations ("[?]") are visible in the rendered output. No `\tbd{}` placeholders
remain. The abstract is quantitative. Figures are generally legible and
well-placed. The main issues are: (1) a large number of orphaned figures and
tables that are never referenced from the body text, (2) many orphaned
equations that are defined but never cited, (3) the reproduction contract
references the wrong filename, and (4) several figures in the appendix lack
body-text references, leaving readers no context for encountering them.

---

## Findings

### 1. Orphaned figures --- 31 figures without `\ref` in text

**(A) Must fix.**

The following 31 figure labels have no corresponding `Figure~\ref{fig:...}`
anywhere in the prose. A reader encountering these figures has no textual
context. Every figure must be introduced and discussed in the body before
it appears.

**Body figures (Category A --- these appear in the main analysis flow):**

| # | Label | Page | Description |
|---|-------|------|-------------|
| 1 | `fig:data-mc-p-theta` | 9 | Data/MC momentum and theta |
| 2 | `fig:data-mc-phi-pt` | 10 | Data/MC phi and pT |
| 3 | `fig:data-mc-thrust` | 10 | Data/MC thrust |
| 4 | `fig:data-mc-nch` | 11 | Data/MC charged multiplicity |
| 5 | `fig:binning` | 12 | Bin population and migration |
| 6 | `fig:correction-map` | 13 | Correction factor map |
| 7 | `fig:efficiency-diagonal` | 13 | Efficiency and diagonal fraction |
| 8 | `fig:split-closure` | 15 | Split-sample closure projections |
| 9 | `fig:bbb-vs-ibu` | 17 | BBB vs IBU comparison |
| 10 | `fig:response-matrix` | 18 | Response matrix and diagonal fraction |
| 11 | `fig:approach-comparison` | 22 | Approach A vs C comparison |
| 12 | `fig:ordering-comparison` | 23 | pT vs energy ordering |
| 13 | `fig:10pct-year-stability` | 24 | Per-year stability (10%) |
| 14 | `fig:full-1d` | 27 | 1D projections (full data) |
| 15 | `fig:full-cutflow` | 35 | Full-data cutflow |
| 16 | `fig:reco-gen-comparison` | 35 | Reco vs gen 1D distributions |
| 17 | `fig:correction-preview` | 36 | Correction factor preview |
| 18 | `fig:full-year-stability` | 36 | Per-year stability (full data) |
| 19 | `fig:full-vs-10pct` | 37 | Full vs 10% ratio map |
| 20 | `fig:lund-10pct` | 38 | 10% corrected Lund plane |
| 21 | `fig:10pct-1d` | 39 | 10% 1D projections |
| 22 | `fig:10pct-data-mc-reco` | 40 | 10% reco-level data/MC ratio |
| 23 | `fig:10pct-cutflow` | 42 | 10% cutflow comparison |

**Appendix figures (Category A --- appendix figures still need at least one
`\ref` from the body or appendix prose):**

| # | Label | Page | Description |
|---|-------|------|-------------|
| 24 | `fig:aux-1` | 47 | Log-scale momentum + reco Lund plane |
| 25 | `fig:self-closure` | 47 | Self-closure projections |
| 26 | `fig:self-closure-pulls` | 48 | Self-closure pull distribution |
| 27 | `fig:stress-2d` | 48 | Full-MC 2D correlated stress test |
| 28 | `fig:aux-closure-pulls` | 48 | Old closure pull distributions |
| 29 | `fig:aux-correlation` | 48 | Old correlation matrix |
| 30 | `fig:aux-syst` | 48 | Old systematic impact plots |
| 31 | `fig:aux-syst-old` | 48 | Old systematic breakdown |

**Root cause:** Many figures appear right after the discussion that motivates
them, but the prose uses descriptions like "The Lund plane shows..." without
a formal `Figure~\ref{fig:...}` callout. Each body figure needs a sentence
like "Figure~\ref{fig:X} shows..." before or after the float.

**Fix:** Add `Figure~\ref{fig:...}` references in the surrounding prose for
all 31 figures. For the 8 appendix figures, add introductory sentences in
Appendix D or cross-reference them from the relevant body section.

---

### 2. Orphaned tables --- 21 tables without `\ref` in text

**(A) Must fix.**

The following 21 table labels have no corresponding `Table~\ref{tbl:...}`
reference in the prose:

| # | Label | Page | Description |
|---|-------|------|-------------|
| 1 | `tbl:provenance` | 7 | Input provenance |
| 2 | `tbl:data` | 7 | ALEPH data samples |
| 3 | `tbl:mc` | 8 | MC sample |
| 4 | `tbl:track-cuts` | 8 | Track-level cuts |
| 5 | `tbl:event-cuts` | 8 | Event-level cuts |
| 6 | `tbl:lund-stats` | 11 | Lund plane construction stats |
| 7 | `tbl:correction-stats` | 12 | Correction factor stats |
| 8 | `tbl:stress` | 16 | Stress test results |
| 9 | `tbl:syst-summary` | 20 | Systematic uncertainty summary |
| 10 | `tbl:approach-comparison` | 21 | Approach A vs C |
| 11 | `tbl:full-summary` | 25 | Full data processing summary |
| 12 | `tbl:full-correction` | 26 | Full-data correction summary |
| 13 | `tbl:normalization` | 27 | Normalization verification |
| 14 | `tbl:full-chi2` | 30 | Full chi2 comparison |
| 15 | `tbl:full-pulls` | 30 | Full pull distribution |
| 16 | `tbl:10pct-summary` | 38 | 10% processing summary |
| 17 | `tbl:10pct-chi2` | 39 | 10% chi2 |
| 18 | `tbl:10pct-cutflow` | 41 | 10% cutflow |
| 19 | `tbl:10pct-reco-ratio` | 40 | 10% reco ratio |
| 20 | `tbl:gen-cutflow` | 46 | Generator-level cutflow |
| 21 | `tbl:limitation-index` | 46 | Limitation index |

**Root cause:** Same as figures --- tables appear near their discussion but
are not formally referenced with `Table~\ref{tbl:...}`.

**Fix:** Add `Table~\ref{tbl:...}` in the surrounding prose for each.

---

### 3. Orphaned equations --- 10 equations without `\ref` or `\eqref`

**(B) Should fix.**

The following equation labels are defined but never referenced:

| Label | Eq # | Content |
|-------|------|---------|
| `eq:rho-def` | (1) | Density definition |
| `eq:coords` | (2) | Lund coordinates (referenced via `\eqref`) |
| `eq:kt-dtheta` | (3) | Opening angle/kT (referenced via `\eqref`) |
| `eq:correction` | (4) | Correction factor definition |
| `eq:corrected-density` | (5) | Corrected density formula |
| `eq:efficiency` | (6) | Efficiency definition |
| `eq:stress-tilt` | (8) | Stress tilt formula |
| `eq:bootstrap-cov` | (9) | Bootstrap covariance |
| `eq:syst-cov` | (10) | Systematic covariance |
| `eq:chi2` | (11) | Chi-squared formula |

Note: `eq:coords` and `eq:kt-dtheta` ARE referenced via `\eqref{}` in the
Lund plane construction section, so only 8 are truly orphaned. The key
equations (Eq. 1, 4, 5, 6, 8, 9, 10, 11) define important quantities but
are never back-referenced. Adding `Eq.~\eqref{eq:...}` where these
quantities are used later would improve readability.

---

### 4. Reproduction contract references wrong filename

**(A) Must fix.** Page 47.

The reproduction contract (Appendix F) ends with:
```
cd analysis_note && tectonic ANALYSIS_NOTE_doc4c_v1.tex
```
This should be `ANALYSIS_NOTE_doc4c_v2.tex` since that is the current
(final) version of the document. A reader following the reproduction
contract would compile the wrong version.

**Source location:** Line 2877 of the `.tex` file.

---

### 5. Section 8.7.5 ("1D projections with 10% data") has no prose

**(A) Must fix.** Page 39.

The subsubsection heading "1D projections with 10% data" (Section 8.7.5)
is immediately followed by a figure with no introductory prose. The figure
appears without any textual context. Every section must have prose before
its first figure.

**Fix:** Add 1--2 sentences introducing the 10% 1D projections before the
figure environment.

---

### 6. Large whitespace gaps on pages 3, 15, 44

**(A) Must fix.**

- **Page 3:** The table of contents ends at roughly the middle of the page,
  leaving the bottom half blank. This is inherent to the `\clearpage` after
  the TOC but creates a large gap. Consider whether the Change Log could
  begin on the same page.
- **Page 15:** Approximately 1/3-page whitespace gap between
  Figure 8 (split-closure) and Figure 9 (closure pulls). LaTeX float
  placement is not optimal here.
- **Page 44:** Page 44 is almost entirely blank (only ~4 lines of text at
  the top, rest is whitespace before the bibliography). This is the end of
  Section 11 (Known Limitations).

**Fix:** Adjust float placement parameters or use `\clearpage` strategically
to reduce gaps. For page 44, consider moving the bibliography to start
immediately after the text.

---

### 7. Figure 45 (page 48): "Stress: ln_1_over_dtheta" in raw code font

**(A) Must fix.** Page 48, top right panel.

Figure 45 (full-MC stress tests) has a label in the upper right that reads
`Stress: ln_1_over_dtheta` in what appears to be raw code/variable-name
style rather than properly formatted math. This should read something like
"Stress: $\ln(1/\Delta\theta)$" to match the rest of the document. The
left panel similarly shows `Stress: ln_kt` which should be
"Stress: $\ln k_T$".

**Root cause:** The plotting script uses raw variable names as subplot
titles.

---

### 8. Figure 17 (page 24): "per_year" visible in experiment label

**(B) Should fix.** Page 24.

The per-year stability plots (Figure 17, 10% data) show experiment labels
that read `ALEPH Open Data (10%, per year)` with the `per year` text
slightly cutting off at the right edge. The font rendering is tight. Both
the left and right panels show `per_yea` truncation artifacts in the
`rlabel` region. Compare with Figure 35 (page 36) which has similar but
slightly cleaner labels.

---

### 9. Equation (13) on page 27 is unnumbered in the display but has no label

**(C) Suggestion.** Page 27.

The 1D projection definitions (integrals for $d\rho/d(\ln k_T)$ and
$d\rho/d(\ln 1/\Delta\theta)$) use a displayed equation that appears
numbered as (13) in the PDF but has no `\label{}`. This equation is not
referenced elsewhere. For consistency with the rest of the document
(where all displayed equations are numbered and most are referenced),
either add a label and reference it, or use `equation*` to suppress
the number.

---

### 10. Inconsistent number formatting

**(B) Should fix.** Multiple pages.

The document mostly uses `\,` for digit grouping (e.g., `3\,050\,610`),
which is correct. However, a few instances use `{,}` grouping instead
(e.g., line 59: `$2{,}846{,}194$`). While both render correctly, the
convention should be consistent. The `\,` form is used more frequently
and should be the standard.

Instances found with `{,}` grouping: abstract (lines 59--60), several
places in the change log, and some table entries. The body text
predominantly uses `\,`.

---

### 11. Figure caption quality

**(B) Should fix.** Multiple pages.

Most figure captions are excellent (2--5 sentences with interpretation).
However, a few captions in the appendix (Figures 42--45) are shorter
than the 2-sentence minimum recommended by the spec:

- Figure 44 (page 48): "Pull distribution for the self-closure test.
  All pulls are identically zero, confirming the algebraic identity of
  the bin-by-bin correction when applied to the same MC sample."
  --- This is exactly 2 sentences, which is acceptable.
- Figure 42 caption is 3 sentences. OK.

All body-text figure captions meet the 2+ sentence requirement. No
action needed.

---

### 12. Non-breaking space usage

**(C) Suggestion.** Throughout.

The document consistently uses `~` for non-breaking spaces before
references (e.g., `Table~\ref{...}`, `Figure~\ref{...}`,
`Section~\ref{...}`, `Eq.~\ref{...}`). This is correct and consistent.

The document also uses `$\sim\!$` for "approximately" throughout, which
is a reasonable convention. No issues found.

---

### 13. Math mode for variables in text

**(B) Should fix.** Page 8.

Table 5 (track-level cuts) has `pwflag == 0` in the "Criterion" column
rendered as `\texttt{pwflag == 0}`, which is appropriate for code. Table 6
similarly uses `\texttt{passesAll == True}`. These are correctly formatted.

However, the variable `passesAll` appears in running prose on pages 7--8
sometimes in `\texttt{}` and sometimes without formatting. A quick check
shows it is consistently in `\texttt{}`, so no issue.

No bare physics variables found outside math mode.

---

### 14. TOC accuracy

**(B) Should fix.**

The table of contents lists Appendix E "Limitation Index" and Appendix F
"Reproduction Contract" both on page 47. In the actual PDF:
- Appendix E (Limitation Index) content is on page 46--47 (table with
  the limitation registry)
- Appendix F (Reproduction Contract) starts on page 47

The TOC page numbers appear consistent with the actual content locations
(the TOC points to the section heading, which is on the listed page).
No discrepancy found.

---

### 15. Page count

The document is 48 pages (including title page, TOC, change log,
bibliography, and appendices). The body text (Sections 1--11) spans
approximately pages 6--44, which is ~38 pages of content. With
appendices, the total is 48 pages. This is slightly below the 50-page
target but above the 30-page Category A threshold. Acceptable.

---

### 16. Appendix E (Limitation Index): heading with no introductory prose

**(A) Must fix.** Page 47.

Appendix E "Limitation Index" consists of just a section heading
immediately followed by a table. There is no introductory sentence.
Every section (including appendix sections) should have at least one
sentence of prose before any table or figure.

**Fix:** Add an introductory sentence, e.g., "Table~\ref{tbl:limitation-index}
provides the complete registry of constraints, limitations, and decisions
from the analysis strategy."

---

## Classification Summary

| Category | Count | Description |
|----------|-------|-------------|
| **(A) Must fix** | 6 | Orphaned figures (31), orphaned tables (21), reproduction contract filename, empty section prose (2 instances), whitespace gaps, raw code in figure title |
| **(B) Should fix** | 4 | Orphaned equations (8), figure label truncation, number formatting consistency, TOC accuracy (minor) |
| **(C) Suggestion** | 2 | Unnumbered equation, non-breaking space note |

**Verdict: ITERATE.** The 31 orphaned figures and 21 orphaned tables are a
pervasive rendering defect --- a journal referee would immediately flag the
lack of formal cross-references. Adding `Figure~\ref{}` and `Table~\ref{}`
callouts throughout the prose is the primary fix needed. The reproduction
contract filename and the two sections with no prose before figures are
also Category A. The core document quality (figures, typography, physics
content, equation rendering) is otherwise excellent.
