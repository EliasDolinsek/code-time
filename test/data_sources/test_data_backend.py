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

        self.test_date = datetime.now()
        self.mock_month_data = {
            self.test_date.day: {
                "name": "PyCharm",
                "time": 1000
            }
        }

    def test_read_month_data(self):
        self._write_mock_month_data()
        result = self.data_backend.read_month_data(self.test_date)
        self.assertDictEqual(self.mock_month_data, result)

    def test_write_month_data(self):
        self.data_backend.write_month_data(data=self.mock_month_data, date=datetime(year=2020, month=1, day=1))

        file = os.path.join(self.mock_paths["data_directory"], f"{self.test_date.month}{self.test_date.year}.json")
        with open(file, "r") as file:
            content = dict(json.loads(file.read()))

            expected_result = {}
            for k, v in content.items():
                expected_result[k] = v

            self.assertDictEqual(expected_result, content)

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
            self.test_date.year: {
                self.test_date.month: [self.test_date.day]
            }
        }

        self.assertDictEqual(expected_result, result)

    def _write_mock_month_data(self):
        if not os.path.exists(self.mock_paths["data_directory"]):
            os.mkdir(self.mock_paths["data_directory"])

        month_name = str(self.test_date.month)
        if self.test_date.month < 10:
            month_name = f"0{month_name}"

        file = os.path.join(self.mock_paths["data_directory"], f"{month_name}{self.test_date.year}.json")
        with open(file, "w") as file:
            file.write(json.dumps(self.mock_month_data))
