# Session Log: Fabiola (Phase 1 Executor)

## Session start: 2026-03-25 16:44 UTC

### Actions taken

1. **Read methodology files**: Phase 1 CLAUDE.md, conventions/unfolding.md, methodology/03-phases.md, methodology/05-artifacts.md
2. **LEP corpus queries** (6 searches):
   - "jet substructure Lund plane Cambridge algorithm declustering" (ALEPH) -> Found cds_388806 (ALEPH subjet analysis), inspire_457159
   - "hadronic Z decay event selection thrust charged particle track cuts" (ALEPH) -> Found cds_2876991 track cuts, inspire_322679 (EEC analysis)
   - "Cambridge Aachen jet algorithm angular ordering splitting kT" -> Found inspire_1661966 (DELPHI splitting), inspire_530425 (DELPHI C/A)
   - compare_measurements: "jet substructure subjet multiplicity" -> ALEPH/DELPHI comparison
   - "ALEPH tracking efficiency systematic uncertainty" -> Found cds_2876991 systematics
   - "ALEPH Monte Carlo PYTHIA simulation" -> Found inspire_458542 (eta production, JETSET MC)
   - "systematic uncertainty hadronization PYTHIA HERWIG" -> Found inspire_515452 (DELPHI gluon fragmentation systematics)
3. **Drilled into key papers**: cds_2876991, inspire_1661966, cds_388806
4. **Data structure exploration**:
   - Wrote and ran check_data_structure.py -> Found tree structure (t, jet trees, boosted event trees)
   - Wrote and ran count_events.py -> 3,050,610 data events, 771,597 MC events (reco=gen)
   - Wrote and ran check_branches.py -> Full branch inventory including Thrust, event shapes, particle kinematics, pwflag
5. **Key findings**:
   - Data: 6 files (1992-1995), main tree "t" has 151 branches per event (px/py/pz/pt/pmag/eta/theta/phi/mass/charge/pwflag/pid/d0/z0)
   - MC: 40 files, has both reco tree "t" and gen-level trees "tgen" (199 branches) and "tgenBefore" (151 branches, before event selection)
   - Pre-computed thrust axes available: Thrust, TTheta, TPhi, plus charged-only and corrected variants
   - Pre-computed SoftDrop (zg, rg) in jet trees
   - pwflag values: 0 (charged tracks), 4 (photons), 5 (neutral hadrons), 1,2 (other)
   - Gen-level has additional pwflag=-11 (likely ISR/detector-material particles excluded at truth level)
   - Event selection flags available: passesAll, passesNTrkMin, passesSTheta, etc.
   - tgenBefore has 24,360 events vs tgen 19,158 -> event selection at gen level is applied

### Phase 1 artifact writing

6. **Wrote plan** (`plan_fabiola_2026-03-25_16-49.md`): Literature queries, sample structure, strategy outline
7. **Wrote STRATEGY.md** (`STRATEGY_fabiola_2026-03-25_16-50.md`): Full 13-section strategy document covering:
   - Observable definition with precise particle-level definition
   - Sample inventory (3.05M data, 772k MC events)
   - Two qualitatively different selection approaches (thrust hemispheres vs kT jets)
   - Full systematic uncertainty plan with conventions/unfolding.md enumeration
   - Reference analysis table (ATLAS, ALICE, DELPHI)
   - 6 flagship figures
   - Theory comparison plan (PYTHIA 8, HERWIG 7)
8. **Populated COMMITMENTS.md**: 10 systematic sources, 7 validation tests, 6 flagship figures, 4 cross-checks, 4 comparison targets
9. **Updated experiment_log.md**: All findings and decisions documented

### Self-check against Phase 1 CLAUDE.md requirements

- [x] Corpus queries executed (6 searches, 3 paper drilldowns, all cited)
- [x] Backgrounds classified (tau-tau irreducible < 0.1%, two-photon reducible < 0.01%, Bhabha/beam-gas instrumental, negligible)
- [x] >= 2 qualitatively different selection approaches (thrust hemispheres vs kT jets)
- [x] MVA infeasibility documented with [D6] label (no background to separate, one-dimensional quality metric)
- [x] Systematic plan enumerates EVERY source in conventions/unfolding.md
- [x] Reference analysis table: 3 analyses (ATLAS, ALICE, DELPHI) with systematic programs
- [x] Method parity: IBU implemented as cross-check matching modern ATLAS/ALICE
- [x] Constraint [A], limitation [L], and decision [D] labels defined
- [x] Flagship figures (~6) identified
- [x] Correction strategy defined (bin-by-bin primary, IBU cross-check)
- [x] Theory comparison independence verified (standalone generators at truth level)
