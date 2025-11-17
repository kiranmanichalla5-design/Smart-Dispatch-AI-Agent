-- SQL Scripts for tables in 'team_core_flux' schema
-- Generated automatically
-- Schema: team_core_flux

-- Ensure the schema exists
CREATE SCHEMA IF NOT EXISTS "team_core_flux";

================================================================================


-- Table: current_dispatches
-- ============================================================================

CREATE TABLE "team_core_flux"."current_dispatches" (
    "Dispatch_id" integer,
    "Ticket_type" character varying(50),
    "Order_type" character varying(50),
    "Priority" character varying(50),
    "Required_skill" character varying(50),
    "Status" character varying(50),
    "Street" character varying(50),
    "City" character varying(50),
    "County" character varying(50),
    "State" character varying(50),
    "Postal_code" integer,
    "Customer_latitude" real,
    "Customer_longitude" real,
    "Appointment_start_datetime" character varying(50),
    "Appointment_end_datetime" character varying(50),
    "Duration_min" integer,
    "Assigned_technician_id" character varying(50),
    "Optimized_technician_id" character varying(50),
    "Resolution_type" character varying(50),
    "Optimization_status" character varying(50),
    "Optimization_timestamp" character varying(50),
    "Optimization_confidence" character varying(50)
);



-- Table: dispatch_history
-- ============================================================================

CREATE TABLE "team_core_flux"."dispatch_history" (
    "Dispatch_id" integer,
    "Ticket_type" character varying(50),
    "Order_type" character varying(50),
    "Priority" character varying(50),
    "Required_skill" character varying(50),
    "Status" character varying(50),
    "City" character varying(50),
    "County" character varying(50),
    "State" character varying(50),
    "Customer_latitude" real,
    "Customer_longitude" real,
    "Appointment_start_time" character varying(50),
    "Appointment_end_time" character varying(50),
    "Duration_min" integer,
    "Assigned_technician_id" character varying(50),
    "Distance_km" real,
    "Actual_duration_min" integer,
    "Productive_dispatch" integer,
    "First_time_fix" integer,
    "Fault_code" integer,
    "Remedy_code" integer,
    "Cause_code" integer,
    "Service_tier" character varying(50),
    "Equipment_installed" character varying(50),
    "Technician_notes" character varying(50)
);



-- Table: technician_calendar
-- ============================================================================

CREATE TABLE "team_core_flux"."technician_calendar" (
    "Technician_id" character varying(50),
    "Date" character varying(50),
    "Day_of_week" character varying(50),
    "Available" integer,
    "Start_time" character varying(50),
    "End_time" character varying(50),
    "Reason" character varying(50),
    "Max_assignments" integer
);



-- Table: technicians
-- ============================================================================

CREATE TABLE "team_core_flux"."technicians" (
    "Technician_id" character varying(50),
    "Name" character varying(50),
    "Primary_skill" character varying(50),
    "City" character varying(50),
    "County" character varying(50),
    "State" character varying(50),
    "Latitude" real,
    "Longitude" real,
    "Workload_capacity" integer,
    "Current_assignments" integer
);

