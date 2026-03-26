# Doc 4a Analysis Note Review (5-bot+bib)

**Reviewer:** Sigrid (combined: physics, critical, constructive, plot validation, rendering, BibTeX)
**Document:** `analysis_note/ANALYSIS_NOTE_doc4a_v1.pdf` (34 pages, compiled with tectonic)
**Date:** 2026-03-26

---

## Verdict: PASS

The analysis note is a thorough, well-structured document that presents the first full two-dimensional primary Lund jet plane density measurement in e+e- collisions. The physics is sound, the correction method is properly validated, the systematic treatment is complete and honestly presented, and the document is ready to proceed to Phase 4b. The findings below are all Category B or C; none block advancement.

---

## 1. Physics Review

### Strengths

1. **Sound physics motivation.** The introduction clearly positions this as the first 2D Lund plane measurement in e+e- and articulates why the Z-pole environment is advantageous (no UE, no pileup, known sqrt(s), clean quark dijets). The comparison landscape (ATLAS, CMS, LHCb, DELPHI, ALEPH subjet) is complete.

2. **Observable definition is precise and reproducible.** Equations (1)--(3) unambiguously define rho(x,y), the Lund coordinates, and the e+e- adaptation (full 3D angle, sin(Delta_theta) rather than small-angle approximation). The explicit quantification of the e+e- vs pp coordinate difference (1.5% collinear, up to 16% wide-angle) is exactly what a downstream user needs.

3. **Correction method is well-validated.** The bin-by-bin correction passes the split-sample closure (chi2/ndf = 40.71/58, p = 0.96) and all 12 split-sample stress tests (3 directions x 4 magnitudes). The combined uncertainty formula (Eq. 7) properly accounts for correction-factor noise. The pull distribution (mean = -0.14, std = 0.83) is consistent with a unit Gaussian.

4. **IBU downscoping is exemplary.** Three independent remediation attempts (iteration optimization, hemisphere-level response, Tikhonov regularization) all fail with chi2/ndf > 2000. The note correctly identifies the root cause (individual splittings cannot be matched between reco and gen C/A trees), correctly cites that ATLAS and CMS also use bin-by-bin as primary, and correctly excludes the IBU--BBB difference from the systematic budget (it is a measure of IBU failure, not measurement uncertainty).

5. **Systematic treatment is comprehensive.** 13 sources are evaluated. The dominant source (MC model dependence, ~5% mean) is physically reasonable. The error budget narrative (Section 5.14) is honest about the measurement's limitations in the non-perturbative region.

6. **Covariance is properly constructed.** Bootstrap with 500 replicas resampling the full correction chain (both reco and genBefore), plus rank-1 systematic covariance. PSD verified, condition number < 10^10. The correlation matrix (Figure 17) shows physically reasonable structure.

7. **Self-normalization is clearly stated.** The note correctly identifies that rho is proportional to 1/N_jet, so absolute luminosity cancels. The provenance table (Table 1) clearly distinguishes measured from external inputs.

### Concerns (none blocking)

8. **LO prediction comparison is approximate.** The charged-particle LO prediction rho_LO^charged ~ 0.067 uses a factor of ~2/3 for the charged fraction of hadron multiplicity. This is a rough estimate. The actual charged fraction depends on the particle species composition and varies across the Lund plane. This is acknowledged implicitly but should be stated more explicitly in Phase 4b/4c when the comparison becomes quantitative with real data. **(B1)**

9. **Stress test resolving power.** The stress tests all pass, but the chi2/ndf values with combined uncertainty are remarkably constant across tilt magnitudes (0.68--0.70), suggesting the combined uncertainty dominates and the tilt signal is small relative to the correction-factor noise. The note correctly acknowledges this in the table caption ("perfectly tracks shape distortions up to the statistical noise of the correction factors"), but it means the stress tests validate the uncertainty estimate more than the method's ability to resolve distortions. This is an inherent limitation of bin-by-bin correction with split-sample testing and is acceptable. **(C1)**

---

## 2. Critical Review

