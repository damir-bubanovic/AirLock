from typing import List

import geopandas as gpd
import pandas as pd

from .models import GridCell, PostcodePoint
from .config import CRS_OSGB36


# Number of postcodes processed per spatial join batch
CHUNK_SIZE = 100_000


def match_postcodes_to_grid(
    postcodes: List[PostcodePoint],
    gridcells: List[GridCell],
) -> gpd.GeoDataFrame:
    """
    Match each postcode to the grid cell polygon that contains it.

    This implementation is chunked to better handle large postcode datasets.
    It processes the postcode list in batches of CHUNK_SIZE, performing a
    spatial join per chunk and concatenating the results.

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

    # Edge case: no postcodes
    if not postcodes:
        return gpd.GeoDataFrame(
            {
                "postcode": [],
                "easting": [],
                "northing": [],
                "matched_grid_id": [],
                "geometry": [],
            },
            crs=CRS_OSGB36,
        )

    # Build GeoDataFrame for grid cells once
    grid_gdf = gpd.GeoDataFrame(
        {
            "grid_id": [c.id for c in gridcells],
            "center_x": [c.center_x for c in gridcells],
            "center_y": [c.center_y for c in gridcells],
            "geometry": [c.geometry for c in gridcells],
        },
        crs=CRS_OSGB36,
    )

    # Trigger spatial index creation once for efficiency
    _ = grid_gdf.sindex

    chunk_results: List[gpd.GeoDataFrame] = []

    n = len(postcodes)
    for start in range(0, n, CHUNK_SIZE):
        end = min(start + CHUNK_SIZE, n)
        chunk = postcodes[start:end]

        pc_gdf = gpd.GeoDataFrame(
            {
                "postcode": [p.postcode for p in chunk],
                "easting": [p.easting for p in chunk],
                "northing": [p.northing for p in chunk],
                "geometry": [p.geometry for p in chunk],
            },
            crs=CRS_OSGB36,
        )

        joined_chunk = gpd.sjoin(
            pc_gdf,
            grid_gdf,
            how="left",
            predicate="within",
        )

        joined_chunk = joined_chunk.rename(columns={"grid_id": "matched_grid_id"})

        joined_chunk = joined_chunk[
            ["postcode", "easting", "northing", "matched_grid_id", "geometry"]
        ]

        chunk_results.append(joined_chunk)

    # Concatenate all chunks into a single GeoDataFrame
    result_df = pd.concat(chunk_results, ignore_index=True)
    result = gpd.GeoDataFrame(result_df, crs=CRS_OSGB36)

    return result


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
