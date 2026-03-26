#!/usr/bin/env python3
"""Script 06: Binning optimization -- resolution, migration, and population studies.

Uses MC matched events (tgen and t) to study Lund plane resolution.
Session: Hugo
"""

import logging
from pathlib import Path

import awkward as ak
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import mplhep as mh
import numpy as np
import uproot
import fastjet
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

mh.style.use("CMS")

MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")
FIG_DIR = Path("phase2_exploration/outputs/figures")
OUT_DIR = Path("phase2_exploration/outputs")
FIG_DIR.mkdir(parents=True, exist_ok=True)

M_PI = 0.13957
N_MC_EVENTS = 20000  # Use 20k MC events for resolution studies


def decluster_primary(jet):
    """Follow the primary declustering chain. Returns list of (ln_inv_dtheta, ln_kt)."""
    splittings = []
    current = jet
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
            splittings.append((np.log(1.0 / delta_theta), np.log(kt)))
        current = harder
    return splittings


def cluster_hemisphere(px, py, pz, pmag):
    """Cluster one hemisphere and extract primary Lund plane."""
    if len(px) < 2:
        return []
    energy = np.sqrt(pmag**2 + M_PI**2)
    particles = [fastjet.PseudoJet(float(px[i]), float(py[i]), float(pz[i]), float(energy[i]))
                 for i in range(len(px))]
    jet_def = fastjet.JetDefinition(fastjet.ee_genkt_algorithm, 999.0, 0.0)
    cs = fastjet.ClusterSequence(particles, jet_def)
    jets = cs.inclusive_jets()
    if not jets:
        return []
    return decluster_primary(jets[0])


def load_mc_matched(n_events):
    """Load matched reco and gen MC events."""
    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    reco_arrays_list = []
    gen_arrays_list = []
    remaining = n_events
    for mf in mc_files:
        if remaining <= 0:
            break
        with uproot.open(mf) as f:
            tree_reco = f["t"]
            tree_gen = f["tgen"]
            take = min(remaining, tree_reco.num_entries)
            reco = tree_reco.arrays(
                ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
                 "Thrust", "TTheta", "TPhi", "passesAll"],
                entry_stop=take,
            )
            gen = tree_gen.arrays(
                ["px", "py", "pz", "pmag", "pwflag",
                 "Thrust", "TTheta", "TPhi"],
                entry_stop=take,
            )
            reco_arrays_list.append(reco)
            gen_arrays_list.append(gen)
            remaining -= take

    return ak.concatenate(reco_arrays_list), ak.concatenate(gen_arrays_list)


def process_events_for_binning(reco, gen):
    """Process matched events to get per-bin populations and resolutions."""
    # Event selection on reco
    evt_mask = (reco["passesAll"] == True) & (reco["Thrust"] > 0.7)  # noqa: E712
    reco_sel = reco[evt_mask]
    gen_sel = gen[evt_mask]

    # Track selection for reco
    reco_trk = (
        (reco_sel["pwflag"] == 0)
        & (reco_sel["pmag"] > 0.2)
        & (np.abs(reco_sel["d0"]) < 2.0)
        & (np.abs(reco_sel["z0"]) < 10.0)
    )
    # Gen-level: charged particles only (pwflag == 0), p > 0.2 GeV
    gen_trk = (gen_sel["pwflag"] == 0) & (gen_sel["pmag"] > 0.2)

    # Require N_ch >= 5 at reco level
    nch_reco = ak.sum(reco_trk, axis=1)
    good = nch_reco >= 5
    reco_sel = reco_sel[good]
    gen_sel = gen_sel[good]
    reco_trk = reco_trk[good]
    gen_trk = gen_trk[good]

    log.info("Processing %d matched events for binning study", len(reco_sel))

    # Build Lund planes at reco and gen level
    all_reco_x, all_reco_y = [], []
    all_gen_x, all_gen_y = [], []

    for i in range(len(reco_sel)):
        # Thrust axis from reco
        ttheta = float(reco_sel["TTheta"][i])
        tphi = float(reco_sel["TPhi"][i])
        tx_val = np.sin(ttheta) * np.cos(tphi)
        ty_val = np.sin(ttheta) * np.sin(tphi)
        tz_val = np.cos(ttheta)

        # Gen thrust axis
        gen_ttheta = float(gen_sel["TTheta"][i])
        gen_tphi = float(gen_sel["TPhi"][i])
        gen_tx = np.sin(gen_ttheta) * np.cos(gen_tphi)
        gen_ty = np.sin(gen_ttheta) * np.sin(gen_tphi)
        gen_tz = np.cos(gen_ttheta)

        for is_gen, (arrays, trk, tvec) in enumerate([
            (reco_sel, reco_trk, (tx_val, ty_val, tz_val)),
            (gen_sel, gen_trk, (gen_tx, gen_ty, gen_tz)),
        ]):
            mask = trk[i]
            px_a = np.asarray(arrays["px"][i][mask], dtype=np.float64)
            py_a = np.asarray(arrays["py"][i][mask], dtype=np.float64)
            pz_a = np.asarray(arrays["pz"][i][mask], dtype=np.float64)
            pmag_a = np.asarray(arrays["pmag"][i][mask], dtype=np.float64)

            dot = px_a * tvec[0] + py_a * tvec[1] + pz_a * tvec[2]
            for sign_mask in [dot > 0, dot <= 0]:
                if np.sum(sign_mask) < 2:
                    continue
                splittings = cluster_hemisphere(
                    px_a[sign_mask], py_a[sign_mask],
                    pz_a[sign_mask], pmag_a[sign_mask],
                )
                for (lx, ly) in splittings:
                    if is_gen == 0:
                        all_reco_x.append(lx)
                        all_reco_y.append(ly)
                    else:
                        all_gen_x.append(lx)
                        all_gen_y.append(ly)

        if (i + 1) % 5000 == 0:
            log.info("  %d/%d events processed", i + 1, len(reco_sel))

    return (np.array(all_reco_x), np.array(all_reco_y),
            np.array(all_gen_x), np.array(all_gen_y))


