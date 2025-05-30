# temp/app/src/about_page.py

from PyQt6.QtWidgets import (
    QDialog, QLabel, QVBoxLayout, QDialogButtonBox, QTextBrowser, QFrame
)
from PyQt6.QtGui import QFont, QPixmap
from PyQt6.QtCore import Qt

import config 

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"About {config.APP_TITLE}")
        self.setModal(True)
        self.setMinimumSize(450, 400) 
        self.setWindowState(Qt.WindowState.WindowMaximized)  # Start maximized

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12) 

        # --- Logo ---
        logo_label = QLabel(self)
        pixmap = QPixmap(config.LOGO_PATH)
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaledToWidth(200, Qt.TransformationMode.SmoothTransformation))
        else:
            logo_label.setText("Logo N/A")
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)
        layout.addSpacing(5)

        # --- App Title and Version ---
        title_font = QFont("Arial", 16, QFont.Weight.Bold)
        app_title_label = QLabel(f"{config.APP_TITLE} - {config.APP_VERSION}") 
        app_title_label.setFont(title_font)
        app_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(app_title_label)

        # --- Description ---
        description_text = (
            "This application spearheads automation in the beef packing industry. "
            "It utilizes computer vision to meticulously analyze the ribbing cut, "
            "made between the 12th and 13th ribs, grading each as 'Good' or 'Bad' "
            "and providing key data to support quality assurance processes."
        )
        description_label = QLabel(description_text)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(description_label)
        
        layout.addSpacing(10)

        # --- Separator ---
        separator = QFrame(self)
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator)
        layout.addSpacing(10)

        # --- Contact Information ---
        contact_title_label = QLabel("Contact Information")
        contact_font = QFont("Arial", 10, QFont.Weight.Bold)
        contact_title_label.setFont(contact_font)
        contact_title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(contact_title_label)

        # Website Link
        website_url = "http://www.MidWestMachinellc.com"
        website_display = "www.MidWestMachinellc.com"
        website_label = QTextBrowser(self)
        website_label.setHtml(f"<div align='center'>Website: <a href='{website_url}'>{website_display}</a></div>")
        website_label.setOpenExternalLinks(True)
        website_label.setFixedHeight(30) 
        website_label.setStyleSheet("QTextBrowser { border: none; background-color: transparent; }")
        layout.addWidget(website_label)

        # Support Email
        support_email_address = "justin@midwestmachinellc.com"
        email_label = QTextBrowser(self)
        email_label.setHtml(f"<div align='center'>Support: <a href='mailto:{support_email_address}'>{support_email_address}</a></div>")
        email_label.setOpenExternalLinks(True)
        email_label.setFixedHeight(30)
        email_label.setStyleSheet("QTextBrowser { border: none; background-color: transparent; }")
        layout.addWidget(email_label)
        
        layout.addStretch(1)

        # --- Copyright ---
        copyright_text = "© 2025 MidWest Machine LLC. All rights reserved. Proprietary software."
        copyright_label = QLabel(copyright_text) 
        copyright_font = QFont("Arial", 8)
        copyright_label.setFont(copyright_font) 
        copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(copyright_label)
        layout.addSpacing(5)

        # --- OK Button ---
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)