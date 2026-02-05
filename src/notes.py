from PyQt6.QtWidgets import QFrame, QVBoxLayout, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap  # CRITICAL: Make sure this is imported!
import json
import os
from pet import resource_path

class NoteWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
        self.setFixedSize(270, 300)

        # 🔹 Outer layout (transparent window)
        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(15, 15, 15, 15)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 🔹 White note card
        self.container = QFrame()
        self.container.setObjectName("MainFrame")
        self.container.setFixedSize(240, 260)
        self.container.setStyleSheet("""
            QFrame#MainFrame {
                background-color: white;
                border: 4px solid #F4A6C1;
                border-radius: 20px;
            }
            QTextEdit {
                border: none;
                background: transparent;
                font-size: 14px;
                color: #555555;
            }
        """)

        outer_layout.addWidget(self.container)

        # 🔹 Layout INSIDE the card
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(15, 15, 10, 85)

        # Title
        self.title = QLabel("notes with 豚豚馒馒")
        self.title.setStyleSheet(
            "color: #A7C7E7; font-size: 14px; font-weight: bold;"
        )
        layout.addWidget(self.title)

        # Text box
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Write something...")
        layout.addWidget(self.text_edit)

        # Decorative image (on top of card)
        self.deco_img = QLabel(self.container)
        pixmap = QPixmap(resource_path("../assets/notes.png"))
        if not pixmap.isNull():
            self.deco_img.setPixmap(
                pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio)
            )

        # Position it at the bottom right corner
        self.deco_img.setGeometry(157, 160, 125, 125)
        self.deco_img.setStyleSheet("border: none; background: transparent;")

        self.save_file = "note_storage.json"
        self.drag_pos = None

        self.load_note()
        self.text_edit.textChanged.connect(self.save_note)
        self.text_edit.installEventFilter(self)

    def save_note(self):
        try:
            content = self.text_edit.toPlainText()
            with open(self.save_file, "w", encoding="utf-8") as f:
                json.dump({"content": content}, f)
        except Exception as e:
            print(f"Save Error: {e}")

    def load_note(self):
        if os.path.exists(self.save_file):
            try:
                with open(self.save_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Block signals so the load doesn't trigger a save
                    self.text_edit.blockSignals(True)
                    self.text_edit.setPlainText(data.get("content", ""))
                    self.text_edit.blockSignals(False)
            except:
                pass

    def show_notes(self):
        if self.note_window is None:
            self.note_window = NoteWindow(self.window())
            # Ensure it stays on top like the pet
            self.note_window.setWindowFlags(
                Qt.WindowType.FramelessWindowHint |
                Qt.WindowType.WindowStaysOnTopHint |
                Qt.WindowType.Tool
            )

        if self.note_window.isVisible():
            self.note_window.hide()
        else:
            pet_pos = self.window().frameGeometry().topLeft()
            self.note_window.move(pet_pos.x() + 300, pet_pos.y())
            self.note_window.show()
            self.note_window.raise_()

    def eventFilter(self, source, event):
        # Check if the event is happening on the text_edit widget
        if source == self.text_edit:
            if event.type() == event.Type.MouseButtonPress:
                if event.button() == Qt.MouseButton.LeftButton:
                    self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                    # Return False so the user can still click to type
                    return False

            elif event.type() == event.Type.MouseMove:
                if self.drag_pos:
                    self.move(event.globalPosition().toPoint() - self.drag_pos)
                    # Return True to stop the text box from selecting text while dragging
                    return True

            elif event.type() == event.Type.MouseButtonRelease:
                self.drag_pos = None

        return super().eventFilter(source, event)

    # Dragging Logic
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(event.globalPosition().toPoint() - self.drag_pos)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None