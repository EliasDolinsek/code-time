from src.data_sources.data_backend import DataBackend
from src.presentation.tray_handler import TrayHandler
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import MacFocusActivityProvider
from src.use_cases.activity_tracker import ActivityTracker
from src.use_cases.image_creator import ImageCreator

if __name__ == "__main__":
    config = {
        "title_color": (0, 0, 0, 255),
        "total_time_color": (0, 0, 0, 255),
        "progress_background_color": (0, 150, 199, 33),
        "progress_foreground_color": (0, 150, 199, 255),
        "activity_title_color": (0, 0, 0, 255),
        "activity_time_color": (0, 0, 0, 255),
        "watermark_color": (0, 0, 0, 255),
        "data_directory": "/Users/eliasdolinsek/development/python-development/code-time/dev_assets/data",
        "config": "/Users/eliasdolinsek/development/python-development/code-time/dev_assets/config.json"
    }

    data_backend = DataBackend(config)
    data_repository = CodeTimeDataRepository(data_backend=data_backend)
    focus_activity_provider = MacFocusActivityProvider()

    image_creator = ImageCreator(data_backend.read_config())
    activity_tracker = ActivityTracker(data_repository=data_repository, focus_activity_provider=focus_activity_provider)
    activity_tracker.start()

    tray_handler = TrayHandler(image_creator=image_creator, activity_tracker=activity_tracker,
                               data_repository=data_repository)
    tray_handler.start()
