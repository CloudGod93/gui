from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QPushButton, QComboBox, QDialogButtonBox, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

import config

class SystemSettingsDialog(QDialog):
    def __init__(self, parent=None, current_mode_id=None):
        super().__init__(parent)
        self.setWindowTitle("System Settings")
        self.setMinimumSize(400, 320) 

        self.selected_mode_id = current_mode_id if current_mode_id is not None else config.DEFAULT_OPERATION_MODE_ID #

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(12)

        title_label = QLabel("System Configuration")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_font = QFont("Arial", 16, QFont.Weight.Bold) 
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)

        main_layout.addSpacing(10)

        # --- Operation Mode Selection ---
        mode_label = QLabel("Select Operation Mode:")
        mode_label_font = QFont("Arial", 11) 
        mode_label.setFont(mode_label_font)
        main_layout.addWidget(mode_label)

        self.mode_combobox = QComboBox()
        combobox_font = QFont("Arial", 10) 
        self.mode_combobox.setFont(combobox_font)
        self.mode_combobox.setMinimumHeight(30) 

        for mode_id, mode_name in config.APP_MODES.items(): 
            self.mode_combobox.addItem(mode_name, userData=mode_id)

        current_mode_index = self.mode_combobox.findData(self.selected_mode_id)
        if current_mode_index != -1:
            self.mode_combobox.setCurrentIndex(current_mode_index)
        main_layout.addWidget(self.mode_combobox)
        # --- End Operation Mode Selection ---

        main_layout.addStretch(1)

        # --- Buttons ---
        self.button_box = QDialogButtonBox()
        save_button = self.button_box.addButton("Save Changes", QDialogButtonBox.ButtonRole.AcceptRole)
        close_button = self.button_box.addButton("Cancel", QDialogButtonBox.ButtonRole.RejectRole)

        button_font = QFont("Arial", 10) 
        save_button.setFont(button_font)
        save_button.setMinimumHeight(30)
        close_button.setFont(button_font)
        close_button.setMinimumHeight(30)

        self.button_box.accepted.connect(self.accept_changes)
        self.button_box.rejected.connect(self.reject)
        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)

    def accept_changes(self):
        new_selected_mode_id = self.mode_combobox.currentData()
        if new_selected_mode_id != self.selected_mode_id:
            self.selected_mode_id = new_selected_mode_id
            QMessageBox.information(self, "Settings Updated", f"Operation mode will be changed to: {self.mode_combobox.currentText()}.")
        super().accept()


    def get_selected_mode_id(self):
        return self.selected_mode_id

if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)

    dialog = SystemSettingsDialog(current_mode_id=config.DEFAULT_OPERATION_MODE_ID) #
    if dialog.exec():
        print(f"Dialog accepted. Selected Mode ID: {dialog.get_selected_mode_id()}")
    else:
        print("Dialog cancelled.")
    sys.exit(app.exec())