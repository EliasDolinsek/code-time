from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QDialog

from src.repositories.code_time_data_repository import CodeTimeDataRepository


class GeneralWidget(QWidget):

    def __init__(self, data_repository: CodeTimeDataRepository, parent: QDialog):
        """Widget containing general settings like username and reset settings."""
        super().__init__()
        self.parent = parent
        self.data_repository = data_repository
        self.layout = QVBoxLayout()

        self.username_label = QLabel()
        self.username_label.setText("Username")

        self.username_field = QLineEdit(self)
        self.username_field.textChanged[str].connect(self.on_username_changed)
        self.display_username()

        self.btn_reset_settings = QPushButton()
        self.btn_reset_settings.setText("RESET SETTINGS")
        self.btn_reset_settings.clicked.connect(self.show_confirm_reset_settings_dialog)

        self.layout.addWidget(self.username_label)
        self.layout.addWidget(self.username_field)
        self.layout.addStretch()
        self.layout.addWidget(self.btn_reset_settings)

        self.setLayout(self.layout)

    def display_username(self):
        self.username_field.setText(self.data_repository.get_setting("username"))

    def on_username_changed(self, value):
        self.data_repository.update_setting("username", value)

    def show_confirm_reset_settings_dialog(self):
        message = QMessageBox()
        message.setIcon(QMessageBox.Question)

        message.setText("Do you really want to reset all settings?")
        message.setInformativeText("This will delete every setting including activities")
        message.setWindowTitle("Reset settings")

        message.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

        self.on_reset_dialog_button_result(message.exec_())

    def on_reset_dialog_button_result(self, result):
        if result == QMessageBox.Ok:
            self.data_repository.reset_settings()
            self.parent.close()
            self.show_settings_reset_dialog()

    @staticmethod
    def show_settings_reset_dialog():
        message = QMessageBox()
        message.setIcon(QMessageBox.Information)

        message.setWindowTitle("Reset settings")
        message.setText("Settings reset successfully")

        message.setStandardButtons(QMessageBox.Ok)
        message.exec_()
