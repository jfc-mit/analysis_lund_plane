#!/usr/bin/env python3
"""Final-round figure fixes — Session: Quentin.

Fixes:
  1. Fig 21 (left): Remove LO lines from reco-level projection.
     Create new corrected 1D ln(kT) projection with LO overlay.
  2. New figure: 2D relative uncertainty map.
  3. Fig 27: Annotated Lund plane with readable per-bin labels.
  4. Figs 28/29/31: Fix experiment labels (remove label abuse).
"""

import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import mplhep as mh
import numpy as np
from rich.logging import RichHandler

mh.style.use("CMS")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

BASE = Path("/n/home07/anovak/work/slopspec/analyses/lund_jet_plane")
AN_FIG_DIR = BASE / "analysis_note" / "figures"
AN_FIG_DIR.mkdir(parents=True, exist_ok=True)

X_EDGES = np.linspace(0, 5, 11)
Y_EDGES = np.linspace(-3, 4, 11)
NX = len(X_EDGES) - 1
NY = len(Y_EDGES) - 1
DX = np.diff(X_EDGES)
DY = np.diff(Y_EDGES)
BIN_AREA = np.outer(DX, DY)


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


def aleph_label_2d(ax, llabel="Open Data"):
    """ALEPH label for 2D plots — remove equal aspect to fit label."""
    ax.set_aspect("auto")
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel=llabel,
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )


# =====================================================================
# Fix 1a: Reco-level ln(kT) projection WITHOUT LO lines
# =====================================================================
def fix_hugo_kt_projection_no_lo():
    """Regenerate the reco-level kT projection without LO reference lines.

    The original hugo_lund_kt_projection.pdf had LO analytical predictions
    overlaid on uncorrected reco-level data, which is nonsensical. This
    version shows only the reco-level data points.
    """
    log.info("\n=== Fix 1a: Reco kT projection (remove LO lines) ===")

    # Load Phase 2 reco-level Lund plane data
    reco_data = np.load(BASE / "phase2_exploration" / "outputs" / "lund_reco_data_hugo.npz")
    lund_y = reco_data["lund_y"]
    n_hemispheres = int(reco_data["n_hemispheres"])

    # Use finer bins matching original exploration figure
    x_bins = np.linspace(0, 5, 26)
    y_bins = np.linspace(-3, 4, 36)
    dy = np.diff(y_bins)

    # We need to reconstruct h2d from the raw lund arrays
    lund_x = reco_data["lund_x"]
    h2d, _, _ = np.histogram2d(lund_x, lund_y, bins=[x_bins, y_bins])
    dx_fine = np.diff(x_bins)
    rho = h2d / n_hemispheres / np.outer(dx_fine, dy)

    # kT projection
    kt_proj = np.sum(rho, axis=0) * dx_fine[0]
    err = np.sqrt(np.sum(h2d, axis=0)) / n_hemispheres / dy

    fig, ax = plt.subplots(figsize=(10, 10))
    mh.histplot(
        (kt_proj, y_bins),
        ax=ax, label="Data (reco)", color="k",
        histtype="errorbar", yerr=err,
    )
    ax.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax.set_ylabel(r"$\rho$ (integrated over $\ln 1/\Delta\theta$)")
    ax.legend(fontsize="x-small")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax * 1.4)
    aleph_label(ax)
    save_fig(fig, "hugo_lund_kt_projection")

    log.info("  Reco kT projection saved (NO LO lines)")


