import json
import os
from os import listdir

DATA_FILES_PATH_KEYWORD = "data_files"
CONFIG_FILE_PATH_KEYWORD = "config"


def _parse_year_from_data_file_name(name: str) -> int:
    return int(name[1:6])


class DataBackend:
    def __init__(self, paths: dict):
        self.paths = paths

    def read_month_data(self, year: int, month: int) -> dict:
        file_path = self._get_data_file_path(year, month)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                return json.load(file)
        else:
            return {}

    def write_month_data(self, year, month, data):
        if not os.path.exists(self.paths[DATA_FILES_PATH_KEYWORD]):
            os.mkdir(self.paths[DATA_FILES_PATH_KEYWORD])

        file_path = self._get_data_file_path(year, month)
        with open(file_path, "w") as file:
            file.write(json.dumps(data))

    def _get_data_file_path(self, year: int, month: int) -> str:
        return os.path.join(self.paths[DATA_FILES_PATH_KEYWORD], f"{month}{year}.json")

    def read_config(self):
        with open(self.paths[CONFIG_FILE_PATH_KEYWORD], "r") as file:
            return json.load(file)

    def write_config(self, config):
        with open(self.paths[CONFIG_FILE_PATH_KEYWORD], "w") as file:
            file.write(json.dumps(config))

    def get_days_with_data(self):
        pass

    def _get_available_years(self) -> list:
        files = listdir(self.paths[DATA_FILES_PATH_KEYWORD])
        years = []

        for file in files:
            year = _parse_year_from_data_file_name(file)
            if year not in years:
                years.append(year)

        years.sort()
        return years

    def _get_available_months(self, year: int) -> list:
        files = listdir(self.paths[DATA_FILES_PATH_KEYWORD])
        months = []

        for file in files:
            if _parse_year_from_data_file_name(file) == year:
                months.append(int(file[:2]))

        months.sort()
        return months
