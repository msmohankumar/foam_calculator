import streamlit as st
import pandas as pd
import numpy as np
import trimesh
import plotly.graph_objects as go
import os
from utils.calculations import calculate_foam_requirements

# --- Page config ---
st.set_page_config(page_title="PU Foam Calculator", layout="wide", page_icon="🧪")

# --- Header ---
st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>PU Foam Shot Calculator 🧪</h1>
<p style='text-align: center;'>Calculate foam requirements and visualize foam filling in a 3D cavity.</p>
""", unsafe_allow_html=True)
st.markdown("---")

# --- Foam Parameters ---
st.header("Foam Dimensions & Material Ratios")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Foam Dimensions")
    foam_size = st.selectbox("Select foam size (cm)",
                             ["Custom", "Small:50x50x50", "Medium:100x60x60", "Large:150x80x70"])
    if foam_size == "Custom":
        length = st.number_input("Length (cm)", 1.0, 500.0, 50.0)
        width = st.number_input("Width (cm)", 1.0, 500.0, 50.0)
        height = st.number_input("Height (cm)", 1.0, 500.0, 50.0)
    else:
        sizes = foam_size.split(":")[1].split("x")
        length, width, height = map(float, sizes)
        st.write(f"Dimensions → L: {length} cm, W: {width} cm, H: {height} cm")

with col2:
    st.subheader("Material Ratios")
    target_density = st.number_input("Target Foam Density (kg/m³)", 10.0, 50.0, 23.6)
    polyol_weight = st.number_input("Polyol weight for standard test (g)", 50.0, 1000.0, 300.0)
    c_pentane_weight = st.number_input("c-Pentane weight for standard test (g)", 10.0, 100.0, 43.0)
    mdi_weight = st.number_input("MDI weight for standard test (g)", 50.0, 500.0, 152.0)
    polyol_mix_weight = st.number_input("Polyol + Pentane mix weight (g)", 50.0, 300.0, 114.2)

st.markdown("---")

# --- Foam Calculation ---
if st.button("Calculate Foam Requirements"):
    results = calculate_foam_requirements(length, width, height,
                                          target_density, polyol_weight,
                                          c_pentane_weight, mdi_weight,
                                          polyol_mix_weight)
    st.header("Results")
    c1, c2, c3 = st.columns(3)
    c1.metric("Foam Volume (cm³)", f"{results['volume_cm3']:.2f}")
    c2.metric("Total Mass (g)", f"{results['total_mass_g']:.2f}")
    c3.metric("Target Density (kg/m³)", f"{results['target_density']:.2f}")

    st.write("### Material Breakdown")
    c1, c2, c3 = st.columns(3)
    c1.success(f"Polyol: {results['required_polyol']:.2f} g")
    c2.info(f"c-Pentane: {results['required_c_pentane']:.2f} g")
    c3.warning(f"MDI: {results['required_mdi']:.2f} g")

    st.write(f"Estimated Foam Thickening Time: {results['thickening_time_sec']} sec")

    # Save results
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

# --- 3D STL Visualization & Bottom-to-Top Foam Fill ---
st.header("3D Foam Flow Visualization")
uploaded_file = st.file_uploader("Upload STL file of cavity", type=["stl"])

if uploaded_file:
    mesh = trimesh.load_mesh(uploaded_file)
    st.write("### 3D Model of Cavity")
    
    # Extract vertices and faces
    vertices = mesh.vertices.copy()
    faces = mesh.faces

    # Plotly initial mesh
    fig = go.Figure(data=[go.Mesh3d(
        x=vertices[:,0], y=vertices[:,1], z=vertices[:,2],
        i=faces[:,0], j=faces[:,1], k=faces[:,2],
        color='lightblue', opacity=0.3, flatshading=True
    )])
    fig.update_layout(scene=dict(aspectmode='data'))
    st.plotly_chart(fig, use_container_width=True)

    # Bottom-to-top foam fill simulation
    st.write("### Foam Expansion Simulation (Bottom-to-Top)")
    steps = st.slider("Animation Steps", 2, 20, 10)
    
    z_min, z_max = vertices[:,2].min(), vertices[:,2].max()
    
    for step in range(1, steps+1):
        fill_height = z_min + (z_max - z_min) * (step / steps)
        
        # Scale vertices: only fill below fill_height
        scaled_vertices = vertices.copy()
        scaled_vertices[:,2] = np.where(scaled_vertices[:,2] <= fill_height,
                                        scaled_vertices[:,2],
                                        z_min + (scaled_vertices[:,2]-z_min)*(step/steps))
        
        fig2 = go.Figure(data=[go.Mesh3d(
            x=scaled_vertices[:,0],
            y=scaled_vertices[:,1],
            z=scaled_vertices[:,2],
            i=faces[:,0], j=faces[:,1], k=faces[:,2],
            color='orange', opacity=0.6, flatshading=True
        )])
        fig2.update_layout(scene=dict(aspectmode='data'))
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("<p style='text-align:center; color:gray;'>Developed by Mohan Kumar</p>", unsafe_allow_html=True)