# =====================================================================
# Fix 1b: NEW corrected 1D kT projection with LO overlay
# =====================================================================
def fix_corrected_kt_with_lo():
    """Create new corrected 1D ln(kT) projection with LO analytical overlay.

    This is the meaningful comparison: particle-level corrected density
    vs LO prediction. Uses the full-data corrected result.
    """
    log.info("\n=== Fix 1b: Corrected kT projection with LO overlay ===")

    with open(BASE / "analysis_note" / "results" / "lund_plane_full.json") as f:
        full = json.load(f)

    rho = np.array(full["rho_corrected_bbb"])
    stat_err = np.array(full["stat_uncertainty"])
    x_edges = np.array(full["bin_edges_x"])
    y_edges = np.array(full["bin_edges_y"])
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)

    # kT projection: integrate over ln(1/dtheta)
    rho_kt = np.sum(rho * dx[:, None], axis=0)
    err_kt = np.sqrt(np.sum((stat_err * dx[:, None]) ** 2, axis=0))
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    # LO predictions (from the analysis note, Eq. 7)
    # alpha_s(M_Z) = 0.1180, C_F = 4/3
    alpha_s = 0.1180
    C_F = 4.0 / 3.0
    rho_lo_all = 2.0 * alpha_s * C_F / np.pi
    rho_lo_charged = 0.67 * rho_lo_all
    # Multiply by the integration range of ln(1/dtheta) = 5 - 0 = 5
    # to get d rho / d ln(kT) = rho_LO * Delta(ln 1/dtheta) = rho_LO * 5
    # No: the 1D projection is integral of rho d(ln 1/dtheta), and in the
    # perturbative plateau rho ~= rho_LO (const), so the integral is
    # rho_LO * (range of ln(1/dtheta) where perturbative).
    # But the *horizontal lines* in the original figure were just rho_LO
    # as a reference for the plateau density. The integral will scale by
    # the x-range. For the corrected 10x10 grid:
    # The projection sums rho * dx, so for the plateau where rho ~ rho_LO:
    # sum(rho_LO * dx[i]) = rho_LO * sum(dx) = rho_LO * 5.0
    # But only bins where rho is perturbative contribute (not boundary).
    # The simplest comparison is: show rho_LO * 5 as a reference line,
    # representing the expected plateau level of the integrated projection.
    # Actually, looking at the original figure, the LO lines were drawn as
    # horizontal lines on the integrated projection at rho_LO values
    # (not multiplied by the x-range). This makes sense if we interpret
    # the projection as an average: rho_integrated / Delta_x ~ rho_LO
    # in the perturbative plateau. But the y-axis label says "integrated".
    # For clarity: show the LO reference as a band in the perturbative
    # region (ln kT > 0.5), where the projection should be rho_LO * sum(dx)
    # over perturbative x-bins. The perturbative region in ln(1/dtheta)
    # is roughly [1, 4] = 3 units. So the projected density in the
    # perturbative kT region should be ~rho_LO * 3.
    #
    # Actually the cleanest approach: plot d rho/d(ln kT) which is
    # sum_i rho(i,j) * dx_i. In the perturbative plateau,
    # rho ~ rho_LO ~ const, so d rho/d(ln kT) ~ rho_LO * (populated x range).
    # The populated x-range varies by kT bin. For high kT (perturbative),
    # it's roughly [0, 3] = 3 units (above that, triangular boundary).
    # So the reference line is rho_LO_charged * 3 ~ 0.067 * 3 = 0.20.
    #
    # But this is model-dependent. Better: just overlay a horizontal
    # line at rho_LO values and label them as "LO plateau density" with
    # a note that the comparison is meaningful in the perturbative regime.
    # The original Phase 2 figure did this on the AVERAGE not the integral.
    # To match, we should plot the same quantity. Actually the axis says
    # "rho (integrated over ln 1/dtheta)". The LO lines at 0.067 and 0.100
    # correspond to the DENSITY, not the integral. They provide a reference
    # for what the density looks like in the perturbative plateau.
    #
    # Simplest and correct: just draw horizontal lines at rho_LO values
    # in the perturbative kT region, noting they represent the plateau density.
    # The reader sees where the 1D projection crosses this reference.

    fig, ax = plt.subplots(figsize=(10, 10))

    ax.errorbar(
        y_centers, rho_kt, yerr=err_kt,
        fmt="ko", markersize=5, label="Corrected data (full)",
    )

    # LO reference lines (perturbative region only: ln kT > 0)
    perturbative_range = y_centers > 0
    ax.axhline(
        rho_lo_all * 5.0, color="red", linestyle="--", linewidth=1.5,
        label=r"LO (all) $\times \Delta\ln(1/\Delta\theta)$" + f" = {rho_lo_all * 5:.2f}",
    )
    ax.axhline(
        rho_lo_charged * 5.0, color="blue", linestyle=":", linewidth=1.5,
        label=r"LO (charged) $\times \Delta\ln(1/\Delta\theta)$" + f" = {rho_lo_charged * 5:.2f}",
    )

    ax.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax.set_ylabel(r"$\int \rho \, d\ln(1/\Delta\theta)$")
    ax.legend(fontsize="x-small", loc="upper right")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax * 1.5)
    aleph_label(ax)
    save_fig(fig, "quentin_corrected_kt_with_lo")

    log.info("  Corrected kT projection with LO overlay saved")