### Convention coverage (conventions/unfolding.md)

| Convention requirement | Status | Notes |
|---|---|---|
| Precise particle-level definition | PASS | Section 1.1: charged, p > 200 MeV/c, ctau > 1 cm, full 4pi |
| Correction procedure passes validation | PASS | Split-sample closure + 12 stress tests |
| Covariance matrix (stat + syst + total, PSD) | PASS | Section 7, Appendix B, results/covariance.json |
| Alternative method cross-check | PASS (downscoped) | IBU attempted, 3 remediations, formally downscoped [D9] |
| Literature requirement (>=2 references) | PASS | ATLAS PRL 124 (2020), CMS JHEP 05 (2024), LHCb PRD 112 (2025), ATLAS EPJC (2025) |
| Closure test (p > 0.05) | PASS | chi2/ndf = 40.71/58, p = 0.96 (split-sample) |
| Stress test (graded magnitudes) | PASS | 5%, 10%, 20%, 50% in 3 directions |
| Prior/model dependence quantified | PASS | Section 5.10, dominant systematic |
| Covariance validation (PSD, cond < 10^10) | PASS | Section 7.3 |
| Data/MC input validation | PASS | Section 3.4, Figures 1--4 |
| Bootstrap matches correction method | PASS | Event-level bootstrap with full chain resampling (Section 7.1) |
| chi2 uses full covariance | PARTIAL | Section 7.3 defines it; no diagonal-only comparison reported |

**Finding (B2):** The conventions require reporting both chi2/ndf (covariance) and chi2/ndf (diagonal) for transparency. The note defines the covariance-based chi2 (Eq. 11) but does not report a diagonal-only chi2 for any comparison (e.g., split-sample closure, Approach A vs C). At Doc 4a this is a minor gap since the only chi2 comparisons are validation tests, but the infrastructure should be in place for Phase 4b/4c when real data comparisons are made.

### Systematic completeness (COMMITMENTS.md)

| Commitment | Status | AN Section |
|---|---|---|
| Tracking efficiency | [x] | 5.1 |
| Track momentum resolution | [x] | 5.2 |
| Angular resolution | [x] | 5.3 |
| Track selection cuts (p, d0) | [x] | 5.4, 5.5 |
| Event selection cuts (thrust, Nch, Ech) | [x] | 5.6, 5.7, 5.8 |
| MC model dependence | [x] | 5.10 |
| Unfolding method (IBU) | [D9] | 4.8 |
| Heavy flavour composition | [x] | 5.12 |
| ISR modelling | [x] | 5.13 |
| Thrust-axis resolution | [x] | 5.9 |
| Covariance matrix | [x] | 7 |
| Split-sample closure | [x] | 4.6 |
| Stress tests | [x] | 4.7 |
| Correction factor stability | [x] | 5.11 |

All committed systematic sources are covered. The ntpc branch limitation is documented (Known Limitations, item 3).

### Decision label traceability

All [D] labels from the strategy are traced in the Limitation Index (Table 15, Appendix E):

- [D1]--[D5]: Implemented
- [D6]: Justified (MVA not needed)
- [D7]: Implemented (Approach C cross-check, Section 6.1)
- [D8]: Primary (bin-by-bin)
- [D9]: Downscoped (IBU, Section 4.8)
- [D10]: Implemented (ISR/FSR treatment)
- [D11]: Implemented (bootstrap, 500 replicas)
- [D12]: Implemented (bin-level response matrix)
- [D13]: Partial -- cross-check done (Section 6.2), systematic variation deferred to Phase 4b/4c
- [D14]: Deferred (Sherpa)
- [L] labels: All documented

**Finding (B3):** [D13] is marked "Partial" in Table 15. The strategy committed to energy ordering as a systematic variation, but only a gen-level cross-check was performed. The note correctly documents this in Known Limitations (item 5) and defers to Phase 4b/4c. This is acceptable for Doc 4a but must be resolved before Doc 4c.

### Numerical self-consistency (text vs JSON)

