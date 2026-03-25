# Session Log: Critical Review (Andrzej)

**Date:** 2026-03-25
**Role:** Critical reviewer (bad cop)
**Artifact reviewed:** `phase1_strategy/outputs/STRATEGY_fabiola_2026-03-25_16-50.md`

## Documents read

1. Strategy artifact (full, 491 lines)
2. Phase 1 CLAUDE.md (148 lines)
3. experiment_log.md (67 lines)
4. COMMITMENTS.md (57 lines)
5. conventions/unfolding.md (157 lines)
6. methodology/03-phases.md (lines 1-338, Phase 1 section + analysis philosophy)
7. methodology/06-review.md (lines 1-264, review protocol + Phase 1 focus)
8. retrieval_log.md (35 lines)

## RAG queries performed (independent verification)

### LEP corpus searches (6 queries)

1. "ALEPH jet substructure Cambridge algorithm declustering Lund plane"
   (ALEPH, hybrid, top_k=10)
   - Confirmed: inspire_457159 / cds_388806 (ALEPH subjet analysis with
     Durham algorithm, ~3M events, multiplicative correction)
   - Found: inspire_1659417 (DELPHI alpha_s from four-jet rate) -- contains
     the Cambridge algorithm definition (d_ij = 2(1-cos theta_ij))
   - Found: inspire_454037 (LEP 4-jet report) -- ALEPH/OPAL selection details
   - No NEW Lund-plane-specific LEP measurement found beyond what the
     strategy cites

2. "Cambridge algorithm angular ordering splitting function kT measurement"
   (all experiments, hybrid, top_k=10)
   - Confirmed: inspire_1659417 has the Cambridge algorithm definition
   - Found: inspire_248756 (ALEPH "Method of Reduced Cross-Entropy") --
     a regularized unfolding technique used by ALEPH. Not cited in the
     strategy. Potentially relevant as an alternative unfolding method.
   - Found: inspire_530425 (DELPHI gg-multiplicity) -- uses jet splitting
     and substructure, broadly consistent with cited references

3. "unfolding correction systematic uncertainty hadronization ALEPH LEP"
   (ALEPH, hybrid, top_k=10)
   - Found: inspire_610230 (ALEPH F2^gamma with Tikhonov regularization)
   - Found: hep-ph/9909283 (ALEPH F2^gamma with 2D unfolding + maximum
     entropy) -- "model dependence of the extracted F2^gamma reduced by
     2D unfolding"
   - Found: inspire_888521 (ALEPH intermittency with correction procedure)
   - Found: inspire_444347 (ALEPH tau spectral functions with regularized
     unfolding)
   - Key takeaway: ALEPH has used regularized unfolding (not just bin-by-bin)
     for several measurements. The strategy's claim that "LEP analyses used
     multiplicative correction" is an overgeneralization.

4. "ALEPH event shape thrust distribution correction factor detector effect"
   (ALEPH, hybrid, top_k=8)
   - Found: inspire_309697 (ALEPH first hadronic Z results -- corrected
     thrust, x_p, rapidity distributions; compared LUND 6.3, HERWIG 3.4,
     matrix element model)
   - Found: hep-ex/0008013 (ALEPH b-quark mass from event shapes -- uses
     cos(theta_T) < 0.7, 2.3M events, JETSET 7.4 MC, Peterson fragmentation)
   - Found: inspire_349416 (ALEPH alpha_s from event shapes -- uses only
     charged particles, correction for detector effects, systematic from
     varying selection cuts and MC generators)

5. "ALEPH particle flow energy flow charged neutral track calorimeter"
   (ALEPH, hybrid, top_k=5)
   - Found: hep-ex/9911015 (ALEPH ALPHA++ object-oriented analysis:
     defines Track, AlEflw, AlGamp objects) -- confirms energy flow objects
     exist alongside charged tracks in the ALEPH framework

6. "ALEPH b quark contamination heavy flavour fraction event shape hadronic Z"
   (ALEPH, hybrid, top_k=5)
   - Found: hep-ex/0008013 (b-quark mass from event shapes)
   - Found: inspire_433306 (ALEPH Rb measurement)
   - Found: 1610.06536 (ALEPH archived data analysis, 3.7M events, 8M MC)
   - Key finding: heavy flavour effects on jet substructure are a known
     and measured effect at ALEPH. The strategy does not include this as
     a systematic source.

### Additional targeted searches (3 queries)

7. "ALEPH secondary particles weak decay strange K lambda long-lived"
   (ALEPH, hybrid, top_k=5)
   - No directly relevant result for Lund plane systematics. Strange particle
     decays (K_S -> pi+pi-, Lambda -> p pi-) produce secondary tracks that
     can contaminate the Lund plane. The particle-level definition requires
     c*tau > 1 cm, which includes K+/- and pi+/- but excludes K_S. The
     strategy handles this correctly.

8. "LEP event shape alpha_s ALEPH OPAL comparison detector correction bin-by-bin"
   (all experiments, hybrid, top_k=5)
   - Found: inspire_1660364 (DELPHI alpha_s from event shapes -- uses
     hadronisation corrections from fragmentation model generators AND
     analytical power ansatz)
   - Found: inspire_349416 (ALEPH alpha_s -- uses only charged particles,
     corrections from MC + detector simulation, systematic from varying
     selection cuts and generators)

9. "b quark mass fragmentation heavy flavour systematic LEP event shape"
   (all experiments, hybrid, top_k=5)
   - Confirmed that b-quark mass effects on event shapes are a well-measured
     systematic at LEP (multiple ALEPH and DELPHI papers)

### Paper drilldowns (3 papers)

1. cds_2876991: Confirmed track cuts, event selection, tracking systematic
   0.7%. The paper uses the same archived ALEPH data as this analysis.

2. inspire_1659417: Contains the Cambridge algorithm definition used in the
   strategy (d_ij = 2(1-cos theta_ij)). Also describes the "soft freezing"
   step in Cambridge (if y_ij >= y_cut, store as jet and delete). The
   strategy does not discuss soft freezing -- this is only relevant for
   exclusive Cambridge clustering, not inclusive C/A used in the Lund plane.

3. inspire_1661966: DELPHI jet splitting analysis. Uses Durham algorithm
   (not Cambridge) for subjet identification. Correction factors from
   JETSET. Explicitly separates quark and gluon jets using b-tagging,
   measuring the splitting ratio. This confirms that flavour composition
   is a relevant systematic for jet substructure measurements at LEP.

## Key findings

### What the strategy gets right
- Observable motivation is clear and well-argued
- Sample inventory is thorough (data + MC event counts, branch inventories)
- Background classification is correct and well-cited
- MVA infeasibility is well-justified with three concrete reasons
- Self-normalization cancelling luminosity is a good design choice
- Self-critique caught and fixed 7 genuine issues
- The bin-by-bin vs IBU dual approach is well-motivated
- Response matrix matching strategy [D12] correctly addresses the
  variable-multiplicity pitfall

### What the strategy gets wrong or misses
- Observable definition not verified by retrieving the foundational paper
- Binning is uniform without physics justification
- Heavy flavour composition systematic is absent
- Published comparison data not numerically extracted
- Hemisphere assignment systematic violates conventions (observable
  redefinition)
- Reweighting limitation for model dependence not discussed
- IBU response matrix definition is non-standard
- No methodology diagram planned
- "Aftercut" pre-selection not investigated

## Time spent
- Reading all inputs: ~15 minutes
- RAG queries and verification: ~10 minutes
- Writing review: ~20 minutes
- Total: ~45 minutes
