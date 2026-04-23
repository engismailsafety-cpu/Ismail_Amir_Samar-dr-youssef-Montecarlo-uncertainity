"""
MONTE CARLO SIMULATION FOR EMISSION PREDICTION
Text-Based Version - No matplotlib required
Works on any Streamlit Cloud environment

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
from datetime import datetime

# ================================================================
# PAGE CONFIGURATION
# ================================================================

st.set_page_config(
    page_title="Monte Carlo Simulation - Emission Predictor",
    page_icon="🎲",
    layout="wide"
)

# ================================================================
# CUSTOM CSS
# ================================================================

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
    }
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 10px;
    }
    .warning-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 10px;
    }
    .danger-box {
        background: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 10px;
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
    <div style="max-width: 400px; margin: 100px auto; padding: 2rem; 
                background: white; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
        <div style="text-align: center;">
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
                st.error("❌ Invalid username or password.")
                st.info("Hint: Username: admin, Password: 1234")
    
    st.markdown("</div>", unsafe_allow_html=True)

def logout():
    """Logout function"""
    st.session_state.logged_in = False
    st.rerun()

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

# ================================================================
# MONTE CARLO SIMULATION
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
        'samples': samples,
        'uncertainty_percent': uncertainty_percent,
        'regulatory_limit': regulatory_limit
    }
    
    return results

# ================================================================
# TEXT VISUALIZATION FUNCTIONS
# ================================================================

def display_text_histogram(results, width=50):
    """Display text-based histogram"""
    
    st.markdown("### 📊 Distribution of Simulated Values")
    
    min_val = results['min']
    max_val = results['max']
    bins = np.linspace(min_val, max_val, 15)
    
    hist, bin_edges = np.histogram(results['all_simulations'], bins=bins)
    max_freq = max(hist)
    scale = width / max_freq if max_freq > 0 else 1
    
    histogram_data = []
    for i in range(len(hist)):
        bar_length = int(hist[i] * scale)
        bar = '█' * bar_length
        
        if bin_edges[i] >= results['regulatory_limit']:
            prefix = '🔴'
        elif bin_edges[i+1] <= results['regulatory_limit']:
            prefix = '🟢'
        else:
            prefix = '🟡'
        
        histogram_data.append({
            'Range': f"{bin_edges[i]:.1f} - {bin_edges[i+1]:.1f}",
            'Distribution': bar,
            'Status': prefix
        })
    
    df_hist = pd.DataFrame(histogram_data)
    st.code('\n'.join([f"{row['Status']} {row['Range']:>15} | {row['Distribution']}" for _, row in df_hist.iterrows()]))
    st.caption("🟢 = Below limit | 🟡 = Crosses limit | 🔴 = Above limit")

def display_text_cdf(results):
    """Display text-based CDF table"""
    
    st.markdown("### 📈 Cumulative Distribution")
    
    percentiles = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    cdf_data = []
    
    for p in percentiles:
        value = np.percentile(results['all_simulations'], p)
        cdf_data.append({
            'Percentile': f"{p}%",
            'Value (ppm)': f"{value:.2f}"
        })
    
    df_cdf = pd.DataFrame(cdf_data)
    st.dataframe(df_cdf, hide_index=True, use_container_width=True)
    
    st.info(f"**At Regulatory Limit ({results['regulatory_limit']} ppm):**\n\n" + 
            f"Probability of Compliance: {results['p_comply']*100:.1f}%\n" +
            f"Probability of Exceedance: {results['p_exceed']*100:.1f}%")

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
        {'Metric': 'Sample Mean', 'Value': f"{results['sample_mean']:.2f} ppm"},
        {'Metric': 'Sample Std Dev', 'Value': f"{results['sample_std']:.2f} ppm"},
        {'Metric': 'Sample Range', 'Value': f"[{results['sample_min']:.2f}, {results['sample_max']:.2f}] ppm"},
        {'Metric': 'Number of Samples', 'Value': str(results['n_samples'])},
        {'Metric': 'Simulation Mean', 'Value': f"{results['mean']:.2f} ppm"},
        {'Metric': 'Simulation Median', 'Value': f"{results['median']:.2f} ppm"},
        {'Metric': 'Simulation Std Dev', 'Value': f"{results['std']:.2f} ppm"},
        {'Metric': 'Total Iterations', 'Value': f"{results['total_iterations']:,}"},
        {'Metric': '90% CI', 'Value': f"[{results['percentile_5']:.2f}, {results['percentile_95']:.2f}] ppm"},
        {'Metric': '95% CI', 'Value': f"[{results['percentile_2.5']:.2f}, {results['percentile_97.5']:.2f}] ppm"},
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
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🎲 Monte Carlo Simulation</h1>
        <p>Environmental Emission Predictor for Petrochemical Facilities</p>
        <p style="font-size: 0.9rem;">Under Supervision of Dr. Mohamed Youssef | Master Program - Alexandria University</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Team information and logout
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1:
        st.markdown("**👨‍💻 Ismail Kamal**")
    with col2:
        st.markdown("**👨‍💻 Amir Salem**")
    with col3:
        st.markdown("**👩‍💻 Samar Zaitoun**")
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Simulation Parameters")
        
        # Batch input
        st.markdown("#### 📝 Batch Sample Input")
        batch_input = st.text_area(
            "Paste values (comma, space, or newline separated):",
            placeholder="95, 102, 88, 110, 97, 105, 92, 108, 99, 101",
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
        
        st.markdown("---")
        
        # Individual samples
        st.markdown("#### 🔢 Individual Samples")
        
        if 'samples' not in st.session_state:
            st.session_state.samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]
        
        n_samples = st.number_input("Number of samples", min_value=3, max_value=50,
                                     value=len(st.session_state.samples), step=1)
        
        if n_samples != len(st.session_state.samples):
            current = st.session_state.samples
            if n_samples > len(current):
                current.extend([100] * (n_samples - len(current)))
            else:
                current = current[:n_samples]
            st.session_state.samples = current
        
        # Display individual fields in columns
        sample_values = []
        cols = st.columns(3)
        for i in range(n_samples):
            col_idx = i % 3
            with cols[col_idx]:
                val = st.number_input(f"#{i+1}", value=float(st.session_state.samples[i]),
                                      step=1.0, key=f"s_{i}", label_visibility="collapsed")
                sample_values.append(val)
        
        st.session_state.samples = sample_values
        
        st.markdown("---")
        
        # Simulation settings
        st.markdown("#### 🎯 Settings")
        uncertainty_percent = st.slider("Uncertainty (%)", 1, 20, 5)
        regulatory_limit = st.number_input("Regulatory Limit (ppm)", value=100.0, step=5.0)
        iterations = st.selectbox("Iterations/sample", [1000, 5000, 10000, 50000], index=2)
        
        run_button = st.button("🚀 Run Simulation", use_container_width=True, type="primary")
    
    # Main content
    if run_button:
        samples = st.session_state.samples
        
        if len(samples) < 3:
            st.warning("⚠️ Please enter at least 3 samples.")
        else:
            with st.spinner("Running Monte Carlo simulation..."):
                results = run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations)
                st.session_state.results = results
                
                # Metrics row
                st.markdown("### 📊 Results Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: bold;">{results['mean']:.1f}</div>
                        <div>Mean (ppm)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: bold;">{results['median']:.1f}</div>
                        <div>Median (ppm)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div style="font-size: 1.8rem; font-weight: bold;">±{results['std']:.1f}</div>
                        <div>Std Dev</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col4:
                    color = "#dc3545" if results['p_exceed'] > 0.5 else "#28a745"
                    st.markdown(f"""
                    <div class="metric-card" style="background: linear-gradient(135deg, {color} 0%, #555 100%);">
                        <div style="font-size: 1.8rem; font-weight: bold;">{results['p_exceed']*100:.1f}%</div>
                        <div>P(Exceed)</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Confidence intervals
                st.markdown("---")
                st.markdown("### 📈 Confidence Intervals")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**90% Confidence Interval:** [{results['percentile_5']:.2f}, {results['percentile_95']:.2f}] ppm")
                with col2:
                    st.success(f"**95% Confidence Interval:** [{results['percentile_2.5']:.2f}, {results['percentile_97.5']:.2f}] ppm")
                
                # Regulatory decision
                st.markdown("---")
                st.markdown("### ⚖️ Regulatory Decision")
                
                if results['p_exceed'] < 0.05:
                    st.markdown("""
                    <div class="success-box">
                        <h3>✅ SAFE ZONE - Declare Compliant</h3>
                        <p>Probability of exceeding limit is less than 5%.</p>
                    </div>
                    """, unsafe_allow_html=True)
                elif results['p_exceed'] > 0.95:
                    st.markdown("""
                    <div class="danger-box">
                        <h3>❌ VIOLATION ZONE - Declare Non-Compliant</h3>
                        <p>Probability of exceeding limit is greater than 95%.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="warning-box">
                        <h3>⚠️ UNCERTAIN ZONE - Need More Data</h3>
                        <p>Probability of exceeding limit is between 5% and 95%.</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Statistics table
                st.markdown("---")
                st.markdown("### 📋 Detailed Statistics")
                display_statistics_table(results)
                
                # Sample table
                st.markdown("---")
                st.markdown("### 📋 Sample Values")
                display_sample_table(results, uncertainty_percent)
                
                # Text histogram
                st.markdown("---")
                display_text_histogram(results)
                
                # CDF table
                st.markdown("---")
                display_text_cdf(results)
                
                # Download
                st.markdown("---")
                st.markdown("### 📥 Download Results")
                
                download_df = pd.DataFrame({
                    'simulated_values': results['all_simulations']
                })
                
                csv = download_df.to_csv(index=False)
                st.download_button(
                    label="📥 Download CSV",
                    data=csv,
                    file_name=f"monte_carlo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
    
    else:
        st.info("👈 **Welcome!** Configure parameters and click 'Run Simulation'.")
        
        with st.expander("ℹ️ How to Use"):
            st.markdown("""
            1. **Paste samples** in batch input or enter individually
            2. Click **"Parse & Load"** to auto-fill fields
            3. Set **uncertainty percentage** (CEMS: ±5%)
            4. Set **regulatory limit**
            5. Click **"Run Simulation"**
            
            **Sample formats:** `95, 102, 88` or `95 102 88` or each on new line
            """)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>© 2024 | Ismail Kamal, Amir Salem, Samar Zaitoun</p>
        <p>Supervisor: Dr. Mohamed Youssef | Alexandria University</p>
        <p style="font-size: 0.8rem;">References: ISO 14064-1:2018 | Cullen & Frey (1999)</p>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# RUN
# ================================================================

if __name__ == "__main__":
    main()
