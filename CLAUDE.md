<!-- Spec developer note: agent prompt templates live in
     src/methodology/appendix-prompts.md. Context assembly rules are in
     src/methodology/03a-orchestration.md §3a.4. -->

# Analysis: lund_jet_plane

Type: measurement

**Sections:** Execution Model / Methodology / Environment / Tool
Requirements / Phase Gates / Review Protocol / Phase Regression / Coding
Rules / Scale-Out / Plotting / Conventions / Analysis Note Format /
Feasibility / Reference Analyses / Pixi Reference / Git

---

## Execution Model

**You are the orchestrator.** You do NOT write analysis code yourself. You
delegate to subagents. Your context stays small; heavy work happens in
subagent contexts.

**Progress tracking (mandatory).** Before any phase work, create a task
list showing all phases with their execution pipeline and review tier.
Use this exact structure:

```
Phase 1: Strategy — executor + 4-bot review
Phase 2: Exploration — executor + self + plot validator
Phase 3: Selection — executor + 1-bot + plot validator
Phase 4a: Inference (expected) — executor + 1-bot + plot validator [blocking]
  Doc 4a: AN writing (full AN in LaTeX) — note writer + 5-bot+bib review
Phase 4b: Inference (10% data) — executor + 1-bot + plot validator [blocking]
  Doc 4b: AN update (10% results) — note writer + 5-bot+bib review + human gate
Phase 4c: Inference (full data) — executor + 1-bot + plot validator [blocking]
  Doc 4c: AN update (full results) — note writer + 5-bot+bib review = FINAL
```

Inference phases (4a/4b/4c) produce physics results. Doc phases produce
the analysis note. These are separated because inference is physics work
and documentation is editorial work — different agents, different reviews.

The 1-bot review at each inference phase is BLOCKING — Doc phases cannot
start until the inference review passes. This catches physics errors
before the note writer builds an AN around wrong results.

All Doc phases get 5-bot+bib review. The review is NEVER lighter at
Doc 4b or Doc 4c.

**All executor subagents start in plan mode.** When spawning an executor,
instruct it to first produce a plan: what scripts it will write, what figures
it will produce, what the artifact structure will be. The subagent executes
only after the plan is set. This prevents agents from diving into code
without thinking.

**Agent definitions (mandatory).** Before spawning any subagent, the
orchestrator MUST read the agent's definition from `agents/{role}.md`.
Each definition contains: role description, reads/writes spec, methodology
references, and a prompt template. Use the prompt template as the basis
for the subagent's instructions — do NOT write ad-hoc prompts from scratch.
Add phase-specific context (physics prompt, data paths, upstream artifact
paths) on top of the template. See `agents/README.md` for the index and
phase activation matrix.

The orchestrator may still spawn ad-hoc subagents for tasks not covered by
the defined roles (e.g., one-off data exploration, debugging). But every
role listed in `agents/README.md` must use its definition file.

**The orchestrator loop:**

```
for each phase in [1, 2, 3]:
  EXECUTE → VERIFY → REVIEW → CHECK → COMMIT → ADVANCE
  (standard loop — see review tiers above for panel composition)

for each inference+doc pair in [(4a, Doc 4a), (4b, Doc 4b), (4c, Doc 4c)]:

  1. INFERENCE — spawn executor for inference phase (4a/4b/4c)
     - Phase CLAUDE.md from phase4_inference/{subphase}/
     - Produces inference artifact + results JSON + figures
     - VERIFY completion before review (see below)

  2. INFERENCE REVIEW — 1-bot + plot validator [blocking]
     - Critical reviewer checks physics correctness
     - Plot validator checks all figures
     - Must PASS before Doc phase begins

  3. DOC — spawn note writer for Doc phase
     - Doc phase CLAUDE.md from analysis_note/review/{doc_phase}/
     - Doc 4a: writes full AN from LaTeX template
     - Doc 4b/4c: updates existing AN with new results
     - Produces .tex + compiled .pdf
     - VERIFY completion before review (see below)

  4. DOC REVIEW — 5-bot+bib (same panel at all Doc phases)
     - Physics + critical + constructive + plot validator +
       rendering + bibtex → arbiter

  5. CHECK — read arbiter verdict. Handle ITERATE/ESCALATE
     as in the standard loop (fix → fresh re-review → repeat).

  6. COMMIT

  7. HUMAN GATE (after Doc 4b only):
     Present the compiled PDF to the human. Pause until approved.

  8. ADVANCE to next inference+doc pair.
```

