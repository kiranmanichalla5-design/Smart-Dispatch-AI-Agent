-- ============================================================================
-- Power BI SQL Queries
-- ============================================================================
-- Use these queries in Power BI for custom data analysis
-- ============================================================================

-- Query 1: Dispatch Summary with Technician Details
-- Use this for a comprehensive view of dispatches and assigned technicians
SELECT 
    d."Dispatch_id",
    d."Ticket_type",
    d."Priority",
    d."Required_skill",
    d."Status",
    d."City",
    d."State",
    d."Customer_latitude",
    d."Customer_longitude",
    d."Appointment_start_datetime",
    d."Duration_min",
    d."Optimized_technician_id",
    CAST(d."Optimization_confidence" AS FLOAT) as Optimization_confidence,
    d."Optimization_status",
    d."Optimization_timestamp",
    t."Name" as Technician_Name,
    t."Primary_skill" as Technician_Skill,
    t."City" as Technician_City,
    t."Latitude" as Technician_Latitude,
    t."Longitude" as Technician_Longitude,
    t."Current_assignments",
    t."Workload_capacity",
    CASE 
        WHEN t."Workload_capacity" > 0 
        THEN ROUND((t."Current_assignments"::FLOAT / t."Workload_capacity") * 100, 2)
        ELSE 0 
    END as Workload_Percentage
FROM "team_core_flux"."current_dispatches" d
LEFT JOIN "team_core_flux"."technicians" t
    ON d."Optimized_technician_id" = t."Technician_id"
WHERE d."Optimization_status" = 'completed'
ORDER BY d."Optimization_confidence" DESC NULLS LAST;

-- ============================================================================

-- Query 2: Technician Performance Summary
-- Shows how well each technician is performing
SELECT 
    t."Technician_id",
    t."Name",
    t."Primary_skill",
    t."City",
    t."State",
    t."Current_assignments",
    t."Workload_capacity",
    COUNT(d."Dispatch_id") as Total_Assigned_Dispatches,
    AVG(CAST(d."Optimization_confidence" AS FLOAT)) as Avg_Confidence_Score,
    COUNT(CASE WHEN d."Priority" = 'Critical' THEN 1 END) as Critical_Dispatches,
    COUNT(CASE WHEN d."Priority" = 'High' THEN 1 END) as High_Dispatches,
    COUNT(CASE WHEN d."Priority" = 'Normal' THEN 1 END) as Normal_Dispatches,
    COUNT(CASE WHEN d."Priority" = 'Low' THEN 1 END) as Low_Dispatches
FROM "team_core_flux"."technicians" t
LEFT JOIN "team_core_flux"."current_dispatches" d
    ON t."Technician_id" = d."Optimized_technician_id"
    AND d."Optimization_status" = 'completed'
GROUP BY 
    t."Technician_id",
    t."Name",
    t."Primary_skill",
    t."City",
    t."State",
    t."Current_assignments",
    t."Workload_capacity"
ORDER BY Total_Assigned_Dispatches DESC;

-- ============================================================================

-- Query 3: Skill Matching Analysis
-- Shows how well skills are being matched
SELECT 
    d."Required_skill",
    COUNT(*) as Total_Dispatches,
    COUNT(CASE WHEN d."Optimization_status" = 'completed' THEN 1 END) as Optimized_Count,
    COUNT(CASE WHEN d."Optimization_status" = 'pending' THEN 1 END) as Pending_Count,
    AVG(CAST(d."Optimization_confidence" AS FLOAT)) as Avg_Confidence,
    COUNT(DISTINCT d."Optimized_technician_id") as Unique_Technicians_Assigned,
    COUNT(CASE WHEN t."Primary_skill" = d."Required_skill" THEN 1 END) as Exact_Skill_Matches
FROM "team_core_flux"."current_dispatches" d
LEFT JOIN "team_core_flux"."technicians" t
    ON d."Optimized_technician_id" = t."Technician_id"
GROUP BY d."Required_skill"
ORDER BY Total_Dispatches DESC;

-- ============================================================================

