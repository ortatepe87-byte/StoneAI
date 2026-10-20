from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QPushButton,
    QMessageBox
)

from core.database import db


class HistoryPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel(
            "📜 ANALİZ GEÇMİŞİ"
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

        self.table = QTableWidget()

        self.table.setColumnCount(4)

        self.table.setHorizontalHeaderLabels([
            "ID",
            "Taş Türü",
            "Güven %",
            "Tarih"
        ])

        self.table.cellDoubleClicked.connect(
            self.show_detail
        )

        layout.addWidget(
            self.table
        )

        buttons = QHBoxLayout()

        self.btn_refresh = QPushButton(
            "🔄 Yenile"
        )

        self.btn_delete = QPushButton(
            "🗑 Seçili Kaydı Sil"
        )

        self.btn_clear = QPushButton(
            "🔥 Tüm Geçmişi Temizle"
        )

        self.btn_refresh.clicked.connect(
            self.load_history
        )

        self.btn_delete.clicked.connect(
            self.delete_selected
        )

        self.btn_clear.clicked.connect(
            self.clear_history
        )

        buttons.addWidget(
            self.btn_refresh
        )

        buttons.addWidget(
            self.btn_delete
        )

        buttons.addWidget(
            self.btn_clear
        )

        layout.addLayout(
            buttons
        )

        self.setLayout(layout)

        self.load_history()

    def load_history(self):

        rows = db.get_last_analyses()

        self.info_label.setText(
            f"Toplam Analiz: {len(rows)}"
        )

        self.table.setRowCount(
            len(rows)
        )

        for row_index, row in enumerate(rows):

            self.table.setItem(
                row_index,
                0,
                QTableWidgetItem(str(row[0]))
            )

            self.table.setItem(
                row_index,
                1,
                QTableWidgetItem(str(row[1]))
            )

            self.table.setItem(
                row_index,
                2,
                QTableWidgetItem(str(row[2]))
            )

            self.table.setItem(
                row_index,
                3,
                QTableWidgetItem(str(row[3]))
            )

        self.table.resizeColumnsToContents()

    def show_detail(self, row, column):

        analysis_id = int(
            self.table.item(row, 0).text()
        )

        data = db.get_analysis_by_id(
            analysis_id
        )

        if not data:
            return

        QMessageBox.information(
            self,
            "Analiz Detayı",
            f"""
ID: {data[0]}

Taş Türü:
{data[1]}

Güven:
%{data[2]}

RGB:
{data[3]}

Not:
{data[4]}

Tarih:
{data[5]}
"""
        )

    def delete_selected(self):

        row = self.table.currentRow()

        if row < 0:
            return

        analysis_id = int(
            self.table.item(row, 0).text()
        )

        answer = QMessageBox.question(
            self,
            "Onay",
            "Seçili kayıt silinsin mi?"
        )

        if answer == QMessageBox.StandardButton.Yes:

            db.delete_analysis(
                analysis_id
            )

            self.load_history()

    def clear_history(self):

        answer = QMessageBox.question(
            self,
            "Onay",
            "Tüm geçmiş silinsin mi?"
        )

        if answer == QMessageBox.StandardButton.Yes:

            db.clear_history()

            self.load_history()