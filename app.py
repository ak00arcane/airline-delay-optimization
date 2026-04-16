import streamlit as st
import pandas as pd
import os

# MUST be first Streamlit command
st.set_page_config(
    page_title="Airline Optimization",
    layout="wide",
    initial_sidebar_state="expanded"
)

from model import train_model, predict
from optimizer import optimize
from simulator import simulate

st.title("✈️ Airline Delay Optimization System")

# Sidebar
st.sidebar.header("Controls")
capacity = st.sidebar.slider("Max Flights per Hour", 50, 1000, 300)

# File uploader
file = st.file_uploader("Upload CSV")

# Load data (ONLY ONCE)
if file:
    df = pd.read_csv(file)
else:
    if os.path.exists("sample_data.csv"):
        df = pd.read_csv("sample_data.csv")
    else:
        st.error("No data file found. Please upload a CSV.")
        st.stop()

# Show raw data
st.subheader("Raw Data")
st.dataframe(df)

# Train model
model = train_model(df)
df = predict(model, df)

# Prediction results
st.subheader("🔮 Delay Predictions")
st.dataframe(df[['ORIGIN', 'DEST', 'predicted_delay']])

# Optimization
if st.button("Run Optimization"):
    df = optimize(df, capacity)

    st.subheader("🧮 Optimized Delays")
    st.dataframe(df[['ORIGIN', 'DEST', 'optimized_delay']])

    # Simulation
    df = simulate(df)

    st.subheader("🎮 Simulation Results")
    st.dataframe(df[['ORIGIN', 'DEST', 'simulated_delay']])

    # Metrics
    st.subheader("📊 Metrics")

    col1, col2, col3 = st.columns(3)

    col1.metric("Avg Original Delay", round(df['DEP_DELAY'].mean(), 2))
    col2.metric("Avg Optimized Delay", round(df['optimized_delay'].mean(), 2))
    col3.metric("Avg Simulated Delay", round(df['simulated_delay'].mean(), 2))

    # Charts
    st.subheader("📈 Delay Comparison")
    st.line_chart(df[['DEP_DELAY', 'optimized_delay', 'simulated_delay']])