#!/usr/bin/env python3
"""Phase 4c Script 02: Apply corrections to full data, compare to expected and 10%.

Applies full-MC bin-by-bin correction factors to the complete data set.
Computes corrected Lund plane density (THE primary result), pulls vs expected,
chi2, and consistency checks against the 10% partial result.

Session: Emeric | Phase 4c
"""

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
    """Load full data, correction factors, expected results, and 10% results."""
    # Full data
    d_full = np.load(OUT_DIR / "data_full_lund_emeric.npz")
    h2d_data = d_full["h2d"]
    n_hemi_data = int(d_full["n_hemispheres"])
    x_edges = d_full["x_edges"]
    y_edges = d_full["y_edges"]

    # Full MC correction factors (from Phase 3)
    corr_d = np.load(BASE / "phase3_selection" / "outputs" / "correction_ingrid.npz")
    correction = corr_d["correction"]
    n_hemi_reco = float(corr_d["n_hemi_reco"])
    n_hemi_genBefore = float(corr_d["n_hemi_genBefore"])
    h2d_reco = corr_d["h2d_reco"]

    # Expected results from Phase 4a
    exp = np.load(
        BASE / "phase4_inference" / "4a_expected" / "outputs" / "expected_results_felix.npz"
    )
    rho_expected = exp["rho_corrected_bbb"]

    # Covariance from Phase 4a (stat + syst on expected)
    cov_d = np.load(
        BASE / "phase4_inference" / "4a_expected" / "outputs" / "covariance_felix.npz"
    )
    cov_total = cov_d["cov_total"]
    total_err = cov_d["total_err"]

    # 10% partial results from Phase 4b
    d10 = np.load(
        BASE / "phase4_inference" / "4b_partial" / "outputs" / "corrected_10pct_oscar.npz"
    )
    rho_10pct = d10["rho_data"]
    stat_err_10pct = d10["stat_err"]
    n_hemi_10pct = int(d10["n_hemi_data"])

    return {
        "h2d_data": h2d_data,
        "n_hemi_data": n_hemi_data,
        "x_edges": x_edges,
        "y_edges": y_edges,
        "correction": correction,
        "n_hemi_reco": n_hemi_reco,
        "n_hemi_genBefore": n_hemi_genBefore,
        "h2d_reco": h2d_reco,
        "rho_expected": rho_expected,
        "cov_total": cov_total,
        "total_err_expected": total_err,
        "rho_10pct": rho_10pct,
        "stat_err_10pct": stat_err_10pct,
        "n_hemi_10pct": n_hemi_10pct,
    }


def apply_correction(inputs):
    """Apply bin-by-bin correction to full data.

    correction C(i,j) = N_genBefore(i,j) / N_reco(i,j)
    corrected_counts(i,j) = N_data(i,j) * C(i,j)
    R_hemi = N_hemi_genBefore / N_hemi_reco
    N_hemi_corrected = N_hemi_data * R_hemi
    rho(i,j) = corrected_counts(i,j) / (N_hemi_corrected * bin_area)
    """
    h2d_data = inputs["h2d_data"]
    correction = inputs["correction"]
    n_hemi_data = inputs["n_hemi_data"]
    n_hemi_reco = inputs["n_hemi_reco"]
    n_hemi_genBefore = inputs["n_hemi_genBefore"]

    # Hemisphere efficiency correction factor
    R_hemi = n_hemi_genBefore / n_hemi_reco
    n_hemi_corrected = n_hemi_data * R_hemi

    # Apply bin-by-bin correction
    corrected_counts = h2d_data * correction

    # Density (using true bin areas, not a constant)
    dx = np.diff(inputs["x_edges"])
    dy = np.diff(inputs["y_edges"])
    bin_area = np.outer(dx, dy)
    rho_data = corrected_counts / (n_hemi_corrected * bin_area)

    # Statistical uncertainty: Poisson on data counts, propagated through C
    # sigma_rho = sqrt(N_data) * C / (N_hemi_corrected * bin_area)
    stat_err = np.zeros_like(rho_data)
    mask = h2d_data > 0
    stat_err[mask] = (
        np.sqrt(h2d_data[mask]) * correction[mask] / (n_hemi_corrected * bin_area[mask])
    )

    log.info("Hemisphere correction factor R_hemi = %.4f", R_hemi)
    log.info("N_hemi_data = %d, N_hemi_corrected = %.0f", n_hemi_data, n_hemi_corrected)
    log.info("Total corrected splittings: %.0f", np.sum(corrected_counts))

    # Normalization: integral of rho * bin_area = mean splittings per hemisphere
    integral = np.sum(rho_data * bin_area)
    log.info("Integral rho * dA = %.3f (mean splittings/hemisphere)", integral)

    return rho_data, stat_err, n_hemi_corrected, corrected_counts


