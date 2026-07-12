"""Starter Streamlit interface for the future surrogate model."""

import streamlit as st
from src.metrics import pumping_power

st.set_page_config(page_title="Cold-Plate Design Tool", layout="wide")
st.title("AI-Assisted Microchannel Cold-Plate Design Tool")

flow = st.sidebar.slider("Total flow rate (L/min)", 0.05, 0.40, 0.20, 0.01)
power = st.sidebar.slider("Chip power (W)", 50, 200, 100)
width = st.sidebar.slider("Channel width (mm)", 0.30, 0.80, 0.50, 0.05)
height = st.sidebar.slider("Channel height (mm)", 0.30, 0.80, 0.50, 0.05)

st.write(
    {
        "chip_power_W": power,
        "flow_rate_L_min": flow,
        "channel_width_mm": width,
        "channel_height_mm": height,
    }
)
st.info("Load a trained surrogate model here after COMSOL data generation.")
st.metric(
    "Illustrative hydraulic pumping power",
    f"{pumping_power(3000, flow):.4f} W",
    help="Uses a placeholder pressure drop of 3000 Pa.",
)
