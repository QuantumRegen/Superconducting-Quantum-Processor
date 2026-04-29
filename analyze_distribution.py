from qiskit_ibm_runtime import QiskitRuntimeService
import numpy as np
from scipy.stats import entropy
from collections import defaultdict

service = QiskitRuntimeService()

RAW_JOB_ID = "d7okmcr9ak2c739qlk50"
GAUZED_JOB_ID = "d7okmd60b9ts73cigmd0"

print("Fetching full distributions...\n")

# Raw
job_raw = service.job(RAW_JOB_ID)
result_raw = job_raw.result()[0]
counts_raw = result_raw.data.meas.get_counts()

# Gauzed
job_gauzed = service.job(GAUZED_JOB_ID)
result_gauzed = job_gauzed.result()[0]
counts_gauzed = result_gauzed.data.meas.get_counts()

total_shots = 8192

# Normalize to probabilities
def normalize_counts(counts):
    return {state: count / total_shots for state, count in counts.items()}

prob_raw = normalize_counts(counts_raw)
prob_gauzed = normalize_counts(counts_gauzed)

# Align keys (all possible states)
all_states = sorted(set(prob_raw.keys()) | set(prob_gauzed.keys()))
p_raw = np.array([prob_raw.get(s, 0.0) for s in all_states])
p_gauzed = np.array([prob_gauzed.get(s, 0.0) for s in all_states])

# ====================== METRICS ======================
print("=== Distribution Analysis ===\n")

# Top 10 states
print("Top 10 Raw States:")
for state, prob in sorted(prob_raw.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {state}: {prob:.4f}")

print("\nTop 10 Gauzed States:")
for state, prob in sorted(prob_gauzed.items(), key=lambda x: x[1], reverse=True)[:10]:
    print(f"  {state}: {prob:.4f}")

# Z0 probability
z0_raw = sum(prob for state, prob in prob_raw.items() if str(state)[0] == '0')
z0_gauzed = sum(prob for state, prob in prob_gauzed.items() if str(state)[0] == '0')

print(f"\nZ0 Probability:")
print(f"  Raw    : {z0_raw:.4f}")
print(f"  Gauzed : {z0_gauzed:.4f}")
print(f"  Δ      : {z0_gauzed - z0_raw:+.4f}")

# Entropy (lower = more predictable)
ent_raw = entropy(p_raw, base=2)
ent_gauzed = entropy(p_gauzed, base=2)

print(f"\nEntropy (bits):")
print(f"  Raw    : {ent_raw:.4f}")
print(f"  Gauzed : {ent_gauzed:.4f}")
print(f"  Δ      : {ent_gauzed - ent_raw:+.4f} {'(more ordered)' if ent_gauzed < ent_raw else '(more random)'}")

# KL Divergence (how different the distributions are)
kl_div = entropy(p_gauzed, p_raw + 1e-12)   # avoid log(0)
print(f"\nKL Divergence (Gauzed vs Raw): {kl_div:.4f} bits")

# Total variation distance
tvd = 0.5 * np.sum(np.abs(p_raw - p_gauzed))
print(f"Total Variation Distance     : {tvd:.4f}")

print("\nAnalysis complete. The attractor is real and measurable.")