**Completion verification (VERIFY step).** When an executor or note writer
first signals completion, the orchestrator does NOT proceed to review.
Instead, send one follow-up message to the still-running agent:

> You are not done yet. Re-read your plan.md line by line. For each
> planned item, verify it is implemented — not just started, DONE.
> Then run every checkbox in the pre-review self-check from your phase
> CLAUDE.md. If anything is incomplete or fails a check, finish it now.
> Only when every planned item is done and every self-check box passes
> may you signal completion again.

The agent continues working until it passes its own plan and self-check,
then signals completion a second time. After the plan/checklist pass, send
a second follow-up — the **self-critique**:

> Now switch to critic mode. Re-read your own figures and artifact as if
> you are a skeptical referee who did NOT produce this work. For each
> figure: what would you criticize? For each major claim: is the evidence
> convincing, or merely asserted? Fix what you find, then signal final
> completion.

This leverages a fundamental property: **LLMs are better at evaluating
than generating.** The executor already knows what's wrong with its
output — it just needs to look at it with a critical framing instead
of a production framing. This step typically catches 3-5 issues per
phase that would otherwise require a full review-iterate cycle. The
cost is one more message exchange while context is still warm.

Only after the self-critique does the orchestrator proceed to review.
Do NOT skip these steps to save tokens — they prevent entire review
rounds.

**Maximality check.** After review PASS, before advancing to the next
phase, the orchestrator checks: is there feasible work the agent didn't
do? Concrete checks:
- Read the experiment log for items flagged as "could improve" or
  "future work" — apply the §12 feasibility test (<2 hours?).
- Check for handoff documents (`outputs/HANDOFF_*.md`) that need
  follow-up agents.
- Check whether all available data/MC was processed.
- For Doc phases: read the Future Directions section — any item that
  could be done now triggers a follow-up agent, not a PASS.

If feasible work remains, spawn a fresh agent with a handoff document
or send the existing agent back to implement. The goal is not just
completion but **maximality** — the strongest result the data and
infrastructure can support.

**Regression during Doc review.** If a Doc phase review triggers
regression to an earlier phase, the orchestrator:
1. Spawns Investigator → REGRESSION_TICKET.md
2. Decides UPDATE vs REWRITE (see methodology/06-review.md §6.7)
3. Fixes origin phase, re-runs affected inference phases
4. Restarts from the Doc phase corresponding to the earliest affected
   inference phase
5. The Doc agent either UPDATEs the existing AN (narrow regression) or
   REWRITEs from current artifacts (deep regression)

**Phase 4 + Doc flow (both measurements and searches):**
All three inference sub-phases (4a → 4b → 4c) and their corresponding
Doc phases are required for both analysis types.
- **4a → Doc 4a:** Inference produces expected results + figures. Doc 4a
  writes the COMPLETE AN in LaTeX (from template), compiles PDF. This is
  the heavy lift — all 13 sections, all figures composed, full structure.
  5-bot+bib review. PDF compilation mandatory before review.
- **4b → Doc 4b:** Inference produces 10% results. Doc 4b updates the
  existing AN (replaces \tbd{} placeholders, regenerates comparison
  figures). 5-bot+bib review → human gate. Human reviews the compiled PDF.
- **4c → Doc 4c:** Inference produces full results. Doc 4c updates the
  AN with final results. 5-bot+bib review. This is the final deliverable.

**Systematic variation sizing:** Every systematic variation must be
motivated by a measurement or published uncertainty. "±50% on the
background" is Category A unless 50% IS the measured uncertainty. Use
the actual uncertainty from the background estimation method (sideband
fit uncertainty, MC normalization uncertainty, data-driven closure).
Arbitrary conservative inflations mask the analysis's true sensitivity.

