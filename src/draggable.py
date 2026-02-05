from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class DraggableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.drag_start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Store the click position relative to the label's top-left
            self.drag_start_pos = event.position().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_start_pos is not None:
            # Calculate the new position relative to the parent (the Pet)
            new_pos = self.mapToParent(event.position().toPoint() - self.drag_start_pos)
            self.move(new_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_start_pos = None
        event.accept()