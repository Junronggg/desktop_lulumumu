from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QPoint, pyqtSignal

class Pet(QLabel):
    clicked = pyqtSignal()

    def __init__(self, gif_path="assets/hedwig_emocat.gif", width=200):
        super().__init__()
        self.drag_position = QPoint()
        self.width = width

        # Load the GIF
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)

        # Whenever the frame changes, scale it
        self.movie.frameChanged.connect(self.scale_frame)

        self.movie.start()

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

    def power_off(self):
        print("Pet: Goodbye 👋")
        QApplication.quit()

