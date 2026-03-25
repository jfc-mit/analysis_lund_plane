#!/usr/bin/env python3
"""Script 03: Data/MC kinematic comparisons with ratio panels.

Produces comparison plots for all kinematic variables entering the Lund plane.
Session: Hugo
"""

import logging
from pathlib import Path

import awkward as ak
import hist
import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
import uproot
# mpl_magic not available in this mplhep version; use manual y-axis extension
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

mh.style.use("CMS")

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")
FIG_DIR = Path("phase2_exploration/outputs/figures")
FIG_DIR.mkdir(parents=True, exist_ok=True)

N_DATA = 50000
N_MC = 50000


def load_data(n_events):
    """Load data tracks with selection applied."""
    data_file = sorted(DATA_DIR.glob("LEP1Data*.root"))[0]
    with uproot.open(data_file) as f:
        tree = f["t"]
        arrays = tree.arrays(
            ["px", "py", "pz", "pt", "pmag", "theta", "phi", "mass",
             "charge", "d0", "z0", "pwflag",
             "Thrust", "Thrust_charged", "nChargedHadrons",
             "passesAll", "TTheta", "TPhi"],
            entry_stop=n_events,
        )
    return arrays


def load_mc(n_events):
    """Load MC reco tracks with selection applied."""
    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    all_arrays = []
    remaining = n_events
    for mf in mc_files:
        if remaining <= 0:
            break
        with uproot.open(mf) as f:
            tree = f["t"]
            take = min(remaining, tree.num_entries)
            arrays = tree.arrays(
                ["px", "py", "pz", "pt", "pmag", "theta", "phi", "mass",
                 "charge", "d0", "z0", "pwflag",
                 "Thrust", "Thrust_charged", "nChargedHadrons",
                 "passesAll", "TTheta", "TPhi"],
                entry_stop=take,
            )
            all_arrays.append(arrays)
            remaining -= take
    return ak.concatenate(all_arrays)


def select_tracks(arrays):
    """Apply track selection: pwflag==0, p > 0.2 GeV, |d0| < 2 cm, |z0| < 10 cm."""
    mask = (
        (arrays["pwflag"] == 0)
        & (arrays["pmag"] > 0.2)
        & (np.abs(arrays["d0"]) < 2.0)
        & (np.abs(arrays["z0"]) < 10.0)
    )
    return mask


def select_events(arrays):
    """Apply event selection: passesAll."""
    return arrays["passesAll"] == True  # noqa: E712


def compute_nch(arrays, track_mask):
    """Compute N_ch per event after track cuts."""
    return ak.sum(track_mask, axis=1)


def compute_hemisphere_mult(arrays, track_mask):
    """Compute hemisphere multiplicity using thrust axis."""
    # Get thrust axis direction
    ttheta = arrays["TTheta"]
    tphi = arrays["TPhi"]
    # Thrust axis unit vector
    tx = np.sin(ttheta) * np.cos(tphi)
    ty = np.sin(ttheta) * np.sin(tphi)
    tz = np.cos(ttheta)

    # Dot product of each track with thrust axis
    dot = arrays["px"] * tx + arrays["py"] * ty + arrays["pz"] * tz
    hemi_plus = track_mask & (dot > 0)
    hemi_minus = track_mask & (dot <= 0)
    n_plus = ak.sum(hemi_plus, axis=1)
    n_minus = ak.sum(hemi_minus, axis=1)
    # Return the minimum hemisphere multiplicity per event
    return ak.min(ak.concatenate([n_plus[:, np.newaxis], n_minus[:, np.newaxis]], axis=1), axis=1)


