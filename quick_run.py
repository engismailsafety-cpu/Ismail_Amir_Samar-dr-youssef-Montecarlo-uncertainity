"""
MONTE CARLO SIMULATION FOR EMISSION PREDICTION
Professional Web Application

Team:
- Ismail Kamal
- Amir Salem  
- Samar Zaitoun

Supervisor:
Dr. Mohamed Youssef
Master Program - Alexandria University

Version: 2.0
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import base64
from io import BytesIO

# ================================================================
# PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="Monte Carlo Simulation - Emission Predictor",
    page_icon="🎲",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================================================================
# CUSTOM CSS FOR PROFESSIONAL DESIGN
# ================================================================

st.markdown("""
<style>
    /* Main container styling */
    .main {
        background-color: #f0f2f6;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: bold;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: bold;
        color: #1e3c72;
        margin-bottom: 1rem;
        border-left: 4px solid #2a5298;
        padding-left: 1rem;
    }
    
    /* Metric card styling */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        border: none;
        padding: 0.5rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    /* Success/Info/Warning boxes */
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .info-box {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
        color: #666;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #f8f9fa;
    }
    
    /* Login form styling */
    .login-container {
        max-width: 400px;
        margin: 100px auto;
        padding: 2rem;
        background: white;
        border-radius: 15px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }
    
    .login-title {
        text-align: center;
        margin-bottom: 2rem;
        color: #1e3c72;
    }
    
    hr {
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ================================================================
# LOGIN FUNCTION
# ================================================================

def check_login():
    """Check if user is logged in"""
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        show_login_form()
        return False
    return True

def show_login_form():
    """Display login form"""
    
    st.markdown("""
    <div class="login-container">
        <div class="login-title">
            <h2>🎲 Monte Carlo Simulation</h2>
            <p>Environmental Emission Predictor</p>
            <hr>
            <h4>Login to Continue</h4>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        
        if st.button("🔐 Login", use_container_width=True):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password. Please try again.")
                st.info("Hint: Username: admin, Password: 1234")
    
    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.rerun()

# ================================================================
# IMAGE HANDLING (Base64 encoded image)
# ================================================================

def get_base64_image():
    """Return base64 encoded image for background or logo"""
    # This is a placeholder - you can replace with your actual image
    # For a chemical plant / refinery image
    return """
    <svg width="200" height="100" viewBox="0 0 200 100" xmlns="http://www.w3.org/2000/svg">
        <rect width="200" height="100" fill="#1e3c72"/>
        <rect x="20" y="40" width="30" height="50" fill="#ffd700"/>
        <rect x="60" y="30" width="30" height="60" fill="#ffd700"/>
        <rect x="100" y="20" width="30" height="70" fill="#ffd700"/>
        <rect x="140" y="35" width="30" height="55" fill="#ffd700"/>
        <circle cx="35" cy="35" r="8" fill="#ff4444"/>
        <circle cx="75" cy="25" r="8" fill="#ff4444"/>
        <circle cx="115" cy="15" r="8" fill="#ff4444"/>
        <circle cx="155" cy="30" r="8" fill="#ff4444"/>
        <text x="60" y="85" fill="white" font-size="12">Petrochemical Facility</text>
    </svg>
    """

# ================================================================
# SAMPLE PARSING FUNCTION
# ================================================================

def parse_samples(batch_text):
    """
    Parse batch text input into list of samples
    Supports: comma-separated, space-separated, newline-separated
    """
    if not batch_text:
        return []
    
    # Try different separators
    if ',' in batch_text:
        # Comma separated
        parts = batch_text.replace('\n', ',').split(',')
    elif ' ' in batch_text:
        # Space separated
        parts = batch_text.replace('\n', ' ').split()
    else:
        # Newline separated
        parts = batch_text.strip().split('\n')
    
    samples = []
    for part in parts:
        part = part.strip()
        if part:
            try:
                samples.append(float(part))
            except ValueError:
                continue
    
    return samples

def distribute_samples_to_fields(samples):
    """Distribute samples to individual input fields"""
    if 'sample_fields' not in st.session_state:
        st.session_state.sample_fields = []
    
    st.session_state.sample_fields = samples
    return st.session_state.sample_fields

# ================================================================
# MONTE CARLO SIMULATION FUNCTION
# ================================================================

def run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations_per_sample):
    """Run Monte Carlo simulation"""
    
    n_samples = len(samples)
    total_iterations = n_samples * iterations_per_sample
    
    all_simulations = []
    sample_contributions = []
    
    for measured in samples:
        sigma = measured * (uncertainty_percent / 100)
        simulated = np.random.normal(loc=measured, scale=sigma, size=iterations_per_sample)
        all_simulations.extend(simulated)
        sample_contributions.append({
            'measured': measured,
            'simulated': simulated,
            'mean': np.mean(simulated),
            'std': np.std(simulated)
        })
    
    all_simulations = np.array(all_simulations)
    
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
        'all_simulations': all_simulations,
        'samples': samples,
        'sample_contributions': sample_contributions,
        'uncertainty_percent': uncertainty_percent,
        'regulatory_limit': regulatory_limit
    }
    
    return results

# ================================================================
# VISUALIZATION FUNCTIONS
# ================================================================

def create_histogram(results):
    """Create histogram of simulated values"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(results['all_simulations'], bins=50, 
                                alpha=0.7, color='steelblue', 
                                edgecolor='black', density=True)
    
    # Color bars based on limit
    for i, (left, right) in enumerate(zip(bins[:-1], bins[1:])):
        if left >= results['regulatory_limit']:
            patches[i].set_facecolor('#dc3545')
            patches[i].set_alpha(0.7)
        elif right <= results['regulatory_limit']:
            patches[i].set_facecolor('#28a745')
            patches[i].set_alpha(0.5)
        else:
            patches[i].set_facecolor('#ffc107')
            patches[i].set_alpha(0.7)
    
    # Add vertical lines
    ax.axvline(x=results['regulatory_limit'], color='#dc3545', 
               linestyle='--', linewidth=2.5, 
               label=f'Regulatory Limit = {results["regulatory_limit"]}')
    
    ax.axvline(x=results['mean'], color='#1e3c72', 
               linestyle='-', linewidth=2.5, 
               label=f'Mean = {results["mean"]:.1f}')
    
    ax.axvline(x=results['median'], color='#17a2b8', 
               linestyle=':', linewidth=2, 
               label=f'Median = {results["median"]:.1f}')
    
    # Add confidence interval shading
    ax.axvspan(results['percentile_2.5'], results['percentile_97.5'], 
               alpha=0.15, color='gray', label='95% Confidence Interval')
    
    ax.set_xlabel('Emission Value (ppm)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Probability Density', fontsize=12, fontweight='bold')
    ax.set_title('Monte Carlo Simulation Results\nDistribution of Possible True Values', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='upper right', frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    return fig

def create_cdf_plot(results):
    """Create cumulative distribution function plot"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sorted_data = np.sort(results['all_simulations'])
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    ax.plot(sorted_data, cdf, 'b-', linewidth=2.5, label='Cumulative Distribution')
    
    ax.axvline(x=results['regulatory_limit'], color='#dc3545', 
               linestyle='--', linewidth=2.5, 
               label=f'Limit = {results["regulatory_limit"]}')
    
    ax.axhline(y=results['p_comply'], color='#28a745', 
               linestyle=':', linewidth=1.5, alpha=0.7)
    ax.axhline(y=results['p_exceed'], color='#dc3545', 
               linestyle=':', linewidth=1.5, alpha=0.7)
    
    # Add annotations
    ax.annotate(f'P(Exceed) = {results["p_exceed"]*100:.1f}%', 
                xy=(results['regulatory_limit'] + 2, results['p_exceed']),
                fontsize=10, color='#dc3545', fontweight='bold')
    
    ax.annotate(f'P(Comply) = {results["p_comply"]*100:.1f}%', 
                xy=(results['regulatory_limit'] - 10, results['p_comply']),
                fontsize=10, color='#28a745', fontweight='bold')
    
    ax.set_xlabel('Emission Value (ppm)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Cumulative Probability', fontsize=12, fontweight='bold')
    ax.set_title('Cumulative Distribution Function (CDF)', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend(loc='lower right', frameon=True, fancybox=True)
    ax.grid(True, alpha=0.3)
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    return fig

def create_sample_comparison_plot(results):
    """Compare original samples with simulated distribution"""
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Original samples histogram
    ax1.hist(results['samples'], bins=15, color='#1e3c72', 
             edgecolor='black', alpha=0.7)
    ax1.axvline(x=results['sample_mean'], color='#dc3545', 
                linestyle='--', linewidth=2, 
                label=f'Mean = {results["sample_mean"]:.1f}')
    ax1.set_xlabel('Measured Value (ppm)', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title(f'Original Samples (n = {results["n_samples"]})', 
                  fontsize=12, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_facecolor('#f8f9fa')
    
    # Simulated distribution
    ax2.hist(results['all_simulations'], bins=50, color='#28a745', 
             edgecolor='black', alpha=0.5, density=True)
    ax2.axvline(x=results['mean'], color='#1e3c72', 
                linestyle='-', linewidth=2, 
                label=f'Mean = {results["mean"]:.1f}')
    ax2.axvspan(results['percentile_2.5'], results['percentile_97.5'], 
                alpha=0.2, color='gray', label='95% CI')
    ax2.set_xlabel('Possible True Value (ppm)', fontsize=11)
    ax2.set_ylabel('Probability Density', fontsize=11)
    ax2.set_title(f'Monte Carlo Simulation ({results["total_iterations"]:,} iterations)', 
                  fontsize=12, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_facecolor('#f8f9fa')
    
    plt.suptitle('Original Samples vs. Simulated Distribution', 
                 fontsize=14, fontweight='bold', y=1.02)
    plt.tight_layout()
    
    return fig

def create_uncertainty_contribution_plot(results):
    """Show uncertainty contribution per sample"""
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    samples = results['samples']
    uncertainties = [s * results['uncertainty_percent'] / 100 for s in samples]
    
    x_pos = np.arange(len(samples))
    
    bars = ax.bar(x_pos, uncertainties, color='#17a2b8', alpha=0.7, edgecolor='black')
    
    # Color code bars based on value
    for i, (bar, sample) in enumerate(zip(bars, samples)):
        if sample > results['regulatory_limit']:
            bar.set_color('#dc3545')
        elif sample < results['regulatory_limit'] * 0.8:
            bar.set_color('#28a745')
    
    ax.axhline(y=results['regulatory_limit'] * results['uncertainty_percent'] / 100,
               color='#dc3545', linestyle='--', linewidth=2, 
               label='Uncertainty at Limit')
    
    ax.set_xlabel('Sample Number', fontsize=12, fontweight='bold')
    ax.set_ylabel('Measurement Uncertainty (± ppm)', fontsize=12, fontweight='bold')
    ax.set_title('Uncertainty Contribution per Sample', 
                 fontsize=14, fontweight='bold', pad=20)
    ax.legend()
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_facecolor('#f8f9fa')
    
    plt.tight_layout()
    return fig

# ================================================================
# MAIN APPLICATION
# ================================================================

def main():
    """Main application function"""
    
    # Check login
    if not check_login():
        return
    
    # Header with image and title
    st.markdown(f"""
    <div class="main-header">
        <h1>🎲 Monte Carlo Simulation</h1>
        <p>Environmental Emission Predictor for Petrochemical Facilities</p>
        <p style="font-size: 0.9rem; margin-top: 1rem;">Under Supervision of Dr. Mohamed Youssef | Master Program - Alexandria University</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Team information
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem; background: #e8f4f8; border-radius: 10px;">
            <strong>👨‍💻 Ismail Kamal</strong>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem; background: #e8f4f8; border-radius: 10px;">
            <strong>👨‍💻 Amir Salem</strong>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style="text-align: center; padding: 0.5rem; background: #e8f4f8; border-radius: 10px;">
            <strong>👩‍💻 Samar Zaitoun</strong>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Sidebar for inputs
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <h3>⚙️ Simulation Parameters</h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Batch sample input
        st.markdown("### 📝 Batch Sample Input")
        st.markdown("Paste all sample values (comma, space, or newline separated):")
        
        batch_input = st.text_area(
            "Sample Values",
            placeholder="Example: 95, 102, 88, 110, 97, 105, 92, 108, 99, 101\nOr:\n95\n102\n88\n110\n97",
            height=150
        )
        
        if st.button("📋 Parse & Distribute Samples", use_container_width=True):
            parsed_samples = parse_samples(batch_input)
            if len(parsed_samples) >= 3:
                st.session_state.samples = parsed_samples
                st.success(f"✅ Parsed {len(parsed_samples)} samples successfully!")
                st.rerun()
            else:
                st.error(f"⚠️ Only {len(parsed_samples)} samples detected. Minimum 3 samples required.")
        
        st.markdown("---")
        
        # Individual sample inputs
        st.markdown("### 🔢 Individual Sample Values")
        
        if 'samples' not in st.session_state:
            st.session_state.samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]
        
        # Dynamic sample fields
        n_samples = st.number_input("Number of samples", min_value=3, max_value=50, 
                                     value=len(st.session_state.samples), step=1)
        
        if n_samples != len(st.session_state.samples):
            # Adjust sample list size
            current = st.session_state.samples
            if n_samples > len(current):
                current.extend([100] * (n_samples - len(current)))
            else:
                current = current[:n_samples]
            st.session_state.samples = current
        
        # Display individual fields
        sample_values = []
        cols = st.columns(3)
        for i in range(n_samples):
            col_idx = i % 3
            with cols[col_idx]:
                val = st.number_input(f"Sample {i+1}", value=float(st.session_state.samples[i]), 
                                       step=1.0, key=f"sample_{i}")
                sample_values.append(val)
        
        st.session_state.samples = sample_values
        
        st.markdown("---")
        
        # Simulation parameters
        st.markdown("### 🎯 Simulation Settings")
        
        uncertainty_percent = st.slider("Measurement Uncertainty (%)", 1, 20, 5, 
                                         help="Typical CEMS accuracy: ±5%")
        
        regulatory_limit = st.number_input("Regulatory Limit (ppm)", value=100.0, step=5.0)
        
        iterations_per_sample = st.selectbox("Iterations per sample", 
                                               [1000, 5000, 10000, 50000], 
                                               index=2)
        
        run_button = st.button("🚀 Run Monte Carlo Simulation", use_container_width=True, type="primary")
    
    # Main content area
    if run_button:
        samples = st.session_state.samples
        
        if len(samples) < 3:
            st.warning("⚠️ Please enter at least 3 samples before running simulation.")
        else:
            with st.spinner("Running Monte Carlo simulation... This may take a few seconds."):
                
                # Run simulation
                results = run_monte_carlo(samples, uncertainty_percent, 
                                          regulatory_limit, iterations_per_sample)
                
                # Store results in session state
                st.session_state.results = results
                
                # Display summary metrics
                st.markdown("## 📊 Simulation Results Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{results['mean']:.1f}</div>
                        <div class="metric-label">Mean Emission (ppm)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{results['median']:.1f}</div>
                        <div class="metric-label">Median Emission (ppm)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">±{results['std']:.1f}</div>
                        <div class="metric-label">Standard Deviation</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    exceed_color = "#dc3545" if results['p_exceed'] > 0.5 else "#28a745"
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, {exceed_color} 0%, #555 100%);">
                        <div class="metric-value">{results['p_exceed']*100:.1f}%</div>
                        <div class="metric-label">Probability > Limit</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Confidence intervals
                st.markdown("---")
                st.markdown("## 📈 Confidence Intervals")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"""
                    ### 90% Confidence Interval
                    **[{results['percentile_5']:.2f}, {results['percentile_95']:.2f}]** ppm
                    
                    We are 90% confident that the true emission value lies within this range.
                    """)
                
                with col2:
                    st.success(f"""
                    ### 95% Confidence Interval
                    **[{results['percentile_2.5']:.2f}, {results['percentile_97.5']:.2f}]** ppm
                    
                    We are 95% confident that the true emission value lies within this range.
                    """)
                
                # Regulatory decision
                st.markdown("---")
                st.markdown("## ⚖️ Regulatory Decision")
                
                if results['p_exceed'] < 0.05:
                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ SAFE ZONE - Declare Compliant</h3>
                        <p>The probability of exceeding the regulatory limit is less than 5%. 
                        The facility is considered compliant with regulations.</p>
                        <p><strong>Recommended Action:</strong> Continue routine monitoring.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif results['p_exceed'] > 0.95:
                    st.markdown("""
                    <div class="warning-box" style="border-left-color: #dc3545;">
                        <h3>❌ VIOLATION ZONE - Declare Non-Compliant</h3>
                        <p>The probability of exceeding the regulatory limit is greater than 95%. 
                        The facility is in violation of regulations.</p>
                        <p><strong>Recommended Action:</strong> Immediate enforcement action required.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                        <h3>⚠️ UNCERTAIN ZONE - Need More Data</h3>
                        <p>The probability of exceeding the regulatory limit is between 5% and 95%. 
                        The compliance status cannot be determined with confidence.</p>
                        <p><strong>Recommended Action:</strong> Collect additional samples or install continuous monitoring.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Detailed statistics
                st.markdown("---")
                st.markdown("## 📋 Detailed Statistics")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("### Original Samples")
                    st.write(f"- **Number of samples:** {results['n_samples']}")
                    st.write(f"- **Sample mean:** {results['sample_mean']:.2f} ppm")
                    st.write(f"- **Sample std deviation:** {results['sample_std']:.2f} ppm")
                    st.write(f"- **Sample range:** [{results['sample_min']:.2f}, {results['sample_max']:.2f}] ppm")
                
                with col2:
                    st.markdown("### Monte Carlo Results")
                    st.write(f"- **Total iterations:** {results['total_iterations']:,}")
                    st.write(f"- **Simulation mean:** {results['mean']:.2f} ppm")
                    st.write(f"- **Simulation median:** {results['median']:.2f} ppm")
                    st.write(f"- **Simulation std:** {results['std']:.2f} ppm")
                    st.write(f"- **Total range:** [{results['min']:.2f}, {results['max']:.2f}] ppm")
                
                # Visualizations
                st.markdown("---")
                st.markdown("## 📊 Visualizations")
                
                tab1, tab2, tab3, tab4 = st.tabs(["📈 Histogram", "📉 CDF Plot", "📊 Sample Comparison", "🎯 Uncertainty Contribution"])
                
                with tab1:
                    fig1 = create_histogram(results)
                    st.pyplot(fig1)
                    plt.close(fig1)
                
                with tab2:
                    fig2 = create_cdf_plot(results)
                    st.pyplot(fig2)
                    plt.close(fig2)
                
                with tab3:
                    fig3 = create_sample_comparison_plot(results)
                    st.pyplot(fig3)
                    plt.close(fig3)
                
                with tab4:
                    fig4 = create_uncertainty_contribution_plot(results)
                    st.pyplot(fig4)
                    plt.close(fig4)
                
                # Sample values table
                st.markdown("---")
                st.markdown("## 📋 Sample Values Summary")
                
                sample_df = pd.DataFrame({
                    'Sample #': range(1, len(results['samples']) + 1),
                    'Measured Value (ppm)': results['samples'],
                    'Uncertainty (± ppm)': [s * uncertainty_percent / 100 for s in results['samples']],
                    '95% CI Lower': [s - 1.96 * s * uncertainty_percent / 100 for s in results['samples']],
                    '95% CI Upper': [s + 1.96 * s * uncertainty_percent / 100 for s in results['samples']]
                })
                
                st.dataframe(sample_df, use_container_width=True, hide_index=True)
                
                # Download results
                st.markdown("---")
                st.markdown("## 📥 Download Results")
                
                # Prepare download data
                download_df = pd.DataFrame({
                    'simulated_values': results['all_simulations']
                })
                
                csv = download_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download Simulated Values (CSV)",
                    data=csv,
                    file_name=f"monte_carlo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
                
    else:
        st.info("👈 **Welcome!** Please configure your simulation parameters in the sidebar and click 'Run Monte Carlo Simulation' to begin.")
        
        # Show example
        with st.expander("ℹ️ How to use this application"):
            st.markdown("""
            ### Step-by-Step Guide:
            
            1. **Enter Samples**: Either paste all samples in batch input or enter them individually
            2. **Click "Parse & Distribute"** to automatically fill individual fields
            3. **Set Uncertainty**: Adjust measurement uncertainty (typical CEMS: ±5%)
            4. **Set Regulatory Limit**: Enter the compliance threshold
            5. **Run Simulation**: Click the button to start Monte Carlo simulation
            6. **Review Results**: Analyze statistics, visualizations, and regulatory decision
            
            ### Sample Data Format:
            - Comma separated: `95, 102, 88, 110, 97`
            - Space separated: `95 102 88 110 97`
            - Newline separated: each value on a new line
            """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2024 Monte Carlo Simulation Tool | Developed by Ismail Kamal, Amir Salem, Samar Zaitoun</p>
        <p>Under Supervision of Dr. Mohamed Youssef | Master Program - Alexandria University</p>
        <p style="font-size: 0.8rem;">References: ISO 14064-1:2018 | Cullen, A.C., & Frey, H.C. (1999)</p>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# RUN APPLICATION
# ================================================================

if __name__ == "__main__":
    main()
