import os
import sys
from io import BytesIO
from typing import Any

# Ensure project root is on sys.path so "import airlock.XXX" works
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import streamlit as st
import pandas as pd

from airlock.grid_builder import build_grid_geodataframe, gridcells_from_geodataframe
from airlock.postcode_loader import load_postcodes_from_dataframe
from airlock.matcher import match_postcodes_to_grid, summarize_matches
from airlock.exporters import prepare_export_table


st.set_page_config(
    page_title="AirLock – Postcode to Grid Matcher",
    layout="wide",
)

st.title("AirLock – UK Postcode to 1 km Grid Cell Matcher")
st.write("Upload NOx grid data and ONSPD postcode data to generate matches.")


@st.cache_data(show_spinner=False)
def cached_read_csv(uploaded_file):
    """Cached CSV reader to speed up re-runs."""
    return pd.read_csv(uploaded_file)


# -----------------------
# File Upload Section
# -----------------------

st.header("1. Upload Data Files")

nox_file = st.file_uploader("NOx grid dataset (CSV)", type=["csv"])
pc_file = st.file_uploader("ONSPD postcode dataset (CSV)", type=["csv"])


# -----------------------
# Data Loading and Processing
# -----------------------

if nox_file and pc_file:
    st.subheader("Loading datasets...")

    with st.spinner("Reading CSV files..."):
        try:
            nox_df = cached_read_csv(nox_file)
            pc_df = cached_read_csv(pc_file)
        except Exception as e:
            st.error(f"Failed to read uploaded files: {e}")
            st.stop()

    st.success("Files loaded successfully.")

    # -----------------------
    # Build grid polygons
    # -----------------------
    st.subheader("Building grid polygons...")
    try:
        with st.spinner("Generating 1 km grid polygons..."):
            grid_gdf = build_grid_geodataframe(nox_df)
            grid_cells = gridcells_from_geodataframe(grid_gdf)
    except Exception as e:
        st.error(f"Error while building grid polygons: {e}")
        st.stop()

    st.write(f"Loaded **{len(grid_cells)}** grid cells.")

    # -----------------------
    # Load postcodes
    # -----------------------
    st.subheader("Processing postcodes...")
    try:
        with st.spinner("Converting postcode coordinates to points..."):
            postcodes = load_postcodes_from_dataframe(pc_df)
    except Exception as e:
        st.error(f"Postcode loading failed: {e}")
        st.stop()

    st.write(f"Loaded **{len(postcodes)}** cleaned postcode points.")

    # -----------------------
    # Run matcher
    # -----------------------
    st.subheader("Matching postcodes to grid cells...")
    try:
        with st.spinner("Spatial matching in progress..."):
            match_gdf = match_postcodes_to_grid(postcodes, grid_cells)
    except Exception as e:
        st.error(f"Error during spatial matching: {e}")
        st.stop()

    summary = summarize_matches(match_gdf)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total postcodes", summary["total_postcodes"])
    with col2:
        st.metric("Matched", summary["matched"])
    with col3:
        st.metric("Unmatched", summary["unmatched"])
    with col4:
        st.metric("Match rate", f"{summary['match_rate'] * 100:.2f}%")

    # -----------------------
    # Preview table
    # -----------------------
    st.subheader("Preview Match Results")

    tab1, tab2 = st.tabs(["Preview (first 20 rows)", "Full table"])
    with tab1:
        st.dataframe(match_gdf.head(20))
    with tab2:
        st.dataframe(match_gdf)

    # -----------------------
    # Export to Excel (download)
    # -----------------------
    st.subheader("Export Results")
    export_df = prepare_export_table(match_gdf)

    # Use Any to satisfy the type checker while still using BytesIO
    buffer: Any = BytesIO()
    export_df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)

    st.download_button(
        label="Download Excel",
        data=buffer,
        file_name="airlock_output.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )
