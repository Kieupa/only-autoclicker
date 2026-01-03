"""
Build script to create .exe file from the autoclicker
"""
import PyInstaller.__main__
import os
import sys

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# PyInstaller arguments
args = [
    'main.py',
    '--onefile',  # Create a single executable file
    '--windowed',  # No console window (GUI only)
    '--name=OnlyAutoclicker',  # Name of the executable
    '--icon=NONE',  # No icon (can add .ico file later if needed)
    '--clean',  # Clean PyInstaller cache
    '--noconfirm',  # Overwrite output directory without asking
]

# Add hidden imports if needed
args.extend([
    '--hidden-import=pyautogui',
    '--hidden-import=keyboard',
    '--hidden-import=PIL',
    '--hidden-import=PIL._tkinter_finder',
    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
])

print("Building executable...")
print(f"Working directory: {script_dir}")

try:
    PyInstaller.__main__.run(args)
    print("\n✓ Build completed successfully!")
    print(f"Executable location: {script_dir}\\dist\\OnlyAutoclicker.exe")
except Exception as e:
    print(f"\n✗ Build failed: {e}")
    sys.exit(1)

