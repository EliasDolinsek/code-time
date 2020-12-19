import datetime

from pathlib import Path

from PIL.ImageQt import ImageQt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.data_sources.errors import CodeTimeError
from src.presentation.add_activity_dialog import AddActivityDialog
from src.presentation.settings.settings_dialog import SettingsDialog
from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.repositories.focus_activity_provider import FocusActivityProvider
from src.use_cases.activity_tracker import ActivityTracker
from src.use_cases.image_creator.basic_image_creator import BasicImageCreator

TEXT_PAUSE = "Pause tracking"
TEXT_CONTINUE = "Continue tracking"


class TrayHandler:

    def __init__(self, image_creator: BasicImageCreator, activity_tracker: ActivityTracker,
                 data_repository: CodeTimeDataRepository, activity_provider: FocusActivityProvider):
        super().__init__()
        self.activity_provider = activity_provider
        self.image_creator = image_creator
        self.activity_tracker = activity_tracker
        self.data_repository = data_repository

        self.action_pause_continue = QAction(TEXT_PAUSE)
        self.action_quit = QAction("Quit")

        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

    def start(self):
        icon = QIcon("../res/clock.svg")

        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()

        self.action_quit.triggered.connect(lambda x: self._on_quit())
        self.action_pause_continue.triggered.connect(lambda x: self._on_pause_continue())

        menu.addAction(self.action_pause_continue)
        self.add_statistics_to_menu(menu)

        self.setup_add_activity(menu)
        self.setup_settings(menu)
        menu.addAction(self.action_quit)

        tray.setContextMenu(menu)
        self.app.exec_()

    def setup_settings(self, menu):
        menu.addAction("Settings").triggered.connect(self.on_settings)

    def on_settings(self):
        dialog = SettingsDialog(self.activity_provider, self.data_repository)
        dialog.exec_()

    def setup_add_activity(self, menu):
        menu.addAction("Add activity").triggered.connect(self.on_add_activity)

    def on_add_activity(self):
        dialog = AddActivityDialog(self.activity_provider, self.data_repository)
        dialog.exec_()

    def save_statistic_as_png(self, date):
        recommended_path = str(Path.home().joinpath(f"code-time_{date.day}{date.month}{date.year}.png"))
        result = QFileDialog.getSaveFileName(QFileDialog(), "Save statistic", recommended_path, "Image (*.png)"),

        selected_path = result[0][0]
        if selected_path != "":
            statistics = self.data_repository.get_statistics(date)
            self.image_creator.create_image(statistics).save(selected_path)

    def add_days_statistics_to_menu(self, menu, date: datetime.date):
        days = self.data_repository.get_days_with_data()[date.year][date.month]
        for day in days:
            day_action = menu.addAction(str(day))
            day_date = date.replace(day=day)
            self.add_statistic_actions_to_menu(day_action, day_date)

    def add_months_statistics_to_menu(self, menu, date: datetime.date):
        months = self.data_repository.get_months_with_data()[date.year]
        for month in months:
            month_str = datetime.date(2000, month, 1).strftime('%B')
            current_month_menu = menu.addMenu(month_str)

            month_date = date.replace(month=month)
            self.add_days_statistics_to_menu(current_month_menu, month_date)

    def add_years_statistics_to_menu(self, menu):
        years = self.data_repository.get_years_with_data()
        for year in years:
            current_year_menu = menu.addMenu(str(year))
            self.add_months_statistics_to_menu(current_year_menu, datetime.date(year, 1, 1))

    def add_statistics_to_menu(self, menu):
        statistics_menu = menu.addMenu("Statistics")
        today_action = statistics_menu.addAction("Today")

        today = datetime.datetime.today()

        try:
            self.add_statistic_actions_to_menu(today_action, today)
            self.add_years_statistics_to_menu(statistics_menu)
        except CodeTimeError as ex:
            self.show_error_message(description=str(ex))

    def show_statics_of_day(self, date: datetime.date):
        image = self.image_creator.create_image(self.data_repository.get_statistics(date))
        self.show_image_preview(image, date)

    def add_statistic_actions_to_menu(self, action, date):
        action.triggered.connect(lambda: self.show_image_preview(date))

    def _on_quit(self):
        self.activity_tracker.on_quit()
        self.app.quit()

    def _on_pause_continue(self):
        if self.activity_tracker.on_pause_continue():
            self.action_pause_continue.setText(TEXT_CONTINUE)
        else:
            self.action_pause_continue.setText(TEXT_PAUSE)

    @staticmethod
    def show_error_message(title="An error occurred", description=None):
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setText(title)
        message.setInformativeText(description)
        message.setWindowTitle("code-time")
        message.setStandardButtons(QMessageBox.Ok)

        message.buttonClicked.connect(lambda: message.hide())
        message.exec_()

    def show_image_preview(self, date: datetime):
        dialog = QDialog()
        dialog.setWindowTitle("Statistics preview")

        layout = QVBoxLayout()

        image = self.image_creator.create_image(self.data_repository.get_statistics(date))
        image = image.resize((image.width // 2, image.height // 2))
        image_view = QPixmap.fromImage(ImageQt(image))

        image_label = QLabel()
        image_label.setPixmap(image_view)

        btn_export = QPushButton("EXPORT AS PNG")
        btn_export.clicked.connect(lambda: self.save_statistic_as_png(date))

        layout.addWidget(image_label)
        layout.addWidget(btn_export)

        dialog.setLayout(layout)
        dialog.exec_()
