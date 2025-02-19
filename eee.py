import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Function to calculate compressor performance
def calculate_compressor(mass_flow_rate, inlet_temp, inlet_pressure, efficiency):
    # Assuming ideal gas behavior and isentropic process
    # For simplicity, we will use a fixed pressure ratio
    pressure_ratio = 3.0  # Example pressure ratio
    outlet_pressure = inlet_pressure * pressure_ratio
    # Isentropic efficiency
    outlet_temp = inlet_temp * (outlet_pressure / inlet_pressure) ** ((1.4 - 1) / 1.4)  # Ideal gas
    work_input = mass_flow_rate * (outlet_temp - inlet_temp) * 1.005  # kJ/kg for air
    return outlet_temp, outlet_pressure, work_input

# Function to calculate evaporator performance
def calculate_evaporator(mass_flow_rate, inlet_temp, inlet_pressure, efficiency):
    # Assuming ideal gas behavior
    outlet_temp = inlet_temp - 10  # Example temperature drop
    heat_absorbed = mass_flow_rate * (inlet_temp - outlet_temp) * 1.005  # kJ/kg for air
    return outlet_temp, heat_absorbed

# Function to calculate condenser performance
def calculate_condenser(mass_flow_rate, inlet_temp, inlet_pressure, efficiency):
    # Assuming ideal gas behavior
    outlet_temp = inlet_temp + 10  # Example temperature rise
    heat_released = mass_flow_rate * (outlet_temp - inlet_temp) * 1.005  # kJ/kg for air
    return outlet_temp, heat_released

# Function to calculate expansion valve performance
def calculate_expansion_valve(inlet_temp, inlet_pressure):
    # Assuming a drop in pressure and temperature
    outlet_pressure = inlet_pressure * 0.5  # Example pressure drop
    outlet_temp = inlet_temp - 5  # Example temperature drop
    return outlet_temp, outlet_pressure

# Function to calculate overall HVAC performance
def calculate_hvac_performance(temp, pressure, mass_flow_rate, efficiency):
    # Compressor calculations
    comp_out_temp, comp_out_pressure, work_input = calculate_compressor(mass_flow_rate, temp, pressure, efficiency)
    
    # Evaporator calculations
    evap_out_temp, heat_absorbed = calculate_evaporator(mass_flow_rate, comp_out_temp, comp_out_pressure, efficiency)
    
    # Condenser calculations
    cond_out_temp, heat_released = calculate_condenser(mass_flow_rate, evap_out_temp, comp_out_pressure, efficiency)
    
    # Expansion valve calculations
    exp_out_temp, exp_out_pressure = calculate_expansion_valve(cond_out_temp, comp_out_pressure)
    
    return {
        "Compressor Outlet Temp (°C)": comp_out_temp,
        "Compressor Outlet Pressure (Pa)": comp_out_pressure,
        "Work Input (kJ)": work_input,
        "Evaporator Outlet Temp (°C)": evap_out_temp,
        "Heat Absorbed (kJ)": heat_absorbed,
        "Condenser Outlet Temp (°C)": cond_out_temp,
        "Heat Released (kJ)": heat_released,
        "Expansion Valve Outlet Temp (°C)": exp_out_temp,
        "Expansion Valve Outlet Pressure (Pa)": exp_out_pressure,
    }

# Streamlit UI
st.title("HVAC System Energy, Entropy, and Exergy Calculator")

# Input fields
st.sidebar.header("Input Parameters")
temp = st.sidebar.number_input("Inlet Temperature (°C)", value=25.0)
pressure = st.sidebar.number_input("Inlet Pressure (Pa)", value=101325.0)
mass_flow_rate = st.sidebar.number_input("Mass Flow Rate (kg/s)", value=1.0)
efficiency = st.sidebar.number_input("Efficiency (%)", value=90.0) / 100.0

# Buttons to run calculations and reset inputs
if st.sidebar.button("Run Calculations"):
    results = calculate_hvac_performance(temp, pressure, mass_flow_rate, efficiency)
    
    # Display results
    st.subheader("Calculation Results")
    results_df = pd.DataFrame(results, index=[0])
   