# =====================================================================
# Fix 2: 2D relative uncertainty map
# =====================================================================
def make_uncertainty_2d_map():
    """Create 2D map of total relative uncertainty per bin."""
    log.info("\n=== Fix 2: 2D relative uncertainty map ===")

    with open(BASE / "analysis_note" / "results" / "lund_plane_full.json") as f:
        full = json.load(f)

    rho = np.array(full["rho_corrected_bbb"])
    stat_err = np.array(full["stat_uncertainty"])
    x_edges = np.array(full["bin_edges_x"])
    y_edges = np.array(full["bin_edges_y"])

    # Load systematic uncertainties
    with open(BASE / "analysis_note" / "results" / "systematics.json") as f:
        syst = json.load(f)

    # Compute total systematic per bin (quadrature sum of all sources)
    syst_squared = np.zeros((NX, NY))
    for src_name, src_data in syst["sources"].items():
        shift = np.array(src_data["symmetric_shift"]).reshape(NX, NY)
        syst_squared += shift ** 2

    syst_err = np.sqrt(syst_squared)

    # Total uncertainty
    total_err = np.sqrt(stat_err ** 2 + syst_err ** 2)

    # Relative uncertainty
    populated = rho > 0
    rel_unc = np.full((NX, NY), np.nan)
    rel_unc[populated] = total_err[populated] / rho[populated]

    # Plot
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(
        x_edges, y_edges, rel_unc.T * 100,  # percent
        cmap="YlOrRd", shading="flat",
        vmin=0, vmax=15,
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Total relative uncertainty [%]")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    # Annotate bins with the percentage
    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])
    for i in range(NX):
        for j in range(NY):
            if populated[i, j]:
                pct = rel_unc[i, j] * 100
                color = "white" if pct > 8 else "black"
                ax.text(
                    x_centers[i], y_centers[j], f"{pct:.1f}",
                    ha="center", va="center", fontsize="xx-small",
                    color=color, fontweight="bold",
                )

    aleph_label_2d(ax)
    save_fig(fig, "quentin_lund_plane_uncertainty_2d")

    log.info("  Relative uncertainty range: %.1f%% -- %.1f%%",
             np.nanmin(rel_unc[populated]) * 100,
             np.nanmax(rel_unc[populated]) * 100)


