import sys
import io
from contextlib import redirect_stdout
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal, QThread, QObject
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtCore import QSize

class StatusSignal(QObject):
    """Emite sinais de mudança de status"""
    status_changed = Signal(str)

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caliope Voice Assistant")
        self.setFixedSize(700, 600)
        self.setup_ui()
        self.start_animation()
        self.setup_status_signal()

    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal centralizado
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setAlignment(Qt.AlignCenter)
        
        # Configurar fundo escuro
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 40))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Título
        self.title_label = QLabel("Caliope")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 40, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #4A90E2;")
        layout.addWidget(self.title_label, alignment=Qt.AlignCenter)
        
        # Indicador visual (pulsação)
        self.pulse_label = QLabel("●")
        self.pulse_label.setAlignment(Qt.AlignCenter)
        pulse_font = QFont("Arial", 50)
        self.pulse_label.setFont(pulse_font)
        self.pulse_label.setStyleSheet("color: #4A90E2; margin-top: 10px;")
        layout.addWidget(self.pulse_label, alignment=Qt.AlignCenter)
        
        # Status principal (grande)
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Arial", 28, QFont.Bold)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #FFFFFF; margin-top: 20px;")
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)
        
        # Área de informações (título do poema, etc)
        self.info_label = QLabel("")
        self.info_label.setAlignment(Qt.AlignCenter)
        info_font = QFont("Arial", 16)
        self.info_label.setFont(info_font)
        self.info_label.setStyleSheet("color: #90EE90; margin-top: 20px;")
        layout.addWidget(self.info_label, alignment=Qt.AlignCenter)
        
        # Adicionar espaço flexível
        layout.addStretch()

    def setup_status_signal(self):
        """Configura sinal de status"""
        self.status_signal = StatusSignal()
        self.status_signal.status_changed.connect(self.update_status)
    
    def update_status(self, status_text):
        """Atualiza o texto de status"""
        # Separar status e informações
        if "|" in status_text:
            status, info = status_text.split("|", 1)
            self.status_label.setText(status.strip().upper())
            self.info_label.setText(info.strip())
        else:
            self.status_label.setText(status_text.strip().upper())
            self.info_label.setText("")

    def start_animation(self):
        # Timer para alternar opacidade do ponto
        self.timer = QTimer()
        self.timer.timeout.connect(self.toggle_opacity)
        self.timer.start(1000)
        
    def toggle_opacity(self):
        current_style = self.pulse_label.styleSheet()
        if "opacity: 0.3" in current_style:
            self.pulse_label.setStyleSheet("color: #4A90E2; margin-top: 5px; opacity: 1.0;")
        else:
            self.pulse_label.setStyleSheet("color: #4A90E2; margin-top: 5px; opacity: 0.3;")