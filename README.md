# Floquet-Engineered Topological Attractor on IBM Kingston

**Author:** Wayne Spratley Independent Researcher (QuantumRegen)  
**Date:** 29 April 2026  
**Hardware:** IBM Kingston

---

## Abstract

We report the experimental realization of a strong, reproducible **topological attractor** in the many-body state space of a superconducting quantum processor.

Using a modular **2×8 loose-cluster circuit** (16 qubits), Floquet engineering via periodic RZ/RX drives and CZ entangling layers creates an effective dissipative Hamiltonian whose low-quasienergy manifold is strongly polarized in the positive-$Z$ sector.

Over **24 independent runs** (8192 shots each), the circuit shifts the primary observable $Z_0$ probability from **0.490 ± 0.003** (raw) to **0.932 ± 0.003** (gauzed), yielding a mean shift **Δ = +0.427** with standard deviation **σ = 0.0064** and 95% confidence interval **±0.0026**. All 24 runs were positive.

The attractor reduces entropy by ~2.15 bits and produces a KL divergence of 1.48 bits, demonstrating deterministic control over collective modes on noisy hardware.

## Key Results (24-run Mega Batch)

| Metric                        | Value                  |
|-------------------------------|------------------------|
| Mean Δ(Z₀)                    | **+0.427**             |
| Std Dev                       | 0.0064                 |
| 95% CI                        | ±0.0026                |
| Gauzed Z₀                     | 0.932 ± 0.003          |
| Success Rate                  | 100%                   |

## Theoretical Backbone

The circuit implements a Floquet drive whose effective Hamiltonian is approximately:

$$
H_{\rm eff} \approx \sum h_k^z Z_k + \sum J_{zz} Z_i Z_j + J_{xy}(X_i X_j + Y_i Y_j) + J_{\rm inter} \text{(weak links)}
$$

This engineered landscape, combined with hardware dissipation, creates a deep basin of attraction — the observed topological attractor.

## Full Technical Note

For proper mathematical rendering, see the attached **`Floquet_Engineered.pdf`** (LaTeX compiled version).

---

**Repository Contents**
- Full Qiskit scripts
- 24-run raw statistics (JSON)
- Analysis tools
- Technical note Floquet_Engineered PDF

**Status:** Experimentally validated, statistically robust (24 runs), theoretically grounded.
Reproduction requires Qiskit runtime, numpy and provided scripts.
---

*“We engineered low-energy collective modes via Floquet driving and let the system do its deterministic thing.”*

## Airbus Quantum Challenge 2026 Submission

**Hybrid Quantum Attractor Stabilisation of Taylor-Green Vortex Dynamics**  
[PDF Submission]()

- Real hardware results on IBM Kingston & Fez  
- +14.8% sustained kinetic energy growth  
- −65% enstrophy reduction (strong large-scale vortex coherence)  
- Full code and notebooks: [hybrid_taylor_green.html](hybrid_taylor_green.html)

- # 3D-Informed Quantum-Classical Hybrid Fluid Dynamics

**Quantum-enhanced turbulence control using IBM superconducting processors**

## Overview

This repository contains a hybrid quantum-classical framework for simulating and controlling three-dimensional incompressible turbulent flows. The system combines a classical pseudo-spectral Navier–Stokes solver with periodic quantum corrections executed on IBM Quantum hardware (ibm_fez, ibm_kingston, ibm_marrakesh).

The quantum component uses measurement statistics from a fixed 16-qubit attractor circuit to inject energy and vorticity, with injection strengths guided by high-enstrophy windows identified in a 3D Gross–Pitaevskii BEC proxy.

## Key Results (ibm_fez run)

- Final Kinetic Energy: **2.81** (started from 0.25)
- Maximum Enstrophy: **4.04**
- Mean absolute dissipation rate: **~1.70**

The hybrid system demonstrates sustained growth of kinetic energy and enstrophy with low net dissipation compared to equivalent classical simulations at the same viscosity (ν = 0.00012).

## Repository Contents

- `floquet_3d_tgv.ipynb` – Main simulation script and iterations
- `tgv_metrics_v16.json` – Full metrics from the Fez run

## How to Run

```bash
pip install qiskit qiskit-ibm-runtime numpy scipy matplotlib
python hybrid_quantum_fluid_v16.py
