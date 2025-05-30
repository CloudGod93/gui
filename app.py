import sys
from PyQt6.QtWidgets import QApplication

from app.src.style import ACCENT_STYLESHEET
from app.startup import SplashScreen 
from app.main_window import MainWindow 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(ACCENT_STYLESHEET) 

    splash = SplashScreen() 
    main_w = MainWindow() 

    splash.start_animation(main_w)
    
    sys.exit(app.exec())