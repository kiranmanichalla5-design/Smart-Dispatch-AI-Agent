# Step-by-Step Guide: Getting Started with Smart Dispatch Agent

## 🎯 Goal
Run the smart dispatch agent that automatically matches technicians to service requests.

---

## ✅ STEP 1: Verify Your Setup

### Check if Python is installed:
```bash
python --version
```

**Expected output:** Python 3.8 or higher

**If you see an error:**
- Download Python from: https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Check if you're in the right folder:
```bash
cd C:\Users\ftrhack93\Downloads\Test_Folder
dir
```

**You should see:** `smart_dispatch_agent.py` and other files

---

## ✅ STEP 2: Install Required Packages

### Install the Python packages needed:
```bash
pip install psycopg2-binary
```

**Expected output:** `Successfully installed psycopg2-binary...`

**If you get an error:**
- Try: `python -m pip install psycopg2-binary`
- Or: `pip3 install psycopg2-binary`

---

## ✅ STEP 3: Test Database Connection

### Create a simple test script:
Create a file called `test_connection.py` with this content:

```python
import psycopg2

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

try:
    connection = psycopg2.connect(**DB_CONFIG)
    print("✅ SUCCESS! Connected to database!")
    connection.close()
except Exception as e:
    print(f"❌ ERROR: {e}")
```

### Run the test:
```bash
python test_connection.py
```

**Expected output:** `✅ SUCCESS! Connected to database!`

**If you see an error:**
- Check your internet connection
- Verify the database credentials are correct
- Make sure the database server is accessible

---

## ✅ STEP 4: Run the Smart Dispatch Agent

### Run the main agent:
```bash
python smart_dispatch_agent.py
```

**What it does:**
1. Connects to your database
2. Finds pending dispatches (status = 'pending')
3. Matches technicians based on:
   - Skills
   - Location (distance)
   - Availability
   - Past performance
4. Updates the database with the best match

**Expected output:**
```
================================================================================
SMART DISPATCH AGENT - MVP
================================================================================
✓ Connected to database

🚀 Processing pending dispatches...

🔍 Finding best match for Dispatch ID: 200000495
   Required Skill: Line repair
   Priority: Critical
   Location: Dallas, TX
   Found 5 available technician(s)

📊 Top Candidates:
--------------------------------------------------------------------------------

1. John Smith (T900045)
   Total Score: 0.856
   - Skill Match: 1.00
   - Distance: 12.34 km (score: 0.88)
   ...
✓ Assigned technician T900045 to dispatch 200000495

✅ Processed 5 dispatch(es)
✓ Database connection closed
```

---

## ✅ STEP 5: Verify Results in Database

### Option A: Using DBeaver (Visual)
1. Open DBeaver
2. Connect to your database
3. Navigate to: `Databases → postgres → Schemas → team_core_flux → Tables → current_dispatches`
4. Right-click → "View Data"
5. Look for rows where `Optimization_status = 'completed'`
6. Check the `Optimized_technician_id` column

### Option B: Using SQL Query
Run this in DBeaver SQL editor:

```sql
SET search_path TO "team_core_flux";

SELECT 
    "Dispatch_id",
    "Required_skill",
    "Priority",
    "Optimized_technician_id",
    "Optimization_status",
    "Optimization_confidence"
FROM current_dispatches
WHERE "Optimization_status" = 'completed'
ORDER BY "Dispatch_id"
LIMIT 10;
```

**You should see:**
- Dispatch IDs
- Assigned technician IDs
- Confidence scores (0-1, higher is better)

---

## ✅ STEP 6: Understand What Happened

### The agent:
1. ✅ Found pending dispatches
2. ✅ Searched for available technicians
3. ✅ Calculated scores for each technician
4. ✅ Selected the best match
5. ✅ Updated the database

### Scoring factors:
- **Skill Match (40%)**: Does technician have the required skill?
- **Distance (30%)**: How close is the technician?
- **Availability (20%)**: Is technician available?
- **Performance (10%)**: How well did they do in the past?

---

## 🎯 Next Steps (After Success)

### Step 7: Process Specific Dispatch
If you want to process a specific dispatch:

```python
# Create a file: process_one.py
from smart_dispatch_agent import SmartDispatchAgent

agent = SmartDispatchAgent()
result = agent.process_dispatch(200000495)  # Replace with your dispatch ID
agent.close()
```

Run: `python process_one.py`

### Step 8: Add LLM Intelligence (Advanced)
See `DISPATCH_AGENT_GUIDE.md` for instructions on adding:
- Ollama (free local LLM)
- Claude API (production LLM)
- LangChain integration

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'psycopg2'"
**Solution:**
```bash
pip install psycopg2-binary
```

### Problem: "Connection refused" or database error
**Solution:**
- Check internet connection
- Verify database is accessible
- Check firewall settings

### Problem: "No pending dispatches found"
**Solution:**
- Check if dispatches exist: `SELECT COUNT(*) FROM "team_core_flux"."current_dispatches" WHERE "Optimization_status" = 'pending';`
- If count is 0, all dispatches are already processed

### Problem: "No available technicians found"
**Solution:**
- Check if technicians exist: `SELECT COUNT(*) FROM "team_core_flux"."technicians";`
- Verify state matches: Dispatches and technicians need to be in same state

---

## 📋 Quick Checklist

- [ ] Python installed (`python --version`)
- [ ] In correct folder (`Test_Folder`)
- [ ] Packages installed (`pip install psycopg2-binary`)
- [ ] Database connection works (`test_connection.py`)
- [ ] Agent runs successfully (`python smart_dispatch_agent.py`)
- [ ] Results visible in database (DBeaver or SQL query)

---

## 💡 Tips for Beginners

1. **Run one step at a time** - Don't skip ahead
2. **Read the error messages** - They usually tell you what's wrong
3. **Check the output** - Look for ✅ (success) or ❌ (error)
4. **Use DBeaver** - Visual tool makes it easier to see results
5. **Ask questions** - If stuck, check the error message and ask for help

---

## 🎉 Success Criteria

You've successfully completed Step 1 when:
- ✅ You can run `python smart_dispatch_agent.py`
- ✅ You see "✅ Processed X dispatch(es)"
- ✅ You can see results in DBeaver with `Optimized_technician_id` filled in

**Congratulations! You've run your first smart dispatch agent! 🚀**

