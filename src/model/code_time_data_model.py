from datetime import datetime

from src.data.data_backend import DataBackend


class CodeTimeDataModel:
    month_data = {}

    def __init__(self, data_backend: DataBackend):
        self.data_backend = data_backend

    def get_month_data(self, year=datetime.today().year, month=datetime.today().month):
        self._cache_month_data(year, month)
        return self.month_data[f"{month}{year}"]

    def _cache_month_data(self, year: int, month: int):
        self.month_data[f"{month}{year}"] = self.data_backend.read_month_data(year=year, month=month)

    def add_month_data(self, month_data, year=datetime.today().year, month=datetime.today().month,
                       day=datetime.today().day):
        key = f"{month}{year}"
        if key not in self.month_data:
            self._cache_month_data(year, month)

        data = self.month_data[key]
        day_str = str(day)
        if day_str not in data["activity"]:
            data["activity"][day_str] = []

        data["activity"][day_str].append(month_data)
        self.data_backend.write_month_data(year, month, data)

    def get_days_with_data(self):
        return self.data_backend.get_days_with_data()
