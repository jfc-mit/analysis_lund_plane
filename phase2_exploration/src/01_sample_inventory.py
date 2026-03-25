#!/usr/bin/env python3
"""Script 01: Sample inventory, aftercut investigation, thrust axis source,
momentum resolution verification.

Deliverables: 1, 7, 8, 9 from the Phase 2 plan.
Session: Hugo
"""

import logging
import json
from pathlib import Path

import numpy as np
import uproot
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

DATA_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH")
MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")
OUT_DIR = Path("phase2_exploration/outputs")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def list_trees_and_branches(filepath, max_branches_detail=20):
    """List all trees and their branches in a ROOT file."""
    info = {}
    with uproot.open(filepath) as f:
        for key in f.keys():
            obj = f[key]
            if hasattr(obj, "keys"):  # It's a tree
                tree_name = key.rstrip(";1")
                n_entries = obj.num_entries
                branches = {}
                for bname in obj.keys():
                    try:
                        branches[bname] = str(obj[bname].typename)
                    except Exception:
                        branches[bname] = "unknown"
                info[tree_name] = {
                    "num_entries": n_entries,
                    "num_branches": len(branches),
                    "branches": branches,
                }
    return info


def check_flag_branches(filepath, tree_name, n_events=5000):
    """Check unique values and statistics of flag/weight branches."""
    import awkward as ak
    flag_branches = [
        "passesAll", "passesNTrkMin", "passesSTheta", "passesMissP",
        "passesISR", "passesWW", "passesNeuNch", "pwflag",
    ]
    results = {}
    with uproot.open(filepath) as f:
        tree = f[tree_name]
        available = [b for b in flag_branches if b in tree.keys()]
        for bname in available:
            arr = tree[bname].array(entry_stop=n_events)
            # Handle jagged arrays (per-particle branches like pwflag)
            if arr.ndim > 1:
                flat_np = np.asarray(ak.flatten(arr))
            else:
                flat_np = np.asarray(arr)
            unique = np.unique(flat_np)
            results[bname] = {
                "unique_values": unique.tolist()[:50],
                "n_unique": len(unique),
                "min": float(np.min(flat_np)),
                "max": float(np.max(flat_np)),
                "mean": float(np.mean(flat_np)),
            }
    return results


def count_all_events():
    """Count events in all data and MC files."""
    data_counts = {}
    data_files = sorted(DATA_DIR.glob("LEP1Data*.root"))
    for f in data_files:
        with uproot.open(f) as rf:
            tree = rf["t"]
            data_counts[f.name] = tree.num_entries

    mc_counts = {"t": {}, "tgen": {}, "tgenBefore": {}}
    mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
    for f in mc_files:
        with uproot.open(f) as rf:
            for tname in ["t", "tgen", "tgenBefore"]:
                if tname in [k.split(";")[0] for k in rf.keys()]:
                    mc_counts[tname][f.name] = rf[tname].num_entries

    return data_counts, mc_counts


def investigate_thrust_axis(filepath, n_events=5000):
    """Compare Thrust vs ThrustCharged to determine if pre-computed thrust
    uses energy-flow or charged-only."""
    with uproot.open(filepath) as f:
        tree = f["t"]
        available_thrust = [b for b in tree.keys() if "hrust" in b.lower() or "hrust" in b]
        log.info("Thrust-related branches: %s", available_thrust)

        # Load Thrust and ThrustCharged
        thrust_branches = {}
        for b in available_thrust:
            try:
                arr = tree[b].array(entry_stop=n_events)
                vals = np.asarray(arr)
                thrust_branches[b] = {
                    "mean": float(np.mean(vals)),
                    "std": float(np.std(vals)),
                    "min": float(np.min(vals)),
                    "max": float(np.max(vals)),
                    "n_events": len(vals),
                }
            except Exception as e:
                thrust_branches[b] = {"error": str(e)}

        # Compare Thrust vs ThrustCharged
        if "Thrust" in tree.keys() and "ThrustCharged" in tree.keys():
            t_all = np.asarray(tree["Thrust"].array(entry_stop=n_events))
            t_ch = np.asarray(tree["ThrustCharged"].array(entry_stop=n_events))
            diff = t_all - t_ch
            thrust_branches["comparison"] = {
                "mean_diff": float(np.mean(diff)),
                "std_diff": float(np.std(diff)),
                "max_abs_diff": float(np.max(np.abs(diff))),
                "fraction_identical": float(np.mean(np.abs(diff) < 1e-6)),
            }

    return thrust_branches


