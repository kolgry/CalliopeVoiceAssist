import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QThread
from main_screen import MainScreen
from assistente_thread import AssistenteWorker

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainScreen()
    window.show()
    
    assistente_worker = AssistenteWorker(window)
    assistente_worker.start()
    
    sys.exit(app.exec())
