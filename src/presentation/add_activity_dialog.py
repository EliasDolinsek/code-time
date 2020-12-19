import time
from threading import Thread

from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton

from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import FocusActivityProvider


class AddActivityDialog(QDialog):
    def __init__(self, activity_provider: FocusActivityProvider, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.data_repository = data_repository
        self.setWindowTitle("Add Activity")

        layout = QVBoxLayout()

        title = QLabel(
            "To add a new activity, simply bring the desired application into foreground\nand then select it from the "
            "list below")

        layout.addWidget(title)

        self.list_widget = QListWidget()
        self.list_widget.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self.list_manager = AddActivityListManager(self.list_widget, activity_provider, data_repository)
        self.list_manager.start()

        self.add_button = QPushButton("ADD SELECTED ACTIVITY")
        self.add_button.setEnabled(False)
        self.add_button.clicked.connect(self.on_add_activity)

        layout.addWidget(self.list_widget)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def on_selection_changed(self):
        self.add_button.setEnabled(True)

    def on_add_activity(self):
        if self.list_widget.currentItem() is not None:
            activities = self.data_repository.get_setting("activities")
            activities.append(self.list_widget.currentItem().text())
            self.data_repository.update_config("activities", activities)

            self.list_manager.stop()
            self.close()

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.list_manager.stop()


class AddActivityListManager(Thread):
    def __init__(self, list_widget: QListWidget, activity_provider: FocusActivityProvider,
                 data_repository: CodeTimeDataRepository):
        super().__init__()

        self.data_repository = data_repository
        self.activity_provider = activity_provider
        self.list_widget = list_widget
        self.running = True

    def is_activity_not_being_tracked(self, activity):
        return activity not in self.data_repository.get_setting("activities")

    def stop(self):
        self.running = False

    def run(self) -> None:
        last_activity = self.activity_provider.get_activity_name()
        while self.running:
            current_activity = self.activity_provider.get_activity_name()
            if last_activity != current_activity and self.is_activity_not_being_tracked(
                    current_activity) and current_activity:
                self.list_widget.addItem(current_activity)
                last_activity = current_activity

            time.sleep(0.25)
