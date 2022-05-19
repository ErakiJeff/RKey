import json

data = json.load("config.json")

def get_data(config_field):
    if config_field in data:
        return data[config_field]
    else:
        raise KeyError