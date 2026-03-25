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
