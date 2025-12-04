from shapely.geometry import Point, Polygon

from airlock.matcher import match_postcodes_to_grid
from airlock.models import GridCell, PostcodePoint


def test_match_postcodes_to_grid():
    # Simple 1 km grid cell centered at (0, 0)
    cell = GridCell(
        id="A1",
        center_x=0,
        center_y=0,
        geometry=Polygon([(-500, -500), (500, -500), (500, 500), (-500, 500)]),
    )

    # Postcode inside the cell
    p = PostcodePoint(
        postcode="TEST1",
        easting=0,
        northing=0,
        geometry=Point(0, 0),
    )

    result = match_postcodes_to_grid([p], [cell])

    assert len(result) == 1
    row = result.iloc[0]

    assert row["postcode"] == "TEST1"
    assert row["matched_grid_id"] == "A1"
    assert row.geometry.x == 0
    assert row.geometry.y == 0
