#!/usr/bin/env python3
"""Phase 4b Script 03: Diagnostic comparisons.

- Data (10%) vs MC reco (before correction): 2D ratio
- Per-year stability
- Cutflow comparison: 10% data vs MC
- Data/MC 1D projections (uncorrected) for shape comparison

Session: Oscar | Phase 4b
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


def load_inputs():
    """Load all needed inputs."""
    # 10% data
    d10 = np.load(OUT_DIR / "data_10pct_lund_oscar.npz")

    # Per-file data
    pf = np.load(OUT_DIR / "data_10pct_per_file_oscar.npz", allow_pickle=True)

    # MC reco from Phase 3
    mc_reco = np.load(BASE / "phase3_selection" / "outputs" / "mc_reco_lund_ingrid.npz")

    # Full data from Phase 3 (for comparison)
    full_data = np.load(BASE / "phase3_selection" / "outputs" / "data_lund_ingrid.npz")

    # Cutflows
    with open(OUT_DIR / "cutflow_10pct_oscar.json") as f:
        cutflow_10pct = json.load(f)
    with open(BASE / "phase3_selection" / "outputs" / "cutflow_ingrid.json") as f:
        cutflow_full = json.load(f)

    return {
        "h2d_data_10pct": d10["h2d"],
        "n_hemi_data_10pct": int(d10["n_hemispheres"]),
        "h2d_per_file": pf["h2d_per_file"],
        "n_hemi_per_file": pf["n_hemi_per_file"],
        "file_names": pf["file_names"],
        "h2d_mc_reco": mc_reco["h2d"],
        "n_hemi_mc_reco": int(mc_reco["n_hemispheres"]),
        "h2d_full_data": full_data["h2d"],
        "n_hemi_full_data": int(full_data["n_hemispheres"]),
        "cutflow_10pct": cutflow_10pct,
        "cutflow_full": cutflow_full,
        "x_edges": d10["x_edges"],
        "y_edges": d10["y_edges"],
    }


def plot_data_mc_ratio_2d(inputs):
    """Plot 2D ratio of 10% data to MC reco (before correction)."""
    h2d_data = inputs["h2d_data_10pct"]
    n_hemi_data = inputs["n_hemi_data_10pct"]
    h2d_mc = inputs["h2d_mc_reco"]
    n_hemi_mc = inputs["n_hemi_mc_reco"]
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    bin_area = np.outer(dx, dy)

    rho_data = h2d_data / (n_hemi_data * bin_area)
    rho_mc = h2d_mc / (n_hemi_mc * bin_area)

    populated = (rho_mc > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_mc[populated]

    log.info("Data/MC reco ratio (reco-level, before correction):")
    log.info("  Mean ratio (populated): %.4f", np.nanmean(ratio[populated]))
    log.info("  Std ratio: %.4f", np.nanstd(ratio[populated]))
    log.info("  Min ratio: %.4f", np.nanmin(ratio[populated]))
    log.info("  Max ratio: %.4f", np.nanmax(ratio[populated]))

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_edges, y_edges, ratio.T, cmap="RdBu_r",
                       vmin=0.8, vmax=1.2, shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data (10%) / MC (reco level)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%) / Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "oscar_data_mc_reco_ratio_2d.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_data_mc_reco_ratio_2d.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_data_mc_reco_ratio_2d.pdf")


def plot_per_year_stability(inputs):
    """Plot per-year stability of Lund plane 1D projections."""
    h2d_per_file = inputs["h2d_per_file"]
    n_hemi_per_file = inputs["n_hemi_per_file"]
    file_names = inputs["file_names"]
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)

    # Map file names to year labels
    year_map = {
        "LEP1Data1992_recons_aftercut-MERGED.root": "1992",
        "LEP1Data1993_recons_aftercut-MERGED.root": "1993",
        "LEP1Data1994P1_recons_aftercut-MERGED.root": "1994 P1",
        "LEP1Data1994P2_recons_aftercut-MERGED.root": "1994 P2",
        "LEP1Data1994P3_recons_aftercut-MERGED.root": "1994 P3",
        "LEP1Data1995_recons_aftercut-MERGED.root": "1995",
    }

    colors = ["C0", "C1", "C2", "C3", "C4", "C5"]

    # --- ln(k_T) projection per year ---
    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    fig, (ax_main, ax_ratio) = plt.subplots(2, 1, figsize=(10, 10),
                                             gridspec_kw={"height_ratios": [3, 1]},
                                             sharex=True)
    fig.subplots_adjust(hspace=0)

    # Combined projection as reference
    h2d_total = np.sum(h2d_per_file, axis=0)
    n_hemi_total = np.sum(n_hemi_per_file)
    rho_total_kt = np.sum(h2d_total, axis=0) / (n_hemi_total * dy)

    for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
        label = year_map.get(str(fn), str(fn))
        h2d = h2d_per_file[i]
        rho_kt = np.sum(h2d, axis=0) / (nh * dy)
        err_kt = np.sqrt(np.sum(h2d, axis=0)) / (nh * dy)

        ax_main.errorbar(y_centers + (i - 2.5) * 0.02, rho_kt, yerr=err_kt,
                         fmt="o", markersize=3, color=colors[i],
                         label=label, alpha=0.8)

        # Ratio to combined
        ratio = np.ones_like(rho_kt)
        mask = rho_total_kt > 0
        ratio[mask] = rho_kt[mask] / rho_total_kt[mask]
        ratio_err = np.zeros_like(err_kt)
        ratio_err[mask] = err_kt[mask] / rho_total_kt[mask]

        ax_ratio.errorbar(y_centers + (i - 2.5) * 0.02, ratio, yerr=ratio_err,
                          fmt="o", markersize=3, color=colors[i], alpha=0.8)

    ax_main.set_ylabel(r"$d\rho / d\ln(k_T)$")
    ax_main.legend(fontsize="x-small", ncol=2)
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%, per year)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax_ratio.set_ylabel("Ratio to combined")
    ax_ratio.set_ylim(0.85, 1.15)

    fig.savefig(FIG_DIR / "oscar_per_year_kt.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_per_year_kt.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_per_year_kt.pdf")

    # --- ln(1/Delta_theta) projection per year ---
    fig, (ax_main, ax_ratio) = plt.subplots(2, 1, figsize=(10, 10),
                                             gridspec_kw={"height_ratios": [3, 1]},
                                             sharex=True)
    fig.subplots_adjust(hspace=0)

    rho_total_dt = np.sum(h2d_total, axis=1) / (n_hemi_total * dx)

    for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
        label = year_map.get(str(fn), str(fn))
        h2d = h2d_per_file[i]
        rho_dt = np.sum(h2d, axis=1) / (nh * dx)
        err_dt = np.sqrt(np.sum(h2d, axis=1)) / (nh * dx)

        ax_main.errorbar(x_centers + (i - 2.5) * 0.02, rho_dt, yerr=err_dt,
                         fmt="o", markersize=3, color=colors[i],
                         label=label, alpha=0.8)

        ratio = np.ones_like(rho_dt)
        mask = rho_total_dt > 0
        ratio[mask] = rho_dt[mask] / rho_total_dt[mask]
        ratio_err = np.zeros_like(err_dt)
        ratio_err[mask] = err_dt[mask] / rho_total_dt[mask]

        ax_ratio.errorbar(x_centers + (i - 2.5) * 0.02, ratio, yerr=ratio_err,
                          fmt="o", markersize=3, color=colors[i], alpha=0.8)

    ax_main.set_ylabel(r"$d\rho / d\ln(1/\Delta\theta)$")
    ax_main.legend(fontsize="x-small", ncol=2)
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%, per year)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax_ratio.set_ylabel("Ratio to combined")
    ax_ratio.set_ylim(0.85, 1.15)

    fig.savefig(FIG_DIR / "oscar_per_year_dtheta.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_per_year_dtheta.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_per_year_dtheta.pdf")

    # Compute per-year chi2 relative to combined
    log.info("\n=== Per-Year Stability (chi2 to combined) ===")
    for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
        label = year_map.get(str(fn), str(fn))
        h2d = h2d_per_file[i]
        # Compare 1D ln(kT) projection
        rho_year = np.sum(h2d, axis=0) / (nh * dy)
        err_year = np.sqrt(np.sum(h2d, axis=0)) / (nh * dy)
        err_total = np.sqrt(np.sum(h2d_total, axis=0)) / (n_hemi_total * dy)

        mask = (rho_total_kt > 0) & (err_year > 0)
        sigma2 = err_year[mask]**2 + err_total[mask]**2
        chi2 = np.sum((rho_year[mask] - rho_total_kt[mask])**2 / sigma2)
        ndf = np.sum(mask)
        log.info("  %s: chi2/ndf = %.1f/%d = %.2f",
                 label, chi2, ndf, chi2 / ndf if ndf > 0 else 0)


def plot_cutflow_comparison(inputs):
    """Compare cutflow: 10% data vs MC (efficiency agreement)."""
    cf10 = inputs["cutflow_10pct"]
    cf_full = inputs["cutflow_full"]

    # Data efficiency at each stage (relative to subsample)
    data_stages = ["total_subsample", "total_selected", "total_hemi_cut"]
    data_vals = [cf10[s] for s in data_stages]
    data_effs = [v / data_vals[0] for v in data_vals]

    # MC efficiency (reco level, relative to total)
    mc_stages = ["reco_total", "reco_selected", "reco_hemi"]
    mc_vals = [cf_full["mc"][s] for s in mc_stages]
    mc_effs = [v / mc_vals[0] for v in mc_vals]

    labels = ["Input", "After selection", "After hemi cut"]

    fig, (ax_main, ax_ratio) = plt.subplots(2, 1, figsize=(10, 10),
                                             gridspec_kw={"height_ratios": [3, 1]},
                                             sharex=True)
    fig.subplots_adjust(hspace=0)

    x = np.arange(len(labels))
    width = 0.35

    ax_main.bar(x - width / 2, data_effs, width, label="Data (10%)", color="C0", alpha=0.7)
    ax_main.bar(x + width / 2, mc_effs, width, label="MC reco", color="C1", alpha=0.7)
    ax_main.set_ylabel("Efficiency (relative to input)")
    ax_main.set_xticks(x)
    ax_main.set_xticklabels(labels, fontsize="x-small")
    ax_main.legend(fontsize="x-small")
    ax_main.set_ylim(0.8, 1.05)

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Cutflow comparison",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    # Ratio
    ratios = [d / m if m > 0 else 1.0 for d, m in zip(data_effs, mc_effs)]
    ax_ratio.bar(x, ratios, 0.6, color="C2", alpha=0.7)
    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.set_ylabel("Data / MC")
    ax_ratio.set_ylim(0.95, 1.05)
    ax_ratio.set_xticks(x)
    ax_ratio.set_xticklabels(labels, fontsize="x-small")

    fig.savefig(FIG_DIR / "oscar_cutflow_comparison.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_cutflow_comparison.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_cutflow_comparison.pdf")

    # Print table
    log.info("\n=== Cutflow Comparison ===")
    log.info("%-25s %12s %12s %10s %10s", "Stage", "Data 10%", "MC reco", "Eff(D)", "Eff(MC)")
    log.info("-" * 70)
    for i, label in enumerate(labels):
        log.info("%-25s %12d %12d %10.4f %10.4f",
                 label, data_vals[i], mc_vals[i], data_effs[i], mc_effs[i])


def plot_full_vs_10pct_consistency(inputs):
    """Verify 10% subsample is statistically consistent with full data (scaled)."""
    h2d_10pct = inputs["h2d_data_10pct"]
    n_hemi_10pct = inputs["n_hemi_data_10pct"]
    h2d_full = inputs["h2d_full_data"]
    n_hemi_full = inputs["n_hemi_full_data"]
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)

    # Density comparison (should agree within statistics)
    rho_10pct = h2d_10pct / (n_hemi_10pct * np.outer(dx, dy))
    rho_full = h2d_full / (n_hemi_full * np.outer(dx, dy))

    populated = (rho_full > 0) & (rho_10pct > 0)
    ratio = np.full_like(rho_10pct, np.nan)
    ratio[populated] = rho_10pct[populated] / rho_full[populated]

    log.info("\n=== 10%% vs Full Data Consistency ===")
    log.info("  Mean ratio: %.4f (expect ~1.0)", np.nanmean(ratio[populated]))
    log.info("  Std ratio: %.4f", np.nanstd(ratio[populated]))

    # Chi2 test (10% should be a subset of full, so ratio ~1 within Poisson)
    err_10pct = np.sqrt(h2d_10pct) / (n_hemi_10pct * np.outer(dx, dy))
    err_full = np.sqrt(h2d_full) / (n_hemi_full * np.outer(dx, dy))
    sigma = np.sqrt(err_10pct**2 + err_full**2)
    pulls = np.zeros_like(rho_10pct)
    mask = populated & (sigma > 0)
    pulls[mask] = (rho_10pct[mask] - rho_full[mask]) / sigma[mask]
    chi2 = np.sum(pulls[mask]**2)
    ndf = np.sum(mask)
    log.info("  chi2/ndf = %.1f/%d = %.3f", chi2, ndf, chi2 / ndf if ndf > 0 else 0)
    log.info("  Pull mean = %.3f, std = %.3f", np.mean(pulls[mask]), np.std(pulls[mask]))


def main():
    log.info("=" * 70)
    log.info("Phase 4b Script 03: Diagnostics")
    log.info("Session: Oscar")
    log.info("=" * 70)

    inputs = load_inputs()

    # Data/MC reco ratio (before correction)
    plot_data_mc_ratio_2d(inputs)

    # Per-year stability
    plot_per_year_stability(inputs)

    # Cutflow comparison
    plot_cutflow_comparison(inputs)

    # 10% vs full data consistency
    plot_full_vs_10pct_consistency(inputs)

    log.info("\nAll diagnostics complete.")


if __name__ == "__main__":
    main()
