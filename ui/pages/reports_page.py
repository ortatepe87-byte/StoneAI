import os

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QMessageBox
)


class ReportsPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel(
            "📄 RAPOR MERKEZİ"
        )

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
            padding:10px;
        """)

        layout.addWidget(title)

        self.info_label = QLabel()

        layout.addWidget(
            self.info_label
        )

        self.report_list = QListWidget()

        self.report_list.itemDoubleClicked.connect(
            self.open_report
        )

        layout.addWidget(
            self.report_list
        )

        buttons = QHBoxLayout()

        self.btn_refresh = QPushButton(
            "🔄 Yenile"
        )

        self.btn_open = QPushButton(
            "👁 Raporu Aç"
        )

        self.btn_delete = QPushButton(
            "🗑 Raporu Sil"
        )

        self.btn_delete_all = QPushButton(
            "🔥 Tümünü Sil"
        )

        self.btn_folder = QPushButton(
            "📂 Klasörü Aç"
        )

        self.btn_refresh.clicked.connect(
            self.load_reports
        )

        self.btn_open.clicked.connect(
            self.open_report
        )

        self.btn_delete.clicked.connect(
            self.delete_report
        )

        self.btn_delete_all.clicked.connect(
            self.delete_all_reports
        )

        self.btn_folder.clicked.connect(
            self.open_folder
        )

        buttons.addWidget(self.btn_refresh)
        buttons.addWidget(self.btn_open)
        buttons.addWidget(self.btn_delete)
        buttons.addWidget(self.btn_delete_all)
        buttons.addWidget(self.btn_folder)

        layout.addLayout(buttons)

        self.setLayout(layout)

        self.load_reports()

    def load_reports(self):

        self.report_list.clear()

        os.makedirs(
            "reports",
            exist_ok=True
        )

        files = sorted(
            os.listdir("reports"),
            reverse=True
        )

        reports = [
            f for f in files
            if f.lower().endswith(".pdf")
        ]

        self.info_label.setText(
            f"Toplam PDF Raporu: {len(reports)}"
        )

        self.report_list.addItems(
            reports
        )

    def open_report(self):

        item = self.report_list.currentItem()

        if not item:
            return

        path = os.path.join(
            "reports",
            item.text()
        )

        if os.path.exists(path):
            os.startfile(path)

    def delete_report(self):

        item = self.report_list.currentItem()

        if not item:
            return

        path = os.path.join(
            "reports",
            item.text()
        )

        try:

            os.remove(path)

            self.load_reports()

            QMessageBox.information(
                self,
                "Başarılı",
                "Rapor silindi."
            )

        except Exception as e:

            QMessageBox.warning(
                self,
                "Hata",
                str(e)
            )

    def delete_all_reports(self):

        answer = QMessageBox.question(
            self,
            "Onay",
            "Tüm PDF raporları silinsin mi?"
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        for file in os.listdir("reports"):

            if file.lower().endswith(".pdf"):

                try:

                    os.remove(
                        os.path.join(
                            "reports",
                            file
                        )
                    )

                except:
                    pass

        self.load_reports()

        QMessageBox.information(
            self,
            "Başarılı",
            "Tüm raporlar silindi."
        )

    def open_folder(self):

        os.makedirs(
            "reports",
            exist_ok=True
        )

        os.startfile("reports")