def main():
    log.info("=" * 60)
    log.info("Script 06: Binning Optimization")
    log.info("=" * 60)

    # Load MC
    log.info("Loading %d MC events...", N_MC_EVENTS)
    reco, gen = load_mc_matched(N_MC_EVENTS)

    # Process
    reco_x, reco_y, gen_x, gen_y = process_events_for_binning(reco, gen)
    log.info("Reco splittings: %d, Gen splittings: %d", len(reco_x), len(gen_x))

    # --- Bin population study (proposed 10x10 binning) ---
    x_bins_10 = np.linspace(0, 5, 11)
    y_bins_10 = np.linspace(-3, 4, 11)

    h_reco, _, _ = np.histogram2d(reco_x, reco_y, bins=[x_bins_10, y_bins_10])
    h_gen, _, _ = np.histogram2d(gen_x, gen_y, bins=[x_bins_10, y_bins_10])

    log.info("\n--- Bin Population (10x10 binning, reco) ---")
    log.info("Min bin count: %d", int(h_reco.min()))
    log.info("Max bin count: %d", int(h_reco.max()))
    log.info("Bins with < 100 entries: %d / %d", np.sum(h_reco < 100), h_reco.size)
    log.info("Bins with < 50 entries: %d / %d", np.sum(h_reco < 50), h_reco.size)
    log.info("Bins with 0 entries: %d / %d", np.sum(h_reco == 0), h_reco.size)

    log.info("\n--- Bin Population (10x10 binning, gen) ---")
    log.info("Min bin count: %d", int(h_gen.min()))
    log.info("Max bin count: %d", int(h_gen.max()))
    log.info("Bins with < 50 entries: %d / %d", np.sum(h_gen < 50), h_gen.size)

    # --- Migration fraction per bin ---
    # For each reco splitting, find its bin; for corresponding gen splitting, find its bin
    # Migration = fraction where reco bin != gen bin
    # Since splittings are not 1-1 matched, we use bin-level migration
    # Compute the 4D response: N(gen_i,gen_j -> reco_k,reco_l)
    n_x = len(x_bins_10) - 1
    n_y = len(y_bins_10) - 1
    n_bins = n_x * n_y

    # Use the bin populations to estimate diagonal fraction
    # For a proper migration study, we need matched splittings
    # Here we use a simpler approach: compare total reco vs gen in each bin
    migration_fraction = np.where(
        h_reco > 0,
        np.abs(h_reco - h_gen) / h_reco,
        0,
    )

    log.info("\n--- Migration Fraction (|reco - gen| / reco per bin) ---")
    log.info("Mean: %.3f", np.mean(migration_fraction[h_reco > 10]))
    log.info("Max: %.3f", np.max(migration_fraction[h_reco > 10]))
    log.info("Bins with migration > 30%%: %d / %d",
             np.sum(migration_fraction > 0.3), h_reco.size)

    # --- Plot: Bin population (reco) ---
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_bins_10, y_bins_10, h_reco.T, cmap="viridis",
                       shading="flat", norm=mcolors.LogNorm(vmin=1, vmax=h_reco.max()))
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Entries per bin (reco)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )
    fig.savefig(FIG_DIR / "hugo_bin_population_reco.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_bin_population_reco.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved bin population plot (reco)")

    # --- Plot: Migration fraction ---
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_bins_10, y_bins_10, migration_fraction.T, cmap="RdYlBu_r",
                       shading="flat", vmin=0, vmax=1)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$|N_{\mathrm{reco}} - N_{\mathrm{gen}}| / N_{\mathrm{reco}}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )
    fig.savefig(FIG_DIR / "hugo_migration_fraction.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_migration_fraction.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved migration fraction plot")

    # --- Plot: Resolution (1D distributions) ---
    # Compare gen and reco distributions as a diagnostic
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))

    ax1.hist(reco_x, bins=50, range=(0, 5), density=True, alpha=0.5, label="Reco")
    ax1.hist(gen_x, bins=50, range=(0, 5), density=True, alpha=0.5, label="Gen")
    ax1.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax1.set_ylabel("Normalized")
    ax1.legend(fontsize="x-small")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax1,
    )

    ax2.hist(reco_y, bins=50, range=(-3, 4), density=True, alpha=0.5, label="Reco")
    ax2.hist(gen_y, bins=50, range=(-3, 4), density=True, alpha=0.5, label="Gen")
    ax2.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax2.set_ylabel("Normalized")
    ax2.legend(fontsize="x-small")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax2,
    )

    fig.savefig(FIG_DIR / "hugo_reco_gen_1d_comparison.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_reco_gen_1d_comparison.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved reco/gen 1D comparison")

    # --- Correction factor map (gen_before/reco) ---
    # Note: this uses gen (post-selection), not genBefore. A placeholder for Phase 3.
    correction = np.where(h_reco > 10, h_gen / h_reco, 1.0)
    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_bins_10, y_bins_10, correction.T, cmap="coolwarm",
                       shading="flat", vmin=0.5, vmax=1.5)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$N_{\mathrm{gen}} / N_{\mathrm{reco}}$ (post-selection)")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )
    fig.savefig(FIG_DIR / "hugo_correction_factor_preview.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_correction_factor_preview.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved correction factor preview")

    log.info("\nBinning optimization complete.")


if __name__ == "__main__":
    main()
