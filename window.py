# window.py
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QApplication
from PyQt6.QtCore import Qt
from pet import Pet
from sidebar import Sidebar

class DesktopPet(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.pet = Pet("assets/hedwig_emocat.gif")
        self.sidebar = Sidebar(self)
        self.sidebar.hide()

        self.pet.clicked.connect(self.toggle_sidebar)

        layout.addWidget(self.pet)
        layout.addWidget(self.sidebar)

        self.adjustSize()
        self.show()

    def toggle_sidebar(self):
        self.sidebar.setVisible(not self.sidebar.isVisible())
        self.adjustSize()

    def power_off(self):
        # Stop pet GIF if running
        if hasattr(self, "pet") and getattr(self.pet, "movie", None):
            self.pet.movie.stop()
        QApplication.instance().quit()

