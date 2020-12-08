import time
from datetime import datetime
import threading

from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import FocusActivityProvider


class ActivityTracker(threading.Thread):
    def __init__(self, data_repository: CodeTimeDataRepository, focus_activity_provider: FocusActivityProvider):
        super().__init__()

        self.focus_activity_provider = focus_activity_provider
        self.data_repository = data_repository

        self.tracking_paused = False
        self.quit_app = False

    def on_pause_continue(self):
        self.tracking_paused = not self.tracking_paused
        return self.tracking_paused

    def on_quit(self):
        self.quit_app = True

    def is_activity_to_track(self, activity):
        return activity in self.data_repository.get_config()["activities"]

    def run(self):
        last_activity = self.focus_activity_provider.get_activity_name()
        activity_start_time = datetime.now().timestamp()

        while not self.quit_app:
            if not self.tracking_paused:
                current_activity = self.focus_activity_provider.get_activity_name()
                if last_activity != current_activity:
                    if self.is_activity_to_track(last_activity):
                        self.data_repository.add_month_data({
                            "name": last_activity,
                            "start_time": activity_start_time,
                            "stop_time": datetime.now().timestamp()
                        })

                    last_activity = current_activity

            time.sleep(1)
