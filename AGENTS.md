# AGENTS.md

## Cursor Cloud specific instructions

### Overview

OnlyAutoclicker is a single-file Python tkinter desktop GUI application (`main.py`) that automates mouse clicks and keyboard key presses. No backend services, databases, or Docker are needed.

### Running the application

```bash
python3 main.py
```

The app requires a display server (X11/Xvfb). In Cursor Cloud, `DISPLAY=:1` is already set and Xvfb is running, so `python3 main.py` works directly.

### Dependencies

- **System**: `python3-tk` (must be installed via apt; not included by default in Cloud VMs)
- **Python**: see `requirements.txt` — install with `pip3 install -r requirements.txt`
- The `keyboard` library requires root privileges for global hotkey hooks on Linux. In the Cloud VM environment, the app runs as `ubuntu` user, so the keyboard library loads but hotkey registration may silently fail. The app degrades gracefully (hotkeys disabled).

### Lint / Test / Build

- No linter or test framework is configured in this repo. Use `python3 -m py_compile main.py` to check for syntax errors.
- Build executable (not required for development): `python3 build_exe.py` (uses PyInstaller). See `BUILD_INSTRUCTIONS.md`.

### Gotchas

- `pyautogui.FAILSAFE` is disabled in the app code. Be careful when testing click automation — it will click wherever the mouse is.
- The interval input uses a 100:1 ratio (value / 100 = seconds). For example, 100 = 1 second delay.
