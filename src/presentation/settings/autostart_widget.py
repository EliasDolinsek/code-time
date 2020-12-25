from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from src.use_cases.autostart import AutostartManager


class AutostartWidget(QWidget):

    def __init__(self, autostart_manager: AutostartManager):
        super().__init__()
        self.autostart_manager = autostart_manager

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        description = QLabel()
        description.setText("Automatically launch code-time when after you boot your computer")
        self.layout.addWidget(description)

        self.autostart_status = QLabel()
        self.btn_change = QPushButton()
        self.btn_change.clicked.connect(self.toggle_autostart)

        self.setup_for_autostart_state()

        self.layout.addWidget(self.autostart_status)
        self.layout.addWidget(self.btn_change)

        self.setLayout(self.layout)

    def setup_for_autostart_state(self):
        self.autostart_status.setStyleSheet("color: gray;")
        if self.autostart_manager.is_enabled():
            self.btn_change.setText("DISABLE AUTOSTART")
            self.autostart_status.setText("Autostart is enabled")
        else:
            self.btn_change.setText("ENABLE AUTOSTART")
            self.autostart_status.setText("Autostart is disabled")

    def toggle_autostart(self):
        try:
            if self.autostart_manager.is_enabled():
                self.autostart_manager.disable()
            else:
                self.autostart_manager.enable()
            self.setup_for_autostart_state()
        except Exception as e:
            self.setup_for_autostart_state()
            self.autostart_status.setStyleSheet("color: red;")
            self.autostart_status.setText(str(e))
