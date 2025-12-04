import pandas as pd
from shapely.geometry import Polygon

from airlock.grid_builder import (
    cell_polygon_from_center,
    build_grid_geodataframe,
)


def test_cell_polygon_shape():
    """
    A polygon generated from a centre point should have:
    - 4 sides (square)
    - Correct corner coordinates for a 1 km grid cell
    """

    x, y = 500000, 200000   # arbitrary OSGB36 coordinates
    poly = cell_polygon_from_center(x, y)

    assert isinstance(poly, Polygon)
    assert len(poly.exterior.coords) == 5  # square = 4 corners + repeated first

    # Verify expected bounds (±500 m)
    minx, miny, maxx, maxy = poly.bounds
    assert minx == x - 500
    assert maxx == x + 500
    assert miny == y - 500
    assert maxy == y + 500


def test_build_grid_geodataframe():
    """
    Ensure the builder converts a DataFrame into a valid GeoDataFrame
    with correct geometry.
    """
    df = pd.DataFrame({
        "X": [500000],
        "Y": [200000],
        "NOx": [15.2],
    })

    gdf = build_grid_geodataframe(df)

    assert len(gdf) == 1
    assert "geometry" in gdf.columns
    assert gdf.geometry.iloc[0].bounds == (499500, 199500, 500500, 200500)
