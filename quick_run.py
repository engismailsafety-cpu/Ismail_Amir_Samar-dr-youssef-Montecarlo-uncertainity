"""
MONTE CARLO SIMULATION
Team: Ismail Kamal, Amir Salem, Samar Zaitoun
Supervisor: Dr. Mohamed Youssef - Alexandria University
"""

import streamlit as st
import numpy as np
import pandas as pd
from datetime import datetime

# ================================================================
# PAGE SETUP
# ================================================================

st.set_page_config(
    page_title="Monte Carlo Simulation",
    page_icon="🎲",
    layout="wide"
)

# ================================================================
# LOGIN SYSTEM
# ================================================================

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("""
    <div style="max-width: 400px; margin: 100px auto; padding: 30px; 
                background: white; border-radius: 15px; box-shadow: 0 5px 20px rgba(0,0,0,0.1);
                text-align: center;">
        <h2 style="color: #1e3c72;">🎲 Monte Carlo Simulation</h2>
        <p>Environmental Emission Predictor</p>
        <hr>
        <h4>Login to Continue</h4>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login", use_container_width=True):
            if username == "admin" and password == "1234":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid credentials. Use: admin / 1234")
    st.stop()

# ================================================================
# HEADER
# ================================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
            padding: 30px; border-radius: 15px; margin-bottom: 20px; text-align: center;">
    <h1 style="color: white; margin: 0;">🎲 Monte Carlo Simulation</h1>
    <p style="color: white; margin: 10px 0 0 0;">Environmental Emission Predictor for Petrochemical Facilities</p>
</div>
""", unsafe_allow_html=True)

# Team Information
st.markdown("### 👥 Research Team")
col1, col2, col3, col4 = st.columns(4)
col1.markdown("**👨‍💻 Ismail Kamal**")
col2.markdown("**👨‍💻 Amir Salem**")
col3.markdown("**👩‍💻 Samar Zaitoun**")
col4.markdown("**👨‍🏫 Dr. Mohamed Youssef**")
st.markdown("---")

# Logout Button
if st.button("🚪 Logout", use_container_width=False):
    st.session_state.logged_in = False
    st.rerun()
st.markdown("---")

# ================================================================
# DEFAULT DATA
# ================================================================

DEFAULT_SAMPLES = [160.0, 195.0, 180.0, 188.0, 175.0, 192.0, 182.0, 186.0, 178.0, 204.0]
DEFAULT_LIMIT = 200.0

# Initialize session state
if 'samples' not in st.session_state:
    st.session_state.samples = DEFAULT_SAMPLES.copy()

# ================================================================
# SIDEBAR - INPUTS
# ================================================================

