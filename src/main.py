from pathlib import Path

from src.data_sources.data_backend import DataBackend
from src.presentation.tray_handler import TrayHandler
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import MacFocusActivityProvider
from src.use_cases.activity_tracker import ActivityTracker
from src.use_cases.autostart import CodeTimeAutostart
from src.use_cases.image_creator.basic_image_creator import BasicImageCreator

if __name__ == "__main__":
    config = {
        "data_directory": Path("../data").resolve(),
        "config": Path("../res/config.json").resolve()
    }

    data_backend = DataBackend(config)
    data_repository = CodeTimeDataRepository(data_backend=data_backend)
    data_repository.create_default_config_if_config_is_missing()

    focus_activity_provider = MacFocusActivityProvider()

    image_creator = BasicImageCreator(data_repository)
    activity_tracker = ActivityTracker(data_repository=data_repository, focus_activity_provider=focus_activity_provider)
    activity_tracker.start()

    autostart = CodeTimeAutostart(Path(__file__).resolve())
    tray_handler = TrayHandler(image_creator=image_creator, activity_tracker=activity_tracker,
                               data_repository=data_repository, activity_provider=focus_activity_provider,
                               autostart=autostart)
    tray_handler.start()
