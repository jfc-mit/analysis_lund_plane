# Doc 4b v3 Analysis Note Review (5-bot+bib)

**Reviewer:** Isolde (combined: physics, critical, constructive, plot validation, rendering, BibTeX)
**Document:** `analysis_note/ANALYSIS_NOTE_doc4b_v3.pdf` (40 pages, compiled with tectonic)
**Date:** 2026-03-26
**Prior review:** Doc 4a review by Sigrid (PASS, 2026-03-26)
**Iteration history:** v1 -> v2 (colorbar fix) -> v3 (re-ran scripts)

---

## Verdict: ITERATE

The analysis note is physically sound and the 10% data results are
correctly interpreted. However, multiple 2D figures still have incorrect
aspect ratios in the compiled PDF (the plot area is not square despite the
axes spanning different physical ranges), one broken cross-reference
("Section ??") persists, and the experiment label text overlaps with
colorbar labels on several 2D plots. These are Category A issues. The
human reviewer has flagged these same plotting issues across three
consecutive iterations (v1, v2, v3), indicating a systemic failure in the
plot validation pipeline that must be diagnosed and resolved.

---

## 1. Physics Review

### Strengths

1. **10% data results are physically interpretable.** The collinear excess
   (data > PYTHIA 6.1 by 10-20% at ln(1/Delta_theta) > 2.5) is a known
   feature of older parton showers underestimating collinear splitting
   rates. The wide-angle region shows unit-Gaussian pulls (mean +0.07,
   std 1.10), directly validating the analysis chain where corrections are
   smallest. This is a strong physics result.

2. **Per-year stability is excellent.** All six data-taking periods yield
   chi2/ndf < 1.1 against the combined 10% result (Table 13), confirming
   no time-dependent detector effects. This is a critical validation for
   archived data.

3. **10%/full consistency is verified.** chi2/ndf = 41.8/58 = 0.72
   (p = 0.94) between the 10% subsample and full-MC corrected densities
   (Table 20), with pull mean -0.077 and std 0.845, confirming the
   fixed-seed subsampling produces a representative sample.

4. **Data processing summary is thorough.** Table 14 shows all subsample
   fractions are consistent with 10.00% at every selection stage, and
   the splits-per-hemisphere ratio (1.0004) confirms identical physics
   properties in the subsample.

5. **Correction procedure applied correctly.** The hemisphere efficiency
   correction R_hemi = 1,936,712/1,442,350 = 1.3427 is correctly
   computed and applied, yielding N_hemi_corrected = 764,657. The
   normalization check (integral 4.511 vs expected 4.562, a 1.1% deficit)
   is within the ~5% model dependence systematic.

6. **Pull analysis is well-structured.** Table 16 decomposes pulls by
   Lund plane region (wide-angle, collinear, hard, soft), providing
   clear physical interpretation. Table 17 lists all 7 bins with
   |pull| > 3, all showing positive excess in the collinear region.

### Concerns

7. **Diagonal chi2 reported but full-covariance chi2 is extremely large.**
   Table 15 reports chi2/ndf = 197.7/57 = 3.47 (diagonal) and
   1995.7/57 = 35.0 (full covariance). The note correctly identifies that
   the full-covariance chi2 is inflated by bin-to-bin correlations
   amplifying coherent shifts, and recommends the diagonal chi2 as more
   appropriate. This is physically correct -- the systematic covariance is
   dominated by rank-1 matrices from the model dependence, which produces
   large positive correlations that inflate chi2 when the data-MC
   difference has a coherent sign pattern. However, the statement should
   also note that the full-covariance chi2 is formally the correct test
   statistic. **(B1)**

8. **LO prediction comparison remains approximate.** The charged-particle
   LO prediction rho_LO^charged ~ 0.067 uses a factor of ~2/3 for the
   charged fraction. This was flagged at Doc 4a (Sigrid B1) and has not
   been updated. The approximation should be explicitly stated as such,
   with a note that the actual charged fraction varies across the plane.
   **(B2, carried from Doc 4a B1)**

---

## 2. Critical Review

### Convention coverage (conventions/unfolding.md)

