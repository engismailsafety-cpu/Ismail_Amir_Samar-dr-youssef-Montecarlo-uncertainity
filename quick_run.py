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
        <h4>Login</h4>
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
                st.error("Invalid credentials. Use admin/1234")
    st.stop()

# ================================================================
# HEADER
# ================================================================

st.markdown("""
<div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); 
            padding: 30px; border-radius: 15px; margin-bottom: 20px; text-align: center;">
    <h1 style="color: white;">🎲 Monte Carlo Simulation</h1>
    <p style="color: white;">Environmental Emission Predictor</p>
</div>
""", unsafe_allow_html=True)

# Team
col1, col2, col3, col4 = st.columns(4)
col1.markdown("**👨‍💻 Ismail Kamal**")
col2.markdown("**👨‍💻 Amir Salem**")
col3.markdown("**👩‍💻 Samar Zaitoun**")
col4.markdown("**👨‍🏫 Dr. Mohamed Youssef**")

st.markdown("---")

# Logout button
if st.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.markdown("---")

# ================================================================
# DEFAULT DATA
# ================================================================

DEFAULT_SAMPLES = [160, 195, 180, 188, 175, 192, 182, 186, 178, 204]
DEFAULT_LIMIT = 200

# Initialize session state
if 'samples' not in st.session_state:
    st.session_state.samples = DEFAULT_SAMPLES.copy()

# ================================================================
# SIDEBAR - INPUTS
# ================================================================

with st.sidebar:
    st.header("⚙️ Settings")
    
    # Input method
    input_method = st.radio("Data Input", ["Manual", "Batch Paste", "Excel"])
    
    if input_method == "Batch Paste":
        text_input = st.text_area("Paste numbers (comma or space separated)", 
                                  placeholder="160, 195, 180, 188, 175")
        if st.button("Load"):
            try:
                text_input = text_input.replace(',', ' ')
                nums = [float(x) for x in text_input.split() if x.strip()]
                if len(nums) >= 3:
                    st.session_state.samples = nums
                    st.success(f"Loaded {len(nums)} samples")
                    st.rerun()
                else:
                    st.error("Need at least 3 samples")
            except:
                st.error("Invalid format")
    
    elif input_method == "Excel":
        uploaded = st.file_uploader("Upload Excel", type=['xlsx', 'xls'])
        if uploaded:
            df = pd.read_excel(uploaded)
            nums = df.iloc[:, 0].dropna().tolist()
            if len(nums) >= 3:
                st.session_state.samples = nums
                st.success(f"Loaded {len(nums)} samples")
                st.rerun()
    
    else:  # Manual
        n = st.number_input("Number of samples", min_value=3, max_value=50, 
                            value=len(st.session_state.samples), step=1)
        
        # Adjust sample list
        current = st.session_state.samples.copy()
        if n > len(current):
            current.extend([current[-1]] * (n - len(current)))
        else:
            current = current[:n]
        
        new_samples = []
        cols = st.columns(3)
        for i in range(n):
            with cols[i % 3]:
                val = st.number_input(f"#{i+1}", value=float(current[i]), step=1.0, key=f"s_{i}")
                new_samples.append(val)
        st.session_state.samples = new_samples
    
    st.markdown("---")
    
    # Reset button
    if st.button("Reset to Default"):
        st.session_state.samples = DEFAULT_SAMPLES.copy()
        st.rerun()
    
    st.markdown("---")
    
    # Simulation parameters
    uncertainty = st.slider("Measurement Uncertainty (%)", 1, 20, 5)
    limit = st.number_input("Regulatory Limit (ppm)", value=DEFAULT_LIMIT, step=5.0)
    iterations = st.selectbox("Iterations per sample", [1000, 5000, 10000], index=2)
    
    st.markdown("---")
    st.write(f"**Samples:** {len(st.session_state.samples)}")
    st.write(f"**Mean:** {np.mean(st.session_state.samples):.1f}")
    
    run = st.button("🚀 RUN SIMULATION", type="primary", use_container_width=True)

# ================================================================
# MAIN CONTENT - RUN SIMULATION
# ================================================================

