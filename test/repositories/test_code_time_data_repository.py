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
        expected_result = {
            2020: {
                12: [str(datetime.today().day)]
            }
        }
        data_backend = DataBackend({})
        data_backend.get_days_with_data = MagicMock(return_value=expected_result)

        data_model = CodeTimeDataRepository(data_backend)
        result = data_model.get_days_with_data()
        self.assertDictEqual(expected_result, result)

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
