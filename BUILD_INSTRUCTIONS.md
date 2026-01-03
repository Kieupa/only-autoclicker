# Building OnlyAutoclicker Executable

## Prerequisites

1. **Install Python 3.7 or higher**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **IMPORTANT**: During installation, check "Add Python to PATH"

## Build Steps

### Option 1: Easy Build (Recommended for Windows)

1. Double-click `build.bat` file
2. Wait for the build to complete
3. Find your executable in: `dist\OnlyAutoclicker.exe`

### Option 2: Manual Build

1. Open Command Prompt or PowerShell in the `onlyAutoclicker` folder

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   Or if `pip` doesn't work:
   ```bash
   python -m pip install -r requirements.txt
   ```

3. Build the executable:
   ```bash
   pyinstaller --onefile --windowed --name=OnlyAutoclicker --clean --noconfirm --hidden-import=pyautogui --hidden-import=keyboard --hidden-import=PIL main.py
   ```

4. The executable will be in the `dist` folder

## Troubleshooting

- **"Python not found"**: Make sure Python is installed and added to PATH
- **"pip not recognized"**: Use `python -m pip` instead of just `pip`
- **Build errors**: Make sure all dependencies are installed correctly
- **Antivirus warnings**: Some antivirus software may flag PyInstaller executables as suspicious. This is a false positive. You may need to add an exception.

## Running the Executable

Once built, you can:
- Run `dist\OnlyAutoclicker.exe` directly
- Copy it anywhere and run it (it's a standalone file)
- No Python installation needed on the target machine!

