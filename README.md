# Grid Generator for uEMEP/NORTRIP

This repository contains a grid generator program for the uEMEP and NORTRIP models. It generates grid files based on a JSON configuration file and outputs NetCDF4 files.

## Prerequisites

Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/grid-generator.git
    cd grid-generator
    ```

2. Install the required packages using pip:

    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

## Usage

### Generating a grid

To generate grid files, run the following command:

```bash
python src/grid-generator.py --config config.json
```

### Configuration file

An empty configuration file can be generated as:

```bash
python src/grid-generator.py --generate-config config.json
```

The configuration file should include the following fields:

```json
{
    "config_name": "Example config",
    "shapefile": "path/to/shapefile.shp",
    "lon_origin": -34.9,
    "lon_spacing": 0.1,
    "lon_points": 1000,
    "lat_origin": 20.0,
    "lat_spacing": 0.05,
    "lat_points": 1100,
    "country_code_type": "ISO3",
    "country_codes": ["AND", "ALB", "ARM", ...]
}
```

- **config_name**: Name identifier for the configuration
- **shapefile**: Path to the shapefile containing country geometries
- **lon_origin** and **lat_origin**: Starting point of the grid
- **lon_spacing** and **lat_spacing**: Spacing intervals for grid points
- **lon_points** and **lat_points**: Number of points in longitude and latitude directions
- **country_code_type**: Type of country codes used (*currently supports "ISO3"*)
- **country_code*s*: List of country codes to include in the grid

## Acknowledgments

This tool is developed for use with the [uEMEP](https://github.com/metno/uEMEP) and [NORTRIP](https://github.com/metno/NORTRIP) models.


