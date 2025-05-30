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

# --- User Configuration ---
APP_USERS = {
    "Maintenance": {"password": "123"},
    "Admin": {"password": "123"},
    "System": {"password": None}
}
DEFAULT_USER_LEVEL = "System" 

# --- Operation Modes ---
APP_MODES = {
    1: "Data Collection",
    2: "Test",
    3: "Production"
}
DEFAULT_OPERATION_MODE_ID = 1 # 1 for Data Collection, 2 for Test, 3 for Production
OPERATION_MODE_CONFIG_KEY = "current_operation_mode_id" 