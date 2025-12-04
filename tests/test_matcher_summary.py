import geopandas as gpd
from shapely.geometry import Point

from airlock.matcher import summarize_matches
from airlock.config import CRS_OSGB36


def test_summarize_matches():
    gdf = gpd.GeoDataFrame(
        {
            "postcode": ["A", "B", "C"],
            "easting": [1, 2, 3],
            "northing": [1, 2, 3],
            "matched_grid_id": ["X1", None, "X2"],
            "geometry": [Point(1, 1), Point(2, 2), Point(3, 3)],
        },
        crs=CRS_OSGB36,
    )

    summary = summarize_matches(gdf)

    assert summary["total_postcodes"] == 3
    assert summary["matched"] == 2
    assert summary["unmatched"] == 1
    assert summary["match_rate"] == 2 / 3
