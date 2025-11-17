# Troubleshooting Dashboard - Step by Step Guide

## 🔍 Problem: Browser not opening http://localhost:5000

Let's fix this step by step!

---

## ✅ STEP 1: Check if Server is Running

### Look at your terminal/command prompt:
- **If you see**: "Running on http://127.0.0.1:5000" → Server is running ✅
- **If you see**: "PS C:\Users\..." (just prompt) → Server is NOT running ❌

### If server is NOT running:
1. **Start it again:**
   ```bash
   python technician_dashboard.py
   ```
2. **Wait for this message:**
   ```
   * Running on http://127.0.0.1:5000
   ```
3. **Keep the terminal window open!** (Don't close it)

---

## ✅ STEP 2: Test Simple Flask Server First

### Run this test to verify everything works:
```bash
python test_dashboard_simple.py
```

**Expected output:**
```
============================================================
SIMPLE TEST SERVER
============================================================
Open: http://localhost:5001
Press Ctrl+C to stop
============================================================
 * Running on http://127.0.0.1:5001
```

### Then open in browser:
- Go to: **http://localhost:5001**
- You should see: "✅ Flask is Working!"

**If this works:** Flask is fine, problem is with main dashboard
**If this doesn't work:** Continue to Step 3

---

## ✅ STEP 3: Check Browser Issues

### Try Different URLs:
1. **http://localhost:5000**
2. **http://127.0.0.1:5000**
3. **http://0.0.0.0:5000**

### Try Different Browsers:
- Chrome
- Firefox
- Edge
- Internet Explorer

### Check Browser Console:
1. Press **F12** in browser
2. Click **Console** tab
3. Look for error messages
4. Share any errors you see

---

## ✅ STEP 4: Check Port Issues

### Check if Port 5000 is Already in Use:

**Windows PowerShell:**
```powershell
netstat -ano | findstr :5000
```

**If you see output:** Port is in use by another program
**Solution:** Use a different port (see Step 5)

### Check Firewall:
- Windows Firewall might be blocking
- Try temporarily disabling firewall
- Or add exception for Python

---

## ✅ STEP 5: Use Different Port

### Edit `technician_dashboard.py`:

Find this line (near the end):
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Change to:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Then run again:
```bash
python technician_dashboard.py
```

### Open in browser:
**http://localhost:5001**

---

## ✅ STEP 6: Check for Errors in Terminal

### Look for error messages in terminal:

**Common errors:**

1. **"Address already in use"**
   - Port is taken
   - Solution: Use different port (Step 5)

2. **"ModuleNotFoundError: No module named 'Flask'"**
   - Flask not installed
   - Solution: `pip install Flask`

3. **"Can't connect to database"**
   - Database connection issue
   - Solution: Check database credentials

4. **"Template not found"**
   - HTML file missing
   - Solution: Check `templates/technician_dashboard.html` exists

---

## ✅ STEP 7: Verify Files Exist

### Check these files exist:
```bash
dir technician_dashboard.py
dir templates\technician_dashboard.html
```

**If files missing:**
- Re-download or recreate them
- Make sure `templates` folder exists

---

## ✅ STEP 8: Run with Error Details

### Add this to see detailed errors:

Edit `technician_dashboard.py`, change last line to:
```python
if __name__ == '__main__':
    try:
        print("=" * 60)
        print("Technician Dashboard Server Starting...")
        print("=" * 60)
        print("Open your browser and go to: http://localhost:5000")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        app.run(debug=True, host='127.0.0.1', port=5000)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
```

---

## ✅ STEP 9: Test Database Connection Separately

### Run this first:
```bash
python test_connection.py
```

**If this fails:** Database connection is the problem
**If this works:** Database is fine, problem is with Flask/HTML

---

## ✅ STEP 10: Minimal Test

### Create minimal test file `minimal_test.py`:

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello! If you see this, Flask works!</h1>'

if __name__ == '__main__':
    print("Open: http://localhost:5002")
    app.run(port=5002)
```

### Run it:
```bash
python minimal_test.py
```

### Open: http://localhost:5002

**If this works:** Flask works, problem is with dashboard code
**If this doesn't work:** Flask installation issue

---

## 🐛 Common Issues & Solutions

### Issue 1: "This site can't be reached"
**Solutions:**
- Make sure server is running
- Check URL is correct
- Try http://127.0.0.1:5000 instead of localhost
- Check firewall

### Issue 2: "Connection refused"
**Solutions:**
- Server not running - start it
- Wrong port - check terminal output
- Firewall blocking - disable temporarily

### Issue 3: "500 Internal Server Error"
**Solutions:**
- Check terminal for error messages
- Check database connection
- Check HTML template exists

### Issue 4: Blank page
**Solutions:**
- Check browser console (F12)
- Check terminal for errors
- Verify database has data

### Issue 5: "Template not found"
**Solutions:**
- Make sure `templates` folder exists
- Make sure `technician_dashboard.html` is in `templates` folder
- Check file name spelling

---

## 📋 Quick Checklist

- [ ] Server is running (see terminal output)
- [ ] Terminal shows "Running on http://..."
- [ ] Browser URL is correct
- [ ] Tried different browsers
- [ ] Checked browser console (F12)
- [ ] Checked terminal for errors
- [ ] Port not in use
- [ ] Firewall not blocking
- [ ] Files exist (technician_dashboard.py, templates folder)
- [ ] Database connection works (test_connection.py)

---

## 🚀 Quick Fix - Try This First

1. **Stop any running servers** (Ctrl+C)
2. **Run simple test:**
   ```bash
   python test_dashboard_simple.py
   ```
3. **Open:** http://localhost:5001
4. **If that works, then run:**
   ```bash
   python technician_dashboard.py
   ```
5. **Open:** http://127.0.0.1:5000 (try this instead of localhost)

---

## 💡 Still Not Working?

**Share with me:**
1. What error message you see (browser or terminal)
2. Screenshot of terminal output
3. Screenshot of browser (if it opens)
4. Browser console errors (F12 → Console)

I'll help you fix it! 🔧

