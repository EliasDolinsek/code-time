import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.repositories.code_time_data_repository import CodeTimeDataRepository
from src.use_cases.activity_tracker import ActivityTracker
from src.use_cases.image_creator import ImageCreator

TEXT_PAUSE = "Pause tracking"
TEXT_CONTINUE = "Continue tracking"


class TrayHandler:

    def __init__(self, image_creator: ImageCreator, activity_tracker: ActivityTracker,
                 data_repository: CodeTimeDataRepository):
        super().__init__()
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
        menu.addAction(self.action_quit)

        tray.setContextMenu(menu)
        self.app.exec_()

    def save_statistic_as_png(self, statistics):
        QFileDialog.saveFileContent("Test")

    def add_days_statistics_to_menu(self, menu, year, month):
        days = self.data_repository.get_days_with_data()[year][month]
        for day in days:
            day_menu = menu.addMenu(str(day))
            self.add_statistic_actions_to_menu(day_menu)

    def add_months_statistics_to_menu(self, menu, year):
        months = self.data_repository.get_months_with_data()[year]
        for month in months:
            month_str = datetime.date(2000, month, 1).strftime('%B')
            current_month_menu = menu.addMenu(month_str)
            self.add_days_statistics_to_menu(current_month_menu, year, month)

    def add_years_statistics_to_menu(self, menu):
        years = self.data_repository.get_years_with_data()
        for year in years:
            current_year_menu = menu.addMenu(str(year))
            self.add_months_statistics_to_menu(current_year_menu, year)

    def add_statistics_to_menu(self, menu):
        statistics_menu = menu.addMenu("Statistics")
        today_menu = statistics_menu.addMenu("Today")

        self.add_statistic_actions_to_menu(today_menu)
        self.add_years_statistics_to_menu(statistics_menu)

    def add_statistic_actions_to_menu(self, menu):
        menu.addAction("Show")
        menu.addAction("Export as PNG")

    def _on_quit(self):
        self.activity_tracker.on_quit()
        self.app.quit()

    def _on_pause_continue(self):
        if self.activity_tracker.on_pause_continue():
            self.action_pause_continue.setText(TEXT_CONTINUE)
        else:
            self.action_pause_continue.setText(TEXT_PAUSE)
