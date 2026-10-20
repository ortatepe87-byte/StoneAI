import cv2
import os

from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QComboBox,
    QMessageBox
)

from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QImage, QPixmap


class CameraPage(QWidget):

    def __init__(self):
        super().__init__()

        self.cap = None
        self.current_frame = None

        self.image_label = QLabel("Kamera Kapalı")
        self.image_label.setAlignment(Qt.AlignCenter)

        self.combo_type = QComboBox()

        self.combo_type.addItems([
            "granit",
            "bazalt",
            "kuvars",
            "kalker",
            "mermer",
            "bilinmeyen"
        ])

        self.btn_start = QPushButton("Kamera Aç")
        self.btn_capture = QPushButton("Fotoğraf Çek ve Kaydet")

        self.btn_start.clicked.connect(
            self.start_camera
        )

        self.btn_capture.clicked.connect(
            self.capture_image
        )

        layout = QVBoxLayout()

        layout.addWidget(self.image_label)
        layout.addWidget(self.combo_type)
        layout.addWidget(self.btn_start)
        layout.addWidget(self.btn_capture)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_frame
        )

    def start_camera(self):

        self.cap = cv2.VideoCapture(0)

        self.timer.start(30)

    def update_frame(self):

        if self.cap is None:
            return

        ret, frame = self.cap.read()

        if not ret:
            return

        self.current_frame = frame.copy()

        frame_rgb = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        h, w, ch = frame_rgb.shape

        image = QImage(
            frame_rgb.data,
            w,
            h,
            ch * w,
            QImage.Format_RGB888
        )

        pixmap = QPixmap.fromImage(image)

        self.image_label.setPixmap(
            pixmap.scaled(
                900,
                700,
                Qt.KeepAspectRatio
            )
        )

    def capture_image(self):

        if self.current_frame is None:
            return

        stone_type = self.combo_type.currentText()

        filename = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        ) + ".jpg"

        save_path = os.path.join(
            "data",
            stone_type,
            filename
        )

        cv2.imwrite(
            save_path,
            self.current_frame
        )

        QMessageBox.information(
            self,
            "Başarılı",
            f"Kaydedildi:\n{save_path}"
        )