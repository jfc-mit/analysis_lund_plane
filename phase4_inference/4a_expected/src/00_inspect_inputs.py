#!/usr/bin/env python3
"""Inspect Phase 3 outputs to understand what we have for Phase 4a."""
import numpy as np

d = np.load("phase3_selection/outputs/correction_ingrid.npz")
print("Keys:", list(d.keys()))
print("correction shape:", d["correction"].shape)
print("h2d_reco shape:", d["h2d_reco"].shape)
print("x_edges:", d["x_edges"])
print("y_edges:", d["y_edges"])
print("n_hemi_reco:", d["n_hemi_reco"])
print("n_hemi_gen:", d["n_hemi_gen"])
print("n_hemi_genBefore:", d["n_hemi_genBefore"])
print("h2d_reco sum:", d["h2d_reco"].sum())
print("h2d_gen sum:", d["h2d_gen"].sum())
print("h2d_genBefore sum:", d["h2d_genBefore"].sum())
print("Populated reco bins:", np.sum(d["h2d_reco"] > 0))
print("Populated genBefore bins:", np.sum(d["h2d_genBefore"] > 0))
c = d["correction"]
mask = c > 0
print("Correction factor range (populated):", c[mask].min(), "-", c[mask].max())
print("Correction factor mean:", c[mask].mean())
print()
print("Correction factors (nonzero):")
print(c[mask])
print()
print("h2d_reco (first few nonzero):")
reco = d["h2d_reco"]
print("reco nonzero bins:", np.argwhere(reco > 0).shape[0])
