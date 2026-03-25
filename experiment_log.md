# Experiment Log

## Phase 1: Strategy (Fabiola, 2026-03-25)

### Data exploration

**2026-03-25 16:46** — Ran `check_data_structure.py` to inspect ROOT file contents.

**Finding:** Data files contain main particle tree "t" (151 branches, variable-length particle arrays per event) plus multiple pre-computed jet trees (anti-kT R=0.4/0.8 with E-scheme and WTA-modp recombination, kT N=2/3 exclusive jets, boosted WTA event trees). Pre-computed SoftDrop variables (zg, rg with beta=0, z_cut=0.1) are stored per jet. Data tree "t" has 433,947 events in the 1994P1 file.

**Finding:** MC files have the same reco structure plus generator-level trees: `tgen` (199 branches, gen-level after event selection) and `tgenBefore` (151 branches, gen-level before event selection). Also has gen-level jet trees for all clustering algorithms. This enables response matrix construction and efficiency correction.

**2026-03-25 16:47** — Ran `count_events.py` to count all events.

**Result:** 3,050,610 total data events across 6 files (1992-1995). 771,597 MC events (40 files, reco = gen count). MC is ~25% of data statistics. tgenBefore has ~27% more events than tgen per file (24,360 vs 19,158), indicating the event selection efficiency at generator level is ~79%.

**2026-03-25 16:47** — Ran `check_branches.py` for full branch inventory.

**Key findings:**
- Pre-computed thrust axis (Thrust, TTheta, TPhi) available, plus charged-only and corrected variants
- Sphericity, Aplanarity, linearized event shapes all pre-computed
- Selection flags per event (passesAll, passesNTrkMin, passesSTheta, passesMissP, passesISR, passesWW, passesNeuNch)
- pwflag in data: 0 (charged tracks, dominant), 1, 2, 4 (photons), 5 (neutral hadrons)
- pwflag in MC gen: includes -11 (ISR/material particles excluded at truth level), 0, 1, 2, 3, 4, 5
- MC gen-level has extra branches for systematic studies: ThrustWithReco, ThrustWithGenIneff, ThrustWithGenIneffFake, ThrustWithRecoCorr, ThrustWithRecoCorrInverse, ThrustWithRecoAndMissP — these compute the truth thrust using various combinations of reco/gen information, enabling systematic evaluation.

### LEP corpus search

**2026-03-25 16:46** — Queried LEP corpus with 6 searches and 3 paper drilldowns.

**Key references found:**
- cds_2876991 (ALEPH QGP search with same archived data): Standard track cuts (p > 200 MeV/c, |d0| < 2 cm, |z0| < 10 cm, ntpc >= 4), event selection (N_ch >= 5, E_ch > 15 GeV, missing P < 20 GeV, |cos theta_sph| < 0.82), tracking systematic ~0.7% from TPC hit variation
- inspire_1661966 (DELPHI jet splitting): Durham kT algorithm splitting probability density, bin-by-bin correction from JETSET, CA = 2.8 +/- 0.8 * CF from splitting ratio
- cds_388806 / inspire_457159 (ALEPH quark/gluon subjet): ~3M events, Durham algorithm, multiplicative detector correction method, systematic assessment includes MC model comparison (JETSET vs HERWIG vs ARIADNE)
- inspire_322679 (ALEPH EEC): Detailed ALEPH track quality cuts with physics justification

### Decisions made

- Use Cambridge/Aachen algorithm for Lund plane construction (angular-ordered; standard choice per Dreyer, Salam, Soyez)
- Primary correction method: bin-by-bin (consistent with LEP practice, justified by excellent ALEPH resolution)
- Cross-check correction: iterative Bayesian unfolding (matching ATLAS/ALICE methodology)
- No MVA for event selection (justified: no background to reject, event quality is one-dimensional)
- Second selection approach: exclusive kT jets instead of thrust hemispheres (qualitatively different jet definition)
- Particle-level definition: charged particles, p > 200 MeV/c, c*tau > 1 cm, full phase space