def make_ratio_plot(
    data_vals, mc_vals, bins, xlabel, figname,
    data_label="Data", mc_label="MC (PYTHIA 6.1)",
    logy=False, density=True,
):
    """Make a data/MC comparison plot with ratio panel."""
    fig, (ax, rax) = plt.subplots(
        2, 1, figsize=(10, 10),
        gridspec_kw={"height_ratios": [3, 1]},
        sharex=True,
    )
    fig.subplots_adjust(hspace=0)

    # Fill histograms
    h_data = hist.Hist(hist.axis.Variable(bins))
    h_mc = hist.Hist(hist.axis.Variable(bins))
    h_data.fill(np.asarray(data_vals))
    h_mc.fill(np.asarray(mc_vals))

    if density:
        # Normalize to unit area
        data_sum = float(h_data.sum())
        mc_sum = float(h_mc.sum())
        if data_sum > 0:
            h_data_norm = h_data.copy()
            h_data_norm.view()[:] = h_data.view() / (data_sum * np.diff(bins))
        if mc_sum > 0:
            h_mc_norm = h_mc.copy()
            h_mc_norm.view()[:] = h_mc.view() / (mc_sum * np.diff(bins))

        # Data errors (Poisson)
        data_counts = h_data.values()
        data_err = np.sqrt(data_counts) / (data_sum * np.diff(bins))
        mc_err = np.sqrt(h_mc.values()) / (mc_sum * np.diff(bins))

        # MC as filled histogram
        mh.histplot(h_mc_norm, ax=ax, label=mc_label, histtype="fill",
                    color="C0", alpha=0.5)
        # Data as errorbar
        centers = 0.5 * (bins[:-1] + bins[1:])
        ax.errorbar(centers, h_data_norm.values(), yerr=data_err,
                    fmt="ko", markersize=4, label=data_label, zorder=5)

        # Ratio panel
        ratio = np.where(
            h_mc_norm.values() > 0,
            h_data_norm.values() / h_mc_norm.values(),
            1.0,
        )
        ratio_err = np.where(
            h_mc_norm.values() > 0,
            data_err / h_mc_norm.values(),
            0.0,
        )
    else:
        # Not density -- use raw counts scaled to data
        data_sum = float(h_data.sum())
        mc_sum = float(h_mc.sum())
        scale = data_sum / mc_sum if mc_sum > 0 else 1.0

        h_mc_scaled = h_mc.copy()
        h_mc_scaled.view()[:] = h_mc.view() * scale

        mh.histplot(h_mc_scaled, ax=ax, label=mc_label, histtype="fill",
                    color="C0", alpha=0.5)
        centers = 0.5 * (bins[:-1] + bins[1:])
        data_err = np.sqrt(h_data.values())
        ax.errorbar(centers, h_data.values(), yerr=data_err,
                    fmt="ko", markersize=4, label=data_label, zorder=5)

        ratio = np.where(
            h_mc_scaled.values() > 0,
            h_data.values() / h_mc_scaled.values(),
            1.0,
        )
        ratio_err = np.where(
            h_mc_scaled.values() > 0,
            data_err / h_mc_scaled.values(),
            0.0,
        )

    rax.errorbar(centers, ratio, yerr=ratio_err, fmt="ko", markersize=4)
    rax.axhline(1.0, color="gray", linestyle="--", linewidth=1)
    rax.set_ylim(0.85, 1.15)
    rax.set_ylabel("Data / MC", fontsize="x-small")
    rax.set_xlabel(xlabel)

    if logy:
        ax.set_yscale("log")

    ax.set_ylabel("Normalized" if density else "Events / bin")
    ax.legend(fontsize="x-small")
    # Extend y-axis to accommodate legend
    ymin, ymax = ax.get_ylim()
    if not logy:
        ax.set_ylim(ymin, ymax * 1.35)
    else:
        ax.set_ylim(ymin, ymax * 5)

    mh.label.exp_label(
        exp="ALEPH", data=True,
        llabel="Open Data",
        rlabel=r"$\sqrt{s} = 91.2$ GeV",
        loc=0, ax=ax,
    )

    fig.savefig(FIG_DIR / f"{figname}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / f"{figname}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("Saved %s", figname)


def main():
    log.info("=" * 60)
    log.info("Script 03: Data/MC Comparisons")
    log.info("=" * 60)

    # Load data and MC
    log.info("Loading data (%d events)...", N_DATA)
    data = load_data(N_DATA)
    log.info("Loading MC (%d events)...", N_MC)
    mc = load_mc(N_MC)

    # Apply event selection
    data_evt_mask = select_events(data)
    mc_evt_mask = select_events(mc)
    data_sel = data[data_evt_mask]
    mc_sel = mc[mc_evt_mask]
    log.info("Data events after passesAll: %d", len(data_sel))
    log.info("MC events after passesAll: %d", len(mc_sel))

    # Apply track selection
    data_trk_mask = select_tracks(data_sel)
    mc_trk_mask = select_tracks(mc_sel)

    # Get flat track arrays
    data_pmag = np.asarray(ak.flatten(data_sel["pmag"][data_trk_mask]))
    mc_pmag = np.asarray(ak.flatten(mc_sel["pmag"][mc_trk_mask]))

    data_theta = np.asarray(ak.flatten(data_sel["theta"][data_trk_mask]))
    mc_theta = np.asarray(ak.flatten(mc_sel["theta"][mc_trk_mask]))

    data_phi = np.asarray(ak.flatten(data_sel["phi"][data_trk_mask]))
    mc_phi = np.asarray(ak.flatten(mc_sel["phi"][mc_trk_mask]))

    data_pt = np.asarray(ak.flatten(data_sel["pt"][data_trk_mask]))
    mc_pt = np.asarray(ak.flatten(mc_sel["pt"][mc_trk_mask]))

    # 1. Track momentum
    make_ratio_plot(
        data_pmag, mc_pmag,
        np.linspace(0.2, 10, 50),
        r"$p$ [GeV/$c$]", "hugo_pmag_data_mc",
    )

    # 2. Track momentum (log scale, wide range)
    make_ratio_plot(
        data_pmag, mc_pmag,
        np.logspace(np.log10(0.2), np.log10(50), 50),
        r"$p$ [GeV/$c$]", "hugo_pmag_log_data_mc",
        logy=True,
    )

    # 3. Track theta
    make_ratio_plot(
        data_theta, mc_theta,
        np.linspace(0.3, 2.85, 40),
        r"$\theta$ [rad]", "hugo_theta_data_mc",
    )

    # 4. Track phi
    make_ratio_plot(
        data_phi, mc_phi,
        np.linspace(-np.pi, np.pi, 40),
        r"$\phi$ [rad]", "hugo_phi_data_mc",
    )

    # 5. Track pT
    make_ratio_plot(
        data_pt, mc_pt,
        np.linspace(0.2, 8, 50),
        r"$p_T$ [GeV/$c$]", "hugo_pt_data_mc",
    )

    # 6. Thrust
    data_thrust = np.asarray(data_sel["Thrust"])
    mc_thrust = np.asarray(mc_sel["Thrust"])
    make_ratio_plot(
        data_thrust, mc_thrust,
        np.linspace(0.6, 1.0, 50),
        "Thrust", "hugo_thrust_data_mc",
    )

    # 7. N_ch per event
    data_nch = np.asarray(compute_nch(data_sel, data_trk_mask))
    mc_nch = np.asarray(compute_nch(mc_sel, mc_trk_mask))
    make_ratio_plot(
        data_nch, mc_nch,
        np.arange(0, 50, 1),
        r"$N_{\mathrm{ch}}$", "hugo_nch_data_mc",
        density=False,
    )

    # 8. Hemisphere multiplicity (minimum)
    data_hemi = np.asarray(compute_hemisphere_mult(data_sel, data_trk_mask))
    mc_hemi = np.asarray(compute_hemisphere_mult(mc_sel, mc_trk_mask))
    make_ratio_plot(
        data_hemi, mc_hemi,
        np.arange(0, 25, 1),
        r"$N_{\mathrm{ch}}^{\mathrm{hemi,min}}$", "hugo_hemi_mult_data_mc",
        density=False,
    )

    # 9. Thrust_charged (separate from energy-flow thrust)
    data_thrust_ch = np.asarray(data_sel["Thrust_charged"])
    mc_thrust_ch = np.asarray(mc_sel["Thrust_charged"])
    make_ratio_plot(
        data_thrust_ch, mc_thrust_ch,
        np.linspace(0.6, 1.0, 50),
        r"Thrust$_{\mathrm{charged}}$", "hugo_thrust_charged_data_mc",
    )

    log.info("\nAll data/MC comparison plots complete.")


if __name__ == "__main__":
    main()
