#!/usr/bin/env python3
"""
Pre-deployment checks for Render
Run this before pushing to git/deploying to Render
"""

import os
import sys

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description}: {filepath} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description} NOT FOUND: {filepath}")
        return False

def check_file_in_git(filename):
    """Check if file is tracked by git"""
    result = os.popen(f'git ls-files | findstr /I "{filename}"').read().strip()
    if result:
        print(f"✅ {filename} is tracked in git")
        return True
    else:
        print(f"⚠️  {filename} is NOT in git (might be in .gitignore)")
        return False

def main():
    print("=" * 60)
    print("🔍 Pre-Deployment Checks for Render")
    print("=" * 60)
    print()
    
    all_ok = True
    
    # Check required files
    print("📁 Checking required files...")
    print("-" * 60)
    required_files = [
        ("animals10_model.keras", "Model file"),
        ("app.py", "Flask app"),
        ("requirements.txt", "Dependencies"),
        ("Procfile", "Render config"),
        ("runtime.txt", "Python version"),
        ("templates/index.html", "Frontend HTML"),
        ("static/script.js", "Frontend JS"),
        ("static/style.css", "Frontend CSS"),
    ]
    
    for filepath, desc in required_files:
        if not check_file_exists(filepath, desc):
            all_ok = False
    
    print()
    
    # Check model file specifically
    print("🤖 Checking model file...")
    print("-" * 60)
    model_path = "animals10_model.keras"
    if os.path.exists(model_path):
        size_mb = os.path.getsize(model_path) / (1024 * 1024)
        print(f"Model size: {size_mb:.2f} MB")
        if size_mb > 100:
            print("⚠️  WARNING: Model file is large (>100MB), may cause issues on Render free tier")
        elif size_mb > 500:
            print("❌ ERROR: Model file too large (>500MB), won't work on Render")
            all_ok = False
        else:
            print("✅ Model size is OK for Render")
    
    print()
    
    # Check git status
    print("📦 Checking Git status...")
    print("-" * 60)
    
    # Check if in git repo
    if os.path.exists(".git"):
        print("✅ Git repository detected")
        
        # Check if model is in git
        check_file_in_git("animals10_model.keras")
        
        # Check for uncommitted changes
        status = os.popen("git status --porcelain").read().strip()
        if status:
            print("⚠️  Uncommitted changes detected:")
            print(status[:500])  # Show first 500 chars
            print("\n💡 Run: git add . && git commit -m 'Your message' && git push")
        else:
            print("✅ No uncommitted changes")
    else:
        print("❌ Not a git repository!")
        all_ok = False
    
    print()
    
    # Check requirements.txt
    print("📋 Checking requirements.txt...")
    print("-" * 60)
    if os.path.exists("requirements.txt"):
        with open("requirements.txt", "r") as f:
            content = f.read()
            required_packages = ["tensorflow", "keras", "flask", "gunicorn", "pillow", "numpy"]
            for package in required_packages:
                if package.lower() in content.lower():
                    print(f"✅ {package} found in requirements.txt")
                else:
                    print(f"❌ {package} NOT found in requirements.txt")
                    all_ok = False
    
    print()
    
    # Check Procfile
    print("⚙️  Checking Procfile...")
    print("-" * 60)
    if os.path.exists("Procfile"):
        with open("Procfile", "r") as f:
            procfile_content = f.read().strip()
            print(f"Procfile content: {procfile_content}")
            if "gunicorn" in procfile_content and "app:app" in procfile_content:
                print("✅ Procfile looks good")
            else:
                print("❌ Procfile may be incorrect")
                all_ok = False
    
    print()
    
    # Check Python version
    print("🐍 Checking Python version...")
    print("-" * 60)
    python_version = sys.version.split()[0]
    print(f"Current Python version: {python_version}")
    
    if os.path.exists("runtime.txt"):
        with open("runtime.txt", "r") as f:
            runtime_version = f.read().strip()
            print(f"runtime.txt specifies: {runtime_version}")
            if runtime_version.startswith("python-"):
                print("✅ runtime.txt format is correct")
            else:
                print("⚠️  runtime.txt format should be: python-3.11.0")
    
    print()
    
    # Final summary
    print("=" * 60)
    if all_ok:
        print("✅ ALL CHECKS PASSED! Ready to deploy to Render! 🚀")
        print()
        print("Next steps:")
        print("1. git add .")
        print("2. git commit -m 'Fix: Model loading for Render deployment'")
        print("3. git push origin main")
        print("4. Render will auto-deploy!")
    else:
        print("❌ SOME CHECKS FAILED! Please fix issues before deploying.")
        print()
        print("Review the errors above and fix them.")
    print("=" * 60)
    
    return 0 if all_ok else 1

if __name__ == "__main__":
    exit(main())
