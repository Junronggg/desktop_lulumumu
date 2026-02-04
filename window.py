# window.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication, QPushButton
from PyQt6.QtCore import Qt
from pet import Pet
from sidebar import Sidebar
class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)

        self.pet = Pet("assets/hedwig_emocat.gif")
        self.sidebar = Sidebar(self)
        self.sidebar.hide()

        # Connect click to toggle sidebar
        self.pet.clicked.connect(self.toggle_sidebar)
        # When pet evolves or is double-clicked, we adjust window size
        self.pet.unlocked_stage.connect(self.adjustSize)

        layout.addWidget(self.pet)
        layout.addWidget(self.sidebar)

        self.adjustSize()
        self.show()

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())
        self.adjustSize()

    def keyPressEvent(self, event):
        # 1. Left Arrow Key -> Go Back
        if event.key() == Qt.Key.Key_Left:
            if self.pet.current_work_index > 0:
                self.pet.change_work_gif(self.pet.current_work_index - 1)
                self.adjustSize()

        # 2. Right Arrow Key -> Go Forward (if unlocked)
        elif event.key() == Qt.Key.Key_Right:
            if self.pet.current_work_index < self.pet.max_unlocked_index:
                self.pet.change_work_gif(self.pet.current_work_index + 1)
                self.adjustSize()

        super().keyPressEvent(event)

    # Add this to __init__ to make sure the window catches keys immediately
    # self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def power_off(self):
        if hasattr(self, "pet") and getattr(self.pet, "movie", None):
            self.pet.movie.stop()
        QApplication.instance().quit()