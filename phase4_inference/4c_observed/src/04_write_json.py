#!/usr/bin/env python3
"""Phase 4c Script 04: Write machine-readable JSON for the primary result.

Writes lund_plane_full.json to analysis_note/results/ with the corrected
Lund jet plane density, statistical uncertainties, comparison metrics,
and diagnostics.

Session: Emeric | Phase 4c
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
OUT_DIR = BASE / "phase4_inference" / "4c_observed" / "outputs"
RESULTS_DIR = BASE / "analysis_note" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def main():
    log.info("=" * 70)
    log.info("Phase 4c Script 04: Write JSON Outputs")
    log.info("Session: Emeric")
    log.info("=" * 70)

    # Load corrected full results
    d = np.load(OUT_DIR / "corrected_full_emeric.npz")
    rho_data = d["rho_data"]
    stat_err = d["stat_err"]
    corrected_counts = d["corrected_counts"]
    n_hemi_data = int(d["n_hemi_data"])
    n_hemi_corrected = float(d["n_hemi_corrected"])
    pulls = d["pulls"]
    chi2_diag = float(d["chi2_diag"])
    chi2_cov = float(d["chi2_cov"])
    ndf = int(d["ndf"])
    p_value_diag = float(d["p_value_diag"])
    p_value_cov = float(d["p_value_cov"])
    x_edges = d["x_edges"].tolist()
    y_edges = d["y_edges"].tolist()

    # Load cutflow
    with open(OUT_DIR / "cutflow_full_emeric.json") as f:
        cutflow = json.load(f)

    # Load diagnostics
    with open(OUT_DIR / "diagnostics_full_emeric.json") as f:
        diagnostics = json.load(f)

    # Compute bin area and integral
    dx = np.diff(np.array(x_edges))
    dy = np.diff(np.array(y_edges))
    bin_area = np.outer(dx, dy)
    integral = float(np.sum(rho_data * bin_area))

    # Populated bins
    populated = rho_data > 0
    n_populated = int(np.sum(populated))

    # Build output JSON
    output = {
        "observable": "Primary Lund jet plane density",
        "data_fraction": 1.0,
        "sqrt_s_gev": 91.2,
        "experiment": "ALEPH",
        "correction_method": "bin_by_bin",
        "correction_source": "Full MC (40 files, Phase 3)",
        "bin_edges_x": x_edges,
        "bin_edges_y": y_edges,
        "bin_labels_x": "ln(1/Delta_theta)",
        "bin_labels_y": "ln(k_T/GeV)",
        "n_events_raw": cutflow["total_events_raw"],
        "n_events_selected": cutflow["total_selected"],
        "n_events_hemi_cut": cutflow["total_hemi_cut"],
        "n_hemispheres_data": n_hemi_data,
        "n_hemispheres_corrected": n_hemi_corrected,
        "n_populated_bins": n_populated,
        "integral_rho_dA": integral,
        "rho_corrected_bbb": rho_data.tolist(),
        "stat_uncertainty": stat_err.tolist(),
        "corrected_counts": corrected_counts.tolist(),
        "comparison_to_expected": {
            "chi2_diag": chi2_diag,
            "chi2_cov": chi2_cov,
            "ndf": ndf,
            "chi2_ndf_diag": chi2_diag / ndf if ndf > 0 else 0,
            "chi2_ndf_cov": chi2_cov / ndf if ndf > 0 else 0,
            "p_value_diag": p_value_diag,
            "p_value_cov": p_value_cov,
            "pull_map": pulls.tolist(),
            "pull_mean": float(np.mean(pulls[pulls != 0])),
            "pull_std": float(np.std(pulls[pulls != 0])),
            "max_abs_pull": float(np.max(np.abs(pulls))),
            "n_bins_pull_gt_3": int(np.sum(np.abs(pulls) > 3)),
            "note": (
                "chi2_diag uses diagonal: sigma^2 = sigma_data_stat^2 + sigma_expected_total^2; "
                "chi2_cov uses full stat+syst covariance matrix"
            ),
        },
        "diagnostics": diagnostics,
        "cutflow": cutflow,
    }

    outpath = RESULTS_DIR / "lund_plane_full.json"
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)

    log.info("Written: %s", outpath)
    log.info("Keys: %s", list(output.keys()))
    log.info("Integral rho * dA = %.3f", integral)
    log.info("N populated bins: %d / 100", n_populated)


if __name__ == "__main__":
    main()
