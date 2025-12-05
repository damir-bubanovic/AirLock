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
from airlock.validation import (
    validate_nox_columns,
    validate_postcode_columns,
    validate_nox_coordinates,
    validate_postcode_coordinates,
)
from airlock.methods_summary import generate_methods_summary

# -------------------------------------------------------------------
# Page config
# -------------------------------------------------------------------
st.set_page_config(
    page_title="AirLock – Postcode to Grid Matcher",
    layout="wide",
)

# -------------------------------------------------------------------
# Sidebar
# -------------------------------------------------------------------
st.sidebar.title("AirLock")
st.sidebar.markdown(
    "Air-quality Integrated Raster–Location Concordance\n\n"
    "1. Upload NOx grid (DEFRA PCM)\n"
    "2. Upload ONSPD postcode CSV\n"
    "3. Run matching and download outputs."
)

st.sidebar.header("Upload data")
nox_file = st.sidebar.file_uploader("NOx grid dataset (CSV)", type=["csv"])
pc_file = st.sidebar.file_uploader("ONSPD postcode dataset (CSV)", type=["csv"])

st.sidebar.markdown("---")
st.sidebar.caption("All processing happens locally on this machine.")


# -------------------------------------------------------------------
# Main title
# -------------------------------------------------------------------
st.title("UK Postcode → 1 km NOx Grid Cell Matcher")
st.write(
    "This tool links UK postcodes (ONSPD) to 1 km grid cells from the "
    "DEFRA NOx dataset using British National Grid (OSGB36) coordinates."
)


@st.cache_data(show_spinner=False)
def cached_read_csv(uploaded_file):
    """Cached CSV reader to speed up re-runs."""
    return pd.read_csv(uploaded_file)


