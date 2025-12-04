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

    points = load_postcodes_from_dataframe(df, apply_basic_filters=False)

    assert len(points) == 1

    p = points[0]
    assert isinstance(p, PostcodePoint)
    assert p.postcode == "AB1 0AA"
    assert p.easting == 395000
    assert p.northing == 800000
    assert isinstance(p.geometry, Point)
    assert p.geometry.x == 395000
    assert p.geometry.y == 800000


def test_loader_with_filters():
    df = pd.DataFrame({
        "pcd": ["PC1", "PC2", "PC3"],
        "oseast1m": [100, None, 300],
        "osnrth1m": [100, 200, None],
        "doterm": [None, None, "202001"],  # PC3 is terminated
    })

    points = load_postcodes_from_dataframe(df, apply_basic_filters=True)

    # Only PC1 survives: PC2 missing coords, PC3 terminated
    assert len(points) == 1
    p = points[0]
    assert p.postcode == "PC1"
    assert p.easting == 100
    assert p.northing == 100
