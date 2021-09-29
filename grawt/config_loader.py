import os
import sys
import yaml


def load_config(config_path: str):
    if not os.path.exists(config_path):
        open(config_path, "a").close()
        print(f"Config file created at: {config_path}")
        print("Please fill out the config and restart the application")
        sys.exit()

    with open(config_path, "r") as file_io:
        return yaml.safe_load(file_io)
