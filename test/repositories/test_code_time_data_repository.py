import unittest
from datetime import datetime
from unittest.mock import MagicMock

from src.data_sources.data_backend import DataBackend
from src.repositories.code_time_data_repository import CodeTimeDataRepository


class CodeTimeDataRepositoryTest(unittest.TestCase):

    def test_get_month_data(self):
        mock_result = {
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

        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=mock_result)

        data_model = CodeTimeDataRepository(data_backend)
        self.assertDictEqual(mock_result, data_model.get_month_data())

    def test_add_month_data(self):
        day = datetime.today().day
        month = datetime.today().month
        year = datetime.today().year

        mock_read_month_data_result = {
            "activity": {
                str(day): [
                    {
                        "name": "PyCharm",
                        "start_time": 0,
                        "end_time": 0
                    }
                ]
            }
        }

        additional_activity = {
            "name": "PyCharm",
            "start_time": 0,
            "end_time": 0
        }

        expected_result = mock_read_month_data_result.copy()
        expected_result["activity"][str(day)].append(additional_activity)

        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=mock_read_month_data_result)
        data_backend.write_month_data = MagicMock()

        data_model = CodeTimeDataRepository(data_backend)
        data_model.add_month_data(additional_activity, year=year, month=month, day=datetime.today().day)

        data_backend.read_month_data.assert_called_with(year=year, month=month)
        data_backend.write_month_data.assert_called_with(year, month, expected_result)

    def test_get_days_with_data(self):
        mock_data = {
            2020: {
                12: [str(datetime.today().day)]
            }
        }
        data_backend = DataBackend({})
        data_backend.get_days_with_data = MagicMock(return_value=mock_data)

        data_model = CodeTimeDataRepository(data_backend)
        result = data_model.get_days_with_data()
        self.assertDictEqual(mock_data, result)

    def test_get_months_with_data(self):
        mock_data = {
            2020: {
                12: [0]
            },
            2019: {
                12: [0]
            }
        }

        expected_data = {
            2020: [
                12
            ],
            2019: [
                12
            ]
        }

        data_backend = DataBackend({})
        data_backend.get_days_with_data = MagicMock(return_value=mock_data)

        data_model = CodeTimeDataRepository(data_backend)
        result = data_model.get_months_with_data()

        self.assertDictEqual(expected_data, result)

    def test_get_years_with_data(self):
        mock_data = {
            2020: {
                12: [0]
            },
            2019: {
                12: [0]
            }
        }

        data_backend = DataBackend({})
        data_backend.get_days_with_data = MagicMock(return_value=mock_data)

        data_model = CodeTimeDataRepository(data_backend)
        result = data_model.get_years_with_data()

        self.assertListEqual([2020, 2019], result)

    def test_write_config(self):
        config = {
            "test": True
        }

        data_backend = DataBackend({})
        data_backend.write_config = MagicMock()

        data_model = CodeTimeDataRepository(data_backend)
        data_model.write_config(config)

        data_backend.write_config.assert_called_with(config)

    def test_get_config(self):
        config = {
            "test": True
        }

        data_backend = DataBackend({})
        data_backend.read_config = MagicMock(return_value=config)

        data_model = CodeTimeDataRepository(data_backend)
        result = data_model.get_config()

        self.assertDictEqual(config, result)

    def test_get_statistics(self):
        mock_month_data = {
            "activity": {
                "0": [
                    {
                        "name": "IntelliJ",
                        "start_time": 0,
                        "end_time": 1000 * 10
                    },
                    {
                        "name": "PyCharm",
                        "start_time": 0,
                        "end_time": 1000 * 20
                    },
                    {
                        "name": "PyCharm",
                        "start_time": 0,
                        "end_time": 1000 * 60
                    },
                    {
                        "name": "VS Code",
                        "start_time": 0,
                        "end_time": 1000 * 5
                    },
                    {
                        "name": "Vim",
                        "start_time": 0,
                        "end_time": 1000 * 3
                    },
                    {
                        "name": "WebStorm",
                        "start_time": 0,
                        "end_time": 1000 * 1.5
                    },
                    {
                        "name": "Terminal",
                        "start_time": 0,
                        "end_time": 1000 * 0.5
                    }
                ]
            }
        }

        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=mock_month_data)

        data_model = CodeTimeDataRepository(data_backend)
        result = data_model.get_statistics(year=2021, month=0, day=0)

        expected_result = {
            "date": "Jan 01 2021",
            "total_time": 100000.0,
            "activities": [
                {
                    "name": "PyCharm",
                    "time": 1000 * 80,
                    "progress": 0.8
                },
                {
                    "name": "IntelliJ",
                    "time": 1000 * 10,
                    "progress": 0.1
                },
                {
                    "name": "VS Code",
                    "time": 1000 * 5,
                    "progress": 0.05
                },
                {
                    "name": "Vim, WebStorm and Terminal",
                    "time": 1000 * 5.0,
                    "progress": 0.05
                },
            ]
        }

        self.maxDiff = None
        self.assertDictEqual(expected_result, result)