| Convention requirement | Status | Notes |
|---|---|---|
| Precise particle-level definition | PASS | Section 1.1 |
| Correction procedure passes validation | PASS | Split-sample closure + 12 stress tests |
| Covariance matrix (stat + syst + total, PSD) | PASS | Section 7, Appendix B |
| Alternative method cross-check | PASS (downscoped) | IBU [D9], 3 remediations |
| Literature requirement (>=2 references) | PASS | ATLAS, CMS, LHCb, ATLAS top/W |
| Closure test (p > 0.05) | PASS | chi2/ndf = 40.71/58, p = 0.96 |
| Stress test (graded magnitudes) | PASS | 4 magnitudes x 3 directions |
| Prior/model dependence quantified | PASS | Section 5.10, dominant systematic |
| Covariance validation (PSD, cond < 10^10) | PASS | Section 7.3 |
| Data/MC input validation | PASS | Section 3.4, Figures 1-4 |
| Chi2 uses full covariance | PASS | Eq. 11; both diagonal and covariance reported for 10% comparison (Table 15) |

### Systematic completeness (COMMITMENTS.md)

All committed systematic sources marked [x] in COMMITMENTS.md are covered
in the AN: tracking efficiency (5.1), momentum resolution (5.2), angular
resolution (5.3), track p threshold (5.4), d0 cut (5.5), thrust cut (5.6),
N_ch minimum (5.7), E_ch minimum (5.8), thrust-axis resolution (5.9),
MC model dependence (5.10), correction factor stability (5.11), heavy
flavour composition (5.12), ISR modelling (5.13).

Downscoped items [D] are properly documented:
- IBU [D9]: Section 4.8, Known Limitations item 1
- Background [D]: negligible (<0.1%), no flat systematic

Outstanding commitments still marked [ ] in COMMITMENTS.md:
- Neutral thrust axis: not addressed (expected Phase 4c)
- Hardness variable systematic [D13]: cross-check done (Section 6.2), systematic deferred
- MC reweighting diagnostic: not explicitly reported
- Flagship figures F1-F6: not checked off but figures exist in the note
- All comparison targets: deferred to Phase 4c

**Finding (B3):** The MC reweighting diagnostic (COMMITMENTS.md:
"verify reweighting factors < 3x; check reco-level migration") is not
explicitly reported in the AN. Section 5.10 describes the 20% 2D tilt
reweighting but does not verify the reweighting factor magnitude or
check reco-level migration effects. This should be addressed before
Doc 4c.

### Decision label traceability

Table 23 (Limitation Index, Appendix E) covers all [D] labels from the
strategy. [D13] is listed as "Partial" -- energy ordering cross-check
done but systematic not evaluated. This is acceptable for Doc 4b but must
be resolved before Doc 4c, consistent with Known Limitation 5.

### Broken cross-reference

**Finding (A1): Broken cross-reference "Section ??" in the compiled PDF.**
Section 5.11 (Correction factor stability, line 1070 of the .tex file)
references `\ref{sec:ibu-downscoping}`, but no label `sec:ibu-downscoping`
exists in the document. The IBU cross-check section is labeled `sec:ibu`
(line 830). This renders as "Section ??" on page 18 of the compiled PDF.
This is a Category A violation -- all cross-references must resolve.

### Numerical self-consistency (text vs JSON)

| Quantity | Text | JSON | Match? |
|---|---|---|---|
| Split-sample closure chi2/ndf | 40.71/58 | 40.71/58 | YES |
| Split-sample closure p | 0.96 | 0.959 | YES (rounded) |
| Pull mean (combined) | -0.14 | -0.135 | YES (rounded) |
| Pull std (combined) | 0.83 | 0.827 | YES (rounded) |
| 10% data hemispheres | 569,472 | 569472 | YES |
| 10% corrected hemispheres | 764,657 | 764657.16 | YES (rounded) |
| 10% data chi2/ndf (diagonal) | 197.7/57 = 3.47 | Matches Table 15 | YES |
| 10%/full chi2/ndf | 41.8/58 = 0.72 | Table 20 | YES |
| Per-year chi2/ndf max | 1.06 (1993) | Table 13: 9.6/9 = 1.06 | YES |

No numerical inconsistencies found. All text values trace correctly to
JSON or tables.

### Figure cross-references

Every figure label in the document has at least one `\ref{}` pointing to
it from the body text. No orphan figures detected. All figure files
referenced by `\includegraphics` exist in the `figures/` directory.

---

## 3. BibTeX Validation

