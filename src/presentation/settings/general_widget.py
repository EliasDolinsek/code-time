from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

from src.repositories.code_time_data_repository import CodeTimeDataRepository


class GeneralWidget(QWidget):

    def __init__(self, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.data_repository = data_repository
        self.layout = QVBoxLayout()

        self.username_label = QLabel()
        self.username_label.setText("Username")

        self.username_field = QLineEdit(self)
        self.username_field.textChanged[str].connect(self.on_username_changed)
        self.display_username()

        self.btn_reset_settings = QPushButton()
        self.btn_reset_settings.setText("RESET SETTINGS")

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_field)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_reset_settings)

        self.setLayout(self.layout)

    def display_username(self):
        self.username_field.setText(self.data_repository.get_setting("username"))

    def on_username_changed(self, value):
        self.data_repository.update_setting("username", value)
