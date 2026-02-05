import os
import sys

from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QPoint, pyqtSignal, QTimer

from draggable import DraggableLabel


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Pet(QLabel):
    clicked = pyqtSignal()
    # Signal to tell the sidebar or window to show/hide the back button
    unlocked_stage = pyqtSignal(int)

    def __init__(self, gif_path="assets/hedwig_emocat.gif", width=200):
        super().__init__()
        self.drag_position = QPoint()
        self.width = width

        # Load the GIF
        full_path = resource_path(gif_path)
        self.movie = QMovie(full_path)
        self.setMovie(self.movie)

        # Whenever the frame changes, scale it
        self.movie.frameChanged.connect(self.scale_frame)

        self.movie.start()

        self.work_gifs = [
            "assets/workmode2.gif",
            "assets/workmode3.gif",
            "assets/workmode.gif"
        ]
        self.current_work_index = 0
        self.max_unlocked_index = 0

        # Timer for work evolution (checks every minute)
        self.work_timer = QTimer(self)
        self.work_timer.timeout.connect(self.update_work_time)
        self.minutes_elapsed = 0

        # 1. Change QLabel to DraggableLabel
        self.bubble_label = DraggableLabel(self)  # Use our new class
        self.bubble_label.setFixedSize(self.width, self.width)
        self.bubble_label.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Set a starting position
        self.bubble_label.move(40, -40)

        # 2. Load the bubble GIF (Keep your existing movie logic)
        self.bubble_movie = QMovie(resource_path("assets/touch.gif"))
        from PyQt6.QtCore import QSize
        self.bubble_movie.setScaledSize(QSize(self.width, self.width))
        self.bubble_label.setMovie(self.bubble_movie)
        self.bubble_label.hide()

    def play_interaction(self):
        self.bubble_label.show()
        self.bubble_movie.start()
        # Automatically hide after 3 seconds
        QTimer.singleShot(6000, self.bubble_label.hide)

    def scale_frame(self):
        # Get current frame and scale it
        pixmap = self.movie.currentPixmap()
        if not pixmap.isNull():
            scaled = pixmap.scaled(
                self.width,
                self.width,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.setPixmap(scaled)
            self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = (
                event.globalPosition().toPoint()
                - self.parentWidget().frameGeometry().topLeft()
            )
            self.clicked.emit()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.MouseButton.LeftButton:
            self.parentWidget().move(
                event.globalPosition().toPoint() - self.drag_position
            )
            event.accept()

    def start_work_timer(self):
        self.minutes_elapsed = 0
        self.current_work_index = 0
        self.max_unlocked_index = 0
        self.work_timer.start(60000)  # 60,000 ms = 1 minute

    def stop_work_timer(self):
        self.work_timer.stop()

    def update_work_time(self):
        self.minutes_elapsed += 1
        # print(f"Work Time: {self.minutes_elapsed} min")  # Debugging help

        new_stage = 0
        if self.minutes_elapsed >= 20:
            new_stage = 2
        elif self.minutes_elapsed >= 10:
            new_stage = 1

        if new_stage > self.max_unlocked_index:
            self.max_unlocked_index = new_stage
            self.change_work_gif(new_stage)
            self.unlocked_stage.emit(new_stage)

    def change_work_gif(self, index):
        self.current_work_index = index
        self.movie.stop()
        self.movie = QMovie(resource_path(self.work_gifs[index]))
        self.movie.frameChanged.connect(self.scale_frame)
        self.setMovie(self.movie)
        self.movie.start()

    def power_off(self):
        print("Pet: Goodbye 👋")
        QApplication.quit()

