import datetime
import unittest

from src.data_sources.data_backend import DataBackend
from src.repositories.code_time_data_repository import CodeTimeDataRepository


class CodeTimeDataRepositoryTest(unittest.TestCase):

    @staticmethod
    def get_default_repository():
        data_backend = DataBackend({})
        repository = CodeTimeDataRepository(data_backend)
        return data_backend, repository

    @staticmethod
    def get_default_month_data():
        return {
            1: {
                "PyCharm": 4000,
                "IntelliJ": 1000
            }
        }

    def test_get_cache_key(self):
        data_backend, repository = self.get_default_repository()
        test_date = datetime.date(2020, 1, 1)

        result = repository.get_cache_key(test_date)
        self.assertEqual("1-2020", result)

