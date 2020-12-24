import datetime
import unittest
from unittest.mock import MagicMock, call

from src.data_sources.data_backend import DataBackend
from src.data_sources.errors import DefaultSettingNotFoundError
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

    def test_get_years_with_data(self):
        data_backend = DataBackend({})

        mock_return = {
            2020: {
                1: [1, 2, 3]
            }
        }

        data_backend.get_days_with_data = MagicMock(return_value=mock_return)
        data_repository = CodeTimeDataRepository(data_backend)

        result = data_repository.get_years_with_data()
        self.assertEqual([2020], result)

    def test_get_months_with_data(self):
        data_backend = DataBackend({})

        mock_return = {
            2020: {
                1: [1, 2, 3]
            }
        }

        data_backend.get_days_with_data = MagicMock(return_value=mock_return)
        data_repository = CodeTimeDataRepository(data_backend)

        result = data_repository.get_months_with_data()

        expected_result = {
            2020: [1]
        }

        self.assertEqual(expected_result, result)

    def test_get_config(self):
        mock_config = {"enabled": True}

        data_backend = DataBackend({})
        data_backend.read_config = MagicMock(return_value=mock_config)

        data_repository = CodeTimeDataRepository(data_backend)
        result = data_repository.get_config()

        self.assertDictEqual(mock_config, result)

    @staticmethod
    def test_write_config():
        mock_config = {"enabled": True}

        data_backend = DataBackend({})
        data_backend.write_config = MagicMock()

        data_repository = CodeTimeDataRepository(data_backend)
        data_repository.write_config(mock_config)

        data_backend.write_config.assert_called_once_with(mock_config)

    def test_update_setting(self):
        mock_config = {"enabled": True}

        data_backend = DataBackend({})
        data_backend.read_config = MagicMock(return_value=mock_config)
        data_backend.write_config = MagicMock()

        data_repository = CodeTimeDataRepository(data_backend)
        data_repository.update_setting("enabled", False)

        data_backend.write_config.assert_called_once_with({"enabled": False})

    def test_get_setting_available_key(self):
        mock_config = {"enabled": True}

        data_backend = DataBackend({})
        data_backend.read_config = MagicMock(return_value=mock_config)

        data_repository = CodeTimeDataRepository(data_backend)
        result = data_repository.get_setting("enabled")

        self.assertTrue(result)
        data_backend.read_config.assert_called_once()

    def test_get_setting_not_available_key(self):
        mock_config = {"enabled": True}
        data_repository = CodeTimeDataRepository(None)
        data_repository.get_config = MagicMock(return_value=mock_config)

        result = data_repository.get_setting("username")
        self.assertEqual("a random user", result)

    @staticmethod
    def test_reset_setting():
        data_repository = CodeTimeDataRepository(None)
        data_repository.get_default_setting = MagicMock(return_value="#000")
        data_repository.update_setting = MagicMock()

        data_repository.reset_setting("title_color")

        data_repository.update_setting.assert_called_once_with("title_color", "#000")
        data_repository.get_default_setting.assert_called_once_with("title_color")

    def test_get_default_setting_title_color(self):
        result = CodeTimeDataRepository.get_default_setting("title_color")
        self.assertEqual(result, "#000")

    def test_get_default_setting_total_time_color(self):
        result = CodeTimeDataRepository.get_default_setting("total_time_color")
        self.assertEqual(result, "#000")

    def test_get_default_setting_progress_background_color(self):
        result = CodeTimeDataRepository.get_default_setting("progress_background_color")
        self.assertEqual(result, "#E0E0E0")

    def test_get_default_setting_progress_foreground_color(self):
        result = CodeTimeDataRepository.get_default_setting("progress_foreground_color")
        self.assertEqual(result, "#3f51b5")

    def test_get_default_setting_activity_title_color(self):
        result = CodeTimeDataRepository.get_default_setting("activity_title_color")
        self.assertEqual(result, "#000")

    def test_get_default_setting_activity_time_color(self):
        result = CodeTimeDataRepository.get_default_setting("activity_time_color")
        self.assertEqual(result, "#000")

    def test_get_default_setting_watermark_color(self):
        result = CodeTimeDataRepository.get_default_setting("watermark_color")
        self.assertEqual(result, "#000")

    def test_get_default_setting_activities(self):
        result = CodeTimeDataRepository.get_default_setting("activities")
        self.assertListEqual(result, [])

    def test_get_default_setting_user_image(self):
        result = CodeTimeDataRepository.get_default_setting("user_image")
        self.assertEqual(result, "default_user.png")

    def test_get_default_setting_username(self):
        result = CodeTimeDataRepository.get_default_setting("username")
        self.assertEqual(result, "a random user")

    def test_get_default_setting_invalid_key(self):
        self.assertRaises(DefaultSettingNotFoundError, CodeTimeDataRepository.get_default_setting, "some_invalid_key")

    def test_get_statistics(self):
        mock_month_data = {
            1: {
                "PyCharm": 4000,
                "IntelliJ": 6000
            }
        }

        data_backend = DataBackend({})
        data_backend.read_month_data = MagicMock(return_value=mock_month_data)

        data_repository = CodeTimeDataRepository(data_backend)
        result = data_repository.get_statistics(datetime.date(2020, 1, 1))

        expected_result = {
            "date": "Jan 01 2020",
            "total_time": 10000,
            "activities": [
                {
                    "name": "IntelliJ",
                    "time": 6000,
                    "progress": 0.6
                },
                {
                    "name": "PyCharm",
                    "time": 4000,
                    "progress": 0.4
                }
            ]
        }

        self.assertDictEqual(expected_result, result)

    def test_summarize_activities_single_activity(self):
        activities = [
            {
                "name": "PyCharm",
                "time": 1000
            }
        ]

        result = CodeTimeDataRepository.summarize_activities(activities)

        self.assertListEqual(activities, result)

    def test_summarize_activities_four_activities(self):
        activities = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion",
                "time": 1000
            }
        ]

        result = CodeTimeDataRepository.summarize_activities(activities)

        self.assertListEqual(activities, result)

    def test_summarize_activities_five_activities(self):
        activities = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion",
                "time": 1000
            },
            {
                "name": "XD",
                "time": 1000
            }
        ]

        result = CodeTimeDataRepository.summarize_activities(activities)

        expected_result = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion, XD",
                "time": 2000
            },
        ]

        self.assertListEqual(expected_result, result)

    def test_summarize_activities_six_activities(self):
        activities = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion",
                "time": 1000
            },
            {
                "name": "XD",
                "time": 1000
            },
            {
                "name": "Vim",
                "time": 1000
            }
        ]

        result = CodeTimeDataRepository.summarize_activities(activities)

        expected_result = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion, XD and Vim",
                "time": 3000
            },
        ]

        self.assertListEqual(expected_result, result)

    def test_summarize_activities_seven_activities(self):
        activities = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion",
                "time": 1000
            },
            {
                "name": "XD",
                "time": 1000
            },
            {
                "name": "Vim",
                "time": 1000
            },
            {
                "name": "VS Code",
                "time": 1000
            }
        ]

        result = CodeTimeDataRepository.summarize_activities(activities)

        expected_result = [
            {
                "name": "PyCharm",
                "time": 1000
            },
            {
                "name": "IntelliJ",
                "time": 1000
            },
            {
                "name": "Terminal",
                "time": 1000
            },
            {
                "name": "CLion, XD and more",
                "time": 4000
            },
        ]

        self.assertListEqual(expected_result, result)

    def test_get_res_file_path(self):
        data_backend = DataBackend({})
        data_backend.get_res_file_path = MagicMock(return_value="/test.txt")

        repository = CodeTimeDataRepository(data_backend)
        result = repository.get_res_file_path("test.txt")

        self.assertEqual("/test.txt", result)
        data_backend.get_res_file_path.assert_called_once_with("test.txt")

    def test_get_file_from_setting(self):
        repository = CodeTimeDataRepository(None)
        repository.get_res_file_path = MagicMock(return_value="/test.txt")
        repository.get_setting = MagicMock(return_value="setting")

        result = repository.get_file_from_setting("setting")

        self.assertEqual(result, "/test.txt")
        repository.get_res_file_path.assert_called_once_with("setting")

    @staticmethod
    def test_write_default_config():
        data_backend = DataBackend({})
        data_backend.write_config = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        repository.write_default_config()

        expected_config = {'title_color': '#000', 'total_time_color': '#000', 'progress_background_color': '#E0E0E0',
                           'progress_foreground_color': '#3f51b5', 'activity_title_color': '#000',
                           'activity_time_color': '#000', 'watermark_color': '#000', 'image': 'default_background.png',
                           'user_image': 'default_user.png', 'activities': [],
                           'fonts': {'semi_bold': 'fonts/OpenSans-SemiBold.ttf', 'bold': 'fonts/OpenSans-Bold.ttf',
                                     'extra_bold': 'fonts/OpenSans-ExtraBold.ttf'}, 'username': 'a random user'}

        data_backend.write_config.assert_called_once_with(expected_config)

    @staticmethod
    def test_reset_settings():
        repository = CodeTimeDataRepository(None)
        repository.write_default_config = MagicMock()
        repository.cache_config = MagicMock()

        repository.reset_settings()

        repository.write_default_config.assert_called_once()
        repository.cache_config.assert_called_once()

    @staticmethod
    def test_create_default_config_if_config_is_missing():
        data_backend = DataBackend({})
        data_backend.does_config_file_exist = MagicMock(return_value=False)
        data_backend.write_config = MagicMock()

        repository = CodeTimeDataRepository(data_backend)
        repository.create_default_config_if_config_is_missing()
        data_backend.write_config.assert_called_once()