### Self-critique fixes (Fabiola, 2026-03-25)

**2026-03-25** — Post-completion self-critique identified and corrected 7 issues in the strategy:

1. **Background systematic was flat-assigned.** Removed the 0.1% flat systematic (violates conventions/unfolding.md pitfall on flat estimates). Backgrounds are negligible; no systematic needed. Cross-check by MC subtraction if ever questioned.

2. **MC model dependence procedure was vague.** Replaced "varied truth shapes" with concrete procedure: reweight PYTHIA 6.1 gen-level to match PYTHIA 8 / HERWIG 7 truth-level shapes, derive new correction factors, take envelope.

3. **ISR systematic "toggle ISR on/off" was not implementable.** Cannot toggle ISR in archived MC. Replaced with: compare thrust axis with/without pwflag=-11 particles at gen-level to quantify ISR effect on hemisphere assignment and Lund plane.

4. **Tracking efficiency 1% drop justification was circular.** Added explicit justification: 0.7% is the TPC hit requirement variation; per-track inefficiency is ~1-2%; 1% random drop is a conservative envelope.

5. **"Harder subjet" definition was ambiguous.** Removed misleading "equivalently, larger E for massless particles" (particles are NOT massless). Clarified: use energy E as hardness criterion (standard for e+e-).

6. **Analytical LO formula was uncited.** Added citation: Dreyer, Salam, Soyez, JHEP 12 (2018) 064, Eq. 2.6. Added numerical estimate: rho_LO ~ 0.050.

7. **Approach C y_cut procedure was underspecified.** Added: scan R_2(y_cut) in data and MC in Phase 2; select y_cut where R_2 ~ 80-85%.

8. **Response matrix matching for variable-multiplicity observable was not discussed.** Added [D12]: bin-level population matching, not object-level 1:1 matching, for Lund declusterings. Addresses conventions/unfolding.md pitfall on wrong matching strategy.

9. **Retrieval log was empty.** Populated with all 6 LEP corpus queries, 3 paper drilldowns, and modern methodology search results.

## Phase 1: Strategy Fix (Peter, 2026-03-25)

### Arbiter verdict: ITERATE

**2026-03-25 17:17** -- Arbiter (Sally) returned ITERATE with 5 Category A and 16 Category B findings. Fix session initiated.

### Web search: foundational paper verification (MANDATORY)

**2026-03-25 17:17** -- Retrieved Dreyer/Salam/Soyez 2018 (arXiv:1807.04758) PDF. Term-by-term comparison with strategy:

**Finding 1 (LO formula):** Strategy had rho_LO = alpha_s * C_F / pi (Eq. 2.6 in paper). Paper's Eq. 2.6 gives rho = 2 * alpha_s(k_T) * C_F / pi. The factor 2 arises from the soft limit of the splitting function p_{gq}(z) = (1+(1-z)^2)/z, which gives 2 as z -> 0. Strategy's numerical estimate was 0.050; correct value is ~0.100 (all-particle) or ~0.067 (charged-particle, with ~2/3 charged fraction correction). **Fixed.**

**Finding 2 (Hardness variable):** Paper Section 2.1 states: "labelled such that p_{ta} > p_{tb}, where p_{ti} is the transverse momentum of i with respect to the colliding beams." The hardness variable is p_T w.r.t. beam, NOT energy. Strategy claimed energy ordering was "standard choice for e+e-" without citation -- no such standard exists. **Fixed:** p_T ordering adopted as primary, energy ordering as systematic variation.

**Finding 3 (Coordinate adaptation):** Paper defines k_t = p_{tb} * Delta_{ab} for pp (Eq. 2.1a), using rapidity-azimuth distance Delta = sqrt((y_a-y_b)^2 + (phi_a-phi_b)^2). Strategy uses Delta_theta = arccos(hat{p}_1 . hat{p}_2) and k_T = |p_2| * sin(Delta_theta). The sin(Delta_theta) vs Delta_theta difference is ~16% at Delta_theta = 1 rad. **Fixed:** Explicit comparison table added, cross-collider validity regime documented.

