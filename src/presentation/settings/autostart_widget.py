from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton


class AutostartWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        description = QLabel()
        description.setText("Automatically launch code-time when after you boot your computer")
        self.layout.addWidget(description)

        autostart_status = QLabel()
        autostart_status.setText("Autostart is not available")
        autostart_status.setStyleSheet("color: red;")
        self.layout.addWidget(autostart_status)

        btn_change = QPushButton()
        btn_change.setText("ENABLE AUTOSTART")
        btn_change.setEnabled(False)
        self.layout.addWidget(btn_change)

        self.setLayout(self.layout)
