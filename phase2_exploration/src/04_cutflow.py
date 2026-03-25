#!/usr/bin/env python3
"""Script 04: Cutflow — event counts after each selection cut.

Processes ALL data and MC files (only reads event-level branches, fast).
Session: Hugo
"""

import logging
from pathlib import Path

import awkward as ak
import numpy as np
import uproot
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")


def process_file_cutflow(filepath, tree_name="t"):
    """Compute cutflow for a single file."""
    with uproot.open(filepath) as f:
        tree = f[tree_name]
        # Read only what we need for cutflow
        arrays = tree.arrays(
            ["passesAll", "Thrust", "pwflag", "pmag", "d0", "z0",
             "charge", "TTheta", "TPhi", "px", "py", "pz"],
        )

    n_total = len(arrays)

    # Cut 1: passesAll
    passes = arrays["passesAll"] == True  # noqa: E712
    n_passes = int(ak.sum(passes))

    # Work with selected events
    sel = arrays[passes]

    # Cut 2: Thrust > 0.7
    thrust_mask = sel["Thrust"] > 0.7
    n_thrust = int(ak.sum(thrust_mask))
    sel2 = sel[thrust_mask]

    # Apply track selection within each event
    trk_mask = (
        (sel2["pwflag"] == 0)
        & (sel2["pmag"] > 0.2)
        & (np.abs(sel2["d0"]) < 2.0)
        & (np.abs(sel2["z0"]) < 10.0)
    )

    # Cut 3: N_ch >= 5 after track cuts (already encoded in passesAll, but verify)
    nch = ak.sum(trk_mask, axis=1)
    nch_mask = nch >= 5
    n_nch = int(ak.sum(nch_mask))
    sel3 = sel2[nch_mask]
    trk_mask3 = trk_mask[nch_mask]

    # Cut 4: >= 2 charged tracks in each hemisphere
    ttheta = sel3["TTheta"]
    tphi = sel3["TPhi"]
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)

    dot = sel3["px"] * tx + sel3["py"] * ty + sel3["pz"] * tz
    hemi_plus = trk_mask3 & (dot > 0)
    hemi_minus = trk_mask3 & (dot <= 0)
    n_plus = ak.sum(hemi_plus, axis=1)
    n_minus = ak.sum(hemi_minus, axis=1)
    hemi_mask = (n_plus >= 2) & (n_minus >= 2)
    n_hemi = int(ak.sum(hemi_mask))

    return {
        "total": n_total,
        "passesAll": n_passes,
        "thrust_gt_0p7": n_thrust,
        "nch_ge_5": n_nch,
        "hemi_ge_2": n_hemi,
    }


def main():
    log.info("=" * 60)
    log.info("Script 04: Cutflow")
    log.info("=" * 60)

    # ---- Data cutflow ----
    log.info("\n--- Data Cutflow ---")
    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    data_totals = {"total": 0, "passesAll": 0, "thrust_gt_0p7": 0,
                   "nch_ge_5": 0, "hemi_ge_2": 0}

    for df in data_files:
        log.info("Processing %s ...", df.name)
        counts = process_file_cutflow(df)
        for key in data_totals:
            data_totals[key] += counts[key]
        log.info(
            "  total=%d, passesAll=%d, T>0.7=%d, Nch>=5=%d, hemi>=2=%d",
            counts["total"], counts["passesAll"], counts["thrust_gt_0p7"],
            counts["nch_ge_5"], counts["hemi_ge_2"],
        )

    log.info("\n--- Data Cutflow Summary ---")
    log.info("| Cut | Events | Efficiency (cumulative) | Efficiency (relative) |")
    log.info("|-----|--------|------------------------|----------------------|")
    prev = data_totals["total"]
    for key, label in [
        ("total", "Total"),
        ("passesAll", "passesAll"),
        ("thrust_gt_0p7", "Thrust > 0.7"),
        ("nch_ge_5", "N_ch >= 5"),
        ("hemi_ge_2", "N_hemi >= 2"),
    ]:
        n = data_totals[key]
        cum_eff = n / data_totals["total"] * 100 if data_totals["total"] > 0 else 0
        rel_eff = n / prev * 100 if prev > 0 else 0
        log.info("| %s | %d | %.2f%% | %.2f%% |", label, n, cum_eff, rel_eff)
        prev = n

    # ---- MC cutflow (reco) ----
    log.info("\n--- MC (reco) Cutflow ---")
    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    mc_totals = {"total": 0, "passesAll": 0, "thrust_gt_0p7": 0,
                 "nch_ge_5": 0, "hemi_ge_2": 0}

    for mf in mc_files:
        counts = process_file_cutflow(mf)
        for key in mc_totals:
            mc_totals[key] += counts[key]

    log.info("| Cut | Events | Efficiency (cumulative) | Efficiency (relative) |")
    log.info("|-----|--------|------------------------|----------------------|")
    prev = mc_totals["total"]
    for key, label in [
        ("total", "Total"),
        ("passesAll", "passesAll"),
        ("thrust_gt_0p7", "Thrust > 0.7"),
        ("nch_ge_5", "N_ch >= 5"),
        ("hemi_ge_2", "N_hemi >= 2"),
    ]:
        n = mc_totals[key]
        cum_eff = n / mc_totals["total"] * 100 if mc_totals["total"] > 0 else 0
        rel_eff = n / prev * 100 if prev > 0 else 0
        log.info("| %s | %d | %.2f%% | %.2f%% |", label, n, cum_eff, rel_eff)
        prev = n

    # Data/MC ratio at each cut
    log.info("\n--- Data/MC Efficiency Comparison ---")
    for key in ["passesAll", "thrust_gt_0p7", "nch_ge_5", "hemi_ge_2"]:
        d_eff = data_totals[key] / data_totals["total"] * 100
        m_eff = mc_totals[key] / mc_totals["total"] * 100
        log.info("  %s: Data=%.2f%%, MC=%.2f%%, ratio=%.4f",
                 key, d_eff, m_eff, d_eff / m_eff if m_eff > 0 else 0)

    log.info("\n--- Final yields ---")
    log.info("Data: %d events (%d hemispheres)", data_totals["hemi_ge_2"], 2 * data_totals["hemi_ge_2"])
    log.info("MC: %d events (%d hemispheres)", mc_totals["hemi_ge_2"], 2 * mc_totals["hemi_ge_2"])

    log.info("\nCutflow complete.")


if __name__ == "__main__":
    main()