if run:
    samples = st.session_state.samples
    
    if len(samples) < 3:
        st.warning("Please enter at least 3 samples")
    else:
        with st.spinner("Running simulation..."):
            
            # Monte Carlo
            all_values = []
            for val in samples:
                sigma = val * uncertainty / 100
                sim = np.random.normal(loc=val, scale=sigma, size=iterations)
                all_values.extend(sim)
            
            all_values = np.array(all_values)
            
            # Calculate results
            mean_val = np.mean(all_values)
            median_val = np.median(all_values)
            std_val = np.std(all_values)
            p_exceed = np.mean(all_values > limit)
            ci_95_lower = np.percentile(all_values, 2.5)
            ci_95_upper = np.percentile(all_values, 97.5)
            ci_90_lower = np.percentile(all_values, 5)
            ci_90_upper = np.percentile(all_values, 95)
            
            # Display metrics
            st.subheader("📊 Results")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Mean", f"{mean_val:.1f} ppm")
            col2.metric("Median", f"{median_val:.1f} ppm")
            col3.metric("Std Dev", f"±{std_val:.1f}")
            col4.metric("P(>Limit)", f"{p_exceed*100:.1f}%")
            
            st.markdown("---")
            
            # Confidence intervals
            st.subheader("📈 Confidence Intervals")
            col1, col2 = st.columns(2)
            col1.info(f"**90% CI:** [{ci_90_lower:.1f}, {ci_90_upper:.1f}] ppm")
            col2.success(f"**95% CI:** [{ci_95_lower:.1f}, {ci_95_upper:.1f}] ppm")
            
            st.markdown("---")
            
            # Decision
            st.subheader("⚖️ Regulatory Decision")
            if p_exceed < 0.05:
                st.success("✅ **SAFE ZONE** - Facility is COMPLIANT")
            elif p_exceed > 0.95:
                st.error("❌ **VIOLATION ZONE** - Facility is NON-COMPLIANT")
            else:
                st.warning("⚠️ **UNCERTAIN ZONE** - Need more data")
            
            st.markdown("---")
            
            # Statistics table
            st.subheader("📋 Detailed Statistics")
            stats_df = pd.DataFrame([
                ["Sample Mean", f"{np.mean(samples):.2f} ppm"],
                ["Sample Std Dev", f"{np.std(samples):.2f} ppm"],
                ["Sample Min", f"{min(samples):.2f} ppm"],
                ["Sample Max", f"{max(samples):.2f} ppm"],
                ["Simulation Mean", f"{mean_val:.2f} ppm"],
                ["Simulation Median", f"{median_val:.2f} ppm"],
                ["Simulation Std Dev", f"{std_val:.2f} ppm"],
                ["Total Iterations", f"{len(all_values):,}"],
                ["90% CI Lower", f"{ci_90_lower:.2f} ppm"],
                ["90% CI Upper", f"{ci_90_upper:.2f} ppm"],
                ["95% CI Lower", f"{ci_95_lower:.2f} ppm"],
                ["95% CI Upper", f"{ci_95_upper:.2f} ppm"],
                ["P(Exceedance)", f"{p_exceed*100:.1f}%"],
                ["Regulatory Limit", f"{limit} ppm"]
            ], columns=["Metric", "Value"])
            st.dataframe(stats_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Sample table
            st.subheader("📋 Input Samples")
            sample_df = pd.DataFrame({
                "Sample #": range(1, len(samples)+1),
                "Value (ppm)": samples,
                "Uncertainty (±)": [f"{s*uncertainty/100:.2f}" for s in samples]
            })
            st.dataframe(sample_df, hide_index=True, use_container_width=True)
            
            st.markdown("---")
            
            # Simple text histogram
            st.subheader("📊 Distribution")
            
            hist, bins = np.histogram(all_values, bins=20)
            max_hist = max(hist)
            
            hist_lines = []
            for i in range(len(hist)):
                bar_len = int(hist[i] / max_hist * 40)
                bar = "█" * bar_len
                
                if bins[i] >= limit:
                    color = "🔴"
                elif bins[i+1] <= limit:
                    color = "🟢"
                else:
                    color = "🟡"
                
                hist_lines.append(f"{color} {bins[i]:6.1f} - {bins[i+1]:6.1f} | {bar}")
            
            st.code("\n".join(hist_lines))
            st.caption("🟢 Below | 🟡 Crosses | 🔴 Above limit")
            
            st.markdown("---")
            
            # Download
            st.subheader("📥 Download")
            download_df = pd.DataFrame({"simulated_values": all_values})
            csv = download_df.to_csv(index=False)
            st.download_button("Download CSV", csv, f"results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")

else:
    st.info("👈 **Configure settings in sidebar and click RUN**")
    
    with st.expander("📋 Default Data"):
        st.write(f"Samples: {DEFAULT_SAMPLES}")
        st.write(f"Mean: {np.mean(DEFAULT_SAMPLES):.2f}")
        st.write(f"Limit: {DEFAULT_LIMIT}")

# ================================================================
# FOOTER
# ================================================================

st.markdown("---")
st.markdown("<div style='text-align: center; color: gray;'>Ismail Kamal | Amir Salem | Samar Zaitoun | Dr. Mohamed Youssef - Alexandria University</div>", unsafe_allow_html=True)
