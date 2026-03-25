#!/usr/bin/env python3
"""Script 04: Approach comparison -- A (thrust hemispheres) vs C (exclusive kT 2-jets).

Approach A: Thrust hemispheres with C/A declustering (primary, from 01_process_all.py)
Approach C: Exclusive kT 2-jets, then C/A declustering of each jet

Processes a subset of data to compare the two approaches quantitatively.
Uses ~200k data events for adequate statistics.

Session: Ingrid | Phase 3
"""

import json
import logging
import time
from pathlib import Path

import awkward as ak
import fastjet
import numpy as np
import uproot
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")

X_EDGES = np.linspace(0, 5, 11)
Y_EDGES = np.linspace(-3, 4, 11)
M_PI = 0.13957
N_EVENTS_PER_FILE = 50000  # Process 50k per file for comparison


def decluster_primary_chain(px, py, pz, pmag):
    """Cluster with C/A and extract primary Lund splittings."""
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

        pt1 = np.sqrt(p1.px()**2 + p1.py()**2)
        pt2 = np.sqrt(p2.px()**2 + p2.py()**2)
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


def approach_c_exclusive_kt(px, py, pz, pmag):
    """Approach C: Cluster full event with kT (Durham) into exactly 2 jets,
    then decluster each jet with C/A."""
    n = len(px)
    if n < 4:  # Need at least 2 particles per jet
        return np.empty(0), np.empty(0)

    energy = np.sqrt(pmag**2 + M_PI**2)
    particles = []
    for i in range(n):
        particles.append(
            fastjet.PseudoJet(float(px[i]), float(py[i]), float(pz[i]), float(energy[i]))
        )

    # Durham kT algorithm for e+e-: ee_genkt_algorithm with p=1
    jet_def_kt = fastjet.JetDefinition(fastjet.ee_genkt_algorithm, 999.0, 1.0)
    cs_kt = fastjet.ClusterSequence(particles, jet_def_kt)

    # Get exactly 2 exclusive jets
    try:
        jets_2 = cs_kt.exclusive_jets(2)
    except Exception:
        return np.empty(0), np.empty(0)

    if len(jets_2) != 2:
        return np.empty(0), np.empty(0)

    # For each jet, get its constituents, then recluster with C/A
    all_lx = []
    all_ly = []

    for jet in jets_2:
        constituents = jet.constituents()
        if len(constituents) < 2:
            continue

        c_px = np.array([c.px() for c in constituents])
        c_py = np.array([c.py() for c in constituents])
        c_pz = np.array([c.pz() for c in constituents])
        c_pmag = np.sqrt(c_px**2 + c_py**2 + c_pz**2)

        lx, ly = decluster_primary_chain(c_px, c_py, c_pz, c_pmag)
        if len(lx) > 0:
            all_lx.extend(lx.tolist())
            all_ly.extend(ly.tolist())

    if len(all_lx) == 0:
        return np.empty(0), np.empty(0)
    return np.array(all_lx), np.array(all_ly)


