#!/usr/bin/env python3
"""Test FastJet API for Lund plane construction."""
import fastjet
import numpy as np

particles = [
    fastjet.PseudoJet(1.0, 0.5, 3.0, np.sqrt(1.0**2 + 0.5**2 + 3.0**2 + 0.14**2)),
    fastjet.PseudoJet(0.8, -0.3, 2.5, np.sqrt(0.8**2 + 0.3**2 + 2.5**2 + 0.14**2)),
    fastjet.PseudoJet(0.2, 0.1, 0.5, np.sqrt(0.2**2 + 0.1**2 + 0.5**2 + 0.14**2)),
    fastjet.PseudoJet(-0.5, 0.2, -2.0, np.sqrt(0.5**2 + 0.2**2 + 2.0**2 + 0.14**2)),
    fastjet.PseudoJet(-0.3, -0.4, -1.5, np.sqrt(0.3**2 + 0.4**2 + 1.5**2 + 0.14**2)),
]

jet_def = fastjet.JetDefinition(fastjet.ee_genkt_algorithm, 999.0, 0.0)
cs = fastjet.ClusterSequence(particles, jet_def)
jets = cs.inclusive_jets()
j = jets[0]

# Test has_parents (SWIG interface requires passing PseudoJet objects)
p1 = fastjet.PseudoJet()
p2 = fastjet.PseudoJet()
has = j.has_parents(p1, p2)
print(f"has_parents: {has}")
if has:
    print(f"  parent1: px={p1.px():.3f}, py={p1.py():.3f}, pz={p1.pz():.3f}, E={p1.E():.3f}")
    print(f"  parent2: px={p2.px():.3f}, py={p2.py():.3f}, pz={p2.pz():.3f}, E={p2.E():.3f}")
    print(f"  parent1 constituents: {len(p1.constituents())}")
    print(f"  parent2 constituents: {len(p2.constituents())}")

# Now follow the primary chain using has_parents
print("\n--- Primary Lund plane declustering ---")


def decluster_primary(jet):
    """Follow the primary declustering chain."""
    splittings = []
    current = jet
    while True:
        p1 = fastjet.PseudoJet()
        p2 = fastjet.PseudoJet()
        if not current.has_parents(p1, p2):
            break

        # Determine harder subjet by p_T w.r.t. beam
        pt1 = np.sqrt(p1.px()**2 + p1.py()**2)
        pt2 = np.sqrt(p2.px()**2 + p2.py()**2)
        if pt1 >= pt2:
            harder, softer = p1, p2
        else:
            harder, softer = p2, p1

        # Compute opening angle
        vec1 = np.array([harder.px(), harder.py(), harder.pz()])
        vec2 = np.array([softer.px(), softer.py(), softer.pz()])
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 < 1e-10 or norm2 < 1e-10:
            break

        cos_theta = np.clip(np.dot(vec1, vec2) / (norm1 * norm2), -1.0, 1.0)
        delta_theta = np.arccos(cos_theta)

        if delta_theta < 1e-10:
            break

        kt = norm2 * np.sin(delta_theta)
        if kt > 0:
            ln_inv_dtheta = np.log(1.0 / delta_theta)
            ln_kt = np.log(kt)
            splittings.append((ln_inv_dtheta, ln_kt))
            print(f"  splitting: delta_theta={delta_theta:.4f}, kt={kt:.4f}, "
                  f"ln(1/dtheta)={ln_inv_dtheta:.3f}, ln(kt)={ln_kt:.3f}")

        current = harder

    return splittings


splittings = decluster_primary(j)
print(f"\nTotal splittings: {len(splittings)}")
