import json

data = None
with open("config.json") as reader:
    data = json.load(reader)


def get_data(config_field):
    if config_field in data:
        return data[config_field]
    else:
        raise KeyError
