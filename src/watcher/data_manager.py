import json as json_parser

FILE = "applications.json"


class DataManager:

    def __init__(self, file_name: str):
        self.file_name = file_name

    def read_config(self) -> dict:
        with open(self.file_name, "r") as file:
            return json_parser.load(file)

    def write_config(self, config: dict):
        with open(self.file_name, "w") as file:
            file.write(json_parser.dumps(config))
