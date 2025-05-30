import os

# --- Application Information ---
APP_TITLE = "Beef Ribbing Automation System"
COMPANY_NAME = "MidWest Machine LLC"
DEPARTMENT_NAME = "Automation R&D Department"
APP_VERSION = ""

# --- Path Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR_NAME = "assets"
LOGO_FILENAME = "Mwlogo.png"
LOGO_PATH = os.path.join(PROJECT_ROOT, ASSETS_DIR_NAME, LOGO_FILENAME)
LOGS_DIR_NAME = "logs"
SESSION_LOGS_PATH = os.path.join(PROJECT_ROOT, LOGS_DIR_NAME, "sessions")
IMAGE_LOGS_PATH = os.path.join(PROJECT_ROOT, LOGS_DIR_NAME, "images")


# --- User Configuration ---
APP_USERS = {
    "Maintenance": {"password": "maintenance123"},
    "Admin": {"password": "admin123"},
    "System": {"password": None}
}
DEFAULT_USER_LEVEL = "System"

# --- Operation Modes ---
APP_MODES = {
    1: "Data Collection",
    2: "Test",
    3: "Production"
}
DEFAULT_OPERATION_MODE_ID = 1
OPERATION_MODE_CONFIG_KEY = "current_operation_mode_id"

# --- Data Storage Configuration ---
# 0 for Online (Google Drive/SQL - placeholder), 1 for Offline (Local)
DATA_STORAGE_FLAG = 1 
ONLINE_DB_CONFIG = {"host": "your_db_host", "db_name": "your_db", "user": "your_user", "password": "your_password"} 

# --- Default Camera Configuration ---
CAMERA_RESOLUTION_WIDTH = 1280
CAMERA_RESOLUTION_HEIGHT = 720
CAMERA_FPS = 30
CAMERA_ROTATION_OPTION = 1 