def compare_to_expected(rho_data, stat_err_data, inputs):
    """Compare full data to expected result (MC pseudo-data)."""
    rho_expected = inputs["rho_expected"]
    total_err_expected = inputs["total_err_expected"].reshape(10, 10)

    # Populated bins
    populated = (rho_expected > 0) & (rho_data > 0)
    n_populated = np.sum(populated)
    log.info("Populated bins in both: %d", n_populated)

    # Combined uncertainty: data stat + expected total (stat + syst) in quadrature
    sigma = np.sqrt(stat_err_data**2 + total_err_expected**2)

    # Pulls
    pulls = np.zeros_like(rho_data)
    pulls[populated] = (rho_data[populated] - rho_expected[populated]) / sigma[populated]

    # Chi2 (diagonal)
    chi2_vals = pulls[populated] ** 2
    chi2_diag = np.sum(chi2_vals)
    ndf = n_populated
    p_value_diag = 1.0 - stats.chi2.cdf(chi2_diag, ndf) if ndf > 0 else 1.0

    # Chi2 with full covariance
    cov_total = inputs["cov_total"]
    rho_flat = rho_data.ravel()
    rho_exp_flat = rho_expected.ravel()
    stat_cov = np.diag(stat_err_data.ravel() ** 2)
    combined_cov = cov_total + stat_cov

    pop_flat = populated.ravel()
    pop_idx = np.where(pop_flat)[0]
    diff = (rho_flat - rho_exp_flat)[pop_idx]
    sub_cov = combined_cov[np.ix_(pop_idx, pop_idx)]

    try:
        inv_cov = np.linalg.inv(sub_cov)
        chi2_cov = float(diff @ inv_cov @ diff)
        p_value_cov = 1.0 - stats.chi2.cdf(chi2_cov, ndf) if ndf > 0 else 1.0
    except np.linalg.LinAlgError:
        chi2_cov = float("nan")
        p_value_cov = float("nan")
        log.warning("Covariance matrix singular -- full chi2 not available")

    log.info("\n=== Comparison to Expected (Full Data) ===")
    log.info("chi2/ndf (diagonal) = %.1f / %d = %.2f (p = %.4e)",
             chi2_diag, ndf, chi2_diag / ndf if ndf > 0 else 0, p_value_diag)
    log.info("chi2/ndf (full cov) = %.1f / %d = %.2f (p = %.4e)",
             chi2_cov, ndf, chi2_cov / ndf if ndf > 0 else 0, p_value_cov)
    log.info("Pull mean = %.3f", np.mean(pulls[populated]))
    log.info("Pull std = %.3f", np.std(pulls[populated]))
    log.info("Max |pull| = %.2f", np.max(np.abs(pulls[populated])))

    # Regional analysis
    x_centers = 0.5 * (inputs["x_edges"][:-1] + inputs["x_edges"][1:])
    y_centers = 0.5 * (inputs["y_edges"][:-1] + inputs["y_edges"][1:])
    xx, yy = np.meshgrid(x_centers, y_centers, indexing="ij")

    regions = {
        "Wide-angle (ln(1/dtheta) < 2.5)": (xx < 2.5) & populated,
        "Collinear (ln(1/dtheta) > 2.5)": (xx >= 2.5) & populated,
        "Hard (ln(kT) > 0.5)": (yy > 0.5) & populated,
        "Soft (ln(kT) < 0.5)": (yy <= 0.5) & populated,
    }
    log.info("\nRegional pull analysis:")
    region_stats = {}
    for name, rmask in regions.items():
        if np.sum(rmask) > 0:
            rp = pulls[rmask]
            log.info("  %s: mean=%.2f, std=%.2f, N=%d", name, np.mean(rp), np.std(rp), len(rp))
            region_stats[name] = {
                "mean": float(np.mean(rp)),
                "std": float(np.std(rp)),
                "n_bins": int(np.sum(rmask)),
            }

    # High-pull bins
    high_pull = np.abs(pulls) > 3
    n_high = np.sum(high_pull & populated)
    log.info("\nBins with |pull| > 3: %d / %d", n_high, n_populated)
    if n_high > 0:
        idx = np.argwhere(high_pull & populated)
        for ix, iy in idx:
            log.info(
                "  Bin (%d,%d) [%.1f-%.1f, %.1f-%.1f]: pull=%.2f, data=%.4f, expected=%.4f",
                ix, iy,
                inputs["x_edges"][ix], inputs["x_edges"][ix + 1],
                inputs["y_edges"][iy], inputs["y_edges"][iy + 1],
                pulls[ix, iy], rho_data[ix, iy], rho_expected[ix, iy],
            )

    return {
        "pulls": pulls,
        "populated": populated,
        "chi2_diag": float(chi2_diag),
        "chi2_cov": float(chi2_cov),
        "ndf": int(ndf),
        "p_value_diag": float(p_value_diag),
        "p_value_cov": float(p_value_cov),
        "pull_mean": float(np.mean(pulls[populated])),
        "pull_std": float(np.std(pulls[populated])),
        "max_abs_pull": float(np.max(np.abs(pulls[populated]))),
        "n_high_pull": int(n_high),
        "sigma": sigma,
        "region_stats": region_stats,
    }


