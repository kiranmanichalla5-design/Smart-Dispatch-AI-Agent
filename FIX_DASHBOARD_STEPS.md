# 🔧 Fix Dashboard - Follow These Steps

## Problem: Browser not opening http://localhost:5000

---

## ✅ STEP 1: Make Sure Server is Running

### Check your terminal/command prompt:

**You should see:**
```
* Running on http://127.0.0.1:5000
```

**If you DON'T see this:**
1. Run: `python technician_dashboard.py`
2. Wait for "Running on..." message
3. **Keep terminal open!**

---

## ✅ STEP 2: Try the SIMPLIFIED Version First

### This version doesn't need templates folder:

```bash
python technician_dashboard_simple.py
```

**You'll see:**
```
============================================================
SIMPLIFIED TECHNICIAN DASHBOARD
============================================================
✅ No templates needed - everything embedded
✅ Open in browser: http://127.0.0.1:5003
✅ Press Ctrl+C to stop
============================================================
```

### Then open in browser:
**http://127.0.0.1:5003**

**This should work!** If it does, the problem is with the template file.

---

## ✅ STEP 3: If Simplified Version Works

### Fix the main dashboard:

1. **Check templates folder exists:**
   ```bash
   dir templates
   ```

2. **Check HTML file exists:**
   ```bash
   dir templates\technician_dashboard.html
   ```

3. **If files are missing:**
   - Make sure `templates` folder is in same directory as `technician_dashboard.py`
   - Make sure `technician_dashboard.html` is inside `templates` folder

---

## ✅ STEP 4: Try Different URLs

### Try these in your browser (one at a time):

1. **http://127.0.0.1:5000** ← Try this first!
2. **http://localhost:5000**
3. **http://0.0.0.0:5000**

**Sometimes `127.0.0.1` works when `localhost` doesn't!**

---

## ✅ STEP 5: Check What Error You See

### In Browser:

**If you see:**
- "This site can't be reached" → Server not running
- "Connection refused" → Server not running or wrong port
- "500 Internal Server Error" → Check terminal for error
- Blank page → Check browser console (F12)

### In Terminal:

**Look for error messages like:**
- "Template not found" → HTML file missing
- "Address already in use" → Port taken, use different port
- "Can't connect to database" → Database issue

---

## ✅ STEP 6: Use Different Port

### If port 5000 is taken:

Edit `technician_dashboard.py`, find this line (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5000)
```

Change to:
```python
app.run(debug=True, host='127.0.0.1', port=5004)
```

Then open: **http://127.0.0.1:5004**

---

## ✅ STEP 7: Test Database Connection

### Make sure database works:

```bash
python test_connection.py
```

**If this fails:** Database is the problem
**If this works:** Database is fine

---

## 🚀 QUICK FIX - Try This Now!

### Option 1: Use Simplified Version (Easiest)

```bash
python technician_dashboard_simple.py
```

Then open: **http://127.0.0.1:5003**

**This should definitely work!**

---

### Option 2: Fix Main Dashboard

1. **Stop any running servers** (Ctrl+C)

2. **Check files exist:**
   ```bash
   dir technician_dashboard.py
   dir templates
   dir templates\technician_dashboard.html
   ```

3. **If templates folder missing:**
   ```bash
   mkdir templates
   ```
   (Then make sure HTML file is in there)

4. **Run with specific host:**
   Edit last line to:
   ```python
   app.run(debug=True, host='127.0.0.1', port=5000)
   ```

5. **Run again:**
   ```bash
   python technician_dashboard.py
   ```

6. **Open:** http://127.0.0.1:5000

---

## 📋 Checklist

- [ ] Server is running (see "Running on..." in terminal)
- [ ] Tried http://127.0.0.1:5000 (not just localhost)
- [ ] Tried simplified version (technician_dashboard_simple.py)
- [ ] Checked terminal for error messages
- [ ] Checked browser console (F12)
- [ ] Templates folder exists
- [ ] HTML file exists in templates folder
- [ ] Database connection works (test_connection.py)

---

## 💡 Most Likely Issues

1. **Server not running** → Start it with `python technician_dashboard.py`
2. **Wrong URL** → Try `http://127.0.0.1:5000` instead of `localhost`
3. **Template missing** → Use `technician_dashboard_simple.py` instead
4. **Port in use** → Use different port (5003, 5004, etc.)

---

## 🎯 Recommended: Use Simplified Version

**The simplified version (`technician_dashboard_simple.py`) is easier and should work immediately!**

It:
- ✅ Doesn't need templates folder
- ✅ Everything embedded in one file
- ✅ Easier to debug
- ✅ Same functionality

**Just run:**
```bash
python technician_dashboard_simple.py
```

**Then open:** http://127.0.0.1:5003

---

## ❓ Still Not Working?

**Tell me:**
1. What happens when you run `python technician_dashboard_simple.py`?
2. What do you see in terminal?
3. What error (if any) in browser?
4. What happens when you open http://127.0.0.1:5003?

I'll help you fix it! 🔧