# =====================================================================
# Fix 3: Annotated Lund plane with readable labels
# =====================================================================
def fix_annotated_lund_plane():
    """Fix the annotated Lund plane (Fig 27) with readable labels.

    - Larger text
    - 2 decimal places (0.XX)
    - Show value +- total_unc
    - Skip boundary bins with very low density
    """
    log.info("\n=== Fix 3: Annotated Lund plane (readable labels) ===")

    with open(BASE / "analysis_note" / "results" / "lund_plane_full.json") as f:
        full = json.load(f)

    rho = np.array(full["rho_corrected_bbb"])
    stat_err = np.array(full["stat_uncertainty"])
    x_edges = np.array(full["bin_edges_x"])
    y_edges = np.array(full["bin_edges_y"])

    # Load systematics for total uncertainty
    with open(BASE / "analysis_note" / "results" / "systematics.json") as f:
        syst = json.load(f)

    syst_squared = np.zeros((NX, NY))
    for src_data in syst["sources"].values():
        shift = np.array(src_data["symmetric_shift"]).reshape(NX, NY)
        syst_squared += shift ** 2
    syst_err = np.sqrt(syst_squared)
    total_err = np.sqrt(stat_err ** 2 + syst_err ** 2)

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    # Identify significant bins (density > 0.005)
    significant = rho > 0.005

    fig, ax = plt.subplots(figsize=(10, 10))

    rho_plot = rho.copy()
    rho_plot[rho_plot == 0] = np.nan

    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="viridis", shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")

    # Annotate significant bins
    n_annotated = 0
    for i in range(NX):
        for j in range(NY):
            if significant[i, j]:
                val = rho[i, j]
                unc = total_err[i, j]
                # Format: value +/- unc, both to 2 decimal places
                if val >= 0.10:
                    txt = f"{val:.2f}\n$\\pm${unc:.2f}"
                else:
                    txt = f"{val:.3f}\n$\\pm${unc:.3f}"
                # Choose color based on background
                bg = rho[i, j] / np.nanmax(rho)
                color = "white" if bg < 0.6 else "black"
                ax.text(
                    x_centers[i], y_centers[j], txt,
                    ha="center", va="center", fontsize="xx-small",
                    color=color, fontweight="bold",
                )
                n_annotated += 1

    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label_2d(ax)
    save_fig(fig, "emeric_lund_plane_full_annotated")

    log.info("  Annotated %d / %d populated bins (threshold rho > 0.005)",
             n_annotated, int(np.sum(rho > 0)))


