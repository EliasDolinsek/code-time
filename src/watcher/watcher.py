import sys
import time
from datetime import datetime

from src.watcher.data_manager import read_config, read_month_data, write_month_data
from src.watcher.focus_activity_provider import MacFocusActivityProvider

if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    focus_activity_provider = MacFocusActivityProvider()


def is_activity_tracked_activity(config, activity_name):
    return activity_name in config["activities"]


def new_activity_data(activity_name):
    return {"activity": activity_name, "start_time": str(datetime.now().timestamp())}


if __name__ == "__main__":
    today_date = datetime.today()
    month_data = read_month_data(str(today_date.month), str(today_date.year))

    if "activity" not in month_data:
        month_data["activity"] = {}

    if str(today_date.day) not in month_data["activity"]:
        month_data["activity"][today_date.day] = []

    current_config = read_config()
    last_activity_data = None

    while True:
        current_activity = focus_activity_provider.get_activity_name()
        if last_activity_data is None and new_activity_data(current_activity):
            last_activity_data = new_activity_data(current_activity)
        if last_activity_data["activity"] != current_activity:
            last_activity_data["stop_time"] = str(datetime.now().timestamp())
            month_data["activity"][str(today_date.day)].append(last_activity_data)

            write_month_data(str(today_date.month), str(today_date.year), month_data)
            if is_activity_tracked_activity(current_config, current_activity):
                last_activity_data = new_activity_data(current_activity)

        time.sleep(1)
