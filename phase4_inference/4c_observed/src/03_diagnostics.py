#!/usr/bin/env python3
"""Phase 4c Script 03: Diagnostic comparisons on full data.

- Per-year stability (full data, all 6 files)
- Data (full) vs MC reco (before correction): 2D ratio
- Cutflow comparison (full data vs MC)

Session: Emeric | Phase 4c
"""

import json
import logging
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from scipy import stats
from rich.logging import RichHandler

mh.style.use("CMS")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

BASE = Path("/n/home07/anovak/work/slopspec/analyses/lund_jet_plane")
OUT_DIR = BASE / "phase4_inference" / "4c_observed" / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_inputs():
    """Load all needed inputs."""
    # Full data
    d_full = np.load(OUT_DIR / "data_full_lund_emeric.npz")

    # Per-file data
    pf = np.load(OUT_DIR / "data_full_per_file_emeric.npz", allow_pickle=True)

    # MC reco from Phase 3
    mc_reco = np.load(BASE / "phase3_selection" / "outputs" / "mc_reco_lund_ingrid.npz")

    # Correction factors
    corr_d = np.load(BASE / "phase3_selection" / "outputs" / "correction_ingrid.npz")

    # Cutflows
    with open(OUT_DIR / "cutflow_full_emeric.json") as f:
        cutflow_full = json.load(f)
    with open(BASE / "phase3_selection" / "outputs" / "cutflow_ingrid.json") as f:
        cutflow_mc = json.load(f)

    return {
        "h2d_data_full": d_full["h2d"],
        "n_hemi_data_full": int(d_full["n_hemispheres"]),
        "h2d_per_file": pf["h2d_per_file"],
        "n_hemi_per_file": pf["n_hemi_per_file"],
        "file_names": pf["file_names"],
        "h2d_mc_reco": mc_reco["h2d"],
        "n_hemi_mc_reco": int(mc_reco["n_hemispheres"]),
        "correction": corr_d["correction"],
        "n_hemi_reco": float(corr_d["n_hemi_reco"]),
        "n_hemi_genBefore": float(corr_d["n_hemi_genBefore"]),
        "cutflow_full": cutflow_full,
        "cutflow_mc": cutflow_mc,
        "x_edges": d_full["x_edges"],
        "y_edges": d_full["y_edges"],
    }


