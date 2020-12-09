from datetime import datetime
import json
import os
import unittest
import tempfile

from src.data_sources.data_backend import DataBackend


class DataBackendTest(unittest.TestCase):

    def setUp(self):
        data_directory = os.path.join(tempfile.gettempdir(), "data/")
        config_file = tempfile.mkstemp()[1]

        print("Data directory: ", data_directory)
        print("Config file: ", config_file)

        self.mock_paths = {
            "data_directory": data_directory,
            "config": config_file
        }

        self.data_backend = DataBackend(paths=self.mock_paths)

        self.mock_config = {
            "title_color": "#FFF",
            "total_time_color": "#FFF",
            "progress_background_color": "#FFF",
            "progress_foreground_color": "#FFF",
            "activity_title_color": "#FFF",
            "activity_time_color": "#FFF",
            "watermark_color": "#FFF",
            "image": tempfile.mkstemp()[1],
            "activities": [
                "PyCharm"
            ]
        }

        self.mock_month_data = {
            "activity": {
                str(datetime.today().day): [
                    {
                        "name": "PyCharm",
                        "start_time": 0,
                        "end_time": 0
                    }
                ]
            }
        }

        self.test_year = datetime.today().year
        self.test_month = datetime.today().month

    def test_read_month_data(self):
        self._write_mock_month_data()
        result = self.data_backend.read_month_data(year=self.test_year, month=self.test_month)
        self.assertDictEqual(self.mock_month_data, result)

    def test_write_month_data(self):
        self.data_backend.write_month_data(year=self.test_year, month=self.test_month, data=self.mock_month_data)

        file = os.path.join(self.mock_paths["data_directory"], f"{self.test_month}{self.test_year}.json")
        with open(file, "r") as file:
            content = dict(json.loads(file.read()))
            self.assertDictEqual(self.mock_month_data, content)

    def test_read_config(self):
        # Write mock config
        with open(self.mock_paths["config"], "w") as file:
            encoded_config = json.dumps(self.mock_config)
            file.write(encoded_config)

        # Read config
        result = self.data_backend.read_config()

        self.assertDictEqual(self.mock_config, result)

    def test_write_config(self):
        self.data_backend.write_config(self.mock_config)

        with open(self.mock_paths["config"], "r") as file:
            result = dict(json.loads(file.read()))
            self.assertDictEqual(self.mock_config, result)

    def test_get_days_with_data(self):
        self._write_mock_month_data()
        result = self.data_backend.get_days_with_data()
        expected_result = {
            2020: {
                12: [str(datetime.today().day)]
            }
        }

        self.assertDictEqual(expected_result, result)

    def _write_mock_month_data(self):
        if not os.path.exists(self.mock_paths["data_directory"]):
            os.mkdir(self.mock_paths["data_directory"])

        file = os.path.join(self.mock_paths["data_directory"], f"{self.test_month}{self.test_year}.json")
        with open(file, "w") as file:
            file.write(json.dumps(self.mock_month_data))
