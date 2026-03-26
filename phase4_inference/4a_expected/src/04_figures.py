#!/usr/bin/env python3
"""Phase 4a Script 04: Generate all figures and JSON outputs.

Produces all Phase 4a figures and machine-readable results.

Session: Felix | Phase 4a
"""

import json
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import mplhep as mh
import numpy as np
from rich.logging import RichHandler

mh.style.use("CMS")

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"
FIG_DIR = OUT_DIR / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

X_EDGES = np.linspace(0, 5, 11)
Y_EDGES = np.linspace(-3, 4, 11)
NX = len(X_EDGES) - 1
NY = len(Y_EDGES) - 1
N_BINS = NX * NY
BIN_AREA = (X_EDGES[1] - X_EDGES[0]) * (Y_EDGES[1] - Y_EDGES[0])


def save_fig(fig, name):
    """Save figure as PDF and PNG."""
    fig.savefig(FIG_DIR / f"{name}.pdf", bbox_inches="tight", dpi=200, transparent=True)
    fig.savefig(FIG_DIR / f"{name}.png", bbox_inches="tight", dpi=200, transparent=True)
    plt.close(fig)
    log.info("  Saved %s", name)


def main():
    log.info("=" * 70)
    log.info("Phase 4a Script 04: Figures and JSON Outputs")
    log.info("Session: Felix")
    log.info("=" * 70)

    # Load data
    exp = np.load(OUT_DIR / "expected_results_felix.npz")
    resp = np.load(OUT_DIR / "response_matrix_felix.npz")

    rho_bbb = exp["rho_corrected_bbb"]
    rho_ibu = exp["rho_unfolded_ibu"]
    rho_truth = exp["rho_truth"]
    correction_a = exp["correction_a"]
    corrected_b_bbb = exp["corrected_b_bbb"]
    truth_b = exp["truth_b"]
    unfolded_b_ibu = exp["unfolded_b_ibu"]
    pulls_split_bbb = exp["pulls_split_bbb"]
    pulls_split_ibu = exp["pulls_split_ibu"]

    response = resp["response"]
    diag_frac = resp["diag_fraction"]

    # Load correction from Phase 3
    corr_d = np.load("phase3_selection/outputs/correction_ingrid.npz")
    correction_p3 = corr_d["correction"]

    # Load covariance if available
    try:
        cov_d = np.load(OUT_DIR / "covariance_felix.npz")
        cov_total = cov_d["cov_total"]
        corr_matrix = cov_d["corr_matrix"]
        total_err = cov_d["total_err"]
        stat_err = cov_d["stat_err"]
        has_cov = True
    except FileNotFoundError:
        log.info("Covariance not yet available; skipping covariance-dependent plots.")
        has_cov = False

    # Load systematics if available
    try:
        syst_d = np.load(OUT_DIR / "systematics_felix.npz")
        rho_nominal_syst = syst_d["rho_nominal"]
        has_syst = True
    except FileNotFoundError:
        log.info("Systematics not yet available; skipping systematic plots.")
        has_syst = False

    # Load validation JSON
    results_dir = Path("analysis_note/results")
    try:
        with open(results_dir / "validation.json") as f:
            validation = json.load(f)
        has_validation = True
    except FileNotFoundError:
        has_validation = False

    x_centers = 0.5 * (X_EDGES[:-1] + X_EDGES[1:])
    y_centers = 0.5 * (Y_EDGES[:-1] + Y_EDGES[1:])

    # ================================================================
    # Figure 1: Corrected Lund plane (2D, central result)
    # ================================================================
    log.info("\n--- Figure 1: Corrected Lund plane (bin-by-bin) ---")
    fig, ax = plt.subplots(figsize=(10, 10))
    rho_plot = rho_bbb.copy()
    rho_plot[rho_plot == 0] = np.nan
    im = ax.pcolormesh(X_EDGES, Y_EDGES, rho_plot.T, cmap="viridis", shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T/\mathrm{GeV})$")
    mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
    save_fig(fig, "felix_lund_plane_corrected_bbb")

    # Same for IBU
    fig, ax = plt.subplots(figsize=(10, 10))
    rho_plot_ibu = rho_ibu.copy()
    rho_plot_ibu[rho_plot_ibu == 0] = np.nan
    im = ax.pcolormesh(X_EDGES, Y_EDGES, rho_plot_ibu.T, cmap="viridis", shading="flat")
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$\rho(\ln 1/\Delta\theta, \ln k_T)$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T/\mathrm{GeV})$")
    mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation (IBU)",
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
    save_fig(fig, "felix_lund_plane_corrected_ibu")

    # ================================================================
    # Figure 2: Correction factor map
    # ================================================================
    log.info("\n--- Figure 2: Correction factor map ---")
    fig, ax = plt.subplots(figsize=(10, 10))
    c_plot = correction_p3.copy()
    c_plot[c_plot == 0] = np.nan
    im = ax.pcolormesh(X_EDGES, Y_EDGES, c_plot.T, cmap="RdYlBu_r", shading="flat",
                       vmin=0.8, vmax=3.0)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label=r"$C(i,j) = N_{\mathrm{genBefore}} / N_{\mathrm{reco}}$")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T/\mathrm{GeV})$")
    mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
    save_fig(fig, "felix_correction_factor_map")

    # ================================================================
    # Figure 3: Split-sample closure (bin-by-bin)
    # ================================================================
    log.info("\n--- Figure 3: Split-sample closure ---")

    # 1D projections with ratio
    for proj_axis, proj_name, centers, edges, xlabel in [
        (1, "kt", y_centers, Y_EDGES, r"$\ln(k_T/\mathrm{GeV})$"),
        (0, "dtheta", x_centers, X_EDGES, r"$\ln(1/\Delta\theta)$"),
    ]:
        corrected_1d = np.nansum(corrected_b_bbb, axis=proj_axis)
        truth_1d = np.nansum(truth_b, axis=proj_axis)
        n_bins_1d = len(centers)

        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [3, 1]},
            sharex=True,
        )
        fig.subplots_adjust(hspace=0)

        # Normalize to density
        bin_w = np.diff(edges)
        other_width = np.sum(np.diff(Y_EDGES if proj_axis == 1 else X_EDGES))

        # Main panel
        err_truth = np.sqrt(truth_1d)
        err_corr = np.sqrt(corrected_1d)

        ax_main.errorbar(centers, truth_1d, yerr=err_truth,
                         fmt="o", color="black", label="MC genBefore truth (half B)",
                         markersize=4, zorder=5)
        ax_main.errorbar(centers + 0.02, corrected_1d, yerr=err_corr,
                         fmt="s", color="tab:red", label="Corrected reco (half A corr)",
                         markersize=4, zorder=4)
        ax_main.set_ylabel("Splittings")
        ax_main.legend(fontsize="x-small")
        mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                           rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax_main, loc=0)

        # Ratio panel
        ratio = np.ones_like(corrected_1d)
        ratio_err = np.zeros_like(corrected_1d)
        mask_t = truth_1d > 0
        ratio[mask_t] = corrected_1d[mask_t] / truth_1d[mask_t]
        ratio_err[mask_t] = err_corr[mask_t] / truth_1d[mask_t]

        ax_ratio.errorbar(centers, ratio, yerr=ratio_err, fmt="s",
                          color="tab:red", markersize=4)
        ax_ratio.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
        ax_ratio.set_ylim(0.85, 1.15)
        ax_ratio.set_ylabel("Corrected / Truth")
        ax_ratio.set_xlabel(xlabel)

        save_fig(fig, f"felix_split_closure_bbb_{proj_name}")

    # IBU split closure
    for proj_axis, proj_name, centers, edges, xlabel in [
        (1, "kt", y_centers, Y_EDGES, r"$\ln(k_T/\mathrm{GeV})$"),
        (0, "dtheta", x_centers, X_EDGES, r"$\ln(1/\Delta\theta)$"),
    ]:
        unfolded_1d = np.nansum(unfolded_b_ibu, axis=proj_axis)
        truth_1d = np.nansum(truth_b, axis=proj_axis)

        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [3, 1]},
            sharex=True,
        )
        fig.subplots_adjust(hspace=0)

        err_truth = np.sqrt(truth_1d)
        err_unf = np.sqrt(np.abs(unfolded_1d))

        ax_main.errorbar(centers, truth_1d, yerr=err_truth,
                         fmt="o", color="black", label="MC genBefore truth (half B)",
                         markersize=4, zorder=5)
        ax_main.errorbar(centers + 0.02, unfolded_1d, yerr=err_unf,
                         fmt="s", color="tab:blue", label="IBU unfolded (half A resp.)",
                         markersize=4, zorder=4)
        ax_main.set_ylabel("Splittings")
        ax_main.legend(fontsize="x-small")
        mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                           rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax_main, loc=0)

        mask_t = truth_1d > 0
        ratio = np.ones_like(unfolded_1d)
        ratio_err = np.zeros_like(unfolded_1d)
        ratio[mask_t] = unfolded_1d[mask_t] / truth_1d[mask_t]
        ratio_err[mask_t] = err_unf[mask_t] / truth_1d[mask_t]

        ax_ratio.errorbar(centers, ratio, yerr=ratio_err, fmt="s",
                          color="tab:blue", markersize=4)
        ax_ratio.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
        ax_ratio.set_ylim(0.85, 1.15)
        ax_ratio.set_ylabel("Unfolded / Truth")
        ax_ratio.set_xlabel(xlabel)

        save_fig(fig, f"felix_split_closure_ibu_{proj_name}")

    # Pull distributions
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 10))
    mask_pop = truth_b.flatten() > 0
    pulls_bbb_pop = pulls_split_bbb.flatten()[mask_pop]
    pulls_ibu_pop = pulls_split_ibu.flatten()[mask_pop]

    ax1.hist(pulls_bbb_pop, bins=20, range=(-5, 5), color="tab:red", alpha=0.7,
             label=f"BBB: mean={pulls_bbb_pop.mean():.2f}, std={pulls_bbb_pop.std():.2f}")
    ax1.axvline(0, color="black", linestyle="--")
    ax1.set_xlabel("Pull")
    ax1.set_ylabel("Bins")
    ax1.legend(fontsize="x-small")

    ax2.hist(pulls_ibu_pop, bins=20, range=(-5, 5), color="tab:blue", alpha=0.7,
             label=f"IBU: mean={pulls_ibu_pop.mean():.2f}, std={pulls_ibu_pop.std():.2f}")
    ax2.axvline(0, color="black", linestyle="--")
    ax2.set_xlabel("Pull")
    ax2.legend(fontsize="x-small")

    save_fig(fig, "felix_split_closure_pulls")

    # ================================================================
    # Figure 4: Stress test results
    # ================================================================
    if has_validation:
        log.info("\n--- Figure 4: Stress tests ---")
        stress = validation["stress_tests"]

        for direction in ["ln_kt", "ln_1_over_dtheta", "2d_correlated"]:
            dir_results = [s for s in stress if s["direction"] == direction]
            epsilons = [s["epsilon"] for s in dir_results]
            bbb_chi2_ndf = [s["bbb_chi2_ndf"] for s in dir_results]
            ibu_chi2_ndf = [s["ibu_chi2_ndf"] for s in dir_results]

            fig, ax = plt.subplots(figsize=(10, 10))
            ax.plot(epsilons, bbb_chi2_ndf, "o-", color="tab:red", label="Bin-by-bin")
            ax.plot(epsilons, ibu_chi2_ndf, "s-", color="tab:blue", label="IBU")
            ax.axhline(1.0, color="gray", linestyle="--", alpha=0.5)
            ax.set_xlabel(r"Tilt magnitude $\epsilon$")
            ax.set_ylabel(r"$\chi^2/\mathrm{ndf}$")
            ax.legend(fontsize="x-small")
            mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                               rlabel=f"Tilt: {direction}", ax=ax, loc=0)
            save_fig(fig, f"felix_stress_test_{direction}")

    # ================================================================
    # Figure 5: Response matrix
    # ================================================================
    log.info("\n--- Figure 5: Response matrix ---")
    fig, ax = plt.subplots(figsize=(10, 10))
    # Show only populated region
    resp_plot = response.copy()
    resp_plot[resp_plot == 0] = np.nan
    im = ax.imshow(resp_plot, cmap="Blues", aspect="equal", origin="lower",
                   vmin=0, vmax=0.5)
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Migration probability")
    ax.set_xlabel("Reco bin (flat index)")
    ax.set_ylabel("Gen bin (flat index)")
    mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
    save_fig(fig, "felix_response_matrix")

    # Diagonal fraction as 2D map
    fig, ax = plt.subplots(figsize=(10, 10))
    df_plot = diag_frac.reshape(NX, NY).copy()
    df_plot[df_plot == 0] = np.nan
    im = ax.pcolormesh(X_EDGES, Y_EDGES, df_plot.T, cmap="RdYlGn", shading="flat",
                       vmin=0.0, vmax=1.0)
    ax.set_aspect("equal")
    cax = mh.utils.make_square_add_cbar(ax)
    fig.colorbar(im, cax=cax, label="Diagonal fraction")
    ax.set_xlabel(r"$\ln(1/\Delta\theta)$")
    ax.set_ylabel(r"$\ln(k_T/\mathrm{GeV})$")
    mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                       rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
    save_fig(fig, "felix_diagonal_fraction_map")

    # ================================================================
    # Figure 6: IBU vs bin-by-bin comparison
    # ================================================================
    log.info("\n--- Figure 6: IBU vs bin-by-bin comparison ---")
    for proj_axis, proj_name, centers, xlabel in [
        (1, "kt", y_centers, r"$\ln(k_T/\mathrm{GeV})$"),
        (0, "dtheta", x_centers, r"$\ln(1/\Delta\theta)$"),
    ]:
        bbb_1d = np.nansum(rho_bbb, axis=proj_axis)
        ibu_1d = np.nansum(rho_ibu, axis=proj_axis)
        truth_1d = np.nansum(rho_truth, axis=proj_axis)

        fig, (ax_main, ax_ratio) = plt.subplots(
            2, 1, figsize=(10, 10), gridspec_kw={"height_ratios": [3, 1]},
            sharex=True,
        )
        fig.subplots_adjust(hspace=0)

        ax_main.plot(centers, truth_1d, "o-", color="black", label="MC truth",
                     markersize=4, zorder=5)
        ax_main.plot(centers, bbb_1d, "s-", color="tab:red", label="Bin-by-bin",
                     markersize=4, zorder=4)
        ax_main.plot(centers, ibu_1d, "^-", color="tab:blue", label="IBU",
                     markersize=4, zorder=3)
        ax_main.set_ylabel(r"$\rho$")
        ax_main.legend(fontsize="x-small")
        mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                           rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax_main, loc=0)

        mask_t = truth_1d > 0
        ratio_bbb = np.ones_like(bbb_1d)
        ratio_ibu = np.ones_like(ibu_1d)
        ratio_bbb[mask_t] = bbb_1d[mask_t] / truth_1d[mask_t]
        ratio_ibu[mask_t] = ibu_1d[mask_t] / truth_1d[mask_t]

        ax_ratio.plot(centers, ratio_bbb, "s-", color="tab:red", markersize=4,
                      label="BBB/Truth")
        ax_ratio.plot(centers, ratio_ibu, "^-", color="tab:blue", markersize=4,
                      label="IBU/Truth")
        ax_ratio.axhline(1.0, color="black", linestyle="--", linewidth=0.8)
        ax_ratio.set_ylim(0.8, 1.2)
        ax_ratio.set_ylabel("Method / Truth")
        ax_ratio.set_xlabel(xlabel)
        ax_ratio.legend(fontsize="x-small")

        save_fig(fig, f"felix_bbb_vs_ibu_{proj_name}")

    # ================================================================
    # Figure 7: Per-systematic impact
    # ================================================================
    if has_syst:
        log.info("\n--- Figure 7: Per-systematic impact ---")
        syst_names = [
            "tracking_efficiency", "momentum_resolution", "angular_resolution",
            "track_p_threshold", "track_d0_cut", "thrust_cut", "nch_min",
            "thrust_axis_resolution", "mc_model_dependence", "heavy_flavour",
            "isr_modelling",
        ]
        if f"unfolding_method_sym" in syst_d:
            syst_names.append("unfolding_method")

        colors = plt.cm.tab20(np.linspace(0, 1, len(syst_names)))

        # Project to 1D for each axis
        for proj_axis, proj_name, centers, xlabel in [
            (1, "kt", y_centers, r"$\ln(k_T/\mathrm{GeV})$"),
            (0, "dtheta", x_centers, r"$\ln(1/\Delta\theta)$"),
        ]:
            fig, ax = plt.subplots(figsize=(10, 10))
            rho_nom_2d = syst_d["rho_nominal"].reshape(NX, NY)
            rho_nom_1d = np.nansum(rho_nom_2d, axis=proj_axis)

            for idx, name in enumerate(syst_names):
                key = f"{name}_sym"
                if key not in syst_d:
                    continue
                shift_2d = syst_d[key].reshape(NX, NY)
                shift_1d = np.nansum(shift_2d, axis=proj_axis)
                mask_n = rho_nom_1d > 0
                rel_shift_1d = np.zeros_like(shift_1d)
                rel_shift_1d[mask_n] = shift_1d[mask_n] / rho_nom_1d[mask_n]
                ax.plot(centers, rel_shift_1d * 100, "-", color=colors[idx],
                        label=name.replace("_", " "), linewidth=1.5)

            ax.axhline(0, color="black", linestyle="--", linewidth=0.5)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Relative systematic shift (%)")
            ax.legend(fontsize="x-small", ncol=2)
            mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                               rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
            save_fig(fig, f"felix_syst_impact_{proj_name}")

        # Systematic breakdown (stacked bar)
        fig, ax = plt.subplots(figsize=(10, 10))
        rho_nom_2d = syst_d["rho_nominal"].reshape(NX, NY)
        rho_nom_1d_kt = np.nansum(rho_nom_2d, axis=1)  # project to kt

        syst_contributions = {}
        for name in syst_names:
            key = f"{name}_sym"
            if key not in syst_d:
                continue
            shift_2d = syst_d[key].reshape(NX, NY)
            shift_1d = np.nansum(shift_2d, axis=1)
            mask_n = rho_nom_1d_kt > 0
            quad_contrib = np.zeros_like(shift_1d)
            quad_contrib[mask_n] = (shift_1d[mask_n] / rho_nom_1d_kt[mask_n]) ** 2 * 100**2
            syst_contributions[name] = quad_contrib

        # Sort by total contribution
        total_per_source = {n: np.sum(v) for n, v in syst_contributions.items()}
        sorted_names = sorted(total_per_source, key=total_per_source.get, reverse=True)

        bottom = np.zeros(NY)
        for idx, name in enumerate(sorted_names):
            ax.bar(y_centers, syst_contributions[name], width=Y_EDGES[1]-Y_EDGES[0],
                   bottom=bottom, label=name.replace("_", " "),
                   color=colors[idx], alpha=0.8)
            bottom += syst_contributions[name]

        ax.set_xlabel(r"$\ln(k_T/\mathrm{GeV})$")
        ax.set_ylabel("Relative systematic variance (%$^2$)")
        ax.legend(fontsize="x-small", ncol=2, loc="upper right")
        mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                           rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
        save_fig(fig, "felix_syst_breakdown_stacked")

    # ================================================================
    # Figure 8: Correlation matrix
    # ================================================================
    if has_cov:
        log.info("\n--- Figure 8: Correlation matrix ---")
        fig, ax = plt.subplots(figsize=(10, 10))
        im = ax.imshow(corr_matrix, cmap="RdBu_r", aspect="equal", origin="lower",
                       vmin=-1, vmax=1)
        cax = mh.utils.make_square_add_cbar(ax)
        fig.colorbar(im, cax=cax, label="Correlation coefficient")
        ax.set_xlabel("Bin index (flat)")
        ax.set_ylabel("Bin index (flat)")
        mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                           rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)
        save_fig(fig, "felix_correlation_matrix")

        # Also show uncertainty summary
        fig, ax = plt.subplots(figsize=(10, 10))
        rho_nom_flat = cov_d["rho_nominal"]
        mask = rho_nom_flat > 0
        rel_stat = np.zeros(N_BINS)
        rel_total = np.zeros(N_BINS)
        rel_stat[mask] = stat_err[mask] / rho_nom_flat[mask]
        rel_total[mask] = total_err[mask] / rho_nom_flat[mask]

        # Project to 1D
        for proj_axis, proj_name, centers, xlabel in [
            (1, "kt", y_centers, r"$\ln(k_T/\mathrm{GeV})$"),
        ]:
            rel_stat_2d = rel_stat.reshape(NX, NY)
            rel_total_2d = rel_total.reshape(NX, NY)
            # Average relative error across the other axis
            stat_1d = np.nanmean(np.where(rel_stat_2d > 0, rel_stat_2d, np.nan), axis=proj_axis)
            total_1d = np.nanmean(np.where(rel_total_2d > 0, rel_total_2d, np.nan), axis=proj_axis)

            ax.plot(centers, stat_1d * 100, "o-", color="tab:blue",
                    label="Statistical", markersize=4)
            ax.plot(centers, total_1d * 100, "s-", color="tab:red",
                    label="Total (stat + syst)", markersize=4)
            ax.set_xlabel(xlabel)
            ax.set_ylabel("Relative uncertainty (%)")
            ax.legend(fontsize="x-small")
            mh.label.exp_label(exp="ALEPH", data=True, llabel="Open Simulation",
                               rlabel=r"$\sqrt{s} = 91.2$ GeV", ax=ax, loc=0)

        save_fig(fig, "felix_uncertainty_summary")

    # ================================================================
    # JSON outputs
    # ================================================================
    log.info("\n=== JSON outputs ===")
    results_dir = Path("analysis_note/results")
    results_dir.mkdir(parents=True, exist_ok=True)

    # Expected Lund plane
    lund_json = {
        "observable": "Primary Lund jet plane density",
        "sqrt_s_gev": 91.2,
        "correction_method_primary": "bin_by_bin",
        "correction_method_secondary": "iterative_bayesian_unfolding",
        "bin_edges_x": X_EDGES.tolist(),
        "bin_edges_y": Y_EDGES.tolist(),
        "bin_area": float(BIN_AREA),
        "n_hemispheres_genBefore": float(exp["n_hemi_genBefore"]),
        "n_hemispheres_reco": float(exp["n_hemi_reco"]),
        "rho_corrected_bbb": rho_bbb.tolist(),
        "rho_corrected_ibu": rho_ibu.tolist(),
        "rho_truth_genBefore": rho_truth.tolist(),
    }
    if has_cov:
        lund_json["stat_uncertainty"] = stat_err.reshape(NX, NY).tolist()
        lund_json["total_uncertainty"] = total_err.reshape(NX, NY).tolist()

    with open(results_dir / "lund_plane_expected.json", "w") as f:
        json.dump(lund_json, f, indent=2)
    log.info("  Saved lund_plane_expected.json")

    log.info("\nAll figures and JSON outputs complete.")
    log.info("Figures in: %s", FIG_DIR)
    log.info("JSON in: %s", results_dir)


if __name__ == "__main__":
    main()
