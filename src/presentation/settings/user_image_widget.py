from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton

from src.repositories.code_time_data_repository import CodeTimeDataRepository


class UserImageWidget(QWidget):
    IMAGE_WIDTH = 256

    def __init__(self, data_repository: CodeTimeDataRepository):
        super().__init__()
        self.data_repository = data_repository

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.image_label = QLabel()

        image_pixmap = self.get_user_image_pixmap()
        image_pixmap = image_pixmap.scaledToWidth(self.IMAGE_WIDTH)
        self.image_label.setPixmap(image_pixmap)

        self.layout.addWidget(self.image_label)
        self.layout.addLayout(self.get_buttons_layout())

        self.setLayout(self.layout)

    def get_buttons_layout(self):
        layout = QHBoxLayout()

        btn_change = QPushButton("CHANGE")
        btn_remove = QPushButton("REMOVE")

        layout.addWidget(btn_change)
        layout.addWidget(btn_remove)

        return layout

    def get_user_image_pixmap(self):
        return QPixmap(self.data_repository.get_config()["user_image"])
