"""
MONTE CARLO SIMULATION FOR EMISSION PREDICTION
NO EXTERNAL LIBRARIES NEEDED - Works on Streamlit Cloud

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
import io
import base64

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
    /* Main header */
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
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        padding: 1rem;
        color: white;
        text-align: center;
        margin: 0.5rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.8rem;
        opacity: 0.9;
    }
    
    /* Result boxes */
    .success-box {
        background: #d4edda;
        border-left: 4px solid #28a745;
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
    .info-box {
        background: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    /* Team cards */
    .team-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 0.8rem;
        text-align: center;
        margin: 0.3rem;
    }
    
    /* Login container */
    .login-container {
        max-width: 450px;
        margin: 80px auto;
        padding: 2rem;
        background: white;
        border-radius: 20px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.2);
        text-align: center;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        margin-top: 2rem;
        border-top: 1px solid #e0e0e0;
        color: #666;
    }
    
    /* Chart container */
    .chart-container {
        background: white;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border: 1px solid #e0e0e0;
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
        <div style="font-size: 4rem;">🎲🏭📊</div>
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
# DEFAULT DATA
# ================================================================

DEFAULT_SAMPLES = [160, 195, 180, 188, 175, 192, 182, 186, 178, 204]
DEFAULT_LIMIT = 200

# ================================================================
# HELPER FUNCTIONS
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
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            samples = df[numeric_cols[0]].dropna().tolist()
            return samples
        return []
    except Exception as e:
        st.error(f"Error reading Excel: {e}")
        return []

# ================================================================
# MONTE CARLO SIMULATION (NO MATPLOTLIB)
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
    
    # Calculate histogram for display (using numpy only)
    hist, bin_edges = np.histogram(all_simulations, bins=30)
    
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
        'histogram': {
            'counts': hist.tolist(),
            'bin_edges': bin_edges.tolist()
        }
    }
    
    return results

# ================================================================
# HTML CHART FUNCTIONS (NO MATPLOTLIB)
# ================================================================

def create_html_histogram(results):
    """Create histogram using HTML/CSS (no matplotlib)"""
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    mean_val = results['mean']
    
    # Create bins
    min_val = results['min']
    max_val = results['max']
    bins = np.linspace(min_val, max_val, 25)
    hist, bin_edges = np.histogram(all_simulations, bins=bins)
    
    # Normalize for display (max height 200px)
    max_count = max(hist) if len(hist) > 0 else 1
    max_height = 200
    
    # Build bars HTML
    bars_html = ""
    for i in range(len(hist)):
        height = int((hist[i] / max_count) * max_height) if max_count > 0 else 0
        bar_color = "#28a745"  # green
        if bin_edges[i] >= regulatory_limit:
            bar_color = "#dc3545"  # red
        elif bin_edges[i+1] <= regulatory_limit:
            bar_color = "#28a745"  # green
        else:
            bar_color = "#ffc107"  # yellow
        
        bars_html += f"""
        <div style="display: inline-block; width: 35px; margin: 0 1px; text-align: center;">
            <div style="height: {height}px; width: 100%; background-color: {bar_color}; 
                        border-radius: 3px 3px 0 0;"></div>
            <div style="font-size: 8px; transform: rotate(-45deg); margin-top: 5px; 
                        white-space: nowrap;">{bin_edges[i]:.0f}</div>
        </div>
        """
    
    html = f"""
    <div class="chart-container">
        <h4 style="text-align: center;">Distribution of Simulated Values</h4>
        <div style="text-align: center; margin: 20px 0;">
            {bars_html}
        </div>
        <div style="text-align: center; margin-top: 20px;">
            <span style="color: #28a745;">■</span> Below Limit &nbsp;&nbsp;
            <span style="color: #ffc107;">■</span> Crosses Limit &nbsp;&nbsp;
            <span style="color: #dc3545;">■</span> Above Limit
        </div>
        <div style="text-align: center; margin-top: 10px;">
            <strong>Red Line = Regulatory Limit ({regulatory_limit} ppm)</strong>
        </div>
        <div style="text-align: center; margin-top: 5px;">
            <strong>Mean = {mean_val:.1f} ppm</strong>
        </div>
    </div>
    """
    return html

def create_html_cdf(results):
    """Create CDF plot using HTML/CSS"""
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    
    # Calculate CDF points
    sorted_data = np.sort(all_simulations)
    cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    
    # Sample points for display (every 50th point)
    step = max(1, len(sorted_data) // 100)
    x_points = sorted_data[::step].tolist()
    y_points = cdf[::step].tolist()
    
    # Find point at regulatory limit
    idx = np.searchsorted(sorted_data, regulatory_limit)
    cdf_at_limit = cdf[idx] if idx < len(cdf) else 1.0
    
    # Create SVG line chart
    width = 600
    height = 400
    padding_left = 50
    padding_right = 30
    padding_top = 30
    padding_bottom = 50
    
    plot_width = width - padding_left - padding_right
    plot_height = height - padding_top - padding_bottom
    
    x_min = min(x_points)
    x_max = max(x_points)
    y_min = 0
    y_max = 1
    
    # Create path
    points = []
    for x, y in zip(x_points, y_points):
        px = padding_left + ((x - x_min) / (x_max - x_min)) * plot_width
        py = padding_top + plot_height - (y / y_max) * plot_height
        points.append(f"{px},{py}")
    
    path = " ".join(points)
    
    # Limit line
    limit_px = padding_left + ((regulatory_limit - x_min) / (x_max - x_min)) * plot_width
    
    html = f"""
    <div class="chart-container">
        <h4 style="text-align: center;">Cumulative Distribution Function (CDF)</h4>
        <svg width="{width}" height="{height}" style="background: white;">
            <!-- Axes -->
            <line x1="{padding_left}" y1="{padding_top}" x2="{padding_left}" y2="{height - padding_bottom}" 
                  stroke="black" stroke-width="2"/>
            <line x1="{padding_left}" y1="{height - padding_bottom}" x2="{width - padding_right}" 
                  y2="{height - padding_bottom}" stroke="black" stroke-width="2"/>
            
            <!-- X-axis labels -->
            <text x="{width/2}" y="{height - 10}" text-anchor="middle" font-size="12">Emission Value (ppm)</text>
            <text x="{padding_left - 10}" y="{height/2}" text-anchor="middle" font-size="12" transform="rotate(-90, {padding_left - 10}, {height/2})">Cumulative Probability</text>
            
            <!-- CDF Line -->
            <polyline points="{path}" fill="none" stroke="#1e3c72" stroke-width="2.5"/>
            
            <!-- Limit Line -->
            <line x1="{limit_px}" y1="{padding_top}" x2="{limit_px}" y2="{height - padding_bottom}" 
                  stroke="#dc3545" stroke-width="2" stroke-dasharray="5,5"/>
            
            <!-- CDF at Limit Line -->
            <line x1="{padding_left}" y1="{padding_top + plot_height - cdf_at_limit * plot_height}" 
                  x2="{limit_px}" y2="{padding_top + plot_height - cdf_at_limit * plot_height}" 
                  stroke="#28a745" stroke-width="1.5" stroke-dasharray="3,3"/>
            
            <!-- Labels -->
            <text x="{limit_px + 5}" y="{padding_top + 20}" fill="#dc3545" font-size="10">Limit = {regulatory_limit}</text>
            <text x="{padding_left + 5}" y="{padding_top + plot_height - cdf_at_limit * plot_height - 5}" fill="#28a745" font-size="10">P(Comply) = {cdf_at_limit*100:.1f}%</text>
            
            <!-- Title -->
            <text x="{width/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">Cumulative Distribution Function</text>
        </svg>
        <div style="text-align: center; margin-top: 10px;">
            <strong>Probability of Exceedance: {results['p_exceed']*100:.1f}%</strong>
        </div>
    </div>
    """
    return html

def create_html_boxplot(results):
    """Create boxplot using HTML/CSS"""
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    mean_val = results['mean']
    median_val = results['median']
    q1 = np.percentile(all_simulations, 25)
    q3 = np.percentile(all_simulations, 75)
    iqr = q3 - q1
    lower_whisker = max(results['min'], q1 - 1.5 * iqr)
    upper_whisker = min(results['max'], q3 + 1.5 * iqr)
    
    width = 500
    height = 300
    center_x = 250
    box_width = 80
    
    # Scale for values
    min_val = results['min']
    max_val = results['max']
    range_val = max_val - min_val
    
    def scale_y(value):
        return height - 50 - ((value - min_val) / range_val) * (height - 100)
    
    html = f"""
    <div class="chart-container">
        <h4 style="text-align: center;">Boxplot of Simulated Values</h4>
        <svg width="{width}" height="{height}" style="background: white;">
            <!-- Whiskers -->
            <line x1="{center_x}" y1="{scale_y(lower_whisker)}" x2="{center_x}" y2="{scale_y(upper_whisker)}" stroke="#333" stroke-width="2"/>
            
            <!-- Box -->
            <rect x="{center_x - box_width/2}" y="{scale_y(q3)}" width="{box_width}" height="{scale_y(q1) - scale_y(q3)}" 
                  fill="#667eea" stroke="#333" stroke-width="1.5" opacity="0.7"/>
            
            <!-- Median line -->
            <line x1="{center_x - box_width/2}" y1="{scale_y(median_val)}" x2="{center_x + box_width/2}" 
                  y2="{scale_y(median_val)}" stroke="#dc3545" stroke-width="2"/>
            
            <!-- Mean point -->
            <circle cx="{center_x}" cy="{scale_y(mean_val)}" r="5" fill="#28a745"/>
            
            <!-- Whisker caps -->
            <line x1="{center_x - 15}" y1="{scale_y(lower_whisker)}" x2="{center_x + 15}" y2="{scale_y(lower_whisker)}" stroke="#333" stroke-width="2"/>
            <line x1="{center_x - 15}" y1="{scale_y(upper_whisker)}" x2="{center_x + 15}" y2="{scale_y(upper_whisker)}" stroke="#333" stroke-width="2"/>
            
            <!-- Limit line -->
            <line x1="{center_x - 40}" y1="{scale_y(regulatory_limit)}" x2="{center_x + 40}" 
                  y2="{scale_y(regulatory_limit)}" stroke="#dc3545" stroke-width="2" stroke-dasharray="5,5"/>
            
            <!-- Labels -->
            <text x="{center_x}" y="{height - 15}" text-anchor="middle" font-size="12">Simulated Values</text>
            <text x="{center_x + 50}" y="{scale_y(regulatory_limit)}" fill="#dc3545" font-size="10">Limit</text>
            <text x="{center_x + 50}" y="{scale_y(mean_val)}" fill="#28a745" font-size="10">Mean</text>
            
            <text x="{width/2}" y="20" text-anchor="middle" font-size="14" font-weight="bold">Boxplot Distribution</text>
        </svg>
        <div style="text-align: center; margin-top: 10px;">
            <span style="color: #667eea;">■</span> Box (Q1-Q3) &nbsp;
            <span style="color: #dc3545;">━</span> Median &nbsp;
            <span style="color: #28a745;">●</span> Mean
        </div>
    </div>
    """
    return html

def create_text_histogram(results, width=50):
    """Create text-based histogram"""
    
    all_simulations = np.array(results['all_simulations'])
    regulatory_limit = results['regulatory_limit']
    
    min_val = float(np.min(all_simulations))
    max_val = float(np.max(all_simulations))
    
    bins = np.linspace(min_val, max_val, 15)
    hist, bin_edges = np.histogram(all_simulations, bins=bins)
    max_freq = float(np.max(hist)) if len(hist) > 0 else 1
    scale = width / max_freq if max_freq > 0 else 1
    
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
    
    return '\n'.join(histogram_lines)

# ================================================================
# DISPLAY FUNCTIONS
# ================================================================

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
        <p style="font-size: 0.9rem;">Advanced Uncertainty Analysis Tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Team information
    st.markdown("### 👥 Research Team")
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
    with col1:
        st.markdown("""<div class="team-card"><strong>👨‍💻 Ismail Kamal</strong></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""<div class="team-card"><strong>👨‍💻 Amir Salem</strong></div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""<div class="team-card"><strong>👩‍💻 Samar Zaitoun</strong></div>""", unsafe_allow_html=True)
    with col4:
        st.markdown("""<div class="team-card"><strong>👨‍🏫 Dr. Mohamed Youssef</strong><br><small>Supervisor</small></div>""", unsafe_allow_html=True)
    with col5:
        if st.button("🚪 Logout", use_container_width=True):
            logout()
    
    st.markdown("---")
    
    # Initialize samples
    if 'samples' not in st.session_state:
        st.session_state.samples = DEFAULT_SAMPLES.copy()
    
    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Simulation Parameters")
        
        # Data input
        st.markdown("### 📂 Data Input")
        input_method = st.radio("Choose input method:", ["📝 Manual Entry", "📋 Batch Paste", "📎 Excel Upload"], horizontal=True)
        
        if input_method == "📋 Batch Paste":
            batch_input = st.text_area("Paste values:", placeholder="160, 195, 180, 188, 175", height=100)
            if st.button("📋 Parse & Load", use_container_width=True):
                parsed = parse_samples(batch_input)
                if len(parsed) >= 3:
                    st.session_state.samples = parsed
                    st.success(f"✅ Loaded {len(parsed)} samples!")
                    st.rerun()
                else:
                    st.error(f"⚠️ Only {len(parsed)} samples. Need at least 3.")
        
        elif input_method == "📎 Excel Upload":
            uploaded_file = st.file_uploader("Choose Excel file", type=['xlsx', 'xls'])
            if uploaded_file is not None:
                samples = load_from_excel(uploaded_file)
                if len(samples) >= 3:
                    st.session_state.samples = samples
                    st.success(f"✅ Loaded {len(samples)} samples!")
                    st.rerun()
                else:
                    st.error(f"⚠️ Only {len(samples)} samples. Need at least 3.")
        
        else:  # Manual Entry
            n_samples = st.number_input("Number of samples:", min_value=3, max_value=50, 
                                         value=len(st.session_state.samples), step=1)
            
            current = st.session_state.samples.copy()
            if n_samples > len(current):
                current.extend([current[-1] if current else 160] * (n_samples - len(current)))
            else:
                current = current[:n_samples]
            
            sample_values = []
            cols = st.columns(4)
            for i in range(n_samples):
                with cols[i % 4]:
                    val = st.number_input(f"#{i+1}", value=float(current[i]), step=1.0, key=f"s_{i}", label_visibility="collapsed")
                    sample_values.append(val)
            st.session_state.samples = sample_values
        
        st.markdown("---")
        
        # Reset button
        if st.button("🔄 Reset to Default", use_container_width=True):
            st.session_state.samples = DEFAULT_SAMPLES.copy()
            st.success(f"✅ Reset to {len(DEFAULT_SAMPLES)} default samples!")
            st.rerun()
        
        st.markdown("---")
        
        # Simulation settings
        st.markdown("### 🎯 Settings")
        uncertainty_percent = st.slider("Uncertainty (%)", 1, 20, 5)
        regulatory_limit = st.number_input("Regulatory Limit (ppm)", value=DEFAULT_LIMIT, step=5.0)
        iterations_per_sample = st.selectbox("Iterations/sample", [1000, 5000, 10000, 50000], index=2)
        
        st.markdown("---")
        
        # Current samples info
        st.markdown("### 📊 Current Samples")
        st.write(f"**Count:** {len(st.session_state.samples)}")
        st.write(f"**Mean:** {np.mean(st.session_state.samples):.2f}")
        st.write(f"**Range:** [{min(st.session_state.samples):.2f}, {max(st.session_state.samples):.2f}]")
        
        run_button = st.button("🚀 Run Simulation", use_container_width=True, type="primary")
    
    # Main content
    if run_button:
        samples = st.session_state.samples
        
        if len(samples) < 3:
            st.warning("⚠️ Please enter at least 3 samples.")
        else:
            with st.spinner("Running Monte Carlo simulation..."):
                
                results = run_monte_carlo(samples, uncertainty_percent, regulatory_limit, iterations_per_sample)
                st.session_state.results = results
                
                # Metrics
                st.markdown("## 📊 Results Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.markdown(f"""<div class="metric-card"><div class="metric-value">{results['mean']:.1f}</div><div class="metric-label">Mean (ppm)</div></div>""", unsafe_allow_html=True)
                with col2:
                    st.markdown(f"""<div class="metric-card"><div class="metric-value">{results['median']:.1f}</div><div class="metric-label">Median (ppm)</div></div>""", unsafe_allow_html=True)
                with col3:
                    st.markdown(f"""<div class="metric-card"><div class="metric-value">±{results['std']:.1f}</div><div class="metric-label">Std Dev</div></div>""", unsafe_allow_html=True)
                with col4:
                    color = "#dc3545" if results['p_exceed'] > 0.5 else "#28a745"
                    st.markdown(f"""<div class="metric-card" style="background: linear-gradient(135deg, {color} 0%, #555 100%);"><div class="metric-value">{results['p_exceed']*100:.1f}%</div><div class="metric-label">P(>Limit)</div></div>""", unsafe_allow_html=True)
                
                # Confidence intervals
                st.markdown("---")
                st.markdown("## 📈 Confidence Intervals")
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"**90% CI:** [{results['percentile_5']:.2f}, {results['percentile_95']:.2f}] ppm")
                with col2:
                    st.success(f"**95% CI:** [{results['percentile_2.5']:.2f}, {results['percentile_97.5']:.2f}] ppm")
                
                # Regulatory decision
                st.markdown("---")
                if results['p_exceed'] < 0.05:
                    st.markdown("""<div class="success-box"><h3>✅ SAFE ZONE - Compliant</h3><p>Probability of exceeding limit is less than 5%.</p></div>""", unsafe_allow_html=True)
                elif results['p_exceed'] > 0.95:
                    st.markdown("""<div class="danger-box"><h3>❌ VIOLATION ZONE - Non-Compliant</h3><p>Probability of exceeding limit is greater than 95%.</p></div>""", unsafe_allow_html=True)
                else:
                    st.markdown("""<div class="warning-box"><h3>⚠️ UNCERTAIN ZONE - Need More Data</h3><p>Probability of exceeding limit is between 5% and 95%.</p></div>""", unsafe_allow_html=True)
                
                # Statistics
                st.markdown("---")
                st.markdown("## 📋 Detailed Statistics")
                display_statistics_table(results)
                
                # Sample table
                st.markdown("---")
                st.markdown("## 📋 Sample Values")
                display_sample_table(results, uncertainty_percent)
                
                # Visualizations (NO MATPLOTLIB)
                st.markdown("---")
                st.markdown("## 📊 Visualizations")
                
                tab1, tab2, tab3, tab4 = st.tabs(["📊 Histogram", "📈 CDF Plot", "📦 Boxplot", "📝 Text View"])
                
                with tab1:
                    html_hist = create_html_histogram(results)
                    st.components.v1.html(html_hist, height=350)
                
                with tab2:
                    html_cdf = create_html_cdf(results)
                    st.components.v1.html(html_cdf, height=450)
                
                with tab3:
                    html_box = create_html_boxplot(results)
                    st.components.v1.html(html_box, height=350)
                
                with tab4:
                    st.code(create_text_histogram(results))
                    st.caption("🟢 = Below limit | 🟡 = Crosses limit | 🔴 = Above limit")
                
                # Download
                st.markdown("---")
                st.markdown("## 📥 Download Results")
                
                download_df = pd.DataFrame({'simulated_values': results['all_simulations']})
                csv = download_df.to_csv(index=False)
                st.download_button("📥 Download CSV", data=csv, file_name=f"monte_carlo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv")
    
    else:
        st.info("👈 **Welcome!** Configure parameters and click 'Run Simulation'.")
        
        with st.expander("📋 Default Samples"):
            st.write(f"**Samples:** {DEFAULT_SAMPLES}")
            st.write(f"**Mean:** {np.mean(DEFAULT_SAMPLES):.2f} ppm")
            st.write(f"**Regulatory Limit:** {DEFAULT_LIMIT} ppm")
        
        with st.expander("ℹ️ Instructions"):
            st.markdown("""
            1. Enter samples (Manual, Batch, or Excel)
            2. Set uncertainty % (typical CEMS: ±5%)
            3. Set regulatory limit (default: 200)
            4. Click **Run Simulation**
            """)
    
    # Footer
    st.markdown("""
    <div class="footer">
        <p>© 2024 | Ismail Kamal, Amir Salem, Samar Zaitoun | Dr. Mohamed Youssef - Alexandria University</p>
        <p>References: ISO 14064-1:2018 | Cullen & Frey (1999)</p>
    </div>
    """, unsafe_allow_html=True)

# ================================================================
# RUN
# ================================================================

if __name__ == "__main__":
    main()
