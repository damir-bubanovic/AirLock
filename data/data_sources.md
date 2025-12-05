# Data Sources

AirLock links UK postcodes to 1 km NOx grid cells. It relies on two main datasets:

1. DEFRA NOx 1 km grid data  
2. ONS Postcode Directory (ONSPD)

Both datasets must use **British National Grid (OSGB36 / EPSG:27700)** with coordinates in metres.

---

## 1. DEFRA NOx 1 km Grid Data

- **Source:** UK AIR (DEFRA) – Pollution Climate Mapping (PCM) data  
- **Link:** https://uk-air.defra.gov.uk/data/pcm-data#nox  
- **Coordinate system:** British National Grid (OSGB36), 1 km × 1 km cells  
- **Geometry representation:**  
  - Grid cell centres given as Eastings (`X`) and Northings (`Y`) in metres  
  - Each row represents one 1 km grid cell

### 1.1 Expected key fields (NOx grid)

These names may vary slightly depending on the file/year; AirLock assumes the following columns exist (or are mapped to them):

- `X` – easting (metres), centre of 1 km cell  
- `Y` – northing (metres), centre of 1 km cell  

Optional but commonly present:

- `GridCode` – grid identifier (not an official OS grid reference)  
- Pollutant fields (example for NOx):  
  - `NOx` or `NOx_YYYY` (annual mean concentrations)  
  - Additional columns may include year, sector breakdowns, etc.

AirLock uses `X` and `Y` to construct 1 km grid cell polygons in OSGB36.  
Any extra columns are preserved in intermediate data but are not required for postcode matching.

---

## 2. ONS Postcode Directory (ONSPD)

- **Source:** Office for National Statistics – ONS Postcode Directory  
- **Typical format:** CSV (inside a ZIP)  
- **Coverage:** All current and some terminated UK postcodes  
- **Coordinate system:**  
  - Eastings (`oseast1m`) and Northings (`osnrth1m`) in OSGB36 (1 m resolution)  
  - Latitude/longitude in WGS84 are also often included, but not used by AirLock

### 2.1 Typical ONSPD fields

Field names may vary slightly by release; typical ONSPD structure includes:

- `pcd` – full postcode (often without space)  
- `pcd2` – formatted postcode (with standard spacing)  
- `pcd3` – truncated version (for grouping)  
- `oseast1m` – easting (metres, OSGB36)  
- `osnrth1m` – northing (metres, OSGB36)  
- `lat` – latitude (WGS84)  
- `long` – longitude (WGS84)  
- `doterm` – termination date (if postcode is no longer active)  
- Various geographic and administrative codes (LSOA, MSOA, LAD, NHS, region, etc.)

AirLock primarily uses:

- Postcode ID: `pcd`  
- Easting: `oseast1m`  
- Northing: `osnrth1m`  
- Optional termination information: `doterm` (for filtering)

Other fields may be present but are ignored by the core matching engine.

---

## 3. Required Columns Summary (AirLock Internal Schema Requirements)

AirLock enforces a minimal schema to ensure it can process data robustly.  
Internally these requirements are expressed as:

```python
NOX_REQUIRED_COLUMNS = ["X", "Y"]
POSTCODE_REQUIRED_COLUMNS = ["pcd", "oseast1m", "osnrth1m"]
