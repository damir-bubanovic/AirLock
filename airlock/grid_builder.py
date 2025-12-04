from typing import List

import geopandas as gpd
from shapely.geometry import Polygon

from .config import (
    CRS_OSGB36,
    GRID_CELL_SIZE_M,
)
from .models import GridCell


def cell_polygon_from_center(x: float, y: float) -> Polygon:
    """
    Given the center point (X, Y) of a 1 km grid cell (in OSGB36),
    return a Shapely Polygon representing the cell boundaries.

    NOx cells are 1 km × 1 km, so half-size = 500 m in each direction.
    """
    half = GRID_CELL_SIZE_M / 2

    return Polygon([
        (x - half, y - half),
        (x + half, y - half),
        (x + half, y + half),
        (x - half, y + half),
    ])


def build_grid_geodataframe(df) -> gpd.GeoDataFrame:
    """
    Convert a NOx grid DataFrame with X/Y columns into a GeoDataFrame
    containing 1 km grid polygons.

    Args:
        df: Pandas DataFrame with at least columns "X" and "Y".

    Returns:
        GeoDataFrame containing:
        - original columns
        - geometry column with 1 km polygons
        - CRS set to OSGB36
    """
    if "X" not in df.columns or "Y" not in df.columns:
        raise ValueError("NOx dataset must contain 'X' and 'Y' columns.")

    geometries: List[Polygon] = [
        cell_polygon_from_center(row["X"], row["Y"])
        for _, row in df.iterrows()
    ]

    gdf = gpd.GeoDataFrame(df.copy(), geometry=geometries, crs=CRS_OSGB36)
    return gdf


def gridcells_from_geodataframe(
    gdf: gpd.GeoDataFrame,
    id_column: str | None = "GridCode",
) -> List[GridCell]:
    """
    Convert a NOx grid GeoDataFrame into a list of GridCell models.

    Args:
        gdf: GeoDataFrame with at least columns X, Y, geometry.
        id_column: Optional column to use as the grid cell identifier.
                   If missing or None, a fallback ID based on X/Y is used.

    Returns:
        List[GridCell]
    """
    cells: List[GridCell] = []

    use_id_column = id_column is not None and id_column in gdf.columns

    for _, row in gdf.iterrows():
        if use_id_column:
            cell_id = str(row[id_column])
        else:
            # Fallback: stable ID from centre coordinates
            cell_id = f"{int(row['X'])}_{int(row['Y'])}"

        cell = GridCell(
            id=cell_id,
            center_x=float(row["X"]),
            center_y=float(row["Y"]),
            geometry=row.geometry,
        )
        cells.append(cell)

    return cells
