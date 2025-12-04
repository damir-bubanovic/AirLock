import geopandas as gpd
from shapely.geometry import Point

from airlock.exporters import prepare_export_table


def test_prepare_export_table():
    gdf = gpd.GeoDataFrame(
        {
            "postcode": ["A", "C", "B"],
            "easting": [1, 3, 2],
            "northing": [10, 30, 20],
            "matched_grid_id": ["G1", "G2", "G1"],
            "geometry": [Point(1, 1), Point(2, 2), Point(3, 3)],
        }
    )

    out = prepare_export_table(gdf)

    # geometry removed
    assert "geometry" not in out.columns

    # Check ordering (G1 first, then G2; postcodes sorted inside each)
    assert list(out["matched_grid_id"]) == ["G1", "G1", "G2"]
    assert list(out["postcode"]) == ["A", "B", "C"]
