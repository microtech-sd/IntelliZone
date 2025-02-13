import streamlit as st
import matplotlib.pyplot as plt
from pythermalcomfort.models import pmv_ppd_iso
from pythermalcomfort.utilities import met_typical_tasks, clo_typical_ensembles

# Function for Comfort Tips
def get_comfort_tips(pmv):
    if -0.5 <= pmv <= 0.5:
        return "✅ The environment is thermally comfortable. No changes needed."
    elif pmv < -0.5:
        return "❄️ It's too cold! Increase air temperature, reduce airspeed, or wear more clothing."
    else:
        return "🔥 It's too warm! Lower air temperature, increase airspeed, or wear lighter clothing."

# Function for Insightful Explanations
def get_insights(pmv, ppd):
    return (
        f"🔍 **Analysis:**\n\n"
        f"- PMV: {round(pmv, 2)} → Measures thermal sensation from -3 (Cold) to +3 (Hot).\n"
        f"- PPD: {round(ppd, 2)}% → Percentage of people likely to be dissatisfied with the environment.\n\n"
        "**Interpretation:**\n"
        "- If PMV is between -0.5 and 0.5, the majority of people feel comfortable.\n"
        "- If PPD is high (>10%), many occupants may feel discomfort. Adjust conditions accordingly."
    )

# Streamlit Page Configuration
st.set_page_config(page_title="PMV & PPD Calculator", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: #E0E0E0;
        }
        .stButton>button {
            background-color: #1DB954;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🌡️ PMV & PPD Thermal Comfort Calculator")
st.markdown(
    """
    This app calculates **Predicted Mean Vote (PMV)** and **Predicted Percentage of Dissatisfied (PPD)** 
    based on **ASHRAE 55 standards** to assess thermal comfort.
    """
)

# Sidebar Inputs
st.sidebar.header("🎛️ Adjust Input Parameters")

# Environmental Factors
st.sidebar.subheader("🌍 Environmental Conditions")
tdb = st.sidebar.slider("Air Temperature (°C)", 10.0, 40.0, 23.0)
tr = st.sidebar.slider("Mean Radiant Temperature (°C)", 10.0, 40.0, 21.4)
vr = st.sidebar.slider("Air Velocity (m/s)", 0.0, 1.5, 0.1)
rh = st.sidebar.slider("Relative Humidity (%)", 10, 100, 50)

# Personal Factors
st.sidebar.subheader("🧑 Personal Conditions")
met = st.sidebar.selectbox("Metabolic Rate (met)", list(met_typical_tasks.values()), index=3)
clo = st.sidebar.selectbox("Clothing Insulation (clo)", list(clo_typical_ensembles.values()), index=2)

# Layout with Columns
col1, col2 = st.columns([2, 1])

with col1:
    # Button to Calculate
    if st.button("⚡ Calculate PMV & PPD"):
        result = pmv_ppd_iso(tdb=tdb, tr=tr, vr=vr, rh=rh, met=met, clo=clo)
        pmv = result['pmv']
        ppd = result['ppd']

        # Choose Icon Based on PMV Value
        if pmv < -0.5:
            emoji = "❄️"
            color = "blue"
        elif pmv > 0.5:
            emoji = "🔥"
            color = "red"
        else:
            emoji = "✅"
            color = "green"

        # Display Results in Columns
        st.subheader(f"{emoji} Comfort Results")
        st.metric(label="Predicted Mean Vote (PMV)", value=round(pmv, 2))
        st.metric(label="Predicted Percentage of Dissatisfied (PPD) %", value=round(ppd, 2))

        # Comfort Tips
        st.info(get_comfort_tips(pmv))

        # Insightful Explanation
        st.subheader("📖 Understanding Your Results")
        st.markdown(get_insights(pmv, ppd))

        # PMV Visualization Chart
        st.subheader("📊 Thermal Comfort Scale")
        fig, ax = plt.subplots(figsize=(7, 1))
        ax.barh(["Comfort"], [pmv], color=color, height=0.4)
        ax.set_xlim(-3, 3)
        ax.axvline(0, color="black", linestyle="--")
        ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
        ax.set_xticklabels(["Cold", "-2", "-1", "Neutral", "1", "2", "Hot"])
        ax.set_yticks([])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_visible(False)
        st.pyplot(fig)

        # PPD vs PMV Graph
        st.subheader("📈 PPD vs. PMV Relationship")
        pmv_values = [-3, -2, -1, 0, 1, 2, 3]
        ppd_values = [100, 75, 25, 5, 25, 75, 100]
        fig2, ax2 = plt.subplots()
        ax2.plot(pmv_values, ppd_values, marker='o', linestyle='-', color='purple')
        ax2.set_xlabel("PMV")
        ax2.set_ylabel("PPD (%)")
        ax2.set_title("PPD as a Function of PMV")
        ax2.grid(True)
        st.pyplot(fig2)
