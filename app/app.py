import os
import sys

# Ensure project root is on sys.path so "import airlock.XXX" works
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from airlock.grid_builder import build_grid_geodataframe, gridcells_from_geodataframe
from airlock.postcode_loader import load_postcodes_from_dataframe
from airlock.matcher import match_postcodes_to_grid, summarize_matches
from airlock.exporters import prepare_export_table, export_to_excel


st.set_page_config(page_title="AirLock – Postcode to Grid Matcher", layout="wide")

st.title("AirLock – UK Postcode to 1 km Grid Cell Matcher")
st.write("Upload NOx grid data and ONSPD postcode data to generate matches.")


# -----------------------
# File Upload Section
# -----------------------

st.header("1. Upload Data Files")

nox_file = st.file_uploader("NOx grid dataset (CSV)", type=["csv"])
pc_file = st.file_uploader("ONSPD postcode dataset (CSV)", type=["csv"])


# -----------------------
# Data Loading
# -----------------------

if nox_file and pc_file:
    st.subheader("Loading datasets...")

    nox_df = pd.read_csv(nox_file)
    pc_df = pd.read_csv(pc_file)

    st.success("Files loaded successfully.")

    # -----------------------
    # Build grid polygons
    # -----------------------
    st.subheader("Building grid polygons...")
    grid_gdf = build_grid_geodataframe(nox_df)
    grid_cells = gridcells_from_geodataframe(grid_gdf)
    st.write(f"Loaded **{len(grid_cells)}** grid cells.")

    # -----------------------
    # Load postcodes
    # -----------------------
    st.subheader("Processing postcodes...")
    postcodes = load_postcodes_from_dataframe(pc_df)
    st.write(f"Loaded **{len(postcodes)}** cleaned postcode points.")

    # -----------------------
    # Run matcher
    # -----------------------
    st.subheader("Matching postcodes to grid cells...")
    match_gdf = match_postcodes_to_grid(postcodes, grid_cells)

    summary = summarize_matches(match_gdf)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total postcodes", summary["total_postcodes"])
    with col2:
        st.metric("Matched", summary["matched"])
    with col3:
        st.metric("Unmatched", summary["unmatched"])
    with col4:
        st.metric("Match rate", f"{summary['match_rate']*100:.2f}%")

    # -----------------------
    # Preview table
    # -----------------------
    st.subheader("Preview Match Results")
    st.dataframe(match_gdf.head(20))

    # -----------------------
    # Export to Excel
    # -----------------------
    st.subheader("Export Results")
    export_df = prepare_export_table(match_gdf)

    if st.button("Download Excel File"):
        export_path = "airlock_output.xlsx"
        export_to_excel(export_df, export_path)
        st.success(f"Excel exported to: {export_path}")