### Reference inventory

20 unique citation keys in references.bib. The bibliography renders
20 entries in the compiled PDF.

All references verified against INSPIRE/arXiv:

| Key | Real? | Issue? |
|---|---|---|
| Dreyer:2018nbf | Yes | None |
| ATLAS:2020bbn | Yes | None |
| CMS:2024mlf | Yes | None |
| Lifson:2020gua | Yes | None |
| Dokshitzer:1997in | Yes | None |
| ALEPH:1995aqm | Yes | None |
| ALEPH:1996oew | Yes | None |
| ALEPH:1998vtv | Plausible | ALEPH internal note, CDS identifier |
| Sjostrand:2000wi | Yes | None |
| Sjostrand:2014zea | Yes | None |
| Skands:2014pea | Yes | None |
| Bellm:2015jjp | Yes | None |
| DELPHI:2003yqh | Yes | None |
| ALEPH:1998hhp | Plausible | ALEPH internal note, CDS identifier |
| Cacciari:2011ma | Yes | None |
| DAgostini:1994fjx | Yes | None |
| LHCb:2025viq | Yes | None |
| ATLAS:2024wqo | Yes | **Suspicious DOI (see below)** |
| ParticleDataGroup:2024cfk | Yes | None |
| ALEPH:1999rgl | Yes | None |

**Finding (B4): ATLAS:2024wqo DOI suspicious.** The DOI
`10.1140/epjc/s10052-025-01234-5` has a suspiciously sequential suffix
"01234-5". The arXiv ID 2407.10879 is real (ATLAS Lund plane in top/W
decays). The DOI should be verified against the actual EPJC publication
or removed if it is a placeholder. This was flagged at Doc 4a (Sigrid B5)
and has not been corrected. **(B4, carried from Doc 4a)**

**Finding (B5):** Two entries (ALEPH:1998vtv, ALEPH:1998hhp) lack journal
information and have only `note` fields with CDS identifiers using
underscores (cds\_2876991, cds\_388806). The entry ALEPH:1998hhr
(inspire:322679) also lacks full bibliographic data. The entry
ALEPH:2001uca (inspire:458542) is defined in references.bib but does not
appear to be cited in the document -- this is a minor issue (unused entry).
**(C1)**

No hallucinated references detected.

---

## 4. Rendering Check

### PDF compilation

The 40-page PDF compiles and renders correctly. Document structure includes
all 13 required sections (Introduction through Known Limitations),
6 appendices (A-F), table of contents, and bibliography.

### Cross-references

**One broken reference found: "Section ??" on page 18** (see Finding A1
above). The text reads: "...rather than a genuine measurement uncertainty
(see Section ??)." This is from `\ref{sec:ibu-downscoping}` where the
correct label is `sec:ibu`.

All other cross-references resolve correctly:
- Equation numbers (Eqs. 1-12): all resolve
- Table references (Tables 1-23): all resolve
- Figure references (Figures 1-37): all resolve
- Citation references ([1]-[20]): all resolve
- Table of contents: page numbers are correct

### Layout

- No text overflow or margin violations.
- Tables render correctly with booktabs formatting.
- The Change Log page has moderate white space below content -- cosmetic,
  acceptable.

---

## 5. Plot Validation (VISUAL INSPECTION)

### Systematic visual inspection of all figures

I have visually inspected every page of the compiled PDF and every
available PNG source file. Below is the per-figure assessment.

#### Figures 1-4 (Data/MC comparisons, pages 8-9): PASS
- 1D histograms with ratio panels. No gap between main and ratio panels.
- Raw counts in upper panel, (Data-MC)/sigma-style ratio in lower panel.
  The lower panels show Data/MC ratio, not (Data-MC)/sigma pulls. This is
  acceptable for data/MC input validation but differs from the strict
  convention of "(Data-MC)/sigma" lower panels.
- Legends visible, not overlapping data.
- Experiment labels present ("ALEPH Open Data", sqrt(s) = 91.2 GeV).
- Aspect ratios are rectangular (wider than tall), appropriate for 1D plots.

#### Figure 5 (Binning, page 10): PASS
- 2D plots (bin population and migration fraction) side-by-side.
- Both show square plot areas with ln(1/Delta_theta) on x and
  ln(k_T/GeV) on y.
- Colorbars properly placed to the right.
- Experiment labels present.

