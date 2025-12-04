import pandas as pd

from airlock.filters import filter_postcodes_basic


def test_filter_postcodes_basic():
    df = pd.DataFrame({
        "pcd": ["PC1", "PC2", "PC2", "PC3"],
        "oseast1m": [100, None, 200, 300],
        "osnrth1m": [100, 150, None, 350],
        "doterm": [None, "202001", "", None],
    })

    cleaned = filter_postcodes_basic(df)

    # PC1: coords ok, active -> keep
    # PC2: row1 has missing easting, row2 missing northing => removed by drop_missing_coords
    # PC3: coords ok, active -> keep
    # Duplicates: only first occurrence of each pcd would be kept (but only PC1/PC3 survive coords filter)

    assert list(cleaned["pcd"]) == ["PC1", "PC3"]
    assert cleaned["oseast1m"].tolist() == [100, 300]
    assert cleaned["osnrth1m"].tolist() == [100, 350]
