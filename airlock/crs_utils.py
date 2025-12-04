from typing import Tuple

import geopandas as gpd
from pyproj import Transformer

from .config import CRS_OSGB36, CRS_WGS84

# Pre-built transformers for performance and reuse
_transformer_wgs84_to_osgb36 = Transformer.from_crs(
    CRS_WGS84,
    CRS_OSGB36,
    always_xy=True,
)

_transformer_osgb36_to_wgs84 = Transformer.from_crs(
    CRS_OSGB36,
    CRS_WGS84,
    always_xy=True,
)


def wgs84_to_osgb36(lon: float, lat: float) -> Tuple[float, float]:
    """
    Convert WGS84 (longitude, latitude) to OSGB36 (easting, northing).

    Args:
        lon: Longitude in degrees (WGS84).
        lat: Latitude in degrees (WGS84).

    Returns:
        (easting, northing) in metres (OSGB36 / British National Grid).
    """
    easting, northing = _transformer_wgs84_to_osgb36.transform(lon, lat)
    return float(easting), float(northing)


def osgb36_to_wgs84(easting: float, northing: float) -> Tuple[float, float]:
    """
    Convert OSGB36 (easting, northing) to WGS84 (longitude, latitude).

    Args:
        easting: Easting in metres (OSGB36).
        northing: Northing in metres (OSGB36).

    Returns:
        (longitude, latitude) in degrees (WGS84).
    """
    lon, lat = _transformer_osgb36_to_wgs84.transform(easting, northing)
    return float(lon), float(lat)


def reproject_gdf(
    gdf: gpd.GeoDataFrame,
    target_crs: str,
) -> gpd.GeoDataFrame:
    """
    Reproject a GeoDataFrame to a target CRS if needed.

    If the GeoDataFrame already has the target CRS, it is returned unchanged.

    Args:
        gdf: Input GeoDataFrame.
        target_crs: Target CRS string (e.g. 'EPSG:27700').

    Returns:
        Reprojected GeoDataFrame.
    """
    if gdf.crs is None:
        raise ValueError("Input GeoDataFrame has no CRS set.")

    if str(gdf.crs) == str(target_crs):
        return gdf

    return gdf.to_crs(target_crs)
