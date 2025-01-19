@echo off
setlocal EnableDelayedExpansion

echo Checking Python installation...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not installed. Installing...
    
    :: Create temp directory
    mkdir temp 2>nul
    
    :: Download Python 3.11.8
    set PYTHON_VERSION=3.11.8
    set PYTHON_INSTALLER=python-%PYTHON_VERSION%-amd64.exe
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_INSTALLER%', 'temp\%PYTHON_INSTALLER%')"
    
    :: Install Python
    echo Installing Python %PYTHON_VERSION%...
    temp\%PYTHON_INSTALLER% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_tcltk=1
    
    :: Delete temp directory
    rmdir /s /q temp
    
    echo Python installation completed!
)

echo.
echo Checking required Python packages...

:: List of required packages
set PACKAGES=ebooklib python-docx PyPDF2 beautifulsoup4

:: Check and install each package if not installed
for %%p in (%PACKAGES%) do (
    python -c "import %%p" 2>nul
    if errorlevel 1 (
        echo Installing %%p...
        python -m pip install %%p
        if errorlevel 1 (
            echo Failed to install %%p
            pause
            exit /b 1
        )
    ) else (
        echo %%p is already installed
    )
)

:: Check PyInstaller (required to create the .exe file)
echo.
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller
        echo You can still use the program using "Lector Horitzontal.bat"
        pause
        exit /b 1
    )
)

echo.
echo Creating executable...
pyinstaller --onefile --noconsole --name "Lector Horitzontal" main.py

:: Move the executable to the current directory
move "dist\Lector Horitzontal.exe" .

:: Delete up PyInstaller files
rmdir /s /q build
rmdir /s /q dist
del "Lector Horitzontal.spec"


echo.
echo Everything setup!
echo You can now run "Lector Horitzontal.exe"
pause
