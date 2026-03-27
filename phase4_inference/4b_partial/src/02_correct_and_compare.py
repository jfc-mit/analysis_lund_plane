#!/usr/bin/env python3
"""Phase 4b Script 02: Apply corrections to 10% data, compare to expected.

Applies full-MC bin-by-bin correction factors to the 10% data subsample.
Computes corrected Lund plane density, pulls vs expected, chi2.

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
OUT_DIR = BASE / "phase4_inference" / "4b_partial" / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

BIN_AREA = 0.5 * 0.7  # dx * dy for uniform bins


def load_inputs():
    """Load 10% data, correction factors, and expected results."""
    # 10% data
    d10 = np.load(OUT_DIR / "data_10pct_lund_oscar.npz")
    h2d_data = d10["h2d"]
    n_hemi_data = int(d10["n_hemispheres"])
    x_edges = d10["x_edges"]
    y_edges = d10["y_edges"]

    # Full MC correction factors (from Phase 3)
    corr_d = np.load(BASE / "phase3_selection" / "outputs" / "correction_ingrid.npz")
    correction = corr_d["correction"]
    n_hemi_reco = float(corr_d["n_hemi_reco"])
    n_hemi_genBefore = float(corr_d["n_hemi_genBefore"])
    h2d_reco = corr_d["h2d_reco"]

    # Expected results from Phase 4a
    exp = np.load(BASE / "phase4_inference" / "4a_expected" / "outputs" /
                  "expected_results_felix.npz")
    rho_expected = exp["rho_corrected_bbb"]

    # Covariance from Phase 4a
    cov_d = np.load(BASE / "phase4_inference" / "4a_expected" / "outputs" /
                    "covariance_felix.npz")
    cov_total = cov_d["cov_total"]
    total_err = cov_d["total_err"]

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
    }


def apply_correction(inputs):
    """Apply bin-by-bin correction to 10% data.

    The correction factor C(i,j) = N_genBefore(i,j) / N_reco(i,j) maps
    reco-level counts to particle-level (genBefore) counts.

    corrected_counts(i,j) = N_data(i,j) * C(i,j)

    Normalization: the corrected counts are at the genBefore level.
    The density is normalized per hemisphere at the corrected level:
    rho(i,j) = corrected_counts(i,j) / (N_hemi_corrected * bin_area)

    where N_hemi_corrected = N_hemi_data * R_hemi, and
    R_hemi = N_hemi_genBefore / N_hemi_reco is the hemisphere-level correction.

    This is consistent with how Phase 4a computed the expected:
    rho = (N_reco * C) / (N_hemi_genBefore * bin_area)
    For MC pseudo-data, N_hemi_data = N_hemi_reco, so
    N_hemi_corrected = N_hemi_reco * (N_hemi_genBefore / N_hemi_reco) = N_hemi_genBefore.
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

    # Density
    dx = np.diff(inputs["x_edges"])
    dy = np.diff(inputs["y_edges"])
    bin_area = np.outer(dx, dy)
    rho_data = corrected_counts / (n_hemi_corrected * bin_area)

    # Statistical uncertainty: Poisson on data counts, propagated through C
    # sigma_rho = sqrt(N_data) * C / (N_hemi_corrected * bin_area)
    stat_err = np.zeros_like(rho_data)
    mask = h2d_data > 0
    stat_err[mask] = np.sqrt(h2d_data[mask]) * correction[mask] / (n_hemi_corrected * bin_area[mask])

    log.info("Hemisphere correction factor R_hemi = %.4f", R_hemi)
    log.info("N_hemi_data = %d, N_hemi_corrected = %.0f", n_hemi_data, n_hemi_corrected)
    log.info("Total corrected splittings: %.0f", np.sum(corrected_counts))

    return rho_data, stat_err, n_hemi_corrected


