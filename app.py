import sys
from PyQt6.QtWidgets import QApplication

from startup import SplashScreen
from main_window import MainWindow 

if __name__ == "__main__":
    app = QApplication(sys.argv)

    splash = SplashScreen()
    main_w = MainWindow()

    splash.start_animation(main_w)
    
    sys.exit(app.exec())