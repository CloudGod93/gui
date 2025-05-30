from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QPoint

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MidWest Machine LLC - Main Application")
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        label = QLabel("Main Application Interface - MidWest Machine LLC")
        label.setFont(QFont("Arial", 22))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        button = QPushButton("Start Automation Task")
        button.setFont(QFont("Arial", 12))
        button.setMinimumHeight(40)
        layout.addWidget(button, 0, Qt.AlignmentFlag.AlignCenter)
        
        self.center_on_screen()

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        if screen_geometry:
             self.move(screen_geometry.center() - QPoint(self.width() // 2, self.height() // 2))
        else: # Fallback if primaryScreen() is not available during init (rare)
             desktop = QApplication.screens()[0].availableGeometry()
             self.move(desktop.center() - QPoint(self.width() // 2, self.height() // 2))