**Inference/Doc separation:** Inference phases (4a/4b/4c) and Doc phases
are already separated — different agents, different directories, different
reviews. The inference executor does physics. The Doc note writer writes
prose. This separation prevents context pressure from forcing compromises.

**Session naming (mandatory).** Every subagent must be assigned a unique
session name from the name pool in `methodology/appendix-sessions.md`.
Include the assigned name in the subagent's prompt:
`"Your session name is {name}. Use it when naming output files."`
The agent uses this name for all output files (artifacts, reviews, logs)
per the `{ARTIFACT}_{session_name}_{timestamp}` convention. Never reuse
a name within an analysis run. This enables traceability — when reading
an artifact, humans and agents can trace who produced it. See
`methodology/appendix-sessions.md` for the full naming protocol and the
name pool.

**Anti-patterns:**
- Running straight from Phase 1 to Doc 4c with no intermediate artifacts
- The orchestrator writing analysis scripts itself
- Writing a workaround when a maintained tool exists — `pixi add` it instead
- Accepting reviewer PASS too easily — the arbiter should ITERATE liberally
- Spawning subagents without `model: "opus"` — this silently degrades quality.
  **Every subagent — executor, reviewer, arbiter, fixer, note writer — must
  be spawned with `model: "opus"`. No exceptions. Sonnet or Haiku silently
  degrades physics reasoning and review quality.**
- Subagents reading files with `cat | sed | head` instead of the Read tool
- **Writing ad-hoc prompts for defined agent roles** — read `agents/{role}.md`
  and use its prompt template. Ad-hoc prompts drift from the spec, miss
  important checks (e.g., plot validator red flags), and are not auditable

**What the orchestrator does NOT do:**
- Read full scripts or data files (subagents do this)
- Debug code (subagents do this)
- Produce figures (subagents do this)
- Write analysis prose (subagents do this)

**What the orchestrator MUST do:**
- **Log the initial prompt.** Before any phase work, write the user's
  physics prompt (the research question / analysis goal) to `prompt.md`
  in the analysis root. This is the first action — the prompt is the
  analysis's founding document and must be on disk for audit, subagent
  context assembly, and reproducibility.
- **Health monitoring.** Commit before spawning each subagent. Check progress
  every ~5 minutes for long-running subagents. Respawn stalled agents from
  the last commit (if no commit in >10 minutes and no progress, terminate
  and respawn). When background/non-blocking agent spawning is available,
  use it for long-running subagents (Phase 3 processing, Phase 4 systematic
  evaluation, Doc phase AN writing) to enable monitoring and respawning.
- **Crash recovery.** When respawning a stalled or crashed agent:
  (1) read the session log (`logs/`) to determine what was accomplished,
  (2) read any partial artifact on disk, (3) tell the replacement agent
  what its predecessor accomplished (from the session log) and instruct it
  to continue from that point, not restart from scratch. If no session log
  exists, the agent produced nothing — restart from scratch.
- Ensure review quality. Do NOT conserve tokens by accepting weak reviews
  or rushing past issues. If a reviewer finds problems, have the work redone
  properly — not minimally patched.
- Trigger phase regression when ANY review finds physics issues traceable
  to an earlier phase.
- **Regression checklist (mandatory after every review).** After reading
  the arbiter's verdict, the orchestrator must independently evaluate:
  - [ ] Any validation test failures without 3 documented remediation attempts?
  - [ ] Any single systematic > 80% of total uncertainty?
  - [ ] Any GoF toy distribution inconsistent with observed chi2?
  - [ ] Any flat-prior gate excluding > 50% of bins?
  - [ ] Any tautological comparison presented as independent validation?
  - [ ] Any visually identical distributions that should be independent?
  - [ ] Any result with > 30% relative deviation from a well-measured
        reference value (§6.8 — triggers calibration investigation)?
  - [ ] All binding commitments [D1]-[DN] from the strategy fulfilled?
        Re-read STRATEGY.md decision labels. A decision committed in
        Phase 1 but silently replaced with an alternative approach is
        Category A — even if the alternative is reasonable, because the
        decision was never formally revised. Common failure: strategy
        commits to published luminosities [D], executor back-calculates
        from data instead, making the fit circular.
  - [ ] Is the fit chi2 identically zero (or within numerical precision)?
        If so, investigate whether the methodology is algebraically
        circular before accepting. chi2 = 0.000 is an alarm, not a
        result. See Phase 4c "Fit triviality gate" in §3.
  If ANY box is checked, the orchestrator must trigger regression or
  re-run the affected phase — even if the arbiter said PASS. The
  orchestrator is the last line of defense against process failures.

