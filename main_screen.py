import sys
import io
from contextlib import redirect_stdout
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal, QThread, QObject
from PySide6.QtGui import QFont, QPalette, QColor, QMovie
from PySide6.QtCore import QSize

class StatusSignal(QObject):
    status_changed = Signal(str)

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calliope Voice Assistant")
        self.setFixedSize(700, 600)
        self.setup_ui()
        self.setup_status_signal()
        
        self.setWindowState(Qt.WindowActive)
        self.raise_()
        self.activateWindow()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)
        
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 40))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        layout.addStretch()
        
        self.title_label = QLabel("Caliope")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Trebuchet MS", 40, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #b174e7;")
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        
        self.indicator_label = QLabel()
        self.indicator_label.setAlignment(Qt.AlignCenter)
        self.indicator_label.setFixedSize(150, 150)
        self.indicator_label.setStyleSheet("background-color: transparent;")
        
        self.listening_movie = QMovie("assets/listening.gif")
        self.listening_movie.setScaledSize(QSize(150, 150))
        
        self.responding_movie = QMovie("assets/responding.gif")
        self.responding_movie.setScaledSize(QSize(150, 150))
        
        self.indicator_label.setMovie(self.listening_movie)
        self.listening_movie.start()
        
        layout.addWidget(self.indicator_label, alignment=Qt.AlignCenter)
        
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Arial", 28, QFont.Bold)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #FFFFFF; margin-top: 20px;")
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        info_font = QFont("Arial", 16)
        self.info_label.setFont(info_font)
        self.info_label.setStyleSheet("color: #90EE90; margin-top: 20px;")
        layout.addWidget(self.info_label, alignment=Qt.AlignCenter)
        
        layout.addStretch()

    def setup_status_signal(self):
        self.status_signal = StatusSignal()
        self.status_signal.status_changed.connect(self.update_status)
    
    def update_status(self, status_text):
        if "|" in status_text:
            status, info = status_text.split("|", 1)
            status = status.strip().upper()
            info = info.strip()
        else:
            status = status_text.strip().upper()
            info = ""
        
        self.status_label.setText(status)
        self.info_label.setText(info)
        
        if status == "RESPONDING" or "POEM" in status or status == "RESPONDING":
            self.listening_movie.stop()
            self.indicator_label.setMovie(self.responding_movie)
            self.responding_movie.start()
        elif status == "LISTENING":
            self.responding_movie.stop()
            self.indicator_label.setMovie(self.listening_movie)
            self.listening_movie.start()
        else:
            self.listening_movie.stop()
            self.indicator_label.setMovie(self.responding_movie)
            self.responding_movie.start()