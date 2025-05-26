#!/usr/bin/env python3
"""
Grid generator for uEMEP/NORTRIP

This program generates grid files for the uEMEP and NORTRIP models based on a json
configuration file.

Example usage:
    python src/grid-generator.py --config config.json
"""

import argparse
import json
import sys
import numpy as np
import utils.mod_generator as generator
from utils.mod_json import generate_empty_config


def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(
        description="Grid generator for uEMEP/NORTRIP",
        epilog="Example usage: python src/grid-generator.py --config config.json",
    )

    # Add arguments to the parser
    parser.add_argument(
        "--config", type=str, help="Path to the json configuration file"
    )
    parser.add_argument(
        "--generate-config", type=str, help="Generate an empty json configuration file"
    )

    # Print help message if no arguments are provided
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Parse the arguments
    args = parser.parse_args()

    # Handle inputs
    if args.generate_config:
        generate_empty_config()

    if args.config:
        with open(args.config, "r") as config_file:
            config = json.load(config_file)["config"]

        # Generate gridded country masks
        generator.make_gridded_country_masks(config)


if __name__ == "__main__":
    main()
