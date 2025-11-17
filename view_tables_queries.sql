-- ============================================================================
-- SQL Queries to View Tables in team_core_flux Schema
-- ============================================================================
-- These queries help you view the tables and data that were copied from
-- SmartDispatchAgentDataset to team_core_flux schema.
-- ============================================================================

-- 1. List all tables in team_core_flux schema
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

-- 2. Count rows in each table
SELECT 
    'current_dispatches' as table_name,
    COUNT(*) as row_count
FROM "team_core_flux"."current_dispatches"
UNION ALL
SELECT 
    'dispatch_history' as table_name,
    COUNT(*) as row_count
FROM "team_core_flux"."dispatch_history"
UNION ALL
SELECT 
    'technician_calendar' as table_name,
    COUNT(*) as row_count
FROM "team_core_flux"."technician_calendar"
UNION ALL
SELECT 
    'technicians' as table_name,
    COUNT(*) as row_count
FROM "team_core_flux"."technicians";

-- 3. View sample data from current_dispatches (first 10 rows)
SELECT * 
FROM "team_core_flux"."current_dispatches"
LIMIT 10;

-- 4. View sample data from dispatch_history (first 10 rows)
SELECT * 
FROM "team_core_flux"."dispatch_history"
LIMIT 10;

-- 5. View sample data from technician_calendar (first 10 rows)
SELECT * 
FROM "team_core_flux"."technician_calendar"
LIMIT 10;

-- 6. View sample data from technicians (first 10 rows)
SELECT * 
FROM "team_core_flux"."technicians"
LIMIT 10;

-- ============================================================================
-- IMPORTANT: How to View Tables in DBeaver
-- ============================================================================
-- 
-- Method 1: Using Database Navigator
--   1. In DBeaver, expand: Databases → postgres → Schemas
--   2. Find and expand: team_core_flux
--   3. Expand: Tables
--   4. You should see all 4 tables listed
--   5. Right-click on any table → "View Data" or "Read Data"
--
-- Method 2: Using SQL Editor
--   - Make sure you're connected to the database
--   - Use the queries above with the schema-qualified table names:
--     "team_core_flux"."table_name"
--
-- Method 3: Set Search Path (easier queries)
--   Run this first, then you can query without schema prefix:
--   SET search_path TO "team_core_flux";
--   Then: SELECT * FROM dispatch_history LIMIT 10;
--
-- ============================================================================

-- 7. Set search path to team_core_flux (makes queries easier)
SET search_path TO "team_core_flux";

-- After running the above, you can query tables without schema prefix:
-- SELECT * FROM dispatch_history LIMIT 10;
-- SELECT * FROM technicians LIMIT 10;
-- etc.

-- 8. View all columns in dispatch_history table
SELECT 
    column_name,
    data_type,
    character_maximum_length,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'team_core_flux'
AND table_name = 'dispatch_history'
ORDER BY ordinal_position;

