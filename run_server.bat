@echo off
cd /d "%~dp0"
echo.
echo ======================================
echo   Animal Classifier Server
echo ======================================
echo.
echo Current directory: %CD%
echo.

REM Check if model file exists
if not exist "animals10_model.keras" (
    echo ERROR: Model file not found!
    echo Expected: animals10_model.keras
    echo.
    pause
    exit /b 1
)

echo Model file found: animals10_model.keras
echo.
echo Starting Flask Server...
echo Please wait 10-15 seconds for model to load...
echo.
echo Watch for: Model loaded successfully!
echo.
echo Once started, open your browser to:
echo http://127.0.0.1:5000
echo.
echo IMPORTANT: Keep this window open while using the website!
echo Press Ctrl+C to stop the server when done
echo.
echo ======================================
echo.

python app.py

echo.
echo Server has stopped.
pause