def compare_to_expected(rho_data, stat_err_data, inputs):
    """Compare 10% data to expected result (MC pseudo-data)."""
    rho_expected = inputs["rho_expected"]
    total_err_expected = inputs["total_err_expected"].reshape(10, 10)

    # Populated bins
    populated = (rho_expected > 0) & (rho_data > 0)
    n_populated = np.sum(populated)
    log.info("Populated bins in both: %d", n_populated)

    # Combined uncertainty for pull computation
    # For 10% data: stat uncertainty dominates (sqrt(10) larger relative to full data)
    # Use data stat error + expected total error in quadrature
    sigma = np.sqrt(stat_err_data**2 + total_err_expected**2)

    # Pulls
    pulls = np.zeros_like(rho_data)
    pulls[populated] = (rho_data[populated] - rho_expected[populated]) / sigma[populated]

    # Chi2 (using diagonal -- simplified, since we don't have off-diagonal for data yet)
    chi2_vals = pulls[populated]**2
    chi2 = np.sum(chi2_vals)
    ndf = n_populated
    p_value = 1.0 - stats.chi2.cdf(chi2, ndf) if ndf > 0 else 1.0

    log.info("\n=== Comparison to Expected ===")
    log.info("chi2/ndf = %.2f / %d = %.3f", chi2, ndf, chi2 / ndf if ndf > 0 else 0)
    log.info("p-value = %.4f", p_value)
    log.info("Pull mean = %.3f", np.mean(pulls[populated]))
    log.info("Pull std = %.3f", np.std(pulls[populated]))
    log.info("Max |pull| = %.2f", np.max(np.abs(pulls[populated])))

    # Check for bins with |pull| > 3
    high_pull = np.abs(pulls) > 3
    n_high = np.sum(high_pull & populated)
    if n_high > 0:
        log.warning("WARNING: %d bins with |pull| > 3", n_high)
        idx = np.argwhere(high_pull & populated)
        for ix, iy in idx:
            log.warning("  Bin (%d,%d): pull=%.2f, data=%.4f, expected=%.4f, sigma=%.4f",
                        ix, iy, pulls[ix, iy], rho_data[ix, iy],
                        rho_expected[ix, iy], sigma[ix, iy])
    else:
        log.info("No bins with |pull| > 3")

    return {
        "pulls": pulls,
        "chi2": float(chi2),
        "ndf": int(ndf),
        "p_value": float(p_value),
        "pull_mean": float(np.mean(pulls[populated])),
        "pull_std": float(np.std(pulls[populated])),
        "max_abs_pull": float(np.max(np.abs(pulls[populated]))),
        "n_high_pull": int(n_high),
        "sigma": sigma,
    }


def plot_corrected_lund_plane(rho_data, inputs):
    """Plot the corrected 10% data Lund plane."""
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
        exp="ALEPH", data=True, llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "oscar_lund_plane_10pct_corrected.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_lund_plane_10pct_corrected.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_lund_plane_10pct_corrected.pdf")


def plot_ratio_to_expected(rho_data, inputs):
    """Plot 2D ratio of 10% data to expected."""
    rho_expected = inputs["rho_expected"]
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]

    populated = (rho_expected > 0) & (rho_data > 0)
    ratio = np.full_like(rho_data, np.nan)
    ratio[populated] = rho_data[populated] / rho_expected[populated]

    fig, ax = plt.subplots(figsize=(10, 10))

    im = ax.pcolormesh(x_edges, y_edges, ratio.T, cmap="RdBu_r",
                       vmin=0.7, vmax=1.3, shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="10% Data / Expected")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "oscar_ratio_10pct_vs_expected.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_ratio_10pct_vs_expected.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_ratio_10pct_vs_expected.pdf")


