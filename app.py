import streamlit as st
import pandas as pd
from utils.calculations import calculate_foam_requirements
import os

# --- Page configuration ---
st.set_page_config(page_title="PU Foam Calculator", layout="wide", page_icon="🧪")

# --- Header Section ---
st.markdown(
    """
    <h1 style='text-align: center; color: #2E86C1;'>PU Foam Shot Calculator 🧪</h1>
    <p style='text-align: center; font-size:16px;'>Calculate required masses of Polyol, c-Pentane, and MDI for your foam batch.</p>
    """,
    unsafe_allow_html=True
)

# Add an illustration (public image from internet)
st.image("https://www.chemicalbook.com/ChemicalProductProperty_EN_CB8242363.htm?imgurl=https://www.chemicalbook.com/ProductPicture/0-1-13019.jpg",
         caption="Polyurethane Foam Mixing Illustration", use_column_width=True)

st.markdown("---")

# --- Input Section ---
st.header("Foam Parameters & Materials")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Foam Dimensions")
    # Predefined sizes dropdown
    foam_size = st.selectbox(
        "Select foam size (cm)",
        ["Custom", "Small: 50x50x50", "Medium: 100x60x60", "Large: 150x80x70"]
    )

    if foam_size == "Custom":
        length = st.number_input("Length (cm)", min_value=1.0, value=50.0)
        width = st.number_input("Width (cm)", min_value=1.0, value=50.0)
        height = st.number_input("Height (cm)", min_value=1.0, value=50.0)
    else:
        sizes = foam_size.split(":")[1].split("x")
        length = float(sizes[0])
        width = float(sizes[1])
        height = float(sizes[2])
        st.write(f"Selected Dimensions → L: {length} cm, W: {width} cm, H: {height} cm")

with col2:
    st.subheader("Material Ratios")
    target_density = st.number_input("Target Foam Density (kg/m³)", value=23.6, help="Typical foam density ~23.6 kg/m³")
    polyol_weight = st.number_input("Polyol weight for standard test (g)", value=300.0)
    c_pentane_weight = st.number_input("c-Pentane weight for standard test (g)", value=43.0)
    mdi_weight = st.number_input("MDI weight for standard test (g)", value=152.0)
    polyol_mix_weight = st.number_input("Polyol + Pentane mix weight for standard test (g)", value=114.2)

st.markdown("---")

# --- Calculation ---
if st.button("Calculate Foam Requirements", type="primary"):
    results = calculate_foam_requirements(
        length, width, height,
        target_density,
        polyol_weight,
        c_pentane_weight,
        mdi_weight,
        polyol_mix_weight
    )

    # --- Display results with columns ---
    st.header("Results")
    col1, col2, col3 = st.columns(3)

    col1.metric("Foam Volume (cm³)", f"{results['volume_cm3']:.2f}")
    col2.metric("Total Mass (g)", f"{results['total_mass_g']:.2f}")
    col3.metric("Target Density (kg/m³)", f"{results['target_density']:.2f}")

    st.write("### Material Breakdown")
    col1, col2, col3 = st.columns(3)
    col1.success(f"Polyol: {results['required_polyol']:.2f} g")
    col2.info(f"c-Pentane: {results['required_c_pentane']:.2f} g")
    col3.warning(f"MDI: {results['required_mdi']:.2f} g")

    st.write(f"Estimated Foam Thickening Time: {results['thickening_time_sec']} sec (at 25°C)")

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
        st.success(f"Results saved to `{file_path}`")

st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Developed by Mohan Kumar | PU Foam Lab Assistant</p>",
    unsafe_allow_html=True
)
