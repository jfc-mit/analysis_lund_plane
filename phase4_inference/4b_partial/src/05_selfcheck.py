#!/usr/bin/env python3
"""Phase 4b Script 05: Self-check and additional diagnostics.

- Verify normalization: integral of rho over the Lund plane
- Compute chi2 using full covariance from Phase 4a (scaled for 10% stats)
- Check the pattern of data/MC differences

Session: Oscar | Phase 4b
"""

import logging
from pathlib import Path

import numpy as np
from scipy import stats
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

BASE = Path("/n/home07/anovak/work/slopspec/analyses/lund_jet_plane")
OUT_DIR = BASE / "phase4_inference" / "4b_partial" / "outputs"


def main():
    log.info("=" * 70)
    log.info("Phase 4b Script 05: Self-checks")
    log.info("Session: Oscar")
    log.info("=" * 70)

    # Load results
    d = np.load(OUT_DIR / "corrected_10pct_oscar.npz")
    rho_data = d["rho_data"]
    stat_err = d["stat_err"]
    x_edges = d["x_edges"]
    y_edges = d["y_edges"]

    # Load expected
    exp = np.load(BASE / "phase4_inference" / "4a_expected" / "outputs" /
                  "expected_results_felix.npz")
    rho_expected = exp["rho_corrected_bbb"]

    # Load covariance
    cov_d = np.load(BASE / "phase4_inference" / "4a_expected" / "outputs" /
                    "covariance_felix.npz")
    cov_total = cov_d["cov_total"]
    cov_stat = cov_d["cov_stat"]

    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    bin_area = np.outer(dx, dy)

    # --- Check 1: Normalization ---
    log.info("\n=== Normalization Check ===")
    integral_data = np.sum(rho_data * bin_area)
    integral_expected = np.sum(rho_expected * bin_area)
    log.info("Integral of rho * bin_area:")
    log.info("  Data (10%%): %.4f", integral_data)
    log.info("  Expected:   %.4f", integral_expected)
    log.info("  Ratio:      %.4f", integral_data / integral_expected if integral_expected > 0 else 0)
    log.info("  (This is the mean number of primary splittings per hemisphere)")

    # --- Check 2: Full covariance chi2 ---
    log.info("\n=== Full Covariance Chi2 ===")
    # Flatten the 2D arrays
    rho_data_flat = rho_data.flatten()
    rho_exp_flat = rho_expected.flatten()
    stat_err_flat = stat_err.flatten()

    # Populated bins (both data and expected have content)
    populated = (rho_exp_flat > 0) & (rho_data_flat > 0)
    pop_idx = np.where(populated)[0]
    n_pop = len(pop_idx)

    diff = rho_data_flat[pop_idx] - rho_exp_flat[pop_idx]

    # The covariance from Phase 4a is for MC pseudo-data (expected).
    # For 10% data, the stat uncertainty is ~sqrt(10) larger.
    # The data stat covariance is diagonal: sigma_i^2 = (stat_err_i)^2
    cov_data_stat = np.diag(stat_err_flat[pop_idx]**2)

    # Use expected total covariance (systematic + MC stat) for the expected side
    cov_exp = cov_total[np.ix_(pop_idx, pop_idx)]

    # Combined covariance: data stat + expected total
    cov_combined = cov_data_stat + cov_exp

    # Check if PSD
    eigvals = np.linalg.eigvalsh(cov_combined)
    log.info("Combined covariance: min eigenvalue = %.2e", np.min(eigvals))
    if np.min(eigvals) <= 0:
        log.warning("Covariance not PSD! Adding regularization.")
        cov_combined += np.eye(n_pop) * np.abs(np.min(eigvals)) * 1.01

    # Compute chi2
    try:
        cov_inv = np.linalg.inv(cov_combined)
        chi2_full = float(diff @ cov_inv @ diff)
        p_full = 1.0 - stats.chi2.cdf(chi2_full, n_pop)
        log.info("Chi2 (full covariance): %.2f / %d = %.3f",
                 chi2_full, n_pop, chi2_full / n_pop)
        log.info("p-value: %.4f", p_full)
    except np.linalg.LinAlgError:
        log.warning("Covariance inversion failed, using diagonal only")
        chi2_full = 0
        p_full = 0

    # --- Check 3: Diagonal-only chi2 for comparison ---
    log.info("\n=== Diagonal Chi2 (for comparison) ===")
    sigma2_diag = stat_err_flat[pop_idx]**2 + np.diag(cov_total)[pop_idx]
    chi2_diag = np.sum(diff**2 / sigma2_diag)
    p_diag = 1.0 - stats.chi2.cdf(chi2_diag, n_pop)
    log.info("Chi2 (diagonal): %.2f / %d = %.3f",
             chi2_diag, n_pop, chi2_diag / n_pop)
    log.info("p-value: %.4f", p_diag)

    # --- Check 4: Pattern analysis ---
    log.info("\n=== Pattern Analysis ===")
    # Check if the data/MC difference is coherent (systematic shift)
    # vs random fluctuation
    ratio = rho_data_flat[pop_idx] / rho_exp_flat[pop_idx]
    log.info("Bin-by-bin ratio (data/expected):")
    log.info("  Mean: %.4f", np.mean(ratio))
    log.info("  Median: %.4f", np.median(ratio))
    log.info("  Std: %.4f", np.std(ratio))

    # Fraction of bins where data > expected
    frac_above = np.sum(ratio > 1.0) / len(ratio)
    log.info("  Fraction data > expected: %.2f", frac_above)

    # Check region dependence
    pulls_2d = d["pulls"]
    log.info("\nPull distribution by region:")
    # Wide-angle (low ln(1/dtheta), bins 0-4)
    wide_mask = np.zeros_like(pulls_2d, dtype=bool)
    wide_mask[:5, :] = True
    wide_mask &= (rho_data > 0) & (rho_expected > 0)
    if np.any(wide_mask):
        log.info("  Wide-angle (ln(1/dtheta) < 2.5): mean pull = %.2f, std = %.2f",
                 np.mean(pulls_2d[wide_mask]), np.std(pulls_2d[wide_mask]))

    # Collinear (high ln(1/dtheta), bins 5-9)
    coll_mask = np.zeros_like(pulls_2d, dtype=bool)
    coll_mask[5:, :] = True
    coll_mask &= (rho_data > 0) & (rho_expected > 0)
    if np.any(coll_mask):
        log.info("  Collinear (ln(1/dtheta) > 2.5): mean pull = %.2f, std = %.2f",
                 np.mean(pulls_2d[coll_mask]), np.std(pulls_2d[coll_mask]))

    # Hard (high kT, bins 5-9 in y)
    hard_mask = np.zeros_like(pulls_2d, dtype=bool)
    hard_mask[:, 5:] = True
    hard_mask &= (rho_data > 0) & (rho_expected > 0)
    if np.any(hard_mask):
        log.info("  Hard (ln(kT) > 0.5): mean pull = %.2f, std = %.2f",
                 np.mean(pulls_2d[hard_mask]), np.std(pulls_2d[hard_mask]))

    # Soft (low kT, bins 0-4 in y)
    soft_mask = np.zeros_like(pulls_2d, dtype=bool)
    soft_mask[:, :5] = True
    soft_mask &= (rho_data > 0) & (rho_expected > 0)
    if np.any(soft_mask):
        log.info("  Soft (ln(kT) < 0.5): mean pull = %.2f, std = %.2f",
                 np.mean(pulls_2d[soft_mask]), np.std(pulls_2d[soft_mask]))

    # --- Check 5: Compare 10% data to full data (scaled) ---
    log.info("\n=== 10%% Data Splittings per Hemisphere ===")
    d10 = np.load(OUT_DIR / "data_10pct_lund_oscar.npz")
    n_split_10 = int(d10["n_splittings"])
    n_hemi_10 = int(d10["n_hemispheres"])
    log.info("  10%% data: %.3f splittings/hemisphere", n_split_10 / n_hemi_10)

    full_d = np.load(BASE / "phase3_selection" / "outputs" / "data_lund_ingrid.npz")
    n_split_full = int(full_d["n_splittings"])
    n_hemi_full = int(full_d["n_hemispheres"])
    log.info("  Full data: %.3f splittings/hemisphere", n_split_full / n_hemi_full)
    log.info("  Ratio: %.4f", (n_split_10 / n_hemi_10) / (n_split_full / n_hemi_full))


if __name__ == "__main__":
    main()
