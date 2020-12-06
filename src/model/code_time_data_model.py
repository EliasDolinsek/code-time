from datetime import datetime

from src.data.data_backend import DataBackend


class CodeTimeDataModel:
    month_data = {}

    def __init__(self, data_backend: DataBackend):
        self.data_backend = data_backend

    def get_month_data(self, year=datetime.today().year, month=datetime.today().month):
        self._store_month_data(year, month)
        return self.month_data[f"{month}{year}"]

    def _store_month_data(self, year: int, month: int):
        self.month_data[f"{month}{year}"] = self.data_backend.read_month_data(year=year, month=month)

    def add_month_data(self, year, month, day, month_data):
        key = f"{month}{year}"
        if key not in self.month_data:
            self._store_month_data(year, month)

        data = self.month_data[key]
        if str(day) not in data:
            data[day] = []

        data[day].append(month_data)
