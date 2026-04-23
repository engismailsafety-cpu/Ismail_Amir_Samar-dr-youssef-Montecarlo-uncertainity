"""
MONTE CARLO SIMULATION FOR EMISSION PREDICTION
With User-Input Samples (10 to Unlimited)

Author: Environmental Data Analyst
Date: 2024
Purpose: Predict emissions based on real measurement samples
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ================================================================
# STEP 1: USER INPUT SECTION
# ================================================================

def get_user_samples():
    """Function to get sample data from user"""
    
    print("=" * 60)
    print("MONTE CARLO SIMULATION - EMISSION PREDICTION")
    print("=" * 60)
    print()
    
    # Method 1: Manual entry
    print("How would you like to enter your samples?")
    print("1. Manual entry (type each value)")
    print("2. Load from CSV file")
    print("3. Use example data")
    
    choice = input("\nEnter your choice (1/2/3): ")
    
    if choice == '1':
        # Manual entry
        n = int(input("\nHow many samples do you have? (Minimum 10): "))
        if n < 10:
            print("\nWARNING: Less than 10 samples may give unreliable results!")
            confirm = input("Continue anyway? (y/n): ")
            if confirm.lower() != 'y':
                return get_user_samples()
        
        samples = []
        print("\nEnter each measured value (in ppm or appropriate units):")
        for i in range(n):
            val = float(input(f"Sample {i+1}: "))
            samples.append(val)
            
    elif choice == '2':
        # Load from CSV
        filename = input("\nEnter CSV filename (e.g., data.csv): ")
        try:
            df = pd.read_csv(filename)
            # Assuming first column contains the data
            samples = df.iloc[:, 0].tolist()
            print(f"\nLoaded {len(samples)} samples from {filename}")
        except:
            print("\nError loading file. Using example data instead.")
            samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]
            
    else:
        # Example data
        print("\nUsing example data (10 samples from a refinery)")
        samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]
    
    return samples


def get_uncertainty():
    """Get measurement uncertainty from user"""
    
    print("\n" + "=" * 60)
    print("MEASUREMENT UNCERTAINTY SETUP")
    print("=" * 60)
    
    print("\nTypical uncertainty values:")
    print("• CEMS (Continuous Monitor): ±5%")
    print("• Handheld Monitor: ±10%")
    print("• Lab Analysis: ±3%")
    print("• Visual/Estimate: ±20%")
    
    choice = input("\nUse same uncertainty for all samples? (y/n): ")
    
    if choice.lower() == 'y':
        uncertainty_percent = float(input("Enter uncertainty percentage (e.g., 5 for ±5%): "))
        uncertainties = None
    else:
        print("\nEnter uncertainty for each sample (in %):")
        uncertainties = []
        n = len(samples)
        for i in range(n):
            u = float(input(f"Sample {i+1} uncertainty (%): "))
            uncertainties.append(u)
    
    return uncertainty_percent, uncertainties


def get_regulatory_limit():
    """Get regulatory limit from user"""
    
    print("\n" + "=" * 60)
    print("REGULATORY LIMIT")
    print("=" * 60)
    
    limit = float(input("\nEnter the regulatory limit (in same units as samples): "))
    return limit


def get_simulation_parameters():
    """Get Monte Carlo parameters from user"""
    
    print("\n" + "=" * 60)
    print("SIMULATION PARAMETERS")
    print("=" * 60)
    
    print("\nRecommended settings:")
    print("• Quick analysis: 1,000 iterations per sample")
    print("• Standard analysis: 10,000 iterations per sample")
    print("• High precision: 100,000 iterations per sample")
    
    iterations_per_sample = int(input("\nEnter iterations per sample (default 10000): ") or 10000)
    
    return iterations_per_sample


# ================================================================
# STEP 2: MONTE CARLO SIMULATION FUNCTION
# ================================================================

def run_monte_carlo(samples, uncertainty_percent, uncertainties, iterations_per_sample):
    """
    Run Monte Carlo simulation
    
    Parameters:
    - samples: list of measured values
    - uncertainty_percent: float (if same for all), or None if per-sample
    - uncertainties: list of per-sample uncertainties (if uncertainty_percent is None)
    - iterations_per_sample: int
    
    Returns:
    - all_simulations: array of all simulated true values
    - results_dict: dictionary with statistical results
    """
    
    n_samples = len(samples)
    total_iterations = n_samples * iterations_per_sample
    
    print("\n" + "=" * 60)
    print("RUNNING MONTE CARLO SIMULATION")
    print("=" * 60)
    print(f"Number of samples: {n_samples}")
    print(f"Iterations per sample: {iterations_per_sample:,}")
    print(f"Total iterations: {total_iterations:,}")
    print("-" * 60)
    
    all_simulations = []
    
    for i, measured in enumerate(samples):
        # Get uncertainty for this sample
        if uncertainty_percent is not None:
            u_percent = uncertainty_percent
        else:
            u_percent = uncertainties[i]
        
        # Calculate standard deviation
        sigma = measured * (u_percent / 100)
        
        # Generate random values from normal distribution
        simulated = np.random.normal(
            loc=measured,      # mean = measured value
            scale=sigma,       # standard deviation
            size=iterations_per_sample
        )
        
        all_simulations.extend(simulated)
        
        # Progress indicator
        if (i + 1) % 10 == 0 or i == n_samples - 1:
            print(f"Processed {i+1}/{n_samples} samples...")
    
    return np.array(all_simulations)


# ================================================================
# STEP 3: RESULTS ANALYSIS FUNCTION
# ================================================================

def analyze_results(all_simulations, regulatory_limit, samples):
    """
    Analyze Monte Carlo results
    
    Returns dictionary with all statistics
    """
    
    results = {}
    
    # Basic statistics
    results['mean'] = np.mean(all_simulations)
    results['median'] = np.median(all_simulations)
    results['std'] = np.std(all_simulations)
    results['min'] = np.min(all_simulations)
    results['max'] = np.max(all_simulations)
    
    # Percentiles for confidence intervals
    results['percentile_2.5'] = np.percentile(all_simulations, 2.5)
    results['percentile_5'] = np.percentile(all_simulations, 5)
    results['percentile_95'] = np.percentile(all_simulations, 95)
    results['percentile_97.5'] = np.percentile(all_simulations, 97.5)
    
    # Probability of exceedance
    results['p_exceed'] = np.mean(all_simulations > regulatory_limit)
    results['p_comply'] = 1 - results['p_exceed']
    
    # Sample statistics
    results['sample_mean'] = np.mean(samples)
    results['sample_std'] = np.std(samples)
    results['sample_min'] = np.min(samples)
    results['sample_max'] = np.max(samples)
    results['n_samples'] = len(samples)
    
    # Regulatory decision zones
    if results['p_exceed'] < 0.05:
        results['decision'] = "SAFE ZONE - Declare Compliant"
        results['decision_color'] = "green"
    elif results['p_exceed'] > 0.95:
        results['decision'] = "VIOLATION ZONE - Declare Non-Compliant"
        results['decision_color'] = "red"
    else:
        results['decision'] = "UNCERTAIN ZONE - Need More Data"
        results['decision_color'] = "orange"
    
    return results


# ================================================================
# STEP 4: VISUALIZATION FUNCTIONS
# ================================================================

def plot_histogram(all_simulations, regulatory_limit, results):
    """Create histogram of simulated values"""
    
    plt.figure(figsize=(12, 6))
    
    # Create histogram
    n, bins, patches = plt.hist(all_simulations, bins=50, alpha=0.7, 
                                 color='steelblue', edgecolor='black', density=True)
    
    # Color bars that exceed limit
    for i, (left, right) in enumerate(zip(bins[:-1], bins[1:])):
        if left >= regulatory_limit:
            patches[i].set_facecolor('red')
            patches[i].set_alpha(0.7)
        elif right <= regulatory_limit:
            patches[i].set_facecolor('green')
            patches[i].set_alpha(0.5)
        else:
            # Bar crosses the limit
            patches[i].set_facecolor('orange')
            patches[i].set_alpha(0.7)
    
    # Add vertical line for regulatory limit
    plt.axvline(x=regulatory_limit, color='red', linestyle='--', 
                linewidth=2, label=f'Regulatory Limit = {regulatory_limit}')
    
    # Add vertical line for mean
    plt.axvline(x=results['mean'], color='blue', linestyle='-', 
                linewidth=2, label=f'Mean = {results["mean"]:.1f}')
    
    # Add confidence interval shading
    plt.axvspan(results['percentile_2.5'], results['percentile_97.5'], 
                alpha=0.2, color='gray', label='95% Confidence Interval')
    
    plt.xlabel('Emission Value (ppm)', fontsize=12)
    plt.ylabel('Probability Density', fontsize=12)
    plt.title('Monte Carlo Simulation Results\nDistribution of Possible True Values', 
              fontsize=14, fontweight='bold')
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt.gcf()


def plot_cdf(all_simulations, regulatory_limit, results):
    """Plot cumulative distribution function"""
    
    plt.figure(figsize=(12, 6))
    
    # Sort data for CDF
    sorted_data = np.sort(all_simulations)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    plt.plot(sorted_data, cdf, 'b-', linewidth=2, label='CDF')
    
    # Add vertical line at limit
    plt.axvline(x=regulatory_limit, color='red', linestyle='--', 
                linewidth=2, label=f'Limit = {regulatory_limit}')
    
    # Add horizontal line at exceedance probability
    plt.axhline(y=results['p_comply'], color='green', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    plt.axhline(y=results['p_exceed'], color='red', linestyle=':', 
                linewidth=1.5, alpha=0.7)
    
    # Add annotation for exceedance probability
    plt.annotate(f'P(Exceed) = {results["p_exceed"]*100:.1f}%', 
                 xy=(regulatory_limit + 2, results['p_exceed']),
                 fontsize=10, color='red')
    
    plt.xlabel('Emission Value (ppm)', fontsize=12)
    plt.ylabel('Cumulative Probability', fontsize=12)
    plt.title('Cumulative Distribution Function (CDF)', 
              fontsize=14, fontweight='bold')
    plt.legend(loc='lower right')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt.gcf()


def plot_confidence_vs_samples(results_list, sample_sizes):
    """Plot how confidence interval width changes with sample size"""
    
    plt.figure(figsize=(10, 6))
    
    ci_widths = [(r['percentile_97.5'] - r['percentile_2.5']) for r in results_list]
    
    plt.plot(sample_sizes, ci_widths, 'bo-', linewidth=2, markersize=8)
    plt.xlabel('Number of Samples', fontsize=12)
    plt.ylabel('95% Confidence Interval Width (ppm)', fontsize=12)
    plt.title('Effect of Sample Size on Uncertainty', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    return plt.gcf()


def plot_original_vs_simulated(samples, all_simulations, results):
    """Compare original samples with simulated distribution"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Original samples
    ax1.hist(samples, bins=10, color='steelblue', edgecolor='black', alpha=0.7)
    ax1.axvline(x=results['sample_mean'], color='blue', linestyle='--', 
                label=f'Mean = {results["sample_mean"]:.1f}')
    ax1.set_xlabel('Measured Value (ppm)')
    ax1.set_ylabel('Frequency')
    ax1.set_title(f'Original Samples (n={results["n_samples"]})')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Simulated distribution
    ax2.hist(all_simulations, bins=50, color='steelblue', edgecolor='black', alpha=0.7, density=True)
    ax2.axvline(x=results['mean'], color='blue', linestyle='--', 
                label=f'Mean = {results["mean"]:.1f}')
    ax2.axvspan(results['percentile_2.5'], results['percentile_97.5'], 
                alpha=0.2, color='gray', label='95% CI')
    ax2.set_xlabel('Possible True Value (ppm)')
    ax2.set_ylabel('Probability Density')
    ax2.set_title(f'Monte Carlo Simulation ({len(all_simulations):,} iterations)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.suptitle('Original Samples vs. Simulated Distribution', fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    return fig


# ================================================================
# STEP 5: REPORT GENERATION
# ================================================================

def print_results(results):
    """Print formatted results to console"""
    
    print("\n" + "=" * 60)
    print("MONTE CARLO SIMULATION RESULTS")
    print("=" * 60)
    
    print("\n📊 ORIGINAL SAMPLES STATISTICS:")
    print("-" * 40)
    print(f"   Number of samples:     {results['n_samples']}")
    print(f"   Sample mean:           {results['sample_mean']:.2f}")
    print(f"   Sample std deviation:  {results['sample_std']:.2f}")
    print(f"   Sample range:          [{results['sample_min']:.2f}, {results['sample_max']:.2f}]")
    
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
    print(f"   Decision:              {results['decision']}")
    
    print("\n" + "=" * 60)


def export_to_csv(all_simulations, results, filename="monte_carlo_results.csv"):
    """Export results to CSV file"""
    
    # Create DataFrame with simulated values
    df_sim = pd.DataFrame({'simulated_values': all_simulations})
    
    # Create DataFrame with statistics
    stats_data = {
        'Metric': ['Mean', 'Median', 'Std Dev', '2.5th Percentile', '5th Percentile', 
                   '95th Percentile', '97.5th Percentile', 'Probability Exceedance', 
                   'Probability Compliance', 'Sample Mean', 'Sample Std Dev', 'Number of Samples'],
        'Value': [results['mean'], results['median'], results['std'], 
                  results['percentile_2.5'], results['percentile_5'],
                  results['percentile_95'], results['percentile_97.5'],
                  results['p_exceed'], results['p_comply'],
                  results['sample_mean'], results['sample_std'], results['n_samples']]
    }
    df_stats = pd.DataFrame(stats_data)
    
    # Save to Excel with multiple sheets
    with pd.ExcelWriter(filename) as writer:
        df_sim.to_excel(writer, sheet_name='Simulated_Values', index=False)
        df_stats.to_excel(writer, sheet_name='Statistics', index=False)
    
    print(f"\n✅ Results exported to {filename}")


# ================================================================
# STEP 6: SAMPLE SIZE ANALYSIS
# ================================================================

def analyze_sample_size_effect(samples, uncertainty_percent, uncertainties, iterations_per_sample):
    """Analyze how results change with different sample sizes"""
    
    print("\n" + "=" * 60)
    print("SAMPLE SIZE EFFECT ANALYSIS")
    print("=" * 60)
    
    sample_sizes = [10, 20, 50, 100, 200, 500]
    results_list = []
    
    for size in sample_sizes:
        if size > len(samples):
            break
        
        # Take first 'size' samples
        sample_subset = samples[:size]
        
        # Run Monte Carlo
        sim = run_monte_carlo(sample_subset, uncertainty_percent, uncertainties, iterations_per_sample)
        
        # Calculate 95% CI width
        ci_lower = np.percentile(sim, 2.5)
        ci_upper = np.percentile(sim, 97.5)
        ci_width = ci_upper - ci_lower
        
        results_list.append({
            'size': size,
            'mean': np.mean(sim),
            'ci_width': ci_width,
            'p_exceed': np.mean(sim > regulatory_limit)
        })
        
        print(f"  {size} samples: Mean={np.mean(sim):.2f}, 95% CI width={ci_width:.2f}")
    
    return results_list, sample_sizes


# ================================================================
# STEP 7: MAIN EXECUTION
# ================================================================

if __name__ == "__main__":
    
    # Get user inputs
    samples = get_user_samples()
    uncertainty_percent, uncertainties = get_uncertainty()
    regulatory_limit = get_regulatory_limit()
    iterations_per_sample = get_simulation_parameters()
    
    # Display input summary
    print("\n" + "=" * 60)
    print("INPUT SUMMARY")
    print("=" * 60)
    print(f"Number of samples: {len(samples)}")
    print(f"Samples: {samples}")
    if uncertainty_percent is not None:
        print(f"Measurement uncertainty: ±{uncertainty_percent}%")
    else:
        print(f"Measurement uncertainty: Per-sample values")
    print(f"Regulatory limit: {regulatory_limit}")
    print(f"Iterations per sample: {iterations_per_sample:,}")
    
    # Run Monte Carlo
    all_simulations = run_monte_carlo(samples, uncertainty_percent, uncertainties, iterations_per_sample)
    
    # Analyze results
    results = analyze_results(all_simulations, regulatory_limit, samples)
    
    # Print results
    print_results(results)
    
    # Create visualizations
    print("\n" + "=" * 60)
    print("GENERATING VISUALIZATIONS")
    print("=" * 60)
    
    fig1 = plot_histogram(all_simulations, regulatory_limit, results)
    plt.show()
    
    fig2 = plot_cdf(all_simulations, regulatory_limit, results)
    plt.show()
    
    fig3 = plot_original_vs_simulated(samples, all_simulations, results)
    plt.show()
    
    # Ask if user wants sample size analysis
    if len(samples) >= 50:
        analyze = input("\nRun sample size effect analysis? (y/n): ")
        if analyze.lower() == 'y':
            results_list, sample_sizes = analyze_sample_size_effect(
                samples, uncertainty_percent, uncertainties, iterations_per_sample)
            fig4 = plot_confidence_vs_samples(results_list, sample_sizes)
            plt.show()
    
    # Export results
    export_choice = input("\nExport results to Excel? (y/n): ")
    if export_choice.lower() == 'y':
        export_to_csv(all_simulations, results)
    
    print("\n" + "=" * 60)
    print("SIMULATION COMPLETE")
    print("=" * 60)