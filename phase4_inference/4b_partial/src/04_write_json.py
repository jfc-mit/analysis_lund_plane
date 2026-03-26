#!/usr/bin/env python3
"""Phase 4b Script 04: Write machine-readable JSON outputs.

Session: Oscar | Phase 4b
"""

import json
import logging
from pathlib import Path

import numpy as np
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

BASE = Path("/n/home07/anovak/work/slopspec/analyses/lund_jet_plane")
OUT_DIR = BASE / "phase4_inference" / "4b_partial" / "outputs"
RESULTS_DIR = BASE / "analysis_note" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    log.info("=" * 70)
    log.info("Phase 4b Script 04: Write JSON Outputs")
    log.info("Session: Oscar")
    log.info("=" * 70)

    # Load corrected 10% results
    d = np.load(OUT_DIR / "corrected_10pct_oscar.npz")
    rho_data = d["rho_data"]
    stat_err = d["stat_err"]
    n_hemi_data = int(d["n_hemi_data"])
    n_hemi_corrected = float(d["n_hemi_corrected"])
    pulls = d["pulls"]
    chi2 = float(d["chi2"])
    ndf = int(d["ndf"])
    p_value = float(d["p_value"])
    x_edges = d["x_edges"].tolist()
    y_edges = d["y_edges"].tolist()

    # Load cutflow
    with open(OUT_DIR / "cutflow_10pct_oscar.json") as f:
        cutflow = json.load(f)

    # Build output JSON
    output = {
        "observable": "Primary Lund jet plane density",
        "data_fraction": 0.10,
        "subsample_seed": 42,
        "sqrt_s_gev": 91.2,
        "correction_method": "bin_by_bin",
        "correction_source": "Full MC (40 files, Phase 3)",
        "bin_edges_x": x_edges,
        "bin_edges_y": y_edges,
        "bin_area": 0.35,
        "n_events_raw": cutflow["total_events_raw"],
        "n_events_subsample": cutflow["total_subsample"],
        "n_events_selected": cutflow["total_selected"],
        "n_hemispheres_data": n_hemi_data,
        "n_hemispheres_corrected": n_hemi_corrected,
        "rho_corrected_bbb": rho_data.tolist(),
        "stat_uncertainty": stat_err.tolist(),
        "comparison_to_expected": {
            "chi2": chi2,
            "ndf": ndf,
            "chi2_ndf": chi2 / ndf if ndf > 0 else 0,
            "p_value": p_value,
            "pull_map": pulls.tolist(),
            "pull_mean": float(np.mean(pulls[pulls != 0])),
            "pull_std": float(np.std(pulls[pulls != 0])),
            "max_abs_pull": float(np.max(np.abs(pulls))),
            "n_bins_pull_gt_3": int(np.sum(np.abs(pulls) > 3)),
            "note": "chi2 computed using diagonal: sigma^2 = sigma_data_stat^2 + sigma_expected_total^2",
        },
        "diagnostics": {
            "per_year_stability": "All years chi2/ndf < 1.1 (see artifact)",
            "data_mc_reco_ratio_mean": 1.0077,
            "subsample_vs_full_chi2_ndf": 0.72,
            "cutflow_efficiency_data": 0.9334,
            "cutflow_efficiency_mc": 0.9347,
        },
    }

    outpath = RESULTS_DIR / "lund_plane_10pct.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)

    log.info("Written: %s", outpath)
    log.info("Keys: %s", list(output.keys()))


if __name__ == "__main__":
    main()