# =====================================================================
# Fix 4a: emeric_ratio_full_vs_expected — clean label
# =====================================================================
def fix_ratio_full_vs_expected():
    """Fix experiment label on the data/expected ratio figure (Fig 28 left)."""
    log.info("\n=== Fix 4a: emeric_ratio_full_vs_expected (clean label) ===")

    corr = np.load(
        BASE / "phase4_inference" / "4c_observed" / "outputs" / "corrected_full_emeric.npz"
    )
    rho_data = corr["rho_data"]
    x_edges = corr["x_edges"]
    y_edges = corr["y_edges"]

    with open(BASE / "analysis_note" / "results" / "lund_plane_expected.json") as f:
        exp_json = json.load(f)
    rho_expected = np.array(exp_json["rho_corrected_bbb"]).reshape(NX, NY)

    populated = (rho_expected > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_expected[populated]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(
        x_edges, y_edges, ratio.T, cmap="RdBu_r", vmin=0.8, vmax=1.2, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / Expected")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    # Clean label: just ALEPH Open Data with sqrt(s)
    aleph_label_2d(ax)
    save_fig(fig, "emeric_ratio_full_vs_expected")


# =====================================================================
# Fix 4b: emeric_pull_map_full — clean label
# =====================================================================
def fix_pull_map_full():
    """Fix experiment label on the pull map (Fig 28 right)."""
    log.info("\n=== Fix 4b: emeric_pull_map_full (clean label) ===")

    corr = np.load(
        BASE / "phase4_inference" / "4c_observed" / "outputs" / "corrected_full_emeric.npz"
    )
    pulls = corr["pulls"]
    x_edges = corr["x_edges"]
    y_edges = corr["y_edges"]

    pull_plot = pulls.copy()
    zero_mask = (pulls == 0)
    pull_plot[zero_mask] = np.nan

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(
        x_edges, y_edges, pull_plot.T, cmap="RdBu_r", vmin=-5, vmax=5, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"Pull = (Data $-$ Expected) / $\sigma$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    # Clean label
    aleph_label_2d(ax)
    save_fig(fig, "emeric_pull_map_full")


# =====================================================================
# Fix 4c: emeric_pull_distribution — clean label
# =====================================================================
def fix_pull_distribution():
    """Fix experiment label on pull distribution (Fig 29)."""
    log.info("\n=== Fix 4c: emeric_pull_distribution (clean label) ===")

    from scipy import stats

    corr = np.load(
        BASE / "phase4_inference" / "4c_observed" / "outputs" / "corrected_full_emeric.npz"
    )
    pulls = corr["pulls"]

    # Reconstruct populated mask from non-zero pulls
    # (same logic as original: populated from both data and expected > 0)
    with open(BASE / "analysis_note" / "results" / "lund_plane_full.json") as f:
        full = json.load(f)
    rho = np.array(full["rho_corrected_bbb"])
    with open(BASE / "analysis_note" / "results" / "lund_plane_expected.json") as f:
        exp = json.load(f)
    rho_exp = np.array(exp["rho_corrected_bbb"]).reshape(NX, NY)

    populated = (rho > 0) & (rho_exp > 0)
    pull_vals = pulls[populated]
    n_bins = len(pull_vals)

    fig, ax = plt.subplots(figsize=(10, 10))

    bins = np.linspace(-8, 8, 33)
    ax.hist(pull_vals, bins=bins, histtype="stepfilled", alpha=0.6, color="C0", label="Pulls")

    # Overlay unit Gaussian
    x_gauss = np.linspace(-8, 8, 200)
    bin_width = bins[1] - bins[0]
    ax.plot(
        x_gauss,
        n_bins * bin_width * stats.norm.pdf(x_gauss),
        "r--", lw=2, label=r"$\mathcal{N}(0,1)$",
    )

    ax.set_xlabel("Pull")
    ax.set_ylabel("Bins")
    ax.legend(fontsize="x-small")

    # Pull statistics as text annotation (not in exp label)
    pull_mean = np.mean(pull_vals)
    pull_std = np.std(pull_vals)
    mh.label.add_text(
        f"Mean = {pull_mean:+.3f}\nStd = {pull_std:.3f}\nN = {n_bins}",
        ax=ax,
    )

    # Clean label
    aleph_label(ax)
    save_fig(fig, "emeric_pull_distribution")


# =====================================================================
# Fix 4d: emeric_data_mc_reco_ratio_2d — clean label
# =====================================================================
def fix_data_mc_reco_ratio():
    """Fix experiment label on data/MC reco ratio (Fig 31)."""
    log.info("\n=== Fix 4d: emeric_data_mc_reco_ratio_2d (clean label) ===")

    OUT_DIR = BASE / "phase4_inference" / "4c_observed" / "outputs"
    d_full = np.load(OUT_DIR / "data_full_lund_emeric.npz")
    h2d_data = d_full["h2d"]
    n_hemi_data = int(d_full["n_hemispheres"])
    x_edges = d_full["x_edges"]
    y_edges = d_full["y_edges"]

    mc_reco = np.load(BASE / "phase3_selection" / "outputs" / "mc_reco_lund_ingrid.npz")
    h2d_mc = mc_reco["h2d"]
    n_hemi_mc = int(mc_reco["n_hemispheres"])

    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    bin_area = np.outer(dx, dy)

    rho_data = h2d_data / (n_hemi_data * bin_area)
    rho_mc = h2d_mc / (n_hemi_mc * bin_area)

    populated = (rho_mc > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_mc[populated]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(
        x_edges, y_edges, ratio.T, cmap="RdBu_r", vmin=0.8, vmax=1.2, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / MC (reco level)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    # Clean label: no "Open Data / Open Simulation" etc.
    aleph_label_2d(ax)
    save_fig(fig, "emeric_data_mc_reco_ratio_2d")


# =====================================================================
# Fix 4e: emeric_cutflow_comparison — clean label
# =====================================================================
def fix_cutflow():
    """Fix experiment label on cutflow comparison."""
    log.info("\n=== Fix 4e: emeric_cutflow_comparison (clean label) ===")

    OUT_DIR = BASE / "phase4_inference" / "4c_observed" / "outputs"
    with open(OUT_DIR / "cutflow_full_emeric.json") as f:
        cf = json.load(f)
    with open(BASE / "phase3_selection" / "outputs" / "cutflow_ingrid.json") as f:
        cf_mc = json.load(f)

    data_vals = [cf["total_events_raw"], cf["total_selected"], cf["total_hemi_cut"]]
    data_effs = [v / data_vals[0] for v in data_vals]
    mc_vals = [cf_mc["mc"]["reco_total"], cf_mc["mc"]["reco_selected"], cf_mc["mc"]["reco_hemi"]]
    mc_effs = [v / mc_vals[0] for v in mc_vals]
    labels = ["Input", "After selection", "After hemi cut"]

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    x = np.arange(len(labels))
    width = 0.35

    ax_main.bar(x - width / 2, data_effs, width, label="Data (full)", color="C0", alpha=0.7)
    ax_main.bar(x + width / 2, mc_effs, width, label="MC reco", color="C1", alpha=0.7)
    ax_main.set_ylabel("Efficiency (relative to input)")
    ax_main.set_xticks(x)
    ax_main.set_xticklabels(labels, fontsize="x-small")
    ax_main.legend(fontsize="x-small")
    ax_main.set_ylim(0.8, 1.05)

    # Clean label
    aleph_label(ax_main)

    ratios = [d / m if m > 0 else 1.0 for d, m in zip(data_effs, mc_effs)]
    ax_ratio.bar(x, ratios, 0.6, color="C2", alpha=0.7)
    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.set_ylabel("Data / MC")
    ax_ratio.set_ylim(0.95, 1.05)
    ax_ratio.set_xticks(x)
    ax_ratio.set_xticklabels(labels, fontsize="x-small")

    save_fig(fig, "emeric_cutflow_comparison")


# =====================================================================
# Fix 4f: emeric_ratio_full_vs_10pct — clean label
# =====================================================================
def fix_ratio_full_vs_10pct():
    """Fix experiment label on full/10pct ratio figure."""
    log.info("\n=== Fix 4f: emeric_ratio_full_vs_10pct (clean label) ===")

    corr_full = np.load(
        BASE / "phase4_inference" / "4c_observed" / "outputs" / "corrected_full_emeric.npz"
    )
    rho_full = corr_full["rho_data"]
    x_edges = corr_full["x_edges"]
    y_edges = corr_full["y_edges"]

    corr_10 = np.load(
        BASE / "phase4_inference" / "4b_partial" / "outputs" / "corrected_10pct_oscar.npz"
    )
    rho_10 = corr_10["rho_data"]

    populated = (rho_full > 0) & (rho_10 > 0)
    ratio = np.full_like(rho_full, np.nan)
    ratio[populated] = rho_full[populated] / rho_10[populated]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(
        x_edges, y_edges, ratio.T, cmap="RdBu_r", vmin=0.9, vmax=1.1, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Full Data / 10% Data")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    aleph_label_2d(ax)
    save_fig(fig, "emeric_ratio_full_vs_10pct")


# =====================================================================
# Fix 4g: per-year stability — clean label
# =====================================================================
def fix_per_year():
    """Fix experiment labels on per-year stability figures."""
    log.info("\n=== Fix 4g: per-year stability (clean label) ===")

    OUT_DIR = BASE / "phase4_inference" / "4c_observed" / "outputs"
    try:
        pf = np.load(OUT_DIR / "data_full_per_file_emeric.npz", allow_pickle=True)
    except FileNotFoundError:
        log.warning("  Per-file NPZ not found, skipping")
        return

    h2d_per_file = pf["h2d_per_file"]
    n_hemi_per_file = pf["n_hemi_per_file"]
    file_names = pf["file_names"]

    year_map = {
        "LEP1Data1992_recons_aftercut-MERGED.root": "1992",
        "LEP1Data1993_recons_aftercut-MERGED.root": "1993",
        "LEP1Data1994P1_recons_aftercut-MERGED.root": "1994 P1",
        "LEP1Data1994P2_recons_aftercut-MERGED.root": "1994 P2",
        "LEP1Data1994P3_recons_aftercut-MERGED.root": "1994 P3",
        "LEP1Data1995_recons_aftercut-MERGED.root": "1995",
    }
    colors = ["C0", "C1", "C2", "C3", "C4", "C5"]

    x_centers = 0.5 * (X_EDGES[:-1] + X_EDGES[1:])
    y_centers = 0.5 * (Y_EDGES[:-1] + Y_EDGES[1:])

    h2d_total = np.sum(h2d_per_file, axis=0)
    n_hemi_total = np.sum(n_hemi_per_file)

    for proj_name, axis_sum, centers_proj, proj_label, widths in [
        ("kt", 0, y_centers, r"$\ln(k_T / \mathrm{GeV})$", DY),
        ("dtheta", 1, x_centers, r"$\ln(1/\Delta\theta)$", DX),
    ]:
        rho_total = np.sum(h2d_total, axis=axis_sum) / (n_hemi_total * widths)

        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, figsize=(10, 10),
            gridspec_kw={"height_ratios": [3, 1]},
            sharex=True,
        )
        fig.subplots_adjust(hspace=0)

        for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
            label = year_map.get(str(fn), str(fn))
            h2d = h2d_per_file[i]
            rho_yr = np.sum(h2d, axis=axis_sum) / (nh * widths)
            err_yr = np.sqrt(np.sum(h2d, axis=axis_sum)) / (nh * widths)

            ax_main.errorbar(
                centers_proj + (i - 2.5) * 0.02, rho_yr, yerr=err_yr,
                fmt="o", markersize=3, color=colors[i], label=label, alpha=0.8,
            )

            ratio_yr = np.ones_like(rho_yr)
            ratio_yr_err = np.zeros_like(err_yr)
            mask_yr = rho_total > 0
            ratio_yr[mask_yr] = rho_yr[mask_yr] / rho_total[mask_yr]
            ratio_yr_err[mask_yr] = err_yr[mask_yr] / rho_total[mask_yr]

            ax_ratio.errorbar(
                centers_proj + (i - 2.5) * 0.02, ratio_yr, yerr=ratio_yr_err,
                fmt="o", markersize=3, color=colors[i], alpha=0.8,
            )

        if proj_name == "kt":
            ax_main.set_ylabel(r"$d\rho / d\ln(k_T)$")
        else:
            ax_main.set_ylabel(r"$d\rho / d\ln(1/\Delta\theta)$")
        ax_main.legend(fontsize="x-small", ncol=2)
        # Clean label
        aleph_label(ax_main)

        ax_ratio.axhline(1, color="gray", linestyle="--")
        ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
        ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
        ax_ratio.set_xlabel(proj_label)
        ax_ratio.set_ylabel("Ratio to combined")
        ax_ratio.set_ylim(0.85, 1.15)

        save_fig(fig, f"emeric_per_year_{proj_name}")


# =====================================================================
# Main
# =====================================================================
def main():
    log.info("=" * 70)
    log.info("Final-round figure fixes -- Session: Quentin")
    log.info("=" * 70)

    # Fix 1a: Remove LO lines from reco-level kT projection
    fix_hugo_kt_projection_no_lo()

    # Fix 1b: New corrected kT projection with LO overlay
    fix_corrected_kt_with_lo()

    # Fix 2: 2D relative uncertainty map
    make_uncertainty_2d_map()

    # Fix 3: Annotated Lund plane with readable labels
    fix_annotated_lund_plane()

    # Fix 4a-g: Clean all experiment labels
    fix_ratio_full_vs_expected()
    fix_pull_map_full()
    fix_pull_distribution()
    fix_data_mc_reco_ratio()
    fix_cutflow()
    fix_ratio_full_vs_10pct()
    fix_per_year()

    log.info("\n" + "=" * 70)
    log.info("All fixes complete")
    log.info("=" * 70)


if __name__ == "__main__":
    main()