# -------------------------------------------------------------------
# Data Loading and Processing
# -------------------------------------------------------------------
if nox_file and pc_file:
    st.header("Step 1 – Load and Validate Datasets")

    with st.spinner("Reading CSV files..."):
        try:
            nox_df = cached_read_csv(nox_file)
            pc_df = cached_read_csv(pc_file)
        except Exception as e:
            st.error(f"Failed to read uploaded files: {e}")
            st.stop()

    # Column validation
    is_valid_nox, missing_nox = validate_nox_columns(nox_df.columns)
    if not is_valid_nox:
        st.error(f"NOx dataset is missing required columns: {missing_nox}")
        st.stop()

    is_valid_pc, missing_pc = validate_postcode_columns(pc_df.columns)
    if not is_valid_pc:
        st.error(f"Postcode dataset is missing required columns: {missing_pc}")
        st.stop()

    # Coordinate sanity checks (non-fatal warnings)
    nox_coord_report = validate_nox_coordinates(nox_df)
    pc_coord_report = validate_postcode_coordinates(pc_df)

    cols_val = st.columns(2)
    with cols_val[0]:
        st.markdown("**NOx grid – coordinate quality**")
        st.write(
            f"Total rows: {nox_coord_report['total_rows']}  \n"
            f"Valid coordinates: {nox_coord_report['valid_coords']}  \n"
            f"Invalid coordinates: {nox_coord_report['invalid_coords']}"
        )
        if nox_coord_report["invalid_coords"] > 0:
            st.warning(
                "NOx dataset contains invalid OSGB36 coordinates. "
                f"Example row indices: {nox_coord_report['invalid_examples']}"
            )

    with cols_val[1]:
        st.markdown("**Postcodes – coordinate quality**")
        st.write(
            f"Total rows: {pc_coord_report['total_rows']}  \n"
            f"Valid coordinates: {pc_coord_report['valid_coords']}  \n"
            f"Invalid coordinates: {pc_coord_report['invalid_coords']}"
        )
        if pc_coord_report["invalid_coords"] > 0:
            st.warning(
                "Postcode dataset contains invalid OSGB36 coordinates. "
                f"Example row indices: {pc_coord_report['invalid_examples']}"
            )

    st.success("Files loaded and validated.")

    # -------------------------------------------------------------------
    # Grid polygons
    # -------------------------------------------------------------------
    st.header("Step 2 – Build 1 km Grid Polygons")

    try:
        with st.spinner("Generating 1 km grid polygons from NOx centres..."):
            grid_gdf = build_grid_geodataframe(nox_df)
            grid_cells = gridcells_from_geodataframe(grid_gdf)
    except Exception as e:
        st.error(f"Error while building grid polygons: {e}")
        st.stop()

    st.write(f"Loaded **{len(grid_cells)}** grid cells.")

    # -------------------------------------------------------------------
    # Postcode points
    # -------------------------------------------------------------------
    st.header("Step 3 – Process Postcodes")

    try:
        with st.spinner("Converting postcode coordinates to points..."):
            postcodes = load_postcodes_from_dataframe(pc_df)
    except Exception as e:
        st.error(f"Postcode loading failed: {e}")
        st.stop()

    st.write(f"Loaded **{len(postcodes)}** cleaned postcode points.")

    # -------------------------------------------------------------------
    # Matching
    # -------------------------------------------------------------------
    st.header("Step 4 – Match Postcodes to Grid Cells")

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

    # -------------------------------------------------------------------
    # Results tabs
    # -------------------------------------------------------------------
    st.header("Step 5 – Inspect Results")

    tab1, tab2, tab3 = st.tabs(
        ["Preview (first 20 rows)", "Full matched table", "Unmatched postcodes"]
    )

    with tab1:
        st.subheader("Preview – first 20 rows")
        st.dataframe(match_gdf.head(20))

    with tab2:
        st.subheader("Full matched table")
        st.dataframe(match_gdf)

    with tab3:
        st.subheader("Unmatched postcodes")
        unmatched = match_gdf[match_gdf["matched_grid_id"].isna()].copy()

        if unmatched.empty:
            st.success("All postcodes were successfully matched to grid cells.")
        else:
            st.warning(
                f"{len(unmatched)} postcodes could not be matched to any grid cell."
            )
            st.dataframe(unmatched.head(50))

            # Allow download of unmatched-only list
            unmatched_export = unmatched[["postcode", "easting", "northing"]].copy()
            b_unmatched: Any = BytesIO()
            unmatched_export.to_excel(b_unmatched, index=False, engine="openpyxl")
            b_unmatched.seek(0)

            st.download_button(
                label="Download unmatched postcodes (Excel)",
                data=b_unmatched,
                file_name="airlock_unmatched_postcodes.xlsx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "spreadsheetml.sheet"
                ),
            )

    # -------------------------------------------------------------------
    # Export matched results
    # -------------------------------------------------------------------
    st.header("Step 6 – Export Matched Results")

    export_df = prepare_export_table(match_gdf)

    buffer: Any = BytesIO()
    export_df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)

    st.download_button(
        label="Download matched grid–postcode table (Excel)",
        data=buffer,
        file_name="airlock_matched_grid_postcodes.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
    )

    st.caption("Exported table lists each postcode and its associated grid cell.")

    # -------------------------------------------------------------------
    # Methods Summary download
    # -------------------------------------------------------------------
    st.header("Step 7 – Export Methods Summary")

    methods_text = generate_methods_summary(
        nox_rows=len(grid_cells),
        postcode_rows=len(postcodes),
        matched_rows=summary["matched"],
        unmatched_rows=summary["unmatched"],
        match_rate=summary["match_rate"],
    )
    methods_bytes = methods_text.encode("utf-8")

    st.download_button(
        label="Download Methods Summary (.txt)",
        data=methods_bytes,
        file_name="airlock_methods_summary.txt",
        mime="text/plain",
    )

else:
    st.info("Use the sidebar to upload both NOx grid and ONSPD postcode CSV files to begin.")