def compare_to_10pct(rho_data, stat_err_data, inputs):
    """Compare full data to 10% partial result -- consistency check."""
    rho_10pct = inputs["rho_10pct"]
    stat_err_10pct = inputs["stat_err_10pct"]

    populated = (rho_data > 0) & (rho_10pct > 0)
    n_pop = np.sum(populated)

    # Combined uncertainty (10% stat dominates over full stat)
    sigma = np.sqrt(stat_err_data**2 + stat_err_10pct**2)

    pulls = np.zeros_like(rho_data)
    pulls[populated] = (rho_data[populated] - rho_10pct[populated]) / sigma[populated]

    chi2 = float(np.sum(pulls[populated] ** 2))
    ndf = int(n_pop)
    p_value = 1.0 - stats.chi2.cdf(chi2, ndf) if ndf > 0 else 1.0

    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_10pct[populated]

    log.info("\n=== Full vs 10%% Consistency ===")
    log.info("chi2/ndf = %.1f / %d = %.2f (p = %.4f)",
             chi2, ndf, chi2 / ndf if ndf > 0 else 0, p_value)
    log.info("Pull mean = %.3f, std = %.3f", np.mean(pulls[populated]), np.std(pulls[populated]))
    log.info("Density ratio mean = %.4f, std = %.4f",
             np.nanmean(ratio[populated]), np.nanstd(ratio[populated]))

    return {
        "chi2": chi2,
        "ndf": ndf,
        "p_value": p_value,
        "pull_mean": float(np.mean(pulls[populated])),
        "pull_std": float(np.std(pulls[populated])),
        "ratio_mean": float(np.nanmean(ratio[populated])),
        "ratio_std": float(np.nanstd(ratio[populated])),
        "pulls": pulls,
        "ratio": ratio,
    }


# =====================================================================
# Plotting functions
# =====================================================================

def plot_corrected_lund_plane(rho_data, inputs):
    """THE primary result: corrected full-data Lund jet plane density."""
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]

    fig, ax = plt.subplots(figsize=(10, 10))

    rho_plot = rho_data.copy()
    rho_plot[rho_plot == 0] = np.nan

    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="viridis", shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_lund_plane_full_corrected.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_lund_plane_full_corrected.pdf")


