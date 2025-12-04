# AirLock

AirLock (Air-quality Integrated Raster–Location Concordance) is a local web application for linking UK postcodes to 1 km NOx grid cells from the DEFRA pollution dataset. It performs a spatial join between ONS postcode coordinates and British National Grid (OSGB36) 1 km grid cells, producing an Excel file of all grid–postcode relationships for air-quality analysis.

## Features

- Upload ONS Postcode Directory and DEFRA NOx grid files  
- Automatic CRS handling (OSGB36 / BNG)  
- Point-in-polygon matching for postcodes and 1 km grid cells  
- Summary of matched and unmatched postcodes  
- Export full results to Excel  
- Generates a brief methods summary for documentation or publication

## Tech Stack

- Python 3  
- pandas, geopandas, shapely, pyproj  
- Streamlit for the local web interface  

## Purpose

AirLock is designed for researchers working on UK air-quality modelling, exposure assessment, and spatial epidemiology who need a reproducible way to relate postcode locations to 1 km pollution grid cells.

## Status

Project under active development. Roadmap in `features.md`.