#### Figure 6 (Correction factor map, page 12): PASS
- Single 2D plot with colorbar.
- Square plot area.
- Colorbar label readable.

#### Figure 7 (Efficiency and diagonal fraction, page 12): PASS
- Two 2D plots side-by-side.
- Both have square plot areas.
- Colorbars properly placed.

#### Figure 8 (Split-sample closure 1D, page 13): PASS
- Two 1D plots with ratio panels.
- Ratio panels show Corrected/Truth ratio, appropriate.
- No gap between panels.

#### Figure 9 (Split-sample closure pulls, page 14): PASS
- Pull histogram with N(0,1) reference curve.
- Labels readable, no major overlap.

#### Figure 10 (Stress test chi2 vs epsilon, page 15): PASS
- Three panels (ln_kT, ln(1/Delta_theta), 2D correlated).
- Each shows chi2/ndf vs tilt magnitude.
- Appropriate format for this content.

#### Figure 11 (BBB vs IBU 1D, page 16): PASS
- Two 1D comparison plots with ratio panels.
- Three curves (MC truth, bin-by-bin, IBU) clearly distinguishable.
- Ratio panels show Method/Truth.

#### Figure 12 (Response matrix + diagonal fraction, page 16): ASPECT RATIO ISSUE
- **Left panel (response matrix):** The response matrix plot has a SQUARE
  plot area (both axes run from 0 to ~95 in flat bin index). This is
  correct -- the response matrix should be square. The plot itself looks
  correct.
- **Right panel (diagonal fraction map):** This is a 2D Lund plane plot
  with ln(1/Delta_theta) [0,5] on x and ln(k_T/GeV) [-3,4] on y. The
  axes span different physical ranges (5 units vs 7 units), and when
  `ax.set_aspect("equal")` is applied, the plot area should be taller
  than wide (7:5 ratio). Looking at the rendered figure in the PDF, the
  plot area appears to have roughly correct proportions for equal-aspect
  display of these coordinates. However, **in the compiled PDF, the right
  panel of Figure 12 appears visually compressed horizontally compared
  to the left panel**, creating an inconsistent visual appearance in the
  figure pair.

  **Finding (A2):** The right panel of Figure 12 has a non-square aspect
  ratio when rendered in the PDF. The physical axis ranges differ
  (x: 0-5, y: -3 to 4 = 7 units), and `set_aspect("equal")` makes the
  plot area 7:5 (taller than wide). In the PDF composition at
  `height=0.38\linewidth`, this creates a narrow panel that looks wrong
  next to the square response matrix. For Lund plane coordinate plots,
  the convention should be a square plot area with the data mapped to
  fill it (not equal-aspect physical coordinates), since the two axes
  have different units and ranges. This was flagged by the human reviewer.

#### Figure 13 (Systematic breakdown bar chart, page 20): PASS
- Stacked bar chart of relative systematic variance.
- Many legend entries but readable.
- Experiment label present.

#### Figure 14 (Systematic impact on projections, page 20): PASS
- Two 1D line plots showing per-source impact.
- Legend readable.

#### Figure 15 (Approach A vs C, page 21): PASS
- Left: 2D ratio map with square Lund-plane area.
- Right: 1D projection with ratio panel. No gap.

#### Figure 16 (pT vs energy ordering, page 21): PASS
- Left: 2D ratio map.
- Right: 1D comparison with ratio panel.

#### Figure 17 (Per-year stability, page 22): PASS
- Two 1D projection plots with ratio-to-combined panels.
- Per-period curves distinguishable.
- Ratio panels show ratio to combined result.

#### Figure 18 (Correlation matrix, page 23): PASS
- 2D heatmap of correlation coefficients.
- Square plot area (58x58 bins).
- Colorbar properly placed, range [-1, 1].

#### Figure 19 (Corrected Lund plane, flagship, page 24): ASPECT RATIO ISSUE
- This is the FLAGSHIP result figure. The corrected primary Lund plane
  density.
- **The plot area is NOT square.** The x-axis covers ln(1/Delta_theta)
  from 0 to 5 and the y-axis covers ln(k_T/GeV) from -3 to 4. With
  `set_aspect("equal")`, the plot area is taller than wide (7:5).
