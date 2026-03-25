"""Check full branch list and key variable ranges in MC."""
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

import uproot
import awkward as ak
import numpy as np

mc_path = "/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/LEP1MC1994_recons_aftercut-001.root"

with uproot.open(mc_path) as f:
    # Full branch list for tgen (gen-level after hadronization)
    tgen = f["tgen"]
    all_branches = tgen.keys()
    log.info(f"All tgen branches ({len(all_branches)}):")
    for b in all_branches:
        log.info(f"  {b}")

    # Check what tgenBefore has different
    tgen_before = f["tgenBefore"]
    before_branches = set(tgen_before.keys())
    gen_branches = set(all_branches)
    extra_in_gen = gen_branches - before_branches
    log.info(f"\nExtra branches in tgen vs tgenBefore: {extra_in_gen}")

    # Check reco tree for thrust and event shape variables
    t = f["t"]
    t_branches = t.keys()
    thrust_branches = [b for b in t_branches if any(kw in b.lower() for kw in ['thrust', 'thr', 'spher', 'aplan'])]
    log.info(f"\nThrust/event-shape branches in reco tree: {thrust_branches}")

    # Sample event-level variables
    sample = t.arrays(["nParticle", "Energy", "process", "isMC"], library="ak", entry_stop=10)
    log.info(f"\nnParticle (first 10): {ak.to_list(sample['nParticle'])}")
    log.info(f"Energy (first 10): {ak.to_list(sample['Energy'])}")
    log.info(f"process (first 10): {ak.to_list(sample['process'])}")

    # Check pwflag distribution in MC
    mc_sample = t.arrays(["pwflag", "charge", "pid"], library="ak", entry_stop=1000)
    all_pw = ak.flatten(mc_sample["pwflag"])
    unique_pw, counts_pw = np.unique(ak.to_numpy(all_pw), return_counts=True)
    log.info(f"\nMC reco pwflag distribution:")
    for v, c in zip(unique_pw, counts_pw):
        log.info(f"  pwflag={v}: {c}")

    # Check gen-level pwflag
    gen_sample = tgen.arrays(["pwflag", "charge", "pid", "nParticle"], library="ak", entry_stop=1000)
    gen_pw = ak.flatten(gen_sample["pwflag"])
    unique_gpw, counts_gpw = np.unique(ak.to_numpy(gen_pw), return_counts=True)
    log.info(f"\nMC gen pwflag distribution:")
    for v, c in zip(unique_gpw, counts_gpw):
        log.info(f"  pwflag={v}: {c}")

    log.info(f"\nGen nParticle (first 10): {ak.to_list(gen_sample['nParticle'][:10])}")
