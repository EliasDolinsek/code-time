import datetime

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from src.watcher.data_manager import get_available_years, get_available_months, read_month_data
from src.watcher.statistics.image_creator import ImageCreator

TEXT_PAUSE = "Pause tracking"
TEXT_CONTINUE = "Continue tracking"


class TrayHandler:

    def __init__(self, image_creator: ImageCreator, on_pause_continue, on_quit):
        super().__init__()
        self.image_creator = image_creator

        self.action_pause_continue = QAction(TEXT_PAUSE)
        self.action_quit = QAction("Quit")

        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)

        self.provided_on_pause_continue = on_pause_continue
        self.provided_on_quit = on_quit

    def start(self):
        icon = QIcon("assets/clock.svg")

        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()

        self.action_quit.triggered.connect(lambda x: self._on_quit(self.provided_on_quit))
        self.action_pause_continue.triggered.connect(lambda x: self._on_pause_continue(self.provided_on_pause_continue))

        menu.addAction(self.action_pause_continue)
        self.add_statistics_to_menu(menu)
        menu.addAction(self.action_quit)

        tray.setContextMenu(menu)
        self.app.exec_()

    def save_statistic_as_png(self, statistics):
        QFileDialog.saveFileContent("Test")

    def add_days_statistics_to_menu(self, menu, year, month):
        month_data = read_month_data(month, year)
        for day in month_data["activity"]:
            day_menu = menu.addMenu(str(day))
            self.add_statistic_actions_to_menu(day_menu)

    def add_months_statistics_to_menu(self, menu, year):
        months = get_available_months(year)
        for month in months:
            month_str = datetime.date(2000, month, 1).strftime('%B')
            current_month_menu = menu.addMenu(month_str)
            self.add_days_statistics_to_menu(current_month_menu, year, month)

    def add_years_statistics_to_menu(self, menu):
        years = get_available_years()
        for year in years:
            current_year_menu = menu.addMenu(year)
            self.add_months_statistics_to_menu(current_year_menu, year)

    def add_statistics_to_menu(self, menu):
        statistics_menu = menu.addMenu("Statistics")
        today_menu = statistics_menu.addMenu("Today")

        self.add_statistic_actions_to_menu(today_menu)
        self.add_years_statistics_to_menu(statistics_menu)

    def add_statistic_actions_to_menu(self, menu):
        menu.addAction("Show")
        menu.addAction("Export as PNG")


def _on_quit(self, on_quit):
    on_quit()
    self.app.quit()


def _on_pause_continue(self, on_pause_continue):
    if on_pause_continue():
        self.action_pause_continue.setText(TEXT_CONTINUE)
    else:
        self.action_pause_continue.setText(TEXT_PAUSE)
