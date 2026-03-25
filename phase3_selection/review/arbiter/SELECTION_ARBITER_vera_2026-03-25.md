# Phase 3 Arbiter Adjudication: Selection

**Arbiter:** Vera | **Date:** 2026-03-25
**Artifact:** `SELECTION_ingrid_2026-03-25_19-01.md`
**Critical review:** `SELECTION_CRITICAL_REVIEW_nadia_2026-03-25.md`
**Plot validation:** `SELECTION_PLOT_VALIDATION_nadia_2026-03-25.md`

---

## 1. Review Summary

The critical review found **0 Category A** and **8 Category B** findings.
The plot validation found **1 Category B** (PV-1: wrong experiment label on
closure figures) and **5 Category C**. I adjudicate each below.

---

## 2. Category B Adjudication

### B-1 / B-6: Thrust vs Thrust_charged for event selection

**Review claim:** The strategy committed to Thrust_charged for the event
selection cut. The implementation uses energy-flow Thrust. This is a
departure without documented justification.

**Adjudication: Accept as B. Defer to Phase 4.**

The Phase 2 quantification (0.15% mean difference) establishes that the
impact is negligible at current precision. The passesAll flag already
encodes an event-quality selection that subsumes the thrust cut's purpose.
However, the reviewer is correct that a committed approach was silently
changed -- this must be documented. Resolution: add a note to the artifact
and COMMITMENTS.md acknowledging the deviation and citing the Phase 2
quantification. Include Thrust_charged vs Thrust as an event selection
systematic variation in Phase 4 (already in COMMITMENTS.md). Does not
require re-running Phase 3 processing.

B-6 is the same finding viewed from COMMITMENTS.md. Merged with B-1.

### B-2: Missing ntpc >= 4 track cut

**Review claim:** The strategy specifies ntpc >= 4 as a track-level cut.
The implementation does not apply it. The branch may not exist in the
archived data.

**Adjudication: Accept as B. Defer to Phase 4.**

The aftercut pre-selection (passesAll) likely enforces a minimum-track
requirement that subsumes this cut. The key question -- whether the ntpc
branch exists in the archived data -- is an empirical check that Phase 3
should have documented but did not. Resolution: document the branch
availability status. If absent, note that the COMMITMENTS.md systematic
variation "vary ntpc from 3 to 5" becomes infeasible and must be
downscoped with justification. This is a documentation gap, not a
reprocessing requirement.

### B-3: One correction factor exceeds 5x (C = 6.67)

**Review claim:** The maximum correction factor of 6.67 exceeds the
plausible range guideline. The bin is not identified.

**Adjudication: Downgrade to C.**

A single boundary bin with a large correction factor is standard in 2D
measurements with kinematic boundaries. The reviewer correctly notes this
affects one bin. The correction factor map shows the bulk is well-behaved
(median 1.47, 54/58 bins below 2.0). The bin will have large statistical
uncertainty in Phase 4 and will be handled by the covariance matrix. The
bin should be identified in the artifact for traceability, but this is a
documentation improvement, not a physics concern.

### B-4: Diagonal fraction is approximate, not event-matched

**Review claim:** The diagonal fraction is computed from aggregate bin
populations (min/max proxy), not from event-level matching. This
overestimates the true diagonal fraction.

**Adjudication: Accept as B. Defer to Phase 4.**

The reviewer is correct that the aggregate proxy is not the true diagonal
fraction. However, the Phase 2 migration study (14% average migration)
provides a more reliable event-matched estimate from a smaller sample.
The two estimates are consistent: 83.6% aggregate vs ~86% event-matched.
The bin-by-bin method viability conclusion is robust -- the true diagonal
fraction is well above the 50% threshold. Phase 4 will construct the full
response matrix with event-level matching, which produces the exact
diagonal fraction. Resolution: flag the approximate nature explicitly in
the artifact text (the figure label already says "approximate").

### B-5: Pion mass assumed for all charged tracks

**Review claim:** All tracks are assigned the pion mass when computing
energy. The strategy does not specify this assumption. The actual mass
branch is available.

**Adjudication: Accept as B. Defer to Phase 4.**

The pion mass assumption is standard practice in charged-particle
substructure measurements (ATLAS, CMS, and DELPHI Lund plane analyses
all use it). For C/A clustering with E-scheme recombination, the mass
enters through the energy. The impact is small: kaons and protons
constitute ~15% of charged tracks, and the mass difference affects the
energy by O(m^2/2p^2), which is sub-percent for p > 200 MeV/c except for
protons at threshold. Resolution: document the assumption in the artifact.
Assess the impact as a Phase 4 systematic by reprocessing with actual
particle masses (the branch exists). Does not require Phase 3 reprocessing.

