import os

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QTextEdit
)

from core.database import db
from core.dataset_stats import DatasetStats


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        title = QLabel("📊 STONE AI PROFESSIONAL")
        title.setAlignment(Qt.AlignCenter)

        title.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            padding:15px;
        """)

        main_layout.addWidget(title)

        cards_layout = QHBoxLayout()

        self.dataset_card = QLabel()
        self.analysis_card = QLabel()
        self.report_card = QLabel()
        self.health_card = QLabel()

        cards = [
            self.dataset_card,
            self.analysis_card,
            self.report_card,
            self.health_card
        ]

        for card in cards:

            card.setAlignment(Qt.AlignCenter)
            card.setMinimumHeight(120)

            card.setStyleSheet("""
                background:#252525;
                border-radius:12px;
                padding:15px;
                font-size:18px;
                font-weight:bold;
            """)

            cards_layout.addWidget(card)

        main_layout.addLayout(cards_layout)

        self.most_detected_label = QLabel()

        self.most_detected_label.setStyleSheet("""
            background:#252525;
            padding:20px;
            border-radius:10px;
            font-size:16px;
        """)

        main_layout.addWidget(self.most_detected_label)

        self.last_analysis_label = QLabel()

        self.last_analysis_label.setStyleSheet("""
            background:#252525;
            padding:20px;
            border-radius:10px;
            font-size:16px;
        """)

        main_layout.addWidget(self.last_analysis_label)

        self.dataset_graph = QTextEdit()
        self.dataset_graph.setReadOnly(True)

        self.dataset_graph.setStyleSheet("""
            background:#252525;
            border-radius:10px;
            padding:10px;
        """)

        main_layout.addWidget(self.dataset_graph)

        self.btn_refresh = QPushButton(
            "🔄 Dashboard Yenile"
        )

        self.btn_refresh.clicked.connect(
            self.load_dashboard
        )

        main_layout.addWidget(self.btn_refresh)

        self.setLayout(main_layout)

        self.load_dashboard()

    def load_dashboard(self):

        stats = DatasetStats.get_stats()

        total_dataset = stats.get("total", 0)

        analysis_count = db.get_analysis_count()

        try:

            report_count = len([
                f for f in os.listdir("reports")
                if f.lower().endswith(".pdf")
            ])

        except:

            report_count = 0

        health = min(
            int((total_dataset / 500) * 100),
            100
        )

        self.dataset_card.setText(
            f"📚 DATASET\n\n{total_dataset}"
        )

        self.analysis_card.setText(
            f"🔎 ANALİZ\n\n{analysis_count}"
        )

        self.report_card.setText(
            f"📄 RAPOR\n\n{report_count}"
        )

        self.health_card.setText(
            f"❤️ SAĞLIK\n\n%{health}"
        )

        most_detected = db.get_most_detected()

        if most_detected:

            self.most_detected_label.setText(
                f"""
🏆 EN ÇOK BULUNAN TAŞ

Tür:
{most_detected[0]}

Toplam:
{most_detected[1]}
"""
            )

        else:

            self.most_detected_label.setText(
                "🏆 Henüz analiz yapılmadı"
            )

        last = db.get_last_analysis()

        if last:

            self.last_analysis_label.setText(
                f"""
📌 SON ANALİZ

Taş Türü:
{last[0]}

Güven:
%{last[1]}

Tarih:
{last[2]}
"""
            )

        else:

            self.last_analysis_label.setText(
                "📌 Henüz analiz yok"
            )

        graph_text = ""

        for stone in [
            "kuvars",
            "granit",
            "mermer",
            "bazalt",
            "kalker"
        ]:

            count = stats.get(stone, 0)

            graph = "█" * min(count, 25)

            graph_text += (
                f"{stone:<10} {graph} ({count})\n"
            )

        self.dataset_graph.setPlainText(
            graph_text
        )