def main():
    log.info("=" * 70)
    log.info("Phase 3 Script 04: Approach A vs C Comparison")
    log.info("Session: Ingrid")
    log.info("=" * 70)

    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    branches = ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                "Thrust", "TTheta", "TPhi", "passesAll"]

    h2d_a = np.zeros((len(X_EDGES) - 1, len(Y_EDGES) - 1), dtype=np.float64)
    h2d_c = np.zeros_like(h2d_a)
    n_hemi_a = 0
    n_jets_c = 0

    total_events = 0
    target_events = 200000

    t0 = time.time()
    for df in data_files:
        if total_events >= target_events:
            break

        remaining = target_events - total_events
        log.info("Processing %s (up to %d events)...", df.name, remaining)

        with uproot.open(df) as f:
            arrays = f["t"].arrays(branches, entry_stop=remaining)

        # Event selection
        evt_mask = (arrays["passesAll"] == True) & (arrays["Thrust"] > 0.7)  # noqa: E712
        sel = arrays[evt_mask]

        # Track selection
        trk_mask = (
            (sel["pwflag"] == 0) & (sel["pmag"] > 0.2)
            & (np.abs(sel["d0"]) < 2.0) & (np.abs(sel["z0"]) < 10.0)
        )

        nch = ak.sum(trk_mask, axis=1)
        evt_mask2 = nch >= 5
        sel = sel[evt_mask2]
        trk_mask = trk_mask[evt_mask2]

        # Hemisphere split (Approach A)
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
        sel = sel[good]
        hemi_plus = hemi_plus[good]
        hemi_minus = hemi_minus[good]
        trk_mask = trk_mask[good]

        n_events = len(sel)
        total_events += n_events
        log.info("  %d events selected", n_events)

        # Process events
        for i in range(n_events):
            # Approach A: hemisphere declustering
            for hemi_m in [hemi_plus, hemi_minus]:
                mask = hemi_m[i]
                px_arr = np.asarray(sel["px"][i][mask], dtype=np.float64)
                py_arr = np.asarray(sel["py"][i][mask], dtype=np.float64)
                pz_arr = np.asarray(sel["pz"][i][mask], dtype=np.float64)
                pmag_arr = np.asarray(sel["pmag"][i][mask], dtype=np.float64)

                lx, ly = decluster_primary_chain(px_arr, py_arr, pz_arr, pmag_arr)
                if len(lx) > 0:
                    h, _, _ = np.histogram2d(lx, ly, bins=[X_EDGES, Y_EDGES])
                    h2d_a += h
                n_hemi_a += 1

            # Approach C: exclusive kT 2-jets
            tmask = trk_mask[i]
            all_px = np.asarray(sel["px"][i][tmask], dtype=np.float64)
            all_py = np.asarray(sel["py"][i][tmask], dtype=np.float64)
            all_pz = np.asarray(sel["pz"][i][tmask], dtype=np.float64)
            all_pmag = np.asarray(sel["pmag"][i][tmask], dtype=np.float64)

            lx_c, ly_c = approach_c_exclusive_kt(all_px, all_py, all_pz, all_pmag)
            if len(lx_c) > 0:
                h, _, _ = np.histogram2d(lx_c, ly_c, bins=[X_EDGES, Y_EDGES])
                h2d_c += h
            n_jets_c += 2  # 2 jets per event

            if (i + 1) % 50000 == 0:
                log.info("    %d/%d events done", i + 1, n_events)

    dt = time.time() - t0
    log.info("\nProcessed %d events in %.1fs", total_events, dt)
    log.info("Approach A: %d hemispheres, %d splittings",
             n_hemi_a, int(np.sum(h2d_a)))
    log.info("Approach C: %d jets, %d splittings",
             n_jets_c, int(np.sum(h2d_c)))

    # === Compute densities ===
    dx = np.diff(X_EDGES)
    dy = np.diff(Y_EDGES)
    area = np.outer(dx, dy)

    rho_a = h2d_a / (n_hemi_a * area)
    rho_c = h2d_c / (n_jets_c * area)

    # === Comparison metrics ===
    populated = (rho_a > 0) & (rho_c > 0)
    ratio = np.zeros_like(rho_a)
    ratio[populated] = rho_c[populated] / rho_a[populated]

    log.info("\n--- Approach comparison ---")
    log.info("Ratio (C/A) statistics in populated bins:")
    log.info("  Mean: %.4f", np.mean(ratio[populated]))
    log.info("  Std: %.4f", np.std(ratio[populated]))
    log.info("  Min: %.4f", np.min(ratio[populated]))
    log.info("  Max: %.4f", np.max(ratio[populated]))

    # Chi2 comparison
    err_a = np.sqrt(h2d_a) / (n_hemi_a * area)
    err_c = np.sqrt(h2d_c) / (n_jets_c * area)
    mask_chi2 = (err_a > 0) & (err_c > 0) & populated
    diff = rho_a[mask_chi2] - rho_c[mask_chi2]
    err2 = err_a[mask_chi2]**2 + err_c[mask_chi2]**2
    chi2 = np.sum(diff**2 / err2)
    ndf = np.sum(mask_chi2)

    log.info("Chi2 (A vs C): %.1f / %d = %.3f", chi2, ndf, chi2 / max(ndf, 1))

    # 1D projections comparison
    kt_proj_a = np.sum(rho_a, axis=0) * dx[0]
    kt_proj_c = np.sum(rho_c, axis=0) * dx[0]
    dtheta_proj_a = np.sum(rho_a, axis=1) * dy[0]
    dtheta_proj_c = np.sum(rho_c, axis=1) * dy[0]

    # === Save ===
    np.savez(
        OUT_DIR / "approach_c_lund_ingrid.npz",
        h2d_a=h2d_a,
        h2d_c=h2d_c,
        rho_a=rho_a,
        rho_c=rho_c,
        ratio=ratio,
        n_hemi_a=n_hemi_a,
        n_jets_c=n_jets_c,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
        kt_proj_a=kt_proj_a,
        kt_proj_c=kt_proj_c,
        dtheta_proj_a=dtheta_proj_a,
        dtheta_proj_c=dtheta_proj_c,
    )

    comparison = {
        "total_events": int(total_events),
        "approach_a_hemispheres": int(n_hemi_a),
        "approach_c_jets": int(n_jets_c),
        "ratio_mean": float(np.mean(ratio[populated])),
        "ratio_std": float(np.std(ratio[populated])),
        "chi2": float(chi2),
        "ndf": int(ndf),
        "chi2_ndf": float(chi2 / max(ndf, 1)),
    }
    with open(OUT_DIR / "approach_comparison_ingrid.json", "w") as f:
        json.dump(comparison, f, indent=2)

    log.info("\nSaved approach comparison to %s", OUT_DIR)
    log.info("Done.")


if __name__ == "__main__":
    main()
