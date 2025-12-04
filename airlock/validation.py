from typing import Iterable, List, Tuple

import pandas as pd

from .config import (
    NOX_REQUIRED_COLUMNS,
    POSTCODE_REQUIRED_COLUMNS,
)


# ---------------------------------------------------------------------------
# Column presence validation
# ---------------------------------------------------------------------------

def _missing_columns(
    available_columns: Iterable[str],
    required_columns: Iterable[str],
) -> List[str]:
    """
    Return a list of required columns that are missing
    from the available columns.
    """
    available = {c.lower() for c in available_columns}
    missing = [col for col in required_columns if col.lower() not in available]
    return missing


def validate_nox_columns(columns: Iterable[str]) -> Tuple[bool, List[str]]:
    """
    Validate that the NOx grid dataset has the required columns.

    Returns:
        (is_valid, missing_columns)
    """
    missing = _missing_columns(columns, NOX_REQUIRED_COLUMNS)
    return len(missing) == 0, missing


def validate_postcode_columns(columns: Iterable[str]) -> Tuple[bool, List[str]]:
    """
    Validate that the ONS postcode dataset has the required columns.

    Returns:
        (is_valid, missing_columns)
    """
    missing = _missing_columns(columns, POSTCODE_REQUIRED_COLUMNS)
    return len(missing) == 0, missing


# ---------------------------------------------------------------------------
# Coordinate quality validation (BNG ranges)
# ---------------------------------------------------------------------------

# Approximate valid British National Grid ranges (meters)
BNG_EASTING_MIN = 0
BNG_EASTING_MAX = 700000
BNG_NORTHING_MIN = 0
BNG_NORTHING_MAX = 1300000


def _validate_bng_frame(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
) -> dict:
    """
    Generic validator for BNG coordinates in a DataFrame.

    Returns a dict:
        {
            "total_rows": int,
            "valid_coords": int,
            "invalid_coords": int,
            "invalid_examples": [row_indices],
        }
    """
    if x_col not in df.columns or y_col not in df.columns:
        raise ValueError(
            f"DataFrame must contain '{x_col}' and '{y_col}' columns."
        )

    total = len(df)

    # Convert to numeric and treat non-numeric as NaN
    x = pd.to_numeric(df[x_col], errors="coerce")
    y = pd.to_numeric(df[y_col], errors="coerce")

    valid_mask = (
        x.between(BNG_EASTING_MIN, BNG_EASTING_MAX)
        & y.between(BNG_NORTHING_MIN, BNG_NORTHING_MAX)
    )

    valid = int(valid_mask.sum())
    invalid = int(total - valid)

    invalid_indices = df.index[~valid_mask].tolist()[:5]

    return {
        "total_rows": int(total),
        "valid_coords": valid,
        "invalid_coords": invalid,
        "invalid_examples": invalid_indices,
    }


def validate_nox_coordinates(df: pd.DataFrame) -> dict:
    """
    Validate NOx grid coordinates (columns: X, Y)
    against plausible BNG ranges.
    """
    return _validate_bng_frame(df, x_col="X", y_col="Y")


def validate_postcode_coordinates(df: pd.DataFrame) -> dict:
    """
    Validate ONSPD postcode coordinates
    (columns: oseast1m, osnrth1m)
    against plausible BNG ranges.
    """
    return _validate_bng_frame(df, x_col="oseast1m", y_col="osnrth1m")
