# Power BI Setup Guide - Smart Dispatch Agent Results

## 🎯 Goal
Connect Power BI to your PostgreSQL database and create dashboards to visualize dispatch agent results.

---

## ✅ STEP 1: Install Power BI Desktop

### Download Power BI Desktop (Free)
1. Go to: https://powerbi.microsoft.com/desktop/
2. Click "Download free"
3. Install Power BI Desktop
4. Open Power BI Desktop

---

## ✅ STEP 2: Connect to PostgreSQL Database

### Method 1: Direct Connection (Recommended)

1. **Open Power BI Desktop**
2. **Click "Get Data"** (top left)
3. **Select "More..."**
4. **Search for "PostgreSQL database"**
5. **Click "Connect"**

### Enter Connection Details:
```
Server: 212.2.245.85
Port: 6432
Database: postgres
```

**Authentication:**
- Select: **Database**
- Username: `postgres`
- Password: `Tea_IWMZ5wuUta97gupb`

6. **Click "OK"**
7. **If prompted about encryption**, click "OK" (use default settings)

---

## ✅ STEP 3: Load Tables

### Select Tables to Import:

1. **In the Navigator window**, you'll see a list of schemas
2. **Expand "team_core_flux"** schema
3. **Select these tables:**
   - ✅ `current_dispatches`
   - ✅ `technicians`
   - ✅ `dispatch_history`
   - ✅ `technician_calendar` (optional)

4. **Click "Load"** (or "Transform Data" if you want to modify first)

**Wait for data to load...** (may take 1-2 minutes)

---

## ✅ STEP 4: Create Relationships

### Link Tables Together:

1. **Click "Model" view** (left sidebar, looks like 3 connected boxes)
2. **Drag and drop to create relationships:**
   - `current_dispatches.Optimized_technician_id` → `technicians.Technician_id`
   - `dispatch_history.Assigned_technician_id` → `technicians.Technician_id`

3. **Verify relationships** (should show lines connecting tables)

---

## ✅ STEP 5: Create Your First Dashboard

### Create a New Report Page:

1. **Click "Report" view** (left sidebar, looks like a chart)
2. **You'll see blank canvas**

### Add Visualizations:

#### **Visualization 1: Dispatch Status Overview**

1. **Select "current_dispatches" table** (right panel)
2. **Drag "Optimization_status" to canvas**
3. **Click "Donut chart"** (or Pie chart) from Visualizations panel
4. **Drag "Dispatch_id" to "Values"** (count)
5. **Title:** "Dispatch Status"

#### **Visualization 2: Top Technicians by Assignments**

1. **Select "technicians" table**
2. **Click "Table" visualization**
3. **Add columns:**
   - `Name`
   - `Primary_skill`
   - `Current_assignments`
   - `Workload_capacity`
4. **Sort by "Current_assignments" descending**
5. **Title:** "Technician Workload"

#### **Visualization 3: Optimization Confidence Scores**

1. **Select "current_dispatches" table**
2. **Click "Column chart"**
3. **Drag "Optimization_confidence" to "Y-axis"**
4. **Drag "Dispatch_id" to "X-axis"** (or use date if available)
5. **Title:** "Optimization Confidence Scores"

#### **Visualization 4: Skills Distribution**

1. **Select "current_dispatches" table**
2. **Click "Bar chart"**
3. **Drag "Required_skill" to "Axis"**
4. **Drag "Dispatch_id" to "Values"** (count)
5. **Title:** "Required Skills Distribution"

---

## ✅ STEP 6: Create Key Metrics (DAX Measures)

### Add Calculated Measures:

1. **Right-click on "current_dispatches" table** → **"New measure"**

#### **Measure 1: Total Optimized Dispatches**
```dax
Total Optimized = 
CALCULATE(
    COUNTROWS(current_dispatches),
    current_dispatches[Optimization_status] = "completed"
)
```

#### **Measure 2: Average Confidence Score**
```dax
Avg Confidence = 
AVERAGE(
    VALUE(current_dispatches[Optimization_confidence])
)
```

#### **Measure 3: Optimization Rate**
```dax
Optimization Rate = 
DIVIDE(
    [Total Optimized],
    COUNTROWS(current_dispatches),
    0
) * 100
```

#### **Measure 4: Pending Dispatches**
```dax
Pending Dispatches = 
CALCULATE(
    COUNTROWS(current_dispatches),
    current_dispatches[Optimization_status] = "pending"
)
```

### Add to Dashboard:
- Drag these measures to create **"Card" visualizations**
- Shows key numbers at a glance

---

## ✅ STEP 7: Create Advanced Visualizations

### **Visualization 5: Map View (Geographic Distribution)**

1. **Click "Map" visualization** (globe icon)
2. **Drag "Customer_latitude" to Latitude**
3. **Drag "Customer_longitude" to Longitude**
4. **Drag "Dispatch_id" to Size**
5. **Drag "Required_skill" to Legend**
6. **Title:** "Dispatch Locations"

### **Visualization 6: Performance Trends**

