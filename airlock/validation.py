from typing import Iterable, List, Tuple

from .config import (
    NOX_REQUIRED_COLUMNS,
    POSTCODE_REQUIRED_COLUMNS,
)


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
