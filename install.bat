@echo off
setlocal EnableDelayedExpansion

echo Checking Python installation...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Installing...
    
    :: Create temp directory
    mkdir temp 2>nul
    
    :: Download Python
    set PYTHON_VERSION=3.11.8
    set PYTHON_MSI=python-%PYTHON_VERSION%-amd64.exe
    powershell -Command "(New-Object Net.WebClient).DownloadFile('https://www.python.org/ftp/python/%PYTHON_VERSION%/%PYTHON_MSI%', 'temp\%PYTHON_MSI%')"
    
    :: Install Python
    echo Installing Python %PYTHON_VERSION%...
    temp\%PYTHON_MSI% /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1 Include_tcltk=1
    
    :: Clean up
    rmdir /s /q temp
    
    echo Python installation completed!
)

echo.
echo Checking required Python packages...

:: List of required packages
set PACKAGES=ebooklib python-docx PyPDF2 beautifulsoup4

:: Check and install each package
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

echo.
echo Checking PyInstaller...
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller
        pause
        exit /b 1
    )
)

echo.
echo Creating executable...
pyinstaller --onefile --noconsole --name "Lector Horitzontal" reader.py

:: Move the executable to the current directory
move "dist\Lector Horitzontal.exe" .

:: Clean up PyInstaller files
rmdir /s /q build
rmdir /s /q dist
del "Lector Horitzontal.spec"


echo.
echo All requirements satisfied!
echo You can now run "Lector Horitzontal.exe"
pause
