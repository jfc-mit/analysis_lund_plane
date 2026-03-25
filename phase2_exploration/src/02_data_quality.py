#!/usr/bin/env python3
"""Script 02: Data quality checks.

Checks for pathologies, outliers, unphysical values in data and MC.
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
N_EVT = 5000


def check_branch_quality(tree, branch_name, n_events, label=""):
    """Check a branch for pathologies."""
    arr = tree[branch_name].array(entry_stop=n_events)
    is_jagged = arr.ndim > 1
    if is_jagged:
        flat = ak.flatten(arr)
    else:
        flat = arr
    vals = np.asarray(flat, dtype=np.float64)

    issues = []
    n_nan = int(np.sum(np.isnan(vals)))
    n_inf = int(np.sum(np.isinf(vals)))
    if n_nan > 0:
        issues.append(f"{n_nan} NaN values")
    if n_inf > 0:
        issues.append(f"{n_inf} Inf values")

    result = {
        "branch": branch_name,
        "label": label,
        "n_entries": len(vals),
        "min": float(np.nanmin(vals)) if len(vals) > 0 else None,
        "max": float(np.nanmax(vals)) if len(vals) > 0 else None,
        "mean": float(np.nanmean(vals)) if len(vals) > 0 else None,
        "std": float(np.nanstd(vals)) if len(vals) > 0 else None,
        "n_nan": n_nan,
        "n_inf": n_inf,
        "n_zero": int(np.sum(vals == 0)),
        "is_jagged": is_jagged,
        "issues": issues,
    }
    return result


def main():
    log.info("=" * 60)
    log.info("Script 02: Data Quality Checks")
    log.info("=" * 60)

    # ---- Data quality ----
    data_file = sorted(DATA_DIR.glob("LEP1Data*.root"))[0]
    log.info("Checking data file: %s (%d events)", data_file.name, N_EVT)

    particle_branches = [
        "px", "py", "pz", "pt", "pmag", "eta", "theta", "phi",
        "mass", "charge", "d0", "z0", "pwflag",
    ]
    event_branches = [
        "Thrust", "Thrust_charged", "Sphericity", "Aplanarity",
        "nChargedHadrons", "nChargedHadrons_GT0p4Thrust",
        "passesAll", "TTheta", "TPhi",
    ]

    with uproot.open(data_file) as f:
        tree = f["t"]
        available = tree.keys()

        log.info("\n--- Particle-level branches (data) ---")
        for b in particle_branches:
            if b in available:
                res = check_branch_quality(tree, b, N_EVT, "data")
                status = "OK" if not res["issues"] else " | ".join(res["issues"])
                log.info(
                    "  %s: min=%.4g, max=%.4g, mean=%.4g, zeros=%d, %s",
                    b, res["min"], res["max"], res["mean"], res["n_zero"], status,
                )

        log.info("\n--- Event-level branches (data) ---")
        for b in event_branches:
            if b in available:
                res = check_branch_quality(tree, b, N_EVT, "data")
                status = "OK" if not res["issues"] else " | ".join(res["issues"])
                log.info(
                    "  %s: min=%.4g, max=%.4g, mean=%.4g, %s",
                    b, res["min"], res["max"], res["mean"], status,
                )

        # Check for charged track subset specifically
        log.info("\n--- Charged track quality (pwflag==0) ---")
        pwflag = tree["pwflag"].array(entry_stop=N_EVT)
        pmag = tree["pmag"].array(entry_stop=N_EVT)
        d0 = tree["d0"].array(entry_stop=N_EVT)
        z0 = tree["z0"].array(entry_stop=N_EVT)
        theta = tree["theta"].array(entry_stop=N_EVT)

        mask_charged = (pwflag == 0)
        pmag_ch = ak.flatten(pmag[mask_charged])
        d0_ch = ak.flatten(d0[mask_charged])
        z0_ch = ak.flatten(z0[mask_charged])
        theta_ch = ak.flatten(theta[mask_charged])

        log.info("  Charged tracks (pwflag==0): %d total in %d events", len(pmag_ch), N_EVT)
        log.info(
            "  pmag: min=%.4f, max=%.4f, mean=%.4f",
            float(ak.min(pmag_ch)), float(ak.max(pmag_ch)), float(ak.mean(pmag_ch)),
        )
        log.info(
            "  d0: min=%.4f, max=%.4f, median=%.4f, RMS=%.4f",
            float(ak.min(d0_ch)), float(ak.max(d0_ch)),
            float(np.median(np.asarray(d0_ch))),
            float(np.sqrt(np.mean(np.asarray(d0_ch)**2))),
        )
        log.info(
            "  z0: min=%.4f, max=%.4f, RMS=%.4f",
            float(ak.min(z0_ch)), float(ak.max(z0_ch)),
            float(np.sqrt(np.mean(np.asarray(z0_ch)**2))),
        )
        log.info(
            "  theta: min=%.4f, max=%.4f (expect [0, pi])",
            float(ak.min(theta_ch)), float(ak.max(theta_ch)),
        )

        # Check for negative momenta
        n_neg_p = int(ak.sum(pmag_ch < 0))
        log.info("  Negative pmag: %d", n_neg_p)

        # Check d0 distribution for TPC-only vs TPC+ITC+VDET
        d0_np = np.asarray(d0_ch)
        d0_abs = np.abs(d0_np)
        log.info("\n--- d0 resolution diagnostic (charged tracks only) ---")
        log.info("  |d0| percentiles:")
        for pct in [50, 68, 90, 95, 99]:
            log.info("    %d%%: %.4f cm", pct, np.percentile(d0_abs, pct))
        log.info(
            "  Interpretation: median |d0| ~ %.0f um",
            np.median(d0_abs) * 10000,  # cm -> um
        )
        sigma_d0 = np.percentile(d0_abs, 68)
        log.info("  sigma_d0 (68%% percentile) ~ %.0f um", sigma_d0 * 10000)
        if sigma_d0 * 10000 < 50:
            log.info("  -> Consistent with TPC+ITC+VDET combined tracking (sigma_d0 ~ 25 um)")
        elif sigma_d0 * 10000 < 200:
            log.info("  -> Intermediate: may include ITC but not VDET")
        else:
            log.info("  -> Consistent with TPC-only tracking (sigma_d0 ~ 150 um)")

    # ---- MC quality ----
    mc_file = sorted(MC_DIR.glob("LEP1MC*.root"))[0]
    log.info("\n--- MC reco quality ---")
    with uproot.open(mc_file) as f:
        tree = f["t"]
        for b in ["pmag", "theta", "d0", "z0", "Thrust"]:
            if b in tree.keys():
                res = check_branch_quality(tree, b, N_EVT, "mc_reco")
                status = "OK" if not res["issues"] else " | ".join(res["issues"])
                log.info(
                    "  %s: min=%.4g, max=%.4g, mean=%.4g, %s",
                    b, res["min"], res["max"], res["mean"], status,
                )

        # MC gen-level quality
        log.info("\n--- MC gen quality (tgen) ---")
        tgen = f["tgen"]
        gen_branches = ["pmag", "theta", "phi", "Thrust", "pwflag"]
        for b in gen_branches:
            if b in tgen.keys():
                res = check_branch_quality(tgen, b, N_EVT, "mc_gen")
                status = "OK" if not res["issues"] else " | ".join(res["issues"])
                log.info(
                    "  %s: min=%.4g, max=%.4g, mean=%.4g, %s",
                    b, res["min"], res["max"], res["mean"], status,
                )

        # Gen-level pwflag values
        pwflag_gen = tgen["pwflag"].array(entry_stop=N_EVT)
        flat_pf = np.asarray(ak.flatten(pwflag_gen))
        unique_pf = np.unique(flat_pf)
        log.info("  Gen pwflag unique values: %s", unique_pf.tolist())
        for val in unique_pf:
            n = int(np.sum(flat_pf == val))
            log.info("    pwflag=%d: %d tracks (%.1f%%)", val, n, 100 * n / len(flat_pf))

    # ---- Year-to-year consistency ----
    log.info("\n--- Year-to-year consistency ---")
    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    for df in data_files:
        with uproot.open(df) as f:
            tree = f["t"]
            thrust = np.asarray(tree["Thrust"].array(entry_stop=2000))
            nch = np.asarray(tree["nChargedHadrons"].array(entry_stop=2000))
            log.info(
                "  %s: <Thrust>=%.4f, <N_ch>=%.2f",
                df.name, np.mean(thrust), np.mean(nch),
            )

    log.info("\nData quality checks complete.")


if __name__ == "__main__":
    main()
