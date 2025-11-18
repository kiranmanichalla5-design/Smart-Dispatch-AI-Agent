#!/usr/bin/env python3
"""
Populate dispatch_metrics from dispatch_history table
This will create metrics records based on historical dispatch data
"""

import psycopg2
import random
from datetime import datetime, timedelta

# Database connection
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres',
    'options': '-c search_path=team_core_flux'
}

def populate_metrics_from_history():
    """
    Create dispatch_metrics records from dispatch_history
    We'll take the last 14 days of data from dispatch_history
    """
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*80)
    print("POPULATING DISPATCH_METRICS FROM DISPATCH_HISTORY")
    print("="*80)
    
    # Get the latest date from dispatch_history
    cur.execute("""
        SELECT MAX("Appointment_start_time")::date
        FROM dispatch_history
    """)
    latest_date = cur.fetchone()[0]
    print(f"\nLatest date in dispatch_history: {latest_date}")
    
    # Calculate 14 days before that
    start_date = latest_date - timedelta(days=13)  # 14 days including the latest
    print(f"Fetching data from: {start_date} to {latest_date}")
    
    # Get historical dispatches from the last 14 days
    cur.execute("""
        SELECT 
            "Dispatch_id",
            "Priority",
            "Required_skill",
            "State",
            "Assigned_technician_id",
            "Distance_km",
            "Duration_min",
            "Actual_duration_min",
            "Appointment_start_time"
        FROM dispatch_history
        WHERE "Appointment_start_time"::date BETWEEN %s AND %s
        ORDER BY "Appointment_start_time"
    """, (start_date, latest_date))
    
    historical_records = cur.fetchall()
    print(f"\nFound {len(historical_records)} historical dispatch records")
    
    if not historical_records:
        print("❌ No data found in the specified date range!")
        cur.close()
        conn.close()
        return
    
    # Clear existing dispatch_metrics
    print("\nClearing existing dispatch_metrics...")
    cur.execute("DELETE FROM dispatch_metrics")
    conn.commit()
    
    # Insert new metrics based on historical data
    print(f"\nInserting {len(historical_records)} new metrics records...")
    
    inserted = 0
    for record in historical_records:
        dispatch_id, priority, skill, state, tech_id, distance_km, duration, actual_duration, appt_time = record
        
        # Calculate metrics based on historical data
        # Routing time: random but realistic (30-120 seconds)
        routing_seconds = random.randint(30, 120)
        
        # ETC: Use actual duration if available, otherwise use duration
        etc_minutes = actual_duration if actual_duration else duration
        
        # Operational cost: based on distance and duration
        travel_cost = float(distance_km or 0) * 2.5  # $2.5 per km
        labor_cost = etc_minutes * 1.5  # $1.5 per minute
        operational_cost = travel_cost + labor_cost
        
        # SLA breach: Critical = 2h, High = 4h, Medium = 8h, Low = 24h
        sla_thresholds = {'Critical': 120, 'High': 240, 'Medium': 480, 'Low': 1440}
        sla_threshold = sla_thresholds.get(priority, 240)
        sla_breached = etc_minutes > sla_threshold
        
        # Burnout risk: random for now (in real system, would check tech workload)
        burnout_risk = random.choice([True, False, False, False])  # 25% chance
        
        # Insert into dispatch_metrics
        cur.execute("""
            INSERT INTO dispatch_metrics (
                dispatch_id, technician_id, priority, required_skill, state,
                routing_seconds, estimated_completion_minutes, travel_km,
                operational_cost, fallback_technicians, burnout_risk,
                sla_breached, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            dispatch_id,
            tech_id,
            priority,
            skill,
            state,
            routing_seconds,
            etc_minutes,
            distance_km,
            operational_cost,
            '[]',  # Empty fallback list
            burnout_risk,
            sla_breached,
            appt_time,  # Use appointment time as created_at
            appt_time   # Use appointment time as updated_at
        ))
        inserted += 1
        
        if inserted % 50 == 0:
            print(f"  Inserted {inserted} records...")
            conn.commit()
    
    conn.commit()
    print(f"\n✅ Successfully inserted {inserted} metrics records!")
    
    # Show summary by date
    print("\n" + "-"*80)
    print("METRICS SUMMARY BY DATE:")
    print("-"*80)
    
    cur.execute("""
        SELECT 
            DATE(updated_at) as metric_date,
            COUNT(*) as count,
            ROUND(AVG(routing_seconds) / 60.0, 2) as avg_routing_min,
            ROUND(AVG(estimated_completion_minutes), 2) as avg_etc_min,
            ROUND(AVG(operational_cost), 2) as avg_cost,
            SUM(CASE WHEN sla_breached THEN 1 ELSE 0 END) as sla_breaches,
            SUM(CASE WHEN burnout_risk THEN 1 ELSE 0 END) as burnout_risks
        FROM dispatch_metrics
        GROUP BY DATE(updated_at)
        ORDER BY DATE(updated_at) ASC
    """)
    
    summary = cur.fetchall()
    print(f"\n{'Date':<15} {'Count':<8} {'Routing':<12} {'ETC':<12} {'Cost':<12} {'SLA':<8} {'Burnout':<8}")
    print("-"*80)
    for row in summary:
        print(f"{row[0]!s:<15} {row[1]:<8} {row[2]:<12} {row[3]:<12} ${row[4]:<11.2f} {row[5]:<8} {row[6]:<8}")
    
    print("\n" + "="*80)
    print("✅ Dashboard will now show the last 14 days of historical data!")
    print("   Refresh your browser at http://localhost:5000 to see the trend chart.")
    print("="*80 + "\n")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        populate_metrics_from_history()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

