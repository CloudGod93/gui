import os
import datetime
import csv
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                             QSizePolicy, QGridLayout, QFrame)
from PyQt6.QtGui import QFont, QPixmap, QImage
from PyQt6.QtCore import Qt, pyqtSignal, QTimer

import config #

class DataCollectionModePage(QWidget):
    go_back_signal = pyqtSignal()

    def __init__(self, main_window_ref=None, parent=None):
        super().__init__(parent)
        self.main_window_ref = main_window_ref
        self.setObjectName("DataCollectionModePage")

        # --- Session State ---
        self.session_id = None
        self.session_start_time = None
        self.images_captured_count = 0
        self.session_image_log = []
        self.current_user_level = "Unknown"
        self.camera_active = False # Will be set true when camera is actually started

        # --- UI Elements ---
        self._setup_ui()

        # --- Timer for Session Duration Display ---
        self.session_duration_timer = QTimer(self)
        self.session_duration_timer.timeout.connect(self._update_session_duration_display)

        # --- Ensure log directories exist (for offline mode) ---
        if config.DATA_STORAGE_FLAG == 1: #
            os.makedirs(config.SESSION_LOGS_PATH, exist_ok=True) #
            os.makedirs(config.IMAGE_LOGS_PATH, exist_ok=True) #

    def _setup_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10,10,10,10)
        main_layout.setSpacing(10)

        # --- Left Panel: Live Feed and Captured Image ---
        left_panel_layout = QVBoxLayout()
        
        self.live_feed_label = QLabel("Live Feed Area (Camera Off)")
        self.live_feed_label.setFont(QFont("Arial", 14))
        self.live_feed_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.live_feed_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.live_feed_label.setMinimumSize(640, 360) 
        self.live_feed_label.setStyleSheet("background-color: black; color: white;")
        left_panel_layout.addWidget(self.live_feed_label, 1)

        self.captured_image_label = QLabel("Last Captured Image")
        self.captured_image_label.setFont(QFont("Arial", 12))
        self.captured_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.captured_image_label.setFrameStyle(QFrame.Shape.Panel | QFrame.Shadow.Sunken)
        self.captured_image_label.setMinimumSize(320, 180) 
        self.captured_image_label.setStyleSheet("background-color: #333; color: white;")
        left_panel_layout.addWidget(self.captured_image_label, 0)

        # --- Right Panel: Info and Controls ---
        right_panel_layout = QVBoxLayout()
        right_panel_layout.setSpacing(15)

        page_title_label = QLabel("Data Collection")
        page_title_font = QFont("Arial", 22, QFont.Weight.Bold)
        page_title_label.setFont(page_title_font)
        page_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        right_panel_layout.addWidget(page_title_label)

        info_grid = QGridLayout()
        self.image_counter_label = QLabel("Images Captured: 0")
        self.image_counter_label.setFont(QFont("Arial", 14))
        self.session_time_label = QLabel("Session Time: 0s")
        self.session_time_label.setFont(QFont("Arial", 14))
        self.storage_mode_label = QLabel(f"Storage: {'Offline (Local)' if config.DATA_STORAGE_FLAG == 1 else 'Online (Cloud)'}") #
        self.storage_mode_label.setFont(QFont("Arial", 14))

        info_grid.addWidget(QLabel("Counter:"), 0, 0)
        info_grid.addWidget(self.image_counter_label, 0, 1)
        info_grid.addWidget(QLabel("Duration:"), 1, 0)
        info_grid.addWidget(self.session_time_label, 1, 1)
        info_grid.addWidget(QLabel("Mode:"), 2, 0)
        info_grid.addWidget(self.storage_mode_label, 2, 1)
        right_panel_layout.addLayout(info_grid)
        
        right_panel_layout.addStretch(1)

        self.capture_button = QPushButton("Capture Image")
        self.capture_button.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.capture_button.setMinimumHeight(60)
        self.capture_button.clicked.connect(self._capture_image)
        self.capture_button.setEnabled(False) # Disabled until camera is active
        right_panel_layout.addWidget(self.capture_button)

        self.end_session_button = QPushButton("End Session & Go Home")
        self.end_session_button.setFont(QFont("Arial", 14))
        self.end_session_button.setMinimumHeight(50)
        self.end_session_button.clicked.connect(self._end_session)
        right_panel_layout.addWidget(self.end_session_button)

        main_layout.addLayout(left_panel_layout, 2)
        main_layout.addLayout(right_panel_layout, 1)
        self.setLayout(main_layout)

    # --- Session Management ---
    def start_session(self):
        self.session_id = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_start_time = datetime.datetime.now()
        self.images_captured_count = 0
        self.session_image_log = []
        if self.main_window_ref:
            self.current_user_level = self.main_window_ref.current_user_level.capitalize()
        else:
            self.current_user_level = "N/A"

        self._update_image_counter_display()
        self.session_time_label.setText("Session Time: 0s")
        self.captured_image_label.setText("Last Captured Image")
        self.live_feed_label.setText("Initializing Camera...")
        
        print(f"Session {self.session_id} started. User: {self.current_user_level}")
        print(f"Attempting to use Camera Config: W:{config.CAMERA_RESOLUTION_WIDTH}, H:{config.CAMERA_RESOLUTION_HEIGHT}, FPS:{config.CAMERA_FPS}, RotationOpt:{config.CAMERA_ROTATION_OPTION}") #

        # --- TODO: Implement Actual Camera Initialization Here ---
        # Example:
        # try:
        #     self.camera = initialize_realsense_camera(config.CAMERA_RESOLUTION_WIDTH, ...)
        #     self.camera_active = True
        #     self.live_feed_label.setText("Camera Active")
        #     self.capture_button.setEnabled(True)
        #     # Start a thread or QTimer to fetch frames and update self.live_feed_label
        # except Exception as e:
        #     self.live_feed_label.setText(f"Failed to start camera: {e}")
        #     self.camera_active = False
        #     self.capture_button.setEnabled(False)
        
        # For now, simulate camera becoming active for UI testing:
        self.camera_active = True # Assume camera started successfully for now
        self.live_feed_label.setText("Camera Feed (Implement Update)")
        self.capture_button.setEnabled(True)

        if self.camera_active:
            if not self.session_duration_timer.isActive():
                self.session_duration_timer.start(1000) # Update duration every second
        print("Data collection session started.")

    def _update_session_duration_display(self):
        if self.session_start_time and self.camera_active: # Only update if session is ongoing
            duration = datetime.datetime.now() - self.session_start_time
            self.session_time_label.setText(f"Session Time: {int(duration.total_seconds())}s")

    # --- Image Handling ---
    def _capture_image(self):
        if not self.camera_active or not self.session_id:
            # This case should ideally be prevented by disabling the capture button
            print("Capture attempt failed: Camera not active or session not started.")
            return

        self.images_captured_count += 1
        capture_time = datetime.datetime.now()
        image_filename_base = f"session_{self.session_id}_img_{self.images_captured_count:04d}"
        
        # --- TODO: Implement Actual Image Capture from Camera Frame Here ---
        # Example:
        # captured_frame_data = self.camera.get_current_frame_for_saving() # Your method
        # if captured_frame_data is None:
        #     print("Failed to capture frame.")
        #     return
        
        # --- TODO: Implement Display of Captured Image ---
        # Example:
        # q_image = QImage(captured_frame_data, width, height, QImage.Format...)
        # pixmap = QPixmap.fromImage(q_image)
        # self.captured_image_label.setPixmap(pixmap.scaled(
        #     self.captured_image_label.width(), self.captured_image_label.height(),
        #     Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
        # ))
        self.captured_image_label.setText(f"Captured: {image_filename_base}.png\n(Display Not Implemented)")
        
        image_path_or_link = "" # Will be the actual path or cloud link

        if config.DATA_STORAGE_FLAG == 1: # Offline
            image_filename = f"{image_filename_base}.png"
            image_full_path = os.path.join(config.IMAGE_LOGS_PATH, image_filename) #
            
            # --- TODO: Implement Actual Image Saving to File ---
            # Example using OpenCV (cv2):
            # import cv2
            # cv2.imwrite(image_full_path, captured_frame_data) 
            print(f"Image would be saved to: {image_full_path}")
            image_path_or_link = image_full_path
        else: # Online
            # --- TODO: Implement Upload to Google Drive ---
            # This would involve Google Drive API calls
            print(f"Image {image_filename_base} would be prepared for Google Drive upload.")
            image_path_or_link = f"gdrive_placeholder_link_for_{image_filename_base}"

        self.session_image_log.append({
            "filename": image_filename_base + (".png" if config.DATA_STORAGE_FLAG == 1 else ""),
            "path_or_link": image_path_or_link,
            "timestamp": capture_time.isoformat(),
            "classification_placeholder": "N/A", # To be filled later
            "classification_log_link_placeholder": "N/A" # To be filled later
        })
        self._update_image_counter_display()
        print(f"Image {self.images_captured_count} captured and logged.")

    def _update_image_counter_display(self):
        self.image_counter_label.setText(f"Images Captured: {self.images_captured_count}")

    def _end_session(self):
        if not self.session_start_time:
            self.go_back_signal.emit()
            return
            
        self.camera_active = False
        self.capture_button.setEnabled(False)
        if self.session_duration_timer.isActive():
            self.session_duration_timer.stop()
        
        # --- TODO: Implement Actual Camera Shutdown/Release Here ---
        # Example:
        # if hasattr(self, 'camera') and self.camera:
        #     self.camera.release() # Or your camera object's equivalent
        self.live_feed_label.setText("Camera Off")
        print("Camera resources released (implementation pending).")

        session_end_time = datetime.datetime.now()
        total_session_time_delta = session_end_time - self.session_start_time
        total_session_time_seconds = int(total_session_time_delta.total_seconds())

        session_summary = {
            "session_id": self.session_id,
            "mode": "Data Collection",
            "permission_level": self.current_user_level,
            "start_time": self.session_start_time.isoformat(),
            "end_time": session_end_time.isoformat(),
            "total_duration_seconds": total_session_time_seconds,
            "images_captured": self.images_captured_count,
            "data_storage_mode": "Offline" if config.DATA_STORAGE_FLAG == 1 else "Online", #
            "images_details_count": len(self.session_image_log)
        }
        print(f"Session {self.session_id} ended. Duration: {total_session_time_seconds}s. Images: {self.images_captured_count}.")

        if config.DATA_STORAGE_FLAG == 1: # Offline - Save to CSV
            session_log_filename = os.path.join(config.SESSION_LOGS_PATH, f"summary_{self.session_id}.csv") #
            image_details_log_filename = os.path.join(config.SESSION_LOGS_PATH, f"images_{self.session_id}.csv") #

            try:
                with open(session_log_filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(session_summary.keys())
                    writer.writerow(session_summary.values())
                print(f"Session summary saved to: {session_log_filename}")

                if self.session_image_log:
                    with open(image_details_log_filename, 'w', newline='') as f:
                        fieldnames = self.session_image_log[0].keys()
                        writer = csv.DictWriter(f, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(self.session_image_log)
                    print(f"Image details saved to: {image_details_log_filename}")
            except IOError as e:
                print(f"Error writing local log files: {e}")
        else: # Online
            # --- TODO: Implement Saving session_summary to SQL Database ---
            print("Session summary (and image details) would be saved to online SQL database.")
        
        self.session_start_time = None 
        self.go_back_signal.emit()

    # --- Qt Event Handlers ---
    def showEvent(self, event):
        super().showEvent(event)
        self.start_session()

    def hideEvent(self, event):
        super().hideEvent(event)
        # If the page is hidden and a session was active, ensure it's properly ended.
        # This might happen if user navigates away by means other than "End Session" button
        # (e.g. closing window, though main_window's closeEvent should handle that).
        if self.session_start_time and self.camera_active: # Check if session was actually running
            print("DataCollectionModePage hidden during active session. Consider auto-ending or prompting.")
            # For now, we'll rely on the explicit "End Session" button.
            # You might want to stop the camera here regardless.
            self.camera_active = False # Mark as inactive
            self.capture_button.setEnabled(False)
            if self.session_duration_timer.isActive():
                self.session_duration_timer.stop()
            # self._end_session() # Potentially auto-end, but could lead to data loss if not intended.