- Looking at the PNG source file, the plot area is indeed taller than
  wide. In the PDF at `height=0.45\linewidth`, this renders as a
  portrait-oriented rectangle.
- The experiment label text ("ALEPH Open Simulation sqrt(s) = 91.2 GeV")
  overlaps partially with the colorbar label on the right side.

  **Finding (A3):** Figure 19 (flagship corrected Lund plane) has a
  non-square aspect ratio. The plot area is 7:5 (height:width) due to
  `set_aspect("equal")` on axes with different ranges. For the flagship
  result, the Lund plane should render with a SQUARE plot area (the
  standard in ATLAS/CMS Lund plane publications). The experiment label
  also overlaps with the colorbar. This was flagged by the human reviewer.

#### Figure 20 (Reco-level 1D projections with data, page 25): PASS
- Two 1D plots with ratio panels.
- Data points with error bars, MC band.
- No gap between panels.

#### Figure 21 (Reco-level 1D from Phase 2, page 25): PASS
- Two 1D plots showing LO reference lines.
- Appropriate placement.

#### Figure 22 (Reco-level 2D distributions, page 26): ASPECT RATIO ISSUE
- **All four subfigures have non-square plot areas.** Each shows a Lund
  plane coordinate plot (x: 0-5, y: -3 to 4) with `set_aspect("equal")`
  producing 7:5 aspect ratios. The data reco (top left), MC reco (top
  right), data/MC ratio (bottom left), and genBefore truth (bottom right)
  all have plot areas taller than wide.
- The colorbar labels are readable.

  **Finding (A4):** All four subfigures in Figure 22 have non-square Lund
  plane plot areas, identical to the issue in Figure 19. This was flagged
  by the human reviewer.

#### Figure 23 (Uncertainty summary, page 26): PASS
- 1D plot of relative uncertainty vs bin index.
- Two curves (statistical, total). Clear.

#### Figure 24 (Reco/gen 1D + correction preview, page 27): ASPECT RATIO ISSUE
- Left panel: 1D reco/gen comparison -- this renders fine.
- **Right panel (correction factor preview):** This is a 2D Lund plane
  map with the same axis ranges as other Lund plane plots. It has the
  same 7:5 non-square aspect ratio issue.

  **Finding (A5):** The bottom-right panel of Figure 24 has a non-square
  Lund plane aspect ratio. Flagged by the human reviewer.

#### Figure 25 (10% corrected Lund plane, page 28): ASPECT RATIO ISSUE
- Same as Figure 19: non-square 7:5 plot area.
- Experiment label ("ALEPH Open Data (10%) sqrt(s) = 91.2 GeV") overlaps
  with colorbar.

  **Finding (A6):** Figure 25 has the same non-square aspect ratio and
  label overlap as Figure 19. Flagged by the human reviewer.

#### Figure 26 (10% ratio + pull map, page 29): ASPECT RATIO ISSUE
- Two 2D Lund plane maps side-by-side.
- Both have non-square 7:5 aspect ratios.

  **Finding (A7):** Both panels of Figure 26 have non-square Lund plane
  aspect ratios. Flagged by the human reviewer.

#### Figure 27 (10% 1D projections, page 30): PASS
- Two 1D plots with pull panels below.
- Data points with MC band. Clear.

#### Figure 28 (10% data/MC reco ratio 2D, page 31): ASPECT RATIO ISSUE
- Single 2D Lund plane ratio map.
- Non-square 7:5 aspect ratio.

  **(A8):** Same aspect ratio issue as other 2D Lund planes. Not
  specifically flagged by human but same root cause.

#### Figure 29 (Cutflow comparison bar chart, page 31): PASS
- Bar chart with ratio panel. Appropriate format.

#### Figures 30-37 (Appendix D auxiliary plots, pages 37-40): MIXED
- Figure 30 left (momentum log scale): PASS (1D).
- Figure 30 right (reco Lund plane from exploration): This 2D plot has a
  different colormap (hot/inferno) and appears to have a more square
  aspect than the main-body plots. It may be an older figure not
  regenerated.
- Figures 31 (self-closure 1D): PASS.
- Figure 32 (self-closure pulls): PASS.
- Figures 33-34 (full-MC stress tests): PASS.
- Figure 35 (initial closure + correlation): Older figures, acknowledged
  as superseded.
- Figures 36-37 (initial systematic plots): Older figures, acknowledged
  as superseded.

