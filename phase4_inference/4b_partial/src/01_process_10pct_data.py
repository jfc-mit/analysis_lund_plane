#!/usr/bin/env python3
"""Phase 4b Script 01: Process 10% of real data with fixed seed.

Applies the same event selection and Lund plane construction as Phase 3,
but on a 10% fixed-seed subsample of each data file. Saves per-file
histograms for per-year stability checks.

Session: Oscar | Phase 4b
"""

import json
import logging
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import awkward as ak
import fastjet
import numpy as np
import uproot
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")

# Binning (must match Phase 3 exactly)
X_EDGES = np.linspace(0, 5, 11)  # 10 bins, ln(1/Delta_theta)
Y_EDGES = np.linspace(-3, 4, 11)  # 10 bins, ln(k_T/GeV)

M_PI = 0.13957  # Pion mass in GeV
SEED = 42
FRACTION = 0.10


def apply_selection(arrays):
    """Apply event and track selection. Returns selected arrays, track mask."""
    evt_mask = (arrays["passesAll"] == True) & (arrays["Thrust"] > 0.7)  # noqa: E712
    sel = arrays[evt_mask]

    trk_mask = (
        (sel["pwflag"] == 0)
        & (sel["pmag"] > 0.2)
        & (np.abs(sel["d0"]) < 2.0)
        & (np.abs(sel["z0"]) < 10.0)
    )

    nch = ak.sum(trk_mask, axis=1)
    evt_mask2 = nch >= 5
    sel = sel[evt_mask2]
    trk_mask = trk_mask[evt_mask2]

    return sel, trk_mask


def split_hemispheres(sel, trk_mask):
    """Split events into thrust hemispheres."""
    ttheta = sel["TTheta"]
    tphi = sel["TPhi"]
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)

    dot = sel["px"] * tx + sel["py"] * ty + sel["pz"] * tz
    hemi_plus = trk_mask & (dot > 0)
    hemi_minus = trk_mask & (dot <= 0)

    n_plus = ak.sum(hemi_plus, axis=1)
    n_minus = ak.sum(hemi_minus, axis=1)
    good = (n_plus >= 2) & (n_minus >= 2)

    return hemi_plus[good], hemi_minus[good], good


def decluster_primary_chain(px, py, pz, pmag):
    """Cluster one hemisphere with C/A and extract primary Lund splittings."""
    n = len(px)
    if n < 2:
        return np.empty(0), np.empty(0)

    energy = np.sqrt(pmag**2 + M_PI**2)
    particles = []
    for i in range(n):
        particles.append(
            fastjet.PseudoJet(float(px[i]), float(py[i]), float(pz[i]), float(energy[i]))
        )

    jet_def = fastjet.JetDefinition(fastjet.ee_genkt_algorithm, 999.0, 0.0)
    cs = fastjet.ClusterSequence(particles, jet_def)
    jets = cs.inclusive_jets()

    if len(jets) == 0:
        return np.empty(0), np.empty(0)

    lx_list = []
    ly_list = []
    current = jets[0]

    while True:
        p1 = fastjet.PseudoJet()
        p2 = fastjet.PseudoJet()
        if not current.has_parents(p1, p2):
            break

        pt1 = np.sqrt(p1.px() ** 2 + p1.py() ** 2)
        pt2 = np.sqrt(p2.px() ** 2 + p2.py() ** 2)
        if pt1 >= pt2:
            harder, softer = p1, p2
        else:
            harder, softer = p2, p1

        vec1 = np.array([harder.px(), harder.py(), harder.pz()])
        vec2 = np.array([softer.px(), softer.py(), softer.pz()])
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            break

        cos_theta = np.clip(np.dot(vec1, vec2) / (norm1 * norm2), -1.0, 1.0)
        delta_theta = np.arccos(cos_theta)

        if delta_theta < 1e-10:
            break

        kt = norm2 * np.sin(delta_theta)
        if kt > 0:
            lx_list.append(np.log(1.0 / delta_theta))
            ly_list.append(np.log(kt))

        current = harder

    if len(lx_list) == 0:
        return np.empty(0), np.empty(0)
    return np.array(lx_list), np.array(ly_list)


def process_events_lund(sel, hemi_plus, hemi_minus):
    """Process selected events: decluster both hemispheres, collect Lund splittings."""
    h2d = np.zeros((len(X_EDGES) - 1, len(Y_EDGES) - 1), dtype=np.float64)
    n_hemispheres = 0
    n_splittings = 0

    n_events = len(sel)
    for i in range(n_events):
        for hemi_mask in [hemi_plus, hemi_minus]:
            mask = hemi_mask[i]
            px_arr = np.asarray(sel["px"][i][mask], dtype=np.float64)
            py_arr = np.asarray(sel["py"][i][mask], dtype=np.float64)
            pz_arr = np.asarray(sel["pz"][i][mask], dtype=np.float64)
            pmag_arr = np.asarray(sel["pmag"][i][mask], dtype=np.float64)

            lx, ly = decluster_primary_chain(px_arr, py_arr, pz_arr, pmag_arr)
            if len(lx) > 0:
                h, _, _ = np.histogram2d(lx, ly, bins=[X_EDGES, Y_EDGES])
                h2d += h
                n_splittings += len(lx)
            n_hemispheres += 1

    return h2d, n_hemispheres, n_splittings


