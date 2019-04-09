import json
import argparse
import numpy as np


def default(o):  # resolve numpy type problem
    if isinstance(o, np.int64):
        return int(o)
    # raise TypeError


def write_to_json_file(path, file_name, data):  # write to json file function
    """
    Saves data given to a JSON file with a specified name and path,
    :param path: a path where the JSON file should be stored
    :param file_name: a file name for the JSON file
    :param data: data to store in the JSON file
    """
    file_path_name_wext = './' + path + './' + file_name + '.json'
    with open(file_path_name_wext, 'w') as fp:
        json.dump(data, fp, indent=2, default=default)


def parse_args():
    # TODO Write more elaborate help message
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="Config file path", required=True)
    cli_args = parser.parse_args()
    return cli_args
