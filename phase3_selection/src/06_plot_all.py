#!/usr/bin/env python3
"""Script 06: All Phase 3 figures.

Reads machine-readable outputs from scripts 01-04 and produces all figures.
Follows plotting rules strictly: figsize=(10,10), CMS style, ALEPH label,
PDF+PNG, no titles, no absolute fontsize.

Session: Ingrid | Phase 3
"""

import json
import logging
from pathlib import Path

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from mplhep.utils import mpl_magic
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

mh.style.use("CMS")

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(fig, name):
    """Save figure as PDF and PNG, then close."""
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: %s", name)


def aleph_label(ax, llabel="Open Data"):
    """Add ALEPH experiment label."""
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel=llabel,
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )


def plot_2d_lund(h2d, n_hemi, x_edges, y_edges, name, label="Open Data"):
    """Plot a 2D Lund plane density."""
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    rho = h2d / (n_hemi * np.outer(dx, dy))
    rho_plot = np.ma.masked_where(rho <= 0, rho)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="inferno", shading="flat",
                       norm=mcolors.LogNorm(vmin=1e-3, vmax=max(rho_plot.max(), 1e-2)))
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel=label)
    save_fig(fig, name)


def plot_ratio_1d(values_data, values_mc, err_data, err_mc, edges, xlabel, ylabel,
                  name, data_label="Data", mc_label="MC (PYTHIA 6.1)"):
    """Data/MC comparison with ratio panel."""
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(10, 10),
                                   gridspec_kw={"height_ratios": [3, 1]},
                                   sharex=True)
    fig.subplots_adjust(hspace=0)

    centers = 0.5 * (edges[:-1] + edges[1:])
    widths = np.diff(edges)

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
    mpl_magic(ax)

    # Ratio panel
    ratio = np.ones_like(values_data)
    ratio_err = np.zeros_like(values_data)
    mask = values_mc > 0
    ratio[mask] = values_data[mask] / values_mc[mask]
    ratio_err[mask] = err_data[mask] / values_mc[mask]

    rax.errorbar(centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    rax.axhline(1.0, color="gray", linestyle="--", linewidth=1)
    rax.set_xlabel(xlabel)
    rax.set_ylabel("Data / MC")
    rax.set_ylim(0.7, 1.3)

    save_fig(fig, name)


def main():
    log.info("=" * 70)
    log.info("Phase 3 Script 06: All Figures")
    log.info("Session: Ingrid")
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
    correction_err = corr_d["correction_err"]
    efficiency = corr_d["efficiency"]
    diag_frac = corr_d["diag_fraction"]

    # === Figure 1: Reco-level 2D Lund plane (data) ===
    log.info("\n--- Figure 1: Reco 2D Lund plane (data) ---")
    plot_2d_lund(h2d_data, n_hemi_data, x_edges, y_edges,
                 "ingrid_lund_2d_data_reco", "Open Data")

    # === Figure 2: Reco-level 2D Lund plane (MC reco) ===
    log.info("\n--- Figure 2: Reco 2D Lund plane (MC) ---")
    plot_2d_lund(h2d_reco, n_hemi_reco, x_edges, y_edges,
                 "ingrid_lund_2d_mc_reco", "Open Simulation")

    # === Figure 3: Data/MC 2D ratio ===
    log.info("\n--- Figure 3: Data/MC 2D ratio ---")
    rho_data = h2d_data / (n_hemi_data * area)
    rho_reco = h2d_reco / (n_hemi_reco * area)
    ratio_2d = np.ones_like(rho_data)
    mask_2d = (rho_reco > 0) & (rho_data > 0)
    ratio_2d[mask_2d] = rho_data[mask_2d] / rho_reco[mask_2d]
    ratio_2d_plot = np.ma.masked_where(~mask_2d, ratio_2d)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio_2d_plot.T, cmap="RdBu_r",
                       shading="flat", vmin=0.8, vmax=1.2)
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / MC")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax)
    save_fig(fig, "ingrid_lund_2d_data_mc_ratio")

    # === Figure 4: Data/MC 1D projection ln(k_T) ===
    log.info("\n--- Figure 4: Data/MC ln(kT) projection ---")
    kt_data = np.sum(rho_data, axis=0) * dx[0]
    kt_mc = np.sum(rho_reco, axis=0) * dx[0]
    kt_data_err = np.sqrt(np.sum(h2d_data, axis=0)) / (n_hemi_data * dy)
    kt_mc_err = np.sqrt(np.sum(h2d_reco, axis=0)) / (n_hemi_reco * dy)
    # Integrate over x dimension properly
    kt_data_err_proj = kt_data_err * dx[0]
    kt_mc_err_proj = kt_mc_err * dx[0]

    plot_ratio_1d(kt_data, kt_mc, kt_data_err_proj, kt_mc_err_proj,
                  y_edges, r"$\ln(k_T / \mathrm{GeV})$",
                  r"$\rho$ (integrated over $\ln 1/\Delta\theta$)",
                  "ingrid_lund_kt_data_mc")

    # === Figure 5: Data/MC 1D projection ln(1/Delta_theta) ===
    log.info("\n--- Figure 5: Data/MC ln(1/dtheta) projection ---")
    dt_data = np.sum(rho_data, axis=1) * dy[0]
    dt_mc = np.sum(rho_reco, axis=1) * dy[0]
    dt_data_err = np.sqrt(np.sum(h2d_data, axis=1)) / (n_hemi_data * dx)
    dt_mc_err = np.sqrt(np.sum(h2d_reco, axis=1)) / (n_hemi_reco * dx)
    dt_data_err_proj = dt_data_err * dy[0]
    dt_mc_err_proj = dt_mc_err * dy[0]

    plot_ratio_1d(dt_data, dt_mc, dt_data_err_proj, dt_mc_err_proj,
                  x_edges, r"$\ln(1/\Delta\theta)$",
                  r"$\rho$ (integrated over $\ln k_T$)",
                  "ingrid_lund_dtheta_data_mc")

    # === Figure 6: Correction factor map ===
    log.info("\n--- Figure 6: Correction factor map ---")
    c_plot = np.ma.masked_where(correction <= 0, correction)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, c_plot.T, cmap="viridis", shading="flat",
                       vmin=0.5, vmax=3.0)
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$C(i,j) = N_\mathrm{genBefore} / N_\mathrm{reco}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "ingrid_correction_factor_map")

    # === Figure 7: Diagonal fraction map ===
    log.info("\n--- Figure 7: Diagonal fraction map ---")
    df_plot = np.ma.masked_where(diag_frac <= 0, diag_frac)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, df_plot.T, cmap="RdYlGn", shading="flat",
                       vmin=0, vmax=1.0)
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Diagonal fraction (approximate)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "ingrid_diagonal_fraction_map")

    # === Figure 8: Efficiency map ===
    log.info("\n--- Figure 8: Efficiency map ---")
    eff_plot = np.ma.masked_where(efficiency <= 0, efficiency)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, eff_plot.T, cmap="viridis", shading="flat",
                       vmin=0.5, vmax=1.0)
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax,
                 label=r"$\varepsilon(i,j) = N_\mathrm{gen} / N_\mathrm{genBefore}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    aleph_label(ax, llabel="Open Simulation")
    save_fig(fig, "ingrid_efficiency_map")

    # === Closure test figures ===
    if (OUT_DIR / "closure_arrays_ingrid.npz").exists():
        log.info("\n--- Closure test figures ---")
        cl_d = np.load(OUT_DIR / "closure_arrays_ingrid.npz")
        rho_corr = cl_d["rho_corrected"]
        rho_corr_err = cl_d["rho_corrected_err"]
        rho_truth = cl_d["rho_truth"]
        rho_truth_err = cl_d["rho_truth_err"]
        pulls_flat = cl_d["pulls"]

        # Figure 9: Closure 1D ln(kT)
        log.info("--- Figure 9: Closure ln(kT) ---")
        kt_corr = np.sum(rho_corr, axis=0) * dx[0]
        kt_truth = np.sum(rho_truth, axis=0) * dx[0]
        kt_corr_err = np.sqrt(np.sum(rho_corr_err**2, axis=0)) * dx[0]
        kt_truth_err = np.sqrt(np.sum(rho_truth_err**2, axis=0)) * dx[0]

        plot_ratio_1d(kt_corr, kt_truth, kt_corr_err, kt_truth_err,
                      y_edges, r"$\ln(k_T / \mathrm{GeV})$",
                      r"$\rho$ (integrated over $\ln 1/\Delta\theta$)",
                      "ingrid_closure_kt",
                      data_label="Corrected MC reco",
                      mc_label="MC gen truth")

        # Figure 10: Closure 1D ln(1/dtheta)
        log.info("--- Figure 10: Closure ln(1/dtheta) ---")
        dt_corr = np.sum(rho_corr, axis=1) * dy[0]
        dt_truth = np.sum(rho_truth, axis=1) * dy[0]
        dt_corr_err = np.sqrt(np.sum(rho_corr_err**2, axis=1)) * dy[0]
        dt_truth_err = np.sqrt(np.sum(rho_truth_err**2, axis=1)) * dy[0]

        plot_ratio_1d(dt_corr, dt_truth, dt_corr_err, dt_truth_err,
                      x_edges, r"$\ln(1/\Delta\theta)$",
                      r"$\rho$ (integrated over $\ln k_T$)",
                      "ingrid_closure_dtheta",
                      data_label="Corrected MC reco",
                      mc_label="MC gen truth")

        # Figure 11: Pull distribution
        log.info("--- Figure 11: Pull distribution ---")
        fig, ax = plt.subplots(figsize=(10, 10))
        n_pulls = len(pulls_flat)
        ax.hist(pulls_flat, bins=30, range=(-5, 5), color="steelblue",
                alpha=0.7, edgecolor="black", linewidth=0.5,
                label=f"Pulls ($N={n_pulls}$)")
        # Gaussian overlay
        x_gauss = np.linspace(-5, 5, 200)
        from scipy.stats import norm
        ax.plot(x_gauss, norm.pdf(x_gauss) * len(pulls_flat) * 10.0 / 30,
                "r-", linewidth=2, label=r"$\mathcal{N}(0,1)$")
        ax.set_xlabel("Pull")
        ax.set_ylabel("Bins")
        ax.legend(fontsize="x-small")
        aleph_label(ax, llabel="Open Simulation")
        mpl_magic(ax)
        save_fig(fig, "ingrid_closure_pulls")

        # Load closure JSON for annotation
        with open(OUT_DIR / "closure_ingrid.json") as f:
            cl_json = json.load(f)
        log.info("Closure chi2/ndf = %.4f, p-value = %.6f",
                 cl_json["chi2_ndf"], cl_json["p_value"])

    # === Approach comparison figures ===
    if (OUT_DIR / "approach_c_lund_ingrid.npz").exists():
        log.info("\n--- Approach comparison figures ---")
        ac_d = np.load(OUT_DIR / "approach_c_lund_ingrid.npz")
        rho_a = ac_d["rho_a"]
        rho_c = ac_d["rho_c"]
        ratio_ac = ac_d["ratio"]

        # Figure 12: Approach A vs C 2D ratio
        log.info("--- Figure 12: Approach A vs C 2D ratio ---")
        ratio_ac_plot = np.ma.masked_where(ratio_ac <= 0, ratio_ac)
        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.pcolormesh(x_edges, y_edges, ratio_ac_plot.T, cmap="RdBu_r",
                           shading="flat", vmin=0.7, vmax=1.3)
        cax = mh.utils.make_square_add_cbar(ax)
        fig.colorbar(im, cax=cax,
                     label=r"$\rho_\mathrm{kT\,2-jet}$ / $\rho_\mathrm{hemisphere}$")
        ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
        ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
        aleph_label(ax)
        save_fig(fig, "ingrid_approach_a_vs_c_2d")

        # Figure 13: Approach comparison 1D ln(kT)
        log.info("--- Figure 13: Approach A vs C ln(kT) ---")
        kt_a = ac_d["kt_proj_a"]
        kt_c = ac_d["kt_proj_c"]

        fig, (ax, rax) = plt.subplots(2, 1, figsize=(10, 10),
                                       gridspec_kw={"height_ratios": [3, 1]},
                                       sharex=True)
        fig.subplots_adjust(hspace=0)

        centers_y = 0.5 * (y_edges[:-1] + y_edges[1:])
        mh.histplot((kt_a, y_edges), ax=ax, label="Approach A (hemispheres)",
                    histtype="step", color="black", linewidth=2)
        mh.histplot((kt_c, y_edges), ax=ax, label="Approach C (kT 2-jets)",
                    histtype="step", color="red", linewidth=2, linestyle="--")
        ax.set_ylabel(r"$\rho$ (integrated over $\ln 1/\Delta\theta$)")
        ax.legend(fontsize="x-small")
        aleph_label(ax)
        mpl_magic(ax)

        ratio_kt = np.ones_like(kt_a)
        mask_kt = kt_a > 0
        ratio_kt[mask_kt] = kt_c[mask_kt] / kt_a[mask_kt]
        rax.plot(centers_y, ratio_kt, "ko-", markersize=4)
        rax.axhline(1.0, color="gray", linestyle="--", linewidth=1)
        rax.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
        rax.set_ylabel("C / A")
        rax.set_ylim(0.7, 1.3)
        save_fig(fig, "ingrid_approach_kt_comparison")

    # === Figure 14: GenBefore Lund plane (truth) ===
    log.info("\n--- Figure 14: GenBefore Lund plane (truth) ---")
    plot_2d_lund(h2d_genBefore, n_hemi_genBefore, x_edges, y_edges,
                 "ingrid_lund_2d_genBefore", "Open Simulation")

    log.info("\nAll figures produced.")


if __name__ == "__main__":
    main()
