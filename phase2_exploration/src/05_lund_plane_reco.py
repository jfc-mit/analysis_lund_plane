#!/usr/bin/env python3
"""Script 05: Reco-level Lund jet plane from data.

Builds the primary Lund plane at detector level using C/A clustering with FastJet.
Session: Hugo
"""

import logging
from pathlib import Path

import awkward as ak
import matplotlib.pyplot as plt
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

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
FIG_DIR = Path("phase2_exploration/outputs/figures")
OUT_DIR = Path("phase2_exploration/outputs")
FIG_DIR.mkdir(parents=True, exist_ok=True)

N_EVENTS = 100000  # Process 100k data events
M_PI = 0.13957  # Pion mass in GeV


def load_and_select(filepath, n_events, tree_name="t"):
    """Load events, apply event and track selection."""
    with uproot.open(filepath) as f:
        tree = f[tree_name]
        arrays = tree.arrays(
            ["px", "py", "pz", "pmag",
             "d0", "z0", "pwflag",
             "Thrust", "TTheta", "TPhi", "passesAll"],
            entry_stop=n_events,
        )

    # Event selection
    evt_mask = (arrays["passesAll"] == True) & (arrays["Thrust"] > 0.7)  # noqa: E712
    sel = arrays[evt_mask]

    # Track selection mask (per-particle)
    trk_mask = (
        (sel["pwflag"] == 0)
        & (sel["pmag"] > 0.2)
        & (np.abs(sel["d0"]) < 2.0)
        & (np.abs(sel["z0"]) < 10.0)
    )

    # Require N_ch >= 5
    nch = ak.sum(trk_mask, axis=1)
    evt_mask2 = nch >= 5
    sel = sel[evt_mask2]
    trk_mask = trk_mask[evt_mask2]

    return sel, trk_mask


def decluster_primary(jet):
    """Follow the primary declustering chain using has_parents.
    Returns list of (ln_1_over_dtheta, ln_kt).
    Uses p_T w.r.t. beam as hardness variable.
    """
    splittings = []
    current = jet
    while True:
        p1 = fastjet.PseudoJet()
        p2 = fastjet.PseudoJet()
        if not current.has_parents(p1, p2):
            break

        # Determine harder subjet by p_T w.r.t. beam
        pt1 = np.sqrt(p1.px()**2 + p1.py()**2)
        pt2 = np.sqrt(p2.px()**2 + p2.py()**2)
        if pt1 >= pt2:
            harder, softer = p1, p2
        else:
            harder, softer = p2, p1

        # Compute opening angle
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
            ln_inv_dtheta = np.log(1.0 / delta_theta)
            ln_kt = np.log(kt)
            splittings.append((ln_inv_dtheta, ln_kt))

        # Follow the harder branch
        current = harder

    return splittings


def process_hemisphere(px, py, pz, pmag):
    """Cluster one hemisphere with C/A and extract primary Lund plane."""
    if len(px) < 2:
        return []

    # Build PseudoJets with pion mass assumption
    energy = np.sqrt(pmag**2 + M_PI**2)
    particles = []
    for i in range(len(px)):
        particles.append(fastjet.PseudoJet(float(px[i]), float(py[i]),
                                           float(pz[i]), float(energy[i])))

    # C/A clustering for e+e-
    jet_def = fastjet.JetDefinition(fastjet.ee_genkt_algorithm, 999.0, 0.0)
    cs = fastjet.ClusterSequence(particles, jet_def)
    jets = cs.inclusive_jets()

    if len(jets) == 0:
        return []

    # Decluster the single hemisphere jet
    return decluster_primary(jets[0])


