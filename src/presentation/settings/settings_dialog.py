from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget

from src.presentation.settings.theme_settings_widget import ThemeSettingsWidget
from src.presentation.settings.user_image_widget import UserImageWidget
from src.repositories.code_time_data_repository import CodeTimeDataRepository


class SettingsDialog(QDialog):
    def __init__(self, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.data_repository = data_repository
        self.layout = QVBoxLayout(self)

        # Tab widget
        self.tabs = QTabWidget()

        # Tabs
        self.autostart_tab = QWidget()
        self.activities_tab = QWidget()

        self.tabs.addTab(ThemeSettingsWidget(self.data_repository), "Theme")
        self.tabs.addTab(UserImageWidget(self.data_repository), "User Image")
        self.tabs.addTab(self.autostart_tab, "Autostart")
        self.tabs.addTab(self.activities_tab, "Activities")

        self.layout.addWidget(self.tabs)