### Additional references found

**2026-03-25 17:17** -- Web search for additional Lund plane measurements:
- CMS Lund plane (JHEP 05 (2024) 116, arXiv:2312.16343): Charged-particle measurement, HEPData available
- ATLAS top/W Lund plane (arXiv:2407.10879, EPJC 2025): W-jet = colour-singlet qq analog to Z -> qq
- LHCb Lund plane (Phys. Rev. D 112 (2025) 072015, arXiv:2505.23530): Dead-cone observation in b-quark Lund plane
- Lifson/Salam/Soyez NLL predictions (JHEP 10 (2020) 170, arXiv:2007.06578): 5-7% precision at high k_T

### Fixes applied (all 5 Category A, all 16 Category B, selected Category C)

**Category A (all 5 resolved):**
1. LO formula corrected to rho = 2*alpha_s*C_F/pi. Numerical estimate updated to ~0.100 (all-particle), ~0.067 (charged). Propagated to Section 10.2, COMMITMENTS.md, F3 description.
2. Hardness variable verified against paper. p_T ordering adopted as primary [D13]. "Standard choice" claim removed. Energy ordering as systematic variation.
3. Coordinate adaptation rewritten. Sections 2.2 and 5.3 now explicitly distinguish e+e- from pp. sin(Delta_theta) usage stated. Cross-collider validity regime documented.
4. Heavy flavour systematic added to systematic table and COMMITMENTS.md. Evaluation: reweight MC b-fraction +/-2%. LHCb 2025 dead-cone evidence cited.
5. Binning: uniform justified as starting point. ATLAS/CMS/ALICE non-uniform cited. Phase 2 deliverables added (migration fraction, resolution study, population, non-uniform comparison).

**Category B (all 16 resolved):**
6. Hemisphere assignment reclassified as cross-check. Thrust-axis resolution systematic added.
7. MC reweighting limitation acknowledged. Diagnostic added (reweighting factors < 3x).
8. (Arbiter #40) Model dependence / unfolding orthogonality discussed in new Section 6.2.
9. (Arbiter #41) Efficiency correction formula clarified: C(i,j) = N_gen_before(i,j) / N_reco(i,j) using tgenBefore.
10. F5 renamed to "Correction factor map." Response matrix added to additional figures list.
11. NLL predictions cited (Lifson/Salam/Soyez 2020). Commitment to investigate numerical predictions.
12. Reference table updated with CMS 2024, ATLAS top/W 2024, LHCb 2025.
13. Published comparison data: DELPHI/ATLAS/CMS HEPData extraction committed with caveats documented.
14. Aftercut pre-selection: Phase 2 deliverable added with specific investigation items.
15. IBU promoted to co-primary method. Result will use whichever passes stress tests better.
16. Momentum resolution: TPC-only vs combined discussed. Phase 2 verification committed.
17. Neutral thrust axis: Phase 2 investigation committed to determine archived data thrust source.
18. (Arbiter #19) Stress test tilts specified: independent in ln(1/Delta_theta), ln(k_T), and 2D correlated. Functional form: w(x) = 1 + epsilon*(x - x_mean)/(x_max - x_mean).
19. (Arbiter #21) IBU response matrix clarified as proper migration probability matrix (rows sum to <= 1).
20. (Arbiter #23) Tracking efficiency: actual ALEPH per-track efficiency cited (~98.5%, NIM A 360 (1995) 481). 1% drop justified as ~1 sigma above measured inefficiency.
21. (Arbiter #26) "First" claim qualified as "first full two-dimensional primary Lund jet plane density" throughout.

**Category C (selected items applied):**
- #28: Charged-particle correction to LO prediction noted (~2/3 factor).
- #10: Secondary Lund plane feasibility noted in one sentence (Section 2.1).
- #18: Explicit discrete binned formula added to Section 2.2.
- #22: Methodology diagram added to additional figures list.
- #25: LO overlay added to F3 description.
- #29: Sherpa commitment made concrete [D14]: assess feasibility in Phase 2, document if infeasible.