def plot_corrected_with_text(rho_data, stat_err_data, inputs):
    """Corrected Lund plane with per-bin values annotated."""
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]
    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])
    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    fig, ax = plt.subplots(figsize=(10, 10))

    rho_plot = rho_data.copy()
    rho_plot[rho_plot == 0] = np.nan

    im = ax.pcolormesh(x_edges, y_edges, rho_plot.T, cmap="viridis", shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")

    # Annotate populated bins
    for i in range(len(x_centers)):
        for j in range(len(y_centers)):
            if rho_data[i, j] > 0:
                txt = f"{rho_data[i, j]:.3f}"
                ax.text(
                    x_centers[i], y_centers[j], txt,
                    ha="center", va="center", fontsize=5, color="white",
                    fontweight="bold",
                )

    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (annotated)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_lund_plane_full_annotated.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_lund_plane_full_annotated.pdf")


def plot_ratio_to_expected(rho_data, inputs):
    """Plot 2D ratio of full data to expected."""
    rho_expected = inputs["rho_expected"]
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]

    populated = (rho_expected > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_expected[populated]

    fig, ax = plt.subplots(figsize=(10, 10))

    im = ax.pcolormesh(
        x_edges, y_edges, ratio.T, cmap="RdBu_r", vmin=0.8, vmax=1.2, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Data / MC Expected")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data / MC Expected",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_ratio_full_vs_expected.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_ratio_full_vs_expected.pdf")


def plot_pull_map(comparison, label_suffix=""):
    """Plot 2D pull map (data vs expected)."""
    pulls = comparison["pulls"]
    x_edges = np.linspace(0, 5, 11)
    y_edges = np.linspace(-3, 4, 11)

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

    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    fname = f"emeric_pull_map_full{label_suffix}"
    for fmt in ("pdf", "png"):
        fig.savefig(FIG_DIR / f"{fname}.{fmt}", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: %s.pdf", fname)


def plot_1d_projections(rho_data, stat_err_data, inputs, comparison):
    """Plot 1D projections with data points and MC band."""
    rho_expected = inputs["rho_expected"]
    total_err_expected = inputs["total_err_expected"].reshape(10, 10)
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)

    # --- ln(k_T) projection (sum over ln(1/Delta_theta)) ---
    rho_kt_data = np.sum(rho_data * dx[:, None], axis=0)
    rho_kt_exp = np.sum(rho_expected * dx[:, None], axis=0)
    err_kt_data = np.sqrt(np.sum((stat_err_data * dx[:, None]) ** 2, axis=0))
    err_kt_exp = np.sqrt(np.sum((total_err_expected * dx[:, None]) ** 2, axis=0))

    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    ax_main.errorbar(
        y_centers, rho_kt_data, yerr=err_kt_data,
        fmt="ko", markersize=5, label="Data (full)",
    )
    ax_main.fill_between(
        y_centers, rho_kt_exp - err_kt_exp, rho_kt_exp + err_kt_exp,
        alpha=0.3, color="C0", label="MC Expected",
    )
    ax_main.step(y_centers, rho_kt_exp, where="mid", color="C0")
    ax_main.set_ylabel(r"$\int \rho \, d\ln(1/\Delta\theta)$")
    ax_main.legend(fontsize="x-small")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    # Ratio panel
    sigma_tot = np.sqrt(err_kt_data**2 + err_kt_exp**2)
    ratio = np.ones_like(rho_kt_data)
    ratio_err = np.zeros_like(rho_kt_data)
    mask = rho_kt_exp > 0
    ratio[mask] = rho_kt_data[mask] / rho_kt_exp[mask]
    ratio_err[mask] = err_kt_data[mask] / rho_kt_exp[mask]

    ax_ratio.errorbar(y_centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.fill_between(
        y_centers,
        1 - err_kt_exp / np.where(rho_kt_exp > 0, rho_kt_exp, 1),
        1 + err_kt_exp / np.where(rho_kt_exp > 0, rho_kt_exp, 1),
        alpha=0.2, color="C0",
    )
    ax_ratio.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax_ratio.set_ylabel("Data / MC")
    ax_ratio.set_ylim(0.8, 1.2)

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_1d_kt_projection.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_1d_kt_projection.pdf")

    # --- ln(1/Delta_theta) projection (sum over ln(k_T)) ---
    rho_dt_data = np.sum(rho_data * dy[None, :], axis=1)
    rho_dt_exp = np.sum(rho_expected * dy[None, :], axis=1)
    err_dt_data = np.sqrt(np.sum((stat_err_data * dy[None, :]) ** 2, axis=1))
    err_dt_exp = np.sqrt(np.sum((total_err_expected * dy[None, :]) ** 2, axis=1))

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])

    fig, (ax_main, ax_ratio) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    ax_main.errorbar(
        x_centers, rho_dt_data, yerr=err_dt_data,
        fmt="ko", markersize=5, label="Data (full)",
    )
    ax_main.fill_between(
        x_centers, rho_dt_exp - err_dt_exp, rho_dt_exp + err_dt_exp,
        alpha=0.3, color="C0", label="MC Expected",
    )
    ax_main.step(x_centers, rho_dt_exp, where="mid", color="C0")
    ax_main.set_ylabel(r"$\int \rho \, d\ln(k_T)$")
    ax_main.legend(fontsize="x-small")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    ratio = np.ones_like(rho_dt_data)
    ratio_err = np.zeros_like(rho_dt_data)
    mask = rho_dt_exp > 0
    ratio[mask] = rho_dt_data[mask] / rho_dt_exp[mask]
    ratio_err[mask] = err_dt_data[mask] / rho_dt_exp[mask]

    ax_ratio.errorbar(x_centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    ax_ratio.axhline(1, color="gray", linestyle="--")
    ax_ratio.fill_between(
        x_centers,
        1 - err_dt_exp / np.where(rho_dt_exp > 0, rho_dt_exp, 1),
        1 + err_dt_exp / np.where(rho_dt_exp > 0, rho_dt_exp, 1),
        alpha=0.2, color="C0",
    )
    ax_ratio.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax_ratio.set_ylabel("Data / MC")
    ax_ratio.set_ylim(0.8, 1.2)

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_1d_dtheta_projection.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_1d_dtheta_projection.pdf")


def plot_full_vs_10pct_ratio(comp_10pct, inputs):
    """Plot 2D ratio of full to 10% corrected density."""
    ratio = comp_10pct["ratio"]
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]

    fig, ax = plt.subplots(figsize=(10, 10))

    im = ax.pcolormesh(
        x_edges, y_edges, ratio.T, cmap="RdBu_r", vmin=0.9, vmax=1.1, shading="flat",
    )
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Full Data / 10% Data")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data (Full / 10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_ratio_full_vs_10pct.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_ratio_full_vs_10pct.pdf")


