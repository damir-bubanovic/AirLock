from __future__ import annotations

from typing import Optional

import pandas as pd


def filter_postcodes_basic(
    df: pd.DataFrame,
    drop_missing_coords: bool = True,
    drop_duplicates: bool = True,
    termination_column: Optional[str] = "doterm",
    only_active: bool = True,
) -> pd.DataFrame:
    """
    Apply basic cleaning to an ONSPD-style postcode DataFrame.

    Operations:
        - Optionally drop rows with missing easting/northing
        - Optionally drop duplicate postcodes
        - Optionally keep only active (non-terminated) postcodes

    Args:
        df: Input postcode DataFrame.
        drop_missing_coords: If True, drop rows with NaN in oseast1m/osnrth1m.
        drop_duplicates: If True, drop duplicate 'pcd' values (keep first).
        termination_column: Column indicating termination date (e.g. 'doterm').
        only_active: If True, keep only rows where termination_column is NaN or empty.

    Returns:
        Cleaned DataFrame.
    """

    cleaned = df.copy()

    # 1) Drop missing coordinates
    if drop_missing_coords:
        if "oseast1m" in cleaned.columns and "osnrth1m" in cleaned.columns:
            cleaned = cleaned.dropna(subset=["oseast1m", "osnrth1m"])

    # 2) Keep only active postcodes (no termination date)
    if only_active and termination_column and termination_column in cleaned.columns:
        cleaned = cleaned[
            cleaned[termination_column].isna() |
            (cleaned[termination_column] == "") |
            (cleaned[termination_column] == " ")
        ]

    # 3) Drop duplicate postcodes
    if drop_duplicates and "pcd" in cleaned.columns:
        cleaned = cleaned.drop_duplicates(subset=["pcd"])

    return cleaned
