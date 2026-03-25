#!/usr/bin/env python3
"""Quick validation: check tree structure and time a small slice."""

import time
import logging
from pathlib import Path

import awkward as ak
import numpy as np
import uproot
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")

f = uproot.open(MC_DIR / "LEP1MC1994_recons_aftercut-001.root")

for tree_name in ["t", "tgen", "tgenBefore"]:
    t = f[tree_name]
    log.info("%s: %d entries, %d branches", tree_name, t.num_entries, len(t.keys()))

# Check tgenBefore for required branches
gb = f["tgenBefore"]
thrust_keys = [k for k in gb.keys() if "Thrust" in k or "TTheta" in k or "TPhi" in k]
log.info("tgenBefore thrust-related keys: %s", thrust_keys)

# Check if passesAll exists in tgenBefore
log.info("tgenBefore has passesAll: %s", "passesAll" in gb.keys())

# Quick timing test: load 500 events from reco
t0 = time.time()
branches = ["px", "py", "pz", "pmag", "d0", "z0", "pwflag",
            "Thrust", "TTheta", "TPhi", "passesAll"]
arr = f["t"].arrays(branches, entry_stop=500)
log.info("Load 500 reco events: %.2fs", time.time() - t0)
log.info("Event 0: %d particles", len(arr["pmag"][0]))

# Check gen branches
gen_arr = f["tgen"].arrays(["px", "py", "pz", "pmag", "pwflag",
                            "Thrust", "TTheta", "TPhi"], entry_stop=10)
log.info("tgen event 0: %d particles", len(gen_arr["pmag"][0]))

# Check genBefore branches
genb_arr = f["tgenBefore"].arrays(["px", "py", "pz", "pmag", "pwflag",
                                   "Thrust", "TTheta", "TPhi"], entry_stop=10)
log.info("tgenBefore event 0: %d particles", len(genb_arr["pmag"][0]))

f.close()
log.info("Validation complete.")