def plot_pull_distribution(comparison):
    """Plot 1D histogram of pulls (data vs expected)."""
    pulls = comparison["pulls"]
    populated = comparison["populated"]
    pull_vals = pulls[populated]

    fig, ax = plt.subplots(figsize=(10, 10))

    bins = np.linspace(-8, 8, 33)
    ax.hist(pull_vals, bins=bins, histtype="stepfilled", alpha=0.6, color="C0", label="Pulls")

    # Overlay unit Gaussian
    x_gauss = np.linspace(-8, 8, 200)
    n_bins = len(pull_vals)
    bin_width = bins[1] - bins[0]
    ax.plot(
        x_gauss,
        n_bins * bin_width * stats.norm.pdf(x_gauss),
        "r--", lw=2, label=r"$\mathcal{N}(0,1)$",
    )

    ax.set_xlabel("Pull")
    ax.set_ylabel("Bins")
    ax.legend(fontsize="x-small")

    txt = (
        f"Mean = {comparison['pull_mean']:.2f}\n"
        f"Std = {comparison['pull_std']:.2f}\n"
        f"N = {n_bins}"
    )
    ax.text(0.95, 0.95, txt, transform=ax.transAxes, ha="right", va="top", fontsize="x-small")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data vs MC Expected",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    for fmt in ("pdf", "png"):
        fig.savefig(
            FIG_DIR / f"emeric_pull_distribution.{fmt}",
            bbox_inches="tight", dpi=200, transparent=True,
        )
    plt.close(fig)
    log.info("Saved: emeric_pull_distribution.pdf")


