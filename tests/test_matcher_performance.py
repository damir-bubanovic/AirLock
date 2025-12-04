from shapely.geometry import Point, Polygon

from airlock.matcher import match_postcodes_to_grid
from airlock.models import GridCell, PostcodePoint


def test_matcher_basic_performance():
    """
    Sanity check that the matcher can handle 1000 points without error
    and that all are matched to the single grid cell.
    """

    # Single 1 km cell centered at (0, 0)
    cell_poly = Polygon([(-500, -500), (500, -500), (500, 500), (-500, 500)])
    gridcells = [GridCell(id="A1", center_x=0, center_y=0, geometry=cell_poly)]

    # 1000 postcode points inside the cell
    postcodes = [
        PostcodePoint(
            postcode=f"PC{i}",
            easting=float(i % 100),
            northing=float(i % 100),
            geometry=Point(float(i % 100), float(i % 100)),
        )
        for i in range(1000)
    ]

    result = match_postcodes_to_grid(postcodes, gridcells)

    assert len(result) == 1000
    assert result["matched_grid_id"].notna().all()
    assert set(result["matched_grid_id"].unique()) == {"A1"}
