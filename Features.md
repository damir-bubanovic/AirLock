# AirLock – Project Roadmap

AirLock (Air-quality Integrated Raster–Location Concordance) is a local web tool for linking UK postcodes to 1 km NOx grid cells (OSGB36 / British National Grid), producing an Excel file of grid–postcode relationships plus a brief methods summary.

This roadmap is split into **Completed** and **To-Do** chapters to track progress.

---

## ✅ Completed Chapters

_None yet – project in initial setup phase._

---

## 📌 To-Do Chapters

### Chapter 1 — Project Setup & Architecture

- Choose tech stack:
  - Python 3.x, pandas, geopandas, pyproj, shapely
  - Streamlit (or similar) for local web UI
- Project structure:
  - `airlock/` (core package)
  - `app/` or `app.py` (web entry point)
  - `data/`, `output/`, `notebooks/`, `docs/`
- Add `requirements.txt` / `pyproject.toml`
- Basic logging and configuration pattern

---

### Chapter 2 — Data Sources & Schema Exploration

- Download and inspect:
  - DEFRA NOx 1 km grid data (BNG coordinates)
  - ONS Postcode Directory (ONSPD) with coordinates
- Explore schemas:
  - Identify postcode, easting/northing, status flags
  - Identify grid cell X/Y, GridCode, year, pollutant fields
- Document assumptions and required fields

---

### Chapter 3 — Coordinate Systems & Geospatial Foundations

- Confirm CRS for:
  - NOx grid (OSGB36 / BNG)
  - ONS postcodes (BNG or WGS84, depending on source)
- Implement coordinate handling:
  - Reprojection if needed (e.g. WGS84 → OSGB36)
  - Utility functions for CRS transforms
- Unit tests for sample coordinate conversions

---

### Chapter 4 — Grid Definition & Spatial Model

- Represent 1 km grid cells as polygons:
  - Derive cell boundaries from centre X/Y and 1 km resolution
- Define core models:
  - `GridCell` (id, centre_x, centre_y, polygon)
  - `PostcodePoint` (postcode, easting, northing, status)
- Optional: generate a unique stable grid ID

---

### Chapter 5 — Postcode–Grid Matching Engine

- Implement core spatial join:
  - Assign each postcode to the containing grid cell polygon
  - Handle postcodes falling outside any cell (if any)
- Decide strategy:
  - Pure spatial join (point-in-polygon) OR
  - Cell index via integer division of coordinates
- Create core function:
  - `match_postcodes_to_grid(postcodes, grid_cells) -> DataFrame`

---

### Chapter 6 — Data Validation & Edge Cases

- Handle:
  - Terminated or non-geographic postcodes
  - Missing or invalid coordinates
  - Duplicated postcodes or aliases
- Build validation checks:
  - Summary of unmatched postcodes
  - Summary of empty grid cells
- Generate small QA reports (counts, sanity checks)

---

### Chapter 7 — Performance & Large Dataset Handling

- Optimise for full UK dataset:
  - Efficient spatial indexing (R-tree, GeoPandas sjoin)
  - Chunked reading / processing if needed
- Benchmark on realistic input sizes
- Provide progress logging for long runs

---

### Chapter 8 — Web UI: Core Workflow

- Basic Streamlit (or similar) app:
  - File upload inputs for NOx grid and ONSPD files
  - Options: year, pollutant, filters (e.g., active postcodes only)
  - “Run mapping” button
- Show:
  - High-level summary (rows, matched %, unmatched count)
  - Preview table of grid–postcode pairs

---

### Chapter 9 — Web UI: UX Enhancements

- Progress indicators and status messages
- Error handling and friendly messages for:
  - Wrong file format
  - Missing columns
- Simple configuration panel:
  - Output options (Excel vs CSV, which fields to keep)
  - Optional subset by region (e.g., England only, London only)

---

### Chapter 10 — Export & Method Summary Generator

- Implement export:
  - Excel workbook with:
    - Main “grid_postcodes” sheet
    - Optional “summary” sheet (counts per grid cell)
  - CSV export as alternative
- Auto-generate brief methods description:
  - Data sources, CRS, join method, filters
- Provide download buttons in the UI

---

### Chapter 11 — Optional Mapping & Visualisation

- Simple map preview (optional/future):
  - Show sample grid cells and postcode points
  - Zoomable map for QA (e.g., around London)
- Simple statistics dashboard:
  - Distribution of postcodes per grid cell
  - Regional summaries

---

### Chapter 12 — Testing, Documentation & Packaging

- Automated tests:
  - Unit tests for CRS, grid creation, matching logic
  - Small integration test with toy dataset
- Documentation:
  - `README.md` with install/run instructions
  - `METHODS.md` or docs section describing methodology
- Packaging:
  - Basic instructions for running locally on Linux Mint
  - Optional: simple script/entry point (`airlock run`)

---
