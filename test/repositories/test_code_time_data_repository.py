import datetime
import unittest
from unittest.mock import MagicMock

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
