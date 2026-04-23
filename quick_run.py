"""
QUICK RUN SCRIPT - Text Only Version (No matplotlib required)
Works on any environment including Streamlit Cloud with limited graphics
"""

import numpy as np
import sys

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

def run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations_per_sample):
    """Run Monte Carlo simulation and return results"""
    
    n_samples = len(samples)
    total_iterations = n_samples * iterations_per_sample
    
    print(f"\n{'='*60}")
    print("MONTE CARLO SIMULATION - EMISSION PREDICTION")
    print(f"{'='*60}")
    print(f"Number of samples: {n_samples}")
    print(f"Iterations per sample: {iterations_per_sample:,}")
    print(f"Total iterations: {total_iterations:,}")
    print(f"Measurement uncertainty: ±{uncertainty_percent}%")
    print(f"Regulatory limit: {regulatory_limit}")
    print(f"{'='*60}")
    
    print("\nRunning simulation...")
    
    # Run simulation
    all_simulations = []
    for i, measured in enumerate(samples):
        sigma = measured * (uncertainty_percent / 100)
        simulated = np.random.normal(loc=measured, scale=sigma, size=iterations_per_sample)
        all_simulations.extend(simulated)
        
        # Progress indicator
        if (i + 1) % 5 == 0 or i == n_samples - 1:
            print(f"  Processed {i+1}/{n_samples} samples...")
    
    all_simulations = np.array(all_simulations)
    
    # Calculate results
    results = {
        'mean': np.mean(all_simulations),
        'median': np.median(all_simulations),
        'std': np.std(all_simulations),
        'min': np.min(all_simulations),
        'max': np.max(all_simulations),
        'percentile_2.5': np.percentile(all_simulations, 2.5),
        'percentile_5': np.percentile(all_simulations, 5),
        'percentile_95': np.percentile(all_simulations, 95),
        'percentile_97.5': np.percentile(all_simulations, 97.5),
        'p_exceed': np.mean(all_simulations > regulatory_limit),
        'p_comply': np.mean(all_simulations <= regulatory_limit),
        'sample_mean': np.mean(samples),
        'sample_std': np.std(samples),
        'sample_min': min(samples),
        'sample_max': max(samples),
        'n_samples': n_samples,
        'total_iterations': total_iterations,
        'all_simulations': all_simulations
    }
    
    return results


def print_results(results, regulatory_limit):
    """Print formatted results"""
    
    print(f"\n{'='*60}")
    print("RESULTS")
    print(f"{'='*60}")
    
    print("\n📊 ORIGINAL SAMPLES STATISTICS:")
    print("-" * 40)
    print(f"   Number of samples:     {results['n_samples']}")
    print(f"   Sample mean:           {results['sample_mean']:.2f}")
    print(f"   Sample std deviation:  {results['sample_std']:.2f}")
    print(f"   Sample range:          [{results['sample_min']:.2f}, {results['sample_max']:.2f}]")
    print(f"   Samples:               {samples}")
    
    print("\n🎲 MONTE CARLO RESULTS:")
    print("-" * 40)
    print(f"   Mean of simulation:    {results['mean']:.2f}")
    print(f"   Median:                {results['median']:.2f}")
    print(f"   Standard deviation:    {results['std']:.2f}")
    print(f"   Total range:           [{results['min']:.2f}, {results['max']:.2f}]")
    
    print("\n📈 CONFIDENCE INTERVALS:")
    print("-" * 40)
    print(f"   90% CI:                [{results['percentile_5']:.2f}, {results['percentile_95']:.2f}]")
    print(f"   95% CI:                [{results['percentile_2.5']:.2f}, {results['percentile_97.5']:.2f}]")
    
    print("\n⚠️ REGULATORY ANALYSIS:")
    print("-" * 40)
    print(f"   Regulatory limit:      {regulatory_limit:.2f}")
    print(f"   Probability exceedance: {results['p_exceed']*100:.1f}%")
    print(f"   Probability compliance: {results['p_comply']*100:.1f}%")
    
    print("\n✅ REGULATORY DECISION:")
    print("-" * 40)
    if results['p_exceed'] < 0.05:
        print(f"   Decision:              SAFE ZONE - Declare Compliant")
        print(f"   Action:                No enforcement action needed")
    elif results['p_exceed'] > 0.95:
        print(f"   Decision:              VIOLATION ZONE - Declare Non-Compliant")
        print(f"   Action:                Enforcement action recommended")
    else:
        print(f"   Decision:              UNCERTAIN ZONE - Need More Data")
        print(f"   Action:                Collect additional samples or install CEMS")
    
    print(f"\n{'='*60}")


def print_histogram_text(results, regulatory_limit, width=50):
    """Print text-based histogram"""
    
    print("\n📊 TEXT-BASED HISTOGRAM (Distribution of Simulated Values)")
    print("-" * 60)
    
    # Create bins
    min_val = results['min']
    max_val = results['max']
    bins = np.linspace(min_val, max_val, 20)
    
    # Count frequencies
    hist, bin_edges = np.histogram(results['all_simulations'], bins=bins)
    
    # Find max frequency for scaling
    max_freq = max(hist)
    scale = width / max_freq
    
    for i in range(len(hist)):
        bar_length = int(hist[i] * scale)
        bar = '█' * bar_length
        
        # Color code based on bin position relative to limit
        if bin_edges[i] >= regulatory_limit:
            prefix = '🔴'
        elif bin_edges[i+1] <= regulatory_limit:
            prefix = '🟢'
        else:
            prefix = '🟡'
        
        print(f"{prefix} {bin_edges[i]:6.1f} - {bin_edges[i+1]:6.1f} | {bar}")
    
    print(f"\n🟢 = Below limit | 🟡 = Crosses limit | 🔴 = Above limit")
    print(f"Limit = {regulatory_limit}")


