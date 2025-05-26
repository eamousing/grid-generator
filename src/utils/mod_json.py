import json


def generate_empty_config():
    """
    Generates an empty configuration file
    """
    config = {
        "config_name": "",
        "shapefile": "",
        "lon_origin": 0,
        "lon_spacing": 0,
        "lon_points": 0,
        "lat_origin": 0,
        "lat_spacing": 0,
        "lat_points": 0,
        "country_code_type": "ISO3",
        "country_codes": [],
    }

    with open("config.json", "w") as config_file:
        json.dump({"config": config}, config_file, indent=4)
