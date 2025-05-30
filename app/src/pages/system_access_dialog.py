from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QMessageBox
)
from PyQt6.QtGui import QFont

import config

class SystemAccessDialog(QDialog): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("User Access Control") 
        self.setModal(True)
        self.setMinimumWidth(300)

        self.selected_user_level = None 

        layout = QVBoxLayout(self)

        title_label = QLabel("Select User Level") 
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)

        layout.addWidget(QLabel("Username:"))
        self.username_combo = QComboBox()
        self.username_combo.addItems([user for user in config.APP_USERS if user != config.DEFAULT_USER_LEVEL])
        layout.addWidget(self.username_combo)

        layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.password_input)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        ok_button = button_box.button(QDialogButtonBox.StandardButton.Ok)
        if ok_button:
             ok_button.setText("Apply")
        
        button_box.accepted.connect(self.attempt_access_change)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def attempt_access_change(self):
        username = self.username_combo.currentText()
        password = self.password_input.text()

        user_data = config.APP_USERS.get(username)

        if user_data and user_data.get("password") == password:
            self.selected_user_level = username
            self.accept()
        else:
            QMessageBox.warning(self, "Access Denied", "Invalid username or password.")
            self.password_input.clear()
            self.password_input.setFocus()

    def get_selected_user_level(self):
        return self.selected_user_level