with st.sidebar:
    st.header("⚙️ Simulation Parameters")
    
    # Input method
    input_method = st.radio("Data Input Method", ["Manual Entry", "Batch Paste", "Excel Upload"], index=0)
    
    if input_method == "Batch Paste":
        st.markdown("### Paste Your Samples")
        text_input = st.text_area(
            "Enter numbers (comma, space, or newline separated):", 
            placeholder="160, 195, 180, 188, 175, 192, 182, 186, 178, 204",
            height=120
        )
        if st.button("📋 Load Batch Data", use_container_width=True):
            try:
                # Replace commas with spaces and split
                text_input = text_input.replace(',', ' ')
                nums = [float(x) for x in text_input.split() if x.strip()]
                if len(nums) >= 3:
                    st.session_state.samples = nums
                    st.success(f"✅ Successfully loaded {len(nums)} samples!")
                    st.rerun()
                else:
                    st.error(f"⚠️ Only {len(nums)} samples found. Need at least 3 samples.")
            except Exception as e:
                st.error(f"Error parsing data: {e}")
    
    elif input_method == "Excel Upload":
        st.markdown("### Upload Excel File")
        uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx', 'xls'])
        if uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                # Get first numeric column
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    samples = df[numeric_cols[0]].dropna().tolist()
                    if len(samples) >= 3:
                        st.session_state.samples = samples
                        st.success(f"✅ Loaded {len(samples)} samples from Excel!")
                        st.rerun()
                    else:
                        st.error(f"⚠️ Only {len(samples)} samples. Need at least 3.")
                else:
                    st.error("No numeric data found in Excel file.")
            except Exception as e:
                st.error(f"Error reading Excel: {e}")
    
    else:  # Manual Entry
        st.markdown("### Manual Data Entry")
        
        # Number of samples
        current_len = len(st.session_state.samples)
        n_samples = st.number_input(
            "Number of samples:", 
            min_value=3, 
            max_value=50, 
            value=current_len,
            step=1
        )
        n_samples = int(n_samples)  # Ensure integer
        
        # Adjust sample list
        current = st.session_state.samples.copy()
        if n_samples > len(current):
            # Add default values
            default_val = current[-1] if current else 160.0
            current.extend([default_val] * (n_samples - len(current)))
        else:
            current = current[:n_samples]
        
        # Display input fields
        st.markdown("**Enter sample values:**")
        new_samples = []
        cols = st.columns(4)
        for i in range(n_samples):
            with cols[i % 4]:
                val = st.number_input(
                    f"Sample {i+1}", 
                    value=float(current[i]), 
                    step=1.0,
                    key=f"sample_{i}",
                    format="%.2f"
                )
                new_samples.append(float(val))
        
        st.session_state.samples = new_samples
    
    st.markdown("---")
    
    # Reset button
    if st.button("🔄 Reset to Default Samples", use_container_width=True):
        st.session_state.samples = DEFAULT_SAMPLES.copy()
        st.success(f"✅ Reset to {len(DEFAULT_SAMPLES)} default samples!")
        st.rerun()
    
    st.markdown("---")
    
    # Simulation parameters
    st.markdown("### 🎯 Simulation Settings")
    
    # All values as floats to avoid type errors
    uncertainty = float(st.slider("Measurement Uncertainty (%)", 1.0, 20.0, 5.0, 1.0))
    
    limit = float(st.number_input(
        "Regulatory Limit (ppm)", 
        value=float(DEFAULT_LIMIT), 
        step=5.0,
        format="%.2f"
    ))
    
    iterations = int(st.select_slider(
        "Iterations per sample", 
        options=[1000, 5000, 10000, 50000],
        value=10000
    ))
    
    st.markdown("---")
    
    # Current samples summary
    st.markdown("### 📊 Current Data Summary")
    st.write(f"**Sample Count:** {len(st.session_state.samples)}")
    st.write(f"**Sample Mean:** {np.mean(st.session_state.samples):.2f} ppm")
    st.write(f"**Sample Range:** [{min(st.session_state.samples):.2f}, {max(st.session_state.samples):.2f}] ppm")
    
    # Run button
    st.markdown("---")
    run_button = st.button("🚀 RUN MONTE CARLO SIMULATION", type="primary", use_container_width=True)

# ================================================================
# MAIN CONTENT - RUN SIMULATION
# ================================================================

