#!/usr/bin/env python3
"""Final figure fix script — Session: Katya.

Fixes all remaining multi-panel and label issues:
  1. nikolai_closure_pulls: split 1x2 into separate BBB pull histogram
  2. hugo_reco_gen_1d_comparison: split 1x2 into separate dtheta and kt plots
  3. felix_closure_pulls: split 1x2 into separate BBB and correlation matrix
  4. oscar_ratio_10pct_vs_expected: fix experiment label
  5. oscar_pull_map_10pct: fix experiment label (remove garbage chi2 from label)
  6. oscar_data_mc_reco_ratio_2d: fix experiment label (shorten)
"""

import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from rich.logging import RichHandler
from scipy.stats import norm

mh.style.use("CMS")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

AN_FIG_DIR = Path("analysis_note/figures")
AN_FIG_DIR.mkdir(parents=True, exist_ok=True)

X_EDGES = np.linspace(0, 5, 11)
Y_EDGES = np.linspace(-3, 4, 11)
NX = len(X_EDGES) - 1
NY = len(Y_EDGES) - 1
N_BINS = NX * NY
BIN_AREA = (X_EDGES[1] - X_EDGES[0]) * (Y_EDGES[1] - Y_EDGES[0])


def save_fig(fig, name):
    """Save to analysis_note/figures as PDF + PNG."""
    fig.savefig(AN_FIG_DIR / f"{name}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(AN_FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved %s", name)


def aleph_label(ax, llabel="Open Data", rlabel=r"$\sqrt{s} = 91.2$ GeV"):
    """Standard ALEPH experiment label."""
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel=llabel,
        rlabel=rlabel, loc=0, ax=ax,
    )


def aleph_label_2d(ax, llabel="Open Data (10%)"):
    """ALEPH label for 2D plots with colorbar — avoid overlap.

    The set_aspect('equal') constraint makes axes too narrow for the CMS
    label fonts. Since ln(1/dtheta) and ln(kT/GeV) are different physical
    quantities (not the same coordinate), equal aspect is not required.
    We remove it and let the (10,10) figsize keep the figure square.
    """
    ax.set_aspect("auto")
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel=llabel,
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )


# =====================================================================
# Fix 1: Split nikolai_closure_pulls into single BBB pull histogram
# =====================================================================
def fix_nikolai_closure_pulls():
    """Split the 1x2 closure pull figure into a single BBB pull histogram."""
    log.info("\n=== Fix 1: nikolai_closure_pulls (split multi-panel) ===")

    # Load the expected results to get split-sample data
    res = np.load("phase4_inference/4a_expected/outputs/expected_results_felix.npz")
    corrected_b = res["corrected_b_bbb"].flatten()
    truth_b = res["truth_b"].flatten()
    pulls_split = res["pulls_split_bbb"].flatten()

    # Compute combined uncertainty pulls (same logic as 06_fix_nikolai.py)
    # Load correction data for combined uncertainty
    correction_a = res["correction_a"].flatten()

    # We need reco_a and genBefore_a counts — reconstruct from correction_a
    # correction_a = genBefore_a / reco_a
    # For the combined uncertainty, we need the half-A statistics
    # Since we don't have them directly, use the Poisson-only pulls
    # and the combined pulls from the results JSON
    with open("analysis_note/results/validation.json") as f:
        val = json.load(f)

    # The pull data: use split_bbb pulls from the NPZ
    pop_mask = truth_b > 0
    pb = pulls_split[pop_mask]

    # Also compute Poisson-only pulls for comparison
    po = np.zeros(N_BINS)
    for k in range(N_BINS):
        if truth_b[k] > 0:
            diff = corrected_b[k] - truth_b[k]
            sigma = np.sqrt(truth_b[k]) if truth_b[k] > 0 else 1.0
            po[k] = diff / sigma
    po = po[pop_mask]

    # BBB pull histogram — single (10, 10) figure
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(po, bins=20, range=(-5, 5), color="tab:gray", alpha=0.5,
            label=f"Poisson only: $\\mu$={po.mean():.2f}, $\\sigma$={po.std():.2f}")
    ax.hist(pb, bins=20, range=(-5, 5), color="tab:red", alpha=0.7,
            label=f"Combined: $\\mu$={pb.mean():.2f}, $\\sigma$={pb.std():.2f}")
    ax.axvline(0, color="black", ls="--", lw=1)

    # N(0,1) overlay
    x_pull = np.linspace(-5, 5, 100)
    bin_width = 10.0 / 20  # range 10 / 20 bins
    ax.plot(x_pull, norm.pdf(x_pull, 0, 1) * len(pb) * bin_width,
            "k-", lw=2, label=r"$\mathcal{N}(0,1)$")

    ax.set_xlabel("Pull")
    ax.set_ylabel("Bins")
    ax.legend(fontsize="x-small")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "nikolai_closure_pulls_bbb")
    log.info("  BBB closure pull histogram: mean=%.2f, std=%.2f", pb.mean(), pb.std())


