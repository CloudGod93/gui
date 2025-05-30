from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, 
    QStatusBar, QMenu, QMessageBox # Added QMessageBox
)
from PyQt6.QtGui import QFont, QAction, QCloseEvent # Added QCloseEvent
from PyQt6.QtCore import Qt, QPoint

import config 
from app.src.about_page import AboutDialog
from app.src.system_access_dialog import SystemAccessDialog 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APP_TITLE)
        self.setGeometry(100, 100, 900, 700)

        self.current_user_level = config.DEFAULT_USER_LEVEL

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        self._create_menu_bar() 

        app_info_label = QLabel(f"Main Application Interface - {config.COMPANY_NAME}")
        app_info_label.setFont(QFont("Arial", 22))
        app_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(app_info_label)

        main_layout.addStretch(1)

        task_button = QPushButton("Start Automation Task")
        task_button.setFont(QFont("Arial", 12))
        task_button.setMinimumHeight(40)
        main_layout.addWidget(task_button, 0, Qt.AlignmentFlag.AlignCenter)
        
        main_layout.addStretch(1)

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        
        self._update_ui_for_user_level() 
        
        self.center_on_screen()


    def _update_ui_for_user_level(self):
        """Updates UI elements that depend on the current user level."""

        self.system_access_menu.setTitle(f"Access: {self.current_user_level}")

        menu_action = self.system_access_menu.menuAction()
        if menu_action:
            font = menu_action.font()
            font.setPointSize(15) 
            font.setBold(True)
            menu_action.setFont(font)

        self.system_access_menu.clear() 

        if self.current_user_level == config.DEFAULT_USER_LEVEL: 
            elevate_action = QAction("Elevate Permissions...", self.system_access_menu)
            elevate_action.triggered.connect(self._handle_user_level_change)
            self.system_access_menu.addAction(elevate_action)
        else:
            change_level_action = QAction("Change User Level...", self.system_access_menu)
            change_level_action.triggered.connect(self._handle_user_level_change)
            self.system_access_menu.addAction(change_level_action)
            
            self.system_access_menu.addSeparator()
            
            logout_action = QAction("Logout", self.system_access_menu)
            logout_action.triggered.connect(self._handle_logout)
            self.system_access_menu.addAction(logout_action)
        
    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        self.system_access_menu = QMenu(self) 
        menu_bar.addMenu(self.system_access_menu) 

        # --- Options Menu ---
        options_menu = menu_bar.addMenu("&Options")
        
        camera_settings_action = QAction("Camera Settings", self)
        options_menu.addAction(camera_settings_action)
        
        system_settings_action = QAction("System Settings", self)
        options_menu.addAction(system_settings_action)
        
        # --- Help Menu ---
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

        help_menu.addSeparator() 

        close_app_action = QAction("Close Application", self) 
        # This action will now indirectly trigger the closeEvent
        close_app_action.triggered.connect(self.close) 
        help_menu.addAction(close_app_action)


    def _show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def _handle_user_level_change(self):
        dialog = SystemAccessDialog(self) 
        if dialog.exec(): 
            selected_user = dialog.get_selected_user_level()
            if selected_user:
                self.current_user_level = selected_user
                self._update_ui_for_user_level()

    def _handle_logout(self):
        self.current_user_level = config.DEFAULT_USER_LEVEL
        self._update_ui_for_user_level()

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        if screen_geometry:
             self.move(screen_geometry.center() - QPoint(self.width() // 2, self.height() // 2))
        else:
             desktop = QApplication.screens()[0].availableGeometry()
             self.move(desktop.center() - QPoint(self.width() // 2, self.height() // 2))

    def closeEvent(self, event: QCloseEvent): 
        """Override the close event to ask for confirmation."""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to close the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  
        )

        if reply == QMessageBox.StandardButton.Yes:
            event.accept() 
        else:
            event.ignore() 