import streamlit as st
import numpy as np
import math

def calculate_pmv_ppd(met, clo, t_a, t_r, v_a, rh):
    """Calculates PMV and PPD based on Fanger's model."""
    # Constants
    M = met * 58.15  # Convert met to W/m²
    W = 0  # External work (assumed negligible)
    I_cl = clo * 0.155  # Convert clothing insulation to m²K/W
    f_cl = 1.05 if I_cl < 0.078 else 1.05 + 0.645 * (I_cl - 0.078)
    t_a_k = t_a + 273.15  # Convert to Kelvin
    t_r_k = t_r + 273.15  # Convert to Kelvin
    p_a = rh * 0.01 * 6.105 * math.exp(17.27 * t_a / (237.7 + t_a))  # Water vapor pressure (Pa)
    
    # Heat transfer coefficients
    h_c = 12.1 * np.sqrt(v_a) if v_a > 0 else 3.0  # Convective heat transfer coefficient
    t_cl = t_a + (35.5 - t_a) / (3.5 * (I_cl + 0.1))  # Clothing surface temp estimate
    h_r = 4.0 * 5.67e-8 * f_cl * ((t_cl + t_r_k) ** 4 - (t_r_k ** 4)) / (t_cl - t_r_k)
    h_c = max(h_c, 2.38 * abs(t_cl - t_a) ** 0.25)  # Update h_c based on temperature diff
    
    # PMV calculation
    L = (M - W) - 3.96e-8 * f_cl * ((t_cl + t_r_k) ** 4 - (t_r_k ** 4)) - f_cl * h_c * (t_cl - t_a)
    PMV = (0.303 * math.exp(-0.036 * M) + 0.028) * L
    PPD = 100 - 95 * math.exp(-0.03353 * PMV ** 4 - 0.2179 * PMV ** 2)
    
    return round(PMV, 2), round(PPD, 2)

# Streamlit UI
st.title("Thermal Comfort Calculator")
st.write("Calculate PMV (Predicted Mean Vote) and PPD (Predicted Percentage of Dissatisfied) based on environmental conditions.")

# Sidebar inputs
met = st.sidebar.slider("Metabolic Rate (met)", 0.8, 2.0, 1.2, 0.1)
clo = st.sidebar.slider("Clothing Insulation (clo)", 0.0, 2.0, 0.5, 0.1)
t_a = st.sidebar.slider("Air Temperature (°C)", 10.0, 40.0, 24.0, 0.1)
t_r = st.sidebar.slider("Mean Radiant Temperature (°C)", 10.0, 40.0, 24.0, 0.1)
v_a = st.sidebar.slider("Air Velocity (m/s)", 0.0, 1.0, 0.1, 0.01)
rh = st.sidebar.slider("Relative Humidity (%)", 0, 100, 50, 1)

# Calculate PMV and PPD
pmv, ppd = calculate_pmv_ppd(met, clo, t_a, t_r, v_a, rh)

# Display results
st.subheader("Results")
st.write(f"**Predicted Mean Vote (PMV):** {pmv}")
st.write(f"**Predicted Percentage of Dissatisfied (PPD):** {ppd}%")

# Interpretation
if abs(pmv) <= 0.5:
    st.success("Thermal comfort is within an acceptable range.")
elif abs(pmv) <= 1:
    st.warning("Some discomfort may be present.")
else:
    st.error("Significant discomfort detected.")

# Visualization
st.progress(min(int(ppd), 100))