def investigate_momentum_resolution(filepath, n_events=5000):
    """Check d0 distribution width to diagnose TPC-only vs TPC+ITC+VDET."""
    import awkward as ak
    with uproot.open(filepath) as f:
        tree = f["t"]
        d0 = tree["d0"].array(entry_stop=n_events)
        d0_flat = ak.flatten(d0)
        d0_np = np.asarray(d0_flat)

        z0 = tree["z0"].array(entry_stop=n_events)
        z0_flat = ak.flatten(z0)
        z0_np = np.asarray(z0_flat)

        # Also check pmag distribution
        pmag = tree["pmag"].array(entry_stop=n_events)
        pmag_flat = ak.flatten(pmag)
        pmag_np = np.asarray(pmag_flat)

        results = {
            "d0": {
                "mean": float(np.mean(d0_np)),
                "std": float(np.std(d0_np)),
                "rms": float(np.sqrt(np.mean(d0_np**2))),
                "median_abs": float(np.median(np.abs(d0_np))),
                "percentile_68": float(np.percentile(np.abs(d0_np), 68)),
            },
            "z0": {
                "mean": float(np.mean(z0_np)),
                "std": float(np.std(z0_np)),
                "rms": float(np.sqrt(np.mean(z0_np**2))),
            },
            "pmag": {
                "mean": float(np.mean(pmag_np)),
                "std": float(np.std(pmag_np)),
                "min": float(np.min(pmag_np)),
                "max": float(np.max(pmag_np)),
            },
        }
    return results


def investigate_tgenBefore(mc_file, n_events=5000):
    """Determine tgenBefore scope: what it contains vs tgen."""
    import awkward as ak
    results = {}
    with uproot.open(mc_file) as f:
        # Compare event counts
        for tname in ["t", "tgen", "tgenBefore"]:
            if tname in [k.split(";")[0] for k in f.keys()]:
                results[f"{tname}_entries"] = f[tname].num_entries

        # Check tgenBefore branches vs tgen branches
        tgen_branches = set(f["tgen"].keys())
        tgenBefore_branches = set(f["tgenBefore"].keys())
        results["branches_only_in_tgen"] = sorted(tgen_branches - tgenBefore_branches)
        results["branches_only_in_tgenBefore"] = sorted(tgenBefore_branches - tgen_branches)
        results["branches_in_both"] = len(tgen_branches & tgenBefore_branches)

        # Check passesAll in tgenBefore
        if "passesAll" in f["tgenBefore"].keys():
            pa = np.asarray(f["tgenBefore"]["passesAll"].array(entry_stop=n_events))
            results["tgenBefore_passesAll_mean"] = float(np.mean(pa))
            results["tgenBefore_passesAll_unique"] = np.unique(pa).tolist()

        # Check if tgenBefore has selection flags
        for flag in ["passesAll", "passesNTrkMin", "passesSTheta"]:
            for tname in ["tgen", "tgenBefore"]:
                key = f"{tname}_{flag}"
                tree = f[tname]
                if flag in tree.keys():
                    arr = np.asarray(tree[flag].array(entry_stop=n_events))
                    results[key] = {
                        "mean": float(np.mean(arr)),
                        "fraction_true": float(np.mean(arr > 0)),
                    }

        # Compare thrust distributions
        for tname in ["tgen", "tgenBefore"]:
            if "Thrust" in f[tname].keys():
                th = np.asarray(f[tname]["Thrust"].array(entry_stop=n_events))
                results[f"{tname}_thrust_mean"] = float(np.mean(th))
                results[f"{tname}_thrust_min"] = float(np.min(th))
                results[f"{tname}_thrust_max"] = float(np.max(th))

    return results


