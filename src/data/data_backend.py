import json
import os

DATA_FILES_PATH_KEYWORD = "data_files"


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
        pass

    def write_config(self):
        pass
