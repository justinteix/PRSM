@echo off
echo.
echo ========================================
echo    Prism AI Voice Assistant
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python -c "import flask, openai, elevenlabs" >nul 2>&1
if errorlevel 1 (
    echo Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error: Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Check if .env file exists
if not exist config\.env (
    echo Creating .env file from template...
    if not exist config mkdir config
    copy docs\env_example.txt config\.env
    echo.
    echo Please edit the config\.env file and add your API keys before running again.
    echo.
    pause
    exit /b 1
)

REM Run the application
echo Starting Prism...
echo.
echo Open your browser and go to: http://localhost:5000
echo Press Ctrl+C to stop the application
echo.
python main.py

pause 