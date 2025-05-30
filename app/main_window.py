from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton, 
    QStatusBar, QMenu, QMessageBox
)
from PyQt6.QtGui import QFont, QAction, QCloseEvent
from PyQt6.QtCore import Qt, QPoint

import config 
from app.src.pages.about_page import AboutDialog
from app.src.pages.system_access_dialog import SystemAccessDialog
from app.src.pages.camera_settings_dialog import CameraSettingsDialog
from app.src.pages.system_settings_dialog import SystemSettingsDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APP_TITLE)
        self.setGeometry(100, 100, 900, 700)

        self.current_user_level = getattr(config, 'DEFAULT_USER_LEVEL', "operator").lower()
        self.ADMIN_LEVEL = getattr(config, 'ADMIN_LEVEL', "admin").lower()
        self.MAINTENANCE_LEVEL = getattr(config, 'MAINTENANCE_LEVEL', "maintenance").lower()

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
        self.system_access_menu.setTitle(f"Access: {self.current_user_level.capitalize()}")

        menu_action = self.system_access_menu.menuAction()
        if menu_action:
            font = menu_action.font()
            font.setPointSize(15) 
            font.setBold(True)
            menu_action.setFont(font)

        self.system_access_menu.clear() 

        if self.current_user_level == getattr(config, 'DEFAULT_USER_LEVEL', "operator").lower(): 
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
        
        can_access_camera = self.current_user_level in [self.ADMIN_LEVEL, self.MAINTENANCE_LEVEL]
        self.camera_settings_action.setEnabled(can_access_camera)
        self.camera_settings_action.setToolTip(
            "Configure camera parameters" if can_access_camera else "Requires Admin or Maintenance access"
        )

        can_access_system = self.current_user_level == self.ADMIN_LEVEL
        self.system_settings_action.setEnabled(can_access_system)
        self.system_settings_action.setToolTip(
            "Configure system parameters" if can_access_system else "Requires Admin access"
        )

    def _create_menu_bar(self):
        menu_bar = self.menuBar()

        self.system_access_menu = QMenu(self) 
        menu_bar.addMenu(self.system_access_menu) 

        options_menu = menu_bar.addMenu("&Options")
        
        self.camera_settings_action = QAction("Camera Settings", self)
        self.camera_settings_action.triggered.connect(self._open_camera_settings_dialog)
        options_menu.addAction(self.camera_settings_action)
        
        self.system_settings_action = QAction("System Settings", self)
        self.system_settings_action.triggered.connect(self._open_system_settings_dialog)
        options_menu.addAction(self.system_settings_action)
        
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about_dialog)
        help_menu.addAction(about_action)

        help_menu.addSeparator() 

        close_app_action = QAction("Close Application", self) 
        close_app_action.triggered.connect(self.close) 
        help_menu.addAction(close_app_action)

    def _show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def _handle_user_level_change(self):
        dialog = SystemAccessDialog(self) 
        if dialog.exec(): 
            selected_user_raw = dialog.get_selected_user_level()
            if selected_user_raw:
                self.current_user_level = selected_user_raw.lower() 
                self._update_ui_for_user_level()

    def _handle_logout(self):
        self.current_user_level = getattr(config, 'DEFAULT_USER_LEVEL', "operator").lower()
        self._update_ui_for_user_level()
        self.statusBar.showMessage(f"Logged out. Access level: {self.current_user_level.capitalize()}", 3000)

    def center_on_screen(self):
        try:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            if screen_geometry:
                self.move(screen_geometry.center() - QPoint(self.width() // 2, self.height() // 2))
            else: 
                desktop = QApplication.screens()[0].availableGeometry()
                self.move(desktop.center() - QPoint(self.width() // 2, self.height() // 2))
        except Exception as e:
            print(f"Warning: Could not center window on screen: {e}")


    def closeEvent(self, event: QCloseEvent): 
        reply = QMessageBox.question(
            self, "Confirm Exit", "Are you sure you want to close the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No  
        )
        if reply == QMessageBox.StandardButton.Yes:
            event.accept() 
        else:
            event.ignore() 

    def _open_camera_settings_dialog(self):
        if self.current_user_level not in [self.ADMIN_LEVEL, self.MAINTENANCE_LEVEL]:
            QMessageBox.warning(self, "Access Denied", "You do not have permission to access Camera Settings.")
            return
        
        dialog = CameraSettingsDialog(self)
        dialog.exec()

    def _open_system_settings_dialog(self):
        if self.current_user_level != self.ADMIN_LEVEL:
            QMessageBox.warning(self, "Access Denied", "You do not have permission to access System Settings.")
            return
            
        dialog = SystemSettingsDialog(self)
        dialog.exec()

