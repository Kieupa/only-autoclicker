# OnlyAutoclicker

A fully functional autoclicker application with a user-friendly GUI.

## Features

- **Customizable Click Interval**: Set click speed from 0.01 to 10 seconds
- **Multiple Click Types**: Left, Right, or Middle mouse button clicks
- **Flexible Positioning**: 
  - Click at current mouse position
  - Click at custom coordinates
- **Click Count Options**:
  - Infinite clicking
  - Custom number of clicks
- **Hotkey Support**:
  - **F6**: Toggle Start/Stop
  - **F7**: Force Stop
- **Real-time Status**: See click count and current status
- **Easy to Use**: Simple, intuitive interface

## Installation

1. Make sure you have Python 3.7+ installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Building Executable (.exe)

To create a standalone .exe file:

**Option 1: Using the batch file (Windows)**
```bash
build.bat
```

**Option 2: Using Python script**
```bash
python build_exe.py
```

**Option 3: Manual build**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=OnlyAutoclicker --clean --noconfirm --hidden-import=pyautogui --hidden-import=keyboard --hidden-import=PIL main.py
```

The executable will be created in the `dist` folder as `OnlyAutoclicker.exe`

## Usage

1. Run the application:

**From Python:**
```bash
python main.py
```

**From executable:**
```bash
dist\OnlyAutoclicker.exe
```

2. Configure your settings:
   - Set the click interval (how fast to click)
   - Choose click type (Left/Right/Middle)
   - Select position (Current mouse or custom coordinates)
   - Set number of clicks (Infinite or custom amount)
   - Enable/disable hotkeys

3. Click "Start" or press **F6** to begin clicking
4. Click "Stop" or press **F7** to stop clicking

## Hotkeys

- **F6**: Toggle Start/Stop clicking
- **F7**: Force stop clicking

## Requirements

- Python 3.7+
- Windows, macOS, or Linux
- Administrator/root privileges may be required for hotkey functionality on some systems

## Notes

- The autoclicker will click at the specified position at the set interval
- Use "Get Current Position" button to capture your mouse coordinates
- Hotkeys work globally (even when the window is not focused)
- Be careful when using infinite clicking mode

## License

MIT
