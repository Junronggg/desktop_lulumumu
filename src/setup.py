from cx_Freeze import setup, Executable
import sys
import os

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # hides the console window

# include your assets and Qt plugins
venv_root = os.path.dirname(os.path.dirname(sys.executable))  # goes up from Scripts -> .venv

includefiles = [
    ("../assets", "assets"),  # copy assets folder to build folder
    (os.path.join(venv_root, "Lib\\site-packages\\PyQt6\\Qt6\\bin"), "Qt6/bin"),
    (os.path.join(venv_root, "Lib\\site-packages\\PyQt6\\Qt6\\plugins"), "Qt6/plugins")
]


setup(
    name="Desktop_lulumumu",
    version="1.0",
    description="Desktop pet for lulumumu",
    options={"build_exe": {"include_files": includefiles}},
    executables=[Executable("main.py", base=base)]
)
