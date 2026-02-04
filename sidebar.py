# responsibility
# Mode / Switch / Power buttons
# Expandable menu
# Mode-specific items

from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt
from pet import resource_path
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtCore import QUrl

BLUE = "#A7C7E7"
PINK = "#F4A6C1"


class Sidebar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.mode = "chill"

        # Main layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(5, 0, 5, 0)
        self.layout.setSpacing(5)  # Spacing between menu and button bar

        # 1. Menu container (appears above buttons)
        self.menu_container = QWidget()
        self.menu_layout = QVBoxLayout(self.menu_container)
        self.menu_layout.setContentsMargins(0, 0, 0, 0)
        self.menu_layout.setSpacing(2)  # Reduced spacing between menu functions
        self.menu_container.hide()

        # Add a spacer so the menu "grows" upwards and keeps buttons at the bottom
        self.layout.addStretch()
        self.layout.addWidget(self.menu_container, alignment=Qt.AlignmentFlag.AlignBottom)

        # 2. Fixed horizontal button bar
        self.button_bar = QWidget()
        self.button_layout = QHBoxLayout(self.button_bar)
        self.button_layout.setContentsMargins(0, 0, 0, 50)  # Added bottom margin
        self.button_layout.setSpacing(4)

        self.mode_btn = QPushButton("Menu")
        self.switch_btn = QPushButton("Switch")
        self.power_btn = QPushButton("✖")  # Power icon

        # Apply consistent styling
        for btn in [self.mode_btn, self.switch_btn, self.power_btn]:
            btn.setFixedSize(60, 30)  # Fixed larger size
            btn.setStyleSheet(f"background-color: {BLUE}; border-radius: 10px; font-weight: bold;")

        # Highlight the Switch button specifically
        self.switch_btn.setStyleSheet(f"background-color: {PINK}; border-radius: 10px; font-weight: bold;")

        self.button_layout.addWidget(self.mode_btn)
        self.button_layout.addWidget(self.switch_btn)
        self.button_layout.addWidget(self.power_btn)

        self.button_layout.addStretch(1)

        self.layout.addWidget(self.button_bar)

        # Connect
        self.mode_btn.clicked.connect(self.toggle_menu)
        self.switch_btn.clicked.connect(self.show_mode_selection)
        self.power_btn.clicked.connect(parent.power_off)

    def clear_menu(self):
        while self.menu_layout.count():
            item = self.menu_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def toggle_menu(self):
        if self.menu_container.isVisible():
            self.menu_container.hide()
            return

        self.clear_menu()
        items = ["摸摸 ^^", "away~", "豚馒宇宙"] if self.mode == "chill" else ["Todos", "Notes", "away~"]

        for item in items:
            btn = QPushButton(item)
            btn.setFixedSize(188, 28)  # Wide buttons to match the bar width
            btn.setStyleSheet(
                f"background-color: white; border-radius: 6px; border: 2px solid {BLUE}; font-weight: bold;")
            # btn.clicked.connect(lambda _, t=item: print(f"{t} clicked"))
            self.menu_layout.addWidget(btn)
            if item == "摸摸 ^^":
                btn.clicked.connect(self.parent().pet.play_interaction)
            elif item == "away~":
                btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.bilibili.com/video/BV1h1kcBfEuJ/?spm_id_from=333.1007.top_right_bar_window_default_collection.content.click&vd_source=ae78803ea852364af36eaf1d7c327038")))
            else:
                btn.clicked.connect(lambda _, t=item: print(f"{t} clicked"))
            self.menu_layout.addWidget(btn)

        self.menu_container.show()

    def show_mode_selection(self):
        if self.menu_container.isVisible():
            self.menu_container.hide()
            return

        self.clear_menu()
        for m in ["Chill", "Work"]:
            btn = QPushButton(m)
            btn.setFixedSize(188, 28)  # Larger buttons for mode selection
            btn.setStyleSheet(
                f"background-color: white; border-radius: 6px; border: 2px solid {PINK}; font-weight: bold;")
            btn.clicked.connect(lambda _, x=m: self.set_mode(x))
            self.menu_layout.addWidget(btn)
        self.menu_container.show()

    def set_mode(self, mode):
        self.mode = mode.lower()
        self.menu_container.hide()

        # Rest of your set_mode logic for changing the GIF...
        if self.mode == "chill":
            # self.parent().pet.movie.stop()
            self.parent().pet.stop_work_timer()
            from PyQt6.QtGui import QMovie
            self.parent().pet.movie = QMovie(resource_path("assets/hedwig_emocat.gif"))
            self.parent().pet.movie.frameChanged.connect(self.parent().pet.scale_frame)
            self.parent().pet.setMovie(self.parent().pet.movie)
            self.parent().pet.movie.start()
        else:
            """
            self.parent().pet.movie.stop()
            from PyQt6.QtGui import QMovie
            self.parent().pet.movie = QMovie(resource_path("assets/workmode3.gif"))
            self.parent().pet.movie.frameChanged.connect(self.parent().pet.scale_frame)
            self.parent().pet.setMovie(self.parent().pet.movie)
            self.parent().pet.movie.start()
            """
            self.parent().pet.start_work_timer()
            # Start with the first work gif
            self.parent().pet.change_work_gif(0)