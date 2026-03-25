#!/usr/bin/env python3
"""Print cutflow summary."""
import json
import logging
from pathlib import Path
from rich.logging import RichHandler

logging.basicConfig(level=logging.INFO, format="%(message)s",
                    handlers=[RichHandler(rich_tracebacks=True)])
log = logging.getLogger(__name__)

HERE = Path(__file__).resolve().parent
OUT_DIR = HERE.parent / "outputs"

with open(OUT_DIR / "cutflow_ingrid.json") as f:
    d = json.load(f)

log.info("DATA:")
log.info("  Total: %d", d["data"]["total_events"])
log.info("  Selected (passesAll + Thrust + Nch): %d", d["data"]["total_selected"])
log.info("  After hemi cut: %d", d["data"]["total_hemi_cut"])
log.info("  Hemispheres: %d", d["data"]["total_hemispheres"])
log.info("  Splittings: %d", d["data"]["total_splittings"])
log.info("")
log.info("MC RECO:")
log.info("  Total: %d", d["mc"]["reco_total"])
log.info("  Selected: %d", d["mc"]["reco_selected"])
log.info("  After hemi cut: %d", d["mc"]["reco_hemi"])
log.info("  Hemispheres: %d", d["mc"]["reco_hemispheres"])
log.info("  Splittings: %d", d["mc"]["reco_splittings"])
log.info("")
log.info("MC GEN:")
log.info("  Total: %d", d["mc"]["gen_total"])
log.info("  Selected: %d", d["mc"]["gen_selected"])
log.info("  After hemi cut: %d", d["mc"]["gen_hemi"])
log.info("  Hemispheres: %d", d["mc"]["gen_hemispheres"])
log.info("  Splittings: %d", d["mc"]["gen_splittings"])
log.info("")
log.info("MC GENBEFORE:")
log.info("  Total: %d", d["mc"]["genBefore_total"])
log.info("  Selected (N_ch >= 5): %d", d["mc"]["genBefore_selected"])
log.info("  After hemi cut: %d", d["mc"]["genBefore_hemi"])
log.info("  Hemispheres: %d", d["mc"]["genBefore_hemispheres"])
log.info("  Splittings: %d", d["mc"]["genBefore_splittings"])