def main():
    log.info("=" * 70)
    log.info("Phase 4c Script 02: Full Data Correction and Comparison")
    log.info("Session: Emeric")
    log.info("=" * 70)

    # Load inputs
    inputs = load_inputs()
    log.info("Loaded full data: %d hemispheres", inputs["n_hemi_data"])
    log.info(
        "Correction factors: range [%.2f, %.2f]",
        np.min(inputs["correction"][inputs["correction"] > 0]),
        np.max(inputs["correction"]),
    )

    # Apply correction
    rho_data, stat_err_data, n_hemi_corrected, corrected_counts = apply_correction(inputs)

    # Compare to expected
    comparison = compare_to_expected(rho_data, stat_err_data, inputs)

    # Compare to 10%
    comp_10pct = compare_to_10pct(rho_data, stat_err_data, inputs)

    # Generate figures
    log.info("\n--- Generating figures ---")
    plot_corrected_lund_plane(rho_data, inputs)
    plot_corrected_with_text(rho_data, stat_err_data, inputs)
    plot_ratio_to_expected(rho_data, inputs)
    plot_pull_map(comparison)
    plot_pull_distribution(comparison)
    plot_1d_projections(rho_data, stat_err_data, inputs, comparison)
    plot_full_vs_10pct_ratio(comp_10pct, inputs)

    # Save numerical results
    np.savez(
        OUT_DIR / "corrected_full_emeric.npz",
        rho_data=rho_data,
        stat_err=stat_err_data,
        corrected_counts=corrected_counts,
        n_hemi_data=inputs["n_hemi_data"],
        n_hemi_corrected=n_hemi_corrected,
        pulls=comparison["pulls"],
        chi2_diag=comparison["chi2_diag"],
        chi2_cov=comparison["chi2_cov"],
        ndf=comparison["ndf"],
        p_value_diag=comparison["p_value_diag"],
        p_value_cov=comparison["p_value_cov"],
        x_edges=inputs["x_edges"],
        y_edges=inputs["y_edges"],
    )

    log.info("\n=== FINAL SUMMARY ===")
    log.info("Full data hemispheres: %d", inputs["n_hemi_data"])
    log.info("Corrected hemispheres: %.0f", n_hemi_corrected)
    log.info("Populated bins: %d / 100", comparison["ndf"])
    log.info(
        "chi2/ndf (diag) = %.1f / %d = %.2f (p = %.2e)",
        comparison["chi2_diag"], comparison["ndf"],
        comparison["chi2_diag"] / comparison["ndf"] if comparison["ndf"] > 0 else 0,
        comparison["p_value_diag"],
    )
    log.info(
        "chi2/ndf (cov) = %.1f / %d = %.2f",
        comparison["chi2_cov"], comparison["ndf"],
        comparison["chi2_cov"] / comparison["ndf"] if comparison["ndf"] > 0 else 0,
    )
    log.info(
        "Pull: mean = %.3f, std = %.3f, max|pull| = %.2f",
        comparison["pull_mean"], comparison["pull_std"], comparison["max_abs_pull"],
    )
    log.info("Bins with |pull| > 3: %d", comparison["n_high_pull"])
    log.info(
        "\nFull vs 10%%: chi2/ndf = %.1f/%d = %.2f (p = %.4f)",
        comp_10pct["chi2"], comp_10pct["ndf"],
        comp_10pct["chi2"] / comp_10pct["ndf"] if comp_10pct["ndf"] > 0 else 0,
        comp_10pct["p_value"],
    )
    log.info("  Density ratio: %.4f +/- %.4f", comp_10pct["ratio_mean"], comp_10pct["ratio_std"])


if __name__ == "__main__":
    main()
