"""Check the structure of ALEPH data and MC ROOT files."""
import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

import uproot

# Check one data file
data_path = "/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPH/LEP1Data1994P1_recons_aftercut-MERGED.root"
mc_path = "/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC/LEP1MC1994_recons_aftercut-001.root"

log.info("=== DATA FILE STRUCTURE ===")
with uproot.open(data_path) as f:
    log.info(f"Keys: {f.keys()}")
    for key in f.keys():
        obj = f[key]
        log.info(f"  {key}: type={type(obj).__name__}")
        if hasattr(obj, 'keys'):
            sub_keys = obj.keys()
            log.info(f"    Sub-keys ({len(sub_keys)}): {sub_keys[:20]}")
            if len(sub_keys) > 20:
                log.info(f"    ... and {len(sub_keys) - 20} more")
        if hasattr(obj, 'num_entries'):
            log.info(f"    Entries: {obj.num_entries}")
            # Show branch names
            branches = obj.keys()
            log.info(f"    Branches ({len(branches)}): {branches[:30]}")
            if len(branches) > 30:
                log.info(f"    ... and {len(branches) - 30} more")
            # Read a small sample to check types
            sample = obj.arrays(library="ak", entry_stop=5)
            for field in sample.fields[:30]:
                arr = sample[field]
                log.info(f"      {field}: type={arr.type}")

log.info("\n=== MC FILE STRUCTURE ===")
with uproot.open(mc_path) as f:
    log.info(f"Keys: {f.keys()}")
    for key in f.keys():
        obj = f[key]
        log.info(f"  {key}: type={type(obj).__name__}")
        if hasattr(obj, 'num_entries'):
            log.info(f"    Entries: {obj.num_entries}")
            branches = obj.keys()
            log.info(f"    Branches ({len(branches)}): {branches[:30]}")
            if len(branches) > 30:
                log.info(f"    ... and {len(branches) - 30} more")
            # Check if there are generator-level branches
            gen_branches = [b for b in branches if any(kw in b.lower() for kw in ['gen', 'true', 'truth', 'mc', 'part', 'had'])]
            if gen_branches:
                log.info(f"    Generator-level branches: {gen_branches}")
            sample = obj.arrays(library="ak", entry_stop=5)
            for field in sample.fields[:30]:
                arr = sample[field]
                log.info(f"      {field}: type={arr.type}")
            if len(sample.fields) > 30:
                log.info(f"    ... and {len(sample.fields) - 30} more fields")
