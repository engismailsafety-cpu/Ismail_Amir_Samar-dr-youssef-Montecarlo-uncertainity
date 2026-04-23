# streamlit_app.py
import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(page_title="Monte Carlo Simulation", layout="wide")

st.title("🎲 Monte Carlo Simulation for Emission Prediction")
st.markdown("---")

# Sidebar for inputs
st.sidebar.header("📊 Input Parameters")

# Sample input method
input_method = st.sidebar.radio(
    "How would you like to enter samples?",
    ["Manual Entry", "Upload CSV", "Use Example Data"]
)

samples = []

if input_method == "Manual Entry":
    n_samples = st.sidebar.number_input("Number of samples", min_value=5, max_value=100, value=10)
    st.sidebar.write("Enter measured values:")
    for i in range(int(n_samples)):
        val = st.sidebar.number_input(f"Sample {i+1}", value=95.0 + i, step=1.0)
        samples.append(val)

elif input_method == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=['csv'])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if 'measured_value' in df.columns:
            samples = df['measured_value'].tolist()
        else:
            samples = df.iloc[:, 0].tolist()
        st.sidebar.success(f"Loaded {len(samples)} samples")
    else:
        samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]

else:
    # Example data
    samples = [95, 102, 88, 110, 97, 105, 92, 108, 99, 101]
    st.sidebar.info("Using example data (10 samples from a refinery)")

# Parameters
uncertainty_percent = st.sidebar.slider("Measurement Uncertainty (%)", 1, 20, 5)
regulatory_limit = st.sidebar.number_input("Regulatory Limit", value=100.0)
iterations_per_sample = st.sidebar.selectbox("Iterations per sample", [1000, 5000, 10000, 50000], index=2)

# Run button
run_button = st.sidebar.button("🚀 Run Monte Carlo Simulation", type="primary")

# Display samples
st.subheader("📋 Input Samples")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Number of samples:** {len(samples)}")
    st.write(f"**Sample mean:** {np.mean(samples):.2f}")
    st.write(f"**Sample std:** {np.std(samples):.2f}")
    st.write(f"**Range:** [{min(samples):.2f}, {max(samples):.2f}]")
with col2:
    st.write("**Sample values:**")
    st.write(samples[:20] if len(samples) > 20 else samples)
    if len(samples) > 20:
        st.write(f"... and {len(samples) - 20} more")

if run_button:
    with st.spinner("Running Monte Carlo simulation..."):
        
        # Run simulation
        n_samples = len(samples)
        total_iterations = n_samples * iterations_per_sample
        
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
        
        # Display results
        st.markdown("---")
        st.subheader("📊 Simulation Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", f"{mean_val:.2f}")
        with col2:
            st.metric("Median", f"{median_val:.2f}")
        with col3:
            st.metric("Std Dev", f"{std_val:.2f}")
        with col4:
            st.metric("Probability > Limit", f"{p_exceed*100:.1f}%")
        
        st.markdown("---")
        st.subheader("📈 Confidence Intervals")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**90% Confidence Interval**\n\n[{np.percentile(all_simulations, 5):.2f}, {np.percentile(all_simulations, 95):.2f}]")
        with col2:
            st.success(f"**95% Confidence Interval**\n\n[{ci_95_lower:.2f}, {ci_95_upper:.2f}]")
        
        # Regulatory decision
        st.markdown("---")
        st.subheader("⚖️ Regulatory Decision")
        
        if p_exceed < 0.05:
            st.success("✅ **SAFE ZONE - Declare Compliant**\n\nNo enforcement action needed.")
        elif p_exceed > 0.95:
            st.error("❌ **VIOLATION ZONE - Declare Non-Compliant**\n\nEnforcement action recommended.")
        else:
            st.warning("⚠️ **UNCERTAIN ZONE - Need More Data**\n\nCollect additional samples or install CEMS.")
        
        # Display distribution stats
        st.markdown("---")
        st.subheader("📊 Distribution Statistics")
        
        stats_data = {
            "Metric": ["Minimum", "Maximum", "Q1 (25th)", "Q3 (75th)", "2.5th Percentile", "97.5th Percentile"],
            "Value": [
                f"{np.min(all_simulations):.2f}",
                f"{np.max(all_simulations):.2f}",
                f"{np.percentile(all_simulations, 25):.2f}",
                f"{np.percentile(all_simulations, 75):.2f}",
                f"{ci_95_lower:.2f}",
                f"{ci_95_upper:.2f}"
            ]
        }
        st.dataframe(pd.DataFrame(stats_data), use_container_width=True)
        
        # Display sample data for download
        results_df = pd.DataFrame({
            'simulated_values': all_simulations
        })
        
        csv = results_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Simulated Values (CSV)",
            data=csv,
            file_name="monte_carlo_results.csv",
            mime="text/csv"
        )
        
        st.markdown("---")
        st.caption(f"Simulation completed with {total_iterations:,} total iterations")

else:
    st.info("👈 Click 'Run Monte Carlo Simulation' to start")
