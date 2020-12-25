from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget

from src.presentation.settings.activities_widget import ActivitiesWidget
from src.presentation.settings.autostart_widget import AutostartWidget
from src.presentation.settings.general_widget import GeneralWidget
from src.presentation.settings.theme_widget import ThemeWidget
from src.presentation.settings.user_image_widget import UserImageWidget
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import FocusActivityProvider
from src.use_cases.autostart import AutostartManager


class SettingsDialog(QDialog):
    def __init__(self, focus_activity_provider: FocusActivityProvider, data_repository: CodeTimeDataRepository, autostart: AutostartManager):
        super().__init__()
        self.autostart = autostart
        self.focus_activity_provider = focus_activity_provider
        self.data_repository = data_repository

        self.setWindowTitle("code-time Settings")
        self.layout = QVBoxLayout(self)

        # Tab widget
        self.tabs = QTabWidget()

        self.tabs.addTab(GeneralWidget(self.data_repository, self), "General")
        self.tabs.addTab(ThemeWidget(self.data_repository), "Theme")
        self.tabs.addTab(UserImageWidget(self.data_repository), "User Image")
        self.tabs.addTab(AutostartWidget(self.autostart), "Autostart")
        self.tabs.addTab(ActivitiesWidget(self.focus_activity_provider, self.data_repository), "Activities")

        self.layout.addWidget(self.tabs)
