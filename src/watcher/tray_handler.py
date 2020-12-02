from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

TEXT_PAUSE = "Pause tracking"
TEXT_CONTINUE = "Continue tracking"


class TrayHandler:

    def __init__(self):
        self.app = QApplication([])
        self.app.setQuitOnLastWindowClosed(False)
        self.action_pause_continue = QAction(TEXT_PAUSE)
        self.action_quit = QAction("Quit")

    def setup_tray_menu(self, on_pause_continue, on_quit):
        icon = QIcon("assets/clock.svg")

        tray = QSystemTrayIcon()
        tray.setIcon(icon)
        tray.setVisible(True)

        menu = QMenu()

        self.action_quit.triggered.connect(lambda x: self._on_quit(on_quit))
        self.action_pause_continue.triggered.connect(lambda x: self._on_pause_continue(on_pause_continue))

        menu.addAction(self.action_pause_continue)
        menu.addAction(self.action_quit)

        tray.setContextMenu(menu)
        self.app.exec()

    def _on_quit(self, on_quit):
        on_quit()
        self.app.quit()

    def _on_pause_continue(self, on_pause_continue):
        if on_pause_continue():
            self.action_pause_continue.setText(TEXT_CONTINUE)
        else:
            self.action_pause_continue.setText(TEXT_PAUSE)
