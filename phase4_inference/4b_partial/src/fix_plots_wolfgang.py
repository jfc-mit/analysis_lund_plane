#!/usr/bin/env python3
"""Fix Script: Phase 4b plots — all issues.

Fixes:
  #7: Figs 25-26 (10% data 2D plots) — square aspect + fix label placement
  #8: Fig 27 (1D projections) — MC as histogram band, all legend entries
  #9: Fig 28 (per-year stability) — square aspect for 2D stability plots

Session: Wolfgang (fix agent) | Phase 4b
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

mh.style.use("CMS")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

BASE = Path("/n/home07/anovak/work/slopspec/analyses/lund_jet_plane")
OUT_DIR = BASE / "phase4_inference" / "4b_partial" / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

AN_FIG_DIR = BASE / "analysis_note" / "figures"
AN_FIG_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(fig, name):
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved %s", name)


def suppress_axis0_text(ax):
    for txt in ax.texts:
        if "Axis" in txt.get_text() or txt.get_text().strip() == "":
            txt.set_visible(False)


def main():
    log.info("=" * 70)
    log.info("Fix Script: Phase 4b Plots (Issues #7-9)")
    log.info("Session: Wolfgang")
    log.info("=" * 70)

    # Load 10% data
    d10 = np.load(OUT_DIR / "data_10pct_lund_oscar.npz")
    h2d_data = d10["h2d"]
    n_hemi_data = int(d10["n_hemispheres"])
    x_edges = d10["x_edges"]
    y_edges = d10["y_edges"]
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    bin_area = np.outer(dx, dy)

    # Load MC reco from Phase 3
    mc_reco = np.load(BASE / "phase3_selection" / "outputs" / "mc_reco_lund_ingrid.npz")
    h2d_mc = mc_reco["h2d"]
    n_hemi_mc = int(mc_reco["n_hemispheres"])

    # Load corrected 10% data
    corr_10 = np.load(OUT_DIR / "corrected_10pct_oscar.npz")
    rho_data = corr_10["rho_data"]
    stat_err_data = corr_10["stat_err"]

    # Load expected from Phase 4a
    exp = np.load(BASE / "phase4_inference" / "4a_expected" / "outputs" /
                  "expected_results_felix.npz")
    rho_expected = exp["rho_corrected_bbb"]

    # Load covariance from Phase 4a
    cov_d = np.load(BASE / "phase4_inference" / "4a_expected" / "outputs" /
                    "covariance_felix.npz")
    total_err_expected = cov_d["total_err"].reshape(10, 10)

    # Load correction factors
    corr_ph3 = np.load(BASE / "phase3_selection" / "outputs" / "correction_ingrid.npz")
    correction = corr_ph3["correction"]

    # ================================================================
    # Issue #7: 10% data 2D plots — SQUARE aspect + fix label
    # ================================================================
    log.info("\n--- 10% data 2D plots (square aspect) ---")

    # Corrected Lund plane (10%)
    fig, ax = plt.subplots(figsize=(10, 10))
    rho_plot = rho_data.copy()
    rho_plot[rho_plot == 0] = np.nan
    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="viridis", shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )
    save_fig(fig, "oscar_lund_plane_10pct_corrected")

    # Ratio to expected (square)
    populated = (rho_expected > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_expected[populated]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio.T, cmap="RdBu_r",
                       vmin=0.7, vmax=1.3, shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="10% Data / Expected")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )
    save_fig(fig, "oscar_ratio_10pct_vs_expected")

    # Pull map (square)
    pulls = corr_10["pulls"]
    pull_plot = pulls.copy()
    pull_plot[(pulls == 0) & (np.abs(pulls) < 1e-10)] = np.nan

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, pull_plot.T, cmap="RdBu_r",
                       vmin=-3, vmax=3, shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"Pull = (Data $-$ Expected) / $\sigma$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    chi2_val = float(corr_10["chi2"])
    ndf_val = int(corr_10["ndf"])
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )
    # Add chi2/ndf as text annotation (not in the label to avoid crowding)
    ax.text(0.05, 0.05, f"$\\chi^2$/ndf = {chi2_val:.1f}/{ndf_val}",
            transform=ax.transAxes, fontsize="small",
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))
    save_fig(fig, "oscar_pull_map_10pct")

    # Data/MC reco ratio 2D (square)
    rho_data_reco = h2d_data / (n_hemi_data * bin_area)
    rho_mc_reco = h2d_mc / (n_hemi_mc * bin_area)
    populated_reco = (rho_mc_reco > 0) & (rho_data_reco > 0)
    ratio_reco = np.full_like(rho_data_reco, np.nan)
    ratio_reco[populated_reco] = rho_data_reco[populated_reco] / rho_mc_reco[populated_reco]

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio_reco.T, cmap="RdBu_r",
                       vmin=0.8, vmax=1.2, shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data (10%) / MC (reco level)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )
    save_fig(fig, "oscar_data_mc_reco_ratio_2d")

    # ================================================================
    # Issue #8: 1D projections — MC as histogram band, all legend entries
    # ================================================================
    log.info("\n--- 1D projections (MC band + complete legend) ---")

    for proj_name, proj_axis_sum, edges_proj, xlabel_proj, other_widths in [
        ("kt", 0, y_edges, r"$\ln(k_T / \mathrm{GeV})$", dx),
        ("dtheta", 1, x_edges, r"$\ln(1/\Delta\theta)$", dy),
    ]:
        centers_p = 0.5 * (edges_proj[:-1] + edges_proj[1:])

        if proj_name == "kt":
            rho_proj_data = np.sum(rho_data * dx[:, None], axis=0)
            rho_proj_exp = np.sum(rho_expected * dx[:, None], axis=0)
            err_proj_data = np.sqrt(np.sum((stat_err_data * dx[:, None])**2, axis=0))
            err_proj_exp = np.sqrt(np.sum((total_err_expected * dx[:, None])**2, axis=0))
        else:
            rho_proj_data = np.sum(rho_data * dy[None, :], axis=1)
            rho_proj_exp = np.sum(rho_expected * dy[None, :], axis=1)
            err_proj_data = np.sqrt(np.sum((stat_err_data * dy[None, :])**2, axis=1))
            err_proj_exp = np.sqrt(np.sum((total_err_expected * dy[None, :])**2, axis=1))

        fig, (ax_main, ax_pull) = plt.subplots(2, 1, figsize=(10, 10),
                                                gridspec_kw={"height_ratios": [3, 1]},
                                                sharex=True)
        fig.subplots_adjust(hspace=0)

        # MC expected as histogram band (filled region) — Issue #8 fix
        mh.histplot((rho_proj_exp, edges_proj), ax=ax_main,
                    histtype="step", color="C0", linewidth=1.5,
                    label="MC Expected (central)")
        ax_main.fill_between(
            centers_p, rho_proj_exp - err_proj_exp, rho_proj_exp + err_proj_exp,
            step="mid", alpha=0.3, color="C0",
            label="MC Expected ($\\pm 1\\sigma$)")

        # Data as black error bars
        ax_main.errorbar(centers_p, rho_proj_data, yerr=err_proj_data,
                         fmt="ko", markersize=5, label="Data (10%)", zorder=5)

        if proj_name == "kt":
            ax_main.set_ylabel(r"$\int \rho \, d\ln(1/\Delta\theta)$")
        else:
            ax_main.set_ylabel(r"$\int \rho \, d\ln(k_T)$")
        ax_main.legend(fontsize="x-small")

        mh.label.exp_label(
            exp="ALEPH", data=True, llabel="Open Data (10%)",
            rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
        )

        # Extend y-axis
        ymin, ymax = ax_main.get_ylim()
        ax_main.set_ylim(ymin, ymax * 1.35)

        # Pull panel
        sigma_tot = np.sqrt(err_proj_data**2 + err_proj_exp**2)
        pull = np.zeros_like(rho_proj_data)
        mask = sigma_tot > 0
        pull[mask] = (rho_proj_data[mask] - rho_proj_exp[mask]) / sigma_tot[mask]

        ax_pull.errorbar(centers_p, pull, yerr=1.0, fmt="ko", markersize=4)
        ax_pull.axhline(0, color="gray", linestyle="--")
        ax_pull.axhline(2, color="gray", linestyle=":", alpha=0.5)
        ax_pull.axhline(-2, color="gray", linestyle=":", alpha=0.5)
        ax_pull.set_xlabel(xlabel_proj)
        ax_pull.set_ylabel("Pull")
        ax_pull.set_ylim(-4, 4)

        suppress_axis0_text(ax_pull)

        save_fig(fig, f"oscar_1d_{proj_name}_projection")

    # ================================================================
    # Issue #9: Per-year stability — the 1D projections are fine as ratio
    # plots, no 2D needed. But ensure clean layout.
    # ================================================================
    log.info("\n--- Per-year stability (clean layout) ---")

    try:
        pf = np.load(OUT_DIR / "data_10pct_per_file_oscar.npz", allow_pickle=True)
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

        x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
        y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

        # Combined reference
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
            mh.label.exp_label(
                exp="ALEPH", data=True, llabel="Open Data (10%, per year)",
                rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
            )

            ax_ratio.axhline(1, color="gray", linestyle="--")
            ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
            ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
            ax_ratio.set_xlabel(proj_label)
            ax_ratio.set_ylabel("Ratio to combined")
            ax_ratio.set_ylim(0.85, 1.15)

            suppress_axis0_text(ax_ratio)

            save_fig(fig, f"oscar_per_year_{proj_name}")

    except Exception as e:
        log.warning("Could not regenerate per-year plots: %s", e)

    # Copy all to analysis_note/figures
    import shutil
    for f in FIG_DIR.glob("oscar_*.pdf"):
        shutil.copy2(f, AN_FIG_DIR / f.name)
    for f in FIG_DIR.glob("oscar_*.png"):
        shutil.copy2(f, AN_FIG_DIR / f.name)

    log.info("\nAll Phase 4b figures regenerated.")


if __name__ == "__main__":
    main()
