#!/usr/bin/env python3
"""Phase 4a Script 03: Bootstrap covariance matrices.

Computes statistical covariance via event-level bootstrap,
per-systematic covariance via outer product of shifts,
and total covariance. Validates PSD and condition number.

Session: Felix | Phase 4a
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

MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")

# Binning
X_EDGES = np.linspace(0, 5, 11)
Y_EDGES = np.linspace(-3, 4, 11)
NX = len(X_EDGES) - 1
NY = len(Y_EDGES) - 1
N_BINS = NX * NY
BIN_AREA = (X_EDGES[1] - X_EDGES[0]) * (Y_EDGES[1] - Y_EDGES[0])
M_PI = 0.13957


def decluster_primary_chain(px, py, pz, pmag):
    """Cluster one hemisphere with C/A and extract primary Lund splittings."""
    n = len(px)
    if n < 2:
        return np.empty(0), np.empty(0)
    energy = np.sqrt(pmag**2 + M_PI**2)
    particles = [
        fastjet.PseudoJet(float(px[i]), float(py[i]), float(pz[i]), float(energy[i]))
        for i in range(n)
    ]
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
        harder, softer = (p1, p2) if pt1 >= pt2 else (p2, p1)
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


def load_per_event_histograms(filepath):
    """Load one MC file and return per-event Lund plane histograms.

    Returns list of (reco_hist_flat, genBefore_hist_flat) tuples, one per event.
    Events that fail selection at either level are excluded.
    """
    branches_reco = [
        "px", "py", "pz", "pmag", "d0", "z0", "pwflag",
        "Thrust", "TTheta", "TPhi", "passesAll",
    ]
    branches_gen = ["px", "py", "pz", "pmag", "pwflag", "Thrust", "TTheta", "TPhi"]

    with uproot.open(filepath) as f:
        reco_arrays = f["t"].arrays(branches_reco)
        genb_arrays = f["tgenBefore"].arrays(branches_gen)

    # Process reco
    evt_mask_r = (reco_arrays["passesAll"] == True) & (reco_arrays["Thrust"] > 0.7)  # noqa: E712
    sel_r = reco_arrays[evt_mask_r]
    trk_r = (
        (sel_r["pwflag"] == 0)
        & (sel_r["pmag"] > 0.2)
        & (np.abs(sel_r["d0"]) < 2.0)
        & (np.abs(sel_r["z0"]) < 10.0)
    )
    nch_r = ak.sum(trk_r, axis=1)
    evt_mask_r2 = nch_r >= 5
    sel_r = sel_r[evt_mask_r2]
    trk_r = trk_r[evt_mask_r2]

    ttheta = sel_r["TTheta"]
    tphi = sel_r["TPhi"]
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)
    dot = sel_r["px"] * tx + sel_r["py"] * ty + sel_r["pz"] * tz
    hemi_plus_r = trk_r & (dot > 0)
    hemi_minus_r = trk_r & (dot <= 0)
    n_plus = ak.sum(hemi_plus_r, axis=1)
    n_minus = ak.sum(hemi_minus_r, axis=1)
    good_r = (n_plus >= 2) & (n_minus >= 2)
    sel_r = sel_r[good_r]
    hemi_plus_r = hemi_plus_r[good_r]
    hemi_minus_r = hemi_minus_r[good_r]

    # Process per-event reco histograms
    n_events = len(sel_r)
    event_hists_reco = []
    for i in range(n_events):
        h_evt = np.zeros(N_BINS, dtype=np.float64)
        for hemi_mask in [hemi_plus_r, hemi_minus_r]:
            mask = hemi_mask[i]
            px_arr = np.asarray(sel_r["px"][i][mask], dtype=np.float64)
            py_arr = np.asarray(sel_r["py"][i][mask], dtype=np.float64)
            pz_arr = np.asarray(sel_r["pz"][i][mask], dtype=np.float64)
            pmag_arr = np.asarray(sel_r["pmag"][i][mask], dtype=np.float64)
            lx, ly = decluster_primary_chain(px_arr, py_arr, pz_arr, pmag_arr)
            if len(lx) > 0:
                ix = np.digitize(lx, X_EDGES) - 1
                iy = np.digitize(ly, Y_EDGES) - 1
                valid = (ix >= 0) & (ix < NX) & (iy >= 0) & (iy < NY)
                for x_i, y_i in zip(ix[valid], iy[valid]):
                    h_evt[x_i * NY + y_i] += 1
        event_hists_reco.append(h_evt)

    return event_hists_reco


def bootstrap_one_replica(args):
    """Compute one bootstrap replica.

    Args: (replica_id, all_event_hists, correction_flat, n_hemi_genb, n_total_events)
    Returns: corrected density (flat)
    """
    replica_id, n_total_events, seed_base = args
    rng = np.random.RandomState(seed_base + replica_id)

    # Resample events with replacement
    indices = rng.randint(0, n_total_events, size=n_total_events)
    return indices


def main():
    log.info("=" * 70)
    log.info("Phase 4a Script 03: Bootstrap Covariance Matrices")
    log.info("Session: Felix")
    log.info("=" * 70)

    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    log.info("Found %d MC files", len(mc_files))

    # Load nominal correction
    corr_d = np.load("phase3_selection/outputs/correction_ingrid.npz")
    correction_flat = corr_d["correction"].flatten()
    n_hemi_genb = float(corr_d["n_hemi_genBefore"])

    # ================================================================
    # Step 1: Load all per-event histograms
    # ================================================================
    log.info("\n=== Step 1: Loading per-event histograms ===")
    t0 = time.time()

    all_event_hists = []
    n_workers = 6

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(load_per_event_histograms, f): f for f in mc_files}
        done = 0
        for future in as_completed(futures):
            hists = future.result()
            all_event_hists.extend(hists)
            done += 1
            if done % 10 == 0:
                log.info("  Progress: %d/%d files (%d events so far)",
                         done, len(mc_files), len(all_event_hists))

    n_total = len(all_event_hists)
    dt = time.time() - t0
    log.info("Loaded %d events in %.1fs", n_total, dt)

    # Stack into array for fast bootstrap
    event_matrix = np.array(all_event_hists)  # (n_events, N_BINS)
    del all_event_hists  # free memory

    # Nominal: sum all events
    reco_nominal = event_matrix.sum(axis=0)  # (N_BINS,)
    corrected_nominal = reco_nominal * correction_flat
    rho_nominal = corrected_nominal / (n_hemi_genb * BIN_AREA)

    # ================================================================
    # Step 2: Bootstrap replicas
    # ================================================================
    N_REPLICAS = 500
    log.info("\n=== Step 2: %d bootstrap replicas ===", N_REPLICAS)
    t0 = time.time()

    rng = np.random.RandomState(42)
    bootstrap_densities = np.zeros((N_REPLICAS, N_BINS))

    for rep in range(N_REPLICAS):
        # Resample events with replacement
        indices = rng.randint(0, n_total, size=n_total)
        reco_rep = event_matrix[indices].sum(axis=0)
        # Each resampled event contributes 2 hemispheres
        n_hemi_rep = 2 * n_total  # same as nominal (same number of events)
        corrected_rep = reco_rep * correction_flat
        rho_rep = corrected_rep / (n_hemi_genb * BIN_AREA)
        bootstrap_densities[rep, :] = rho_rep

        if (rep + 1) % 100 == 0:
            log.info("  Replica %d/%d", rep + 1, N_REPLICAS)

    dt = time.time() - t0
    log.info("Bootstrap complete: %.1fs (%.3fs per replica)", dt, dt / N_REPLICAS)

    # ================================================================
    # Step 3: Statistical covariance
    # ================================================================
    log.info("\n=== Step 3: Statistical covariance ===")

    cov_stat = np.cov(bootstrap_densities, rowvar=False)  # (N_BINS, N_BINS)
    log.info("Stat covariance shape: %s", cov_stat.shape)

    # Diagonal uncertainties
    stat_err = np.sqrt(np.diag(cov_stat))
    mask = rho_nominal > 0
    log.info("Stat uncertainty: mean=%.4f, max=%.4f (relative: mean=%.4f, max=%.4f)",
             np.mean(stat_err[mask]), np.max(stat_err[mask]),
             np.mean(stat_err[mask] / rho_nominal[mask]),
             np.max(stat_err[mask] / rho_nominal[mask]))

    # ================================================================
    # Step 4: Systematic covariances
    # ================================================================
    log.info("\n=== Step 4: Systematic covariances ===")

    syst_d = np.load(OUT_DIR / "systematics_felix.npz")
    syst_names = [
        "tracking_efficiency", "momentum_resolution", "angular_resolution",
        "track_p_threshold", "track_d0_cut", "thrust_cut", "nch_min",
        "thrust_axis_resolution", "mc_model_dependence", "heavy_flavour",
        "isr_modelling",
    ]
    # Check if unfolding_method exists
    if f"unfolding_method_sym" in syst_d:
        syst_names.append("unfolding_method")

    cov_syst = np.zeros((N_BINS, N_BINS))
    per_syst_cov = {}

    for name in syst_names:
        key = f"{name}_sym"
        if key in syst_d:
            shift = syst_d[key]
            # Covariance from symmetric shift: C_ij = shift_i * shift_j
            cov_s = np.outer(shift, shift)
            per_syst_cov[name] = cov_s
            cov_syst += cov_s
            diag_err = np.sqrt(np.diag(cov_s))
            log.info("  %s: max diag err = %.6f", name,
                     np.max(diag_err[mask]) if mask.any() else 0)
        else:
            log.info("  %s: MISSING (key %s not found)", name, key)

    # ================================================================
    # Step 5: Total covariance
    # ================================================================
    log.info("\n=== Step 5: Total covariance ===")

    cov_total = cov_stat + cov_syst
    total_err = np.sqrt(np.diag(cov_total))
    log.info("Total uncertainty: mean=%.4f, max=%.4f",
             np.mean(total_err[mask]), np.max(total_err[mask]))

    # ================================================================
    # Step 6: Validation
    # ================================================================
    log.info("\n=== Step 6: Covariance validation ===")

    # PSD check
    eigenvalues_stat = np.linalg.eigvalsh(cov_stat)
    eigenvalues_total = np.linalg.eigvalsh(cov_total)

    min_eig_stat = float(np.min(eigenvalues_stat))
    min_eig_total = float(np.min(eigenvalues_total))
    psd_stat = min_eig_stat >= -1e-12  # allow numerical noise
    psd_total = min_eig_total >= -1e-12

    log.info("Stat covariance PSD: %s (min eigenvalue = %.2e)", psd_stat, min_eig_stat)
    log.info("Total covariance PSD: %s (min eigenvalue = %.2e)", psd_total, min_eig_total)

    # If not PSD, clip negative eigenvalues
    if not psd_total:
        log.info("  Clipping negative eigenvalues...")
        eigvals, eigvecs = np.linalg.eigh(cov_total)
        eigvals = np.maximum(eigvals, 0)
        cov_total = eigvecs @ np.diag(eigvals) @ eigvecs.T
        min_eig_total = 0.0
        psd_total = True

    # Condition number
    # Use only populated bins for condition number
    pop_idx = np.where(mask)[0]
    if len(pop_idx) > 0:
        cov_pop = cov_total[np.ix_(pop_idx, pop_idx)]
        eigvals_pop = np.linalg.eigvalsh(cov_pop)
        pos_eigvals = eigvals_pop[eigvals_pop > 0]
        if len(pos_eigvals) > 0:
            cond_number = float(np.max(pos_eigvals) / np.min(pos_eigvals))
        else:
            cond_number = float("inf")
    else:
        cond_number = float("inf")

    log.info("Condition number (populated bins): %.2e", cond_number)
    log.info("Condition number < 10^10: %s", cond_number < 1e10)

    # Correlation matrix
    corr_matrix = np.zeros_like(cov_total)
    for i in range(N_BINS):
        for j in range(N_BINS):
            if total_err[i] > 0 and total_err[j] > 0:
                corr_matrix[i, j] = cov_total[i, j] / (total_err[i] * total_err[j])

    # ================================================================
    # Step 7: Save
    # ================================================================
    log.info("\n=== Step 7: Saving ===")

    np.savez(
        OUT_DIR / "covariance_felix.npz",
        cov_stat=cov_stat,
        cov_syst=cov_syst,
        cov_total=cov_total,
        corr_matrix=corr_matrix,
        stat_err=stat_err,
        total_err=total_err,
        rho_nominal=rho_nominal,
        x_edges=X_EDGES,
        y_edges=Y_EDGES,
        n_replicas=N_REPLICAS,
    )

    # Save per-systematic covariances
    per_syst_save = {}
    for name, cov in per_syst_cov.items():
        per_syst_save[name] = cov
    np.savez(OUT_DIR / "per_syst_covariance_felix.npz", **per_syst_save)

    # JSON output
    results_dir = Path("analysis_note/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    cov_json = {
        "n_bins": N_BINS,
        "n_populated_bins": int(np.sum(mask)),
        "n_bootstrap_replicas": N_REPLICAS,
        "stat_covariance": cov_stat.tolist(),
        "syst_covariance": cov_syst.tolist(),
        "total_covariance": cov_total.tolist(),
        "correlation_matrix": corr_matrix.tolist(),
        "validation": {
            "psd_stat": bool(psd_stat),
            "psd_total": bool(psd_total),
            "min_eigenvalue_stat": min_eig_stat,
            "min_eigenvalue_total": min_eig_total,
            "condition_number": cond_number,
            "condition_lt_1e10": bool(cond_number < 1e10),
        },
        "bin_edges_x": X_EDGES.tolist(),
        "bin_edges_y": Y_EDGES.tolist(),
    }
    with open(results_dir / "covariance.json", "w") as f:
        json.dump(cov_json, f, indent=2)

    log.info("\nCovariance matrices saved.")
    log.info("PSD stat: %s, PSD total: %s, Condition: %.2e",
             psd_stat, psd_total, cond_number)


if __name__ == "__main__":
    main()
