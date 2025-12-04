import pandas as pd

from airlock.validation import (
    validate_nox_coordinates,
    validate_postcode_coordinates,
)


def test_validate_nox_coordinates():
    df = pd.DataFrame({
        "X": [500000, -10, 800000],
        "Y": [200000, 100000, 2000000],
    })

    result = validate_nox_coordinates(df)

    assert result["total_rows"] == 3
    # Only first row is within BNG ranges
    assert result["valid_coords"] == 1
    assert result["invalid_coords"] == 2
    assert len(result["invalid_examples"]) == 2


def test_validate_postcode_coordinates():
    df = pd.DataFrame({
        "oseast1m": [100000, 750000],
        "osnrth1m": [100000, -50],
    })

    result = validate_postcode_coordinates(df)

    assert result["total_rows"] == 2
    # Only first row valid, second is out of range
    assert result["valid_coords"] == 1
    assert result["invalid_coords"] == 1
    assert len(result["invalid_examples"]) == 1