def plot_data_mc_ratio_2d(inputs):
    """Plot 2D ratio of full data to MC reco (before correction)."""
    h2d_data = inputs["h2d_data_full"]
    n_hemi_data = inputs["n_hemi_data_full"]
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
    im = ax.pcolormesh(
        x_edges, y_edges, ratio.T, cmap="RdBu_r", vmin=0.8, vmax=1.2, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / MC (reco level)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data / Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_data_mc_reco_ratio_2d.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_data_mc_reco_ratio_2d.pdf")

    return {
        "mean": float(np.nanmean(ratio[populated])),
        "std": float(np.nanstd(ratio[populated])),
        "min": float(np.nanmin(ratio[populated])),
        "max": float(np.nanmax(ratio[populated])),
    }


def plot_per_year_stability(inputs):
    """Plot per-year stability of Lund plane 1D projections (full data)."""
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
    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    # Combined totals
    h2d_total = np.sum(h2d_per_file, axis=0)
    n_hemi_total = np.sum(n_hemi_per_file)

    per_year_chi2 = {}

    # --- ln(k_T) projection per year ---
    rho_total_kt = np.sum(h2d_total, axis=0) / (n_hemi_total * dy)

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
        label = year_map.get(str(fn), str(fn))
        h2d = h2d_per_file[i]
        rho_kt = np.sum(h2d, axis=0) / (nh * dy)
        err_kt = np.sqrt(np.sum(h2d, axis=0)) / (nh * dy)

        ax_main.errorbar(
            y_centers + (i - 2.5) * 0.02, rho_kt, yerr=err_kt,
            fmt="o", markersize=3, color=colors[i], label=label, alpha=0.8,
        )

        ratio = np.ones_like(rho_kt)
        ratio_err = np.zeros_like(err_kt)
        mask = rho_total_kt > 0
        ratio[mask] = rho_kt[mask] / rho_total_kt[mask]
        ratio_err[mask] = err_kt[mask] / rho_total_kt[mask]

        ax_ratio.errorbar(
            y_centers + (i - 2.5) * 0.02, ratio, yerr=ratio_err,
            fmt="o", markersize=3, color=colors[i], alpha=0.8,
        )

        # Chi2 for this year vs combined
        err_total = np.sqrt(np.sum(h2d_total, axis=0)) / (n_hemi_total * dy)
        chi2_mask = (rho_total_kt > 0) & (err_kt > 0)
        sigma2 = err_kt[chi2_mask] ** 2 + err_total[chi2_mask] ** 2
        chi2 = float(np.sum((rho_kt[chi2_mask] - rho_total_kt[chi2_mask]) ** 2 / sigma2))
        ndf = int(np.sum(chi2_mask))
        per_year_chi2[label] = {"chi2_kt": chi2, "ndf_kt": ndf}

    ax_main.set_ylabel(r"$d\rho / d\ln(k_T)$")
    ax_main.legend(fontsize="x-small", ncol=2)
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (per year)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax_ratio.set_ylabel("Ratio to combined")
    ax_ratio.set_ylim(0.85, 1.15)

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_per_year_kt.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_per_year_kt.pdf")

    # --- ln(1/Delta_theta) projection per year ---
    rho_total_dt = np.sum(h2d_total, axis=1) / (n_hemi_total * dx)

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    for i, (fn, nh) in enumerate(zip(file_names, n_hemi_per_file)):
        label = year_map.get(str(fn), str(fn))
        h2d = h2d_per_file[i]
        rho_dt = np.sum(h2d, axis=1) / (nh * dx)
        err_dt = np.sqrt(np.sum(h2d, axis=1)) / (nh * dx)

        ax_main.errorbar(
            x_centers + (i - 2.5) * 0.02, rho_dt, yerr=err_dt,
            fmt="o", markersize=3, color=colors[i], label=label, alpha=0.8,
        )

        ratio = np.ones_like(rho_dt)
        ratio_err = np.zeros_like(err_dt)
        mask = rho_total_dt > 0
        ratio[mask] = rho_dt[mask] / rho_total_dt[mask]
        ratio_err[mask] = err_dt[mask] / rho_total_dt[mask]

        ax_ratio.errorbar(
            x_centers + (i - 2.5) * 0.02, ratio, yerr=ratio_err,
            fmt="o", markersize=3, color=colors[i], alpha=0.8,
        )

        # Chi2 for this year vs combined (dtheta projection)
        err_total = np.sqrt(np.sum(h2d_total, axis=1)) / (n_hemi_total * dx)
        chi2_mask = (rho_total_dt > 0) & (err_dt > 0)
        sigma2 = err_dt[chi2_mask] ** 2 + err_total[chi2_mask] ** 2
        chi2 = float(np.sum((rho_dt[chi2_mask] - rho_total_dt[chi2_mask]) ** 2 / sigma2))
        ndf = int(np.sum(chi2_mask))
        per_year_chi2[label]["chi2_dt"] = chi2
        per_year_chi2[label]["ndf_dt"] = ndf

    ax_main.set_ylabel(r"$d\rho / d\ln(1/\Delta\theta)$")
    ax_main.legend(fontsize="x-small", ncol=2)
    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (per year)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.axhline(1.05, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.axhline(0.95, color="gray", linestyle=":", alpha=0.5)
    ax_ratio.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax_ratio.set_ylabel("Ratio to combined")
    ax_ratio.set_ylim(0.85, 1.15)

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_per_year_dtheta.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_per_year_dtheta.pdf")

    # Print per-year chi2 table
    log.info("\n=== Per-Year Stability (full data, chi2 to combined) ===")
    log.info("%-12s %18s %18s", "Year", "chi2/ndf (ln kT)", "chi2/ndf (ln 1/dtheta)")
    log.info("-" * 50)
    for label in sorted(per_year_chi2.keys()):
        v = per_year_chi2[label]
        log.info(
            "%-12s %8.1f / %-3d = %.2f %8.1f / %-3d = %.2f",
            label,
            v["chi2_kt"], v["ndf_kt"],
            v["chi2_kt"] / v["ndf_kt"] if v["ndf_kt"] > 0 else 0,
            v["chi2_dt"], v["ndf_dt"],
            v["chi2_dt"] / v["ndf_dt"] if v["ndf_dt"] > 0 else 0,
        )

    return per_year_chi2


def plot_cutflow_comparison(inputs):
    """Compare cutflow: full data vs MC (efficiency agreement)."""
    cf = inputs["cutflow_full"]
    cf_mc = inputs["cutflow_mc"]

    # Data efficiency at each stage (relative to total events)
    data_vals = [cf["total_events_raw"], cf["total_selected"], cf["total_hemi_cut"]]
    data_effs = [v / data_vals[0] for v in data_vals]

    # MC efficiency (reco level, relative to total)
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

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Cutflow comparison",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    ratios = [d / m if m > 0 else 1.0 for d, m in zip(data_effs, mc_effs)]
    ax_ratio.bar(x, ratios, 0.6, color="C2", alpha=0.7)
    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.set_ylabel("Data / MC")
    ax_ratio.set_ylim(0.95, 1.05)
    ax_ratio.set_xticks(x)
    ax_ratio.set_xticklabels(labels, fontsize="x-small")

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_cutflow_comparison.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_cutflow_comparison.pdf")

    # Print table
    log.info("\n=== Cutflow Comparison (Full Data vs MC) ===")
    log.info("%-25s %12s %12s %10s %10s", "Stage", "Data", "MC reco", "Eff(D)", "Eff(MC)")
    log.info("-" * 70)
    for i, label in enumerate(labels):
        log.info(
            "%-25s %12d %12d %10.4f %10.4f",
            label, data_vals[i], mc_vals[i], data_effs[i], mc_effs[i],
        )

    return {
        "data_effs": data_effs,
        "mc_effs": mc_effs,
        "data_vals": data_vals,
        "mc_vals": mc_vals,
    }


def main():
    log.info("=" * 70)
    log.info("Phase 4c Script 03: Full Data Diagnostics")
    log.info("Session: Emeric")
    log.info("=" * 70)

    inputs = load_inputs()

    # Data/MC reco ratio (before correction)
    ratio_stats = plot_data_mc_ratio_2d(inputs)

    # Per-year stability
    per_year_chi2 = plot_per_year_stability(inputs)

    # Cutflow comparison
    cutflow_stats = plot_cutflow_comparison(inputs)

    # Save diagnostic results
    diag = {
        "data_mc_reco_ratio": ratio_stats,
        "per_year_chi2": per_year_chi2,
        "cutflow_data_effs": cutflow_stats["data_effs"],
        "cutflow_mc_effs": cutflow_stats["mc_effs"],
    }
    import json
    with open(OUT_DIR / "diagnostics_full_emeric.json", "w") as fp:
        json.dump(diag, fp, indent=2, default=str)

    log.info("\nAll diagnostics complete.")


if __name__ == "__main__":
    main()
