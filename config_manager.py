import json


class ConfigManager:
    def __init__(self, config_file: str):
        with open(config_file, "r") as f:
            self.config = json.load(f)

    def get(self, key: str, default=None):
        return self.config.get(key, default)
