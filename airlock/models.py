from dataclasses import dataclass
from shapely.geometry import Polygon, Point


@dataclass
class GridCell:
    """
    Internal representation of a 1 km grid cell.
    """
    id: str
    center_x: float
    center_y: float
    geometry: Polygon


@dataclass
class PostcodePoint:
    """
    Internal representation of a postcode location.
    """
    postcode: str
    easting: float
    northing: float
    geometry: Point
