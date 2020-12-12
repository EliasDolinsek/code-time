import datetime
import unittest
from unittest.mock import MagicMock, call

from src.data_sources.data_backend import DataBackend
from src.repositories.code_time_data_repository import CodeTimeDataRepository


class CodeTimeDataRepositoryTest(unittest.TestCase):

    @staticmethod
    def get_default_month_data():
        return {
            1: {
                "PyCharm": 4000,
                "IntelliJ": 1000
            }
        }

    def test_get_cache_key(self):
        data_backend = DataBackend({})
        repository = CodeTimeDataRepository(data_backend)
        test_date = datetime.date(2020, 1, 1)

        result = repository.get_cache_key(test_date)
        self.assertEqual("1-2020", result)

    def test_cache_month_data(self):
        data_backend = DataBackend({})
        test_date = datetime.date(2020, 1, 1)

        data_backend.read_month_data = MagicMock(return_value=self.get_default_month_data())
        repository = CodeTimeDataRepository(data_backend)

        repository.cache_month_data(test_date)

        expected_result = {
            "1-2020": self.get_default_month_data()
        }

        self.assertEqual(expected_result, repository.cached_month_data)

    def test_get_month_data_cached(self):
        data_backend = DataBackend({})
        test_date = datetime.date(2020, 1, 1)

        data_backend.read_month_data = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        repository.cached_month_data["1-2020"] = self.get_default_month_data()

        result = repository.get_month_data(test_date)

        data_backend.read_month_data.assert_not_called()
        self.assertEqual(self.get_default_month_data(), result)

    def test_get_month_data_not_cached(self):
        data_backend = DataBackend({})
        test_date = datetime.date(2020, 1, 1)

        data_backend.read_month_data = MagicMock(return_value=self.get_default_month_data())
        repository = CodeTimeDataRepository(data_backend)

        result = repository.get_month_data(test_date)

        data_backend.read_month_data.assert_called_once_with(test_date)
        self.assertEqual(self.get_default_month_data(), result)

    @staticmethod
    def get_default_day_data_to_add(start_time=datetime.time(0, 0, 0)):
        return {
            "name": "PyCharm",
            "time": 4000,
            "start_time": start_time
        }

    def test_add_day_data_new_day(self):
        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=self.get_default_month_data())
        data_backend.write_month_data = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        test_date = datetime.datetime(2020, 2, 2)

        repository.add_day_data(self.get_default_day_data_to_add(), test_date)

        expected_month_data = self.get_default_month_data()
        expected_month_data[2] = {}
        expected_month_data[2]["PyCharm"] = 4000

        data_backend.read_month_data.assert_called_once_with(test_date)
        data_backend.write_month_data.assert_called_once_with(expected_month_data, test_date)

    def test_add_day_data_new_activity(self):
        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=self.get_default_month_data())
        data_backend.write_month_data = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        test_date = datetime.date(2020, 1, 1)

        day_data_to_add = {
            "name": "Terminal",
            "time": 4000,
            "start_time": datetime.time(0, 0, 0)
        }
        repository.add_day_data(day_data_to_add, test_date)

        expected_month_data = self.get_default_month_data()
        expected_month_data[1]["Terminal"] = 4000

        data_backend.read_month_data.assert_called_once_with(test_date)
        data_backend.write_month_data.assert_called_once_with(expected_month_data, test_date)

    def test_add_day_data_activity(self):
        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=self.get_default_month_data())
        data_backend.write_month_data = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        test_date = datetime.date(2020, 1, 1)

        repository.add_day_data(self.get_default_day_data_to_add(), test_date)

        expected_month_data = self.get_default_month_data()
        expected_month_data[1]["PyCharm"] = 8000

        data_backend.read_month_data.assert_called_once_with(test_date)
        data_backend.write_month_data.assert_called_once_with(expected_month_data, test_date)

    def test_add_day_data_activity_exceeding_current_day(self):
        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=self.get_default_month_data())
        data_backend.write_month_data = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        test_date = datetime.date(2020, 1, 1)

        test_start_time = datetime.time(23, 59, 59)
        repository.add_day_data(self.get_default_day_data_to_add(test_start_time), test_date)

        expected_month_data = {
            1: {
                "PyCharm": 5000,
                "IntelliJ": 1000
            },
            2: {
                "PyCharm": 3000
            }
        }

        data_backend.read_month_data.assert_called_once_with(datetime.date(2020, 1, 2))
        data_backend.write_month_data.assert_has_calls([call(expected_month_data, test_date)], any_order=True)

    def test_get_days_with_data(self):
        data_backend = DataBackend({})

        mock_return = {
            2020: {
                1: [1, 2, 3]
            }
        }

        data_backend.get_days_with_data = MagicMock(return_value=mock_return)
        data_repository = CodeTimeDataRepository(data_backend)

        result = data_repository.get_days_with_data()
        self.assertEqual(mock_return, result)
