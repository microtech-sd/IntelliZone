import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pythermalcomfort.models import pmv_ppd, adaptive_ashrae
from pythermalcomfort.utilities import met_typical_tasks, clo_typical_ensembles

# Streamlit App Configuration
st.set_page_config(page_title="Thermal Comfort Analyzer", layout="wide")
st.title("🌡️ Thermal Comfort Analyzer")
st.markdown("Analyze and optimize indoor thermal comfort based on ASHRAE 55 standards.")

# Sidebar Inputs
st.sidebar.header("Environmental Conditions")

temp_air = st.sidebar.slider("Air Temperature (°C)", 10.0, 40.0, 23.0)
temp_mrt = st.sidebar.slider("Mean Radiant Temperature (°C)", 10.0, 40.0, 21.4)
relative_humidity = st.sidebar.slider("Relative Humidity (%)", 10, 90, 50)
air_velocity = st.sidebar.slider("Air Velocity (m/s)", 0.0, 1.5, 0.1)

st.sidebar.header("Personal Factors")
met = st.sidebar.selectbox("Metabolic Rate (MET)", list(met_typical_tasks.values()), index=2)
clo = st.sidebar.selectbox("Clothing Insulation (CLO)", list(clo_typical_ensembles.values()), index=1)

# Calculate PMV & PPD
pmv_value, ppd_value = pmv_ppd(tdb=temp_air, tr=temp_mrt, vr=air_velocity, rh=relative_humidity, met=met, clo=clo, standard="ASHRAE")

# Display Results
st.subheader("🌡️ Predicted Mean Vote (PMV) and Predicted Percentage of Dissatisfied (PPD)")
st.write(f"**PMV:** {pmv_value:.2f} (Ideal Range: -0.5 to +0.5)")
st.write(f"**PPD:** {ppd_value:.1f}% (Should be <10% for optimal comfort)")

# Thermal Comfort Level Interpretation
comfort_status = "✅ Comfortable" if -0.5 <= pmv_value <= 0.5 else "⚠️ Discomfort Detected"
st.markdown(f"**Comfort Status:** {comfort_status}")

# Adaptive Model (for naturally ventilated spaces)
st.subheader("🌍 Adaptive Comfort Model (ASHRAE 55)")
outdoor_temp = st.slider("Outdoor Temperature (°C)", 5.0, 40.0, 20.0)
adaptive_result = adaptive_ashrae(tdb=temp_air, tr=temp_mrt, t_running_mean=outdoor_temp)

st.write(f"**Acceptable Temperature Range:** {adaptive_result['acceptability']} ")

# Visualization: PMV Scale
fig, ax = plt.subplots(figsize=(7, 1))
ax.barh(["PMV"], [pmv_value], color=("green" if -0.5 <= pmv_value <= 0.5 else "red"))
ax.set_xlim([-3, 3])
ax.axvline(x=-0.5, color='gray', linestyle='dashed')
ax.axvline(x=0.5, color='gray', linestyle='dashed')
ax.set_xlabel("Thermal Comfort Scale")
st.pyplot(fig)

# Recommendations
st.subheader("🔍 Recommendations for Improved Comfort")
recommendations = []
if pmv_value > 0.5:
    recommendations.append("❄️ Reduce air temperature or increase air movement.")
if pmv_value < -0.5:
    recommendations.append("🔥 Increase air temperature or wear warmer clothing.")
if relative_humidity > 60:
    recommendations.append("💨 Reduce humidity to avoid discomfort.")
if air_velocity < 0.1:
    recommendations.append("🌬️ Increase air velocity for better cooling.")

for rec in recommendations:
    st.markdown(f"- {rec}")

st.markdown("---")
st.write("**Built for IntelliZone: Smart Climate Control**")
