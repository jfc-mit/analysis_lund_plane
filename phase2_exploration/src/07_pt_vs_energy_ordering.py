#!/usr/bin/env python3
"""Script 07: p_T vs energy ordering comparison at MC truth level.

Compares the two hardness orderings for the primary Lund plane.
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
FIG_DIR.mkdir(parents=True, exist_ok=True)

M_PI = 0.13957
N_EVENTS = 15000


def decluster_primary_with_ordering(jet, use_energy=False):
    """Follow the primary declustering chain.
    If use_energy=True, order by energy instead of p_T w.r.t. beam.
    """
    splittings = []
    current = jet
    while True:
        p1 = fastjet.PseudoJet()
        p2 = fastjet.PseudoJet()
        if not current.has_parents(p1, p2):
            break

        if use_energy:
            # Order by energy
            if p1.E() >= p2.E():
                harder, softer = p1, p2
            else:
                harder, softer = p2, p1
        else:
            # Order by p_T w.r.t. beam
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
    """Cluster one hemisphere and return (jet, cs) for declustering.
    Must return cs to keep ClusterSequence in scope.
    """
    if len(px) < 2:
        return None, None
    energy = np.sqrt(pmag**2 + M_PI**2)
    particles = [fastjet.PseudoJet(float(px[i]), float(py[i]), float(pz[i]), float(energy[i]))
                 for i in range(len(px))]
    jet_def = fastjet.JetDefinition(fastjet.ee_genkt_algorithm, 999.0, 0.0)
    cs = fastjet.ClusterSequence(particles, jet_def)
    jets = cs.inclusive_jets()
    if not jets:
        return None, None
    return jets[0], cs


def main():
    log.info("=" * 60)
    log.info("Script 07: p_T vs Energy Ordering Comparison")
    log.info("=" * 60)

    # Load MC gen-level events
    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    gen_arrays_list = []
    remaining = N_EVENTS
    for mf in mc_files:
        if remaining <= 0:
            break
        with uproot.open(mf) as f:
            tree = f["tgen"]
            take = min(remaining, tree.num_entries)
            gen = tree.arrays(
                ["px", "py", "pz", "pmag", "pwflag", "Thrust", "TTheta", "TPhi"],
                entry_stop=take,
            )
            gen_arrays_list.append(gen)
            remaining -= take

    gen = ak.concatenate(gen_arrays_list)
    log.info("Loaded %d gen-level events", len(gen))

    # Select charged particles with p > 0.2 GeV
    trk_mask = (gen["pwflag"] == 0) & (gen["pmag"] > 0.2)
    # Thrust cut
    evt_mask = gen["Thrust"] > 0.7
    gen = gen[evt_mask]
    trk_mask = trk_mask[evt_mask]

    # Build Lund planes with both orderings
    pt_x, pt_y = [], []
    e_x, e_y = [], []
    n_hemi = 0

    for i in range(len(gen)):
        mask = trk_mask[i]
        px_a = np.asarray(gen["px"][i][mask], dtype=np.float64)
        py_a = np.asarray(gen["py"][i][mask], dtype=np.float64)
        pz_a = np.asarray(gen["pz"][i][mask], dtype=np.float64)
        pmag_a = np.asarray(gen["pmag"][i][mask], dtype=np.float64)

        ttheta = float(gen["TTheta"][i])
        tphi = float(gen["TPhi"][i])
        tx = np.sin(ttheta) * np.cos(tphi)
        ty = np.sin(ttheta) * np.sin(tphi)
        tz = np.cos(ttheta)

        dot = px_a * tx + py_a * ty + pz_a * tz

        for sign_mask in [dot > 0, dot <= 0]:
            if np.sum(sign_mask) < 2:
                continue

            jet, cs = cluster_hemisphere(
                px_a[sign_mask], py_a[sign_mask],
                pz_a[sign_mask], pmag_a[sign_mask],
            )
            if jet is None:
                continue

            for lx, ly in decluster_primary_with_ordering(jet, use_energy=False):
                pt_x.append(lx)
                pt_y.append(ly)
            for lx, ly in decluster_primary_with_ordering(jet, use_energy=True):
                e_x.append(lx)
                e_y.append(ly)
            del cs  # Explicitly clean up
            n_hemi += 1

        if (i + 1) % 5000 == 0:
            log.info("  %d/%d events processed", i + 1, len(gen))

    log.info("Processed %d hemispheres", n_hemi)
    log.info("p_T ordering: %d splittings", len(pt_x))
    log.info("Energy ordering: %d splittings", len(e_x))

    pt_x, pt_y = np.array(pt_x), np.array(pt_y)
    e_x, e_y = np.array(e_x), np.array(e_y)

    # --- 2D comparison ---
    x_bins = np.linspace(0, 5, 26)
    y_bins = np.linspace(-3, 4, 36)
    dx = np.diff(x_bins)
    dy = np.diff(y_bins)

    h_pt, _, _ = np.histogram2d(pt_x, pt_y, bins=[x_bins, y_bins])
    h_e, _, _ = np.histogram2d(e_x, e_y, bins=[x_bins, y_bins])
    rho_pt = h_pt / n_hemi / np.outer(dx, dy)
    rho_e = h_e / n_hemi / np.outer(dx, dy)

    # Ratio plot
    ratio = np.where((rho_pt > 0) & (rho_e > 0), rho_e / rho_pt, 1.0)

    fig, ax = plt.subplots(figsize=(10, 10))
    im = ax.pcolormesh(x_bins, y_bins, ratio.T, cmap="coolwarm", shading="flat",
                       vmin=0.7, vmax=1.3)
    cax = mh.plot.append_axes(ax, size="5%", pad=0.05)
    fig.colorbar(im, cax=cax, label=r"$\rho_{\mathrm{energy}} / \rho_{p_T}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T / \mathrm{GeV})$")
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )
    fig.savefig(FIG_DIR / "hugo_pt_vs_energy_ordering_ratio.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_pt_vs_energy_ordering_ratio.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved p_T vs energy ordering ratio")

    # --- 1D projections comparison ---
    fig, (ax, rax) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    kt_proj_pt = np.sum(rho_pt, axis=0) * dx[0]
    kt_proj_e = np.sum(rho_e, axis=0) * dx[0]
    centers_y = 0.5 * (y_bins[:-1] + y_bins[1:])

    mh.histplot((kt_proj_pt, y_bins), ax=ax, label=r"$p_T$ ordering",
                color="C0", histtype="step")
    mh.histplot((kt_proj_e, y_bins), ax=ax, label="Energy ordering",
                color="C1", histtype="step")
    ax.set_ylabel(r"$\rho$ (integrated over $\ln 1/\Delta\theta$)")
    ax.legend(fontsize="x-small")
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(0, ymax * 1.4)
    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Simulation",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )

    rat = np.where(kt_proj_pt > 0, kt_proj_e / kt_proj_pt, 1.0)
    mh.histplot((rat, y_bins), ax=rax, color="k", histtype="step")
    rax.axhline(1.0, color="gray", linestyle="--", linewidth=1)
    rax.set_xlabel(r"$\ln(k_T / \mathrm{GeV})$")
    rax.set_ylabel("Energy / $p_T$", fontsize="x-small")
    rax.set_ylim(0.85, 1.15)

    fig.savefig(FIG_DIR / "hugo_pt_vs_energy_kt_projection.pdf",
                bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / "hugo_pt_vs_energy_kt_projection.png",
                bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved p_T vs energy 1D projection")

    # Quantify the difference
    valid = (kt_proj_pt > 0) & (kt_proj_e > 0)
    if np.any(valid):
        max_diff = np.max(np.abs(rat[valid] - 1.0))
        mean_diff = np.mean(np.abs(rat[valid] - 1.0))
        log.info("Max |ratio - 1|: %.4f", max_diff)
        log.info("Mean |ratio - 1|: %.4f", mean_diff)

    log.info("\np_T vs energy ordering comparison complete.")


if __name__ == "__main__":
    main()
