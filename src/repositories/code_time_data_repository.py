from datetime import datetime

from src.data_sources.data_backend import DataBackend


class CodeTimeDataRepository:
    month_data = {}

    def __init__(self, data_backend: DataBackend):
        self.data_backend = data_backend

    def get_month_data(self, year=datetime.today().year, month=datetime.today().month):
        self._cache_month_data(year, month)
        return self.month_data[f"{month}{year}"]

    def _cache_month_data(self, year: int, month: int):
        self.month_data[f"{month}{year}"] = self.data_backend.read_month_data(year=year, month=month)

    def add_day_data(self, day_data, year=datetime.today().year, month=datetime.today().month,
                     day=datetime.today().day):
        key = f"{month}{year}"
        name = day_data["name"]
        time = day_data["time"]

        if key not in self.month_data:
            self._cache_month_data(year, month)

        data = self.month_data[key]
        if day not in data:
            data[day] = {}
            data[day][name] = time
        else:
            if name not in data[day]:
                data[day][name] = time
            else:
                data[day][name] += time
        self.data_backend.write_month_data(year, month, data)

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

    def get_config(self):
        return self.data_backend.read_config()

    def write_config(self, config):
        self.data_backend.write_config(config)

    @staticmethod
    def index_of_item_dict_with_name(name, activities):
        for i, d in enumerate(activities):
            if d["name"] == name:
                return i

        return -1

    def get_statistics(self, year, month, day):
        data = self.get_month_data(year, month)[day]
        total_time = 0
        sorted_activities = []

        for name in data:
            total_time += data[name]
            sorted_activities.append({
                "name": name,
                "time": data[name]
            })

        sorted_activities = sorted(sorted_activities, key=lambda activity: activity["time"], reverse=True)
        sorted_activities = CodeTimeDataRepository._summarize_activities(sorted_activities)

        for d in sorted_activities:
            d["progress"] = d["time"] / total_time

        return {
            "date": datetime(year, month, day).strftime("%b %d %Y"),
            "total_time": total_time,
            "activities": sorted_activities
        }

    @staticmethod
    def _summarize_activities(activities):
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
