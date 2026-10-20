import os

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QComboBox,
    QListWidget,
    QPushButton,
    QMessageBox
)

from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

from core.dataset_stats import DatasetStats


class DatasetPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.title = QLabel(
            "VERI SETI YONETIMI"
        )

        self.layout.addWidget(
            self.title
        )

        self.combo = QComboBox()

        self.combo.addItems([
            "granit",
            "bazalt",
            "kuvars",
            "kalker",
            "mermer",
            "bilinmeyen"
        ])

        self.combo.currentTextChanged.connect(
            self.load_images
        )

        self.layout.addWidget(
            self.combo
        )

        self.count_label = QLabel()

        self.layout.addWidget(
            self.count_label
        )

        content = QHBoxLayout()

        self.image_list = QListWidget()

        self.image_list.currentTextChanged.connect(
            self.preview_image
        )

        content.addWidget(
            self.image_list
        )

        self.preview = QLabel(
            "Önizleme"
        )

        self.preview.setAlignment(
            Qt.AlignCenter
        )

        content.addWidget(
            self.preview
        )

        self.layout.addLayout(content)

        self.btn_delete = QPushButton(
            "Seçilen Resmi Sil"
        )

        self.btn_delete.clicked.connect(
            self.delete_image
        )

        self.layout.addWidget(
            self.btn_delete
        )

        self.setLayout(self.layout)

        self.load_images()
    
    
    def load_images(self):

        self.image_list.clear()

        stone_type = (
            self.combo.currentText()
        )

        folder = os.path.join(
            "data",
            stone_type
        )

        if not os.path.exists(folder):
            return

        files = sorted(
            os.listdir(folder)
        )

        images = [
            f for f in files
            if f.lower().endswith(
                (".jpg", ".jpeg", ".png")
            )
        ]

        self.count_label.setText(
            f"Fotoğraf Sayısı : {len(images)}"
        )

        self.image_list.addItems(
            images
        )

    def preview_image(self, filename):

        if not filename:
            return

        stone_type = (
            self.combo.currentText()
        )

        path = os.path.join(
            "data",
            stone_type,
            filename
        )

        pixmap = QPixmap(path)

        self.preview.setPixmap(
            pixmap.scaled(
                500,
                500,
                Qt.KeepAspectRatio
            )
        )

    def delete_image(self):

        item = self.image_list.currentItem()

        if not item:
            return

        stone_type = (
            self.combo.currentText()
        )

        path = os.path.join(
            "data",
            stone_type,
            item.text()
        )

        try:

            os.remove(path)

            QMessageBox.information(
                self,
                "Başarılı",
                "Resim silindi."
            )

            self.load_images()

        except Exception as e:

            QMessageBox.warning(
                self,
                "Hata",
                str(e)
            )