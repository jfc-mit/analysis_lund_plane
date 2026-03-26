#!/usr/bin/env python3
"""Phase 4a Script 02: Systematic uncertainty evaluation.

Evaluates all committed systematic sources on MC pseudo-data.
Each source produces bin-dependent shifts (not flat percentages).

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
FIG_DIR = OUT_DIR / "figures"

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
    """Process selected events, return 2D histogram + hemisphere count."""
    h2d = np.zeros((NX, NY), dtype=np.float64)
    n_hemi = 0
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
            n_hemi += 1
    return h2d, n_hemi


def split_hemispheres(sel, trk_mask):
    """Split into thrust hemispheres."""
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


# ============================================================
# Systematic variation functions
# ============================================================


def process_mc_file_with_variation(args):
    """Process one MC file with a systematic variation applied.

    Args: tuple of (filepath, variation_name, variation_params)
    Returns: dict with h2d_reco, h2d_genBefore, n_hemi_reco, n_hemi_genBefore
    """
    filepath, var_name, var_params = args

    branches_reco = [
        "px", "py", "pz", "pmag", "d0", "z0", "pwflag",
        "Thrust", "TTheta", "TPhi", "passesAll", "bFlag", "theta", "phi",
    ]
    branches_gen = ["px", "py", "pz", "pmag", "pwflag", "Thrust", "TTheta", "TPhi"]

    with uproot.open(filepath) as f:
        reco_arrays = f["t"].arrays(branches_reco)
        genb_arrays = f["tgenBefore"].arrays(branches_gen)

    rng = np.random.RandomState(hash(filepath.name) % (2**31) + hash(var_name) % (2**31))

    # ---- Apply variation to reco-level tracks ----
    if var_name == "tracking_efficiency_down":
        # Drop 1% of tracks randomly
        drop_prob = var_params.get("drop_fraction", 0.01)
        n_events = len(reco_arrays)
        new_pwflag = []
        for i in range(n_events):
            pf = np.asarray(reco_arrays["pwflag"][i])
            charged = pf == 0
            drops = rng.random(len(pf)) < drop_prob
            # Drop: set pwflag to -1 for dropped charged tracks
            pf_new = pf.copy()
            pf_new[charged & drops] = -1
            new_pwflag.append(pf_new)
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pwflag), "pwflag")

    elif var_name == "momentum_resolution_up":
        # Smear momenta by +10% of resolution
        # ALEPH TPC resolution: sigma(p)/p ~ 0.6e-3 * p (p in GeV/c)
        # +10% means sigma_smear = 0.1 * 0.6e-3 * p^2
        smear_frac = var_params.get("smear_fraction", 0.1)
        sigma_coeff = 0.6e-3  # ALEPH TPC resolution coefficient
        n_events = len(reco_arrays)
        new_pmag = []
        new_px = []
        new_py = []
        new_pz = []
        for i in range(n_events):
            pm = np.asarray(reco_arrays["pmag"][i], dtype=np.float64)
            sigma_p = smear_frac * sigma_coeff * pm**2
            smeared = pm + rng.normal(0, 1, len(pm)) * sigma_p
            smeared = np.maximum(smeared, 0.01)  # floor
            scale = smeared / np.maximum(pm, 1e-10)
            new_pmag.append(smeared)
            new_px.append(np.asarray(reco_arrays["px"][i], dtype=np.float64) * scale)
            new_py.append(np.asarray(reco_arrays["py"][i], dtype=np.float64) * scale)
            new_pz.append(np.asarray(reco_arrays["pz"][i], dtype=np.float64) * scale)
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pmag), "pmag")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_px), "px")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_py), "py")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pz), "pz")

    elif var_name == "momentum_resolution_down":
        smear_frac = var_params.get("smear_fraction", -0.1)
        sigma_coeff = 0.6e-3
        n_events = len(reco_arrays)
        new_pmag = []
        new_px = []
        new_py = []
        new_pz = []
        for i in range(n_events):
            pm = np.asarray(reco_arrays["pmag"][i], dtype=np.float64)
            sigma_p = abs(smear_frac) * sigma_coeff * pm**2
            smeared = pm + rng.normal(0, 1, len(pm)) * sigma_p
            smeared = np.maximum(smeared, 0.01)
            scale = smeared / np.maximum(pm, 1e-10)
            new_pmag.append(smeared)
            new_px.append(np.asarray(reco_arrays["px"][i], dtype=np.float64) * scale)
            new_py.append(np.asarray(reco_arrays["py"][i], dtype=np.float64) * scale)
            new_pz.append(np.asarray(reco_arrays["pz"][i], dtype=np.float64) * scale)
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pmag), "pmag")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_px), "px")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_py), "py")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pz), "pz")

    elif var_name == "angular_resolution_up":
        # Smear angles by +1 mrad
        smear_rad = var_params.get("smear_mrad", 1.0) * 1e-3
        n_events = len(reco_arrays)
        new_px = []
        new_py = []
        new_pz = []
        for i in range(n_events):
            pm = np.asarray(reco_arrays["pmag"][i], dtype=np.float64)
            px_i = np.asarray(reco_arrays["px"][i], dtype=np.float64)
            py_i = np.asarray(reco_arrays["py"][i], dtype=np.float64)
            pz_i = np.asarray(reco_arrays["pz"][i], dtype=np.float64)
            theta = np.arctan2(np.sqrt(px_i**2 + py_i**2), pz_i)
            phi = np.arctan2(py_i, px_i)
            theta += rng.normal(0, smear_rad, len(theta))
            phi += rng.normal(0, smear_rad, len(phi))
            pt_new = pm * np.sin(theta)
            new_px.append(pt_new * np.cos(phi))
            new_py.append(pt_new * np.sin(phi))
            new_pz.append(pm * np.cos(theta))
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_px), "px")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_py), "py")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pz), "pz")

    elif var_name == "angular_resolution_down":
        smear_rad = var_params.get("smear_mrad", 1.0) * 1e-3
        n_events = len(reco_arrays)
        new_px = []
        new_py = []
        new_pz = []
        for i in range(n_events):
            pm = np.asarray(reco_arrays["pmag"][i], dtype=np.float64)
            px_i = np.asarray(reco_arrays["px"][i], dtype=np.float64)
            py_i = np.asarray(reco_arrays["py"][i], dtype=np.float64)
            pz_i = np.asarray(reco_arrays["pz"][i], dtype=np.float64)
            theta = np.arctan2(np.sqrt(px_i**2 + py_i**2), pz_i)
            phi = np.arctan2(py_i, px_i)
            theta += rng.normal(0, smear_rad, len(theta))
            phi += rng.normal(0, smear_rad, len(phi))
            pt_new = pm * np.sin(theta)
            new_px.append(pt_new * np.cos(phi))
            new_py.append(pt_new * np.sin(phi))
            new_pz.append(pm * np.cos(theta))
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_px), "px")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_py), "py")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_pz), "pz")

    elif var_name == "thrust_axis_smear":
        # Smear thrust axis direction
        smear_rad = var_params.get("smear_mrad", 2.0) * 1e-3
        n_events = len(reco_arrays)
        new_ttheta = []
        new_tphi = []
        for i in range(n_events):
            tt = float(reco_arrays["TTheta"][i])
            tp = float(reco_arrays["TPhi"][i])
            tt += rng.normal(0, smear_rad)
            tp += rng.normal(0, smear_rad)
            new_ttheta.append(tt)
            new_tphi.append(tp)
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_ttheta), "TTheta")
        reco_arrays = ak.with_field(reco_arrays, ak.Array(new_tphi), "TPhi")

    # Now process with standard selection
    # -- Reco --
    evt_mask = (reco_arrays["passesAll"] == True) & (reco_arrays["Thrust"] > 0.7)  # noqa: E712

    # Override thrust cut for event selection variations
    if var_name == "thrust_cut_low":
        evt_mask = (reco_arrays["passesAll"] == True) & (reco_arrays["Thrust"] > var_params["cut"])  # noqa: E712
    elif var_name == "thrust_cut_high":
        evt_mask = (reco_arrays["passesAll"] == True) & (reco_arrays["Thrust"] > var_params["cut"])  # noqa: E712

    sel = reco_arrays[evt_mask]

    # Track selection
    p_cut = var_params.get("p_cut", 0.2)
    d0_cut = var_params.get("d0_cut", 2.0)
    trk_mask = (
        (sel["pwflag"] == 0)
        & (sel["pmag"] > p_cut)
        & (np.abs(sel["d0"]) < d0_cut)
        & (np.abs(sel["z0"]) < 10.0)
    )

    nch_min = var_params.get("nch_min", 5)
    nch = ak.sum(trk_mask, axis=1)
    evt_mask2 = nch >= nch_min
    sel = sel[evt_mask2]
    trk_mask = trk_mask[evt_mask2]

    hp_reco, hm_reco, good_reco = split_hemispheres(sel, trk_mask)
    sel = sel[good_reco]

    h2d_reco, n_hemi_reco = process_events_lund(sel, hp_reco, hm_reco)

    # -- GenBefore (nominal, no variation) --
    sel_genb, trk_genb = _apply_genBefore_selection(genb_arrays)
    hp_genb, hm_genb, good_genb = split_hemispheres(sel_genb, trk_genb)
    sel_genb = sel_genb[good_genb]

    h2d_genb, n_hemi_genb = process_events_lund(sel_genb, hp_genb, hm_genb)

    return {
        "h2d_reco": h2d_reco,
        "h2d_genBefore": h2d_genb,
        "n_hemi_reco": n_hemi_reco,
        "n_hemi_genBefore": n_hemi_genb,
    }


def _apply_genBefore_selection(arrays):
    """GenBefore selection (no variation)."""
    trk_mask = (arrays["pwflag"] == 0) & (arrays["pmag"] > 0.2)
    nch = ak.sum(trk_mask, axis=1)
    evt_mask = nch >= 5
    return arrays[evt_mask], trk_mask[evt_mask]


def evaluate_systematic(mc_files, var_name, var_params, nominal_correction,
                        nominal_rho, n_hemi_genb_nominal, n_workers=6):
    """Evaluate one systematic source. Returns shift vector (density shift per bin)."""
    log.info("\n--- Systematic: %s ---", var_name)
    t0 = time.time()

    args_list = [(f, var_name, var_params) for f in mc_files]

    h2d_reco_var = np.zeros((NX, NY))
    h2d_genb_var = np.zeros((NX, NY))
    n_hemi_reco_var = 0
    n_hemi_genb_var = 0

    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = [executor.submit(process_mc_file_with_variation, a) for a in args_list]
        for future in as_completed(futures):
            r = future.result()
            h2d_reco_var += r["h2d_reco"]
            h2d_genb_var += r["h2d_genBefore"]
            n_hemi_reco_var += r["n_hemi_reco"]
            n_hemi_genb_var += r["n_hemi_genBefore"]

    # Apply nominal correction to varied reco
    corrected_var = h2d_reco_var * nominal_correction
    rho_var = corrected_var / (n_hemi_genb_nominal * BIN_AREA)

    # Shift = varied - nominal (bin-dependent)
    shift = rho_var.flatten() - nominal_rho.flatten()

    # Relative shift
    mask = nominal_rho.flatten() > 0
    rel_shift = np.zeros(N_BINS)
    rel_shift[mask] = shift[mask] / nominal_rho.flatten()[mask]

    dt = time.time() - t0
    log.info("  %s: max |rel shift| = %.4f, mean |rel shift| = %.4f (%.1fs)",
             var_name, np.max(np.abs(rel_shift[mask])) if mask.any() else 0,
             np.mean(np.abs(rel_shift[mask])) if mask.any() else 0, dt)

    return {
        "name": var_name,
        "shift": shift,
        "rel_shift": rel_shift,
        "rho_var": rho_var.flatten(),
        "n_hemi_reco": n_hemi_reco_var,
        "n_hemi_genb": n_hemi_genb_var,
    }


def main():
    log.info("=" * 70)
    log.info("Phase 4a Script 02: Systematic Uncertainty Evaluation")
    log.info("Session: Felix")
    log.info("=" * 70)

    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    log.info("Found %d MC files", len(mc_files))

    # Load nominal results
    corr_d = np.load("phase3_selection/outputs/correction_ingrid.npz")
    nominal_correction = corr_d["correction"]
    h2d_reco_nom = corr_d["h2d_reco"]
    h2d_genb_nom = corr_d["h2d_genBefore"]
    n_hemi_genb_nom = float(corr_d["n_hemi_genBefore"])

    # Nominal corrected density
    corrected_nom = h2d_reco_nom * nominal_correction
    rho_nom = corrected_nom / (n_hemi_genb_nom * BIN_AREA)

    # Also load IBU result if available
    try:
        exp_d = np.load(OUT_DIR / "expected_results_felix.npz")
        rho_ibu = exp_d["rho_unfolded_ibu"]
    except FileNotFoundError:
        log.info("IBU results not yet available, computing method difference later.")
        rho_ibu = None

    # Define all systematic variations
    variations = [
        # 1. Tracking efficiency
        ("tracking_efficiency_down", {"drop_fraction": 0.01}),

        # 2. Track momentum resolution
        ("momentum_resolution_up", {"smear_fraction": 0.1}),
        ("momentum_resolution_down", {"smear_fraction": -0.1}),

        # 3. Angular resolution
        ("angular_resolution_up", {"smear_mrad": 1.0}),
        ("angular_resolution_down", {"smear_mrad": 1.0}),

        # 4. Track selection: p threshold
        ("track_p_low", {"p_cut": 0.15}),
        ("track_p_high", {"p_cut": 0.25}),

        # 5. Track selection: d0 cut
        ("track_d0_low", {"d0_cut": 1.5}),
        ("track_d0_high", {"d0_cut": 2.5}),

        # 6. Event selection: thrust cut
        ("thrust_cut_low", {"cut": 0.6}),
        ("thrust_cut_high", {"cut": 0.8}),

        # 7. Event selection: N_ch_min
        ("nch_min_low", {"nch_min": 4}),
        ("nch_min_high", {"nch_min": 6}),

        # 8. Thrust-axis resolution
        ("thrust_axis_smear", {"smear_mrad": 2.0}),
    ]

    # Run all variations
    syst_results = {}
    for var_name, var_params in variations:
        result = evaluate_systematic(
            mc_files, var_name, var_params,
            nominal_correction, rho_nom, n_hemi_genb_nom,
            n_workers=6,
        )
        syst_results[var_name] = result

    # ================================================================
    # Gen-level systematics (reweighting-based)
    # ================================================================
    log.info("\n=== Gen-level systematics (reweighting) ===")

    x_centers = 0.5 * (X_EDGES[:-1] + X_EDGES[1:])
    y_centers = 0.5 * (Y_EDGES[:-1] + Y_EDGES[1:])
    x_range = X_EDGES[-1] - X_EDGES[0]
    y_range = Y_EDGES[-1] - Y_EDGES[0]
    x_mean = np.mean(x_centers)
    y_mean = np.mean(y_centers)

    # 9. MC model dependence: reweight gen to tilted shape, derive new correction
    log.info("\n--- MC model dependence (20%% 2D tilt) ---")
    weights_model = np.ones((NX, NY))
    for i in range(NX):
        for j in range(NY):
            wx = (x_centers[i] - x_mean) / x_range
            wy = (y_centers[j] - y_mean) / y_range
            weights_model[i, j] = 1.0 + 0.20 * (wx + wy) / np.sqrt(2.0)

    # Reweight genBefore -> new correction factors
    genb_rw = h2d_genb_nom * weights_model
    correction_rw = np.zeros_like(nominal_correction)
    mask_reco = h2d_reco_nom > 0
    correction_rw[mask_reco] = genb_rw[mask_reco] / h2d_reco_nom[mask_reco]

    # Apply reweighted correction to nominal reco
    corrected_model = h2d_reco_nom * correction_rw
    rho_model = corrected_model / (n_hemi_genb_nom * BIN_AREA)
    shift_model = rho_model.flatten() - rho_nom.flatten()
    mask = rho_nom.flatten() > 0
    rel_shift_model = np.zeros(N_BINS)
    rel_shift_model[mask] = shift_model[mask] / rho_nom.flatten()[mask]

    syst_results["mc_model_dependence"] = {
        "name": "mc_model_dependence",
        "shift": shift_model,
        "rel_shift": rel_shift_model,
        "rho_var": rho_model.flatten(),
        "description": "20% 2D correlated tilt of gen truth, new correction factors",
        "reweight_diagnostic": float(np.max(np.abs(weights_model))),
    }
    log.info("  MC model: max |rel shift| = %.4f, reweight max = %.3f",
             np.max(np.abs(rel_shift_model[mask])) if mask.any() else 0,
             np.max(np.abs(weights_model)))

    # 10. Heavy flavour composition: reweight b-fraction by +/-2%
    log.info("\n--- Heavy flavour composition ---")
    # bFlag is per-event. Process MC files to get per-event b-tagging info
    # and compute b-enriched/depleted Lund planes.
    # We use bFlag at reco level to identify b-events.
    # bFlag values: typically 1 = b-event, 0 = non-b-event

    # Process a subset to determine b-fraction and create reweighted histograms
    h2d_reco_b = np.zeros((NX, NY))
    h2d_reco_nonb = np.zeros((NX, NY))
    n_hemi_b = 0
    n_hemi_nonb = 0

    branches = ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                "Thrust", "TTheta", "TPhi", "passesAll", "bFlag"]

    log.info("  Processing MC files for b-fraction...")
    for filepath in mc_files[:10]:  # use first 10 files for speed
        with uproot.open(filepath) as f:
            reco_arrays = f["t"].arrays(branches)

        evt_mask = (reco_arrays["passesAll"] == True) & (reco_arrays["Thrust"] > 0.7)  # noqa: E712
        sel = reco_arrays[evt_mask]
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

        hp, hm, good = split_hemispheres(sel, trk_mask)
        sel = sel[good]

        bflag_raw = sel["bFlag"]
        if bflag_raw.ndim > 1:
            bflags = np.asarray(ak.firsts(bflag_raw))
        else:
            bflags = np.asarray(bflag_raw)

        n_events = len(sel)
        for i in range(n_events):
            is_b = bflags[i] == 1
            for hemi_mask in [hp, hm]:
                mask = hemi_mask[i]
                px_arr = np.asarray(sel["px"][i][mask], dtype=np.float64)
                py_arr = np.asarray(sel["py"][i][mask], dtype=np.float64)
                pz_arr = np.asarray(sel["pz"][i][mask], dtype=np.float64)
                pmag_arr = np.asarray(sel["pmag"][i][mask], dtype=np.float64)
                lx, ly = decluster_primary_chain(px_arr, py_arr, pz_arr, pmag_arr)
                if len(lx) > 0:
                    h, _, _ = np.histogram2d(lx, ly, bins=[X_EDGES, Y_EDGES])
                    if is_b:
                        h2d_reco_b += h
                        n_hemi_b += 1
                    else:
                        h2d_reco_nonb += h
                        n_hemi_nonb += 1
                else:
                    if is_b:
                        n_hemi_b += 1
                    else:
                        n_hemi_nonb += 1

    b_fraction = n_hemi_b / (n_hemi_b + n_hemi_nonb) if (n_hemi_b + n_hemi_nonb) > 0 else 0
    log.info("  b-fraction (reco): %.4f (%d b-hemi / %d total)",
             b_fraction, n_hemi_b, n_hemi_b + n_hemi_nonb)

    # Scale to full sample
    scale_b = (n_hemi_b + n_hemi_nonb) / n_hemi_b if n_hemi_b > 0 else 1
    scale_nonb = (n_hemi_b + n_hemi_nonb) / n_hemi_nonb if n_hemi_nonb > 0 else 1

    # b-fraction up by 2%: reweight b-events up, non-b down
    delta_fb = 0.02
    w_b_up = (b_fraction + delta_fb) / b_fraction if b_fraction > 0 else 1
    w_nonb_up = (1 - b_fraction - delta_fb) / (1 - b_fraction) if b_fraction < 1 else 1

    h2d_reco_hf_up = h2d_reco_b * w_b_up + h2d_reco_nonb * w_nonb_up
    # Rescale to match total of nominal (from these 10 files)
    h2d_reco_10files = h2d_reco_b + h2d_reco_nonb
    # The b-fraction variation shifts the density shape
    # Apply nominal correction to varied reco
    corrected_hf_up = h2d_reco_hf_up * nominal_correction
    rho_hf_up = corrected_hf_up / (n_hemi_genb_nom * BIN_AREA)
    # Nominal from these 10 files (for comparison)
    corrected_10 = h2d_reco_10files * nominal_correction
    rho_10 = corrected_10 / (n_hemi_genb_nom * BIN_AREA)

    shift_hf_up = rho_hf_up.flatten() - rho_10.flatten()
    rel_shift_hf_up = np.zeros(N_BINS)
    mask_10 = rho_10.flatten() > 0
    rel_shift_hf_up[mask_10] = shift_hf_up[mask_10] / rho_10.flatten()[mask_10]

    # b-fraction down
    w_b_down = (b_fraction - delta_fb) / b_fraction if b_fraction > 0 else 1
    w_nonb_down = (1 - b_fraction + delta_fb) / (1 - b_fraction) if b_fraction < 1 else 1
    h2d_reco_hf_down = h2d_reco_b * w_b_down + h2d_reco_nonb * w_nonb_down
    corrected_hf_down = h2d_reco_hf_down * nominal_correction
    rho_hf_down = corrected_hf_down / (n_hemi_genb_nom * BIN_AREA)
    shift_hf_down = rho_hf_down.flatten() - rho_10.flatten()
    rel_shift_hf_down = np.zeros(N_BINS)
    rel_shift_hf_down[mask_10] = shift_hf_down[mask_10] / rho_10.flatten()[mask_10]

    syst_results["heavy_flavour_up"] = {
        "name": "heavy_flavour_up",
        "shift": shift_hf_up,
        "rel_shift": rel_shift_hf_up,
        "b_fraction": float(b_fraction),
        "delta_fb": float(delta_fb),
    }
    syst_results["heavy_flavour_down"] = {
        "name": "heavy_flavour_down",
        "shift": shift_hf_down,
        "rel_shift": rel_shift_hf_down,
        "b_fraction": float(b_fraction),
        "delta_fb": float(delta_fb),
    }
    log.info("  HF up: max |rel shift| = %.4f", np.max(np.abs(rel_shift_hf_up[mask_10])) if mask_10.any() else 0)
    log.info("  HF down: max |rel shift| = %.4f", np.max(np.abs(rel_shift_hf_down[mask_10])) if mask_10.any() else 0)

    # 11. ISR modelling: compare with/without pwflag=-11 particles at gen-level
    log.info("\n--- ISR modelling ---")
    # At gen-level, ISR particles may have specific pwflag values.
    # We compare: genBefore with pwflag==0 (nominal) vs genBefore including pwflag={0,1,2}
    h2d_genb_isr = np.zeros((NX, NY))
    n_hemi_genb_isr = 0
    branches_gen_isr = ["px", "py", "pz", "pmag", "pwflag", "Thrust", "TTheta", "TPhi"]

    for filepath in mc_files[:10]:
        with uproot.open(filepath) as f:
            genb_arrays_isr = f["tgenBefore"].arrays(branches_gen_isr)

        # Include pwflag 0 and 1 (add non-prompt particles)
        trk_mask_isr = (genb_arrays_isr["pwflag"] <= 1) & (genb_arrays_isr["pmag"] > 0.2)
        nch_isr = ak.sum(trk_mask_isr, axis=1)
        evt_mask_isr = nch_isr >= 5
        sel_isr = genb_arrays_isr[evt_mask_isr]
        trk_isr = trk_mask_isr[evt_mask_isr]
        hp_isr, hm_isr, good_isr = split_hemispheres(sel_isr, trk_isr)
        sel_isr = sel_isr[good_isr]
        h2d_isr, n_h_isr = process_events_lund(sel_isr, hp_isr, hm_isr)
        h2d_genb_isr += h2d_isr
        n_hemi_genb_isr += n_h_isr

    # Compare to nominal genBefore (first 10 files)
    h2d_genb_10 = np.zeros((NX, NY))
    n_hemi_genb_10 = 0
    for filepath in mc_files[:10]:
        with uproot.open(filepath) as f:
            genb_arrays_nom = f["tgenBefore"].arrays(branches_gen_isr)
        sel_gb, trk_gb = _apply_genBefore_selection(genb_arrays_nom)
        hp_gb, hm_gb, good_gb = split_hemispheres(sel_gb, trk_gb)
        sel_gb = sel_gb[good_gb]
        h2d_gb, n_h_gb = process_events_lund(sel_gb, hp_gb, hm_gb)
        h2d_genb_10 += h2d_gb
        n_hemi_genb_10 += n_h_gb

    rho_isr = h2d_genb_isr.flatten() / (n_hemi_genb_isr * BIN_AREA) if n_hemi_genb_isr > 0 else np.zeros(N_BINS)
    rho_nom_gb10 = h2d_genb_10.flatten() / (n_hemi_genb_10 * BIN_AREA) if n_hemi_genb_10 > 0 else np.zeros(N_BINS)

    shift_isr = rho_isr - rho_nom_gb10
    rel_shift_isr = np.zeros(N_BINS)
    mask_gb10 = rho_nom_gb10 > 0
    rel_shift_isr[mask_gb10] = shift_isr[mask_gb10] / rho_nom_gb10[mask_gb10]

    syst_results["isr_modelling"] = {
        "name": "isr_modelling",
        "shift": shift_isr,
        "rel_shift": rel_shift_isr,
        "description": "pwflag<=1 vs pwflag==0 at genBefore level",
    }
    log.info("  ISR: max |rel shift| = %.4f", np.max(np.abs(rel_shift_isr[mask_gb10])) if mask_gb10.any() else 0)

    # 12. Unfolding method: bin-by-bin vs IBU
    if rho_ibu is not None:
        shift_method = rho_ibu.flatten() - rho_nom.flatten()
        rel_shift_method = np.zeros(N_BINS)
        mask_nom = rho_nom.flatten() > 0
        rel_shift_method[mask_nom] = shift_method[mask_nom] / rho_nom.flatten()[mask_nom]
        syst_results["unfolding_method"] = {
            "name": "unfolding_method",
            "shift": shift_method,
            "rel_shift": rel_shift_method,
            "description": "IBU - bin-by-bin difference",
        }
        log.info("  Method: max |rel shift| = %.4f", np.max(np.abs(rel_shift_method[mask_nom])) if mask_nom.any() else 0)

    # ================================================================
    # Save systematics results
    # ================================================================
    log.info("\n=== Saving systematics ===")

    # Symmetrize paired variations
    def symmetrize(name_up, name_down):
        if name_up in syst_results and name_down in syst_results:
            s_up = syst_results[name_up]["shift"]
            s_down = syst_results[name_down]["shift"]
            return 0.5 * (np.abs(s_up) + np.abs(s_down))
        elif name_up in syst_results:
            return np.abs(syst_results[name_up]["shift"])
        return np.zeros(N_BINS)

    # Group systematics
    syst_groups = {
        "tracking_efficiency": {
            "shift_up": syst_results["tracking_efficiency_down"]["shift"],
            "shift_down": -syst_results["tracking_efficiency_down"]["shift"],
            "symmetric": np.abs(syst_results["tracking_efficiency_down"]["shift"]),
        },
        "momentum_resolution": {
            "shift_up": syst_results["momentum_resolution_up"]["shift"],
            "shift_down": syst_results["momentum_resolution_down"]["shift"],
            "symmetric": symmetrize("momentum_resolution_up", "momentum_resolution_down"),
        },
        "angular_resolution": {
            "shift_up": syst_results["angular_resolution_up"]["shift"],
            "shift_down": syst_results["angular_resolution_down"]["shift"],
            "symmetric": symmetrize("angular_resolution_up", "angular_resolution_down"),
        },
        "track_p_threshold": {
            "shift_up": syst_results["track_p_high"]["shift"],
            "shift_down": syst_results["track_p_low"]["shift"],
            "symmetric": symmetrize("track_p_high", "track_p_low"),
        },
        "track_d0_cut": {
            "shift_up": syst_results["track_d0_high"]["shift"],
            "shift_down": syst_results["track_d0_low"]["shift"],
            "symmetric": symmetrize("track_d0_high", "track_d0_low"),
        },
        "thrust_cut": {
            "shift_up": syst_results["thrust_cut_high"]["shift"],
            "shift_down": syst_results["thrust_cut_low"]["shift"],
            "symmetric": symmetrize("thrust_cut_high", "thrust_cut_low"),
        },
        "nch_min": {
            "shift_up": syst_results["nch_min_high"]["shift"],
            "shift_down": syst_results["nch_min_low"]["shift"],
            "symmetric": symmetrize("nch_min_high", "nch_min_low"),
        },
        "thrust_axis_resolution": {
            "shift_up": syst_results["thrust_axis_smear"]["shift"],
            "shift_down": -syst_results["thrust_axis_smear"]["shift"],
            "symmetric": np.abs(syst_results["thrust_axis_smear"]["shift"]),
        },
        "mc_model_dependence": {
            "shift_up": syst_results["mc_model_dependence"]["shift"],
            "shift_down": -syst_results["mc_model_dependence"]["shift"],
            "symmetric": np.abs(syst_results["mc_model_dependence"]["shift"]),
        },
        "heavy_flavour": {
            "shift_up": syst_results["heavy_flavour_up"]["shift"],
            "shift_down": syst_results["heavy_flavour_down"]["shift"],
            "symmetric": symmetrize("heavy_flavour_up", "heavy_flavour_down"),
        },
        "isr_modelling": {
            "shift_up": syst_results["isr_modelling"]["shift"],
            "shift_down": -syst_results["isr_modelling"]["shift"],
            "symmetric": np.abs(syst_results["isr_modelling"]["shift"]),
        },
    }

    if "unfolding_method" in syst_results:
        syst_groups["unfolding_method"] = {
            "shift_up": syst_results["unfolding_method"]["shift"],
            "shift_down": -syst_results["unfolding_method"]["shift"],
            "symmetric": np.abs(syst_results["unfolding_method"]["shift"]),
        }

    # Save as npz
    save_dict = {"x_edges": X_EDGES, "y_edges": Y_EDGES, "rho_nominal": rho_nom.flatten()}
    for name, data in syst_groups.items():
        save_dict[f"{name}_up"] = data["shift_up"]
        save_dict[f"{name}_down"] = data["shift_down"]
        save_dict[f"{name}_sym"] = data["symmetric"]
    np.savez(OUT_DIR / "systematics_felix.npz", **save_dict)

    # Save JSON for analysis_note/results/
    results_dir = Path("analysis_note/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    syst_json = {
        "bin_edges_x": X_EDGES.tolist(),
        "bin_edges_y": Y_EDGES.tolist(),
        "sources": {},
    }
    for name, data in syst_groups.items():
        mask_nom = rho_nom.flatten() > 0
        syst_json["sources"][name] = {
            "shift_up": data["shift_up"].tolist(),
            "shift_down": data["shift_down"].tolist(),
            "symmetric_shift": data["symmetric"].tolist(),
            "max_abs_rel_shift": float(np.max(np.abs(data["symmetric"][mask_nom] / rho_nom.flatten()[mask_nom]))) if mask_nom.any() else 0,
            "mean_abs_rel_shift": float(np.mean(np.abs(data["symmetric"][mask_nom] / rho_nom.flatten()[mask_nom]))) if mask_nom.any() else 0,
        }

    with open(results_dir / "systematics.json", "w") as f:
        json.dump(syst_json, f, indent=2)

    log.info("\n=== SUMMARY ===")
    log.info("%-30s %10s %10s", "Source", "Max |rel|", "Mean |rel|")
    log.info("-" * 52)
    for name, data in sorted(syst_groups.items()):
        mask_nom = rho_nom.flatten() > 0
        if mask_nom.any():
            max_rel = np.max(np.abs(data["symmetric"][mask_nom] / rho_nom.flatten()[mask_nom]))
            mean_rel = np.mean(np.abs(data["symmetric"][mask_nom] / rho_nom.flatten()[mask_nom]))
        else:
            max_rel = 0
            mean_rel = 0
        log.info("%-30s %10.4f %10.4f", name, max_rel, mean_rel)

    log.info("\nSystematics saved.")


if __name__ == "__main__":
    main()