### B-7: genBefore hemisphere splitting uses gen-level thrust axis

**Review claim:** The genBefore tree uses its own thrust axis for
hemisphere splitting, which may differ from the reco-level computation.

**Adjudication: Downgrade to C.**

This is by design. The particle-level definition uses the particle-level
thrust axis. The reco-level uses the detector-level thrust axis. The
correction factors absorb the difference between the two. The reviewer
correctly identifies this as a systematic source, but it is already
covered by the "thrust-axis resolution" systematic in COMMITMENTS.md.
No action required beyond noting the consistency.

### B-8: Approach C has no MC correction infrastructure

**Review claim:** The approach comparison is reco-level only. Phase 4
will need Approach C correction factors for the cross-check systematic.

**Adjudication: Accept as B. Defer to Phase 4.**

The purpose of the Phase 3 approach comparison is to validate the primary
method choice, which it does (chi2/ndf = 0.185, approaches agree within
1%). Building full correction infrastructure for the cross-check approach
is Phase 4 work. The artifact correctly identifies this as a Phase 4
requirement (Section 8.2). No Phase 3 action needed.

### PV-1: Wrong experiment label on closure test figures

**Review claim:** Figures 9 and 10 (closure test 1D projections) read
"ALEPH Open Data" but are pure-MC comparisons. Should be "Open Simulation."

**Adjudication: Accept as B. Fix before commit.**

This is a concrete, one-line code fix: pass `llabel="Open Simulation"` to
the `aleph_label()` call in the closure test plotting function. The fix is
trivial and should be applied before committing Phase 3. It does not
require re-review.

---

## 3. Regression Trigger Check

Independent assessment against mandatory regression triggers:

| Trigger | Status | Evidence |
|---------|--------|---------|
| Any validation test failure? | NO | Self-consistency closure passes (algebraic identity, correctly identified). Split-sample closure deferred to Phase 4 per conventions/unfolding.md. |
| Any single systematic > 80% of total? | N/A | No systematics evaluated in Phase 3. Deferred to Phase 4. |
| Any closure test failure? | NO | chi2/ndf ~ 0 is the expected algebraic identity, not a failure. The alarm band (chi2/ndf < 0.1) is correctly flagged and explained. |
| Data/MC agreement gate? | PASS | 1D projection ratios within 5-10%. 2D ratio mean 1.005, std 0.105. |
| Diagonal fraction below 50%? | NO | 57/58 bins above 50%. One boundary bin below -- acceptable for kinematic edge. |
| Correction factors pathological? | NO | Median 1.47, range [1.17, 6.67]. Bulk well-behaved. One boundary outlier (downgraded to C). |

**No regression triggers fired.**

---

## 4. Dispositions Summary

| Finding | Original | Adjudicated | Action | Phase |
|---------|----------|-------------|--------|-------|
| B-1/B-6 | B | B | Document deviation, add systematic variation | Phase 4 |
| B-2 | B | B | Document branch availability, assess passesAll coverage | Phase 4 |
| B-3 | B | C | Identify the bin in artifact text | Before commit |
| B-4 | B | B | Flag approximation in artifact text | Before commit |
| B-5 | B | B | Document pion mass assumption, assess with real masses | Phase 4 |
| B-7 | B | C | Already covered by thrust-axis resolution systematic | None |
| B-8 | B | B | Build Approach C correction infrastructure | Phase 4 |
| PV-1 | B | B | Fix experiment label in closure figures | Before commit |

**Items to fix before commit (non-blocking for Phase 3 advancement):**
1. Fix closure figure labels to "Open Simulation" (PV-1)
2. Identify the C = 6.67 bin by (i, j) coordinates in artifact (B-3)
3. Add sentence to artifact Section 3.3 noting the diagonal fraction is
   an aggregate-level approximation (B-4)

**Items deferred to Phase 4 (with tracking):**
1. Thrust_charged vs Thrust systematic variation (B-1/B-6)
2. ntpc branch availability documentation (B-2)
3. Pion mass vs actual mass systematic (B-5)
4. Approach C correction infrastructure (B-8)

---

## 5. Verdict

**PASS**

Phase 3 is well-executed. The selection, Lund plane construction, and
correction infrastructure are correctly implemented. The observable
definition matches the strategy. Two qualitatively different approaches
are compared quantitatively. All data and MC files are processed. The
closure test correctly identifies the algebraic identity and defers the
genuine test to Phase 4.

The three pre-commit fixes (label, bin identification, diagonal fraction
note) are minor and do not require re-review. The four Phase 4 deferrals
are legitimate -- they require either reprocessing or systematic evaluation
that belongs in the inference phase.

Phase 3 may advance to Phase 4 after the pre-commit fixes are applied.
