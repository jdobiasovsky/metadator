import json


def load_config(path):
    '''Read configuration file and return dictionary with configuration.'''
    with open(path) as configfile:
        configuration_data = json.loads(configfile.read())
        return configuration_data
