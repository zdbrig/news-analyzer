import json


def read_config():
    """Reads the configuration from the config.json file and returns it."""
    with open("config.json", "r") as f:
        config = json.load(f)
        return config
