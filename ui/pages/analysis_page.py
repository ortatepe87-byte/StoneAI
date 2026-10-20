from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QFileDialog,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt
from core.quality import calculate_quality
from ultralytics import YOLO
from core.pdf_report import create_report
from core.database import db
import cv2
import shutil
import os
import webbrowser

class AnalysisPage(QWidget):

    def __init__(self):
        super().__init__()

        self.model = None

        self.image_label = QLabel("Taş Fotoğrafı")
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setMinimumWidth(600)

        self.result_label = QTextEdit()

        self.result_label.setReadOnly(True)

        self.result_label.setText(
            "Analiz Bekleniyor..."
        )

        self.result_label.setStyleSheet("""
        font-size:16px;
        font-weight:bold;
        padding:10px;
        background:#252525;
        border-radius:10px;
        """)


        self.btn_open = QPushButton(
            "📷 Fotoğraf Seç ve Analiz Et"
        )

        self.btn_open.clicked.connect(
            self.open_and_analyze
        )
      
        self.btn_pdf = QPushButton(
            "📄 PDF Rapor Oluştur"
        )

        self.btn_pdf.clicked.connect(
            self.create_pdf
        )

        self.btn_web_search = QPushButton(
            "🌍 İnternette Araştır"
        )

        self.btn_web_search.clicked.connect(
            self.web_research
        )

        content_layout = QHBoxLayout()

        content_layout.addWidget(
            self.image_label,
            2
        )

        content_layout.addWidget(
            self.result_label,
            1
        )

        main_layout = QVBoxLayout()

        main_layout.addLayout(
            content_layout
        )

        main_layout.addWidget(
            self.btn_open
        )

        main_layout.addWidget(
            self.btn_pdf
        )

        main_layout.addWidget(
            self.btn_web_search
        )

        content_widget = QWidget()

        content_widget.setLayout(
            main_layout
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        scroll.setWidget(
            content_widget
        )

        outer_layout = QVBoxLayout()

        outer_layout.addWidget(
            scroll
        )

        self.setLayout(
            outer_layout
        
        )
     
    def web_research(self):

        if not hasattr(self, "last_class"):

            self.result_label.setText(
                "⚠ Önce analiz yapın."
            )

            return

        stone = self.last_class

        url = (
            "https://www.google.com/search?q="
            f"{stone}+stone+mineral+rock"
        )

        webbrowser.open(url)
    def create_pdf(self):

        if not hasattr(self, "last_class"):

            self.result_label.setText(
                "⚠ Önce bir analiz yapın."
            )

            return

        path = create_report(
            self.last_image,
            self.last_class,
            self.last_conf,
            self.last_rgb,
            self.last_hardness,
            self.last_value,
            self.last_usage,
            self.last_quality
        )

        self.result_label.setText(
            self.result_label.text()
            + f"\n\n✅ PDF Oluşturuldu\n{path}"
        )

    def open_and_analyze(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Fotoğraf Seç",
            "",
            "Images (*.jpg *.jpeg *.png)"
        )

        if not file_name:
            return

        pixmap = QPixmap(file_name)

        self.image_label.setPixmap(
            pixmap.scaled(
                600,
                500,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
        )

        if self.model is None:

            self.result_label.setText(
                "Model yükleniyor..."
            )

            self.model = YOLO(
                "models/stone_v1.pt"
            )

        results = self.model(file_name)

        probs = results[0].probs

        top1_id = int(probs.top1)
        top1_conf = float(probs.top1conf)

        unknown_stone = False

        if top1_conf < 0.65:

            unknown_stone = True

            os.makedirs(
                "dataset/unknown",
                exist_ok=True
            )

            try:

                shutil.copy(
                    file_name,
                    os.path.join(
                        "dataset",
                        "unknown",
                        os.path.basename(file_name)
                    )
                )

            except Exception:
                pass

        top5_ids = probs.top5
        top5_confs = probs.top5conf.tolist()

        class_name = self.model.names[top1_id]

        image = cv2.imread(file_name)

        if image is None:

            self.result_label.setText(
                "Fotoğraf okunamadı."
            )

            return
        avg_color = image.mean(axis=0).mean(axis=0)

        b = int(avg_color[0])
        g = int(avg_color[1])
        r = int(avg_color[2])

        rgb_text = f"{r}, {g}, {b}"

        quality_score = calculate_quality(
            file_name
        )

        second_text = ""
        third_text = ""

        if len(top5_ids) > 1:

            second_text = (
                f"{self.model.names[top5_ids[1]]} "
                f"(%{top5_confs[1] * 100:.2f})"
            )

        if len(top5_ids) > 2:

            third_text = (
                f"{self.model.names[top5_ids[2]]} "
                f"(%{top5_confs[2] * 100:.2f})"
            )

        info = {

            "kuvars": {
                "sertlik": "7",
                "deger": "50-150 TL",
                "kullanim": "Takı, Dekorasyon"
            },

            "granit": {
                "sertlik": "6-7",
                "deger": "20-100 TL",
                "kullanim": "Yapı Taşı"
            },

            "bazalt": {
                "sertlik": "6",
                "deger": "20-80 TL",
                "kullanim": "Peyzaj"
            },

            "mermer": {
                "sertlik": "3-4",
                "deger": "50-250 TL",
                "kullanim": "Dekorasyon"
            },

            "kalker": {
                "sertlik": "3",
                "deger": "10-50 TL",
                "kullanim": "İnşaat"
            }
        }

        detay = info.get(
            class_name.lower(),
            {
                "sertlik": "?",
                "deger": "?",
                "kullanim": "Bilinmiyor"
            }
        )

        self.last_image = file_name
        self.last_class = class_name
        self.last_conf = round(
            top1_conf * 100,
            2
        )
        self.last_rgb = rgb_text
        self.last_hardness = detay["sertlik"]
        self.last_value = detay["deger"]
        self.last_usage = detay["kullanim"]
        self.last_quality = quality_score

        db.add_analysis(
            image_path=file_name,
            stone_type=class_name,
            confidence=round(
                top1_conf * 100,
                2
            ),
            color=rgb_text,
            note="StoneAI Analizi"
        )

        unknown_text = ""

        if unknown_stone:

            unknown_text = """

⚠ BİLİNMEYEN TAŞ

Bu taş veri setinde bulunamadı.

🌍 İleride internet analizi önerilir.

📁 dataset/unknown klasörüne kaydedildi.
"""

        self.result_label.setText(
            f"""
🪨 TAŞ TÜRÜ

{class_name.upper()}

🎯 GÜVEN

%{top1_conf * 100:.2f}

🥈 2. TAHMİN

{second_text}

🥉 3. TAHMİN

{third_text}

💎 SERTLİK

{detay['sertlik']}

⭐ KALİTE PUANI

{quality_score}/10

🎨 RGB

{rgb_text}

💰 TAHMİNİ DEĞER

{detay['deger']}

🏗 KULLANIM

{detay['kullanim']}

{unknown_text}
"""
        )  