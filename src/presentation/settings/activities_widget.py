from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListWidget, QPushButton, QFrame

from src.presentation.add_activity_dialog import AddActivityDialog
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import FocusActivityProvider


class ActivitiesWidget(QWidget):
    def __init__(self, focus_activity_provider: FocusActivityProvider, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.focus_activity_provider = focus_activity_provider
        self.data_repository = data_repository
        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()
        self.list_widget.selectionModel().selectionChanged.connect(self.on_selection_changed)

        self.btn_remove = QPushButton()
        self.btn_remove.setText("REMOVE")
        self.btn_remove.setEnabled(False)
        self.btn_remove.clicked.connect(self.on_remove)

        self.div = QFrame()
        self.div.setFrameShape(QFrame.HLine)
        self.div.setFrameShadow(QFrame.Sunken)

        self.btn_add_activities = QPushButton()
        self.btn_add_activities.setText("ADD NEW ACTIVITY")
        self.btn_add_activities.clicked.connect(self.on_add_new_activity)

        self.layout.addWidget(self.btn_add_activities)
        self.layout.addWidget(self.div)
        self.layout.addWidget(self.list_widget)
        self.layout.addWidget(self.btn_remove)

        self.load_activities_into_list()
        self.setLayout(self.layout)

    def on_selection_changed(self):
        self.btn_remove.setEnabled(True)

    def on_add_new_activity(self):
        dialog = AddActivityDialog(self.focus_activity_provider, self.data_repository)
        dialog.exec_()
        self.load_activities_into_list()

    def on_remove(self):
        if self.list_widget.currentItem() is not None:
            activities = self.data_repository.get_setting("activities")
            activities.remove(self.list_widget.currentItem().text())

            self.data_repository.update_config("activities", activities)
            self.load_activities_into_list()

    def load_activities_into_list(self):
        self.list_widget.clear()
        for activity in self.data_repository.get_setting("activities"):
            self.list_widget.addItem(activity)