-- Query 4: Daily Optimization Metrics
-- Shows optimization performance over time
SELECT 
    DATE("Optimization_timestamp") as Optimization_Date,
    COUNT(*) as Total_Optimized,
    AVG(CAST("Optimization_confidence" AS FLOAT)) as Avg_Confidence,
    COUNT(CASE WHEN "Priority" = 'Critical' THEN 1 END) as Critical_Count,
    COUNT(CASE WHEN "Priority" = 'High' THEN 1 END) as High_Count,
    COUNT(CASE WHEN "Priority" = 'Normal' THEN 1 END) as Normal_Count,
    COUNT(CASE WHEN "Priority" = 'Low' THEN 1 END) as Low_Count
FROM "team_core_flux"."current_dispatches"
WHERE "Optimization_status" = 'completed'
    AND "Optimization_timestamp" IS NOT NULL
GROUP BY DATE("Optimization_timestamp")
ORDER BY Optimization_Date DESC;

-- ============================================================================

-- Query 5: Geographic Distribution
-- Shows dispatches by location
SELECT 
    "State",
    "City",
    COUNT(*) as Dispatch_Count,
    COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END) as Optimized_Count,
    COUNT(CASE WHEN "Optimization_status" = 'pending' THEN 1 END) as Pending_Count,
    AVG("Customer_latitude") as Avg_Latitude,
    AVG("Customer_longitude") as Avg_Longitude,
    COUNT(DISTINCT "Required_skill") as Unique_Skills_Required
FROM "team_core_flux"."current_dispatches"
GROUP BY "State", "City"
ORDER BY Dispatch_Count DESC;

-- ============================================================================

-- Query 6: Priority Distribution
-- Shows dispatches by priority level
SELECT 
    "Priority",
    COUNT(*) as Total_Dispatches,
    COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END) as Optimized,
    COUNT(CASE WHEN "Optimization_status" = 'pending' THEN 1 END) as Pending,
    ROUND(
        (COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END)::FLOAT / 
         COUNT(*)) * 100, 
        2
    ) as Optimization_Rate_Percent,
    AVG(CAST("Optimization_confidence" AS FLOAT)) as Avg_Confidence
FROM "team_core_flux"."current_dispatches"
GROUP BY "Priority"
ORDER BY 
    CASE "Priority"
        WHEN 'Critical' THEN 1
        WHEN 'High' THEN 2
        WHEN 'Normal' THEN 3
        WHEN 'Low' THEN 4
        ELSE 5
    END;

-- ============================================================================

-- Query 7: Technician Availability Status
-- Shows which technicians are available vs fully booked
SELECT 
    "Technician_id",
    "Name",
    "Primary_skill",
    "City",
    "State",
    "Current_assignments",
    "Workload_capacity",
    CASE 
        WHEN "Workload_capacity" = 0 THEN 'No Capacity'
        WHEN "Current_assignments" >= "Workload_capacity" THEN 'Fully Booked'
        WHEN "Current_assignments" >= ("Workload_capacity" * 0.8) THEN 'Nearly Full'
        ELSE 'Available'
    END as Availability_Status,
    ROUND(
        CASE 
            WHEN "Workload_capacity" > 0 
            THEN ("Current_assignments"::FLOAT / "Workload_capacity") * 100
            ELSE 0 
        END, 
        2
    ) as Utilization_Percentage
FROM "team_core_flux"."technicians"
ORDER BY Utilization_Percentage DESC;

-- ============================================================================

-- Query 8: Historical Performance Comparison
-- Compares current dispatches with historical performance
SELECT 
    'Current' as Period,
    COUNT(*) as Total_Dispatches,
    AVG(CAST("Optimization_confidence" AS FLOAT)) as Avg_Confidence
FROM "team_core_flux"."current_dispatches"
WHERE "Optimization_status" = 'completed'

UNION ALL

SELECT 
    'Historical' as Period,
    COUNT(*) as Total_Dispatches,
    AVG(
        CASE 
            WHEN "Productive_dispatch" = 1 AND "First_time_fix" = 1 THEN 1.0
            WHEN "Productive_dispatch" = 1 THEN 0.7
            WHEN "First_time_fix" = 1 THEN 0.6
            ELSE 0.5
        END
    ) as Avg_Confidence
FROM "team_core_flux"."dispatch_history"
WHERE "Status" = 'Completed';

-- ============================================================================
-- END OF QUERIES
-- ============================================================================
-- 
-- How to use in Power BI:
-- 1. Get Data → PostgreSQL database
-- 2. Click "Advanced options"
-- 3. Paste one of these queries
-- 4. Click "OK" to load
-- ============================================================================