def main():
    log.info("=" * 60)
    log.info("Script 05: Reco-level Lund Jet Plane")
    log.info("=" * 60)

    all_lund_x = []
    all_lund_y = []
    n_hemispheres = 0
    n_splittings_total = 0

    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    remaining = N_EVENTS
    for df in data_files:
        if remaining <= 0:
            break
        log.info("Processing %s (up to %d events)...", df.name, remaining)
        sel, trk_mask = load_and_select(df, remaining)

        # Split into hemispheres using thrust axis
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
        sel = sel[good]
        hemi_plus = hemi_plus[good]
        hemi_minus = hemi_minus[good]

        n_events = len(sel)
        log.info("  %d events pass all cuts", n_events)
        remaining -= n_events

        # Process each event
        for i in range(n_events):
            for hemi_mask in [hemi_plus, hemi_minus]:
                mask = hemi_mask[i]
                px_arr = np.asarray(sel["px"][i][mask], dtype=np.float64)
                py_arr = np.asarray(sel["py"][i][mask], dtype=np.float64)
                pz_arr = np.asarray(sel["pz"][i][mask], dtype=np.float64)
                pmag_arr = np.asarray(sel["pmag"][i][mask], dtype=np.float64)

                splittings = process_hemisphere(px_arr, py_arr, pz_arr, pmag_arr)
                for (lx, ly) in splittings:
                    all_lund_x.append(lx)
                    all_lund_y.append(ly)
                n_splittings_total += len(splittings)
                n_hemispheres += 1

            if (i + 1) % 20000 == 0:
                log.info("    %d/%d events done (%d hemi, %d splittings)",
                         i + 1, n_events, n_hemispheres, n_splittings_total)

    log.info("Total: %d hemispheres, %d splittings", n_hemispheres, n_splittings_total)
    log.info("Average splittings per hemisphere: %.2f",
             n_splittings_total / max(n_hemispheres, 1))

    lund_x = np.array(all_lund_x)
    lund_y = np.array(all_lund_y)

    # --- Plot 1: 2D Lund plane density ---
    x_bins = np.linspace(0, 5, 26)
    y_bins = np.linspace(-3, 4, 36)

    h2d, xedges, yedges = np.histogram2d(lund_x, lund_y, bins=[x_bins, y_bins])
    dx = np.diff(x_bins)
    dy = np.diff(y_bins)
    rho = h2d / n_hemispheres / np.outer(dx, dy)

    fig, ax = plt.subplots(figsize=(10, 10))
    # Mask zero bins for log color scale
    rho_plot = np.ma.masked_where(rho <= 0, rho)
    import matplotlib.colors as mcolors
    im = ax.pcolormesh(xedges, yedges, rho_plot.T, cmap="inferno", shading="flat",
                       norm=mcolors.LogNorm(vmin=1e-3, vmax=rho_plot.max()))
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "hugo_lund_plane_reco_data.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_lund_plane_reco_data.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved reco-level Lund plane (data)")

    # --- Plot 2: ln(k_T) projection ---
    fig, ax = plt.subplots(figsize=(10, 10))
    kt_proj = np.sum(rho, axis=0) * dx[0]
    centers_y = 0.5 * (y_bins[:-1] + y_bins[1:])
    mh.histplot(
        (kt_proj, y_bins),
        ax=ax, label="Data (reco)", color="k",
        histtype="errorbar", yerr=np.sqrt(np.sum(h2d, axis=0)) / n_hemispheres / dy,
    )
    # LO prediction lines
    alpha_s_mz = 0.118
    C_F = 4.0 / 3.0
    rho_lo_all = 2.0 * alpha_s_mz * C_F / np.pi
    rho_lo_charged = 0.67 * rho_lo_all
    ax.axhline(rho_lo_all, color="red", linestyle="--", linewidth=1,
               label=r"LO all-particle $\approx %.3f$" % rho_lo_all)
    ax.axhline(rho_lo_charged, color="blue", linestyle=":", linewidth=1,
               label=r"LO charged $\approx %.3f$" % rho_lo_charged)
    ax.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    ax.set_ylabel(r"$\rho$ (integrated over $\ln 1/\Delta\theta$)")
    ax.legend(fontsize="x-small")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax * 1.4)
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "hugo_lund_kt_projection.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_lund_kt_projection.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved k_T projection")

    # --- Plot 3: ln(1/Delta_theta) projection ---
    fig, ax = plt.subplots(figsize=(10, 10))
    dtheta_proj = np.sum(rho, axis=1) * dy[0]
    mh.histplot(
        (dtheta_proj, x_bins),
        ax=ax, label="Data (reco)", color="k",
        histtype="errorbar", yerr=np.sqrt(np.sum(h2d, axis=1)) / n_hemispheres / dx,
    )
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\rho$ (integrated over $\ln k_T$)")
    ax.legend(fontsize="x-small")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax * 1.4)
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / "hugo_lund_dtheta_projection.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_lund_dtheta_projection.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved Delta_theta projection")

    # Save raw arrays for further analysis
    np.savez(
        OUT_DIR / "lund_reco_data_hugo.npz",
        lund_x=lund_x,
        lund_y=lund_y,
        n_hemispheres=n_hemispheres,
    )
    log.info("Saved raw Lund plane arrays to lund_reco_data_hugo.npz")

    log.info("\nLund plane construction complete.")


if __name__ == "__main__":
    main()
