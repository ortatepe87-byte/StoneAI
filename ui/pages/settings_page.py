from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QMessageBox
)

from core.database import db


class SettingsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("⚙ AYARLAR")

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(title)

        self.info_label = QLabel(
            """
StoneAI Professional v1.1

Sistem Durumu:
✅ Veritabanı
✅ Yapay Zeka Modeli
✅ PDF Raporlama
✅ Analiz Geçmişi
            """
        )

        layout.addWidget(
            self.info_label
        )

        self.btn_clear_history = QPushButton(
            "🗑 Analiz Geçmişini Temizle"
        )

        self.btn_clear_history.clicked.connect(
            self.clear_history
        )

        layout.addWidget(
            self.btn_clear_history
        )

        self.btn_about = QPushButton(
            "ℹ Hakkında"
        )

        self.btn_about.clicked.connect(
            self.show_about
        )

        layout.addWidget(
            self.btn_about
        )

        layout.addStretch()

        self.setLayout(layout)

    def clear_history(self):

        answer = QMessageBox.question(
            self,
            "Onay",
            "Tüm analiz geçmişi silinsin mi?"
        )

        if answer == QMessageBox.StandardButton.Yes:

            db.clear_history()

            QMessageBox.information(
                self,
                "Başarılı",
                "Analiz geçmişi temizlendi."
            )

    def show_about(self):

        QMessageBox.information(
            self,
            "StoneAI Professional",
            """
StoneAI Professional

Versiyon: 1.1

Özellikler:

• Taş Analizi
• RGB Analizi
• Kalite Puanı
• PDF Raporlama
• Analiz Geçmişi
• Veri Seti Yönetimi
• Yapay Zeka Eğitimi
"""
        )