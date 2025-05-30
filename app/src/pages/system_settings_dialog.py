from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class SystemSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("System Settings")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)

        title_label = QLabel("System Configuration")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)
        
        layout.addStretch(1)

        placeholder_label = QLabel("System settings content will be implemented here.\n\n(e.g., Logging, Network, Paths)")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder_label)

        layout.addStretch(1)

        button_layout = QVBoxLayout()
        
        save_button = QPushButton("Save (Placeholder)")
        save_button.setEnabled(False)
        # save_button.clicked.connect(self.accept)
        button_layout.addWidget(save_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.reject)
        button_layout.addWidget(close_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    app = QApplication(sys.argv)
    dialog = SystemSettingsDialog()
    dialog.show()
    sys.exit(app.exec())
