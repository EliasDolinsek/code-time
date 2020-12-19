from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget

from src.presentation.settings.activities_widget import ActivitiesWidget
from src.presentation.settings.autostart_widget import AutostartWidget
from src.presentation.settings.theme_settings_widget import ThemeSettingsWidget
from src.presentation.settings.user_image_widget import UserImageWidget
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import FocusActivityProvider


class SettingsDialog(QDialog):
    def __init__(self, focus_activity_provider: FocusActivityProvider, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.focus_activity_provider = focus_activity_provider
        self.data_repository = data_repository

        self.setWindowTitle("code-time Settings")
        self.layout = QVBoxLayout(self)

        # Tab widget
        self.tabs = QTabWidget()

        self.tabs.addTab(ThemeSettingsWidget(self.data_repository), "Theme")
        self.tabs.addTab(UserImageWidget(self.data_repository), "User Image")
        self.tabs.addTab(AutostartWidget(), "Autostart")
        self.tabs.addTab(ActivitiesWidget(self.focus_activity_provider, self.data_repository), "Activities")

        self.layout.addWidget(self.tabs)
