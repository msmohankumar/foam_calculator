import streamlit as st
import pandas as pd
from utils.calculations import calculate_foam_requirements
import os

# --- App config ---
st.set_page_config(page_title="PU Foam Calculator", layout="centered")
st.title("PU Foam Shot Calculator")
st.markdown("Calculate required masses for Polyol, c-Pentane, and MDI based on foam size.")

# --- Input Section ---
st.header("Foam Dimensions")
length = st.number_input("Length (cm)", min_value=1.0, value=50.0)
width = st.number_input("Width (cm)", min_value=1.0, value=50.0)
height = st.number_input("Height (cm)", min_value=1.0, value=50.0)

st.header("Material Ratios")
target_density = st.number_input("Target Foam Density (kg/m³)", value=23.6)
polyol_weight = st.number_input("Polyol weight for standard test (g)", value=300.0)
c_pentane_weight = st.number_input("c-Pentane weight for standard test (g)", value=43.0)
mdi_weight = st.number_input("MDI weight for standard test (g)", value=152.0)
polyol_mix_weight = st.number_input("Polyol + Pentane mix weight for standard test (g)", value=114.2)

# --- Calculate ---
if st.button("Calculate Foam Requirements"):
    results = calculate_foam_requirements(
        length, width, height,
        target_density,
        polyol_weight,
        c_pentane_weight,
        mdi_weight,
        polyol_mix_weight
    )

    # --- Display results ---
    st.header("Results")
    st.write(f"Foam Volume: {results['volume_cm3']:.2f} cm³ ({results['volume_m3']:.6f} m³)")
    st.write(f"Total Mass Required: {results['total_mass_g']:.2f} g ({results['total_mass_kg']:.2f} kg)")
    st.write(f"Polyol required: {results['required_polyol']:.2f} g")
    st.write(f"c-Pentane required: {results['required_c_pentane']:.2f} g")
    st.write(f"MDI required: {results['required_mdi']:.2f} g")
    st.write(f"Estimated Foam Thickening Time: {results['thickening_time_sec']} sec (at 25°C)")
    st.write(f"Target Foam Density Reference: {results['target_density']} kg/m³")

    # --- Save results ---
    if st.checkbox("Save results to CSV"):
        if not os.path.exists("data"):
            os.makedirs("data")
        df = pd.DataFrame([results])
        file_path = "data/results.csv"
        if os.path.exists(file_path):
            df.to_csv(file_path, mode="a", index=False, header=False)
        else:
            df.to_csv(file_path, index=False)
        st.success(f"Results saved to {file_path}")
