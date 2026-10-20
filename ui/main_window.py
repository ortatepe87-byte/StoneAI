from PySide6.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QStackedWidget
)

from ui.pages.dashboard_page import DashboardPage
from ui.pages.camera_page import CameraPage
from ui.pages.analysis_page import AnalysisPage
from ui.pages.dataset_page import DatasetPage
from ui.pages.reports_page import ReportsPage
from ui.pages.training_page import TrainingPage
from ui.pages.settings_page import SettingsPage
from ui.pages.history_page import HistoryPage

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stone AI Professional")
        self.resize(1400, 900)

        self.setStyleSheet("""
        QWidget{
            background:#1e1e1e;
            color:white;
            font-size:14px;
        }

        QPushButton{
            background:#2d2d2d;
            border:none;
            padding:12px;
            text-align:left;
        }

        QPushButton:hover{
            background:#3d3d3d;
        }
        """)

        # SOL MENU

        self.btn_dashboard = QPushButton("🏠 Dashboard")
        self.btn_camera = QPushButton("📷 Kamera")
        self.btn_analysis = QPushButton("🔎 Analiz")
        self.btn_dataset = QPushButton("📚 Veri Seti")
        self.btn_reports = QPushButton("📄 Raporlar")
        self.btn_training = QPushButton("🧠 AI Eğitim")
        self.btn_settings = QPushButton("⚙ Ayarlar")
        self.btn_history = QPushButton(
            "📜 Analiz Geçmişi"
        )
        menu_layout = QVBoxLayout()

        menu_layout.addWidget(self.btn_dashboard)
        menu_layout.addWidget(self.btn_camera)
        menu_layout.addWidget(self.btn_analysis)
        menu_layout.addWidget(self.btn_dataset)
        menu_layout.addWidget(self.btn_history)
        menu_layout.addWidget(self.btn_reports)
        menu_layout.addWidget(self.btn_training)
        menu_layout.addWidget(self.btn_settings) 
        menu_layout.addStretch()

        # SAYFALAR

        self.pages = QStackedWidget()

        self.dashboard_page = DashboardPage()
        self.camera_page = CameraPage()
        self.analysis_page = AnalysisPage()
        self.dataset_page = DatasetPage()
        self.reports_page = ReportsPage()
        self.training_page = TrainingPage()
        self.settings_page = SettingsPage()
        self.history_page = HistoryPage()

        self.pages.addWidget(self.dashboard_page)   # 0
        self.pages.addWidget(self.camera_page)      # 1
        self.pages.addWidget(self.analysis_page)    # 2
        self.pages.addWidget(self.dataset_page)     # 3
        self.pages.addWidget(self.reports_page)     # 4
        self.pages.addWidget(self.training_page)    # 5
        self.pages.addWidget(self.settings_page)    # 6
        self.pages.addWidget(self.history_page)     # 7

        # MENU EVENTLERI

        self.btn_dashboard.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.btn_camera.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.btn_analysis.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.btn_dataset.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        self.btn_reports.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        self.btn_training.clicked.connect(
            lambda: self.pages.setCurrentIndex(5)
        )

        self.btn_settings.clicked.connect(
            lambda: self.pages.setCurrentIndex(6)
        )
        
        self.btn_history.clicked.connect(
            lambda: self.pages.setCurrentIndex(7)
        )
        # ANA LAYOUT

        main_layout = QHBoxLayout()

        main_layout.addLayout(menu_layout, 1)
        main_layout.addWidget(self.pages, 5)

        self.setLayout(main_layout)