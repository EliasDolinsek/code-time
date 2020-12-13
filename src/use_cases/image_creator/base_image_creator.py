from abc import ABC, abstractmethod

from PIL import ImageDraw

from src.repositories.code_time_data_repository import CodeTimeDataRepository


class BaseImageCreator(ABC):
    def __init__(self, data_repository: CodeTimeDataRepository):
        self.data_repository = data_repository

    @staticmethod
    def time_as_str(time):
        seconds = time / 1000

        minutes = int(seconds / 60 % 60)
        hours = int(seconds / 3600)

        return f"{hours}h {minutes}min"

    @abstractmethod
    def create_image(self, statistics: dict) -> ImageDraw:
        pass

    def get_config(self):
        return self.data_repository.get_config()

    def get_font(self, name):
        return self.get_config()["fonts"][name]
