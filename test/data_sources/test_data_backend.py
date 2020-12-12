import json
import os
import tempfile
import unittest
from datetime import date
from os import listdir

from src.data_sources.data_backend import DataBackend, DATA_FILES_PATH_KEYWORD, CONFIG_FILE_PATH_KEYWORD
from src.data_sources.errors import MonthDataFileNotFoundError, EmptyMonthDataError, ConfigFileNotFoundError, \
    EmptyConfigError, InvalidMonthDataFileNameError


class DataBackendTest(unittest.TestCase):

    def setUp(self) -> None:
        temp_directory = tempfile.gettempdir()
        if not os.path.exists(temp_directory):
            os.mkdir(temp_directory)

        self.data_directory = os.path.join(tempfile.gettempdir(), "data/")
        if not os.path.exists(self.data_directory):
            os.mkdir(self.data_directory)

    def tearDown(self) -> None:
        for file in listdir(self.data_directory):
            os.remove(os.path.join(self.data_directory, file))
        os.removedirs(self.data_directory)

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
        mock_data = {
            1: {
                "PyCharm": 20000,
                "IntelliJ": 5000
            }
        }

        file_name = "01-2020.json"
        with open(os.path.join(self.data_directory, file_name), "w") as file:
            file.write(json.dumps(mock_data))

        data_backend = DataBackend(paths)
        result = data_backend.read_month_data(test_date)
        self.assertDictEqual(mock_data, result)

    def test_write_month_data_empty_data(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        test_date = date(2020, 1, 1)
        data_backend = DataBackend(paths)
        self.assertRaises(EmptyMonthDataError, data_backend.write_month_data, {}, test_date)

    def test_write_month_data_non_empty_data(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        test_date = date(2002, 1, 1)
        data_backend = DataBackend(paths)
        mock_data = {
            1: {
                "PyCharm": 20000,
                "IntelliJ": 5000
            }
        }

        data_backend.write_month_data(mock_data, test_date)

        with open(os.path.join(self.data_directory, "01-2020.json")) as file:
            self.assertEqual(json.dumps(mock_data), file.read())

    def test_read_config_file_available(self):
        temp_config = tempfile.mkstemp()[1]
        paths = {
            CONFIG_FILE_PATH_KEYWORD: temp_config
        }

        mock_config = {
            "enabled": True
        }

        with open(temp_config, "w") as file:
            file.write(json.dumps(mock_config))

        data_backend = DataBackend(paths)
        result = data_backend.read_config()

        self.assertDictEqual(mock_config, result)
        os.remove(temp_config)

    def test_read_config_file_not_available(self):
        paths = {
            CONFIG_FILE_PATH_KEYWORD: "/this/file/does/no/exist"
        }

        data_backend = DataBackend(paths)
        self.assertRaises(ConfigFileNotFoundError, data_backend.read_config)

    def test_write_config_file_empty_config(self):
        data_backend = DataBackend({})
        self.assertRaises(EmptyConfigError, data_backend.write_config, {})

    def test_write_config_file_not_empty(self):
        temp_config = tempfile.mkstemp()[1]
        paths = {
            CONFIG_FILE_PATH_KEYWORD: temp_config
        }

        data_backend = DataBackend(paths)
        mock_config = {
            "enabled": True
        }

        data_backend.write_config(mock_config)
        with open(temp_config, "r") as file:
            self.assertDictEqual(mock_config, json.loads(file.read()))

        os.remove(temp_config)

    def test_parse_year_from_data_file_name_valid_name(self):
        name = "12-2020.json"
        data_backend = DataBackend({})
        self.assertEquals(2020, data_backend.parse_year_from_data_file_name(name))

    def test_parse_year_from_data_file_name_valid_name_invalid_name(self):
        name = "122020.json"
        data_backend = DataBackend({})
        self.assertRaises(InvalidMonthDataFileNameError, data_backend.parse_year_from_data_file_name, name)

    def test_get_existing_years(self):
        file_names = ["12-2020.json", "01-2021.json", "09-2019.json"]
        for f_name in file_names:
            with open(os.path.join(self.data_directory, f_name), "w") as _:
                pass

        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        data_backend = DataBackend(paths)
        result = data_backend.get_existing_years()
        self.assertEqual([2019, 2020, 2021], result)

    def test_get_existing_years_no_years(self):
        paths = {
            DATA_FILES_PATH_KEYWORD: self.data_directory
        }

        data_backend = DataBackend(paths)
        result = data_backend.get_existing_years()
        self.assertEqual([], result)
