import pandas as pd
from shapely.geometry import Point

from airlock.postcode_loader import load_postcodes_from_dataframe
from airlock.models import PostcodePoint


def test_load_postcodes_from_dataframe():
    df = pd.DataFrame({
        "pcd": ["AB1 0AA"],
        "oseast1m": [395000],
        "osnrth1m": [800000],
    })

    points = load_postcodes_from_dataframe(df)

    assert len(points) == 1

    p = points[0]
    assert isinstance(p, PostcodePoint)
    assert p.postcode == "AB1 0AA"
    assert p.easting == 395000
    assert p.northing == 800000
    assert isinstance(p.geometry, Point)
    assert p.geometry.x == 395000
    assert p.geometry.y == 800000