def main():
    log.info("=" * 60)
    log.info("Script 01: Sample Inventory")
    log.info("=" * 60)

    # --- 1. Data file inventory ---
    log.info("\n--- Data Files ---")
    data_file = sorted(DATA_DIR.glob("LEP1Data*.root"))[0]
    log.info("Inspecting representative data file: %s", data_file.name)
    data_info = list_trees_and_branches(data_file)
    for tree_name, tinfo in data_info.items():
        log.info(
            "  Tree '%s': %d entries, %d branches",
            tree_name, tinfo["num_entries"], tinfo["num_branches"],
        )

    # --- 2. MC file inventory ---
    log.info("\n--- MC Files ---")
    mc_file = sorted(MC_DIR.glob("LEP1MC*.root"))[0]
    log.info("Inspecting representative MC file: %s", mc_file.name)
    mc_info = list_trees_and_branches(mc_file)
    for tree_name, tinfo in mc_info.items():
        log.info(
            "  Tree '%s': %d entries, %d branches",
            tree_name, tinfo["num_entries"], tinfo["num_branches"],
        )

    # --- 3. Event counts ---
    log.info("\n--- Event Counts (all files) ---")
    data_counts, mc_counts = count_all_events()
    total_data = sum(data_counts.values())
    log.info("Data files: %d, total events: %d", len(data_counts), total_data)
    for fname, cnt in sorted(data_counts.items()):
        log.info("  %s: %d", fname, cnt)

    total_mc_reco = sum(mc_counts["t"].values())
    total_mc_gen = sum(mc_counts["tgen"].values())
    total_mc_genBefore = sum(mc_counts["tgenBefore"].values())
    log.info("MC files: %d", len(mc_counts["t"]))
    log.info("  Total reco (t): %d", total_mc_reco)
    log.info("  Total gen (tgen): %d", total_mc_gen)
    log.info("  Total genBefore (tgenBefore): %d", total_mc_genBefore)
    log.info("  genBefore/gen ratio: %.3f", total_mc_genBefore / total_mc_gen if total_mc_gen > 0 else 0)

    # --- 4. Flag branches ---
    log.info("\n--- Flag/Weight Branches (data) ---")
    data_flags = check_flag_branches(data_file, "t")
    for bname, stats in data_flags.items():
        log.info("  %s: unique=%s, mean=%.4f", bname, stats["unique_values"][:10], stats["mean"])

    log.info("\n--- Flag/Weight Branches (MC reco) ---")
    mc_flags_reco = check_flag_branches(mc_file, "t")
    for bname, stats in mc_flags_reco.items():
        log.info("  %s: unique=%s, mean=%.4f", bname, stats["unique_values"][:10], stats["mean"])

    # --- 5. Thrust axis investigation ---
    log.info("\n--- Thrust Axis Investigation (data) ---")
    thrust_data = investigate_thrust_axis(data_file)
    for bname, stats in thrust_data.items():
        log.info("  %s: %s", bname, stats)

    log.info("\n--- Thrust Axis Investigation (MC reco) ---")
    thrust_mc = investigate_thrust_axis(mc_file)
    for bname, stats in thrust_mc.items():
        log.info("  %s: %s", bname, stats)

    # --- 6. Momentum resolution investigation ---
    log.info("\n--- Momentum Resolution Investigation (data) ---")
    mom_res_data = investigate_momentum_resolution(data_file)
    for bname, stats in mom_res_data.items():
        log.info("  %s: %s", bname, stats)

    # --- 7. tgenBefore investigation ---
    log.info("\n--- tgenBefore Investigation ---")
    tgenb_info = investigate_tgenBefore(mc_file)
    for key, val in tgenb_info.items():
        log.info("  %s: %s", key, val)

    # --- Save all results as JSON ---
    results = {
        "data_representative": {
            "file": data_file.name,
            "trees": {k: {"num_entries": v["num_entries"], "num_branches": v["num_branches"]}
                      for k, v in data_info.items()},
        },
        "mc_representative": {
            "file": mc_file.name,
            "trees": {k: {"num_entries": v["num_entries"], "num_branches": v["num_branches"]}
                      for k, v in mc_info.items()},
        },
        "data_event_counts": data_counts,
        "mc_event_counts": {
            "reco_total": total_mc_reco,
            "gen_total": total_mc_gen,
            "genBefore_total": total_mc_genBefore,
        },
        "data_flags": data_flags,
        "mc_flags_reco": mc_flags_reco,
        "thrust_data": thrust_data,
        "thrust_mc": thrust_mc,
        "momentum_resolution_data": mom_res_data,
        "tgenBefore_info": tgenb_info,
    }

    # Save full branch lists
    results["data_branches_t"] = data_info.get("t", {}).get("branches", {})
    results["mc_branches_t"] = mc_info.get("t", {}).get("branches", {})
    results["mc_branches_tgen"] = mc_info.get("tgen", {}).get("branches", {})
    results["mc_branches_tgenBefore"] = mc_info.get("tgenBefore", {}).get("branches", {})

    outfile = OUT_DIR / "sample_inventory_hugo.json"
    with open(outfile, "w") as f:
        json.dump(results, f, indent=2, default=str)
    log.info("\nResults saved to %s", outfile)


if __name__ == "__main__":
    main()
