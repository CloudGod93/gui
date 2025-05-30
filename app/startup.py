import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QGraphicsOpacityEffect
)
from PyQt6.QtGui import QFont, QColor, QLinearGradient, QBrush, QPainter, QPixmap, QPen
from PyQt6.QtCore import (
    Qt, QPropertyAnimation, QEasingCurve, QSequentialAnimationGroup,
    QRect, QPoint, pyqtSignal, QTimer, pyqtProperty, QPointF
)

from config import LOGO_PATH, COMPANY_NAME, DEPARTMENT_NAME

class LoadingSpinner(QWidget):
    def __init__(self, parent=None, color=Qt.GlobalColor.white, minimumTrailOpacity=3.0, rotationSpeed=60, diameter=30, lines=12):
        super().__init__(parent)
        self._color = QColor(color)
        self._minimumTrailOpacity = min(100.0, minimumTrailOpacity)
        self._rotationSpeed = rotationSpeed
        self._diameter = diameter
        self._lines = max(1, lines)
        
        self._timer = QTimer(self)
        self._timer.timeout.connect(self.rotate)
        self._timer.start(int(self._rotationSpeed))
        
        self._current_rotation_angle = 0.0
        self.setFixedSize(diameter + 10, diameter + 10)

    @pyqtProperty(QColor)
    def color(self):
        return self._color

    @color.setter
    def color(self, color):
        self._color = QColor(color)
        self.update() 

    @pyqtProperty(int)
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, diameter):
        self._diameter = diameter
        self.setFixedSize(diameter + 10, diameter + 10)
        self.update()

    def rotate(self):
        self._current_rotation_angle = (self._current_rotation_angle + (360.0 / self._lines)) % 360.0
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        centerX = self.width() / 2.0
        centerY = self.height() / 2.0
        painter.translate(centerX, centerY)
        pen = QPen()
        pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        pen.setWidth(max(2, self._diameter // 10))

        for i in range(self._lines):
            angle_diff = (i * (360.0 / self._lines)) - self._current_rotation_angle
            if angle_diff < 0:
                angle_diff += 360.0
            opacity_factor = 1.0 - (angle_diff / 360.0)
            opacity = max(self._minimumTrailOpacity / 100.0, opacity_factor**2)
            current_color = QColor(self._color)
            current_color.setAlphaF(opacity)
            pen.setColor(current_color)
            painter.setPen(pen)
            painter.rotate(360.0 / self._lines)
            inner_radius = self._diameter / 4.0
            outer_radius = self._diameter / 2.0
            painter.drawLine(QPointF(0, inner_radius), QPointF(0, outer_radius))

class SplashScreen(QWidget):
    animation_finished_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.main_window_instance = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.SplashScreen)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.setFixedSize(450, 350)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel()
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        pixmap = QPixmap(LOGO_PATH) 
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(scaled_pixmap)
        else:
            self.logo_label.setText("LOGO (Not Found)")
            self.logo_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
            self.logo_label.setStyleSheet("color: white;")
        
        self.company_name_label = QLabel(COMPANY_NAME) 
        self.company_name_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        self.company_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.company_name_label.setStyleSheet("color: white;")

        self.department_label = QLabel(DEPARTMENT_NAME) 
        self.department_label.setFont(QFont("Arial", 16, QFont.Weight.Normal))
        self.department_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.department_label.setStyleSheet("color: #FFCDD2;")

        self.spinner = LoadingSpinner(self, color=Qt.GlobalColor.white, diameter=30, rotationSpeed=60)

        self.loading_text_label = QLabel("Loading...")
        self.loading_text_label.setFont(QFont("Arial", 12))
        self.loading_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loading_text_label.setStyleSheet("color: #EEEEEE;")

        layout.addWidget(self.logo_label)
        layout.addSpacing(15)
        layout.addWidget(self.company_name_label)
        layout.addSpacing(5)
        layout.addWidget(self.department_label)
        layout.addSpacing(25)
        layout.addWidget(self.spinner, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.loading_text_label)

        self.logo_opacity_effect = QGraphicsOpacityEffect(self.logo_label)
        self.logo_label.setGraphicsEffect(self.logo_opacity_effect)
        self.logo_opacity_effect.setOpacity(0.0)

        self.company_name_opacity_effect = QGraphicsOpacityEffect(self.company_name_label)
        self.company_name_label.setGraphicsEffect(self.company_name_opacity_effect)
        self.company_name_opacity_effect.setOpacity(0.0)

        self.department_opacity_effect = QGraphicsOpacityEffect(self.department_label)
        self.department_label.setGraphicsEffect(self.department_opacity_effect)
        self.department_opacity_effect.setOpacity(0.0)

        self.spinner_opacity_effect = QGraphicsOpacityEffect(self.spinner)
        self.spinner.setGraphicsEffect(self.spinner_opacity_effect)
        self.spinner_opacity_effect.setOpacity(0.0)

        self.loading_text_opacity_effect = QGraphicsOpacityEffect(self.loading_text_label)
        self.loading_text_label.setGraphicsEffect(self.loading_text_opacity_effect)
        self.loading_text_opacity_effect.setOpacity(0.0)
        
        self.center_on_screen()
        self.overall_animation = QSequentialAnimationGroup(self)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(25, 50, 100))
        gradient.setColorAt(1, QColor(50, 100, 200))
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(self.rect(), 20, 20)

    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        if screen_geometry:
            self.move(screen_geometry.center() - self.rect().center())
        else:
            screens = QApplication.screens()
            if screens:
                 desktop = screens[0].availableGeometry()
                 self.move(desktop.center() - self.rect().center())

    def start_animation(self, main_window):
        self.main_window_instance = main_window
        anim_logo_fadein = QPropertyAnimation(self.logo_opacity_effect, b"opacity")
        anim_logo_fadein.setDuration(800)
        anim_logo_fadein.setStartValue(0.0)
        anim_logo_fadein.setEndValue(1.0)
        anim_logo_fadein.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_company_fadein = QPropertyAnimation(self.company_name_opacity_effect, b"opacity")
        anim_company_fadein.setDuration(800)
        anim_company_fadein.setStartValue(0.0)
        anim_company_fadein.setEndValue(1.0)
        anim_company_fadein.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_department_fadein = QPropertyAnimation(self.department_opacity_effect, b"opacity")
        anim_department_fadein.setDuration(600)
        anim_department_fadein.setStartValue(0.0)
        anim_department_fadein.setEndValue(1.0)
        anim_department_fadein.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_spinner_fadein = QPropertyAnimation(self.spinner_opacity_effect, b"opacity")
        anim_spinner_fadein.setDuration(500)
        anim_spinner_fadein.setStartValue(0.0)
        anim_spinner_fadein.setEndValue(1.0)
        anim_spinner_fadein.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_loading_text_fadein = QPropertyAnimation(self.loading_text_opacity_effect, b"opacity")
        anim_loading_text_fadein.setDuration(500)
        anim_loading_text_fadein.setStartValue(0.0)
        anim_loading_text_fadein.setEndValue(1.0)
        anim_loading_text_fadein.setEasingCurve(QEasingCurve.Type.InOutQuad)

        anim_splash_fadeout = QPropertyAnimation(self, b"windowOpacity")
        anim_splash_fadeout.setDuration(500)
        anim_splash_fadeout.setStartValue(1.0)
        anim_splash_fadeout.setEndValue(0.0)
        anim_splash_fadeout.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.overall_animation.addAnimation(anim_logo_fadein)
        self.overall_animation.addPause(100)
        self.overall_animation.addAnimation(anim_company_fadein)
        self.overall_animation.addPause(50)
        self.overall_animation.addAnimation(anim_department_fadein)
        self.overall_animation.addPause(300)
        self.overall_animation.addAnimation(anim_spinner_fadein)
        self.overall_animation.addAnimation(anim_loading_text_fadein)
        self.overall_animation.addPause(2000)
        self.overall_animation.addAnimation(anim_splash_fadeout)
        
        self.overall_animation.finished.connect(self._on_animation_finished)
        
        self.setWindowOpacity(1.0)
        self.show()
        self.overall_animation.start()

    def _on_animation_finished(self):
        if self.main_window_instance:
            self.main_window_instance.showMaximized()
        self.animation_finished_signal.emit()
        self.close()