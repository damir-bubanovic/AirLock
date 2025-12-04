# Data Sources

AirLock links UK postcodes to 1 km NOx grid cells. It relies on two main datasets:

---

## 1. DEFRA NOx 1 km Grid Data

- **Source:** UK AIR (DEFRA) – Pollution Climate Mapping (PCM) data  
- **Link:** https://uk-air.defra.gov.uk/data/pcm-data#nox  
- **Coordinate system:** British National Grid (OSGB36), 1 km × 1 km cells  
- **Geometry representation:**  
  - Grid cell centres given as Eastings (X) and Northings (Y) in metres  
  - Each row represents one 1 km grid cell

### Expected key fields (NOx grid)

These names may vary slightly depending on the file/year; AirLock will allow mapping or configuration if needed:

- `X` – easting (metres), centre of 1 km cell  
- `Y` – northing (metres), centre of 1 km cell  
- `GridCode` – grid identifier (not an official OS grid reference)  
- Pollutant fields (example for NOx):  
  - `NOx` or `nox_annual_mean` (main value of interest)  
  - Additional columns may include year, source contributions, etc.

The application uses `X` and `Y` to construct 1 km grid cell polygons in OSGB36.

---

## 2. ONS Postcode Directory (ONSPD)

- **Source:** Office for National Statistics – ONS Postcode Directory  
- **Typical format:** CSV (inside a ZIP)  
- **Coverage:** All current and some terminated UK postcodes  
- **Coordinate system:**  
  - Eastings (`oseast1m`) and Northings (`osnrth1m`) in OSGB36 (1 m resolution)  
  - Latitude/longitude in WGS84 are also often included

### Expected key fields (ONSPD)

Field names may vary slightly by release; typical ONSPD structure includes:

- `pcd` – full postcode (often without space)  
- `pcd2` – formatted postcode (with standard spacing)  
- `pcd3` – truncated version (sometimes used for grouping)  
- `oseast1m` – easting (metres, OSGB36)  
- `osnrth1m` – northing (metres, OSGB36)  
- `lat` – latitude (WGS84, optional for our purposes)  
- `long` – longitude (WGS84, optional for our purposes)  
- `oseast1m` / `osnrth1m` may be blank for some special or non-geographic codes

Additional fields (not strictly required for AirLock but may be useful filters):

- `dointr` / `doterm` – date of introduction / termination  
- `usertype` or similar – indicator of large user / small user  
- Region, local authority, health area codes, etc.

AirLock primarily uses:

- Postcode ID (`pcd` or `pcd2`)  
- Easting and northing (`oseast1m`, `osnrth1m`)  
- Optional status or termination flags for filtering.

---

## File Location in the Project

During development, datasets are expected to be placed (manually) in:

- `data/ons/` – ONSPD files (raw CSV or unzipped contents)  
- `data/defra_nox/` – DEFRA NOx grid files

AirLock will not commit these datasets to the repository; they are large and often subject to licensing terms. The application will instead allow the user to select or upload the relevant files at runtime.
