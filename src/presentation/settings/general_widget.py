from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton


class GeneralWidget(QWidget):

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.username_label = QLabel()
        self.username_label.setText("Username")

        self.username_field = QLineEdit(self)
        self.username_field.textChanged[str].connect(self.on_username_changed)

        self.btn_reset_settings = QPushButton()
        self.btn_reset_settings.setText("RESET SETTINGS")

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_field)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_reset_settings)

        self.setLayout(self.layout)

    def on_username_changed(self, value):
        print(value)
