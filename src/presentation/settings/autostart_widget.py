from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from src.use_cases.autostart import CodeTimeAutostart


class AutostartWidget(QWidget):

    def __init__(self, code_time_autostart: CodeTimeAutostart):
        super().__init__()
        self.code_time_autostart = code_time_autostart

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        description = QLabel()
        description.setText("Automatically launch code-time when after you boot your computer")
        self.layout.addWidget(description)

        self.autostart_status = QLabel()
        self.btn_change = QPushButton()

        self.setup_for_autostart_state()

        self.layout.addWidget(self.btn_change)
        self.layout.addWidget(self.autostart_status)

        self.setLayout(self.layout)

    def setup_for_autostart_state(self):
        self.autostart_status.setStyleSheet("color: gray;")
        if self.code_time_autostart.is_enabled():
            self.btn_change.setText("DISABLE AUTOSTART")
            self.autostart_status.setText("Autostart is enabled")
        else:
            self.btn_change.setText("ENABLE AUTOSTART")
            self.autostart_status.setText("Autostart is disabled")

        self.btn_change.clicked.connect(self.toggle_autostart)

    def toggle_autostart(self):
        try:
            if self.code_time_autostart.is_enabled():
                self.code_time_autostart.disable()
            else:
                self.code_time_autostart.enable()
            self.setup_for_autostart_state()
        except Exception as e:
            self.setup_for_autostart_state()
            self.autostart_status.setStyleSheet("color: red;")
            self.autostart_status.setText(str(e))