if run_button:
    samples = st.session_state.samples
    
    if len(samples) < 3:
        st.warning("⚠️ Please enter at least 3 samples before running simulation.")
    else:
        with st.spinner("🔄 Running Monte Carlo simulation... This may take a few seconds."):
            
            # Monte Carlo Simulation
            np.random.seed(42)  # For reproducibility
            all_values = []
            
            for val in samples:
                sigma = val * (uncertainty / 100.0)
                simulated = np.random.normal(loc=val, scale=sigma, size=iterations)
                all_values.extend(simulated)
            
            all_values = np.array(all_values)
            
            # Calculate results
            mean_val = float(np.mean(all_values))
            median_val = float(np.median(all_values))
            std_val = float(np.std(all_values))
            min_val = float(np.min(all_values))
            max_val = float(np.max(all_values))
            p_exceed = float(np.mean(all_values > limit))
            p_comply = 1.0 - p_exceed
            
            # Confidence intervals
            ci_90_lower = float(np.percentile(all_values, 5))
            ci_90_upper = float(np.percentile(all_values, 95))
            ci_95_lower = float(np.percentile(all_values, 2.5))
            ci_95_upper = float(np.percentile(all_values, 97.5))
            
            # Sample statistics
            sample_mean = float(np.mean(samples))
            sample_std = float(np.std(samples))
            sample_min = float(min(samples))
            sample_max = float(max(samples))
            
            # ============================================================
            # DISPLAY RESULTS
            # ============================================================
            
            st.markdown("## 📊 Simulation Results Summary")
            
            # Metrics row
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Mean Emission", f"{mean_val:.1f} ppm")
            with col2:
                st.metric("Median Emission", f"{median_val:.1f} ppm")
            with col3:
                st.metric("Standard Deviation", f"±{std_val:.1f} ppm")
            with col4:
                color = "red" if p_exceed > 0.5 else "green"
                st.metric("Probability > Limit", f"{p_exceed*100:.1f}%", delta_color="off")
            
            st.markdown("---")
            
            # Confidence intervals
            st.markdown("## 📈 Confidence Intervals")
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"""
                ### 90% Confidence Interval
                **{ci_90_lower:.2f}** to **{ci_90_upper:.2f}** ppm
                
                We are 90% confident that the true emission value lies within this range.
                """)
            with col2:
                st.success(f"""
                ### 95% Confidence Interval
                **{ci_95_lower:.2f}** to **{ci_95_upper:.2f}** ppm
                
                We are 95% confident that the true emission value lies within this range.
                """)
            
            st.markdown("---")
            
            # Regulatory decision
            st.markdown("## ⚖️ Regulatory Decision")
            
            if p_exceed < 0.05:
                st.markdown("""
                <div style="background: #d4edda; border-left: 4px solid #28a745; padding: 20px; border-radius: 10px;">
                    <h3 style="color: #155724; margin: 0;">✅ SAFE ZONE - Declare Compliant</h3>
                    <p style="color: #155724; margin: 10px 0 0 0;">The probability of exceeding the regulatory limit is less than 5%.</p>
                    <p style="color: #155724; margin: 5px 0 0 0;"><strong>Recommended Action:</strong> Continue routine monitoring.</p>
                </div>
                """, unsafe_allow_html=True)
            elif p_exceed > 0.95:
                st.markdown("""
                <div style="background: #f8d7da; border-left: 4px solid #dc3545; padding: 20px; border-radius: 10px;">
                    <h3 style="color: #721c24; margin: 0;">❌ VIOLATION ZONE - Declare Non-Compliant</h3>
                    <p style="color: #721c24; margin: 10px 0 0 0;">The probability of exceeding the regulatory limit is greater than 95%.</p>
                    <p style="color: #721c24; margin: 5px 0 0 0;"><strong>Recommended Action:</strong> Immediate enforcement action required.</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: #fff3cd; border-left: 4px solid #ffc107; padding: 20px; border-radius: 10px;">
                    <h3 style="color: #856404; margin: 0;">⚠️ UNCERTAIN ZONE - Need More Data</h3>
                    <p style="color: #856404; margin: 10px 0 0 0;">The probability of exceeding the regulatory limit is between 5% and 95%.</p>
                    <p style="color: #856404; margin: 5px 0 0 0;"><strong>Recommended Action:</strong> Collect additional samples or install continuous monitoring.</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Detailed statistics table
            st.markdown("## 📋 Detailed Statistics")
            
            stats_data = {
                "Metric": [
                    "📊 Sample Mean",
                    "📐 Sample Standard Deviation",
                    "📏 Sample Range",
                    "🔢 Number of Samples",
                    "🎯 Simulation Mean",
                    "📊 Simulation Median",
                    "📐 Simulation Standard Deviation",
                    "🔄 Total Iterations",
                    "📈 90% Confidence Interval",
                    "📊 95% Confidence Interval",
                    "⚠️ Probability of Exceedance",
                    "✅ Probability of Compliance",
                    "⚖️ Regulatory Limit"
                ],
                "Value": [
                    f"{sample_mean:.2f} ppm",
                    f"{sample_std:.2f} ppm",
                    f"[{sample_min:.2f}, {sample_max:.2f}] ppm",
                    str(len(samples)),
                    f"{mean_val:.2f} ppm",
                    f"{median_val:.2f} ppm",
                    f"{std_val:.2f} ppm",
                    f"{len(all_values):,}",
                    f"[{ci_90_lower:.2f}, {ci_90_upper:.2f}] ppm",
                    f"[{ci_95_lower:.2f}, {ci_95_upper:.2f}] ppm",
                    f"{p_exceed*100:.1f}%",
                    f"{p_comply*100:.1f}%",
                    f"{limit:.2f} ppm"
                ]
            }
            
            stats_df = pd.DataFrame(stats_data)
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Sample values table
            st.markdown("## 📋 Input Sample Values")
            
            sample_data = []
            for i, val in enumerate(samples):
                uncertainty_val = val * (uncertainty / 100.0)
                sample_data.append({
                    "Sample #": i + 1,
                    "Measured Value (ppm)": f"{val:.2f}",
                    "Uncertainty (± ppm)": f"{uncertainty_val:.2f}",
                    "95% CI Lower": f"{val - 1.96 * uncertainty_val:.2f}",
                    "95% CI Upper": f"{val + 1.96 * uncertainty_val:.2f}"
                })
            
            sample_df = pd.DataFrame(sample_data)
            st.dataframe(sample_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Text histogram
            st.markdown("## 📊 Distribution Visualization")
            
            hist, bin_edges = np.histogram(all_values, bins=25)
            max_hist = max(hist) if len(hist) > 0 else 1
            
            hist_lines = []
            for i in range(len(hist)):
                bar_length = int(hist[i] / max_hist * 50)
                bar = "█" * bar_length
                
                left = bin_edges[i]
                right = bin_edges[i+1]
                
                if left >= limit:
                    color = "🔴"
                elif right <= limit:
                    color = "🟢"
                else:
                    color = "🟡"
                
                hist_lines.append(f"{color} {left:7.1f} - {right:7.1f} | {bar}")
            
            st.code("\n".join(hist_lines))
            st.caption("🟢 = Below regulatory limit | 🟡 = Crosses limit | 🔴 = Above limit")
            st.caption(f"🎯 Regulatory Limit = {limit:.1f} ppm")
            
            st.markdown("---")
            
            # Download results
            st.markdown("## 📥 Download Results")
            
            download_df = pd.DataFrame({
                "simulated_value_ppm": all_values
            })
            
            csv_data = download_df.to_csv(index=False)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            st.download_button(
                label="📥 Download Simulated Values (CSV)",
                data=csv_data,
                file_name=f"monte_carlo_results_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            # Summary message
            st.markdown("---")
            st.success(f"✅ Simulation completed successfully! Total iterations: {len(all_values):,}")

else:
    # Display instructions when not running
    st.info("👈 **Welcome!** Please configure your simulation parameters in the sidebar and click 'RUN MONTE CARLO SIMULATION' to begin.")
    
    with st.expander("📋 Default Data Preview", expanded=True):
        st.write(f"**Default Samples ({len(DEFAULT_SAMPLES)} samples):**")
        st.write(DEFAULT_SAMPLES)
        st.write(f"**Sample Mean:** {np.mean(DEFAULT_SAMPLES):.2f} ppm")
        st.write(f"**Sample Standard Deviation:** {np.std(DEFAULT_SAMPLES):.2f} ppm")
        st.write(f"**Regulatory Limit:** {DEFAULT_LIMIT} ppm")
    
    with st.expander("ℹ️ How to Use This Application"):
        st.markdown("""
        ### Step-by-Step Guide:
        
        1. **Enter Your Data** (choose one of three methods):
           - **Manual Entry**: Set number of samples and enter each value individually
           - **Batch Paste**: Copy-paste all values at once (comma, space, or newline separated)
           - **Excel Upload**: Upload an Excel file with your sample values
        
        2. **Configure Simulation Settings**:
           - **Measurement Uncertainty**: Typical CEMS accuracy is ±5%
           - **Regulatory Limit**: The compliance threshold (default: 200 ppm)
           - **Iterations per sample**: More iterations = more accurate results
        
        3. **Run Simulation**: Click the "RUN MONTE CARLO SIMULATION" button
        
        4. **Review Results**:
           - Summary metrics (mean, median, probability)
           - Confidence intervals (90% and 95%)
           - Regulatory decision (Safe / Uncertain / Violation)
           - Detailed statistics table
           - Distribution visualization
        
        5. **Download Results**: Export simulated values as CSV
        
        ### Sample Data Formats:
        - Comma separated: `160, 195, 180, 188, 175`
        - Space separated: `160 195 180 188 175`
        - Newline separated: each value on a new line
        """)

# ================================================================
# FOOTER
# ================================================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 20px;">
    <p>© 2024 Monte Carlo Simulation Tool</p>
    <p>Developed by: <strong>Ismail Kamal, Amir Salem, Samar Zaitoun</strong></p>
    <p>Under Supervision of: <strong>Dr. Mohamed Youssef</strong> | Master Program - Alexandria University</p>
    <p style="font-size: 12px;">References: ISO 14064-1:2018 | Cullen, A.C., & Frey, H.C. (1999)</p>
</div>
""", unsafe_allow_html=True)
