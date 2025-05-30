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
    "Maintenance": {"password": "maintenance123"},
    "Admin": {"password": "admin123"},
    "System": {"password": None} 
}
DEFAULT_USER_LEVEL = "System"