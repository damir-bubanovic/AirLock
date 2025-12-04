from typing import List

import pandas as pd
from shapely.geometry import Point

from .models import PostcodePoint
from .validation import validate_postcode_columns
from .filters import filter_postcodes_basic


def load_postcodes_from_dataframe(
    df: pd.DataFrame,
    apply_basic_filters: bool = True,
) -> List[PostcodePoint]:
    """
    Convert a postcode DataFrame (from ONSPD) into a list of PostcodePoint models.

    Required columns:
        - pcd      : postcode
        - oseast1m : easting
        - osnrth1m : northing

    Optional:
        - doterm (used by filters)

    Args:
        df: Raw postcode DataFrame.
        apply_basic_filters: If True, clean the DataFrame (drop missing coords,
                             drop duplicates, keep only active codes).

    Returns:
        List[PostcodePoint]
    """

    # Validate expected columns
    is_valid, missing = validate_postcode_columns(df.columns)
    if not is_valid:
        raise ValueError(f"Postcode dataset missing required columns: {missing}")

    # Apply filters (remove missing coords, duplicates, terminated, etc.)
    if apply_basic_filters:
        df = filter_postcodes_basic(df)

    points: List[PostcodePoint] = []

    for _, row in df.iterrows():
        postcode = str(row["pcd"])
        e = row["oseast1m"]
        n = row["osnrth1m"]

        # Safety check in case filters were disabled or incomplete
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
