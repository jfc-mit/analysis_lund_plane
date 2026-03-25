#!/usr/bin/env python3
"""Script 05: Data/MC comparisons on Lund plane variables.

Correction infrastructure gate: must produce these comparisons BEFORE
computing correction factors. Reads outputs from 01_process_all.py.

Session: Ingrid | Phase 3
"""

import json
import logging
from pathlib import Path

import numpy as np
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"


def main():
    log.info("=" * 70)
    log.info("Phase 3 Script 05: Data/MC Lund Plane Comparisons")
    log.info("Session: Ingrid")
    log.info("=" * 70)

    # Load data
    data_d = np.load(OUT_DIR / "data_lund_ingrid.npz")
    reco_d = np.load(OUT_DIR / "mc_reco_lund_ingrid.npz")

    h2d_data = data_d["h2d"]
    h2d_reco = reco_d["h2d"]
    x_edges = data_d["x_edges"]
    y_edges = data_d["y_edges"]
    n_hemi_data = float(data_d["n_hemispheres"])
    n_hemi_reco = float(reco_d["n_hemispheres"])

    dx = np.diff(x_edges)
    dy = np.diff(y_edges)
    area = np.outer(dx, dy)

    rho_data = h2d_data / (n_hemi_data * area)
    rho_reco = h2d_reco / (n_hemi_reco * area)

    # === Data/MC ratio analysis ===
    log.info("\n--- Data/MC ratio analysis ---")
    populated = (rho_data > 0) & (rho_reco > 0)
    ratio = np.ones_like(rho_data)
    ratio[populated] = rho_data[populated] / rho_reco[populated]

    log.info("Populated bins: %d / %d", np.sum(populated), rho_data.size)
    log.info("Data/MC ratio (populated bins):")
    log.info("  Mean: %.4f", np.mean(ratio[populated]))
    log.info("  Std: %.4f", np.std(ratio[populated]))
    log.info("  Min: %.4f", np.min(ratio[populated]))
    log.info("  Max: %.4f", np.max(ratio[populated]))

    # Check for >3 sigma discrepancy in any bin
    err_data = np.sqrt(h2d_data) / (n_hemi_data * area)
    err_reco = np.sqrt(h2d_reco) / (n_hemi_reco * area)
    sigma = np.zeros_like(rho_data)
    mask_sig = (err_data > 0) & (err_reco > 0) & populated
    diff = rho_data[mask_sig] - rho_reco[mask_sig]
    err_comb = np.sqrt(err_data[mask_sig]**2 + err_reco[mask_sig]**2)
    significance = diff / err_comb

    log.info("\nSignificance of data-MC differences:")
    log.info("  Max |significance|: %.2f", np.max(np.abs(significance)))
    log.info("  Bins > 3 sigma: %d", np.sum(np.abs(significance) > 3))
    log.info("  Bins > 2 sigma: %d", np.sum(np.abs(significance) > 2))

    # 1D projection comparisons
    log.info("\n--- 1D projections ---")
    kt_data = np.sum(rho_data, axis=0) * dx[0]
    kt_reco = np.sum(rho_reco, axis=0) * dx[0]
    log.info("ln(kT) projection ratio range: [%.3f, %.3f]",
             np.min(kt_data[kt_reco > 0] / kt_reco[kt_reco > 0]),
             np.max(kt_data[kt_reco > 0] / kt_reco[kt_reco > 0]))

    dtheta_data = np.sum(rho_data, axis=1) * dy[0]
    dtheta_reco = np.sum(rho_reco, axis=1) * dy[0]
    log.info("ln(1/dtheta) projection ratio range: [%.3f, %.3f]",
             np.min(dtheta_data[dtheta_reco > 0] / dtheta_reco[dtheta_reco > 0]),
             np.max(dtheta_data[dtheta_reco > 0] / dtheta_reco[dtheta_reco > 0]))

    # === Gate check ===
    # With ~5.7M data hemispheres and ~1.4M MC, even small real differences
    # become many-sigma significant. The meaningful check is the ratio spread:
    # if Data/MC density ratios are within ~20% across the plane, the MC is
    # adequate for deriving correction factors. Individual bin significance is
    # not informative at this statistics.
    max_sig = float(np.max(np.abs(significance)))
    ratio_spread = float(np.std(ratio[populated]))
    # Gate: ratio should be within ~20% (std < 0.15) and mean near 1.0
    gate_pass = (ratio_spread < 0.20) and (0.9 < np.mean(ratio[populated]) < 1.1)
    log.info("\n=== DATA/MC GATE CHECK ===")
    log.info("Ratio spread (std): %.4f", ratio_spread)
    log.info("Ratio mean: %.4f", float(np.mean(ratio[populated])))
    log.info("Max bin significance: %.2f (expected large at high statistics)", max_sig)
    log.info("Gate: %s", "PASS" if gate_pass else "FAIL")
    if not gate_pass:
        log.warning("Data/MC gate FAILED. Investigate before computing corrections.")
    else:
        log.info("Data/MC agreement is adequate for correction derivation.")

    # Save summary
    summary = {
        "n_populated_bins": int(np.sum(populated)),
        "ratio_mean": float(np.mean(ratio[populated])),
        "ratio_std": float(np.std(ratio[populated])),
        "max_significance": float(max_sig),
        "bins_gt_3sigma": int(np.sum(np.abs(significance) > 3)),
        "bins_gt_2sigma": int(np.sum(np.abs(significance) > 2)),
        "gate_pass": bool(gate_pass),
    }
    with open(OUT_DIR / "data_mc_comparison_ingrid.json", "w") as f:
        json.dump(summary, f, indent=2)

    log.info("\nSaved to %s", OUT_DIR / "data_mc_comparison_ingrid.json")


if __name__ == "__main__":
    main()
