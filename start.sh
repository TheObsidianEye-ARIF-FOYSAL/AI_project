#!/bin/bash

echo "🚀 Starting deployment script..."

# Check if model exists
if [ ! -f "animals10_model.keras" ]; then
    echo "❌ Model file not found!"
    echo "📦 Attempting to download model from Google Drive..."
    
    # Install gdown if needed
    pip install -q gdown
    
    # TODO: Replace with your Google Drive file ID
    # gdown <YOUR_FILE_ID> -O animals10_model.keras
    
    echo "⚠️  Please upload model file or configure Google Drive download"
    exit 1
else
    echo "✅ Model file found ($(du -h animals10_model.keras | cut -f1))"
fi

echo "✅ Deployment script completed!"
