# Session Log: Physics Review of Phase 1 Strategy

**Session:** Albert (PI / physics referee)
**Date:** 2026-03-25
**Artifact reviewed:** `phase1_strategy/outputs/STRATEGY_fabiola_2026-03-25_16-50.md`

---

## Actions Taken

1. **Read the physics prompt** (`prompt.md`) and the full strategy artifact.

2. **Verified the observable definition against the foundational paper.**
   Downloaded and read Dreyer, Salam, Soyez, JHEP 12 (2018) 064
   (arXiv:1807.04758), Sections 2.1-2.3 and Equations 2.1-2.6.
   - Found the LO density formula in the strategy is missing a factor
     of 2 (Eq. 2.6 gives 2*alpha_s*C_F/pi, not alpha_s*C_F/pi).
   - Found the "harder subjet" is defined by beam-axis pT in the paper,
     not energy as the strategy claims.
   - Found the coordinate definitions (Delta, k_T) differ between the
     pp formalism and the e+e- adaptation proposed in the strategy.
     The strategy's choice (theta, p*sin(theta)) is physically motivated
     but must be clearly documented as an adaptation.

3. **Searched the LEP corpus** for:
   - ALEPH tracking resolution: found Delta_p/p^2 = 1.2e-3 from
     inspire_322679 (TPC only), vs. 0.6e-3 claimed in strategy
     (likely combined TPC+ITC+VDET).
   - ALEPH hadronic event selection: confirmed standard cuts from
     cds_2876991 and inspire_401685 match the strategy.
   - ALEPH tracking efficiency uncertainty: confirmed 0.7% from
     cds_2876991, consistent with strategy's 1% conservative envelope.
   - DELPHI jet splitting: confirmed inspire_1661966 used bin-by-bin
     correction, consistent with strategy's claim.

4. **Searched for modern Lund plane measurements** beyond the strategy's
   reference list.  Found:
   - CMS, JHEP 05 (2024) 116 -- pp at 13 TeV, AK8 jets, IBU.
   - ATLAS, arXiv:2407.10879 (2024) -- top quark/W boson Lund plane.
   - LHCb, arXiv:2505.23530 (2025) -- light/beauty quark jets, dead
     cone observation.
   All three are missing from the strategy's reference table.

5. **Evaluated the correction method choice.**  Noted that all four modern
   Lund plane measurements (ATLAS, ALICE, CMS, LHCb) use iterative
   Bayesian unfolding as their primary method.  The strategy's choice of
   bin-by-bin as primary is an outlier relative to the field.

6. **Checked for missing systematics.**  Identified b-quark flavor
   composition (~22% of Z decays) and neutral-particle contamination
   of the thrust axis as unaddressed systematic sources.

7. **Wrote the physics review** to
   `phase1_strategy/review/physics/STRATEGY_PHYSICS_REVIEW_albert_2026-03-25.md`
   with 13 findings (3A, 7B, 3C).

## Key Findings

- **3 Category A (must resolve):** LO formula factor-of-2 error; "harder
  subjet" definition ambiguous and falsely claimed as standard; coordinate
  definitions need clear e+e- adaptation documentation.
- **7 Category B (should address):** Incomplete reference table; bin-by-bin
  as primary weakly motivated; momentum resolution possibly wrong; no
  b-quark systematic; thrust axis neutral contamination; binned formula
  unstated; stress test underspecified.
- **3 Category C (suggestions):** Thrust cut may bias; F5 mislabeled;
  NLL predictions should be committed.

## Verdict

**ITERATE.**  The strategy cannot advance until the observable definition
(F1-F3) is precise and correct.  These are foundational errors that would
propagate through every downstream phase.

## Time Spent

Approximately 45 minutes of review time, including literature verification.
