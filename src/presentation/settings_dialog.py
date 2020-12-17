from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget


class SettingsDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout(self)

        # Tab widget
        self.tabs = QTabWidget()

        # Tabs
        self.colors_tab = QWidget()
        self.user_image_tab = QWidget()
        self.autostart_tab = QWidget()
        self.activities_tab = QWidget()

        # Add tabs to tab widget
        self.tabs.addTab(self.colors_tab, "Colors")
        self.tabs.addTab(self.user_image_tab, "User Image Tab")
        self.tabs.addTab(self.autostart_tab, "Autostart")
        self.tabs.addTab(self.activities_tab, "Activities")

        self.layout.addWidget(self.tabs)
