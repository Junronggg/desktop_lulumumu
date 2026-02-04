from cx_Freeze import setup, Executable
import PyQt6
import os

# Correct Qt6 DLL folder
qt_bin = os.path.join(os.path.dirname(PyQt6.__file__), "Qt6", "bin")

setup(
    name="DesktopPet",
    version="1.0",
    description="Desktop Pet",
    options={
        "build_exe": {
            "packages": ["PyQt6"],
            "include_files": [
                "assets/",           # your GIFs
                (qt_bin, ".")        # copy all DLLs directly into build folder
            ],
        }
    },
    executables=[Executable("main.py", base="Win32GUI")]
)
