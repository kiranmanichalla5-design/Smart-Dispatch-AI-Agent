# How to View Tables in team_core_flux Schema

## ✅ Confirmation: Tables and Data ARE Present

The verification script confirms that all tables and data exist in the `team_core_flux` schema:
- ✅ `current_dispatches`: 600 rows
- ✅ `dispatch_history`: 1,000 rows  
- ✅ `technician_calendar`: 13,500 rows
- ✅ `technicians`: 150 rows

## Why You Might Not See Them in DBeaver

### Common Reasons:

1. **Database Navigator Not Refreshed**
   - DBeaver may need to refresh to show new tables
   - Solution: Right-click on "Schemas" → "Refresh"

2. **Wrong Schema Selected**
   - Make sure you're looking in `team_core_flux`, not `public` or another schema
   - Solution: Navigate to: `Databases → postgres → Schemas → team_core_flux → Tables`

3. **Schema Not Visible**
   - Some schemas might be filtered out
   - Solution: Check DBeaver filters/settings

4. **Using Wrong Table Names in Queries**
   - You must use schema-qualified names: `"team_core_flux"."table_name"`
   - Solution: Use the queries in `view_tables_queries.sql`

## How to View Tables in DBeaver

### Method 1: Database Navigator (Easiest)

1. In the left panel (Database Navigator), expand:
   ```
   Databases
   └── postgres
       └── Schemas
           └── team_core_flux
               └── Tables
   ```

2. You should see 4 tables:
   - current_dispatches
   - dispatch_history
   - technician_calendar
   - technicians

3. Right-click on any table → Select "View Data" or "Read Data"

4. **If tables don't appear**: Right-click on "Schemas" → "Refresh"

### Method 2: SQL Editor (Recommended)

1. Open a new SQL script in DBeaver
2. Copy and run the queries from `view_tables_queries.sql`
3. Or use these quick queries:

```sql
-- First, set the search path (makes queries easier)
SET search_path TO "team_core_flux";

-- Then query tables directly (no schema prefix needed)
SELECT * FROM dispatch_history LIMIT 10;
SELECT * FROM technicians LIMIT 10;
SELECT * FROM current_dispatches LIMIT 10;
SELECT * FROM technician_calendar LIMIT 10;
```

### Method 3: Using Schema-Qalified Names

If you don't set the search path, use full schema names:

```sql
SELECT * FROM "team_core_flux"."dispatch_history" LIMIT 10;
SELECT * FROM "team_core_flux"."technicians" LIMIT 10;
SELECT * FROM "team_core_flux"."current_dispatches" LIMIT 10;
SELECT * FROM "team_core_flux"."technician_calendar" LIMIT 10;
```

## Quick Verification Query

Run this to confirm tables exist:

```sql
SELECT 
    table_name,
    (SELECT COUNT(*) 
     FROM information_schema.columns 
     WHERE table_schema = 'team_core_flux' 
     AND table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'team_core_flux'
AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

## Troubleshooting Steps

1. **Refresh DBeaver Connection**
   - Right-click on your database connection → "Refresh"
   - Or press `F5` while the connection is selected

2. **Check Schema Filters**
   - Right-click on "Schemas" → "Filter" → Make sure `team_core_flux` is not filtered out

3. **Verify Connection**
   - Make sure you're connected to the correct database (`postgres`)
   - Check connection settings match:
     - Host: 212.2.245.85
     - Port: 6432
     - Database: postgres

4. **Run Verification Script**
   - Run: `python verify_tables.py`
   - This confirms tables exist with data

## Files Created

- `view_tables_queries.sql` - Ready-to-use SQL queries
- `verify_tables.py` - Python script to verify tables exist
- `team_core_flux_schema.sql` - CREATE TABLE statements (structure only)

## Need Help?

If tables still don't appear:
1. Run `python verify_tables.py` to confirm they exist
2. Try refreshing DBeaver (F5 or right-click → Refresh)
3. Check that you're looking in the correct schema (`team_core_flux`)
4. Use the SQL queries in `view_tables_queries.sql`

