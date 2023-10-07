import sys
from cx_Freeze import setup, Executable

# Include additional files or packages if needed
additional_files = []

# Include tkinter
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # For Windows GUI applications

executables = [
    Executable("myapp.py", base=base, icon="logo.ico"),  # Replace with your main script and icon file
]

options = {
    "build_exe": {
        "includes": [],  # Add additional modules here if needed
        "include_files": additional_files,
    },
}

setup(
    name="MyApp",
    version="1.0",
    description="Description of your app",
    executables=executables,
    options=options,
)