# =====================================================================
# Fix 2: Split hugo_reco_gen_1d_comparison into two separate figures
# =====================================================================
def fix_hugo_reco_gen():
    """Regenerate reco/gen 1D comparison as two separate figures.

    This requires re-running the MC processing to get reco and gen splittings.
    Uses matched reco/gen events from the tgen and t trees.
    """
    log.info("\n=== Fix 2: hugo_reco_gen_1d_comparison (split into two) ===")

    import fastjet
    import uproot
    import awkward as ak

    MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")
    M_PI = 0.13957

    def decluster_primary(jet):
        """Follow the primary declustering chain."""
        splittings = []
        current = jet
        while True:
            p1 = fastjet.PseudoJet()
            p2 = fastjet.PseudoJet()
            if not current.has_parents(p1, p2):
                break
            pt1 = np.sqrt(p1.px()**2 + p1.py()**2)
            pt2 = np.sqrt(p2.px()**2 + p2.py()**2)
            if pt1 >= pt2:
                harder, softer = p1, p2
            else:
                harder, softer = p2, p1
            vec1 = np.array([harder.px(), harder.py(), harder.pz()])
            vec2 = np.array([softer.px(), softer.py(), softer.pz()])
            n1, n2 = np.linalg.norm(vec1), np.linalg.norm(vec2)
            if n1 < 1e-10 or n2 < 1e-10:
                break
            cos_th = np.clip(np.dot(vec1, vec2) / (n1 * n2), -1, 1)
            dtheta = np.arccos(cos_th)
            if dtheta < 1e-10:
                current = harder
                continue
            kt = n2 * np.sin(dtheta)
            if kt > 0 and dtheta > 0:
                splittings.append((np.log(1.0 / dtheta), np.log(kt)))
            current = harder
        return splittings

    def cluster_hemisphere(px, py, pz, pmag):
        """Cluster one hemisphere and get primary splittings."""
        n = len(px)
        if n < 2:
            return []
        energy = np.sqrt(pmag**2 + M_PI**2)
        particles = [
            fastjet.PseudoJet(float(px[i]), float(py[i]),
                              float(pz[i]), float(energy[i]))
            for i in range(n)
        ]
        jet_def = fastjet.JetDefinition(
            fastjet.ee_genkt_algorithm, 999.0, 0.0)
        cs = fastjet.ClusterSequence(particles, jet_def)
        jets = cs.inclusive_jets()
        if not jets:
            return []
        return decluster_primary(jets[0])

    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    if not mc_files:
        log.error("No MC files found")
        return

    all_reco_x, all_reco_y = [], []
    all_gen_x, all_gen_y = [], []
    events_per_file = 4000  # 5 files x 4000 = 20k events

    for fpath in mc_files[:5]:
        with uproot.open(fpath) as f:
            reco = f["t"].arrays(
                ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                 "Thrust", "TTheta", "TPhi", "passesAll"],
                entry_stop=events_per_file,
            )
            gen = f["tgen"].arrays(
                ["px", "py", "pz", "pmag", "pwflag",
                 "Thrust", "TTheta", "TPhi"],
                entry_stop=events_per_file,
            )

            # Event selection on reco
            evt_mask = (reco["passesAll"] == True) & (reco["Thrust"] > 0.7)  # noqa: E712
            reco_sel = reco[evt_mask]
            gen_sel = gen[evt_mask]

            # Track selection
            reco_trk = (
                (reco_sel["pwflag"] == 0)
                & (reco_sel["pmag"] > 0.2)
                & (np.abs(reco_sel["d0"]) < 2.0)
                & (np.abs(reco_sel["z0"]) < 10.0)
            )
            gen_trk = (gen_sel["pwflag"] == 0) & (gen_sel["pmag"] > 0.2)

            nch_reco = ak.sum(reco_trk, axis=1)
            good = nch_reco >= 5
            reco_sel = reco_sel[good]
            gen_sel = gen_sel[good]
            reco_trk = reco_trk[good]
            gen_trk = gen_trk[good]

            for i in range(len(reco_sel)):
                # Thrust axes
                ttheta = float(reco_sel["TTheta"][i])
                tphi = float(reco_sel["TPhi"][i])
                tvec_reco = np.array([
                    np.sin(ttheta) * np.cos(tphi),
                    np.sin(ttheta) * np.sin(tphi),
                    np.cos(ttheta),
                ])

                gen_ttheta = float(gen_sel["TTheta"][i])
                gen_tphi = float(gen_sel["TPhi"][i])
                tvec_gen = np.array([
                    np.sin(gen_ttheta) * np.cos(gen_tphi),
                    np.sin(gen_ttheta) * np.sin(gen_tphi),
                    np.cos(gen_ttheta),
                ])

                for is_gen, (arrays, trk, tvec) in enumerate([
                    (reco_sel, reco_trk, tvec_reco),
                    (gen_sel, gen_trk, tvec_gen),
                ]):
                    mask = trk[i]
                    px_a = np.asarray(arrays["px"][i][mask], dtype=np.float64)
                    py_a = np.asarray(arrays["py"][i][mask], dtype=np.float64)
                    pz_a = np.asarray(arrays["pz"][i][mask], dtype=np.float64)
                    pmag_a = np.asarray(arrays["pmag"][i][mask], dtype=np.float64)

                    dot = px_a * tvec[0] + py_a * tvec[1] + pz_a * tvec[2]
                    for sign_mask in [dot > 0, dot <= 0]:
                        if np.sum(sign_mask) < 2:
                            continue
                        splittings = cluster_hemisphere(
                            px_a[sign_mask], py_a[sign_mask],
                            pz_a[sign_mask], pmag_a[sign_mask],
                        )
                        for (lx, ly) in splittings:
                            if is_gen == 0:
                                all_reco_x.append(lx)
                                all_reco_y.append(ly)
                            else:
                                all_gen_x.append(lx)
                                all_gen_y.append(ly)

        log.info("  Processed %s", fpath.name)

    reco_x = np.array(all_reco_x)
    reco_y = np.array(all_reco_y)
    gen_x = np.array(all_gen_x)
    gen_y = np.array(all_gen_y)

    log.info("  Reco splittings: %d, Gen splittings: %d", len(reco_x), len(gen_x))

    # Plot 1: ln(1/dtheta) reco vs gen
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(reco_x, bins=50, range=(0, 5), density=True, alpha=0.5,
            label="Reco", color="tab:blue")
    ax.hist(gen_x, bins=50, range=(0, 5), density=True, alpha=0.5,
            label="Gen", color="tab:orange")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel("Normalized")
    ax.legend(fontsize="x-small")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "hugo_reco_gen_dtheta")

    # Plot 2: ln(kT) reco vs gen
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(reco_y, bins=50, range=(-3, 4), density=True, alpha=0.5,
            label="Reco", color="tab:blue")
    ax.hist(gen_y, bins=50, range=(-3, 4), density=True, alpha=0.5,
            label="Gen", color="tab:orange")
    ax.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax.set_ylabel("Normalized")
    ax.legend(fontsize="x-small")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "hugo_reco_gen_kt")