def plot_pull_map(comparison):
    """Plot 2D pull map."""
    pulls = comparison["pulls"]
    x_edges = np.linspace(0, 5, 11)
    y_edges = np.linspace(-3, 4, 11)

    pull_plot = pulls.copy()
    pull_plot[(pulls == 0) & (np.abs(pulls) < 1e-10)] = np.nan

    fig, ax = plt.subplots(figsize=(10, 10))

    im = ax.pcolormesh(x_edges, y_edges, pull_plot.T, cmap="RdBu_r",
                       vmin=-3, vmax=3, shading="flat")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Pull = (Data - Expected) / $\\sigma$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")

    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "oscar_pull_map_10pct.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_pull_map_10pct.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_pull_map_10pct.pdf")


def plot_1d_projections(rho_data, stat_err_data, inputs, comparison):
    """Plot 1D projections with data points and MC overlay."""
    rho_expected = inputs["rho_expected"]
    total_err_expected = inputs["total_err_expected"].reshape(10, 10)
    x_edges = inputs["x_edges"]
    y_edges = inputs["y_edges"]
    dx = np.diff(x_edges)
    dy = np.diff(y_edges)

    # --- ln(k_T) projection (sum over ln(1/Delta_theta)) ---
    rho_kt_data = np.sum(rho_data * dx[:, None], axis=0)
    rho_kt_exp = np.sum(rho_expected * dx[:, None], axis=0)
    err_kt_data = np.sqrt(np.sum((stat_err_data * dx[:, None])**2, axis=0))
    err_kt_exp = np.sqrt(np.sum((total_err_expected * dx[:, None])**2, axis=0))

    y_centers = 0.5 * (y_edges[:-1] + y_edges[1:])

    fig, (ax_main, ax_pull) = plt.subplots(2, 1, figsize=(10, 10),
                                            gridspec_kw={"height_ratios": [3, 1]},
                                            sharex=True)
    fig.subplots_adjust(hspace=0)

    ax_main.errorbar(y_centers, rho_kt_data, yerr=err_kt_data,
                     fmt="ko", markersize=5, label="Data (10%)")
    ax_main.fill_between(y_centers, rho_kt_exp - err_kt_exp, rho_kt_exp + err_kt_exp,
                         alpha=0.3, color="C0", label="MC Expected")
    ax_main.step(y_centers, rho_kt_exp, where="mid", color="C0")
    ax_main.set_ylabel(r"$\int \rho \, d\ln(1/\Delta\theta)$")
    ax_main.legend(fontsize="x-small")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    # Pull panel
    sigma_tot = np.sqrt(err_kt_data**2 + err_kt_exp**2)
    pull_kt = np.zeros_like(rho_kt_data)
    mask = sigma_tot > 0
    pull_kt[mask] = (rho_kt_data[mask] - rho_kt_exp[mask]) / sigma_tot[mask]

    ax_pull.errorbar(y_centers, pull_kt, yerr=1.0, fmt="ko", markersize=4)
    ax_pull.axhline(0, color="gray", linestyle="--")
    ax_pull.axhline(2, color="gray", linestyle=":", alpha=0.5)
    ax_pull.axhline(-2, color="gray", linestyle=":", alpha=0.5)
    ax_pull.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax_pull.set_ylabel("Pull")
    ax_pull.set_ylim(-4, 4)

    fig.savefig(FIG_DIR / "oscar_1d_kt_projection.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_1d_kt_projection.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_1d_kt_projection.pdf")

    # --- ln(1/Delta_theta) projection (sum over ln(k_T)) ---
    rho_dt_data = np.sum(rho_data * dy[None, :], axis=1)
    rho_dt_exp = np.sum(rho_expected * dy[None, :], axis=1)
    err_dt_data = np.sqrt(np.sum((stat_err_data * dy[None, :])**2, axis=1))
    err_dt_exp = np.sqrt(np.sum((total_err_expected * dy[None, :])**2, axis=1))

    x_centers = 0.5 * (x_edges[:-1] + x_edges[1:])

    fig, (ax_main, ax_pull) = plt.subplots(2, 1, figsize=(10, 10),
                                            gridspec_kw={"height_ratios": [3, 1]},
                                            sharex=True)
    fig.subplots_adjust(hspace=0)

    ax_main.errorbar(x_centers, rho_dt_data, yerr=err_dt_data,
                     fmt="ko", markersize=5, label="Data (10%)")
    ax_main.fill_between(x_centers, rho_dt_exp - err_dt_exp, rho_dt_exp + err_dt_exp,
                         alpha=0.3, color="C0", label="MC Expected")
    ax_main.step(x_centers, rho_dt_exp, where="mid", color="C0")
    ax_main.set_ylabel(r"$\int \rho \, d\ln(k_T)$")
    ax_main.legend(fontsize="x-small")

    mh.label.exp_label(
        exp="ALEPH", data=True, llabel="Open Data (10%)",
        rlabel=r"$\sqrt{s} = 91.2$ GeV", loc=0, ax=ax_main,
    )

    sigma_tot = np.sqrt(err_dt_data**2 + err_dt_exp**2)
    pull_dt = np.zeros_like(rho_dt_data)
    mask = sigma_tot > 0
    pull_dt[mask] = (rho_dt_data[mask] - rho_dt_exp[mask]) / sigma_tot[mask]

    ax_pull.errorbar(x_centers, pull_dt, yerr=1.0, fmt="ko", markersize=4)
    ax_pull.axhline(0, color="gray", linestyle="--")
    ax_pull.axhline(2, color="gray", linestyle=":", alpha=0.5)
    ax_pull.axhline(-2, color="gray", linestyle=":", alpha=0.5)
    ax_pull.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax_pull.set_ylabel("Pull")
    ax_pull.set_ylim(-4, 4)

    fig.savefig(FIG_DIR / "oscar_1d_dtheta_projection.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "oscar_1d_dtheta_projection.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved: oscar_1d_dtheta_projection.pdf")


def main():
    log.info("=" * 70)
    log.info("Phase 4b Script 02: Correction and Comparison to Expected")
    log.info("Session: Oscar")
    log.info("=" * 70)

    # Load inputs
    inputs = load_inputs()
    log.info("Loaded 10%% data: %d hemispheres", inputs["n_hemi_data"])
    log.info("Correction factors: range [%.2f, %.2f]",
             np.min(inputs["correction"][inputs["correction"] > 0]),
             np.max(inputs["correction"]))

    # Apply correction
    rho_data, stat_err_data, n_hemi_corrected = apply_correction(inputs)

    # Compare to expected
    comparison = compare_to_expected(rho_data, stat_err_data, inputs)

    # Generate figures
    plot_corrected_lund_plane(rho_data, inputs)
    plot_ratio_to_expected(rho_data, inputs)
    plot_pull_map(comparison)
    plot_1d_projections(rho_data, stat_err_data, inputs, comparison)

    # Save numerical results
    np.savez(
        OUT_DIR / "corrected_10pct_oscar.npz",
        rho_data=rho_data,
        stat_err=stat_err_data,
        n_hemi_data=inputs["n_hemi_data"],
        n_hemi_corrected=n_hemi_corrected,
        pulls=comparison["pulls"],
        chi2=comparison["chi2"],
        ndf=comparison["ndf"],
        p_value=comparison["p_value"],
        x_edges=inputs["x_edges"],
        y_edges=inputs["y_edges"],
    )

    log.info("\n=== Summary ===")
    log.info("10%% data hemispheres: %d", inputs["n_hemi_data"])
    log.info("Corrected hemispheres: %.0f", n_hemi_corrected)
    log.info("chi2/ndf = %.2f / %d = %.3f (p = %.4f)",
             comparison["chi2"], comparison["ndf"],
             comparison["chi2"] / comparison["ndf"] if comparison["ndf"] > 0 else 0,
             comparison["p_value"])
    log.info("Pull: mean = %.3f, std = %.3f, max|pull| = %.2f",
             comparison["pull_mean"], comparison["pull_std"], comparison["max_abs_pull"])
    log.info("Bins with |pull| > 3: %d", comparison["n_high_pull"])


if __name__ == "__main__":
    main()
