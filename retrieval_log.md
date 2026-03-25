# Retrieval Log

## Phase 1: Strategy (Fabiola, 2026-03-25)

### LEP corpus queries

| # | Query | Tool | Mode | Results | Key findings |
|---|-------|------|------|---------|-------------|
| 1 | "jet substructure Lund plane Cambridge algorithm declustering" (ALEPH) | search_lep_corpus | hybrid | cds_388806 (ALEPH subjet analysis), inspire_457159 | ALEPH ~3M event subjet multiplicity with Durham algorithm; multiplicative detector correction method |
| 2 | "hadronic Z decay event selection thrust charged particle track cuts" (ALEPH) | search_lep_corpus | hybrid | cds_2876991, inspire_322679 | Standard ALEPH track cuts (p>200 MeV/c, d0<2 cm, z0<10 cm, ntpc>=4); event selection (Nch>=5, Ech>15 GeV, missP<20 GeV, cos_theta_sph<0.82) |
| 3 | "Cambridge Aachen jet algorithm angular ordering splitting kT" | search_lep_corpus | hybrid | inspire_1661966, inspire_530425 | DELPHI jet splitting probability with Durham kT; splitting probability density as 1D Lund projection |
| 4 | "jet substructure subjet multiplicity" | compare_measurements | -- | ALEPH vs DELPHI comparison | Cross-experiment comparison of subjet analyses; consistent methodologies |
| 5 | "ALEPH tracking efficiency systematic uncertainty" | search_lep_corpus | hybrid | cds_2876991 | Tracking systematic ~0.7% from TPC hit variation |
| 6 | "ALEPH Monte Carlo PYTHIA simulation" / "systematic uncertainty hadronization PYTHIA HERWIG" | search_lep_corpus | hybrid | inspire_458542, inspire_515452 | JETSET MC for e+e-; DELPHI gluon fragmentation systematic methodology (JETSET vs HERWIG vs ARIADNE) |

### Paper drilldowns

| # | Paper ID | Tool | Key content extracted |
|---|----------|------|---------------------|
| 1 | cds_2876991 | get_paper | ALEPH QGP search with same archived data; track cuts, event selection, efficiency corrections, tracking systematic 0.7% |
| 2 | inspire_1661966 | get_paper | DELPHI modified differential one-jet rate; Durham kT splitting; bin-by-bin correction from JETSET; CA = 2.8 +/- 0.8 * CF |
| 3 | cds_388806 | get_paper | ALEPH quark/gluon subjet multiplicity; ~3M events, Durham algorithm, multiplicative correction, MC model systematics (JETSET vs HERWIG vs ARIADNE) |

### Modern methodology search

Modern Lund plane analyses identified from prompt context (not from LEP corpus):
- ATLAS, Phys. Rev. Lett. 124 (2020) 222002 -- First Lund plane measurement in pp collisions at 13 TeV. Used Bayesian iterative unfolding. Dominant systematic: MC model dependence (5-30%).
- ALICE, JHEP 05 (2024) 116 -- Lund plane in pp and Pb-Pb at 5.02 TeV. Used 2D Bayesian unfolding. Dominant systematic: MC model (5-15%).

These modern references motivated the IBU cross-check (matching ATLAS/ALICE methodology) alongside the primary bin-by-bin correction (matching LEP-era practice).

### Failed retrievals

None. All queries returned relevant results.
