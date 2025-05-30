import unittest
import os
import datetime
import logging
import shutil

from app.src.utils.logger import Logger
from config import LOGS_DIR_NAME, SESSION_LOGS_PATH, IMAGE_LOGS_PATH, APP_TITLE, APP_VERSION
import config as app_config # Import for direct patching

TEST_LOGS_DIR_NAME = "test_logs"
TEST_SESSION_LOGS_PATH = os.path.join(TEST_LOGS_DIR_NAME, "sessions")
TEST_IMAGE_LOGS_PATH = os.path.join(TEST_LOGS_DIR_NAME, "images")

class TestLogger(unittest.TestCase):
    """Tests for the Logger class."""

    def setUp(self):
        """Prepare test environment: clean/create test log dirs, patch config."""
        self.test_log_root = TEST_LOGS_DIR_NAME
        if os.path.exists(self.test_log_root):
            shutil.rmtree(self.test_log_root)
        os.makedirs(self.test_log_root)
        os.makedirs(TEST_SESSION_LOGS_PATH)
        os.makedirs(TEST_IMAGE_LOGS_PATH)

        self.app_name = "TestApp"
        self.app_version = "1.0-test"
        self.user_level = "TestUser"
        self.operation_mode = "TestMode"

        self._original_config_values = {
            'LOGS_DIR_NAME': app_config.LOGS_DIR_NAME,
            'SESSION_LOGS_PATH': app_config.SESSION_LOGS_PATH,
            'IMAGE_LOGS_PATH': app_config.IMAGE_LOGS_PATH,
            'DATA_STORAGE_FLAG': getattr(app_config, 'DATA_STORAGE_FLAG', 1)
        }

        app_config.LOGS_DIR_NAME = TEST_LOGS_DIR_NAME
        app_config.SESSION_LOGS_PATH = TEST_SESSION_LOGS_PATH
        app_config.IMAGE_LOGS_PATH = TEST_IMAGE_LOGS_PATH
        app_config.DATA_STORAGE_FLAG = 1 # Default to local storage for most tests

        self.logger_instance = Logger(
            app_name=self.app_name,
            app_version=self.app_version,
            user_level=self.user_level,
            operation_mode=self.operation_mode
        )
        self.log_file_path = self.logger_instance.log_file_path
        self.assertTrue(self.log_file_path.startswith(TEST_LOGS_DIR_NAME))

    def tearDown(self):
        """Clean up test environment: close handlers, remove test log dir, restore config."""
        if hasattr(self, 'logger_instance') and self.logger_instance and self.logger_instance.logger.handlers:
            for handler in list(self.logger_instance.logger.handlers):
                handler.close()
                self.logger_instance.logger.removeHandler(handler)

        if os.path.exists(self.test_log_root):
            shutil.rmtree(self.test_log_root)

        app_config.LOGS_DIR_NAME = self._original_config_values['LOGS_DIR_NAME']
        app_config.SESSION_LOGS_PATH = self._original_config_values['SESSION_LOGS_PATH']
        app_config.IMAGE_LOGS_PATH = self._original_config_values['IMAGE_LOGS_PATH']
        app_config.DATA_STORAGE_FLAG = self._original_config_values['DATA_STORAGE_FLAG']

    def read_log_file(self, file_path=None):
        path_to_read = file_path if file_path else self.log_file_path
        try:
            with open(path_to_read, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def test_01_log_file_creation(self):
        """Test that the main log file is created in the test logs directory."""
        self.assertTrue(os.path.exists(self.log_file_path), f"Log file was not created at {self.log_file_path}")

    def test_02_initial_information_logged(self):
        """Test that initial application information is logged correctly."""
        content = self.read_log_file()
        self.assertIn(f"Application Started: {self.app_name} (Version: {self.app_version})", content)
        self.assertIn(f"Initial User Level: {self.user_level}", content)
        self.assertIn(f"Initial Operation Mode: {self.operation_mode}", content)
        self.assertIn(f"Data Storage Mode: Local", content)

    def test_03_log_permission_level_change(self):
        """Test logging of permission level changes."""
        old_level = self.logger_instance.user_level
        new_level = "AdminUser"
        self.logger_instance.log_permission_level_change(new_level)
        content = self.read_log_file()
        self.assertIn(f"Permission Level Changed: From {old_level} to {new_level}", content)
        self.assertEqual(self.logger_instance.user_level, new_level)

    def test_04_log_mode_change(self):
        """Test logging of operation mode changes."""
        old_mode = self.logger_instance.operation_mode
        new_mode = "ProductionMode"
        self.logger_instance.log_mode_change(new_mode)
        content = self.read_log_file()
        self.assertIn(f"Operation Mode Changed: From {old_mode} to {new_mode}", content)
        self.assertEqual(self.logger_instance.operation_mode, new_mode)

    def test_05_log_session_start(self):
        """Test logging of session start events."""
        session_type = "Test Data Collection Session"
        self.logger_instance.log_session_start(session_type)
        content = self.read_log_file()
        self.assertIn(f"Session Started: {session_type}", content)

    def test_06_log_data_collection_local(self):
        """Test log_data_collection with local storage (DATA_STORAGE_FLAG=1)."""
        original_instance_flag = self.logger_instance.data_storage_flag
        app_config.DATA_STORAGE_FLAG = 1 # Ensure config module is also set
        self.logger_instance.data_storage_flag = 1

        image_info = ["img1.jpg", "img2.png"]
        totals = {"items": 10, "errors": 1}
        self.logger_instance.log_data_collection(image_info, totals)

        main_log_content = self.read_log_file()
        self.assertIn(f"Data collection event logged to:", main_log_content)

        session_log_files = [f for f in os.listdir(TEST_SESSION_LOGS_PATH) if f.startswith("session_data_") and f.endswith(".log")]
        self.assertTrue(session_log_files, f"No session data log file found in {TEST_SESSION_LOGS_PATH}.")

        latest_session_log_file = max(session_log_files, key=lambda f: os.path.getmtime(os.path.join(TEST_SESSION_LOGS_PATH, f)))
        session_log_path = os.path.join(TEST_SESSION_LOGS_PATH, latest_session_log_file)
        session_log_content = self.read_log_file(session_log_path)

        self.assertIn("Session Type: Data Collection", session_log_content)
        self.assertIn("Image Information:", session_log_content)
        self.assertIn("- img1.jpg", session_log_content)
        self.assertIn("- img2.png", session_log_content)
        self.assertIn("Totals:", session_log_content)
        self.assertIn("- items: 10", session_log_content)
        self.assertIn("- errors: 1", session_log_content)

        self.logger_instance.data_storage_flag = original_instance_flag
        # app_config.DATA_STORAGE_FLAG will be reset in tearDown

    def test_07_log_data_collection_online_placeholder(self):
        """Test log_data_collection with online storage (DATA_STORAGE_FLAG=0)."""
        original_instance_flag = self.logger_instance.data_storage_flag
        app_config.DATA_STORAGE_FLAG = 0
        self.logger_instance.data_storage_flag = 0

        image_info = "online_img.raw"
        totals = {"status": "uploaded"}
        self.logger_instance.log_data_collection(image_info, totals)
        content = self.read_log_file()
        self.assertIn("Data collection event (Online Storage - Not Implemented):", content)
        self.assertIn(f"Image Info: {image_info}", content)
        self.assertIn(f"Totals: {totals}", content)

        self.logger_instance.data_storage_flag = original_instance_flag
        # app_config.DATA_STORAGE_FLAG will be reset in tearDown

if __name__ == '__main__':
    # This block is for direct script execution, usually for debugging.
    # Prefer using a test runner like 'python -m unittest discover -s app/tests' from the project root.

    # Attempt to create a dummy config.py if not found in project root, for standalone run.
    current_script_path = os.path.dirname(os.path.abspath(__file__))
    project_root_path = os.path.abspath(os.path.join(current_script_path, "../../"))
    dummy_config_path = os.path.join(project_root_path, "config.py")

    if not os.path.exists(dummy_config_path):
        print(f"Warning: Dummy config.py not found. Attempting to create at {dummy_config_path} for standalone test run.")
        try:
            with open(dummy_config_path, "w") as f:
                f.write("LOGS_DIR_NAME = 'logs_dummy'\n")
                f.write("SESSION_LOGS_PATH = 'logs_dummy/sessions'\n")
                f.write("IMAGE_LOGS_PATH = 'logs_dummy/images'\n")
                f.write("APP_TITLE = 'Dummy Test App'\n")
                f.write("APP_VERSION = '0.0-dummy'\n")
                f.write("DATA_STORAGE_FLAG = 1\n")
                f.write("DEFAULT_USER_LEVEL = 'operator'\n")
                f.write("DEFAULT_OPERATION_MODE_ID = 1\n")
                f.write("APP_MODES = {1: 'Mode1_dummy', 2: 'Mode2_dummy'}\n")
        except Exception as e:
            print(f"Could not create dummy config.py: {e}")

    unittest.main(verbosity=2)