**Subagent model selection:** All subagents — executors, reviewers, arbiters,
fix agents — must be spawned with `model: "opus"`. Never use Sonnet or Haiku
for any analysis subagent. This is non-negotiable.

**Subagent file reading:** Instruct all subagents to use the Read tool to
read files in full (no line limits). Never use `cat`, `sed`, `head`, or
`tail` to read files in chunks — the Read tool handles files of any size
and gives the subagent the complete content.

---

## Methodology

Read relevant sections from `methodology/` as needed:

| Topic | File | When |
|-------|------|------|
| Phase definitions | `methodology/03-phases.md` | Before each phase |
| Orchestration | `methodology/03a-orchestration.md` | Orchestrator planning |
| Blinding | `methodology/04-blinding.md` | Phase 4 |
| Artifacts | `methodology/05-artifacts.md` | Writing phase artifacts |
| Analysis note spec | `methodology/analysis-note.md` | Doc phases (writing AN) |
| Review protocol | `methodology/06-review.md` | Spawning reviewers |
| Tools & paradigms | `methodology/07-tools.md` | Coding phases |
| Coding practices | `methodology/11-coding.md` | Coding phases |
| Downscoping | `methodology/12-downscoping.md` | Hitting limitations |
| Plotting | `methodology/appendix-plotting.md` | All figure-producing phases |
| Checklist | `methodology/appendix-checklist.md` | Review, Doc phases |

---

## Environment

This analysis has its own pixi environment defined in `pixi.toml`.
All scripts must run through pixi:

```bash
pixi run py path/to/script.py          # run a script
pixi run py -c "import uproot; ..."     # quick check
pixi shell                              # interactive shell with all deps
```

**Never use bare `python`, `pip install`, or `conda`.** If you need a
package, add it to `pixi.toml` and run `pixi install`. Never use system
calls to install packages.

---

## Numeric Constants: Never From Memory

**Every number that enters the analysis must come from a citable source.**
PDG masses, widths, coupling constants, world-average measurements,
QCD coefficients, radiative correction formulae — all must be fetched
from the RAG corpus, web (PDG live tables, HEPData), or a cited paper.

LLM training data is NOT a source. Quote $M_Z = 91.1876$ GeV? Cite
where it came from. Use $\alpha_s = 0.1180$? Fetch and cite. Use the
QCD correction coefficient 1.405? Cite the paper.

**At review, any uncited numeric constant is Category A.**

See `methodology/02-inputs.md` §2.3 for the full policy.

---

## Tool Requirements

Non-negotiable. Use these — not alternatives.

| Task | Use | NOT |
|------|-----|-----|
| ROOT file I/O | `uproot` | PyROOT, ROOT C++ macros |
| Array operations | `awkward-array`, `numpy` | pandas (for HEP event data) |
| Histogramming | `hist`, `boost-histogram` | ROOT TH1, numpy.histogram (for filling) |
| Plotting | `matplotlib` + `mplhep` | ROOT TCanvas, plotly |
| Statistical model | `pyhf` (binned), `zfit` (unbinned) | RooFit, RooStats, custom likelihood code |
| Jet clustering | `fastjet` (Python) | manual clustering |
| Logging | `logging` + `rich` | `print()` — never use bare print |
| Document prep | `tectonic` | pandoc, pdflatex |
| Dependency mgmt | `pixi` | pip, conda |

**Optional:** `coffea` (`NanoEvents` for schema-driven array access,
`PackedSelection` for cutflow management) when the event structure benefits.

---

## Phase Gates

Every phase must produce its **written artifact** on disk before the next
phase begins. No exceptions.

