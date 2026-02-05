import os

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QListWidgetItem, QLabel, QFrame, \
    QPushButton
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QPixmap, QIcon
from pet import resource_path
import json


class TodoWindow(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 1. Unified Sheet Design: White background + Pink Border
        self.setFixedSize(300, 450)
        self.setStyleSheet("""
            QFrame#MainFrame {
                background-color: white;
                border: 4px solid #F4A6C1;
                border-radius: 20px;
            }
            QLineEdit {
                border: 2px solid #A7C7E7;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
                background: #fdfdfd;
            }
            QListWidget {
                border: 2px solid #F4A6C1;
                border-radius: 8px;
                padding: 5px;
                font-size: 14px;
                background: #fdfdfd;
            }
        """)
        self.setObjectName("MainFrame")

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(15, 15, 15, 80)  # Large bottom margin for the image

        # Title
        self.title = QLabel("Todo List")
        self.title.setStyleSheet("color: #F4A6C1; font-size: 14px; font-weight: bold; border: none;")
        self.layout.addWidget(self.title)

        # Input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type task and press Enter...")
        self.input_field.returnPressed.connect(self.add_task)
        self.layout.addWidget(self.input_field)

        # 2. Checklist and Delete Functionality
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.toggle_item_check)
        # Enable double-click to delete
        self.list_widget.itemDoubleClicked.connect(self.delete_task)
        self.layout.addWidget(self.list_widget)

        # Instruction label
        self.info = QLabel("Double-click a task to delete it")
        self.info.setStyleSheet("color: gray; font-size: 10px; border: none;")
        self.layout.addWidget(self.info)

        # 1. Install event filters on widgets that usually block dragging
        self.list_widget.installEventFilter(self)
        self.title.installEventFilter(self)
        # We don't filter the input_field so you can still click it to type

        self.drag_pos = None

        # 3. Larger Bottom-Right Image
        self.deco_img = QLabel(self)
        pixmap = QPixmap(resource_path("../assets/todo.png"))
        if not pixmap.isNull():
            # Scaled to be larger as requested
            self.deco_img.setPixmap(
                pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))

        # Position it at the bottom right corner
        self.deco_img.setGeometry(195, 245, 100, 100)
        self.deco_img.setStyleSheet("border: none; background: transparent;")

        self.drag_pos = None

        # for storage
        self.save_file = "todo_storage.json"
        self.load_tasks()

    def add_task(self):
        text = self.input_field.text().strip()
        if text:
            item = QListWidgetItem(text)
            # Add a checkbox to the item
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.list_widget.addItem(item)
            self.input_field.clear()
            self.save_tasks()  # Save after adding

    def toggle_item_check(self, item):
        font = item.font()
        # Toggle the state
        if item.checkState() == Qt.CheckState.Checked:
            # Task was just checked (or was already checked)
            font.setStrikeOut(True)
            item.setFont(font)
            item.setForeground(Qt.GlobalColor.gray)
        else:
            # Task is unchecked
            font.setStrikeOut(False)
            item.setFont(font)
            item.setForeground(Qt.GlobalColor.black)

            # Optional: update the list widget to ensure the change is visible immediately
        self.list_widget.update()

        self.save_tasks()

    def delete_task(self, item):
        self.list_widget.takeItem(self.list_widget.row(item))
        self.save_tasks()  # Save after deleting

    def eventFilter(self, source, event):
        """Intercepts events from child widgets to allow dragging"""
        if event.type() == event.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                # Map the click from the child widget to the main window's coordinates
                self.drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
                return False  # Let the child still handle the click (for checking tasks)

        elif event.type() == event.Type.MouseMove:
            if self.drag_pos:
                self.move(event.globalPosition().toPoint() - self.drag_pos)
                return True  # Stop the child from scrolling while we drag

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

    def create_task_item(self, text, check_state):
        """Helper to create an item with the correct font styling"""
        item = QListWidgetItem(text)
        item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
        item.setCheckState(check_state)

        # Apply strikethrough immediately if it's already checked
        if check_state == Qt.CheckState.Checked:
            font = item.font()
            font.setStrikeOut(True)
            item.setFont(font)
            item.setForeground(Qt.GlobalColor.gray)

        return item

    def save_tasks(self):
        """Saves all tasks in the list to a JSON file"""
        tasks = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            tasks.append({
                "text": item.text(),
                "completed": item.checkState() == Qt.CheckState.Checked
            })

        with open(self.save_file, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=4)

    def load_tasks(self):
        """Loads tasks from the JSON file on startup"""
        if not os.path.exists(self.save_file):
            return

        try:
            with open(self.save_file, "r", encoding="utf-8") as f:
                tasks = json.load(f)
                for task in tasks:
                    state = Qt.CheckState.Checked if task["completed"] else Qt.CheckState.Unchecked
                    item = self.create_task_item(task["text"], state)
                    self.list_widget.addItem(item)
        except Exception as e:
            print(f"Error loading tasks: {e}")