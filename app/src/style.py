ACCENT_STYLESHEET = """
    QMenuBar {
        background-color: rgb(45, 85, 150); 
        color: white;
        font-family: Arial;
        font-size: 10pt; 
        padding: 2px; 
    }
    QMenuBar::item {
        background-color: transparent;
        padding: 6px 12px; 
        color: white;
        border-radius: 3px; 
    }
    QMenuBar::item:selected { 
        background-color: rgb(65, 105, 170); 
    }
    QMenuBar::item:pressed {
        background-color: rgb(35, 75, 140); 
    }

    QMenu {
        background-color: rgb(50, 90, 160); 
        color: white;
        border: 1px solid rgb(65, 105, 170); 
        font-family: Arial;
        font-size: 10pt;
        padding: 2px; 
    }
    QMenu::item {
        padding: 6px 24px; 
    }
    QMenu::item:selected {
        background-color: rgb(65, 105, 170); 
    }
    QMenu::separator {
        height: 1px;
        background: rgb(65, 105, 170);
        margin-left: 5px;
        margin-right: 5px;
        margin-top: 2px;
        margin-bottom: 2px;
    }

    QPushButton {
        background-color: rgb(65, 105, 170); 
        color: white;
        border: 1px solid rgb(80, 120, 185); 
        padding: 8px 16px; 
        font-family: Arial;
        border-radius: 4px;
    }
    QPushButton:hover {
        background-color: rgb(80, 120, 185); 
    }
    QPushButton:pressed {
        background-color: rgb(50, 90, 160); 
    }
    QPushButton:disabled {
        background-color: rgb(140, 140, 140); 
        color: rgb(210, 210, 210);
        border-color: rgb(160, 160, 160);
    }

    QStatusBar {
        background-color: rgb(45, 85, 150); 
        color: white;
        font-family: Arial;
        font-size: 9pt; 
    }
    QStatusBar::item {
        border: none; 
    }
"""