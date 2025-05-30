from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QPushButton,
    QStatusBar, QMenu, QMessageBox, QHBoxLayout, QSpacerItem, QSizePolicy,
    QStackedWidget
)
from PyQt6.QtGui import QFont, QAction, QCloseEvent, QPixmap, QShowEvent
from PyQt6.QtCore import Qt, QPoint

import config 
from app.src.pages.about_page import AboutDialog 
from app.src.pages.system_access_dialog import SystemAccessDialog 
from app.src.pages.camera_settings_dialog import CameraSettingsDialog 
from app.src.pages.system_settings_dialog import SystemSettingsDialog 

from app.src.modes.data_collection_mode import DataCollectionModePage
from app.src.modes.test_mode import TestModePage
from app.src.modes.production_mode import ProductionModePage


class MainWindow(QMainWindow):
    HOME_PAGE_INDEX = 0
    DATA_COLLECTION_PAGE_INDEX = 1
    TEST_PAGE_INDEX = 2
    PRODUCTION_PAGE_INDEX = 3

    def __init__(self):
        super().__init__()
        self.setWindowTitle(config.APP_TITLE)
        self.setGeometry(100, 100, 1200, 800)
        self._initial_show_done = False

        self.current_user_level = getattr(config, 'DEFAULT_USER_LEVEL', "operator").lower()
        self.ADMIN_LEVEL = getattr(config, 'ADMIN_LEVEL', "admin").lower()
        self.MAINTENANCE_LEVEL = getattr(config, 'MAINTENANCE_LEVEL', "maintenance").lower()
        self.current_operation_mode_id = config.DEFAULT_OPERATION_MODE_ID

        self._create_menu_bar()

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self._create_home_page()
        self._create_mode_pages()

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        self._update_ui_for_user_level()
        self.center_on_screen()
        
        self.go_to_home_page()

    # --- Page Creation and Management ---
    def _create_home_page(self):
        self.home_page_widget = QWidget()
        main_app_layout = QVBoxLayout(self.home_page_widget)
        main_app_layout.setContentsMargins(30, 30, 30, 30)
        main_app_layout.setSpacing(30)

        content_group_layout = QVBoxLayout()
        content_group_layout.setSpacing(25)
        content_group_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(config.LOGO_PATH)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaledToWidth(400, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
        else:
            self.logo_label.setText("Logo N/A")
            self.logo_label.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        content_group_layout.addWidget(self.logo_label)

        self.operation_mode_label = QLabel() 
        self.operation_mode_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.operation_mode_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_group_layout.addWidget(self.operation_mode_label)
        
        content_group_layout.addSpacing(40)

        self.task_button = QPushButton("Begin Automation")
        self.task_button.setFont(QFont("Arial", 22, QFont.Weight.Bold))
        self.task_button.setMinimumHeight(80)
        self.task_button.setMinimumWidth(450)
        self.task_button.setMaximumWidth(500)
        self.task_button.clicked.connect(self._start_automation_task) 
        content_group_layout.addWidget(self.task_button, 0, Qt.AlignmentFlag.AlignCenter)

        main_app_layout.addStretch(1)
        main_app_layout.addLayout(content_group_layout)
        main_app_layout.addStretch(1)
        
        self.stacked_widget.addWidget(self.home_page_widget)

    def _create_mode_pages(self):
        self.data_collection_page = DataCollectionModePage()
        self.test_page = TestModePage()
        self.production_page = ProductionModePage()

        self.data_collection_page.go_back_signal.connect(self.go_to_home_page)
        self.test_page.go_back_signal.connect(self.go_to_home_page)
        self.production_page.go_back_signal.connect(self.go_to_home_page)

        self.stacked_widget.addWidget(self.data_collection_page)
        self.stacked_widget.addWidget(self.test_page)            
        self.stacked_widget.addWidget(self.production_page)      
        
    def _start_automation_task(self):
        if self.current_operation_mode_id == 1:
            self.stacked_widget.setCurrentIndex(self.DATA_COLLECTION_PAGE_INDEX)
        elif self.current_operation_mode_id == 2:
            self.stacked_widget.setCurrentIndex(self.TEST_PAGE_INDEX)
        elif self.current_operation_mode_id == 3:
            self.stacked_widget.setCurrentIndex(self.PRODUCTION_PAGE_INDEX)
        else:
            QMessageBox.warning(self, "Mode Error", "Invalid operation mode selected.")
            self.go_to_home_page()

    def go_to_home_page(self):
        self.stacked_widget.setCurrentIndex(self.HOME_PAGE_INDEX)
        self._update_operation_mode_display()

    # --- Event Handlers and UI Updates ---
    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        if not self._initial_show_done:
            self._update_operation_mode_display()
            self._initial_show_done = True

    def _update_operation_mode_display(self):
        mode_name = config.APP_MODES.get(self.current_operation_mode_id, "Unknown Mode")
        if hasattr(self, 'operation_mode_label'): 
            self.operation_mode_label.setText(f"Mode: {mode_name}")
        
        status_text = f"Current Mode: {mode_name}  |  User: {self.current_user_level.capitalize()}"
        if self.statusBar:
             self.statusBar.showMessage(status_text, 0)

    def _update_ui_for_user_level(self):
        access_menu_title = f"Access: {self.current_user_level.capitalize()}"
        self.system_access_menu.setTitle(access_menu_title)
        menu_action = self.system_access_menu.menuAction()
        if menu_action:
            menu_action.setText(access_menu_title) 

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
            logout_action.triggered.connect(self._handle_logout_and_go_home)
            self.system_access_menu.addAction(logout_action)

        can_access_camera = self.current_user_level in [self.ADMIN_LEVEL, self.MAINTENANCE_LEVEL]
        self.camera_settings_action.setEnabled(can_access_camera)
        self.camera_settings_action.setToolTip(
            "Configure camera parameters" if can_access_camera else "Requires Admin or Maintenance access")

        can_access_system = self.current_user_level == self.ADMIN_LEVEL
        self.system_settings_action.setEnabled(can_access_system)
        self.system_settings_action.setToolTip(
            "Configure system parameters" if can_access_system else "Requires Admin access")
            
        self._update_operation_mode_display()

    # --- Menu Bar Creation ---
    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        self.system_access_menu = QMenu(self)
        menu_bar.addMenu(self.system_access_menu)

        self.options_menu = menu_bar.addMenu("&Options")
        self.camera_settings_action = QAction("Camera Settings", self)
        self.camera_settings_action.triggered.connect(self._open_camera_settings_dialog)
        self.options_menu.addAction(self.camera_settings_action)

        self.system_settings_action = QAction("System Settings", self)
        self.system_settings_action.triggered.connect(self._open_system_settings_dialog_with_mode_handling)
        self.options_menu.addAction(self.system_settings_action)
        
        self.help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self._show_about_dialog)
        self.help_menu.addAction(about_action)
        self.help_menu.addSeparator()
        
        close_app_action = QAction("Close Application", self)
        close_app_action.triggered.connect(self.close)
        self.help_menu.addAction(close_app_action)

    # --- Dialog Handling and Actions ---
    def _show_about_dialog(self):
        dialog = AboutDialog(self)
        dialog.exec()

    def _handle_user_level_change(self):
        if self.stacked_widget.currentIndex() != self.HOME_PAGE_INDEX:
             QMessageBox.information(self, "User Level Change", "Please return to the home screen to change user level.")
             return

        dialog = SystemAccessDialog(self)
        if dialog.exec():
            selected_user_raw = dialog.get_selected_user_level()
            if selected_user_raw:
                self.current_user_level = selected_user_raw.lower()
                self._update_ui_for_user_level()

    def _handle_logout_and_go_home(self): 
        self.current_user_level = getattr(config, 'DEFAULT_USER_LEVEL', "operator").lower()
        self._update_ui_for_user_level()
        self.go_to_home_page() 

    def _open_camera_settings_dialog(self):
        if self.stacked_widget.currentIndex() != self.HOME_PAGE_INDEX:
             QMessageBox.information(self, "Settings", "Camera settings can only be accessed from the home screen.")
             return
        if self.current_user_level not in [self.ADMIN_LEVEL, self.MAINTENANCE_LEVEL]:
            QMessageBox.warning(self, "Access Denied", "You do not have permission to access Camera Settings.")
            return
        dialog = CameraSettingsDialog(self)
        dialog.exec()

    def _open_system_settings_dialog_with_mode_handling(self):
        if self.stacked_widget.currentIndex() != self.HOME_PAGE_INDEX:
             QMessageBox.information(self, "Settings", "System settings can only be accessed from the home screen.")
             return
        if self.current_user_level != self.ADMIN_LEVEL:
            QMessageBox.warning(self, "Access Denied", "You do not have permission to access System Settings.")
            return

        dialog = SystemSettingsDialog(self, current_mode_id=self.current_operation_mode_id)
        if dialog.exec():
            new_mode_id = dialog.get_selected_mode_id()
            if new_mode_id != self.current_operation_mode_id:
                self.current_operation_mode_id = new_mode_id
                self._update_operation_mode_display() 

    # --- Window Management ---
    def center_on_screen(self):
        try:
            screen_geometry = QApplication.primaryScreen().availableGeometry()
            if screen_geometry:
                 self.move(screen_geometry.center() - QPoint(self.width() // 2, self.height() // 2))
            else:
                screens = QApplication.screens()
                if screens:
                    desktop = screens[0].availableGeometry()
                    self.move(desktop.center() - QPoint(self.width() // 2, self.height() // 2))
        except Exception as e:
            print(f"Warning: Could not center window on screen: {e}")

    def closeEvent(self, event: QCloseEvent):
        if self.stacked_widget.currentIndex() != self.HOME_PAGE_INDEX:
            reply = QMessageBox.question(
                self, "Confirm Exit", 
                "A task is currently active. Are you sure you want to exit?\n"
                "Exiting now might discard unsaved data or interrupt processes.",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                event.ignore()
                return

        final_reply = QMessageBox.question(
            self, "Confirm Exit", "Are you sure you want to close the application?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if final_reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()