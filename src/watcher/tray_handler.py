from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

TEXT_PAUSE = "Pause tracking"
TEXT_CONTINUE = "Continue tracking"


class TrayHandler:

    def __init__(self, on_pause_continue, on_quit):
        super().__init__()
        self.action_quit = QAction("Quit")
        self.action_pause_continue = QAction(TEXT_PAUSE)

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
        menu.addAction(self.action_quit)

        tray.setContextMenu(menu)
        self.app.exec_()

    def _on_quit(self, on_quit):
        on_quit()
        self.app.quit()

    def _on_pause_continue(self, on_pause_continue):
        if on_pause_continue():
            self.action_pause_continue.setText(TEXT_CONTINUE)
        else:
            self.action_pause_continue.setText(TEXT_PAUSE)
