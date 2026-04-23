"""
MONTE CARLO SIMULATION FOR EMISSION PREDICTION
Complete Working Version - No Errors

Team:
- Ismail Kamal
- Amir Salem  
- Samar Zaitoun

Supervisor: Dr. Mohamed Youssef
Master Program - Alexandria University
"""

import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io

# ================================================================
# PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="Monte Carlo Simulation - Emission Predictor",
    page_icon="🎲",
    layout="wide"
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
    
    .danger-box {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
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
    
    /* Login form styling */
    .login-container {
        max-width: 450px;
        margin: 80px auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    .login-logo {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    hr {
        margin: 1.5rem 0;
    }
    
    /* Team card */
    .team-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        margin: 0.3rem;
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
    """Display login form with image"""
    
    st.markdown("""
    <div class="login-container">
        <div class="login-logo">
            🎲🏭📊
        </div>
        <h1 style="color: #1e3c72;">Monte Carlo Simulation</h1>
        <p style="color: #666;">Environmental Emission Predictor</p>
        <p style="color: #888; font-size: 0.8rem;">for Petrochemical Facilities</p>
        <hr>
        <h3>Login to Continue</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("👤 Username", placeholder="Enter your username")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        if st.button("🔐 Login", use_container_width=True):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")
                st.info("ℹ️ Hint: Username: **admin**, Password: **1234**")
    
    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.rerun()

# ================================================================
# DEFAULT SAMPLES (as requested)
# ================================================================

DEFAULT_SAMPLES = [160, 195, 180, 188, 175, 192, 182, 186, 178, 204]
DEFAULT_LIMIT = 200

# ================================================================
# SAMPLE PARSING FUNCTION
# ================================================================

def parse_samples(batch_text):
    """Parse batch text input into list of samples"""
    if not batch_text:
        return []
    
    # Try different separators
    if ',' in batch_text:
        parts = batch_text.replace('\n', ',').split(',')
    elif ' ' in batch_text:
        parts = batch_text.replace('\n', ' ').split()
    else:
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

def load_from_excel(uploaded_file):
    """Load samples from Excel file"""
    try:
        df = pd.read_excel(uploaded_file)
        # Try to find numeric columns
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            samples = df[numeric_cols[0]].dropna().tolist()
            return samples
        else:
            return []
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
        return []

# ================================================================
# MONTE CARLO SIMULATION FUNCTION
# ================================================================

def run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations_per_sample):
    """Run Monte Carlo simulation"""
    
    n_samples = len(samples)
    total_iterations = n_samples * iterations_per_sample
    
    all_simulations = []
    
    for measured in samples:
        sigma = measured * (uncertainty_percent / 100)
        simulated = np.random.normal(loc=measured, scale=sigma, size=iterations_per_sample)
        all_simulations.extend(simulated)
    
    all_simulations = np.array(all_simulations)
    
    results = {
        'mean': float(np.mean(all_simulations)),
        'median': float(np.median(all_simulations)),
        'std': float(np.std(all_simulations)),
        'min': float(np.min(all_simulations)),
        'max': float(np.max(all_simulations)),
        'percentile_2.5': float(np.percentile(all_simulations, 2.5)),
        'percentile_5': float(np.percentile(all_simulations, 5)),
        'percentile_95': float(np.percentile(all_simulations, 95)),
        'percentile_97.5': float(np.percentile(all_simulations, 97.5)),
        'p_exceed': float(np.mean(all_simulations > regulatory_limit)),
        'p_comply': float(np.mean(all_simulations <= regulatory_limit)),
        'sample_mean': float(np.mean(samples)),
        'sample_std': float(np.std(samples)),
        'sample_min': float(min(samples)),
        'sample_max': float(max(samples)),
        'n_samples': n_samples,
        'total_iterations': total_iterations,
        'samples': samples,
        'uncertainty_percent': uncertainty_percent,
        'regulatory_limit': regulatory_limit,
        'all_simulations': all_simulations.tolist()
    }
    
    return results

# ================================================================
# HISTOGRAM FUNCTION (FIXED - NO KEY ERROR)
# ================================================================

def create_histogram(results):
    """Create matplotlib histogram"""
    
    # Extract data safely
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    mean_val = results['mean']
    median_val = results['median']
    ci_lower = results['percentile_2.5']
    ci_upper = results['percentile_97.5']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Create histogram
    n, bins, patches = ax.hist(all_simulations, bins=50, alpha=0.7, 
                                color='steelblue', edgecolor='black', density=True)
    
    # Color bars based on limit
    for i, (left, right) in enumerate(zip(bins[:-1], bins[1:])):
        if left >= regulatory_limit:
            patches[i].set_facecolor('#dc3545')
            patches[i].set_alpha(0.7)
        elif right <= regulatory_limit:
            patches[i].set_facecolor('#28a745')
            patches[i].set_alpha(0.5)
        else:
            patches[i].set_facecolor('#ffc107')
            patches[i].set_alpha(0.7)
    
    # Add vertical lines
    ax.axvline(x=regulatory_limit, color='#dc3545', linestyle='--', 
               linewidth=2.5, label=f'Regulatory Limit = {regulatory_limit}')
    
    ax.axvline(x=mean_val, color='#1e3c72', linestyle='-', 
               linewidth=2.5, label=f'Mean = {mean_val:.1f}')
    
    ax.axvline(x=median_val, color='#17a2b8', linestyle=':', 
               linewidth=2, label=f'Median = {median_val:.1f}')
    
    # Add confidence interval shading
    ax.axvspan(ci_lower, ci_upper, alpha=0.15, color='gray', 
               label=f'95% CI: [{ci_lower:.1f}, {ci_upper:.1f}]')
    
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
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    p_comply = results['p_comply']
    p_exceed = results['p_exceed']
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    sorted_data = np.sort(all_simulations)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    ax.plot(sorted_data, cdf, 'b-', linewidth=2.5, label='Cumulative Distribution')
    
    ax.axvline(x=regulatory_limit, color='#dc3545', linestyle='--', 
               linewidth=2.5, label=f'Limit = {regulatory_limit}')
    
    ax.axhline(y=p_comply, color='#28a745', linestyle=':', linewidth=1.5, alpha=0.7)
    ax.axhline(y=p_exceed, color='#dc3545', linestyle=':', linewidth=1.5, alpha=0.7)
    
    ax.annotate(f'P(Exceed) = {p_exceed*100:.1f}%', 
                xy=(regulatory_limit + 5, p_exceed),
                fontsize=10, color='#dc3545', fontweight='bold')
    
    ax.annotate(f'P(Comply) = {p_comply*100:.1f}%', 
                xy=(regulatory_limit - 20, p_comply),
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

def create_boxplot(results):
    """Create boxplot of results"""
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bp = ax.boxplot([all_simulations], patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#667eea')
    bp['boxes'][0].set_alpha(0.7)
    
    ax.axhline(y=regulatory_limit, color='#dc3545', linestyle='--', 
               linewidth=2, label=f'Regulatory Limit = {regulatory_limit}')
    
    ax.set_xticklabels(['Simulated Values'])
    ax.set_ylabel('Emission Value (ppm)', fontsize=12, fontweight='bold')
    ax.set_title('Boxplot of Simulated Values', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

# ================================================================
# TEXT VISUALIZATION (FIXED - SAFE)
# ================================================================

def display_text_histogram(results):
    """Display text-based histogram - SAFE VERSION"""
    
    st.markdown("### 📊 Distribution of Simulated Values")
    
    # Safely extract data
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    
    if len(all_simulations) == 0:
        st.warning("No simulation data available.")
        return
    
    min_val = float(np.min(all_simulations))
    max_val = float(np.max(all_simulations))
    
    # Create bins
    bins = np.linspace(min_val, max_val, 15)
    hist, bin_edges = np.histogram(all_simulations, bins=bins)
    max_freq = float(np.max(hist)) if len(hist) > 0 else 1
    width = 40
    scale = width / max_freq if max_freq > 0 else 1
    
    # Build histogram text
    histogram_lines = []
    for i in range(len(hist)):
        bar_length = int(hist[i] * scale)
        bar = '█' * bar_length
        
        left = bin_edges[i]
        right = bin_edges[i+1]
        
        if left >= regulatory_limit:
            prefix = '🔴'
        elif right <= regulatory_limit:
            prefix = '🟢'
        else:
            prefix = '🟡'
        
        histogram_lines.append(f"{prefix} {left:6.1f} - {right:6.1f} | {bar}")
    
    st.code('\n'.join(histogram_lines))
    st.caption("🟢 = Below limit | 🟡 = Crosses limit | 🔴 = Above limit")
    st.caption(f"Regulatory Limit = {regulatory_limit}")

def display_text_cdf(results):
    """Display text-based CDF table"""
    
    st.markdown("### 📈 Cumulative Distribution Table")
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    
    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    cdf_data = []
    
    for p in percentiles:
        value = np.percentile(all_simulations, p)
        cdf_data.append({
            'Percentile': f"{p}%",
            'Value (ppm)': f"{value:.2f}"
        })
    
    df_cdf = pd.DataFrame(cdf_data)
    st.dataframe(df_cdf, hide_index=True, use_container_width=True)
    
    st.info(f"**At Regulatory Limit ({regulatory_limit} ppm):**\n\n" + 
            f"📊 Probability of Compliance: **{results['p_comply']*100:.1f}%**\n" +
            f"⚠️ Probability of Exceedance: **{results['p_exceed']*100:.1f}%**")

def display_sample_table(results, uncertainty_percent):
    """Display sample values table"""
    
    sample_data = []
    for i, sample in enumerate(results['samples']):
        uncertainty = sample * uncertainty_percent / 100
        sample_data.append({
            'Sample #': i + 1,
            'Measured Value (ppm)': f"{sample:.2f}",
            'Uncertainty (± ppm)': f"{uncertainty:.2f}",
            '95% CI Lower': f"{sample - 1.96 * uncertainty:.2f}",
            '95% CI Upper': f"{sample + 1.96 * uncertainty:.2f}"
        })
    
    df_samples = pd.DataFrame(sample_data)
    st.dataframe(df_samples, hide_index=True, use_container_width=True)

def display_statistics_table(results):
    """Display statistics in table format"""
    
    stats_data = [
        {'Metric': '📊 Sample Mean', 'Value': f"{results['sample_mean']:.2f} ppm"},
        {'Metric': '📐 Sample Std Dev', 'Value': f"{results['sample_std']:.2f} ppm"},
        {'Metric': '📏 Sample Range', 'Value': f"[{results['sample_min']:.2f}, {results['sample_max']:.2f}] ppm"},
        {'Metric': '🔢 Number of Samples', 'Value': str(results['n_samples'])},
        {'Metric': '🎯 Simulation Mean', 'Value': f"{results['mean']:.2f} ppm"},
        {'Metric': '📊 Simulation Median', 'Value': f"{results['median']:.2f} ppm"},
        {'Metric': '📐 Simulation Std Dev', 'Value': f"{results['std']:.2f} ppm"},
        {'Metric': '🔄 Total Iterations', 'Value': f"{results['total_iterations']:,}"},
        {'Metric': '📈 90% Confidence Interval', 'Value': f"[{results['percentile_5']:.2f}, {results['percentile_95']:.2f}] ppm"},
        {'Metric': '📊 95% Confidence Interval', 'Value': f"[{results['percentile_2.5']:.2f}, {results['percentile_97.5']:.2f}] ppm"},
    ]
    
    df_stats = pd.DataFrame(stats_data)
    st.dataframe(df_stats, hide_index=True, use_container_width=True)

# ================================================================
# MAIN APPLICATION
# ================================================================

def main():
    """Main application function"""
    
    # Check login
    if not check_login():
        return
    
    # Header with image
    st.markdown("""
    <div class="main-header">
        <h1>🎲 Monte Carlo Simulation</h1>
        <p>Environmental Emission Predictor for Petrochemical Facilities</p>
        <p style="font-size: 0.9rem;">Advanced Uncertainty Analysis Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Team information
    st.markdown("### 👥 Research Team")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1:
        st.markdown("""
        <div class="team-card">
            <strong>👨‍💻 Ismail Kamal</strong>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="team-card">
            <strong>👨‍💻 Amir Salem</strong>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="team-card">
            <strong>👩‍💻 Samar Zaitoun</strong>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="team-card">
            <strong>👨‍🏫 Dr. Mohamed Youssef</strong><br>
            <small>Supervisor</small>
        </div>
        """, unsafe_allow_html=True)
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    # Initialize session state for samples
    if 'samples' not in st.session_state:
        st.session_state.samples = DEFAULT_SAMPLES.copy()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Simulation Parameters")
        
        # Data input method
        st.markdown("### 📂 Data Input")
        input_method = st.radio(
            "Choose input method:",
            ["📝 Manual Entry", "📋 Batch Paste", "📎 Excel Upload"],
            horizontal=True
        )
        
        if input_method == "📋 Batch Paste":
            st.markdown("#### Paste your samples:")
            batch_input = st.text_area(
                "Values (comma, space, or newline separated):",
                placeholder="160, 195, 180, 188, 175, 192, 182, 186, 178, 204",
                height=100
            )
            if st.button("📋 Parse & Load", use_container_width=True):
                parsed = parse_samples(batch_input)
                if len(parsed) >= 3:
                    st.session_state.samples = parsed
                    st.success(f"✅ Loaded {len(parsed)} samples!")
                    st.rerun()
                else:
                    st.error(f"⚠️ Only {len(parsed)} samples. Need at least 3.")
        
        elif input_method == "📎 Excel Upload":
            st.markdown("#### Upload Excel file:")
            uploaded_file = st.file_uploader("Choose Excel file", type=['xlsx', 'xls'])
            if uploaded_file is not None:
                samples = load_from_excel(uploaded_file)
                if len(samples) >= 3:
                    st.session_state.samples = samples
                    st.success(f"✅ Loaded {len(samples)} samples from Excel!")
                    st.rerun()
                elif len(samples) > 0:
                    st.error(f"⚠️ Only {len(samples)} samples. Need at least 3.")
                else:
                    st.error("No numeric data found in Excel file.")
        
        else:  # Manual Entry
            st.markdown("#### Manual Entry")
            
            n_samples = st.number_input(
                "Number of samples:", 
                min_value=3, 
                max_value=50, 
                value=len(st.session_state.samples), 
                step=1
            )
            
            # Adjust sample list size
            current = st.session_state.samples.copy()
            if n_samples > len(current):
                current.extend([current[-1] if current else 160] * (n_samples - len(current)))
            else:
                current = current[:n_samples]
            
            # Display individual fields
            st.markdown("#### Enter sample values:")
            sample_values = []
            cols = st.columns(4)
            for i in range(n_samples):
                col_idx = i % 4
                with cols[col_idx]:
                    val = st.number_input(
                        f"#{i+1}", 
                        value=float(current[i]), 
                        step=1.0, 
                        key=f"s_{i}",
                        label_visibility="collapsed"
                    )
                    sample_values.append(val)
            
            st.session_state.samples = sample_values
        
        st.markdown("---")
        
        # Default samples button
        if st.button("🔄 Reset to Default Samples", use_container_width=True):
            st.session_state.samples = DEFAULT_SAMPLES.copy()
            st.success(f"✅ Reset to {len(DEFAULT_SAMPLES)} default samples!")
            st.rerun()
        
        st.markdown("---")
        
        # Simulation settings
        st.markdown("### 🎯 Simulation Settings")
        uncertainty_percent = st.slider("Measurement Uncertainty (%)", 1, 20, 5, 
                                         help="Typical CEMS accuracy: ±5%")
        regulatory_limit = st.number_input("Regulatory Limit (ppm)", value=DEFAULT_LIMIT, step=5.0)
        iterations_per_sample = st.selectbox("Iterations per sample", [1000, 5000, 10000, 50000], index=2)
        
        st.markdown("---")
        
        # Display current samples info
        st.markdown("### 📊 Current Samples")
        st.write(f"**Count:** {len(st.session_state.samples)}")
        st.write(f"**Mean:** {np.mean(st.session_state.samples):.2f}")
        st.write(f"**Range:** [{min(st.session_state.samples):.2f}, {max(st.session_state.samples):.2f}]")
        
        run_button = st.button("🚀 Run Monte Carlo Simulation", use_container_width=True, type="primary")
    
    # Main content area
    if run_button:
        samples = st.session_state.samples
        
        if len(samples) < 3:
            st.warning("⚠️ Please enter at least 3 samples before running simulation.")
        else:
            with st.spinner("Running Monte Carlo simulation... This may take a few seconds."):
                
                # Run simulation
                results = run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations_per_sample)
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
                    <div class="danger-box">
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
                display_statistics_table(results)
                
                # Sample values table
                st.markdown("---")
                st.markdown("## 📋 Sample Values Summary")
                display_sample_table(results, uncertainty_percent)
                
                # Visualizations
                st.markdown("---")
                st.markdown("## 📊 Visualizations")
                
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogram", "📈 CDF Plot", "📦 Boxplot", "📝 Text View"])
                
                with tab1:
                    st.markdown("### Distribution of Simulated Values")
                    fig1 = create_histogram(results)
                    st.pyplot(fig1)
                    plt.close(fig1)
                
                with tab2:
                    st.markdown("### Cumulative Distribution Function")
                    fig2 = create_cdf_plot(results)
                    st.pyplot(fig2)
                    plt.close(fig2)
                
                with tab3:
                    st.markdown("### Boxplot of Simulated Values")
                    fig3 = create_boxplot(results)
                    st.pyplot(fig3)
                    plt.close(fig3)
                
                with tab4:
                    display_text_histogram(results)
                    display_text_cdf(results)
                
                # Download results
                st.markdown("---")
                st.markdown("## 📥 Download Results")
                
                # Create download data
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
        
        # Show default samples
        with st.expander("📋 View Default Samples"):
            st.write(f"**Default Samples ({len(DEFAULT_SAMPLES)} samples):**")
            st.write(DEFAULT_SAMPLES)
            st.write(f"**Default Regulatory Limit:** {DEFAULT_LIMIT} ppm")
            st.write(f"**Sample Mean:** {np.mean(DEFAULT_SAMPLES):.2f} ppm")
            st.write(f"**Sample Std Dev:** {np.std(DEFAULT_SAMPLES):.2f} ppm")
        
        with st.expander("ℹ️ How to use this application"):
            st.markdown("""
            ### Step-by-Step Guide:
            
            1. **Enter Samples**: Choose one of three methods:
               - Manual Entry: Set number of samples and enter values
               - Batch Paste: Copy-paste all values at once
               - Excel Upload: Upload Excel file with samples
            
            2. **Set Parameters**:
               - Measurement Uncertainty (typical CEMS: ±5%)
               - Regulatory Limit (default: 200 ppm)
               - Iterations per sample (more = more accurate)
            
            3. **Run Simulation**: Click the button to start
            
            4. **Review Results**:
               - Summary metrics (mean, median, probability)
               - Confidence intervals
               - Regulatory decision
               - Visualizations (Histogram, CDF, Boxplot)
            
            ### Sample Data Formats:
            - Comma separated: `160, 195, 180, 188, 175`
            - Space separated: `160 195 180 188 175`
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
