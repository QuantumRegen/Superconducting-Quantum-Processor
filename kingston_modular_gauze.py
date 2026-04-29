from qiskit import QuantumCircuit, transpile
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
import numpy as np
import json
from datetime import datetime

service = QiskitRuntimeService()
backend = service.backend("ibm_kingston")

MODULE_SIZE = 8
NUM_MODULES = 3  # Change this easily
TOTAL_QUBITS = MODULE_SIZE * NUM_MODULES
SHOTS = 8192
BATCH_SIZE = 6

print(f"Refined Modular Cluster: {NUM_MODULES} × {MODULE_SIZE} qubits = {TOTAL_QUBITS} total\n")


def create_modular_gauzed(num_modules):
    n = MODULE_SIZE * num_modules
    qc = QuantumCircuit(n)

    for m in range(num_modules):
        start = m * MODULE_SIZE
        # Strong per-module warm-up (from successful run)
        qc.x(range(start, start + 4))
        qc.h(range(start, start + 6))

        # Gold steering per module
        angles = [1.64, 0.82, 2.46, 1.18, 3.54, 2.36, 0.91, 1.45]
        for i in range(MODULE_SIZE):
            idx = start + i
            qc.rz(angles[i % len(angles)], idx)
            qc.rx(angles[(i + 3) % len(angles)] * 0.85, idx)

        # Intra-module collective
        for i in range(MODULE_SIZE - 1):
            qc.cz(start + i, start + i + 1)

    # Loose but meaningful inter-module coupling
    for m in range(num_modules - 1):
        qc.cz(m * MODULE_SIZE + 3, (m + 1) * MODULE_SIZE + 4)  # stronger link than before

    qc.measure_all()
    return qc


def create_raw(n):
    qc = QuantumCircuit(n)
    for i in range(n):
        qc.h(i)
    for i in range(n - 1):
        qc.cx(i, i + 1)
    qc.measure_all()
    return qc


# Transpile and run (same as before)
raw_t = transpile(create_raw(TOTAL_QUBITS), backend=backend, optimization_level=1)
gauzed_t = transpile(create_modular_gauzed(NUM_MODULES), backend=backend, optimization_level=1)

sampler = Sampler(mode=backend)

results = []
for run in range(BATCH_SIZE):
    print(f"Run {run + 1}/{BATCH_SIZE}...")
    job_raw = sampler.run([raw_t], shots=SHOTS)
    job_g = sampler.run([gauzed_t], shots=SHOTS)

    counts_raw = job_raw.result()[0].data.meas.get_counts()
    counts_g = job_g.result()[0].data.meas.get_counts()

    z0_raw = sum(c for s, c in counts_raw.items() if str(s)[0] == '0') / SHOTS
    z0_g = sum(c for s, c in counts_g.items() if str(s)[0] == '0') / SHOTS

    delta = z0_g - z0_raw
    print(f"  Raw Z0: {z0_raw:.4f} | Gauzed Z0: {z0_g:.4f} | Δ = {delta:+.4f}")
    results.append({"run": run + 1, "raw": float(z0_raw), "gauzed": float(z0_g), "delta": float(delta)})

avg_delta = np.mean([r["delta"] for r in results])
print(f"\n{NUM_MODULES}×{MODULE_SIZE} Refined Cluster Average Δ : {avg_delta:+.4f}")

timestamp = datetime.now().strftime("%Y%m%d_%H%M")
with open(f"{NUM_MODULES}x{MODULE_SIZE}q_refined_{timestamp}.json", "w") as f:
    json.dump(results, f, indent=2)

print("Results saved.")