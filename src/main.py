import os
import sys

if getattr(sys, "frozen", False):
    # Add PyQt6 DLLs to PATH for PyInstaller EXE
    qt_bin = os.path.join(sys._MEIPASS, "PyQt6", "Qt6", "bin")
    os.environ["PATH"] = qt_bin + os.pathsep + os.environ.get("PATH", "")

# now import PyQt6 safely
from PyQt6.QtWidgets import QApplication
from window import DesktopPet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet()
    sys.exit(app.exec())
