from PyQt6.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class CameraSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Camera Settings")
        self.setMinimumSize(400, 300)

        layout = QVBoxLayout(self)

        title_label = QLabel("Camera Configuration")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        layout.addWidget(title_label)

        layout.addStretch(1) # Add some space

        placeholder_label = QLabel("Camera settings content will be implemented here.\n\n(e.g., Resolution, FPS, Rotation)")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder_label)

        layout.addStretch(1) # Add some space

        # Example buttons (can be removed or adapted later)
        button_layout = QVBoxLayout() # Changed to QVBoxLayout for stacking
        
        apply_button = QPushButton("Apply (Placeholder)")
        apply_button.setEnabled(False) # Initially disabled
        # apply_button.clicked.connect(self.accept) 
        button_layout.addWidget(apply_button)

        cancel_button = QPushButton("Close")
        cancel_button.clicked.connect(self.reject) # Closes the dialog
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)

        self.setLayout(layout)
