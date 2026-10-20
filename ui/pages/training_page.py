from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QMessageBox
)

from core.ai.trainer import Trainer


class TrainingPage(QWidget):

    def __init__(self):
        super().__init__()

        score, counts = Trainer.dataset_health()

        layout = QVBoxLayout()

        title = QLabel(
            "🧠 STONE AI EGITIM MERKEZI"
        )

        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        layout.addWidget(title)

        layout.addWidget(
            QLabel(
                f"Dataset Saglik Skoru : %{score}"
            )
        )

        total = sum(counts.values())

        layout.addWidget(
            QLabel(
                f"Toplam Veri : {total}"
            )
        )

        eksik = []

        for cls, count in counts.items():

            if count < 100:
                eksik.append(
                    f"{cls} ({count})"
                )

        if eksik:

            layout.addWidget(
                QLabel(
                    "Eksik Siniflar:"
                )
            )

            for item in eksik:

                layout.addWidget(
                    QLabel(
                        f"❌ {item}"
                    )
                )

        else:

            layout.addWidget(
                QLabel(
                    "✅ Tum siniflar hazir"
                )
            )

        self.train_button = QPushButton(
            "STONE V1 EGIT"
        )

        self.train_button.clicked.connect(
            self.start_training
        )

        layout.addWidget(
            self.train_button
        )

        layout.addStretch()

        self.setLayout(layout)

    def start_training(self):

        QMessageBox.information(
            self,
            "Bilgi",
            "Gercek YOLO egitimi sonraki adimda baglanacak."
        )