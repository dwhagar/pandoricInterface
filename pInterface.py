#!/usr/bin/env python3

import argparse
import os
import json
import sys

# Name and version for Configuration checking.  A version mismatch could cause the system to attempt to update
# the configuration file and fail, resulting in a corrupted configuration.  Configuration files without the proper
# name will also refuse to load.
MYNAME = "Pandoric Interface for Discord"
VERSION = "v0.0 Conceptual Version"
MYHOME = os.path.dirname(os.path.abspath(__file__))


def parse_args():
    parser = argparse.ArgumentParser(description='Sample Python Script with Config Options')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose mode')
    parser.add_argument('-c', '--config', type=str, default='config.json',
                        help='Path to config file (default: config.json)')
    parser.add_argument('-d', '--dump', action='store_true', help='Dump the configuration to the console and exit')
    return parser.parse_args()


def load_config_file(file_path):
    default_config = {'name': MYNAME, 'version': VERSION}

    # Prepend MYPATH if file_path doesn't include a directory
    if not os.path.dirname(file_path):
        file_path = os.path.join(MYHOME, file_path)

    # Check if the directory is readable and writable
    directory = os.path.dirname(file_path) or '.'
    if not os.access(directory, os.R_OK | os.W_OK):
        sys.exit(f'Error: The directory "{directory}" cannot be read from or written to. Please check your permissions.')

    result = default_config  # Default to using the default configuration

    # Check if the file exists and is readable before trying to open
    if os.path.exists(file_path) and os.access(file_path, os.R_OK):
        try:
            with open(file_path, 'r') as f:
                config_data = json.load(f)
                # Validate the required 'name' in the config
                if config_data.get('name') == MYNAME:
                    result = config_data  # Valid configuration loaded from file
                else:
                    sys.exit(f'Error: The configuration file "{file_path}" is invalid. The "name" variable must match "{MYNAME}".')
        except json.JSONDecodeError:
            sys.exit(f'Error: The file "{file_path}" is not a valid JSON file. Please specify a valid JSON file.')

    # If the file does not exist or isn't readable, create it with the default configuration
    else:
        try:
            with open(file_path, 'w') as f:
                json.dump(default_config, f, indent=4)
        except Exception as e:
            sys.exit(f'Error creating the configuration file "{file_path}": {e}')

    return result  # Return the valid bot configuration


def save_config_file(filename):
    """
    Saves the given configuration dictionary to the specified filename.

    Args:
    filename (str): The name of the file where the configuration will be saved.
    """
    try:
        with open(filename, 'w') as f:
            json.dump(config, f, indent=4)
        if args.verbose:
            print(f"Configuration saved successfully to {filename}")
    except Exception as e:
        print(f"Error saving configuration to {filename}: {e}")


def main():
    if args.dump:
        print(json.dumps(config, indent=4))
        sys.exit(0)  # Exit after dumping the config

    if args.verbose:
        print('Verbose mode enabled')
        print('Using configuration file:', args.config)

    # Main script logic goes here if not in dump mode


if __name__ == "__main__":
    args = parse_args()
    config = load_config_file(args.config)
    main()