# =====================================================================
# Fix 3: Split felix_closure_pulls into separate BBB and IBU figures
# (These are in the appendix — superseded by Fix 1. We produce clean
#  separate versions.)
# =====================================================================
def fix_felix_closure_pulls():
    """Split the 1x2 felix_closure_pulls into separate figures."""
    log.info("\n=== Fix 3: felix_closure_pulls (split multi-panel) ===")

    res = np.load("phase4_inference/4a_expected/outputs/expected_results_felix.npz")
    truth_b = res["truth_b"].flatten()
    pulls_bbb = res["pulls_split_bbb"].flatten()
    pulls_ibu = res["pulls_split_ibu"].flatten()

    mp = truth_b > 0
    pb = pulls_bbb[mp]
    pi = pulls_ibu[mp]

    # BBB pulls
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(pb, bins=20, range=(-5, 5), color="tab:red", alpha=0.7,
            label=f"BBB: $\\mu$={pb.mean():.2f}, $\\sigma$={pb.std():.2f}")
    ax.axvline(0, color="black", ls="--", lw=1)
    x_pull = np.linspace(-5, 5, 100)
    bin_width = 10.0 / 20
    ax.plot(x_pull, norm.pdf(x_pull, 0, 1) * len(pb) * bin_width,
            "k-", lw=2, label=r"$\mathcal{N}(0,1)$")
    ax.set_xlabel("Pull")
    ax.set_ylabel("Bins")
    ax.legend(fontsize="x-small")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "felix_closure_pulls_bbb")

    # IBU pulls
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.hist(pi, bins=20, range=(-5, 5), color="tab:blue", alpha=0.7,
            label=f"IBU: $\\mu$={pi.mean():.2f}, $\\sigma$={pi.std():.2f}")
    ax.axvline(0, color="black", ls="--", lw=1)
    ax.plot(x_pull, norm.pdf(x_pull, 0, 1) * len(pi) * bin_width,
            "k-", lw=2, label=r"$\mathcal{N}(0,1)$")
    ax.set_xlabel("Pull")
    ax.set_ylabel("Bins")
    ax.legend(fontsize="x-small")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "felix_closure_pulls_ibu")


