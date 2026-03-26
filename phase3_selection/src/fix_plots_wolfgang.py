#!/usr/bin/env python3
"""Fix Script: Phase 3 2D plots — square aspect ratio (Issue #2).

Regenerates all Phase 3 2D Lund plane plots with ax.set_aspect('equal')
and proper colorbar handling via make_square_add_cbar.

Also fixes the 1D ratio plots to use pull-style lower panels.

Session: Wolfgang (fix agent) | Phase 3
"""

import json
import logging
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

mh.style.use("CMS")

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

AN_FIG_DIR = Path("analysis_note/figures")
AN_FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(fig, name):
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: %s", name)


def aleph_label(ax, llabel="Open Data"):
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel=llabel,
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )


def suppress_axis0_text(ax):
    for txt in ax.texts:
        if "Axis" in txt.get_text() or txt.get_text().strip() == "":
            txt.set_visible(False)


def plot_2d_lund(h2d, n_hemi, x_edges, y_edges, name, label="Open Data"):
    """Plot a 2D Lund plane density with SQUARE aspect."""
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    rho = h2d / (n_hemi * np.outer(dx, dy))
    rho_plot = np.ma.masked_where(rho <= 0, rho)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="inferno", shading="flat",
                       norm=mcolors.LogNorm(vmin=1e-3, vmax=max(rho_plot.max(), 1e-2)))
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel=label)
    save_fig(fig, name)


def plot_ratio_1d(values_data, values_mc, err_data, err_mc, edges, xlabel, ylabel,
                  name, data_label="Data", mc_label="MC (PYTHIA 6.1)"):
    """Data/MC comparison with pull-style ratio panel."""
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(10, 10),
                                   gridspec_kw={"height_ratios": [3, 1]},
                                   sharex=True)
    fig.subplots_adjust(hspace=0)

    centers = 0.5 * (edges[:-1] + edges[1:])

    # MC as filled histogram
    mh.histplot((values_mc, edges), ax=ax, label=mc_label,
                histtype="fill", color="steelblue", alpha=0.5)
    mh.histplot((values_mc, edges), ax=ax,
                histtype="step", color="steelblue", linewidth=1.5)

    # Data as error bars
    ax.errorbar(centers, values_data, yerr=err_data, fmt="ko",
                markersize=4, label=data_label, zorder=5)

    ax.set_ylabel(ylabel)
    ax.legend(fontsize="x-small")
    aleph_label(ax)

    # Extend y-axis to avoid legend overlap
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(ymin, ymax * 1.35)

    # Pull panel: (Data - MC) / sigma_Data
    pull = np.zeros_like(values_data)
    mask = err_data > 0
    pull[mask] = (values_data[mask] - values_mc[mask]) / err_data[mask]

    rax.errorbar(centers, pull, yerr=np.ones_like(pull), fmt="ko", markersize=4)
    rax.axhline(0.0, color="gray", linestyle="--", linewidth=1)
    rax.axhline(2.0, color="gray", linestyle=":", linewidth=0.5, alpha=0.5)
    rax.axhline(-2.0, color="gray", linestyle=":", linewidth=0.5, alpha=0.5)
    rax.set_xlabel(xlabel)
    rax.set_ylabel(r"$\frac{\mathrm{Data} - \mathrm{MC}}{\sigma_{\mathrm{Data}}}$")
    rax.set_ylim(-4, 4)

    suppress_axis0_text(rax)

    save_fig(fig, name)


