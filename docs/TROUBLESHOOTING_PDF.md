# Troubleshooting: ModuleNotFoundError for xhtml2pdf

## Problem
Getting error: `ModuleNotFoundError: No module named 'xhtml2pdf'` when running Streamlit app.

## Root Cause
Streamlit is running with a Python interpreter that doesn't have `xhtml2pdf` installed. This usually happens when:
1. Virtual environment is not activated
2. Multiple Python installations exist on the system
3. Streamlit was installed globally, not in the venv
4. Terminal/IDE is using wrong Python

## Solutions (Try in Order)

### Solution 1: Use the Startup Script (Easiest)
```bash
cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering/AI-Powered-CBG"
./start.sh
```

This script automatically:
- Activates the virtual environment
- Installs missing dependencies
- Starts Streamlit with correct Python

### Solution 2: Manual Activation
```bash
# 1. Navigate to project
cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering/AI-Powered-CBG"

# 2. Activate venv
source venv/bin/activate

# 3. Verify Python
which python
which streamlit

# 4. Install xhtml2pdf in venv
pip install xhtml2pdf

# 5. Run Streamlit
streamlit run app.py
```

### Solution 3: Reinstall Everything in Venv
```bash
# Navigate to project
cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering/AI-Powered-CBG"

# Delete venv (start fresh)
rm -rf venv

# Create new venv
python3 -m venv venv

# Activate
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "streamlit|xhtml2pdf"

# Run app
streamlit run app.py
```

### Solution 4: Install in Streamlit's Python
Find which Python Streamlit is using and install there:

```bash
# Find Streamlit's Python
which streamlit
# Output might be: /usr/local/bin/streamlit

# Find the Python interpreter
head -1 $(which streamlit)
# Will show something like: #!/usr/bin/python3

# Install xhtml2pdf for that Python
/usr/bin/python3 -m pip install xhtml2pdf
```

### Solution 5: Disable PDF Feature (Temporary)
The app now gracefully handles missing xhtml2pdf. If you run without it:
- Markdown download will still work
- PDF button will show "PDF export not available"
- App will run normally otherwise

## Verification Steps

### Step 1: Check Virtual Environment
```bash
# Should show venv's Python
which python
# Expected: /Users/.../AI-Powered-CBG/venv/bin/python

# Should show venv's Streamlit
which streamlit
# Expected: /Users/.../AI-Powered-CBG/venv/bin/streamlit
```

### Step 2: Test Import
```bash
python -c "from xhtml2pdf import pisa; print('✅ Success')"
```

### Step 3: Check Streamlit's Python
```bash
streamlit --version
python -c "import streamlit; import sys; print('Streamlit Python:', sys.executable)"
```

### Step 4: Verify Installation
```bash
pip show xhtml2pdf
# Should show: Location: .../venv/lib/python.../site-packages
```

## Prevention

### Always Activate Venv Before Running
Add to your shell profile (~/.zshrc or ~/.bashrc):

```bash
# Alias for quick activation
alias cbg-app='cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering/AI-Powered-CBG" && source venv/bin/activate && streamlit run app.py'
```

Then just run: `cbg-app`

### Use VS Code Python Interpreter
If using VS Code:
1. Press Cmd+Shift+P
2. Search: "Python: Select Interpreter"
3. Choose: ".../AI-Powered-CBG/venv/bin/python"
4. VS Code terminal will auto-activate venv

## Common Mistakes

❌ **Running from wrong directory**
```bash
# Wrong:
cd ~/
streamlit run app.py
```

✅ **Correct:**
```bash
cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering/AI-Powered-CBG"
source venv/bin/activate
streamlit run app.py
```

❌ **Installing globally**
```bash
# Wrong (installs for system Python):
pip install xhtml2pdf
```

✅ **Correct:**
```bash
# Activate venv first:
source venv/bin/activate
pip install xhtml2pdf
```

❌ **Multiple terminals**
```bash
# Terminal 1: Activated venv and installed packages
# Terminal 2: Different terminal, venv NOT activated ❌
```

✅ **Correct:**
- Always activate venv in each new terminal
- Or use the start.sh script

## Still Not Working?

### Check for Multiple Python Installations
```bash
# List all Python installations
which -a python python3

# Check each one
/usr/bin/python3 --version
/usr/local/bin/python3 --version
venv/bin/python --version
```

### Check sys.path
```bash
python -c "import sys; print('\\n'.join(sys.path))"
```

Should include paths like:
- `.../AI-Powered-CBG/venv/lib/python3.12/site-packages`

### Nuclear Option: Clean Reinstall
```bash
# Remove everything
cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering"
rm -rf "AI-Powered-CBG/venv"
rm -rf "AI-Powered-CBG/__pycache__"

# Fresh start
cd "AI-Powered-CBG"
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Verify
pip list | grep xhtml2pdf

# Run
./start.sh
```

## Quick Reference

```bash
# ✅ Correct way to run app
cd "/Users/shubhranshumohanty/Developer/demo/LLM Engineering/AI-Powered-CBG"
source venv/bin/activate
streamlit run app.py

# OR use the startup script
./start.sh
```

---

**Last Updated**: October 14, 2025
