import geopandas as gpd
import xarray as xr
import numpy as np
import shapely
import sys
from tqdm import tqdm


def make_gridded_country_masks(config):
    """
    Create country masks for the configured grid
    """

    # Store configuration variables
    lon_origin = config["lon_origin"]
    lon_spacing = config["lon_spacing"]
    lon_points = int(config["lon_points"])
    lat_origin = config["lat_origin"]
    lat_spacing = config["lat_spacing"]
    lat_points = int(config["lat_points"])

    # Open shapefile
    countries = gpd.read_file(config["shapefile"])

    # Get countries list
    if config["country_code_type"] != "ISO3":
        print("Currently only ISO3 country names are supported")
        sys.exit(1)

    country_codes = config["country_codes"]
    selected_countries = countries[countries["ISO3_CODE"].isin(country_codes)]

    # Create the grid points
    lon = np.arange(lon_origin, lon_origin + lon_spacing * lon_points, lon_spacing)
    lat = np.arange(lat_origin, lat_origin + lat_spacing * lat_points, lat_spacing)

    # Create dataset
    ds = xr.Dataset(coords={"lon": lon, "lat": lat})

    # Add coordinate attributes
    ds["lon"].attrs.update(
        {"origin": lon_origin, "spacing": lon_spacing, "points": lon_points}
    )

    ds["lat"].attrs.update(
        {"origin": lat_origin, "spacing": lat_spacing, "points": lat_points}
    )

    # Initialize the combined mask
    combined_mask = np.zeros((lat_points, lon_points))

    # Loop countries and make the gridded masks
    for _, country in tqdm(
        selected_countries.iterrows(),
        total=selected_countries.shape[0],
        desc="Processing countries",
    ):
        mask = np.zeros((lat_points, lon_points))
        country_geom = country.geometry

        for i, lon_val in enumerate(lon):
            for j, lat_val in enumerate(lat):
                grid_cell = shapely.geometry.box(
                    lon_val, lat_val, lon_val + lon_spacing, lat_val + lat_spacing
                )
                intersection = country_geom.intersection(grid_cell)

                if not intersection.is_empty:
                    mask[j, i] = intersection.area / grid_cell.area
                    combined_mask[j, i] += mask[j, i]

        # Add mask to dataset
        iso_code = country["ISO3_CODE"]
        long_name = country["NAME_ENGL"]
        ds[iso_code] = (("lat", "lon"), mask)
        ds[iso_code].attrs["long_name"] = long_name

    # Validate combined mask values
    tolerance = 1.0e-9
    if not np.all(combined_mask <= 1 + tolerance):
        max_value = combined_mask.max()
        raise ValueError(
            f"Combined mask contains values outside the upper range [0, 1]. Max values: {max_value}"
        )

    # Cap values at 1 if below tolerance
    combined_mask[np.isclose(combined_mask, 1, atol=tolerance)] = 1

    # Add combined mask
    ds["ALL_COUNTRIES"] = (("lat", "lon"), combined_mask)
    ds["ALL_COUNTRIES"].attrs["description"] = "Combined mask of all included countries"

    # Add configuration name
    ds.attrs["config_name"] = config["config_name"]

    # Write to NetCDF4
    ds.to_netcdf("country_masks.nc")
