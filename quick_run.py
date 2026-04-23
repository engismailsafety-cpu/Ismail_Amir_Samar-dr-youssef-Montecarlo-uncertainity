"""
QUICK RUN SCRIPT - Minimal version for fast execution
"""

import numpy as np
import matplotlib.pyplot as plt

# ================================================================
# INPUT YOUR DATA HERE
# ================================================================

# Enter your measured samples (at least 10)
samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]

# Measurement uncertainty (%)
uncertainty_percent = 5

# Regulatory limit
regulatory_limit = 100

# Number of iterations per sample
iterations_per_sample = 10000

# ================================================================
# RUN SIMULATION
# ================================================================

n_samples = len(samples)
total_iterations = n_samples * iterations_per_sample

print(f"\nRunning Monte Carlo with {n_samples} samples...")
print(f"Total iterations: {total_iterations:,}")

# Run simulation
all_simulations = []
for measured in samples:
    sigma = measured * (uncertainty_percent / 100)
    simulated = np.random.normal(loc=measured, scale=sigma, size=iterations_per_sample)
    all_simulations.extend(simulated)

all_simulations = np.array(all_simulations)

# Calculate results
mean_val = np.mean(all_simulations)
median_val = np.median(all_simulations)
std_val = np.std(all_simulations)
ci_95_lower = np.percentile(all_simulations, 2.5)
ci_95_upper = np.percentile(all_simulations, 97.5)
p_exceed = np.mean(all_simulations > regulatory_limit)

# Print results
print("\n" + "=" * 50)
print("RESULTS")
print("=" * 50)
print(f"Mean:                    {mean_val:.2f}")
print(f"Median:                  {median_val:.2f}")
print(f"Standard Deviation:      {std_val:.2f}")
print(f"95% Confidence Interval: [{ci_95_lower:.2f}, {ci_95_upper:.2f}]")
print(f"Probability > {regulatory_limit}: {p_exceed*100:.1f}%")

# Regulatory decision
if p_exceed < 0.05:
    print("\nDECISION: SAFE ZONE - Declare Compliant")
elif p_exceed > 0.95:
    print("\nDECISION: VIOLATION ZONE - Declare Non-Compliant")
else:
    print("\nDECISION: UNCERTAIN ZONE - Need More Data")

# Quick plot
plt.figure(figsize=(10, 6))
plt.hist(all_simulations, bins=50, alpha=0.7, color='steelblue', edgecolor='black')
plt.axvline(x=regulatory_limit, color='red', linestyle='--', linewidth=2, label=f'Limit = {regulatory_limit}')
plt.axvline(x=mean_val, color='blue', linestyle='-', linewidth=2, label=f'Mean = {mean_val:.1f}')
plt.xlabel('Emission Value')
plt.ylabel('Frequency')
plt.title('Monte Carlo Simulation Results')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()

print("\nSimulation complete!")