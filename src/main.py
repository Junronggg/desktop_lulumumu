# main.py
import sys
from PyQt6.QtWidgets import QApplication
from window import DesktopPet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
