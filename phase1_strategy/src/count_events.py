"""Count events in all data and MC files and check MC gen-level branches."""
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

import uproot
import glob

# Count data events
data_dir = "/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/"
data_files = sorted(glob.glob(data_dir + "LEP1Data*.root"))

total_data = 0
for f_path in data_files:
    with uproot.open(f_path) as f:
        n = f["t"].num_entries
        total_data += n
        name = f_path.split("/")[-1]
        log.info(f"Data: {name}: {n:,} events")
log.info(f"Total data events: {total_data:,}")

# Count MC events
mc_dir = "/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/"
mc_files = sorted(glob.glob(mc_dir + "LEP1MC*.root"))

total_mc_reco = 0
total_mc_gen = 0
for f_path in mc_files[:3]:  # Check first 3 for structure
    with uproot.open(f_path) as f:
        n_reco = f["t"].num_entries
        n_gen = f["tgen"].num_entries
        total_mc_reco += n_reco
        total_mc_gen += n_gen
        name = f_path.split("/")[-1]
        log.info(f"MC: {name}: reco={n_reco:,}, gen={n_gen:,}")

# Extrapolate for remaining files
for f_path in mc_files[3:]:
    with uproot.open(f_path) as f:
        n_reco = f["t"].num_entries
        n_gen = f["tgen"].num_entries
        total_mc_reco += n_reco
        total_mc_gen += n_gen

log.info(f"Total MC files: {len(mc_files)}")
log.info(f"Total MC reco events: {total_mc_reco:,}")
log.info(f"Total MC gen events: {total_mc_gen:,}")

# Check MC gen-level branch structure
log.info("\n=== MC GEN-LEVEL BRANCHES ===")
with uproot.open(mc_files[0]) as f:
    tgen = f["tgen"]
    branches = tgen.keys()
    log.info(f"tgen branches ({len(branches)}): {branches[:40]}")
    if len(branches) > 40:
        log.info(f"  ... and {len(branches) - 40} more")

    # Check tgenBefore
    tgen_before = f["tgenBefore"]
    branches_before = tgen_before.keys()
    log.info(f"\ntgenBefore branches ({len(branches_before)}): {branches_before[:40]}")
    log.info(f"tgenBefore entries: {tgen_before.num_entries:,}")

    # Sample gen-level data types
    sample = tgen.arrays(library="ak", entry_stop=3)
    log.info("\ntgen field types:")
    for field in sample.fields[:20]:
        log.info(f"  {field}: {sample[field].type}")

    # Check isMC and pwflag values
    log.info("\n=== DATA pwflag values (track types) ===")
    data_sample = uproot.open(data_files[0])["t"]
    arr = data_sample.arrays(["pwflag", "charge", "nParticle"], library="ak", entry_stop=100)
    import awkward as ak
    all_pwflag = ak.flatten(arr["pwflag"])
    import numpy as np
    unique_pw, counts_pw = np.unique(ak.to_numpy(all_pwflag), return_counts=True)
    for v, c in zip(unique_pw, counts_pw):
        log.info(f"  pwflag={v}: {c} particles")