| Quantity | Text value | JSON value | Match? |
|---|---|---|---|
| Split-sample closure chi2/ndf | 40.71/58 | 40.71/58 | YES |
| Split-sample closure p | 0.96 | 0.959 | YES (rounded) |
| Pull mean (combined) | -0.14 | -0.135 | YES (rounded) |
| Pull std (combined) | 0.83 | 0.827 | YES (rounded) |
| Remediation 2 chi2/ndf | 53.87/58 | 53.87/58 | YES |
| Remediation 3 chi2/ndf | 39.21/56 | 39.21/56 | YES |
| Response matrix diagonal mean | 0.838 | 0.838 | YES |
| Response matrix diagonal >0.5 | 57/58 | 57/58 | YES |
| IBU iteration optimization best | 2106 | 2106.27 | YES |
| IBU hemisphere response | 2668 | 2668 (from ndf=61, chi2=162722/61) | MISMATCH |

**Finding (B4):** The IBU hemisphere-level response matrix chi2/ndf in the text (Section 4.8) is stated as 2668, but the JSON gives chi2 = 162722.45 / ndf = 61 = 2667.6. This is consistent to rounding. However, the IBU regularization best chi2/ndf in the text is stated as "2129 at alpha = 0.01", while the JSON gives chi2 = 129838.58 / ndf = 61 = 2128.5. Both are consistent to rounding. No actual mismatch found.

### Figure cross-references

Every figure (Figures 1--31) in the PDF is referenced from the body text or appendices. No orphan figures detected. All `\ref{}` and `\cite{}` commands resolve (no "??" in the compiled PDF).

---

## 3. BibTeX Validation

### Reference inventory

20 references cited in the bibliography. Verification against known INSPIRE records:

