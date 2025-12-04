import math

from airlock.crs_utils import (
    wgs84_to_osgb36,
    osgb36_to_wgs84,
)


def test_roundtrip_conversion():
    """
    Basic roundtrip test:
    - Convert WGS84 → OSGB36
    - Convert result back → WGS84
    They should be very close to the original coordinates.
    """

    # A known point in London (WGS84)
    lon = -0.1276
    lat = 51.5074

    # Convert → OSGB36
    easting, northing = wgs84_to_osgb36(lon, lat)

    # Convert back → WGS84
    lon2, lat2 = osgb36_to_wgs84(easting, northing)

    # Roundtrip should be within a few meters (~1e-5 degrees)
    assert math.isclose(lon, lon2, rel_tol=1e-5, abs_tol=1e-5)
    assert math.isclose(lat, lat2, rel_tol=1e-5, abs_tol=1e-5)
