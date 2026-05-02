from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
import numpy as np
import json
from datetime import datetime

service = QiskitRuntimeService()
backend = service.backend("ibm_kingston")

SHOTS = 8192
RUNS = 12

print("=== Optimized 2×8 Attractor (with Transpilation) ===\n")


def create_2x8_attractor():
    qc = QuantumCircuit(16)

    # Warm-up bias
    qc.x([0, 1, 2, 3, 8, 9, 10, 11])
    qc.h(range(16))

    # Drive
    for i in range(16):
        qc.rz(1.75, i)
        qc.rx(0.85, i)

    # Intra-module CZ
    for i in [0, 1, 2, 3, 4, 5, 6]:
        qc.cz(i, i + 1)
    for i in [8, 9, 10, 11, 12, 13, 14]:
        qc.cz(i, i + 1)

    # Weak inter-module
    qc.cz(3, 11)
    qc.cz(4, 12)

    qc.measure_all()
    return qc


# Create and transpile
raw_circuit = create_2x8_attractor()
transpiled_circuit = transpile(raw_circuit, backend=backend, optimization_level=2)
print(f"Circuit depth after transpilation: {transpiled_circuit.depth()}")

# Run
results = []
sampler = Sampler(mode=backend)

print(f"Running {RUNS} runs...\n")
for r in range(RUNS):
    job = sampler.run([transpiled_circuit], shots=SHOTS)
    counts = job.result()[0].data.meas.get_counts()

    z0_prob = sum(count for bitstring, count in counts.items() if bitstring[0] == '0') / SHOTS
    results.append({"run": r + 1, "z0_probability": z0_prob})

    print(f"Run {r + 1:2d} → Z0 = {z0_prob:.4f}")

# Summary
z0_values = [r["z0_probability"] for r in results]
print(f"\n=== Final Summary ===")
print(f"Mean Z0     : {np.mean(z0_values):.4f}")
print(f"Std Dev     : {np.std(z0_values):.4f}")
print(f"Min/Max     : {np.min(z0_values):.4f} / {np.max(z0_values):.4f}")
print(f"Success Rate (>0.5): {sum(1 for v in z0_values if v > 0.5)}/{RUNS}")

# Save
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
with open(f"2x8_locked_transpiled_{timestamp}.json", "w") as f:
    json.dump(results, f, indent=2)

print(f"Data saved.")