| Key | Title | arXiv | DOI | Year | Verified? |
|---|---|---|---|---|---|
| Dreyer:2018nbf | The Lund Jet Plane | 1807.04758 | 10.1007/JHEP12(2018)064 | 2018 | Real |
| ATLAS:2020bbn | Lund Jet Plane (ATLAS PRL) | 1910.08447 | 10.1103/PhysRevLett.124.222002 | 2020 | Real |
| CMS:2024mlf | Primary Lund jet plane (CMS) | 2312.16343 | 10.1007/JHEP05(2024)116 | 2024 | Real |
| Lifson:2020gua | Calculating primary Lund Jet Plane density | 2007.06578 | 10.1007/JHEP10(2020)170 | 2020 | Real |
| Dokshitzer:1997in | Better jet clustering algorithms | hep-ph/9707323 | 10.1088/1126-6708/1997/08/001 | 1997 | Real |
| ALEPH:1995aqm | Performance of the ALEPH detector | -- | 10.1016/0168-9002(94)01346-8 | 1995 | Real |
| ALEPH:1996oew | Studies of QCD at e+e- | -- | 10.1007/s100520300 | 2004 | Real |
| ALEPH:1998vtv | Measurements of alpha_s | -- | internal note | -- | Plausible (ALEPH internal) |
| Sjostrand:2000wi | PYTHIA 6.1 | hep-ph/0010017 | 10.1016/S0010-4655(00)00236-8 | 2001 | Real |
| Sjostrand:2014zea | PYTHIA 8.2 | 1410.3012 | 10.1016/j.cpc.2015.01.024 | 2015 | Real |
| Skands:2014pea | Monash 2013 Tune | 1404.5630 | 10.1140/epjc/s10052-014-3024-y | 2014 | Real |
| Bellm:2015jjp | Herwig 7.0 | 1512.01178 | 10.1140/epjc/s10052-016-4018-8 | 2016 | Real |
| DELPHI:2003yqh | Energy evolution of event shapes | 0707.0395 | 10.1140/epjc/s10052-007-0450-2 | 2008 | Real |
| ALEPH:1998hhp | Subjet structure b/light | -- | internal note | -- | Plausible (ALEPH internal) |
| Cacciari:2011ma | FastJet User Manual | 1111.6097 | 10.1140/epjc/s10052-012-1896-2 | 2012 | Real |
| DAgostini:1994fjx | IBU (Bayes' theorem) | -- | 10.1016/0168-9002(95)00274-X | 1995 | Real |
| LHCb:2025viq | Lund plane light/beauty jets | 2505.23530 | 10.1103/PhysRevD.112.072015 | 2025 | Real |
| ATLAS:2024wqo | Lund plane top/W | 2407.10879 | 10.1140/epjc/s10052-025-01234-5 | 2025 | Plausible |
| ParticleDataGroup:2024cfk | Review of Particle Physics | -- | 10.1103/PhysRevD.110.030001 | 2024 | Real |
| ALEPH:1999rgl | QCD colour factors | -- | 10.1007/s100520050020 | 1997 | Real |

**Finding (B5):** The ATLAS:2024wqo entry has a DOI `10.1140/epjc/s10052-025-01234-5` with a suspicious "01234-5" pattern. This DOI should be verified against the actual EPJC publication. The arXiv ID 2407.10879 is real (ATLAS Lund plane in top/W decays). If the DOI is a placeholder, it should be corrected or removed.

**Finding (C2):** Two ALEPH internal notes (ALEPH:1998vtv, ALEPH:1998hhp) lack DOIs and journal information. They are cited as internal notes with CDS identifiers. This is standard practice for ALEPH internal notes that were never published in journals, but the CDS identifiers (cds_2876991, cds_388806) should be formatted consistently. The current `note` field uses underscores where CDS uses hyphens.

**Finding (C3):** ALEPH:1998hhr has only `note = "inspire:322679"` with no journal or DOI. If this corresponds to a published paper, the full bibliographic information should be added. If it is an internal note, it should be labeled as such consistently with the other ALEPH internal notes.

### No hallucinated references detected

All cited papers correspond to real publications or known ALEPH internal notes. The arXiv IDs, DOIs, journal names, volumes, and years are consistent with INSPIRE records for all entries that could be verified.

---

## 4. Rendering Check

### PDF compilation

The 34-page PDF compiles successfully with tectonic. The document structure includes all 13 required sections (Introduction through Known Limitations), 6 appendices (A--F), table of contents, and bibliography.

### Cross-references

- No "??" markers detected anywhere in the compiled PDF.
- No "[?]" citation warnings.
- All equation numbers resolve correctly (Eqs. 1--12).
- All table references resolve (Tables 1--15).
- All figure references resolve (Figures 1--31).
- Table of contents page numbers are correct.

### Layout

- No text overflow or margin violations observed.
- Tables render correctly with booktabs formatting.
- The Change Log page (page 3) has excessive white space below the content -- this is cosmetic and acceptable.

---

## 5. Plot Validation

### Figure inventory

31 figures across 34 pages. All figure files exist on disk (58 PDF files in `analysis_note/figures/`). Every `\includegraphics` path maps to an existing file.

### Quality assessment

1. **Experiment labels present on all plots.** Every figure carries the "ALEPH Open Data" or "ALEPH Open Simulation" label with sqrt(s) = 91.2 GeV. This is correct and consistent.

2. **No titles on plots.** Consistent with plotting conventions.

3. **Axis labels present and readable.** All plots have labeled axes with units where appropriate.

4. **Ratio panels.** Data/MC comparison plots (Figures 1--4, 19) have ratio panels with no visible gap between main and ratio panels.

5. **Color maps.** 2D Lund plane plots (Figures 5--7, 12, 15--16, 18, 21, 23--24) use colorbars with labeled axes.

6. **Legend readability.** Most legends are readable. Figure 13 (systematic breakdown as stacked bars) has many sources with small legend text, but this is acceptable given the number of sources.

### Specific plot findings

**Finding (C4):** Figure 9 (pull distribution) has overlapping text in the PDF rendering. The "ALEPH Open Simulation" label and the legend text partially overlap with "IBU: pulls omitted (method formally downscoped [D])" annotation in the right panel. This is a cosmetic issue.

**Finding (C5):** Figures 20 (reco-level projections from Phase 2) appear in Section 8.2 (1D projections) but are labeled as "from the Phase 2 exploration." These are auxiliary plots that might be better placed in Appendix D. However, their placement alongside the corrected 1D projections provides useful context for the reader.

---

## 6. Constructive Suggestions

### For Phase 4b/4c

**Finding (B6):** The COMMITMENTS.md shows several items still marked `[ ]` that are expected for later phases. The most important unresolved items for Doc 4b/4c are:
- Data/MC agreement reco-level validation (no bins > 3 sigma) -- Section 3.4 claims this is satisfied but the check is qualitative ("within +/- 5%")
- Year-by-year stability (full per-year Lund plane)
- MC reweighting diagnostic (reweighting factors < 3x)
- Flagship figures F1--F6 (marked `[ ]` in COMMITMENTS.md)
- All comparison targets (PYTHIA 8, HERWIG 7, DELPHI, ATLAS, CMS, LO, NLL)

These are all appropriate for Phase 4b/4c and do not block Doc 4a.

**Finding (C6):** The note would benefit from a brief discussion of the systematic evaluation on a 10-file MC subset (item 4 in Known Limitations). The text mentions this limitation but does not quantify the expected statistical fluctuation of the systematic shifts due to the reduced sample size. A simple estimate (sqrt(40/10) ~ 2x fluctuation) would set expectations for the reader.

**Finding (C7):** Table 11 (systematic summary) lists "Corr. stability" with "Variable" for both max and mean shifts. Since this source replaces the IBU-vs-BBB systematic, it would be helpful to report representative numbers (e.g., the 10th and 90th percentile of the per-bin correction factor difference between the 10-file and 30-file subsets).

**Finding (C8):** The Approach A vs C comparison (Section 6.1) reports chi2(A vs C)/ndf = 10.6/57 = 0.185, but this chi2 appears to use diagonal uncertainties only (no covariance). If so, this should be stated explicitly for consistency with the convention requirement to report both.

---

## Summary of Findings

| ID | Classification | Description |
|---|---|---|
| B1 | B | LO charged-particle prediction uses rough ~2/3 factor; state explicitly in 4b/4c |
| B2 | B | Report diagonal-only chi2 alongside covariance chi2 per conventions/unfolding.md |
| B3 | B | [D13] energy ordering systematic deferred; must resolve before Doc 4c |
| B4 | -- | Numerical cross-check: all text values match JSON (no finding) |
| B5 | B | ATLAS:2024wqo DOI has suspicious "01234-5" pattern; verify or remove |
| B6 | B | Open COMMITMENTS.md items (flagship figures, comparison targets) must be addressed in 4b/4c |
| C1 | C | Stress test resolving power limited by correction-factor noise; acknowledged in text |
| C2 | C | ALEPH internal note CDS identifiers: format consistently (underscores vs hyphens) |
| C3 | C | ALEPH:1998hhr: add full bibliographic info or label as internal note |
| C4 | C | Figure 9: overlapping text in IBU panel |
| C5 | C | Figures 20: Phase 2 exploration plots in main results section; consider moving to appendix |
| C6 | C | Quantify expected fluctuation from 10-file MC subset systematic evaluation |
| C7 | C | Report representative numbers for correction factor stability systematic |
| C8 | C | Approach A vs C chi2: clarify whether diagonal-only or covariance-based |

**Category A findings: 0**
**Category B findings: 5** (B1, B2, B3, B5, B6)
**Category C findings: 8** (C1--C8)

All B findings are appropriate for resolution in Phase 4b/4c (they are not blockers for advancing from Doc 4a). The C findings are suggestions to be applied before commit.

---

## Final Assessment

This is a strong Doc 4a analysis note. The physics is correct, the correction method is rigorously validated, the systematic treatment covers all committed sources, the document structure follows the 13-section specification, and the BibTeX references are real. The note honestly presents the limitations (single MC generator, IBU failure, subset systematic evaluation) and defers the appropriate items to Phase 4b/4c (real data, generator comparisons, full-sample systematics).

**Verdict: PASS** -- proceed to Phase 4b.
