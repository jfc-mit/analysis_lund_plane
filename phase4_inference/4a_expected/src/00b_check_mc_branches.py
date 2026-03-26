#!/usr/bin/env python3
"""Check MC ROOT file branch structure for Phase 4a planning."""
import uproot
from pathlib import Path

MC_DIR = Path("/n/holystore01/LABS/iaifi_lab/Lab/sambt/LEP/ALEPHMC")
mc_files = sorted(MC_DIR.glob("LEP1MC*.root"))
print(f"Found {len(mc_files)} MC files")
print(f"First file: {mc_files[0].name}")

f = uproot.open(mc_files[0])
print("\nTrees:", list(f.keys()))

t = f["t"]
print("\nReco branches:", sorted(t.keys()))

tg = f["tgen"]
print("\nGen branches:", sorted(tg.keys()))

tgb = f["tgenBefore"]
print("\nGenBefore branches:", sorted(tgb.keys()))

# Check number of events
import awkward as ak
reco = t.arrays(["pmag"], entry_stop=5)
print(f"\nFirst 5 reco events, particles per event: {ak.num(reco['pmag']).tolist()}")
gen = tg.arrays(["pmag"], entry_stop=5)
print(f"First 5 gen events, particles per event: {ak.num(gen['pmag']).tolist()}")
genb = tgb.arrays(["pmag"], entry_stop=5)
print(f"First 5 genBefore events, particles per event: {ak.num(genb['pmag']).tolist()}")

# Check for pid branch
for tree_name in ["t", "tgen", "tgenBefore"]:
    tree = f[tree_name]
    has_pid = "pid" in tree.keys()
    has_id = "id" in tree.keys()
    print(f"\n{tree_name}: has pid={has_pid}, has id={has_id}")
    if has_pid:
        arr = tree.arrays(["pid"], entry_stop=2)
        print(f"  pid sample: {arr['pid'][0].tolist()[:10]}")
    if has_id:
        arr = tree.arrays(["id"], entry_stop=2)
        print(f"  id sample: {arr['id'][0].tolist()[:10]}")

print("\nTotal reco events:", t.num_entries)
print("Total gen events:", tg.num_entries)
print("Total genBefore events:", tgb.num_entries)
