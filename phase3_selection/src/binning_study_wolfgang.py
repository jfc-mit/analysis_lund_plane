#!/usr/bin/env python3
"""Binning Investigation: Can we go finer than 10x10?

Issue #12: Current 10x10 has 42 empty bins (only 58 populated).
The core has very healthy stats (>10k entries per bin at reco level).
Investigate 15x15 and 20x20 binning — bin populations and migration fractions.

Session: Wolfgang (fix agent) | Binning study
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
OUT_DIR = BASE / "phase3_selection" / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

AN_FIG_DIR = BASE / "analysis_note" / "figures"


def save_fig(fig, name):
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved %s", name)


def rebin_histogram(h2d_orig, x_edges_orig, y_edges_orig, x_edges_new, y_edges_new):
    """Rebin a 2D histogram from original edges to new edges.

    Assumes uniform bins in the original. Projects via 2D digitize
    from the original bin centers.
    """
    nx_orig = len(x_edges_orig) - 1
    ny_orig = len(y_edges_orig) - 1
    nx_new = len(x_edges_new) - 1
    ny_new = len(y_edges_new) - 1

    h2d_new = np.zeros((nx_new, ny_new))

    # Map original bin centers to new bin indices
    x_centers = 0.5 * (x_edges_orig[:-1] + x_edges_orig[1:])
    y_centers = 0.5 * (y_edges_orig[:-1] + y_edges_orig[1:])

    for i in range(nx_orig):
        ix_new = np.searchsorted(x_edges_new, x_centers[i]) - 1
        if ix_new < 0 or ix_new >= nx_new:
            continue
        for j in range(ny_orig):
            iy_new = np.searchsorted(y_edges_new, y_centers[j]) - 1
            if iy_new < 0 or iy_new >= ny_new:
                continue
            h2d_new[ix_new, iy_new] += h2d_orig[i, j]

    return h2d_new


def main():
    log.info("=" * 70)
    log.info("Binning Investigation (Issue #12)")
    log.info("Session: Wolfgang")
    log.info("=" * 70)

    # We need the raw data histograms. Since Phase 3 used a specific binning
    # to fill the histograms, we can't truly rebin from histograms — we would
    # need to re-process from the raw data. However, we can use the existing
    # fine-grained data to estimate.
    #
    # For a proper study, we load the raw Lund coordinates from the Phase 3
    # processing and re-histogram at finer binning.
    #
    # But the Phase 3 output only has h2d (already histogrammed at 10x10).
    # We can still do a meaningful study:
    # 1. Load the 10x10 histograms
    # 2. Estimate what the bin populations would be at finer binning
    #    (by splitting the counts proportionally)
    # 3. Compute approximate migration fractions
    #
    # For a true rebin study we would need the per-event coordinates.
    # Instead, let's check if Phase 3 stored any finer-grained data.

    # Load existing 10x10 data
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

    nx = len(x_edges) - 1
    ny = len(y_edges) - 1

    log.info("\n=== Current 10x10 binning ===")
    log.info("x_edges: [%.1f, %.1f] with %d bins", x_edges[0], x_edges[-1], nx)
    log.info("y_edges: [%.1f, %.1f] with %d bins", y_edges[0], y_edges[-1], ny)
    log.info("Total bins: %d", nx * ny)
    log.info("Populated (data > 0): %d", np.sum(h2d_data > 0))
    log.info("Populated (reco > 0): %d", np.sum(h2d_reco > 0))

    # Bin population statistics
    populated = h2d_data > 0
    log.info("\nData bin populations (populated bins):")
    log.info("  Min: %.0f", np.min(h2d_data[populated]))
    log.info("  Max: %.0f", np.max(h2d_data[populated]))
    log.info("  Mean: %.0f", np.mean(h2d_data[populated]))
    log.info("  Median: %.0f", np.median(h2d_data[populated]))

    pop_reco = h2d_reco > 0
    log.info("\nMC reco bin populations (populated bins):")
    log.info("  Min: %.0f", np.min(h2d_reco[pop_reco]))
    log.info("  Max: %.0f", np.max(h2d_reco[pop_reco]))
    log.info("  Mean: %.0f", np.mean(h2d_reco[pop_reco]))
    log.info("  Median: %.0f", np.median(h2d_reco[pop_reco]))

    # Core region: 1 < ln(1/dtheta) < 4, -1 < ln(kT) < 3
    core_x = (x_edges[:-1] >= 1.0) & (x_edges[1:] <= 4.0)
    core_y = (y_edges[:-1] >= -1.0) & (y_edges[1:] <= 3.0)
    core_mask = np.outer(core_x, core_y)

    log.info("\n=== Core region (1 < ln(1/dtheta) < 4, -1 < ln(kT) < 3) ===")
    n_core = np.sum(core_mask)
    log.info("Core bins: %d / %d", n_core, nx * ny)
    log.info("Data in core: %.0f / %.0f (%.1f%%)",
             np.sum(h2d_data[core_mask]), np.sum(h2d_data),
             100 * np.sum(h2d_data[core_mask]) / np.sum(h2d_data))
    log.info("Core bin populations (data):")
    if np.any(core_mask & (h2d_data > 0)):
        core_data = h2d_data[core_mask & (h2d_data > 0)]
        log.info("  Min: %.0f", np.min(core_data))
        log.info("  Mean: %.0f", np.mean(core_data))
        log.info("  Median: %.0f", np.median(core_data))

    # Estimate populations at finer binning (assuming uniform distribution within bins)
    log.info("\n=== Estimated populations at finer binning ===")
    for n_bins_new, label in [(15, "15x15"), (20, "20x20")]:
        # If we go from 10 to N bins in each direction,
        # each original bin gets split into (N/10)^2 sub-bins on average
        # (or some integer subdivision)
        factor = n_bins_new / 10.0
        # Average population per sub-bin
        avg_pop_data = np.mean(h2d_data[populated]) / factor**2
        avg_pop_reco = np.mean(h2d_reco[pop_reco]) / factor**2

        # Core region
        if np.any(core_mask & (h2d_data > 0)):
            avg_core_data = np.mean(h2d_data[core_mask & (h2d_data > 0)]) / factor**2
            min_core_data = np.min(h2d_data[core_mask & (h2d_data > 0)]) / factor**2
        else:
            avg_core_data = 0
            min_core_data = 0

        # Estimated number of populated bins
        # At finer binning, same kinematic region is covered, but empty area stays empty
        # Populated fraction stays approximately the same
        pop_frac = np.sum(populated) / (nx * ny)
        est_populated = int(n_bins_new**2 * pop_frac)

        log.info("\n%s binning:", label)
        log.info("  Total bins: %d", n_bins_new**2)
        log.info("  Estimated populated: ~%d", est_populated)
        log.info("  Avg data entries per bin (all populated): ~%.0f", avg_pop_data)
        log.info("  Avg reco entries per bin (all populated): ~%.0f", avg_pop_reco)
        log.info("  Core avg data entries: ~%.0f", avg_core_data)
        log.info("  Core min data entries: ~%.0f", min_core_data)

        # Migration fraction estimate: finer bins -> higher migration
        # Original diagonal fraction from Phase 3:
        corr_d = np.load(OUT_DIR / "correction_ingrid.npz")
        diag_frac = corr_d["diag_fraction"]
        avg_diag = np.mean(diag_frac[diag_frac > 0])
        # Estimate: migration fraction ~ 1 - diag_frac
        # At finer binning, migration increases roughly as (bin_width_ratio)
        mig_est = 1.0 - avg_diag * (10.0 / n_bins_new)
        mig_est = min(mig_est, 0.99)
        log.info("  Estimated mean migration fraction: ~%.0f%%", 100 * mig_est)

        # Minimum population threshold check
        threshold = 100  # minimum for meaningful correction
        pct_above = 100 * avg_core_data / threshold if threshold > 0 else 0
        log.info("  Core avg / 100-entry threshold: %.0f%%", pct_above)
        if avg_core_data >= threshold:
            log.info("  -> VIABLE: Core bins have sufficient statistics")
        elif avg_core_data >= 50:
            log.info("  -> MARGINAL: Core bins have borderline statistics")
        else:
            log.info("  -> NOT VIABLE: Core bins have insufficient statistics")

    # Summary and recommendation
    log.info("\n" + "=" * 70)
    log.info("BINNING INVESTIGATION SUMMARY")
    log.info("=" * 70)

    total_data = np.sum(h2d_data)
    total_reco = np.sum(h2d_reco)
    log.info("Total data splittings: %.0f", total_data)
    log.info("Total MC reco splittings: %.0f", total_reco)
    log.info("Total data hemispheres: %.0f", n_hemi_data)

    log.info("\nCurrent 10x10:")
    log.info("  58 populated bins, avg %.0f data entries/bin",
             np.mean(h2d_data[populated]))
    log.info("  Core avg: %.0f data entries/bin",
             np.mean(h2d_data[core_mask & (h2d_data > 0)]))
    log.info("  Mean diagonal fraction: %.2f", np.mean(diag_frac[diag_frac > 0]))

    log.info("\n15x15 estimate:")
    log.info("  ~131 populated bins, avg ~%.0f data entries/bin",
             np.mean(h2d_data[populated]) / 2.25)
    log.info("  Core avg: ~%.0f data entries/bin",
             np.mean(h2d_data[core_mask & (h2d_data > 0)]) / 2.25)

    log.info("\n20x20 estimate:")
    log.info("  ~232 populated bins, avg ~%.0f data entries/bin",
             np.mean(h2d_data[populated]) / 4.0)
    log.info("  Core avg: ~%.0f data entries/bin",
             np.mean(h2d_data[core_mask & (h2d_data > 0)]) / 4.0)

    log.info("\nRECOMMENDATION:")
    avg_core_10 = np.mean(h2d_data[core_mask & (h2d_data > 0)])
    if avg_core_10 / 2.25 >= 500:
        log.info("  15x15 is VIABLE in the core: avg ~%.0f entries/bin > 500 threshold",
                 avg_core_10 / 2.25)
        log.info("  This would increase the number of measured bins by ~2.5x")
        log.info("  while maintaining healthy statistics in the core.")
    else:
        log.info("  15x15 is MARGINAL: avg ~%.0f entries/bin",
                 avg_core_10 / 2.25)

    if avg_core_10 / 4.0 >= 500:
        log.info("  20x20 is VIABLE in the core: avg ~%.0f entries/bin > 500 threshold",
                 avg_core_10 / 4.0)
    elif avg_core_10 / 4.0 >= 100:
        log.info("  20x20 is MARGINAL: avg ~%.0f entries/bin (above 100 but below 500)",
                 avg_core_10 / 4.0)
        log.info("  Migration fractions would increase significantly.")
    else:
        log.info("  20x20 is NOT VIABLE: avg ~%.0f entries/bin < 100",
                 avg_core_10 / 4.0)

    log.info("\nIMPORTANT CAVEAT: These are estimates from the 10x10 histograms.")
    log.info("A proper study requires re-histogramming the raw Lund coordinates")
    log.info("at the finer binning, which involves reprocessing Phase 3 data.")
    log.info("The migration fraction estimates are particularly crude.")
    log.info("If finer binning is pursued, Phase 3 should be re-run with the")
    log.info("new binning to produce proper bin population and migration maps.")

    # Save summary as JSON
    summary = {
        "current_10x10": {
            "total_bins": 100,
            "populated_data": int(np.sum(populated)),
            "populated_reco": int(np.sum(pop_reco)),
            "total_data_splittings": int(total_data),
            "total_reco_splittings": int(total_reco),
            "avg_data_per_bin": float(np.mean(h2d_data[populated])),
            "core_avg_data_per_bin": float(np.mean(h2d_data[core_mask & (h2d_data > 0)])),
            "mean_diag_fraction": float(np.mean(diag_frac[diag_frac > 0])),
        },
        "estimate_15x15": {
            "total_bins": 225,
            "est_populated": int(225 * pop_frac),
            "est_avg_data_per_bin": float(np.mean(h2d_data[populated]) / 2.25),
            "est_core_avg": float(avg_core_10 / 2.25),
            "viable_core": bool(avg_core_10 / 2.25 >= 500),
        },
        "estimate_20x20": {
            "total_bins": 400,
            "est_populated": int(400 * pop_frac),
            "est_avg_data_per_bin": float(np.mean(h2d_data[populated]) / 4.0),
            "est_core_avg": float(avg_core_10 / 4.0),
            "viable_core": bool(avg_core_10 / 4.0 >= 100),
        },
        "recommendation": "15x15 if core avg >= 500; requires Phase 3 reprocessing for proper study",
    }

    with open(OUT_DIR / "binning_study_wolfgang.json", "w") as f:
        json.dump(summary, f, indent=2)
    log.info("\nSaved: binning_study_wolfgang.json")


if __name__ == "__main__":
    main()
