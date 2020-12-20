import datetime

from src.data_sources.data_backend import DataBackend
from src.data_sources.errors import DefaultSettingNotFoundError


class CodeTimeDataRepository:
    cached_month_data = {}
    cached_config = None

    def __init__(self, data_backend: DataBackend):
        self.data_backend = data_backend

    @staticmethod
    def get_cache_key(date: datetime.date):
        return f"{date.month}-{date.year}"

    def cache_month_data(self, date: datetime.date):
        self.cached_month_data[self.get_cache_key(date)] = self.data_backend.read_month_data(date)

    def get_month_data(self, date: datetime.date):
        """
        :param date: date of desired month
        :return: month data using DataBackend
        """
        cache_key = self.get_cache_key(date)

        if cache_key not in self.cached_month_data:
            self.cache_month_data(date)

        return self.cached_month_data[cache_key]

    def add_day_data(self, data: dict, date: datetime.date):
        """
        Saves time tracking data

        Example structure for data argument:
        data: dict
            {
                "name": "PyCharm",
                "time": 3000,
                "start_time": datetime.time
            }
        """

        cache_key = self.get_cache_key(date)

        name = data["name"]
        time = data["time"]
        start_time = data["start_time"]

        start_datetime = datetime.datetime.combine(date, start_time)
        if (start_datetime + datetime.timedelta(milliseconds=time)).date() > date:
            next_day_date = datetime.datetime.combine(date, start_time) + datetime.timedelta(days=1)
            next_day_date = next_day_date.replace(hour=0, minute=0, second=0)
            time_diff = next_day_date - start_datetime

            day_data = {
                "name": name,
                "time": time - time_diff.seconds * 1000,
                "start_time": datetime.time(0, 0, 0)
            }

            self.add_day_data(day_data, next_day_date.date())
            time = time_diff.seconds * 1000

        if cache_key not in self.cached_month_data:
            self.cache_month_data(date)

        cached_data = self.cached_month_data[cache_key]

        day = date.day
        if date.day not in cached_data:
            cached_data[day] = {}

        if name not in cached_data[day]:
            cached_data[day][name] = time
        else:
            cached_data[day][name] += time

        self.cached_month_data[cache_key] = cached_data
        self.data_backend.write_month_data(cached_data, date)

    def get_days_with_data(self):
        return self.data_backend.get_days_with_data()

    def get_months_with_data(self):
        data = self.get_days_with_data()
        result = {}
        for key in data.keys():
            result[key] = list(data[key].keys())

        return result

    def get_years_with_data(self):
        data = self.get_days_with_data()
        return list(data.keys())

    def cache_config(self):
        self.cached_config = self.data_backend.read_config()

    def get_config(self):
        if self.cached_config is None:
            self.cache_config()

        return self.cached_config

    def write_config(self, config):
        self.cached_config = config
        self.data_backend.write_config(config)

    def get_setting(self, name):
        return self.get_config()[name]

    def update_setting(self, name, value):
        config = self.get_config()
        config[name] = value
        self.write_config(config)

    def reset_setting(self, name):
        self.update_setting(name, self.get_default_setting(name))

    def get_file_from_setting(self, name):
        return self.get_res_file_path(self.get_setting(name))

    def get_res_file_path(self, relative_name):
        return str(self.data_backend.get_res_file_path(relative_name))

    @staticmethod
    def get_default_setting(name):
        if name == "title_color":
            return "#000"
        elif name == "total_time_color":
            return "#000"
        elif name == "progress_background_color":
            return "#E0E0E0"
        elif name == "progress_foreground_color":
            return "#3f51b5"
        elif name == "activity_title_color":
            return "#000"
        elif name == "activity_time_color":
            return "#000"
        elif name == "watermark_color":
            return "#000"
        elif name == "image":
            return "default_background.png"
        elif name == "user_image":
            return "default_user.png"
        elif name == "activities":
            return []
        elif name == "fonts":
            return {
                "semi_bold": "fonts/OpenSans-SemiBold.ttf",
                "bold": "fonts/OpenSans-Bold.ttf",
                "extra_bold": "fonts/OpenSans-ExtraBold.ttf"
            }
        else:
            raise DefaultSettingNotFoundError(message=f"Invalid settings key {name}")

    def get_statistics(self, date: datetime.date):
        data = self.get_month_data(date)[date.day]
        total_time = 0
        sorted_activities = []

        for name in data.keys():
            total_time += data[name]
            sorted_activities.append({
                "name": name,
                "time": data[name]
            })

        sorted_activities = sorted(sorted_activities, key=lambda activity: activity["time"], reverse=True)
        sorted_activities = CodeTimeDataRepository.summarize_activities(sorted_activities)

        for d in sorted_activities:
            d["progress"] = d["time"] / total_time

        return {
            "date": date.strftime("%b %d %Y"),
            "total_time": total_time,
            "activities": sorted_activities
        }

    @staticmethod
    def summarize_activities(activities):
        if len(activities) > 3:
            summarised_activities = activities[3:]
            summarised_activities_time = 0

            names_str = ""

            for i, d in enumerate(summarised_activities[:2]):
                summarised_activities_time += d["time"]
                if i == 0:
                    names_str += d["name"]
                else:
                    names_str += f", {d['name']}"

            remaining_activities = summarised_activities[2:]

            if len(remaining_activities) > 1:
                names_str += " and more"
                for activity in remaining_activities:
                    summarised_activities_time += activity["time"]
            elif len(remaining_activities) == 1:
                names_str += f" and {remaining_activities[0]['name']}"
                summarised_activities_time += remaining_activities[0]["time"]

            return activities[:3] + [{
                "name": names_str,
                "time": summarised_activities_time
            }]
        else:
            return activities
