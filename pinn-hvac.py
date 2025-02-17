import streamlit as st
import numpy as np
import torch
import torch.nn as nn
import matplotlib.pyplot as plt

# Define the Physics-Informed Neural Network (PINN) model
class PINN(nn.Module):
    def __init__(self):
        super(PINN, self).__init__()
        self.hidden = nn.Sequential(
            nn.Linear(2, 20), nn.Tanh(),
            nn.Linear(20, 20), nn.Tanh(),
            nn.Linear(20, 1)
        )
    
    def forward(self, x):
        return self.hidden(x)

# Initialize the model
model = PINN()

# Simulated real-time HVAC sensor data (replace with actual sensor data in the future)
def get_real_time_data():
    return {
        "Temperature (°C)": np.random.uniform(20, 26),
        "Airflow (m/s)": np.random.uniform(0.5, 2.5),
        "Humidity (%)": np.random.uniform(30, 60),
        "CO₂ Level (ppm)": np.random.uniform(400, 800)
    }

# Streamlit UI
st.title("🏥 Smart HVAC Monitoring for Hospitals")

st.sidebar.header("🔧 System Controls")
update_interval = st.sidebar.slider("Data Update Interval (seconds)", 1, 10, 3)

# Real-time data visualization
st.subheader("📊 Live Sensor Data")
data = get_real_time_data()
for key, value in data.items():
    st.metric(label=key, value=f"{value:.2f}")

# Prediction & Optimization
st.subheader("🔍 PINN-Based HVAC Optimization")
test_input = torch.tensor([[data["Temperature (°C)"], data["Airflow (m/s)"]]], dtype=torch.float32)
predicted_output = model(test_input).item()
st.write(f"🔹 Optimized Energy Efficiency Score: {predicted_output:.2f}")

# Plot simulation results (placeholder example)
st.subheader("📈 Temperature vs. Airflow Analysis")
x = np.linspace(20, 26, 100)
y = np.sin(x)
plt.plot(x, y, label="Simulated Data")
plt.xlabel("Temperature (°C)")
plt.ylabel("Airflow Efficiency")
plt.legend()
st.pyplot(plt)

st.success("✅ System Running Smoothly! Expandable for IoT & Cloud Integrations.")