| Phase | Required artifact | Review type |
|-------|-------------------|-------------|
| 1 | `phase1_strategy/outputs/STRATEGY.md` | 4-bot |
| 2 | `phase2_exploration/outputs/EXPLORATION.md` | Self + plot-val |
| 3 | `phase3_selection/outputs/SELECTION.md` | 1-bot + plot-val |
| 4a | `phase4_inference/4a_expected/outputs/INFERENCE_EXPECTED.md` + `results/*.json` | 1-bot + plot-val |
| Doc 4a | `analysis_note/ANALYSIS_NOTE_doc4a_v1.{tex,pdf}` | 5-bot+bib |
| 4b | `phase4_inference/4b_partial/outputs/INFERENCE_PARTIAL.md` + `results/*.json` | 1-bot + plot-val |
| Doc 4b | `analysis_note/ANALYSIS_NOTE_doc4b_v1.{tex,pdf}` | 5-bot+bib → human gate |
| 4c | `phase4_inference/4c_observed/outputs/INFERENCE_OBSERVED.md` + `results/*.json` | 1-bot + plot-val |
| Doc 4c | `analysis_note/ANALYSIS_NOTE_doc4c_v1.{tex,pdf}` | 5-bot+bib |

**Review before advancing.** After each artifact, spawn a reviewer subagent.
Self-review is only acceptable for Phase 2 (exploration). All other phases
require independent reviewer agents. Write findings to
`phase*/review/{role}/` using session-named files.

**Experiment log.** Append to `experiment_log.md` throughout. An empty
experiment log at the end of a phase is a process failure.

**`all` task.** `pixi.toml` must have an `all` task that runs the full
analysis chain. Update it whenever scripts are added.

---

## Review Protocol

See `methodology/06-review.md` for the full protocol. Key rules:

**Classification:** **(A) Must resolve** — blocks advancement. **(B) Must fix before PASS** — weakens the analysis. **(C) Suggestion** — applied before commit, no re-review.

The arbiter must not PASS with unresolved A or B items.

| Phase | Review type |
|-------|-------------|
| 1: Strategy | 4-bot |
| 2: Exploration | Self + plot validator |
| 3: Processing | 1-bot + plot-val |
| 4a: Inference (expected) | 1-bot + plot-val [blocking] |
| Doc 4a: AN (expected) | 5-bot+bib |
| 4b: Inference (10%) | 1-bot + plot-val [blocking] |
| Doc 4b: AN (10%) | 5-bot+bib → human gate |
| 4c: Inference (full) | 1-bot + plot-val [blocking] |
| Doc 4c: AN (full) | 5-bot+bib (final) |

**Iteration limits:** 4/5-bot: warn at 3, strong warn at 5, hard cap at 10. 1-bot: warn at 2, escalate after 3. All subagents use `model: "opus"`.

**Validation target rule (§6.8):** Any result with a pull > 3-sigma from a
well-measured reference value (PDG, published measurement) is **Category A**
unless the reviewer verifies: (1) a quantitative explanation for the
deviation, (2) a demonstrated magnitude match (calculation/toy/fit variant),
and (3) no simpler explanation (bugs, sign errors). A narrative list of
"possible causes" does not satisfy this rule. Applies at Phases 4a–Doc 4c.

---

## Phase Regression

When a reviewer at Phase N finds a **physics issue** traceable to Phase M < N,
this triggers regression. See `methodology/06-review.md` §6.7 for the full protocol.

**Regression trigger:** Spawn an Investigator to trace impact →
`REGRESSION_TICKET.md` → fix origin phase → re-run affected downstream →
resume review.

**Concrete triggers (must not be rationalized away):**
- Data/MC disagreement on observable or MVA inputs
- Closure test failure (p < 0.05)
- Stress test failure without successful remediation (3+ attempts required)
- Operating point instability
- Unexplained dominant systematic (single source > 80% of total)
- Result > 3-sigma from a well-measured reference value (§6.8)
- GoF toy distribution inconsistent with observed chi2 (outside 95% interval)
- Wholesale bin exclusion (> 50% of bins excluded by flat-prior gate or
  similar criterion)
- Two distributions that should be independent appear visually identical

**Not regression (local fix):** Axis labels, captions, current-phase code bugs
→ normal Category A fix-and-re-review cycle.

