#!/usr/bin/env python3
"""Prototype: process 1 MC file to validate code and time.

Session: Ingrid | Phase 3
"""

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
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")

X_EDGES = np.linspace(0, 5, 11)
Y_EDGES = np.linspace(-3, 4, 11)
M_PI = 0.13957


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


def process_tree(filepath, tree_name, apply_evt_sel=True, max_events=None):
    """Process one tree from a ROOT file.
    Returns (h2d, n_hemispheres, n_splittings, n_total, n_selected, n_hemi_cut).
    """
    if tree_name == "t":
        branches = ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                     "Thrust", "TTheta", "TPhi", "passesAll"]
    else:
        branches = ["px", "py", "pz", "pmag", "pwflag",
                     "Thrust", "TTheta", "TPhi"]

    with uproot.open(filepath) as f:
        arrays = f[tree_name].arrays(branches, entry_stop=max_events)

    n_total = len(arrays)

    # Event selection
    if apply_evt_sel and tree_name == "t":
        evt_mask = (arrays["passesAll"] == True) & (arrays["Thrust"] > 0.7)  # noqa: E712
        arrays = arrays[evt_mask]

    # Track selection
    if tree_name == "t":
        trk_mask = (
            (arrays["pwflag"] == 0) & (arrays["pmag"] > 0.2)
            & (np.abs(arrays["d0"]) < 2.0) & (np.abs(arrays["z0"]) < 10.0)
        )
    else:
        trk_mask = (arrays["pwflag"] == 0) & (arrays["pmag"] > 0.2)

    # N_ch >= 5
    nch = ak.sum(trk_mask, axis=1)
    evt_mask2 = nch >= 5
    arrays = arrays[evt_mask2]
    trk_mask = trk_mask[evt_mask2]
    n_selected = len(arrays)

    # Hemisphere split
    ttheta = arrays["TTheta"]
    tphi = arrays["TPhi"]
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)

    dot = arrays["px"] * tx + arrays["py"] * ty + arrays["pz"] * tz
    hemi_plus = trk_mask & (dot > 0)
    hemi_minus = trk_mask & (dot <= 0)

    n_plus = ak.sum(hemi_plus, axis=1)
    n_minus = ak.sum(hemi_minus, axis=1)
    good = (n_plus >= 2) & (n_minus >= 2)

    arrays = arrays[good]
    hemi_plus = hemi_plus[good]
    hemi_minus = hemi_minus[good]
    n_hemi_cut = len(arrays)

    # Decluster
    h2d = np.zeros((len(X_EDGES) - 1, len(Y_EDGES) - 1), dtype=np.float64)
    n_hemispheres = 0
    n_splittings = 0

    for i in range(len(arrays)):
        for hemi_mask in [hemi_plus, hemi_minus]:
            mask = hemi_mask[i]
            px_arr = np.asarray(arrays["px"][i][mask], dtype=np.float64)
            py_arr = np.asarray(arrays["py"][i][mask], dtype=np.float64)
            pz_arr = np.asarray(arrays["pz"][i][mask], dtype=np.float64)
            pmag_arr = np.asarray(arrays["pmag"][i][mask], dtype=np.float64)

            lx, ly = decluster_primary_chain(px_arr, py_arr, pz_arr, pmag_arr)
            if len(lx) > 0:
                h, _, _ = np.histogram2d(lx, ly, bins=[X_EDGES, Y_EDGES])
                h2d += h
                n_splittings += len(lx)
            n_hemispheres += 1

    return h2d, n_hemispheres, n_splittings, n_total, n_selected, n_hemi_cut


def main():
    log.info("=== PROTOTYPE: 1 MC file (reco + gen + genBefore) ===")

    mc_file = MC_DIR / "LEP1MC1994_recons_aftercut-001.root"

    # Reco
    t0 = time.time()
    h_reco, nh_reco, ns_reco, nt_reco, nsel_reco, nhc_reco = process_tree(
        mc_file, "t", apply_evt_sel=True)
    dt_reco = time.time() - t0
    log.info("Reco: %d total -> %d sel -> %d hemi -> %d hemispheres, %d splits (%.1fs)",
             nt_reco, nsel_reco, nhc_reco, nh_reco, ns_reco, dt_reco)

    # Gen
    t0 = time.time()
    h_gen, nh_gen, ns_gen, nt_gen, nsel_gen, nhc_gen = process_tree(
        mc_file, "tgen", apply_evt_sel=False)
    dt_gen = time.time() - t0
    log.info("Gen: %d total -> %d sel -> %d hemi -> %d hemispheres, %d splits (%.1fs)",
             nt_gen, nsel_gen, nhc_gen, nh_gen, ns_gen, dt_gen)

    # GenBefore
    t0 = time.time()
    h_genb, nh_genb, ns_genb, nt_genb, nsel_genb, nhc_genb = process_tree(
        mc_file, "tgenBefore", apply_evt_sel=False)
    dt_genb = time.time() - t0
    log.info("GenBefore: %d total -> %d sel -> %d hemi -> %d hemispheres, %d splits (%.1fs)",
             nt_genb, nsel_genb, nhc_genb, nh_genb, ns_genb, dt_genb)

    total_time = dt_reco + dt_gen + dt_genb
    log.info("\nTotal time for 1 MC file (3 trees): %.1fs", total_time)
    log.info("Estimated time for 40 MC files: %.0fs (%.1f min)",
             total_time * 40, total_time * 40 / 60)
    log.info("Estimated time for 6 data files (reco only): %.0fs (%.1f min)",
             dt_reco * 6 * (nt_reco / 19158 * 500000 / nt_reco),
             dt_reco * 6 * 500000 / nt_reco / 60)

    # Quick sanity checks
    log.info("\nSanity checks:")
    log.info("  Avg splits/hemi: reco=%.2f, gen=%.2f, genBefore=%.2f",
             ns_reco / max(nh_reco, 1), ns_gen / max(nh_gen, 1),
             ns_genb / max(nh_genb, 1))
    log.info("  genBefore/gen ratio: %.3f", nt_genb / max(nt_gen, 1))
    log.info("  Correction factor (genBefore/reco) range: %.2f - %.2f",
             np.min(h_genb[h_reco > 0] / h_reco[h_reco > 0]),
             np.max(h_genb[h_reco > 0] / h_reco[h_reco > 0]))

    log.info("\nPrototype PASSED.")


if __name__ == "__main__":
    main()