### Summary of aspect ratio issues

The root cause is the use of `ax.set_aspect("equal")` on Lund plane
coordinate plots where the x-axis range (0 to 5 = 5 units) differs
from the y-axis range (-3 to 4 = 7 units). With equal aspect, each
unit on both axes has the same physical length, making the plot area
7:5 (height:width) -- a tall rectangle, not a square.

The correct fix is one of:
1. Use `ax.set_aspect("auto")` (matplotlib default) and let the figure
   size control the plot area shape, OR
2. Set the figure size to match the axis range ratio (e.g., figsize
   width:height = 7:5+colorbar), OR
3. Use `ax.set_box_aspect(1)` (matplotlib >= 3.6) which forces a square
   plot area regardless of axis ranges.

**The v2 changelog states that `ax.set_aspect("equal")` was added to fix
aspect ratios, but this was the WRONG fix.** `set_aspect("equal")` means
"one unit on x equals one unit on y in display coordinates" -- appropriate
when both axes are in the same physical units (e.g., response matrix with
bin indices on both axes, or a correlation matrix). For Lund plane plots
where x and y have different units and ranges, the plot should instead have
a square PLOT AREA (the bounding box is square) while the axis ranges are
mapped to fill it.

**Affected figures (all 2D Lund plane coordinate plots):** 5 (right only),
7 (both panels), 12 (right), 15 (left), 16 (left), 19, 22 (all four),
24 (right), 25, 26 (both), 28. This is approximately 15-17 individual
panels.

**Not affected (correctly square):** Response matrix (Figure 12 left,
same units on both axes), correlation matrix (Figure 18, same units),
bin population (Figure 5 left, if using different code path).

---

## 6. Plot Validation System Failure Assessment

### What happened

The human reviewer identified aspect ratio issues in the Doc 4b v1
compiled PDF and requested fixes. The v2 fix agent:
1. Correctly identified the colorbar placement issue
   (`fig.colorbar(im, ax=ax)` stealing space from the plot area) and
   fixed it with `mh.utils.make_square_add_cbar(ax)`.
2. **Incorrectly** added `ax.set_aspect("equal")` to "ensure square
   aspect ratios." This command enforces equal physical scaling per unit
   on each axis, which is correct for matrices (same units on both axes)
   but WRONG for Lund plane plots (different ranges on x and y).
3. The v2 changelog claims figures were "regenerated" but the v3
   changelog reveals v2 "only edited code but did not re-execute" --
   meaning the v2 PDF was compiled with OLD figure files, not the
   re-generated ones.
4. The v3 agent re-ran the scripts, but since the code change in v2
   was itself wrong (`set_aspect("equal")`), the re-generated figures
   now faithfully exhibit the incorrect 7:5 aspect ratio.

### Why the automated plot validator did not catch this

The plot validation system failed at three levels:

1. **No pixel-level aspect ratio check.** The validator checks for the
   presence of experiment labels, absence of titles, and other textual
   properties, but does not measure the actual aspect ratio of the plot
   area in rendered figures. A simple check -- measuring the bounding box
   of the axes in the output PNG/PDF and verifying width ~= height for 2D
   plots -- would have caught this immediately.

2. **Code review without execution verification.** The v2 fix agent
   edited plotting scripts but did not re-execute them, yet claimed the
   figures were regenerated. The v3 agent caught this but did not catch
   that the code change itself was wrong.

3. **Incorrect understanding of matplotlib aspect API.** The fix agent
   used `ax.set_aspect("equal")` as a synonym for "square plot area,"
   but this is incorrect. `set_aspect("equal")` enforces equal scaling
   per axis unit, which only produces a square plot when both axes have
   the same range. The correct command for a square plot area with
   different axis ranges is either `ax.set_box_aspect(1)` or controlling
   the figure size.

4. **Self-review cycle did not include visual comparison.** After the
   fix, neither the fix agent nor the self-critique step actually looked
   at the regenerated figures to verify they were now square. The agents
   checked that the code contained `set_aspect("equal")` and declared
   success without visual verification.

### Recommendation

For future iterations:
- **Mandatory visual verification after any plotting fix.** The agent
  that fixes a figure MUST read the output PNG and visually confirm the
  fix before declaring completion.
