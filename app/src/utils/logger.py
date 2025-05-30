import os
import datetime
import logging
# Assuming config.py is in the parent directory of 'app' or accessible in PYTHONPATH
# If app.py is in the root and runs from there, 'from config import ...' should work if 'config.py' is also in the root.
# For robustness if the structure is 'root/app/src/utils' and 'root/config.py',
# and the execution context is 'root', then 'from config import ...' is fine.
# If the execution context might change, or for better modularity,
# consider passing config values during Logger initialization or using relative imports if config was part of the app package.
# For now, we'll stick to the direct import as per existing structure in the file.
from config import APP_TITLE, APP_VERSION, LOGS_DIR_NAME, SESSION_LOGS_PATH, IMAGE_LOGS_PATH, DATA_STORAGE_FLAG

class Logger:
    def __init__(self, app_name, app_version, user_level, operation_mode):
        self.app_name = app_name
        self.app_version = app_version
        self.user_level = user_level
        self.operation_mode = operation_mode
        self.data_storage_flag = DATA_STORAGE_FLAG

        log_dir_path = LOGS_DIR_NAME
        if not os.path.exists(log_dir_path):
            os.makedirs(log_dir_path)

        if self.data_storage_flag == 1: # Local
            if not os.path.exists(SESSION_LOGS_PATH):
                os.makedirs(SESSION_LOGS_PATH)
            if not os.path.exists(IMAGE_LOGS_PATH):
                os.makedirs(IMAGE_LOGS_PATH)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_name = f"{self.app_name.replace(' ', '_')}_{timestamp}.log"
        self.log_file_path = os.path.join(log_dir_path, log_file_name)

        self.logger = logging.getLogger(self.app_name)
        self.logger.setLevel(logging.INFO)

        if not self.logger.handlers:
            fh = logging.FileHandler(self.log_file_path)
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
            fh.setFormatter(formatter)
            self.logger.addHandler(fh)

        self.logger.info(f"Application Started: {self.app_name} (Version: {self.app_version})")
        self.logger.info(f"Timestamp: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.logger.info(f"Initial User Level: {self.user_level}")
        self.logger.info(f"Initial Operation Mode: {self.operation_mode}")
        self.logger.info(f"Data Storage Mode: {'Local' if self.data_storage_flag == 1 else 'Online'}")

    def log_permission_level_change(self, new_level):
        self.logger.info(f"Permission Level Changed: From {self.user_level} to {new_level}")
        self.user_level = new_level

    def log_mode_change(self, new_mode):
        self.logger.info(f"Operation Mode Changed: From {self.operation_mode} to {new_mode}")
        self.operation_mode = new_mode

    def log_session_start(self, session_type):
        self.logger.info(f"Session Started: {session_type}")

    def log_data_collection(self, image_info, totals):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        if self.data_storage_flag == 1: # Local storage
            session_file_name = f"session_data_{timestamp}.log"
            session_file_path = os.path.join(SESSION_LOGS_PATH, session_file_name)
            try:
                with open(session_file_path, 'a') as f:
                    f.write(f"Timestamp: {timestamp}\n")
                    f.write(f"Session Type: Data Collection\n")
                    f.write(f"User Level: {self.user_level}\n")
                    f.write(f"Operation Mode: {self.operation_mode}\n")
                    f.write("Image Information:\n")
                    if isinstance(image_info, list):
                        for info in image_info:
                            f.write(f"  - {info}\n")
                    else:
                        f.write(f"  - {image_info}\n")
                    f.write("Totals:\n")
                    if isinstance(totals, dict):
                        for key, value in totals.items():
                            f.write(f"  - {key}: {value}\n")
                    else:
                        f.write(f"  - {totals}\n")
                    f.write("-" * 30 + "\n")
                self.logger.info(f"Data collection event logged to: {session_file_path}")
            except Exception as e:
                self.logger.error(f"Failed to log data collection to file {session_file_path}: {e}")

            if image_info: # Log reference to image storage path
                 self.logger.info(f"Image data related to this session would be stored in: {IMAGE_LOGS_PATH}")

        else: # Online storage
            self.logger.info("Data collection event (Online Storage - Not Implemented):")
            self.logger.info(f"  Image Info: {image_info}")
            self.logger.info(f"  Totals: {totals}")

if __name__ == '__main__':
    # Example Usage
    try:
        from config import APP_TITLE as AT, APP_VERSION as AV
    except ImportError: # Fallback if config is not available for direct script run
        AT = "DefaultApp"
        AV = "0.1-local"

    logger_instance = Logger(AT, AV if AV else "1.0", "Admin", "Data Collection")
    logger_instance.logger.info("This is an initial test log message from __main__.")

    logger_instance.log_permission_level_change("Maintenance")
    logger_instance.log_mode_change("Test Mode")
    logger_instance.log_session_start("Data Collection Test Session")

    test_image_info = ["image1.jpg path_on_disk", "image2.jpg path_on_disk"]
    test_totals = {"items_processed": 150, "defects_found": 5}
    logger_instance.log_data_collection(test_image_info, test_totals)

    logger_instance.log_data_collection("single_image.png", {"total_widgets": 10}) # Test single entries

    # Test online storage logging
    try:
        from config import DATA_STORAGE_FLAG as DSF
        original_dsf = logger_instance.data_storage_flag
        logger_instance.data_storage_flag = 0
        logger_instance.log_data_collection("online_image.jpg", {"online_items": 5})
        logger_instance.data_storage_flag = original_dsf
    except ImportError:
        logger_instance.logger.warning("Could not import DATA_STORAGE_FLAG for online test simulation.")

    print(f"Main application log file is at: {logger_instance.log_file_path}")
    if logger_instance.data_storage_flag == 1:
        print(f"Session logs are in: {SESSION_LOGS_PATH if 'SESSION_LOGS_PATH' in globals() else 'config.SESSION_LOGS_PATH'}")
        print(f"Image logs (directory reference) are in: {IMAGE_LOGS_PATH if 'IMAGE_LOGS_PATH' in globals() else 'config.IMAGE_LOGS_PATH'}")
