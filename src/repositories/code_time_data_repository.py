from datetime import datetime

from src.data_sources.data_backend import DataBackend


class CodeTimeDataRepository:
    month_data_year = None
    month_data_month = None
    month_data = {}

    def __init__(self, data_backend: DataBackend):
        self.data_backend = data_backend

    def get_month_data(self, year=datetime.today().year, month=datetime.today().month):
        self._cache_month_data(year, month)
        return self.month_data[f"{month}{year}"]

    def _cache_month_data(self, year: int, month: int):
        self.month_data[f"{month}{year}"] = self.data_backend.read_month_data(year=year, month=month)
        self.month_data_year = year
        self.month_data_month = month

    def add_month_data(self, month_data, year=datetime.today().year, month=datetime.today().month,
                       day=datetime.today().day):
        key = f"{month}{year}"

        if self.month_data_year != year or self.month_data_month != month or key not in self.month_data:
            self._cache_month_data(year, month)

        data = self.month_data[key]
        day_str = str(day)

        if "activity" not in data:
            data["activity"] = {}

        if day_str not in data["activity"]:
            data["activity"][day_str] = []

        data["activity"][day_str].append(month_data)
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