def print_cdf_text(results, regulatory_limit):
    """Print text-based CDF table"""
    
    print("\n📈 TEXT-BASED CDF (Cumulative Distribution Function)")
    print("-" * 60)
    print(f"{'Value (ppm)':>12} | {'Probability Non-Exceedance':>25}")
    print("-" * 60)
    
    # Calculate percentiles at regular intervals
    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    for p in percentiles:
        value = np.percentile(results['all_simulations'], p)
        print(f"{value:12.2f} | {p:25}%")
    
    print("-" * 60)
    print(f"{regulatory_limit:12.2f} | {results['p_comply']*100:25.1f}% (at limit)")
    print("-" * 60)


def print_sample_analysis(samples):
    """Print statistical analysis of input samples"""
    
    print("\n📋 SAMPLE STATISTICAL ANALYSIS")
    print("-" * 60)
    
    sorted_samples = sorted(samples)
    n = len(sorted_samples)
    
    print(f"Minimum value:     {sorted_samples[0]:.2f}")
    print(f"Maximum value:     {sorted_samples[-1]:.2f}")
    print(f"Mean:              {np.mean(sorted_samples):.2f}")
    print(f"Median:            {np.median(sorted_samples):.2f}")
    print(f"Standard deviation: {np.std(sorted_samples):.2f}")
    
    # Quartiles
    q1 = np.percentile(sorted_samples, 25)
    q3 = np.percentile(sorted_samples, 75)
    print(f"Q1 (25th):         {q1:.2f}")
    print(f"Q3 (75th):         {q3:.2f}")
    print(f"IQR:               {q3 - q1:.2f}")
    
    # Check for outliers using IQR method
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in samples if x < lower_bound or x > upper_bound]
    
    if outliers:
        print(f"\n⚠️ Potential outliers detected: {outliers}")
    else:
        print(f"\n✓ No outliers detected")


def run_sample_size_analysis(samples, uncertainty_percent, regulatory_limit, iterations_per_sample):
    """Analyze how results change with different sample sizes"""
    
    print("\n" + "=" * 60)
    print("SAMPLE SIZE EFFECT ANALYSIS")
    print("=" * 60)
    
    sample_sizes = [10, 20, 30, 50, 100]
    results_list = []
    
    print(f"\n{'Samples':>8} | {'Mean':>10} | {'95% CI Width':>12} | {'P(Exceed)':>10}")
    print("-" * 50)
    
    for size in sample_sizes:
        if size > len(samples):
            break
        
        sample_subset = samples[:size]
        sigma_vals = [s * (uncertainty_percent / 100) for s in sample_subset]
        
        all_sim = []
        for j, measured in enumerate(sample_subset):
            sim = np.random.normal(loc=measured, scale=sigma_vals[j], size=iterations_per_sample)
            all_sim.extend(sim)
        
        all_sim = np.array(all_sim)
        mean_val = np.mean(all_sim)
        ci_lower = np.percentile(all_sim, 2.5)
        ci_upper = np.percentile(all_sim, 97.5)
        ci_width = ci_upper - ci_lower
        p_exceed = np.mean(all_sim > regulatory_limit)
        
        results_list.append((size, mean_val, ci_width, p_exceed))
        print(f"{size:8} | {mean_val:10.2f} | {ci_width:12.2f} | {p_exceed*100:10.1f}%")
    
    print("\n💡 INTERPRETATION:")
    print("   As sample size increases, the confidence interval width decreases.")
    print("   More samples = More precise estimate of true emissions.")


def export_to_csv(results, filename="monte_carlo_results.csv"):
    """Export results to CSV file"""
    import csv
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Metric', 'Value'])
            writer.writerow(['Number of Samples', results['n_samples']])
            writer.writerow(['Sample Mean', results['sample_mean']])
            writer.writerow(['Sample Std Dev', results['sample_std']])
            writer.writerow(['Simulation Mean', results['mean']])
            writer.writerow(['Simulation Median', results['median']])
            writer.writerow(['Simulation Std Dev', results['std']])
            writer.writerow(['95% CI Lower', results['percentile_2.5']])
            writer.writerow(['95% CI Upper', results['percentile_97.5']])
            writer.writerow(['Probability of Exceedance', results['p_exceed']])
            writer.writerow(['Probability of Compliance', results['p_comply']])
            writer.writerow(['Regulatory Limit', regulatory_limit])
        
        print(f"\n✅ Results exported to {filename}")
    except Exception as e:
        print(f"\n⚠️ Could not export to CSV: {e}")


# ================================================================
# MAIN EXECUTION
# ================================================================

if __name__ == "__main__":
    
    # Run Monte Carlo simulation
    results = run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations_per_sample)
    
    # Print results
    print_results(results, regulatory_limit)
    
    # Print sample analysis
    print_sample_analysis(samples)
    
    # Print text-based histogram
    print_histogram_text(results, regulatory_limit)
    
    # Print text-based CDF
    print_cdf_text(results, regulatory_limit)
    
    # Run sample size analysis if enough samples
    if len(samples) >= 30:
        run_sample_size_analysis(samples, uncertainty_percent, regulatory_limit, 1000)
    
    # Export to CSV
    export_to_csv(results)
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)
