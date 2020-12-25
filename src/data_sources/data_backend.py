import datetime
import json
import os
from os import listdir
from pathlib import Path

from src.data_sources.errors import MonthDataFileNotFoundError, EmptyMonthDataError, ConfigFileNotFoundError, \
    EmptyConfigError, InvalidMonthDataFileNameError

DATA_FILES_PATH_KEYWORD = "data_directory"
CONFIG_FILE_PATH_KEYWORD = "config"
RES_DIRECTORY_KEYWORD = "res_directory"


class DataBackend:
    def __init__(self, paths: dict):
        self.paths = paths

    def get_data_file_path(self, date: datetime.date) -> Path:
        month_str = str(date.month)
        if date.month < 10:
            month_str = f"0{month_str}"

        print(self.paths[DATA_FILES_PATH_KEYWORD].joinpath(Path(f"{month_str}-{date.year}.json")))
        return self.paths[DATA_FILES_PATH_KEYWORD].joinpath(Path(f"{month_str}-{date.year}.json"))

    def read_month_data(self, date: datetime.date) -> dict:
        """
        example format of month data which is being returned:
        {
            1: {
                "PyCharm": 1000,
                "IntelliJ": 2000
            }
        }
        :param date: date of desired month
        :return: dict of month data
        """
        file_path = self.get_data_file_path(date)
        if file_path.exists():
            with open(file_path, "r") as file:
                content = json.loads(file.read())
                formatted_month_data = {}

                for k, v in content.items():
                    formatted_month_data[int(k)] = v

                return formatted_month_data
        else:
            return {}

    def write_month_data(self, data: dict, date: datetime):
        if not bool(data):
            raise EmptyMonthDataError()

        if not os.path.exists(self.paths[DATA_FILES_PATH_KEYWORD]):
            os.mkdir(self.paths[DATA_FILES_PATH_KEYWORD])

        file_path = self.get_data_file_path(date)
        with open(file_path, "w") as file:
            file.write(json.dumps(data))

    def read_config(self):
        try:
            with open(self.paths[CONFIG_FILE_PATH_KEYWORD], "r") as file:
                return json.load(file)
        except FileNotFoundError:
            raise ConfigFileNotFoundError

    def write_config(self, config):
        if type(config) is not dict or not bool(config):
            raise EmptyConfigError()

        with open(self.paths[CONFIG_FILE_PATH_KEYWORD], "w") as file:
            file.write(json.dumps(config))

    def get_days_with_data(self):
        """
        return format example:
        {
            2020: {
                1: [1,2,3]
            }
        }
        :return: list of days with tracking data
        """
        result = {}
        years = self.get_existing_years()

        for year in years:
            months = self.get_existing_months(datetime.date(year, 1, 1))
            year_data = {}

            for month in months:
                month_date = datetime.date(year, month, 1)
                year_data[month] = list(self.read_month_data(month_date).keys())

            result[year] = year_data

        return result

    def get_existing_years(self) -> list:
        if not os.path.exists(self.paths[DATA_FILES_PATH_KEYWORD]):
            return []

        files = listdir(self.paths[DATA_FILES_PATH_KEYWORD])
        years = []

        for file in files:
            year = self.parse_year_from_data_file_name(file)
            if year not in years:
                years.append(year)

        years.sort()
        return years

    def get_existing_months(self, year: datetime) -> list:
        months = []

        files = listdir(self.paths[DATA_FILES_PATH_KEYWORD])
        for file in files:
            if self.parse_year_from_data_file_name(file) == year.year:
                months.append(int(file[:file.index("-")]))

        months.sort()
        return months

    def get_res_file_path(self, relative_path):
        return self.paths["res_directory"].joinpath(relative_path)

    def does_config_file_exist(self):
        return Path(self.paths[CONFIG_FILE_PATH_KEYWORD]).resolve().exists()

    @staticmethod
    def parse_year_from_data_file_name(name) -> int:
        """File name example: 12-2020.json"""
        try:
            return int(name[name.index("-") + 1:name.index(".json")])
        except Exception:
            raise InvalidMonthDataFileNameError()
