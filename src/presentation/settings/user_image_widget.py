import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileDialog

from src.repositories.code_time_data_repository import CodeTimeDataRepository


class UserImageWidget(QWidget):
    IMAGE_WIDTH = 256

    def __init__(self, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.data_repository = data_repository
        self.layout = QVBoxLayout()

        # Description label
        description = QLabel()
        description.setText("Change your user image or replace it with the default one by removing it.\nNote that your "
                            "image will be scaled down to a eqal width to height ratio.")
        description.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(description)

        # Image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)

        self.load_user_image()
        self.layout.addWidget(self.image_label)

        # Buttons
        self.layout.addLayout(self.get_buttons_layout())

        self.setLayout(self.layout)

    def get_buttons_layout(self):
        layout = QHBoxLayout()

        btn_change = QPushButton("CHANGE")
        btn_change.clicked.connect(self.on_change)
        btn_remove = QPushButton("REMOVE")
        btn_remove.clicked.connect(self.on_remove)

        layout.addWidget(btn_change)
        layout.addWidget(btn_remove)

        return layout

    def on_change(self):
        result = QFileDialog.getOpenFileName(self, "Select user image", self.get_user_image_path(), "Image (*.png)")
        selected_file = result[0]
        if selected_file != "":
            self.data_repository.update_setting("user_image", selected_file)
            self.load_user_image()

    def on_remove(self):
        self.data_repository.update_setting("user_image", "default_user.png")
        self.load_user_image()

    def load_user_image(self):
        image_pixmap = self.get_user_image_pixmap()
        image_pixmap = image_pixmap.scaled(256, 256)
        self.image_label.setPixmap(image_pixmap)

    def get_user_image_pixmap(self):
        return QPixmap(self.get_user_image_path())

    def get_user_image_path(self):
        return self.data_repository.get_file_from_setting("user_image")
