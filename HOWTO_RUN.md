# 🚀 How to Run the Animal Classifier Website

## Problem
The "model not loaded" error occurs when the Flask server isn't running or has crashed.

## Solution: Keep the Server Running

### Method 1: Using the Batch File (Recommended for Windows)
1. Double-click `run_server.bat`
2. Wait for the message: "✅ Model loaded successfully!"
3. Open your browser to: http://127.0.0.1:5000
4. **Keep the command window open** while using the website
5. Press Ctrl+C to stop the server when done

### Method 2: Using Command Prompt
1. Open Command Prompt
2. Navigate to the project:
   ```
   cd d:\Matchine_Learning\CampusX\tutorial\AI_project
   ```
3. Run:
   ```
   python app.py
   ```
4. Wait for "✅ Model loaded successfully!"
5. Open browser to: http://127.0.0.1:5000
6. **Keep the terminal open**

### Method 3: Using VS Code Terminal
1. Open a terminal in VS Code (Terminal → New Terminal)
2. Run:
   ```powershell
   cd d:\Matchine_Learning\CampusX\tutorial\AI_project
   python app.py
   ```
3. Wait for the success message
4. Open: http://127.0.0.1:5000
5. **Keep the terminal running**

## Checking if Server is Running

Test the health endpoint in your browser:
```
http://127.0.0.1:5000/health
```

You should see:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "Animal Classification API is running 🚀"
}
```

## Common Issues

### Issue 1: "Model not loaded"
**Cause:** Server isn't running or crashed
**Fix:** Start the server using one of the methods above

### Issue 2: Server starts then immediately stops
**Cause:** Python error or port already in use
**Fix:** 
- Check if another program is using port 5000
- Look for error messages in the terminal
- Try a different port by editing app.py (change PORT=5000 to PORT=8000)

### Issue 3: Can't connect to server
**Cause:** Server not running or wrong URL
**Fix:**
- Make sure server is running (see terminal output)
- Use: http://127.0.0.1:5000 (NOT https)
- Check firewall settings

## Server Output to Look For

When the server starts successfully, you'll see:
```
INFO:__main__:Loading model from: ...animals10_model.keras
INFO:__main__:Model file size: 10.42 MB
INFO:__main__:✅ Model loaded successfully!
INFO:__main__:🚀 Starting Flask app on port 5000
 * Running on http://127.0.0.1:5000
```

## Testing the Website

1. Ensure server is running
2. Open: http://127.0.0.1:5000
3. Click the upload area or drag an image
4. Click "🔮 Predict Animal"
5. Wait for the result

## Stopping the Server

When done:
- Press `Ctrl+C` in the terminal
- Or close the command window

## For Production Deployment

For deploying to Render or other platforms, see DEPLOYMENT.md

---

**Remember:** The Flask development server must remain running in a terminal while you use the website. This is normal for local development!
