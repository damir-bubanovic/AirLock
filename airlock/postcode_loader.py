from typing import List

import pandas as pd
from shapely.geometry import Point

from .models import PostcodePoint

from .validation import validate_postcode_columns


def load_postcodes_from_dataframe(df: pd.DataFrame) -> List[PostcodePoint]:
    """
    Convert a postcode DataFrame (from ONSPD) into a list of PostcodePoint models.

    Required columns:
        - pcd      : postcode
        - oseast1m : easting (OSGB36)
        - osnrth1m : northing (OSGB36)

    Returns:
        List[PostcodePoint]
    """

    # Validate expected columns
    is_valid, missing = validate_postcode_columns(df.columns)
    if not is_valid:
        raise ValueError(f"Postcode dataset missing required columns: {missing}")

    points: List[PostcodePoint] = []

    for _, row in df.iterrows():
        postcode = str(row["pcd"])
        e = row["oseast1m"]
        n = row["osnrth1m"]

        # Skip non-geographic or missing coordinates
        if pd.isna(e) or pd.isna(n):
            continue

        geometry = Point(float(e), float(n))

        points.append(
            PostcodePoint(
                postcode=postcode,
                easting=float(e),
                northing=float(n),
                geometry=geometry,
            )
        )

    return points
