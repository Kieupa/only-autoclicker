@echo off
echo ========================================
echo OnlyAutoclicker - Build Script
echo ========================================
echo.

REM Try to find Python
where python >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=python
    goto :found_python
)

where py >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    set PYTHON_CMD=py
    goto :found_python
)

echo ERROR: Python not found!
echo Please install Python 3.7+ from https://www.python.org/
echo Make sure to check "Add Python to PATH" during installation.
pause
exit /b 1

:found_python
echo Found Python: %PYTHON_CMD%
echo.

echo Installing/updating dependencies...
%PYTHON_CMD% -m pip install --upgrade pip
%PYTHON_CMD% -m pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo WARNING: Failed to install from requirements.txt!
    echo Trying alternative method...
    %PYTHON_CMD% -m pip install pyautogui keyboard Pillow pyinstaller
    if %ERRORLEVEL% NEQ 0 (
        echo ERROR: Failed to install dependencies!
        pause
        exit /b 1
    )
    echo Dependencies installed via alternative method.
)

echo.
echo Building executable...
%PYTHON_CMD% -m PyInstaller --onefile --windowed --name=OnlyAutoclicker --clean --noconfirm --hidden-import=pyautogui --hidden-import=keyboard --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=tkinter --hidden-import=tkinter.ttk main.py

echo.
if exist "dist\OnlyAutoclicker.exe" (
    echo ========================================
    echo ✓ Build successful!
    echo ========================================
    echo Executable location: %CD%\dist\OnlyAutoclicker.exe
    echo.
    echo You can now run OnlyAutoclicker.exe from the dist folder!
) else (
    echo ========================================
    echo ✗ Build failed!
    echo ========================================
    echo Check the error messages above.
)

echo.
pause