def main():
    log.info("=" * 70)
    log.info("Fix Script: Phase 3 Plots (Issues #2)")
    log.info("Session: Wolfgang")
    log.info("=" * 70)

    # Load data
    data_d = np.load(OUT_DIR / "data_lund_ingrid.npz")
    reco_d = np.load(OUT_DIR / "mc_reco_lund_ingrid.npz")
    gen_d = np.load(OUT_DIR / "mc_gen_lund_ingrid.npz")
    genb_d = np.load(OUT_DIR / "mc_genBefore_lund_ingrid.npz")

    h2d_data = data_d["h2d"]
    h2d_reco = reco_d["h2d"]
    h2d_gen = gen_d["h2d"]
    h2d_genBefore = genb_d["h2d"]
    x_edges = data_d["x_edges"]
    y_edges = data_d["y_edges"]
    n_hemi_data = float(data_d["n_hemispheres"])
    n_hemi_reco = float(reco_d["n_hemispheres"])
    n_hemi_gen = float(gen_d["n_hemispheres"])
    n_hemi_genBefore = float(genb_d["n_hemispheres"])

    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    area = np.outer(dx, dy)

    corr_d = np.load(OUT_DIR / "correction_ingrid.npz")
    correction = corr_d["correction"]
    efficiency = corr_d["efficiency"]
    diag_frac = corr_d["diag_fraction"]

    # === 2D Lund planes with SQUARE aspect ===
    log.info("\n--- 2D Lund planes (square aspect) ---")
    plot_2d_lund(h2d_data, n_hemi_data, x_edges, y_edges,
                 "ingrid_lund_2d_data_reco", "Open Data")
    plot_2d_lund(h2d_reco, n_hemi_reco, x_edges, y_edges,
                 "ingrid_lund_2d_mc_reco", "Open Simulation")
    plot_2d_lund(h2d_genBefore, n_hemi_genBefore, x_edges, y_edges,
                 "ingrid_lund_2d_genBefore", "Open Simulation")

    # === Data/MC 2D ratio (square) ===
    log.info("\n--- Data/MC 2D ratio (square) ---")
    rho_data = h2d_data / (n_hemi_data * area)
    rho_reco = h2d_reco / (n_hemi_reco * area)
    ratio_2d = np.ones_like(rho_data)
    mask_2d = (rho_reco > 0) & (rho_data > 0)
    ratio_2d[mask_2d] = rho_data[mask_2d] / rho_reco[mask_2d]
    ratio_2d_plot = np.ma.masked_where(~mask_2d, ratio_2d)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio_2d_plot.T, cmap="RdBu_r",
                       shading="flat", vmin=0.8, vmax=1.2)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / MC")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax)
    save_fig(fig, "ingrid_lund_2d_data_mc_ratio")

    # === Correction factor map (square) ===
    log.info("\n--- Correction factor map (square) ---")
    c_plot = np.ma.masked_where(correction <= 0, correction)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, c_plot.T, cmap="viridis", shading="flat",
                       vmin=0.5, vmax=3.0)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$C(i,j) = N_\mathrm{genBefore} / N_\mathrm{reco}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "ingrid_correction_factor_map")

    # === Diagonal fraction (square) ===
    log.info("\n--- Diagonal fraction map (square) ---")
    df_plot = np.ma.masked_where(diag_frac <= 0, diag_frac)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, df_plot.T, cmap="RdYlGn", shading="flat",
                       vmin=0, vmax=1.0)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Diagonal fraction (approximate)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "ingrid_diagonal_fraction_map")

    # === Efficiency map (square) ===
    log.info("\n--- Efficiency map (square) ---")
    eff_plot = np.ma.masked_where(efficiency <= 0, efficiency)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, eff_plot.T, cmap="viridis", shading="flat",
                       vmin=0.5, vmax=1.0)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax,
                 label=r"$\varepsilon(i,j) = N_\mathrm{gen} / N_\mathrm{genBefore}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "ingrid_efficiency_map")

    # === 1D projections with pull panels ===
    log.info("\n--- 1D projections (pull panels) ---")
    kt_data = np.sum(rho_data, axis=0) * dx[0]
    kt_mc = np.sum(rho_reco, axis=0) * dx[0]
    kt_data_err = np.sqrt(np.sum(h2d_data, axis=0)) / (n_hemi_data * dy) * dx[0]
    kt_mc_err = np.sqrt(np.sum(h2d_reco, axis=0)) / (n_hemi_reco * dy) * dx[0]

    plot_ratio_1d(kt_data, kt_mc, kt_data_err, kt_mc_err,
                  y_edges, r"$\ln(k_T / \mathrm{GeV})$",
                  r"$\rho$ (integrated over $\ln 1/\Delta\theta$)",
                  "ingrid_lund_kt_data_mc")

    dt_data = np.sum(rho_data, axis=1) * dy[0]
    dt_mc = np.sum(rho_reco, axis=1) * dy[0]
    dt_data_err = np.sqrt(np.sum(h2d_data, axis=1)) / (n_hemi_data * dx) * dy[0]
    dt_mc_err = np.sqrt(np.sum(h2d_reco, axis=1)) / (n_hemi_reco * dx) * dy[0]

    plot_ratio_1d(dt_data, dt_mc, dt_data_err, dt_mc_err,
                  x_edges, r"$\ln(1/\Delta\theta)$",
                  r"$\rho$ (integrated over $\ln k_T$)",
                  "ingrid_lund_dtheta_data_mc")

    # === Closure test pull distribution (fix) ===
    if (OUT_DIR / "closure_arrays_ingrid.npz").exists():
        log.info("\n--- Closure pull distribution ---")
        cl_d = np.load(OUT_DIR / "closure_arrays_ingrid.npz")
        pulls_flat = cl_d["pulls"]

        fig, ax = plt.subplots(figsize=(10, 10))
        n_pulls = len(pulls_flat)
        ax.hist(pulls_flat, bins=30, range=(-5, 5), color="steelblue",
                alpha=0.7, edgecolor="black", linewidth=0.5,
                label=f"Pulls ($N={n_pulls}$)")
        from scipy.stats import norm
        x_gauss = np.linspace(-5, 5, 200)
        ax.plot(x_gauss, norm.pdf(x_gauss) * len(pulls_flat) * 10.0 / 30,
                "r-", linewidth=2, label=r"$\mathcal{N}(0,1)$")
        ax.set_xlabel("Pull")
        ax.set_ylabel("Bins")
        ax.legend(fontsize="x-small")
        aleph_label(ax, llabel="Open Simulation")
        ymin, ymax = ax.get_ylim()
        ax.set_ylim(ymin, ymax * 1.35)
        save_fig(fig, "ingrid_closure_pulls")

    # === Approach comparison 2D (square) ===
    if (OUT_DIR / "approach_c_lund_ingrid.npz").exists():
        log.info("\n--- Approach comparison 2D (square) ---")
        ac_d = np.load(OUT_DIR / "approach_c_lund_ingrid.npz")
        ratio_ac = ac_d["ratio"]

        ratio_ac_plot = np.ma.masked_where(ratio_ac <= 0, ratio_ac)
        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.pcolormesh(x_edges, y_edges, ratio_ac_plot.T, cmap="RdBu_r",
                           shading="flat", vmin=0.7, vmax=1.3)
        ax.set_aspect("equal")
        cax = mh.utils.make_square_add_cbar(ax)
        fig.colorbar(im, cax=cax,
                     label=r"$\rho_\mathrm{kT\,2-jet}$ / $\rho_\mathrm{hemisphere}$")
        ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
        ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
        aleph_label(ax)
        save_fig(fig, "ingrid_approach_a_vs_c_2d")

    # Copy all to analysis_note/figures
    import shutil
    for f in FIG_DIR.glob("ingrid_*.pdf"):
        shutil.copy2(f, AN_FIG_DIR / f.name)
    for f in FIG_DIR.glob("ingrid_*.png"):
        shutil.copy2(f, AN_FIG_DIR / f.name)

    log.info("\nAll Phase 3 figures regenerated with fixes.")


if __name__ == "__main__":
    main()
