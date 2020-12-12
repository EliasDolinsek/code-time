import json
import os
import tempfile
import unittest
from datetime import date

from src.data_sources.data_backend import DataBackend, DATA_FILES_PATH_KEYWORD
from src.data_sources.errors import MonthDataFileNotFoundError


class DataBackendTest(unittest.TestCase):

    def setUp(self) -> None:
        temp_directory = tempfile.gettempdir()
        if not os.path.exists(temp_directory):
            os.mkdir(temp_directory)

        self.data_directory = os.path.join(tempfile.gettempdir(), "data/")
        if not os.path.exists(self.data_directory):
            os.mkdir(self.data_directory)

    def test_get_data_file_path_single_digit_month(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        test_date = date(2020, 1, 1)
        data_backend = DataBackend(paths)

        expected_result = os.path.join(self.data_directory, "01-2020.json")
        result = data_backend.get_data_file_path(test_date)

        self.assertEqual(expected_result, result)

    def test_get_data_file_path_double_digit_month(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        test_date = date(2020, 10, 1)
        data_backend = DataBackend(paths)

        expected_result = os.path.join(self.data_directory, "10-2020.json")
        result = data_backend.get_data_file_path(test_date)

        self.assertEqual(expected_result, result)

    def test_read_month_data_file_not_available(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: "/this/path/does/not/exist"
        }

        data_backend = DataBackend(paths)
        self.assertRaises(MonthDataFileNotFoundError, data_backend.read_month_data, date(2020, 1, 1))

    def test_read_month_data_file_available(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        test_date = date(2020, 1, 1)
        mock_content = {
            1: {
                "PyCharm": 20000,
                "IntelliJ": 5000
            }
        }

        file_name = "01-2020.json"
        with open(os.path.join(self.data_directory, file_name), "w") as file:
            file.write(json.dumps(mock_content))

        data_backend = DataBackend(paths)
        result = data_backend.read_month_data(test_date)
        self.assertDictEqual(mock_content, result)
