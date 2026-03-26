# Doc 4b Review Note: Analysis Note Update Coherence Check

**Reviewer:** Hana | **Date:** 2026-03-26
**Document:** `analysis_note/ANALYSIS_NOTE_doc4b_v1.tex` (40 pages, compiled PDF)

---

## Verdict: COHERENT

The Doc 4b update is well-integrated with the existing Doc 4a content.
The analysis note tells a coherent physics story from expected results
through 10% data validation.

---

## Changes Verified

| Change | Location | Status |
|--------|----------|--------|
| Header comment updated (Doc 4b v1) | Line 3 | Done |
| Abstract expanded with 10% data findings | Page 1 | Done |
| Change Log: Doc 4b entry added above Doc 4a | Page 4 | Done |
| Section 8.6: 10% data results (8 subsections) | Pages 27-32 | Done |
| Section 6.3.1: Per-year stability on 10% data | Page 22 | Done |
| Conclusions: items 6-9 added for 10% data | Pages 32-33 | Done |
| Known Limitations: Phase 4b/4c refs updated to 4c | Pages 33-34 | Done |
| Reproduction Contract: Phase 4b commands added | Page 38 | Done |
| \tbd references updated (4b/4c -> 4c) | Throughout | Done |
| 9 new figures staged in figures/ | All oscar_*.pdf | Done |

## Content Coherence

1. **Narrative flow.** The 10% data results (Section 8.6) follow naturally
   after the expected results and uncertainty breakdown (Sections 8.1-8.5).
   The subsection structure (processing summary, correction, corrected
   plane, comparison, projections, diagnostics) mirrors the Phase 4b
   artifact structure.

2. **Cross-references.** The corrected 10% Lund plane (Figure 25) correctly
   references the expected result (Figure 19). The pull map and ratio
   (Figure 26) are properly captioned with the chi2/ndf value. The
   per-year stability (Section 6.3.1) is linked from the cross-checks
   section with a proper subsection label.

3. **Numerical consistency.** All numbers in the AN match the Phase 4b
   artifact and the machine-readable JSON:
   - chi2/ndf = 197.7/57 = 3.47 (consistent)
   - Pull mean +0.60, std 1.76 (consistent)
   - N_hemispheres = 569,472 (consistent)
   - R_hemi = 1.3427 (consistent)
   - Per-year chi2/ndf values all match

4. **Conclusions updated appropriately.** The original 5 findings from
   expected results are preserved. Four new findings (items 6-9) from
   the 10% data are added with proper bold headers. The forward-looking
   statement about chi2 increasing with full statistics is physically
   correct and well-placed.

5. **Remaining \tbd markers.** Two \tbd placeholders remain, both
   appropriately targeting Phase 4c:
   - PYTHIA 8 / HERWIG 7 generator comparison
   - Quantitative comparison to ATLAS/CMS published data
   These are correct -- they cannot be resolved at the Doc 4b stage.

## PDF Quality

- Total: 40 pages (up from ~38 in Doc 4a), well within the 50-100 page target range.
- All 9 new figures render correctly with proper ALEPH labels.
- Tables are properly formatted with booktabs.
- No broken cross-references visible.
- Minor overfull hbox warnings (cosmetic, no content impact).

## No Issues Found

The Doc 4b update is ready for the 5-bot+bib review panel.
