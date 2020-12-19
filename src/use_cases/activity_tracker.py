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
        return activity in self.data_repository.get_setting("activities")

    def run(self):
        last_activity = self.focus_activity_provider.get_activity_name()
        start_date = datetime.now()
        time_diff = 0

        def write_if_activity_is_to_track():
            if self.is_activity_to_track(last_activity):
                self.data_repository.add_day_data({
                    "name": last_activity,
                    "time": time_diff,
                    "start_time": start_date.time()
                }, start_date.date())

        while not self.quit_app:
            if not self.tracking_paused:
                current_activity = self.focus_activity_provider.get_activity_name()
                if last_activity != current_activity:
                    write_if_activity_is_to_track()
                    last_activity = current_activity

                    time_diff = 0
                    start_date = datetime.now()
            else:
                if time_diff > 0:
                    write_if_activity_is_to_track()
                    time_diff = 0

            time_diff += 1000
            time.sleep(1)

        write_if_activity_is_to_track()
