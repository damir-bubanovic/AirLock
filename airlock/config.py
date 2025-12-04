# AirLock configuration and schema constants

# Coordinate Reference Systems
CRS_OSGB36 = "EPSG:27700"  # British National Grid
CRS_WGS84 = "EPSG:4326"    # Latitude/Longitude

# Grid configuration
GRID_CELL_SIZE_M = 1000  # 1 km × 1 km grid cells

# Expected columns for NOx grid dataset (DEFRA)
NOX_REQUIRED_COLUMNS = [
    "X",  # Easting of grid cell centre
    "Y",  # Northing of grid cell centre
]

# Expected optional pollutant columns (may vary by dataset)
NOX_OPTIONAL_COLUMNS = [
    "NOx",
    "nox_annual_mean",
    "nox",
]

# Expected columns for ONS Postcode Directory
POSTCODE_REQUIRED_COLUMNS = [
    "pcd",        # Postcode
    "oseast1m",   # Easting (OSGB36)
    "osnrth1m",   # Northing (OSGB36)
]

POSTCODE_OPTIONAL_COLUMNS = [
    "pcd2",       # Normalised postcode
    "pcd3",
    "lat",
    "long",
    "dointr",
    "doterm",
]
