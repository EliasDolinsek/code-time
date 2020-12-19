from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QColorDialog

from src.repositories.code_time_data_repository import CodeTimeDataRepository


class ThemeSettingsWidget(QWidget):
    def __init__(self, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.data_repository = data_repository
        self.layout = QVBoxLayout()

        description = QLabel()
        description.setText("Edit various theme colors to change the appearance of your statistics image.")
        self.layout.addWidget(description)

        title_layout = self.get_color_selection_layout("Title", "title_color")
        self.layout.addLayout(title_layout)

        total_time_layout = self.get_color_selection_layout("Total time", "total_time_color", )
        self.layout.addLayout(total_time_layout)

        progress_foreground_layout = self.get_color_selection_layout("Progress foreground", "progress_foreground_color")
        self.layout.addLayout(progress_foreground_layout)

        progress_background_layout = self.get_color_selection_layout("Progress background", "progress_background_color")
        self.layout.addLayout(progress_background_layout)

        activity_title_layout = self.get_color_selection_layout("Activity title", "activity_title_color")
        self.layout.addLayout(activity_title_layout)

        activity_time_layout = self.get_color_selection_layout("Activity time", "activity_time_color")
        self.layout.addLayout(activity_time_layout)

        watermark_layout = self.get_color_selection_layout("Watermark", "watermark_color")
        self.layout.addLayout(watermark_layout)

        self.setLayout(self.layout)

    def get_color(self, name):
        return self.data_repository.get_setting(name)

    def get_color_selection_layout(self, name, settings_key):
        color = self.get_color(settings_key)
        layout = QHBoxLayout()

        button = QPushButton()
        self.set_color_selection_button_color(button, color)
        button.clicked.connect(lambda: self.on_color_button_clicked(button, settings_key, color))

        label = QLabel()
        label.setText(name)

        layout.addWidget(button)
        layout.addWidget(label)

        layout.setStretch(0, 1)
        layout.setStretch(1, 3)

        return layout

    def on_color_button_clicked(self, button, settings_key, color):
        result = self.show_color_selection(color)
        if result is not None:
            self.on_color_changed(settings_key, result)
            self.set_color_selection_button_color(button, result)

    def show_color_selection(self, current_color):
        dialog = QColorDialog(self)
        dialog.setCurrentColor(QColor(current_color))

        if dialog.exec_():
            return dialog.currentColor().name()

    @staticmethod
    def set_color_selection_button_color(button, color):
        button.setStyleSheet(f"background-color: {color};")

    def on_color_changed(self, settings_key, color):
        self.data_repository.update_config(settings_key, color)
