# Animal Classifier Server Startup Script
# Run this script to start the Flask server

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host " 🐾 Animal Classifier Server" -ForegroundColor Yellow
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Change to script directory
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "📂 Working Directory: $scriptPath" -ForegroundColor Green
Write-Host ""

# Check if model file exists
if (-not (Test-Path "animals10_model.keras")) {
    Write-Host "❌ ERROR: Model file not found!" -ForegroundColor Red
    Write-Host "   Expected: animals10_model.keras" -ForegroundColor Red
    Write-Host ""
    Write-Host "   Please ensure the model file is in the same directory as this script." -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "✅ Model file found: animals10_model.keras" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python not found!" -ForegroundColor Red
    Write-Host "   Please install Python 3.9+ from python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🚀 Starting Flask server..." -ForegroundColor Cyan
Write-Host "   Please wait for model to load (10-15 seconds)..." -ForegroundColor Yellow
Write-Host ""
Write-Host "📋 Watch for this message:" -ForegroundColor Magenta
Write-Host "   ✅ Model loaded successfully!" -ForegroundColor Green
Write-Host "   🚀 Starting Flask app on port 5000" -ForegroundColor Green
Write-Host ""
Write-Host "🌐 Once started, open your browser to:" -ForegroundColor Cyan
Write-Host "   http://127.0.0.1:5000" -ForegroundColor White -BackgroundColor DarkBlue
Write-Host ""
Write-Host "⚠️  IMPORTANT: Keep this window open while using the website!" -ForegroundColor Yellow
Write-Host "   Press Ctrl+C to stop the server when done" -ForegroundColor Yellow
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Start the Flask app
try {
    python app.py
} catch {
    Write-Host ""
    Write-Host "❌ Server stopped or error occurred" -ForegroundColor Red
    Write-Host ""
}

Write-Host ""
Write-Host "Server has stopped." -ForegroundColor Yellow
Read-Host "Press Enter to exit"
