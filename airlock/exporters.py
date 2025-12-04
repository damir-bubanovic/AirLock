import pandas as pd
from geopandas import GeoDataFrame


def prepare_export_table(match_gdf: GeoDataFrame) -> pd.DataFrame:
    """
    Convert the geo-based match result into a clean DataFrame
    suitable for Excel export.

    Output columns:
        - postcode
        - easting
        - northing
        - matched_grid_id
    """

    # Drop geometry column for Excel export
    if "geometry" in match_gdf.columns:
        df = match_gdf.drop(columns=["geometry"]).copy()
    else:
        df = match_gdf.copy()

    # Sort by grid ID then postcode for readability
    df = df.sort_values(by=["matched_grid_id", "postcode"], na_position="last")

    return df.reset_index(drop=True)


def export_to_excel(df: pd.DataFrame, filepath: str) -> None:
    """
    Export the prepared DataFrame to Excel (.xlsx).

    Uses pandas Excel writer (openpyxl/xlsxwriter).
    """

    # Ensure .xlsx extension
    if not filepath.lower().endswith(".xlsx"):
        filepath += ".xlsx"

    df.to_excel(filepath, index=False)
