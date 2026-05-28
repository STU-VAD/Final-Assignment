# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## TOP RULES
HAVE TO USE SUPERPOWER
THINK ABOUT REUSE
ASKING BEFORE DOING
superpower's docs should directly put in docs/, not /superpower/plans or /specs.
WHEN YOU WRITE COMMIT NOTES, DONT WRITE CO-AUTHOR-BY

## Project Overview

This is a data visualization course project analyzing global climate data (CO2 concentrations and temperature anomalies) from 1880-2025. The project creates an interactive 3D visualization showing the relationship between CO2 levels, latitude bands, and temperature changes.

## Project Structure

```
Finel-Assignment/
├── data/                        # Data files
│   ├── co2_annmean_gl.csv      # NOAA CO2 annual mean data (1979-2025)
│   └── ZonAnn.Ts+dSST.csv     # NASA GISTEMP temperature anomalies by latitude (1880-2025)
├── docs/                        # Design documentation
│   ├── 2026-05-27-co2-latitude-temperature-3d-viz-design.md
│   └── 2026-05-27-co2-latitude-temperature-3d-viz-plan.md
├── src/                         # Source code
│   ├── analyse/                # Analysis pages
│   │   └── analysis.html
│   └── observable/             # Observable visualizations
│       ├── index.html          # Main 3D visualization
│       └── prototype.html      # Prototype visualization
├── .gitignore
└── README.md
```

## Data Sources

- **CO2 Data**: NOAA Global Monitoring Laboratory (GML) - annual mean global CO2 mole fraction in ppm
- **Temperature Data**: NASA GISTEMP v4 - temperature anomalies relative to 1951-1980 baseline by latitude bands

## Key Technical Details

- **Visualization Tool**: Observable Plot / D3.js for interactive visualizations
- **Data Format**: CSV files with headers
- **Python Environment**: Uses uv for dependency management (pyproject.toml)
- **Deployment**: GitHub Pages for public access

## Development Commands

### Local Preview
```bash
# For observable visualizations
cd src/observable
# Open index.html in browser directly

# For Python-based builds (if applicable)
python -m uv run python build.py
```

### Data Processing
```bash
# Data files are in CSV format
# CO2 data: year, mean, uncertainty
# Temperature data: year, global, hemisphere, latitude band anomalies
```

## Important Notes

- **Data Timeframes**: CO2 data starts 1979, temperature data starts 1880
- **Latitude Bands**: 8 bands from Arctic (64N-90N) to Antarctic (90S-64S)
- **Visualization Focus**: 3D scatter plot with CO2 (X), Latitude (Y), Temperature anomaly (Z)
- **Language**: Documentation in Chinese, code comments in English
- **Submission Deadline**: June 7, 2026 @ 23:59 GMT+8
