import sys
import time
from src.watcher.data_manager import DataManager, CONFIG_FILE
from src.watcher.focus_activity_provider import MacFocusActivityProvider

data_manager = DataManager(CONFIG_FILE)
if sys.platform in ['Mac', 'darwin', 'os2', 'os2emx']:
    focus_activity_provider = MacFocusActivityProvider()


def is_activity_tracked_activity(config, activity_name):
    return activity_name in config["activities"]


if __name__ == "__main__":
    current_config = data_manager.read_config()
    while True:
        current_activity = focus_activity_provider.get_activity_name()
        if is_activity_tracked_activity(current_config, current_activity):
            print("Track", current_activity)
        else:
            print("No track", current_activity)

        time.sleep(1)
