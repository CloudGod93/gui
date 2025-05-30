from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QSizePolicy
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, pyqtSignal

class TestModePage(QWidget):
    go_back_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)

        title_label = QLabel("Test Mode")
        title_font = QFont("Arial", 28, QFont.Weight.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        placeholder_label = QLabel("This is the placeholder for Test Mode features and diagnostics.")
        placeholder_font = QFont("Arial", 16)
        placeholder_label.setFont(placeholder_font)
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.back_button = QPushButton("Back to Home")
        self.back_button.setFont(QFont("Arial", 12))
        self.back_button.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        self.back_button.setMinimumWidth(200)
        self.back_button.clicked.connect(self.go_back_signal.emit)

        layout.addStretch(1)
        layout.addWidget(title_label)
        layout.addWidget(placeholder_label)
        layout.addStretch(1)
        layout.addWidget(self.back_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch(0)

        self.setLayout(layout)