- **Add a pixel-level aspect ratio check** to the plot validation
  pipeline: for every 2D figure, measure the axes bounding box in the
  rendered image and flag if |width - height| / max(width, height) > 5%.
- **Use `ax.set_box_aspect(1)`** (not `set_aspect("equal")`) for Lund
  plane plots where a square plot area is desired but the axis ranges
  differ.

---

## 7. Summary of Findings

| ID | Category | Description |
|---|---|---|
| A1 | A | Broken cross-reference: `\ref{sec:ibu-downscoping}` renders as "Section ??" (page 18). Correct label is `sec:ibu`. |
| A2 | A | Figure 12 right panel: non-square Lund plane aspect ratio (7:5 height:width from `set_aspect("equal")`) |
| A3 | A | Figure 19 (flagship): non-square aspect ratio + experiment label overlaps colorbar |
| A4 | A | Figure 22 (all four subfigures): non-square Lund plane aspect ratios |
| A5 | A | Figure 24 bottom-right: non-square Lund plane aspect ratio |
| A6 | A | Figure 25 (10% data flagship): non-square aspect ratio + label overlap |
| A7 | A | Figure 26 (both panels): non-square Lund plane aspect ratios |
| A8 | A | Figure 28: non-square Lund plane aspect ratio (same root cause) |
| B1 | B | Table 15: note that full-covariance chi2 is formally correct but inflated by rank-1 systematics |
| B2 | B | LO charged-particle prediction ~2/3 factor not explicitly qualified (carried from Doc 4a B1) |
| B3 | B | MC reweighting diagnostic (factors < 3x) not reported in AN |
| B4 | B | ATLAS:2024wqo DOI suspicious "01234-5" pattern (carried from Doc 4a B5) |
| B5 | B | ALEPH internal notes lack consistent bibliographic formatting |
| C1 | C | ALEPH:2001uca defined in bib but not cited |

**Category A findings: 8** (A1-A8, though A2-A8 share the same root cause)
**Category B findings: 5** (B1-B5)
**Category C findings: 1** (C1)

### Root cause grouping

The 7 aspect-ratio findings (A2-A8) share a single root cause: the use
of `ax.set_aspect("equal")` instead of `ax.set_box_aspect(1)` for Lund
plane coordinate plots. A single fix to the plotting utility function
(replacing `set_aspect("equal")` with `set_box_aspect(1)` for 2D Lund
plots, keeping `set_aspect("equal")` only for response/correlation
matrices) and regeneration of all figures would resolve all 7 findings
simultaneously. The label overlap on Figures 19 and 25 would also be
resolved by the aspect ratio fix (the tall-narrow plot area pushes the
label into the colorbar space).

Finding A1 is a one-line fix: change `sec:ibu-downscoping` to `sec:ibu`.

### Required actions for v4

1. Replace `ax.set_aspect("equal")` with `ax.set_box_aspect(1)` (or
   remove `set_aspect` and use `figsize=(10,10)`) for all 2D Lund plane
   coordinate plots. Keep `set_aspect("equal")` ONLY for the response
   matrix and correlation matrix.
2. Regenerate ALL 2D figures and recompile the PDF.
3. Fix `\ref{sec:ibu-downscoping}` -> `\ref{sec:ibu}` in the .tex file.
4. **Visually verify** every regenerated 2D figure in the compiled PDF
   before declaring completion.
5. Address B4 (verify ATLAS:2024wqo DOI).

---

## 8. Final Assessment

The physics content of the analysis note is strong. The 10% data results
are correctly processed, honestly interpreted, and provide genuine new
information about PYTHIA 6.1's modelling of collinear splittings. The
systematic treatment is complete and the validation chain is rigorous.
However, the rendering quality does not match the physics quality: the
flagship result figure and ~15 other 2D panels have incorrect aspect
ratios, and one cross-reference is broken. These are Category A issues
that must be resolved before the human gate.

The three-iteration cycle of plotting fixes (v1 -> v2 -> v3) without
resolution of the aspect ratio issue constitutes a systemic failure in
the plot validation pipeline. The fix agent misunderstood the matplotlib
aspect API and no downstream check (self-review, plot validator, rendering
check) caught the error visually. This must be addressed structurally.

**Verdict: ITERATE** -- fix A1-A8 (one root cause for A2-A8 + one-line
fix for A1), then regenerate and visually verify before re-review.