**Arbiter dismissal rule:** The arbiter may NOT dismiss reviewer findings
as "out of scope" if the fix requires less than ~1 hour of agent time.
Re-running a Phase 4 script with different parameters is NOT out of scope.
When multiple findings require upstream reprocessing, batch them into a
single regression iteration. See `methodology/06-review.md` §6.5.1.

---

## Human Gate Protocol

After the Doc 4b 5-bot+bib review returns PASS, present the **compiled
PDF** to the human along with the unblinding checklist. Do NOT proceed
to Phase 4c without explicit human approval.

The human may respond with:
- **APPROVE** — proceed to Phase 4c (inference on full data)
- **ITERATE** — fix specific issues within 4b scope, re-review, re-present
- **REGRESS(N)** — fundamental issue traced to Phase N (see
  `methodology/06-review.md` §6.6 for the full non-destructive regression
  protocol)
- **PAUSE** — wait for external input

**On REGRESS:** Spawn the Investigator to assess cascade scope. Fix the
origin phase non-destructively (new artifact versions, not overwrites).
Re-evaluate each downstream phase. After regression, the note writer
must produce a new AN version that tells a cohesive physics story —
the body text reflects the current analysis, the Change Log records
what changed. Re-present the updated PDF to the human.

See `methodology/06-review.md` §6.6 for the full protocol.

---

## Coding Rules

- **Columnar analysis.** Arrays, not event loops. Selections are boolean masks.
- **Prototype on a slice.** ~1000 events first, full data only for production.
- **No bare `print()`.** Use `logging` + `rich`. Ruff T201 enforces this.
- **Conventional commits.** `<type>(phase): <description>`.
- **Scripts as pixi tasks.** Every script gets a named task in `pixi.toml`.
  The `all` task runs the full chain.
- **KISS / YAGNI.** No CLIs, config systems, or plugin architectures. Write scripts.

Standard logging setup:
```python
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)
```

See `methodology/11-coding.md` for full coding practices.

---

## Scale-Out Rules

**Always estimate before running at full scale.** Check input size, time a
1000-event slice, extrapolate.

| Estimated time | Action |
|---|---|
| < 2 min | Single-core local — just run it |
| 2–15 min | `ProcessPoolExecutor` or equivalent multicore |
| > 15 min | SLURM: `sbatch --wait` (single) or `--array` (per-file) |

---

## Plotting Rules

See `methodology/appendix-plotting.md` for full plotting standards. Essentials:

- **Style:** `import mplhep as mh; mh.style.use("CMS")` (CMS style is the default mplhep preset — clean, widely used)
- **Experiment label:** On every figure (mandatory). For open/archived data:
  - Data: `mh.label.exp_label(exp="<EXPERIMENT>", data=True, llabel="Open Data", rlabel=r"$\sqrt{s} = X$ GeV", loc=0)`
  - MC: `mh.label.exp_label(exp="<EXPERIMENT>", data=True, llabel="Open Simulation", rlabel=r"$\sqrt{s} = X$ GeV", loc=0)`
  - On main panel only — never on ratio panels.
- **Figure size:** `figsize=(10, 10)` for all single-panel and ratio plots.
- **No matplotlib grid plots.** Produce individual `(10, 10)` figures and
  compose in the AN with LaTeX subfigures. Exception: ratio plots and
  tightly-coupled panels that share axes (`sharex=True`, `hspace=0`).
- **Ratio plot spacing:** `fig.subplots_adjust(hspace=0)` is non-negotiable.
  Any visible gap between main and ratio panels is Category A.
- **AN rendering:** Single-panel figures render at `0.45\linewidth` (default).
  Multi-panel figures composed in LaTeX render at `\linewidth`.
- **No titles.** Never `ax.set_title()`. Captions go in the analysis note.
- **No absolute font sizes.** The CMS stylesheet sets sizes. Use `'x-small'` for legends.
- **Save as PDF + PNG.** `bbox_inches="tight"`, `dpi=200`, `transparent=True`. Close after saving.
- **Figures in artifacts:** `![Detailed caption](figures/name.pdf)` (in
  markdown artifacts). In the AN (LaTeX), use `\includegraphics` inside
  `\begin{figure}` environments.
