#!/usr/bin/env python3
"""Script 01: Full event selection + Lund plane construction on ALL data and MC.

Processes all 6 data files and all 40 MC files. For MC, processes reco, gen,
and genBefore levels. Uses ProcessPoolExecutor for parallel file processing.

Session: Ingrid | Phase 3
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

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")

# Binning
X_EDGES = np.linspace(0, 5, 11)  # 10 bins, ln(1/Delta_theta)
Y_EDGES = np.linspace(-3, 4, 11)  # 10 bins, ln(k_T/GeV)

M_PI = 0.13957  # Pion mass in GeV


def apply_selection(arrays):
    """Apply event and track selection. Returns selected arrays, track mask."""
    # Event selection
    evt_mask = (arrays["passesAll"] == True) & (arrays["Thrust"] > 0.7)  # noqa: E712
    sel = arrays[evt_mask]

    # Track selection (per-particle)
    trk_mask = (
        (sel["pwflag"] == 0)
        & (sel["pmag"] > 0.2)
        & (np.abs(sel["d0"]) < 2.0)
        & (np.abs(sel["z0"]) < 10.0)
    )

    # N_ch >= 5
    nch = ak.sum(trk_mask, axis=1)
    evt_mask2 = nch >= 5
    sel = sel[evt_mask2]
    trk_mask = trk_mask[evt_mask2]

    return sel, trk_mask


def apply_gen_selection(arrays):
    """Apply gen-level selection for tgen tree (after event selection).
    Track selection: pwflag == 0, p > 200 MeV.
    """
    # tgen already has event selection applied
    trk_mask = (arrays["pwflag"] == 0) & (arrays["pmag"] > 0.2)

    # N_ch >= 5
    nch = ak.sum(trk_mask, axis=1)
    evt_mask = nch >= 5
    sel = arrays[evt_mask]
    trk_mask = trk_mask[evt_mask]

    return sel, trk_mask


def apply_genBefore_selection(arrays):
    """Apply gen-level selection for tgenBefore tree (before event selection).
    Only particle-level cuts (no event selection).
    Track selection: pwflag == 0, p > 200 MeV.
    """
    trk_mask = (arrays["pwflag"] == 0) & (arrays["pmag"] > 0.2)

    # N_ch >= 5 at particle level
    nch = ak.sum(trk_mask, axis=1)
    evt_mask = nch >= 5
    sel = arrays[evt_mask]
    trk_mask = trk_mask[evt_mask]

    return sel, trk_mask


def split_hemispheres(sel, trk_mask):
    """Split events into thrust hemispheres. Returns hemisphere masks and
    event mask for events with >= 2 tracks in each hemisphere."""
    ttheta = sel["TTheta"]
    tphi = sel["TPhi"]
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)

    dot = sel["px"] * tx + sel["py"] * ty + sel["pz"] * tz
    hemi_plus = trk_mask & (dot > 0)
    hemi_minus = trk_mask & (dot <= 0)

    # Require >= 2 tracks per hemisphere
    n_plus = ak.sum(hemi_plus, axis=1)
    n_minus = ak.sum(hemi_minus, axis=1)
    good = (n_plus >= 2) & (n_minus >= 2)

    return hemi_plus[good], hemi_minus[good], good


def decluster_primary_chain(px, py, pz, pmag):
    """Cluster one hemisphere with C/A and extract primary Lund splittings.

    Returns arrays of (ln_1_over_dtheta, ln_kt).
    """
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

        # p_T w.r.t. beam as hardness variable
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
    """Process selected events: decluster both hemispheres, collect Lund splittings.
    Returns 2D histogram, total hemispheres, total splittings.
    """
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


def process_data_file(filepath):
    """Process a single data file. Returns (h2d, n_hemi, n_split, cutflow_dict)."""
    log.info("DATA: %s", filepath.name)
    t0 = time.time()

    branches = ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                "Thrust", "TTheta", "TPhi", "passesAll"]

    with uproot.open(filepath) as f:
        arrays = f["t"].arrays(branches)

    n_total = len(arrays)

    sel, trk_mask = apply_selection(arrays)
    n_after_sel = len(sel)

    hemi_plus, hemi_minus, good = split_hemispheres(sel, trk_mask)
    sel = sel[good]
    n_after_hemi = len(sel)

    h2d, n_hemi, n_split = process_events_lund(sel, hemi_plus, hemi_minus)

    dt = time.time() - t0
    log.info("  %s: %d events -> %d selected -> %d hemi-cut -> %d hemi, %d splits (%.1fs)",
             filepath.name, n_total, n_after_sel, n_after_hemi, n_hemi, n_split, dt)

    cutflow = {
        "file": filepath.name,
        "total": int(n_total),
        "after_selection": int(n_after_sel),
        "after_hemi_cut": int(n_after_hemi),
        "hemispheres": int(n_hemi),
        "splittings": int(n_split),
    }
    return h2d, n_hemi, n_split, cutflow


def process_mc_file(filepath):
    """Process a single MC file at reco, gen, and genBefore levels.
    Returns dict with h2d/n_hemi/n_split for each level, plus cutflow.
    """
    log.info("MC: %s", filepath.name)
    t0 = time.time()

    branches_reco = ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                     "Thrust", "TTheta", "TPhi", "passesAll"]
    branches_gen = ["px", "py", "pz", "pmag", "pwflag",
                    "Thrust", "TTheta", "TPhi"]

    result = {}

    with uproot.open(filepath) as f:
        # --- Reco level ---
        reco_arrays = f["t"].arrays(branches_reco)
        n_reco_total = len(reco_arrays)

        sel_reco, trk_reco = apply_selection(reco_arrays)
        n_reco_sel = len(sel_reco)
        hp_reco, hm_reco, good_reco = split_hemispheres(sel_reco, trk_reco)
        sel_reco = sel_reco[good_reco]
        n_reco_hemi = len(sel_reco)

        h2d_reco, n_h_reco, n_s_reco = process_events_lund(sel_reco, hp_reco, hm_reco)
        result["reco"] = {"h2d": h2d_reco, "n_hemi": n_h_reco, "n_split": n_s_reco}

        # --- Gen level (tgen, after event selection) ---
        gen_arrays = f["tgen"].arrays(branches_gen)
        n_gen_total = len(gen_arrays)

        sel_gen, trk_gen = apply_gen_selection(gen_arrays)
        n_gen_sel = len(sel_gen)
        hp_gen, hm_gen, good_gen = split_hemispheres(sel_gen, trk_gen)
        sel_gen = sel_gen[good_gen]
        n_gen_hemi = len(sel_gen)

        h2d_gen, n_h_gen, n_s_gen = process_events_lund(sel_gen, hp_gen, hm_gen)
        result["gen"] = {"h2d": h2d_gen, "n_hemi": n_h_gen, "n_split": n_s_gen}

        # --- GenBefore level (tgenBefore, before event selection) ---
        genb_arrays = f["tgenBefore"].arrays(branches_gen)
        n_genb_total = len(genb_arrays)

        sel_genb, trk_genb = apply_genBefore_selection(genb_arrays)
        n_genb_sel = len(sel_genb)
        hp_genb, hm_genb, good_genb = split_hemispheres(sel_genb, trk_genb)
        sel_genb = sel_genb[good_genb]
        n_genb_hemi = len(sel_genb)

        h2d_genb, n_h_genb, n_s_genb = process_events_lund(sel_genb, hp_genb, hm_genb)
        result["genBefore"] = {"h2d": h2d_genb, "n_hemi": n_h_genb, "n_split": n_s_genb}

    dt = time.time() - t0
    log.info("  %s: reco %d/%d, gen %d/%d, genB %d/%d (%.1fs)",
             filepath.name, n_reco_hemi, n_reco_total,
             n_gen_hemi, n_gen_total, n_genb_hemi, n_genb_total, dt)

    cutflow = {
        "file": filepath.name,
        "reco_total": int(n_reco_total),
        "reco_selected": int(n_reco_sel),
        "reco_hemi": int(n_reco_hemi),
        "reco_hemispheres": int(n_h_reco),
        "reco_splittings": int(n_s_reco),
        "gen_total": int(n_gen_total),
        "gen_selected": int(n_gen_sel),
        "gen_hemi": int(n_gen_hemi),
        "gen_hemispheres": int(n_h_gen),
        "gen_splittings": int(n_s_gen),
        "genBefore_total": int(n_genb_total),
        "genBefore_selected": int(n_genb_sel),
        "genBefore_hemi": int(n_genb_hemi),
        "genBefore_hemispheres": int(n_h_genb),
        "genBefore_splittings": int(n_s_genb),
    }
    result["cutflow"] = cutflow
    return result


def main():
    log.info("=" * 70)
    log.info("Phase 3 Script 01: Full Event Selection + Lund Plane Construction")
    log.info("Session: Ingrid")
    log.info("=" * 70)

    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    log.info("Found %d data files, %d MC files", len(data_files), len(mc_files))

    # === PRODUCTION: All files ===
    # Timing from prototype: ~122s per MC file (3 trees), ~35s per data file.
    # Always use parallel for this dataset.
    n_workers = 8
    log.info("\n--- PRODUCTION: %d data + %d MC files (workers=%d) ---",
             len(data_files), len(mc_files), n_workers)

    # --- Process ALL MC files ---
    log.info("\nProcessing ALL MC files...")
    mc_h2d_reco = np.zeros((len(X_EDGES) - 1, len(Y_EDGES) - 1), dtype=np.float64)
    mc_h2d_gen = np.zeros_like(mc_h2d_reco)
    mc_h2d_genBefore = np.zeros_like(mc_h2d_reco)
    mc_n_hemi_reco = 0
    mc_n_hemi_gen = 0
    mc_n_hemi_genBefore = 0
    mc_n_split_reco = 0
    mc_n_split_gen = 0
    mc_n_split_genBefore = 0
    mc_cutflows = []

    mc_t0 = time.time()
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_mc_file, f): f for f in mc_files}
        done_count = 0
        for future in as_completed(futures):
            r = future.result()
            mc_h2d_reco += r["reco"]["h2d"]
            mc_h2d_gen += r["gen"]["h2d"]
            mc_h2d_genBefore += r["genBefore"]["h2d"]
            mc_n_hemi_reco += r["reco"]["n_hemi"]
            mc_n_hemi_gen += r["gen"]["n_hemi"]
            mc_n_hemi_genBefore += r["genBefore"]["n_hemi"]
            mc_n_split_reco += r["reco"]["n_split"]
            mc_n_split_gen += r["gen"]["n_split"]
            mc_n_split_genBefore += r["genBefore"]["n_split"]
            mc_cutflows.append(r["cutflow"])
            done_count += 1
            if done_count % 10 == 0:
                log.info("  MC progress: %d/%d files done", done_count, len(mc_files))

    mc_dt = time.time() - mc_t0
    log.info("\nMC total: %.1fs", mc_dt)
    log.info("MC reco: %d hemispheres, %d splittings", mc_n_hemi_reco, mc_n_split_reco)
    log.info("MC gen: %d hemispheres, %d splittings", mc_n_hemi_gen, mc_n_split_gen)
    log.info("MC genBefore: %d hemispheres, %d splittings",
             mc_n_hemi_genBefore, mc_n_split_genBefore)

    # --- Process ALL data files ---
    log.info("\nProcessing ALL data files...")
    data_h2d = np.zeros((len(X_EDGES) - 1, len(Y_EDGES) - 1), dtype=np.float64)
    data_n_hemi = 0
    data_n_split = 0
    data_cutflows = []

    data_t0 = time.time()
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_data_file, f): f for f in data_files}
        for future in as_completed(futures):
            h2d, n_h, n_s, cf = future.result()
            data_h2d += h2d
            data_n_hemi += n_h
            data_n_split += n_s
            data_cutflows.append(cf)

    data_dt = time.time() - data_t0
    log.info("\nData total: %.1fs", data_dt)
    log.info("Data: %d hemispheres, %d splittings", data_n_hemi, data_n_split)

    # === SAVE RESULTS ===
    log.info("\nSaving results...")

    np.savez(
        OUT_DIR / "data_lund_ingrid.npz",
        h2d=data_h2d,
        n_hemispheres=data_n_hemi,
        n_splittings=data_n_split,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
    )

    np.savez(
        OUT_DIR / "mc_reco_lund_ingrid.npz",
        h2d=mc_h2d_reco,
        n_hemispheres=mc_n_hemi_reco,
        n_splittings=mc_n_split_reco,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
    )

    np.savez(
        OUT_DIR / "mc_gen_lund_ingrid.npz",
        h2d=mc_h2d_gen,
        n_hemispheres=mc_n_hemi_gen,
        n_splittings=mc_n_split_gen,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
    )

    np.savez(
        OUT_DIR / "mc_genBefore_lund_ingrid.npz",
        h2d=mc_h2d_genBefore,
        n_hemispheres=mc_n_hemi_genBefore,
        n_splittings=mc_n_split_genBefore,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
    )

    # Save cutflow summary
    cutflow_summary = {
        "data": {
            "per_file": data_cutflows,
            "total_events": sum(c["total"] for c in data_cutflows),
            "total_selected": sum(c["after_selection"] for c in data_cutflows),
            "total_hemi_cut": sum(c["after_hemi_cut"] for c in data_cutflows),
            "total_hemispheres": int(data_n_hemi),
            "total_splittings": int(data_n_split),
        },
        "mc": {
            "per_file": mc_cutflows,
            "reco_total": sum(c["reco_total"] for c in mc_cutflows),
            "reco_selected": sum(c["reco_selected"] for c in mc_cutflows),
            "reco_hemi": sum(c["reco_hemi"] for c in mc_cutflows),
            "reco_hemispheres": int(mc_n_hemi_reco),
            "reco_splittings": int(mc_n_split_reco),
            "gen_total": sum(c["gen_total"] for c in mc_cutflows),
            "gen_selected": sum(c["gen_selected"] for c in mc_cutflows),
            "gen_hemi": sum(c["gen_hemi"] for c in mc_cutflows),
            "gen_hemispheres": int(mc_n_hemi_gen),
            "gen_splittings": int(mc_n_split_gen),
            "genBefore_total": sum(c["genBefore_total"] for c in mc_cutflows),
            "genBefore_selected": sum(c["genBefore_selected"] for c in mc_cutflows),
            "genBefore_hemi": sum(c["genBefore_hemi"] for c in mc_cutflows),
            "genBefore_hemispheres": int(mc_n_hemi_genBefore),
            "genBefore_splittings": int(mc_n_split_genBefore),
        },
    }

    with open(OUT_DIR / "cutflow_ingrid.json", "w") as f:
        json.dump(cutflow_summary, f, indent=2)

    log.info("All results saved to %s", OUT_DIR)
    log.info("\n=== SUMMARY ===")
    log.info("Data: %d hemispheres, %d splittings (%.2f splits/hemi)",
             data_n_hemi, data_n_split, data_n_split / max(data_n_hemi, 1))
    log.info("MC reco: %d hemispheres, %d splittings (%.2f splits/hemi)",
             mc_n_hemi_reco, mc_n_split_reco,
             mc_n_split_reco / max(mc_n_hemi_reco, 1))
    log.info("MC gen: %d hemispheres, %d splittings (%.2f splits/hemi)",
             mc_n_hemi_gen, mc_n_split_gen,
             mc_n_split_gen / max(mc_n_hemi_gen, 1))
    log.info("MC genBefore: %d hemispheres, %d splittings (%.2f splits/hemi)",
             mc_n_hemi_genBefore, mc_n_split_genBefore,
             mc_n_split_genBefore / max(mc_n_hemi_genBefore, 1))


if __name__ == "__main__":
    main()
