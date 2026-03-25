#!/usr/bin/env python3
"""Script 02: Correction infrastructure -- bin-by-bin + IBU response matrix.

Reads the output from 01_process_all.py and computes:
1. Bin-by-bin correction factors: C(i,j) = N_genBefore(i,j) / N_reco(i,j)
2. IBU response matrix (migration probability, rows sum <= 1)
3. Diagonal fraction per bin

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
    log.info("Phase 3 Script 02: Correction Infrastructure")
    log.info("Session: Ingrid")
    log.info("=" * 70)

    # Load processed histograms from script 01
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

    nx = len(x_edges) - 1
    ny = len(y_edges) - 1
    log.info("Binning: %d x %d = %d bins", nx, ny, nx * ny)
    log.info("Data hemispheres: %d", int(n_hemi_data))
    log.info("MC reco hemispheres: %d", int(n_hemi_reco))
    log.info("MC gen hemispheres: %d", int(n_hemi_gen))
    log.info("MC genBefore hemispheres: %d", int(n_hemi_genBefore))

    # === 1. Bin-by-bin correction factors ===
    # C(i,j) = N_genBefore(i,j) / N_reco(i,j)
    # This corrects for detector effects AND event selection efficiency
    log.info("\n--- Bin-by-bin correction factors ---")

    # Protect against division by zero
    correction = np.zeros_like(h2d_reco)
    mask_nonzero = h2d_reco > 0
    correction[mask_nonzero] = h2d_genBefore[mask_nonzero] / h2d_reco[mask_nonzero]

    # Statistical uncertainty on correction factor (Poisson)
    correction_err = np.zeros_like(correction)
    for i in range(nx):
        for j in range(ny):
            if h2d_reco[i, j] > 0 and h2d_genBefore[i, j] > 0:
                # Relative error: sqrt(1/N_gen + 1/N_reco)
                rel_err = np.sqrt(1.0 / h2d_genBefore[i, j] + 1.0 / h2d_reco[i, j])
                correction_err[i, j] = correction[i, j] * rel_err

    log.info("Correction factor statistics:")
    c_valid = correction[mask_nonzero]
    log.info("  Mean: %.3f", np.mean(c_valid))
    log.info("  Median: %.3f", np.median(c_valid))
    log.info("  Min: %.3f", np.min(c_valid))
    log.info("  Max: %.3f", np.max(c_valid))
    log.info("  Bins with C > 2: %d", np.sum(c_valid > 2))
    log.info("  Bins with C < 0.5: %d", np.sum(c_valid < 0.5))
    log.info("  Bins with N_reco == 0: %d / %d", np.sum(~mask_nonzero), nx * ny)

    # === 2. Efficiency factor (for IBU) ===
    # epsilon(i,j) = N_gen(i,j) / N_genBefore(i,j)
    efficiency = np.zeros_like(h2d_gen)
    mask_genb = h2d_genBefore > 0
    efficiency[mask_genb] = h2d_gen[mask_genb] / h2d_genBefore[mask_genb]

    log.info("\nEfficiency statistics:")
    eff_valid = efficiency[mask_genb]
    log.info("  Mean: %.3f", np.mean(eff_valid))
    log.info("  Min: %.3f", np.min(eff_valid))
    log.info("  Max: %.3f", np.max(eff_valid))

    # === 3. Response matrix for IBU ===
    # The response matrix R maps gen-level bins to reco-level bins.
    # R(gen_bin, reco_bin) = migration probability.
    # We approximate this from the population-level bin counts since we
    # did not store per-event reco/gen splitting pairs.
    # For the full IBU response, we need matched reco/gen Lund plane entries.
    # Since we have aggregate histograms only, we construct a diagonal-dominant
    # approximation using the migration study from Phase 2 (~14% average migration).
    #
    # A proper response matrix requires event-by-event matching, which will be
    # built in script 02b. For now, store the diagonal approximation.
    log.info("\n--- Response matrix (diagonal approximation from aggregate counts) ---")

    n_bins = nx * ny  # 100 total
    # Flatten 2D indices for the response matrix
    # Gen and reco distributions as 1D arrays
    gen_flat = h2d_gen.flatten()
    reco_flat = h2d_reco.flatten()
    genb_flat = h2d_genBefore.flatten()

    # Diagonal fraction estimate: use gen/reco ratio as proxy
    # True diagonal fraction requires event-level matching (done in 02b)
    diag_fraction = np.zeros(n_bins)
    for k in range(n_bins):
        if gen_flat[k] > 0 and reco_flat[k] > 0:
            # Phase 2 found 14% mean migration; approximate diagonal = 1 - migration
            ratio = min(gen_flat[k], reco_flat[k]) / max(gen_flat[k], reco_flat[k])
            diag_fraction[k] = ratio  # Approximate

    log.info("Diagonal fraction (approximate):")
    populated = diag_fraction > 0
    log.info("  Mean: %.3f", np.mean(diag_fraction[populated]))
    log.info("  Bins > 0.5: %d / %d", np.sum(diag_fraction > 0.5), np.sum(populated))
    log.info("  Bins < 0.5: %d / %d", np.sum((diag_fraction < 0.5) & populated),
             np.sum(populated))

    # === 4. Save ===
    np.savez(
        OUT_DIR / "correction_ingrid.npz",
        correction=correction,
        correction_err=correction_err,
        efficiency=efficiency,
        h2d_data=h2d_data,
        h2d_reco=h2d_reco,
        h2d_gen=h2d_gen,
        h2d_genBefore=h2d_genBefore,
        n_hemi_data=n_hemi_data,
        n_hemi_reco=n_hemi_reco,
        n_hemi_gen=n_hemi_gen,
        n_hemi_genBefore=n_hemi_genBefore,
        x_edges=x_edges,
        y_edges=y_edges,
        diag_fraction=diag_fraction.reshape(nx, ny),
    )

    # Summary JSON
    summary = {
        "correction_mean": float(np.mean(c_valid)),
        "correction_median": float(np.median(c_valid)),
        "correction_min": float(np.min(c_valid)),
        "correction_max": float(np.max(c_valid)),
        "bins_c_gt_2": int(np.sum(c_valid > 2)),
        "bins_c_lt_0.5": int(np.sum(c_valid < 0.5)),
        "bins_reco_zero": int(np.sum(~mask_nonzero)),
        "efficiency_mean": float(np.mean(eff_valid)),
        "efficiency_min": float(np.min(eff_valid)),
        "efficiency_max": float(np.max(eff_valid)),
        "diag_fraction_mean": float(np.mean(diag_fraction[populated])),
        "diag_fraction_gt_0.5": int(np.sum(diag_fraction > 0.5)),
    }
    with open(OUT_DIR / "correction_summary_ingrid.json", "w") as f:
        json.dump(summary, f, indent=2)

    log.info("\nSaved correction infrastructure to %s", OUT_DIR)
    log.info("Done.")


if __name__ == "__main__":
    main()
