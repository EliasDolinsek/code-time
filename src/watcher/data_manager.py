import json as json_parser
import os
from os import listdir

CONFIG_FILE = "config.json"
DATA_DIRECTORY = "data/"


def get_data_folder_path():
    return os.path.join(os.path.dirname(__file__), DATA_DIRECTORY)


def get_file_path_for_data_file(month_str: str, year_str: str):
    return os.path.join(get_data_folder_path(), f"{month_str}_{year_str}.json")


def read_month_data(month_str: str, year_str: str) -> dict:
    file_path = get_file_path_for_data_file(month_str, year_str)
    if os.path.isfile(file_path):
        with open(file_path, "r") as file:
            return json_parser.load(file)
    else:
        return {}


def write_month_data(mont_str: str, year_str: str, data: dict):
    file_path = get_file_path_for_data_file(mont_str, year_str)
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    with open(file_path, "w") as file:
        file.write(json_parser.dumps(data))


def read_config() -> dict:
    with open(CONFIG_FILE, "r") as file:
        return json_parser.load(file)


def write_config(config: dict):
    with open(CONFIG_FILE, "w") as file:
        file.write(json_parser.dumps(config))


def get_year_of_data_file_name(name: str):
    month_removed = name[name.index("_") + 1:]
    return month_removed[:month_removed.index(".")]


def get_available_years() -> list:
    files = listdir(get_data_folder_path())
    years = []
    for file in files:
        year = get_year_of_data_file_name(file)
        if year not in years:
            years.append(year)

    years.sort()
    return years


def get_available_months(year: int) -> list:
    files = listdir(get_data_folder_path())
    months = []
    for file in files:
        if get_year_of_data_file_name(file) == year:
            months.append(int(file[:file.index("_")]))

    months.sort()
    return months


def read_config() -> dict:
    with open(CONFIG_FILE) as file:
        return json_parser.loads(file.read())