1. **Click "Line chart"**
2. **Drag "Optimization_timestamp" to Axis** (if available)
3. **Drag "Dispatch_id" to Values** (count)
4. **Drag "Optimization_status" to Legend**
5. **Title:** "Dispatch Trends Over Time"

### **Visualization 7: Technician Performance**

1. **Click "Matrix" visualization**
2. **Rows:** `technicians[Name]`
3. **Columns:** `current_dispatches[Required_skill]`
4. **Values:** Count of `Dispatch_id`
5. **Title:** "Technician Skills Matrix"

---

## ✅ STEP 8: Create Summary Dashboard

### Layout Your Dashboard:

```
┌─────────────────────────────────────────────────┐
│  SMART DISPATCH AGENT - DASHBOARD              │
├─────────────────────────────────────────────────┤
│  [Total Optimized] [Avg Confidence] [Pending]  │
│  [Optimization Rate]                            │
├─────────────────────────────────────────────────┤
│  [Dispatch Status]    [Skills Distribution]    │
├─────────────────────────────────────────────────┤
│  [Technician Workload]  [Map View]              │
├─────────────────────────────────────────────────┤
│  [Performance Trends]                           │
└─────────────────────────────────────────────────┘
```

### Tips:
- Use **consistent colors** (Format → Colors)
- Add **filters** (Filter panel → Add filters)
- Set **page title** (Format → Page title)
- Add **text boxes** for explanations

---

## ✅ STEP 9: Add Filters

### Create Slicers (Interactive Filters):

1. **Click "Slicer" visualization**
2. **Add slicers for:**
   - `Priority` (Critical, High, Normal, Low)
   - `Required_skill`
   - `State`
   - `Optimization_status`

3. **All visualizations will filter automatically**

---

## ✅ STEP 10: Refresh Data

### Update Data in Power BI:

1. **Click "Refresh" button** (top ribbon)
2. **Or:** Home → Refresh → Refresh all
3. **Data will update** from PostgreSQL

### Schedule Automatic Refresh (Power BI Service):

1. **Publish report** to Power BI Service
2. **Go to dataset settings**
3. **Set up scheduled refresh** (daily/hourly)

---

## 📊 Sample Queries for Custom Analysis

### Create Custom SQL Query (Advanced):

1. **Get Data → PostgreSQL database**
2. **Click "Advanced options"**
3. **Paste SQL query:**

```sql
SELECT 
    d."Dispatch_id",
    d."Required_skill",
    d."Priority",
    d."Optimized_technician_id",
    d."Optimization_confidence",
    t."Name" as Technician_Name,
    t."Primary_skill",
    t."Current_assignments",
    t."Workload_capacity"
FROM "team_core_flux"."current_dispatches" d
LEFT JOIN "team_core_flux"."technicians" t
    ON d."Optimized_technician_id" = t."Technician_id"
WHERE d."Optimization_status" = 'completed'
ORDER BY d."Optimization_confidence" DESC;
```

---

## 🎨 Dashboard Design Tips

### Color Scheme:
- **Green**: Completed/Optimized
- **Yellow**: Pending
- **Red**: Critical priority
- **Blue**: Normal status

### Best Practices:
1. **Keep it simple** - Don't overcrowd
2. **Use consistent formatting**
3. **Add titles and labels**
4. **Include date filters**
5. **Make it interactive** (slicers, drill-through)

---

## 🔄 Keeping Data Fresh

### Option 1: Manual Refresh
- Click "Refresh" button in Power BI Desktop

### Option 2: Scheduled Refresh (Power BI Service)
1. **Publish report** to Power BI Service
2. **Set up data gateway** (if needed)
3. **Configure scheduled refresh**

### Option 3: DirectQuery (Real-time)
- Use DirectQuery mode instead of Import
- Data always current (slower performance)

---

## 📋 Quick Checklist

- [ ] Power BI Desktop installed
- [ ] Connected to PostgreSQL database
- [ ] Tables loaded (current_dispatches, technicians, etc.)
- [ ] Relationships created
- [ ] Basic visualizations created
- [ ] DAX measures added
- [ ] Filters/slicers added
- [ ] Dashboard formatted and titled
- [ ] Data refreshed

---

## 🐛 Troubleshooting

### Problem: Can't connect to database
**Solution:**
- Check firewall settings
- Verify database credentials
- Try "Use encrypted connection" option

### Problem: Tables not showing
**Solution:**
- Make sure you're looking in "team_core_flux" schema
- Check if schema exists in database
- Refresh connection

### Problem: Relationships not working
**Solution:**
- Verify column names match exactly
- Check data types are compatible
- Use "Manage relationships" to fix

### Problem: Data not updating
**Solution:**
- Click "Refresh" button
- Check database connection
- Verify data exists in PostgreSQL

---

## 🎉 Success!

You should now see:
- ✅ Real-time dispatch data
- ✅ Technician assignments
- ✅ Optimization metrics
- ✅ Performance trends
- ✅ Interactive dashboards

**Your Smart Dispatch Agent results are now visualized in Power BI! 🚀**

