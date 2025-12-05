import sys
import io
from contextlib import redirect_stdout
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QTextEdit
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve, Signal, QThread, QObject
from PySide6.QtGui import QFont, QPalette, QColor
from PySide6.QtCore import QSize

class PrintCapture(QObject):
    """Captura prints e emite signals"""
    print_signal = Signal(str)
    
    def __init__(self):
        super().__init__()
        self.original_stdout = sys.stdout
        sys.stdout = self
        
    def write(self, text):
        if text.strip():
            self.print_signal.emit(text.strip())
        self.original_stdout.write(text)
    
    def flush(self):
        pass

class MainScreen(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caliope Voice Assistant")
        self.setFixedSize(700, 600)
        self.setup_ui()
        self.start_animation()
        self.setup_print_capture()

    def setup_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Configurar fundo escuro
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(30, 30, 40))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # Título
        self.title_label = QLabel("Caliope")
        self.title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 32, QFont.Bold)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #4A90E2;")
        layout.addWidget(self.title_label)
        
        # Status
        self.status_label = QLabel("Estou ouvindo...")
        self.status_label.setAlignment(Qt.AlignCenter)
        status_font = QFont("Arial", 14)
        self.status_label.setFont(status_font)
        self.status_label.setStyleSheet("color: #FFFFFF; margin-top: 10px;")
        layout.addWidget(self.status_label)
        
        # Indicador visual (pulsação)
        self.pulse_label = QLabel("●")
        self.pulse_label.setAlignment(Qt.AlignCenter)
        pulse_font = QFont("Arial", 36)
        self.pulse_label.setFont(pulse_font)
        self.pulse_label.setStyleSheet("color: #4A90E2; margin-top: 5px;")
        layout.addWidget(self.pulse_label)
        
        # Área de log
        log_label = QLabel("Log:")
        log_label.setStyleSheet("color: #FFFFFF; font-weight: bold;")
        layout.addWidget(log_label)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #1a1a25;
                color: #4A90E2;
                border: 1px solid #4A90E2;
                border-radius: 5px;
                font-family: Courier New;
                font-size: 10pt;
                padding: 5px;
            }
        """)
        self.log_text.setMaximumHeight(300)
        layout.addWidget(self.log_text)

    def setup_print_capture(self):
        """Configura captura de prints"""
        self.print_capture = PrintCapture()
        self.print_capture.print_signal.connect(self.update_log)
    
    def update_log(self, text):
        """Atualiza o log com novo texto"""
        self.log_text.append(f"> {text}")
        # Auto-scroll para o final
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def start_animation(self):
        # Timer para alternar opacidade
        self.timer = QTimer()
        self.timer.timeout.connect(self.toggle_opacity)
        self.timer.start(1000)
        
    def toggle_opacity(self):
        current_style = self.pulse_label.styleSheet()
        if "opacity: 0.3" in current_style:
            self.pulse_label.setStyleSheet("color: #4A90E2; margin-top: 5px; opacity: 1.0;")
        else:
            self.pulse_label.setStyleSheet("color: #4A90E2; margin-top: 5px; opacity: 0.3;")
    
    def update_status(self, status_text):
        """Atualiza o texto de status"""
        self.status_label.setText(status_text)