- **Self-lint before committing.** Run `pixi run lint-plots` to catch
  Category A violations before review. See executor agent prompt for checklist.

---

## Conventions

Read applicable files in `conventions/` at three mandatory checkpoints:

1. **Phase 1 (Strategy):** Read all applicable conventions before writing
   the systematic plan. Enumerate every required source with "Will implement"
   or "Not applicable because [reason]."
2. **Phase 4a (Inference):** Re-read conventions before finalizing
   systematics. Produce a completeness table comparing sources against
   conventions AND reference analyses.
3. **Doc 4c (Final documentation):** Final conventions check — verify everything
   required is present in the analysis note.

If a convention requires something you plan to omit, justify explicitly.

**Which conventions apply:**

| Analysis technique | Read these files |
|--------------------|-----------------|
| Unfolded measurement (IBU, SVD, TUnfold, OmniFold, bin-by-bin) | `conventions/unfolding.md` |
| Extraction measurement (double-tag, ratio, branching fraction, counting) | `conventions/extraction.md` |
| Search / limit-setting | `conventions/search.md` |

If unsure, the technique selection in Phase 1 determines which file applies.
Read the "When this applies" section of each candidate file to confirm.
Ignore `conventions/TEMPLATE.md` — it is a skeleton for spec developers
creating new conventions files.

---

## Analysis Note Format

**The gold standard:** a physicist who has never seen the analysis should
be able to reproduce every number from the AN alone. If they need to read
the code, the AN has a gap. Target 50-100 pages; under 30 is Category A.

The analysis note is written **directly in LaTeX** (no pandoc conversion).
The note writer starts from `conventions/an_template.tex` and compiles
with `tectonic`.

- **LaTeX math:** `$...$` inline, `\begin{equation}...\end{equation}` display.
- **Figures:** `\includegraphics[height=0.45\linewidth]{figures/name.pdf}`
  inside `\begin{figure}[htbp]...\end{figure}`. Captions must be 2-5
  sentences. See `conventions/an_template.tex` for compositing patterns
  (pair, 2x2, 3-column).
- **Tables:** `\begin{table}[htbp]\begin{tabular}...\end{tabular}\end{table}`
  with `\toprule/\midrule/\bottomrule` (booktabs).
- **Cross-references:** `\label{fig:name}` / `Figure~\ref{fig:name}`.
- **Citations:** `\cite{key}` with `references.bib` at analysis root.
- **Placeholders:** `\tbd{description}` for future-phase values (Doc 4a
  uses this for 10%/full data columns in results tables).

Required AN sections — see `methodology/analysis-note.md` for the full
specification including depth calibration and completeness test.

---

## Feasibility Evaluation

When the analysis encounters a limitation, do not silently downscope.
See `methodology/12-downscoping.md` for the full evaluation protocol.

---

## Reference Analyses

To be filled during Phase 1. The strategy must identify 2-3 published
reference analyses and tabulate their systematic programs. This table is
a binding input to Phase 4 and Doc phase reviews.

---

## Pixi Reference

Common patterns and pitfalls for `pixi.toml`:

```toml
# === Structure ===
[workspace]
name = "my-analysis"
channels = ["conda-forge"]
platforms = ["linux-64"]

# Conda packages (compiled, from conda-forge)
[dependencies]
python = ">=3.11"
tectonic = ">=0.15"

# Python packages (from PyPI)
[pypi-dependencies]
uproot = ">=5.0"
numpy = ">=1.24"

# Named tasks
[tasks]
py = "python"
select = "python phase3_selection/src/apply_selection.py"
all = "python phase3_selection/src/apply_selection.py && ..."
```

**Common pitfalls:**
- PyPI packages go in `[pypi-dependencies]`, NOT `[dependencies]`.
- After editing `pixi.toml`, run `pixi install` to update the environment.
- Task values are shell command strings. Chain with `&&` for sequential.
- The `py` task (`py = "python"`) lets you run arbitrary scripts.

---

## Git

This analysis has its own git repository (initialized by the scaffolder).
Commit work within this directory. Do not modify files outside this
directory — the spec repository is separate.
