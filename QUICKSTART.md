# ⚡ Quick Start Guide

## The "Model Not Loaded" Error - SOLVED! ✅

### The Problem
You're getting "model not loaded" because the Flask server isn't running or has stopped.

### The Solution
**You must keep the Flask server running in a terminal while using the website!**

## 🚀 How to Start the Server

### Option 1: Double-Click (Easiest!)
1. **Double-click**: `run_server.bat` (Windows)
2. Wait for: "✅ Model loaded successfully!"
3. Open browser: http://127.0.0.1:5000
4. **Keep the window open!**

### Option 2: PowerShell
1. Right-click `start_server.ps1` → Run with PowerShell
2. Wait for success message
3. Open browser: http://127.0.0.1:5000
4. **Keep the window open!**

### Option 3: VS Code Terminal
```powershell
cd AI_project
python app.py
```

## ✅ How to Know It's Working

You'll see this in the terminal:
```
INFO:__main__:✅ Model loaded successfully!
INFO:__main__:🚀 Starting Flask app on port 5000
 * Running on http://127.0.0.1:5000
```

Test it by visiting: http://127.0.0.1:5000/health

## 🎯 Using the Website

1. ✅ **Ensure server is running** (see above)
2. Open: http://127.0.0.1:5000
3. Upload an animal image
4. Click "Predict Animal"
5. See the result!

## ⚠️ Important Notes

- **Keep the terminal/window open** while using the website
- The server takes 10-15 seconds to load the model
- Press `Ctrl+C` to stop the server when done
- If you close the terminal, the website stops working

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Model not loaded" | Start the server (see above) |
| Server immediately closes | Check for errors in terminal |
| Can't connect | Use http://127.0.0.1:5000 (not https) |
| Port already in use | Another program is using port 5000 |

## 📚 More Help

- See: [HOWTO_RUN.md](HOWTO_RUN.md) for detailed instructions
- See: [DEPLOYMENT.md](DEPLOYMENT.md) for deploying online
- See: [README.md](README.md) for full project documentation

---

**Remember:** Flask development server = terminal must stay open! 🖥️