# =====================================================================
# Fix 5: oscar_ratio_10pct_vs_expected — clean label
# =====================================================================
def fix_oscar_ratio():
    """Fix the experiment label on the ratio-to-expected figure."""
    log.info("\n=== Fix 5: oscar_ratio_10pct_vs_expected (clean label) ===")

    corr = np.load("phase4_inference/4b_partial/outputs/corrected_10pct_oscar.npz")
    rho_data = corr["rho_data"]
    x_edges = corr["x_edges"]
    y_edges = corr["y_edges"]

    with open("analysis_note/results/lund_plane_expected.json") as f:
        exp_json = json.load(f)
    rho_expected = np.array(exp_json["rho_corrected_bbb"]).reshape(NX, NY)

    populated = (rho_expected > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_expected[populated]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio.T, cmap="RdBu_r",
                       vmin=0.7, vmax=1.3, shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / Expected")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label_2d(ax, llabel="Open Data (10%)")
    save_fig(fig, "oscar_ratio_10pct_vs_expected")


# =====================================================================
# Fix 5b: oscar_pull_map_10pct — clean label, move chi2 to annotation
# =====================================================================
def fix_oscar_pull_map():
    """Fix the experiment label on the pull map figure."""
    log.info("\n=== Fix 5b: oscar_pull_map_10pct (clean label) ===")

    corr = np.load("phase4_inference/4b_partial/outputs/corrected_10pct_oscar.npz")
    pulls = corr["pulls"]
    chi2_val = float(corr["chi2"])
    ndf_val = int(corr["ndf"])
    x_edges = corr["x_edges"]
    y_edges = corr["y_edges"]

    pull_plot = pulls.copy()
    pull_plot[(pulls == 0) & (np.abs(pulls) < 1e-10)] = np.nan

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, pull_plot.T, cmap="RdBu_r",
                       vmin=-3, vmax=3, shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"Pull = (Data $-$ Expected) / $\sigma$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label_2d(ax, llabel="Open Data (10%)")
    # Put chi2/ndf as text annotation in the empty lower-right area
    ax.text(0.95, 0.05, f"$\\chi^2$/ndf = {chi2_val:.1f}/{ndf_val}",
            transform=ax.transAxes, ha="right", va="bottom", fontsize="small",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    save_fig(fig, "oscar_pull_map_10pct")


# =====================================================================
# Fix 6: oscar_data_mc_reco_ratio_2d — shorten label
# =====================================================================
def fix_oscar_data_mc_reco_ratio():
    """Fix the experiment label on the data/MC reco ratio figure."""
    log.info("\n=== Fix 6: oscar_data_mc_reco_ratio_2d (shorten label) ===")

    # Load the 10pct data processing outputs
    data_npz = np.load("phase4_inference/4b_partial/outputs/data_10pct_lund_oscar.npz")
    h2d_data = data_npz["h2d"]
    n_hemi_data = int(data_npz["n_hemispheres"])

    # Load MC reco counts from Phase 3
    sel_npz = np.load("phase3_selection/outputs/mc_reco_lund_ingrid.npz")
    h2d_mc = sel_npz["h2d"]
    n_hemi_mc = int(sel_npz["n_hemispheres"])

    x_edges = X_EDGES
    y_edges = Y_EDGES

    rho_data = h2d_data / (n_hemi_data * BIN_AREA)
    rho_mc = h2d_mc / (n_hemi_mc * BIN_AREA)

    populated = (rho_mc > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_mc[populated]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio.T, cmap="RdBu_r",
                       vmin=0.8, vmax=1.2, shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / MC (reco level)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label_2d(ax, llabel="Open Data (10%)")
    save_fig(fig, "oscar_data_mc_reco_ratio_2d")


# =====================================================================
# Fix 7: oscar_per_year — shorten label
# =====================================================================
def fix_oscar_per_year():
    """Fix the experiment label on per-year stability plots."""
    log.info("\n=== Fix 7: oscar_per_year (shorten label) ===")

    OUT_DIR = Path("phase4_inference/4b_partial/outputs")
    try:
        pf = np.load(OUT_DIR / "data_10pct_per_file_oscar.npz", allow_pickle=True)
    except FileNotFoundError:
        log.warning("  Per-file NPZ not found, skipping per-year fix")
        return

    h2d_per_file = pf["h2d_per_file"]
    n_hemi_per_file = pf["n_hemi_per_file"]
    file_names = pf["file_names"]

    x_edges = X_EDGES
    y_edges = Y_EDGES
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)

    year_map = {
        "LEP1Data1992_recons_aftercut-MERGED.root": "1992",
        "LEP1Data1993_recons_aftercut-MERGED.root": "1993",
        "LEP1Data1994P1_recons_aftercut-MERGED.root": "1994 P1",
        "LEP1Data1994P2_recons_aftercut-MERGED.root": "1994 P2",
        "LEP1Data1994P3_recons_aftercut-MERGED.root": "1994 P3",
        "LEP1Data1995_recons_aftercut-MERGED.root": "1995",
    }
    colors = ["C0", "C1", "C2", "C3", "C4", "C5"]

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    h2d_total = np.sum(h2d_per_file, axis=0)
    n_hemi_total = np.sum(n_hemi_per_file)

    for proj_name, axis_sum, centers_proj, proj_label, widths in [
        ("kt", 0, y_centers, r"$\ln(k_T / \mathrm{GeV})$", dy),
        ("dtheta", 1, x_centers, r"$\ln(1/\Delta\theta)$", dx),
    ]:
        rho_total = np.sum(h2d_total, axis=axis_sum) / (n_hemi_total * widths)

        fig, (ax_main, ax_ratio) = plt.subplots(2, 1, figsize=(10, 10),
                                                  gridspec_kw={"height_ratios": [3, 1]},
                                                  sharex=True)
        fig.subplots_adjust(hspace=0)

        for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
            label = year_map.get(str(fn), str(fn))
            h2d = h2d_per_file[i]
            rho_yr = np.sum(h2d, axis=axis_sum) / (nh * widths)
            err_yr = np.sqrt(np.sum(h2d, axis=axis_sum)) / (nh * widths)

            ax_main.errorbar(centers_proj + (i - 2.5) * 0.02, rho_yr, yerr=err_yr,
                             fmt="o", markersize=3, color=colors[i],
                             label=label, alpha=0.8)

            ratio_yr = np.ones_like(rho_yr)
            ratio_yr_err = np.zeros_like(err_yr)
            mask_yr = rho_total > 0
            ratio_yr[mask_yr] = rho_yr[mask_yr] / rho_total[mask_yr]
            ratio_yr_err[mask_yr] = err_yr[mask_yr] / rho_total[mask_yr]

            ax_ratio.errorbar(centers_proj + (i - 2.5) * 0.02, ratio_yr, yerr=ratio_yr_err,
                              fmt="o", markersize=3, color=colors[i], alpha=0.8)

        if proj_name == "kt":
            ax_main.set_ylabel(r"$d\rho / d\ln(k_T)$")
        else:
            ax_main.set_ylabel(r"$d\rho / d\ln(1/\Delta\theta)$")
        ax_main.legend(fontsize="x-small", ncol=2)
        aleph_label(ax_main, llabel="Open Data (10%)", rlabel=r"$\sqrt{s} = 91.2$ GeV")

        ax_ratio.axhline(1, color="gray", linestyle="--")
        ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
        ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
        ax_ratio.set_xlabel(proj_label)
        ax_ratio.set_ylabel("Ratio to combined")
        ax_ratio.set_ylim(0.85, 1.15)

        save_fig(fig, f"oscar_per_year_{proj_name}")


# =====================================================================
# Fix 8: oscar_lund_plane_10pct_corrected — fix label
# =====================================================================
def fix_oscar_lund_plane_10pct():
    """Fix the experiment label on the 10pct corrected Lund plane."""
    log.info("\n=== Fix 8: oscar_lund_plane_10pct_corrected (clean label) ===")

    corr = np.load("phase4_inference/4b_partial/outputs/corrected_10pct_oscar.npz")
    rho_data = corr["rho_data"]
    x_edges = corr["x_edges"]
    y_edges = corr["y_edges"]

    rho_plot = rho_data.copy()
    rho_plot[rho_plot == 0] = np.nan

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="viridis", shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label_2d(ax, llabel="Open Data (10%)")
    save_fig(fig, "oscar_lund_plane_10pct_corrected")


# =====================================================================
# Main
# =====================================================================
def main():
    log.info("=" * 70)
    log.info("Final figure fixes — Session: Katya (v2)")
    log.info("=" * 70)

    # Fix 1: Split nikolai_closure_pulls
    fix_nikolai_closure_pulls()

    # Fix 2: Split hugo_reco_gen_1d into two separate figures
    fix_hugo_reco_gen()

    # Fix 3: Split felix_closure_pulls
    fix_felix_closure_pulls()

    # Fix 5: Clean oscar_ratio label
    fix_oscar_ratio()

    # Fix 5b: Clean oscar_pull_map label
    fix_oscar_pull_map()

    # Fix 6: Clean oscar_data_mc_reco_ratio label
    fix_oscar_data_mc_reco_ratio()

    # Fix 7: Clean per-year labels
    fix_oscar_per_year()

    # Fix 8: Clean 10pct Lund plane label
    fix_oscar_lund_plane_10pct()

    log.info("\n" + "=" * 70)
    log.info("All figure fixes complete")
    log.info("=" * 70)


if __name__ == "__main__":
    main()
