# Power BI Quick Start - 5 Minutes

## 🚀 Fastest Way to See Your Results

### Step 1: Open Power BI Desktop
- Download if needed: https://powerbi.microsoft.com/desktop/
- Open Power BI Desktop

### Step 2: Connect to Database
1. Click **"Get Data"** (top left)
2. Search: **"PostgreSQL"**
3. Click **"PostgreSQL database"** → **"Connect"**

### Step 3: Enter Connection Info
```
Server: 212.2.245.85
Port: 6432
Database: postgres
Username: postgres
Password: Tea_IWMZ5wuUta97gupb
```

### Step 4: Select Tables
- ✅ Check: `team_core_flux.current_dispatches`
- ✅ Check: `team_core_flux.technicians`
- Click **"Load"**

### Step 5: Create Quick Visualizations

#### A. Dispatch Status (Donut Chart)
1. Click **"Donut chart"** icon
2. Drag `Optimization_status` to **Legend**
3. Drag `Dispatch_id` to **Values**

#### B. Top Technicians (Table)
1. Click **"Table"** icon
2. Add columns:
   - `Name`
   - `Primary_skill`
   - `Current_assignments`
   - `Workload_capacity`

#### C. Confidence Scores (Bar Chart)
1. Click **"Bar chart"** icon
2. Drag `Optimization_confidence` to **Y-axis**
3. Drag `Dispatch_id` to **X-axis**

### Step 6: Refresh Data
- Click **"Refresh"** button (top ribbon)
- Your data updates!

---

## 📊 That's It! You're Done!

You now have:
- ✅ Live data from your database
- ✅ Visual dashboards
- ✅ Dispatch agent results

**See `POWER_BI_SETUP_GUIDE.md` for advanced features!**

