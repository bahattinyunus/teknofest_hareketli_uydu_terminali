import streamlit as st
import pandas as pd
import numpy as np
import time
import os

# Set page config for a truly modern, Elite Full-Stack feel
st.set_page_config(
    page_title="GÖKBÖRÜ SOTM Web Dashboard",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for Dark Styling
st.markdown("""
    <style>
    .main {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .metric-card {
        background-color: #21262d;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
    }
    .metric-value {
        font-size: 24px;
        font-weight: bold;
        color: #58a6ff;
    }
    .metric-label {
        font-size: 14px;
        color: #8b949e;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛰️ GÖKBÖRÜ SOTM Web Telemetry Dashboard")
st.markdown("*Real-time remote monitoring and control interface via Streamlit.*")

# Sidebar
st.sidebar.image("assets/logo.png", use_container_width=True)
st.sidebar.markdown("## Control Center")
status = st.sidebar.radio("Mission State", ["Standby", "Active Tracking", "Hardware-in-the-Loop (HIL)"])
st.sidebar.button("Initiate IMU Calibration")
st.sidebar.markdown("---")
st.sidebar.caption("Gökbörü Otonom Sistemleri © 2026")

# Layout Columns
col1, col2, col3, col4 = st.columns(4)

# Live Data Placeholder (Simulated for Web)
def get_live_data():
    return {
        "roll": np.random.normal(0, 1.5),
        "pitch": np.random.normal(0, 1.5),
        "az_err": np.random.normal(0, 0.4),
        "el_err": np.random.normal(0, 0.4),
        "rssi": np.random.normal(-55, 2)
    }

placeholder = st.empty()

# Real-time Loop
for seconds in range(100):
    data = get_live_data()
    
    with placeholder.container():
        # Metrics Top Row
        c1, c2, c3, c4 = st.columns(4)
        c1.metric(label="Tracking Accuracy (Az Error)", value=f"{data['az_err']:.2f}°", delta=f"{0.0-data['az_err']:.2f}°")
        c2.metric(label="Tracking Accuracy (El Error)", value=f"{data['el_err']:.2f}°", delta=f"{0.0-data['el_err']:.2f}°")
        c3.metric(label="System Signal (RSSI)", value=f"{data['rssi']:.1f} dBm")
        c4.metric(label="Platform Pitch", value=f"{data['pitch']:.2f}°")
        
        # Charts
        st.markdown("### 📈 Live Kinematic Telemetry")
        
        # Create a dummy dataframe for charts
        chart_data = pd.DataFrame(
            np.random.randn(20, 3) * [0.4, 0.4, 1.5],
            columns=['Azimuth Error', 'Elevation Error', 'Platform Roll']
        )
        st.line_chart(chart_data)

    time.sleep(0.5)