def process_data_file_10pct(filepath):
    """Process a single data file with 10% subsampling.

    Uses a fixed seed per file: seed = SEED + hash(filename) to ensure
    reproducibility while giving each file a different random sequence.
    The global SEED=42 ensures the overall subsample is deterministic.
    """
    log.info("DATA (10%%): %s", filepath.name)
    t0 = time.time()

    branches = [
        "px", "py", "pz", "pmag", "d0", "z0", "pwflag",
        "Thrust", "TTheta", "TPhi", "passesAll",
    ]

    with uproot.open(filepath) as f:
        arrays = f["t"].arrays(branches)

    n_total = len(arrays)

    # 10% subsampling with fixed seed
    # Use SEED directly for all files -- same global seed, applied per file
    # Subsample BEFORE selection (this is raw event subsampling)
    rng = np.random.default_rng(SEED)
    n_select = int(n_total * FRACTION)
    indices = rng.choice(n_total, size=n_select, replace=False)
    indices.sort()
    arrays = arrays[indices]
    n_after_subsample = len(arrays)

    sel, trk_mask = apply_selection(arrays)
    n_after_sel = len(sel)

    hemi_plus, hemi_minus, good = split_hemispheres(sel, trk_mask)
    sel = sel[good]
    n_after_hemi = len(sel)

    h2d, n_hemi, n_split = process_events_lund(sel, hemi_plus, hemi_minus)

    dt = time.time() - t0
    log.info(
        "  %s: %d total -> %d subsample -> %d selected -> %d hemi-cut "
        "-> %d hemi, %d splits (%.1fs)",
        filepath.name, n_total, n_after_subsample, n_after_sel,
        n_after_hemi, n_hemi, n_split, dt,
    )

    cutflow = {
        "file": filepath.name,
        "total": int(n_total),
        "subsample_10pct": int(n_after_subsample),
        "after_selection": int(n_after_sel),
        "after_hemi_cut": int(n_after_hemi),
        "hemispheres": int(n_hemi),
        "splittings": int(n_split),
    }
    return h2d, n_hemi, n_split, cutflow


def main():
    log.info("=" * 70)
    log.info("Phase 4b Script 01: Process 10%% of Real Data")
    log.info("Session: Oscar | Seed: %d | Fraction: %.0f%%", SEED, FRACTION * 100)
    log.info("=" * 70)

    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    log.info("Found %d data files", len(data_files))

    # Process data files in parallel
    n_workers = 6
    data_h2d = np.zeros((len(X_EDGES) - 1, len(Y_EDGES) - 1), dtype=np.float64)
    data_n_hemi = 0
    data_n_split = 0
    data_cutflows = []
    per_file_h2d = {}
    per_file_n_hemi = {}

    t0 = time.time()
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_data_file_10pct, f): f for f in data_files}
        for future in as_completed(futures):
            f = futures[future]
            h2d, n_h, n_s, cf = future.result()
            data_h2d += h2d
            data_n_hemi += n_h
            data_n_split += n_s
            data_cutflows.append(cf)
            per_file_h2d[f.name] = h2d.copy()
            per_file_n_hemi[f.name] = n_h

    dt = time.time() - t0
    log.info("\nTotal processing time: %.1fs", dt)
    log.info("10%% Data: %d hemispheres, %d splittings (%.2f splits/hemi)",
             data_n_hemi, data_n_split, data_n_split / max(data_n_hemi, 1))

    # Save combined 10% result
    np.savez(
        OUT_DIR / "data_10pct_lund_oscar.npz",
        h2d=data_h2d,
        n_hemispheres=data_n_hemi,
        n_splittings=data_n_split,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
        seed=SEED,
        fraction=FRACTION,
    )

    # Save per-file histograms for per-year stability
    file_names = sorted(per_file_h2d.keys())
    per_file_arrays = np.stack([per_file_h2d[fn] for fn in file_names])
    per_file_hemi = np.array([per_file_n_hemi[fn] for fn in file_names])
    np.savez(
        OUT_DIR / "data_10pct_per_file_oscar.npz",
        h2d_per_file=per_file_arrays,
        n_hemi_per_file=per_file_hemi,
        file_names=np.array(file_names),
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
    )

    # Save cutflow
    cutflow_summary = {
        "seed": SEED,
        "fraction": FRACTION,
        "per_file": sorted(data_cutflows, key=lambda c: c["file"]),
        "total_events_raw": sum(c["total"] for c in data_cutflows),
        "total_subsample": sum(c["subsample_10pct"] for c in data_cutflows),
        "total_selected": sum(c["after_selection"] for c in data_cutflows),
        "total_hemi_cut": sum(c["after_hemi_cut"] for c in data_cutflows),
        "total_hemispheres": int(data_n_hemi),
        "total_splittings": int(data_n_split),
    }

    with open(OUT_DIR / "cutflow_10pct_oscar.json", "w") as f:
        json.dump(cutflow_summary, f, indent=2)

    log.info("\nAll results saved to %s", OUT_DIR)

    # Print summary table
    log.info("\n=== 10%% DATA CUTFLOW ===")
    log.info("%-50s %10s %10s %10s %10s %10s",
             "File", "Total", "10%", "Selected", "Hemi-cut", "Hemispheres")
    log.info("-" * 100)
    for cf in sorted(data_cutflows, key=lambda c: c["file"]):
        log.info("%-50s %10d %10d %10d %10d %10d",
                 cf["file"], cf["total"], cf["subsample_10pct"],
                 cf["after_selection"], cf["after_hemi_cut"], cf["hemispheres"])
    log.info("-" * 100)
    log.info("%-50s %10d %10d %10d %10d %10d",
             "TOTAL",
             cutflow_summary["total_events_raw"],
             cutflow_summary["total_subsample"],
             cutflow_summary["total_selected"],
             cutflow_summary["total_hemi_cut"],
             cutflow_summary["total_hemispheres"])


if __name__ == "__main__":
    main()
