import json as json_parser
import os

CONFIG_FILE = "config.json"
DATA_DIRECTORY = "data/"


def get_file_path_for_data_file(month_str: str, year_str: str):
    return os.path.join(os.path.dirname(__file__), DATA_DIRECTORY, f"{month_str}_{year_str}.json")


def read_month_data(month_str: str, year_str: str) -> dict:
    file_path = get_file_path_for_data_file(month_str, year_str)
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return json_parser.load(file)
    else:
        return {}


def write_month_data(mont_str: str, year_str: str, data: dict):
    file_path = get_file_path_for_data_file(mont_str, year_str)
    if not os.path.exists(file_path):
        os.mkdir(os.path.dirname(file_path))
    with open(file_path, "w") as file:
        file.write(json_parser.dumps(data))


def read_config() -> dict:
    with open(CONFIG_FILE, "r") as file:
        return json_parser.load(file)


def write_config(config: dict):
    with open(CONFIG_FILE, "w") as file:
        file.write(json_parser.dumps(config))
