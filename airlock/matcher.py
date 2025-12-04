from typing import List

import geopandas as gpd

from .models import GridCell, PostcodePoint
from .config import CRS_OSGB36


def match_postcodes_to_grid(
    postcodes: List[PostcodePoint],
    gridcells: List[GridCell],
) -> gpd.GeoDataFrame:
    """
    Match each postcode to the grid cell polygon that contains it.

    Args:
        postcodes: List of PostcodePoint models.
        gridcells: List of GridCell models.

    Returns:
        GeoDataFrame with columns:
            - postcode
            - easting
            - northing
            - matched_grid_id
            - geometry (postcode point)
    """

    # Build GeoDataFrame for postcodes
    pc_gdf = gpd.GeoDataFrame(
        {
            "postcode": [p.postcode for p in postcodes],
            "easting": [p.easting for p in postcodes],
            "northing": [p.northing for p in postcodes],
            "geometry": [p.geometry for p in postcodes],
        },
        crs=CRS_OSGB36,
    )

    # Build GeoDataFrame for grid cells
    grid_gdf = gpd.GeoDataFrame(
        {
            "grid_id": [c.id for c in gridcells],
            "center_x": [c.center_x for c in gridcells],
            "center_y": [c.center_y for c in gridcells],
            "geometry": [c.geometry for c in gridcells],
        },
        crs=CRS_OSGB36,
    )

    # Trigger spatial index creation for faster joins on large datasets
    _ = grid_gdf.sindex

    # Spatial join: which polygon contains each postcode point
    joined = gpd.sjoin(
        pc_gdf,
        grid_gdf,
        how="left",
        predicate="within",
    )

    # Rename for clarity
    joined = joined.rename(columns={"grid_id": "matched_grid_id"})

    return joined[["postcode", "easting", "northing", "matched_grid_id", "geometry"]]


def summarize_matches(match_gdf: gpd.GeoDataFrame) -> dict:
    """
    Produce simple summary statistics for the postcode-to-grid mapping.

    Returns:
        {
            "total_postcodes": int,
            "matched": int,
            "unmatched": int,
            "match_rate": float (0–1),
        }
    """

    total = len(match_gdf)
    matched = match_gdf["matched_grid_id"].notna().sum()
    unmatched = total - matched

    match_rate = matched / total if total > 0 else 0.0

    return {
        "total_postcodes": int(total),
        "matched": int(matched),
        "unmatched": int(unmatched),
        "match_rate": float(match_rate),
    }
