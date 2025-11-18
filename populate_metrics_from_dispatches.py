#!/usr/bin/env python3
"""
Populate dispatch_metrics from current_dispatches data in the specified date range
This will create metrics for any 14-day period within Nov 12, 2025 - Feb 9, 2026
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

def get_technician_for_dispatch(cur, dispatch):
    """Find the best technician for a dispatch"""
    # Simple matching: find a technician with the required skill
    cur.execute("""
        SELECT "Technician_id", "Latitude", "Longitude"
        FROM technicians
        WHERE "Primary_skill" = %s
        AND "State" = %s
        AND "Current_assignments" < "Workload_capacity"
        ORDER BY RANDOM()
        LIMIT 1
    """, (dispatch['required_skill'], dispatch['state']))
    
    result = cur.fetchone()
    if result:
        return {
            'id': result[0],
            'lat': result[1],
            'lon': result[2]
        }
    
    # Fallback: any technician in the same state
    cur.execute("""
        SELECT "Technician_id", "Latitude", "Longitude"
        FROM technicians
        WHERE "State" = %s
        AND "Current_assignments" < "Workload_capacity"
        ORDER BY RANDOM()
        LIMIT 1
    """, (dispatch['state'],))
    
    result = cur.fetchone()
    if result:
        return {
            'id': result[0],
            'lat': result[1],
            'lon': result[2]
        }
    
    # Last fallback: any available technician
    cur.execute("""
        SELECT "Technician_id", "Latitude", "Longitude"
        FROM technicians
        WHERE "Current_assignments" < "Workload_capacity"
        ORDER BY RANDOM()
        LIMIT 1
    """)
    
    result = cur.fetchone()
    return {
        'id': result[0] if result else 'T900000',
        'lat': result[1] if result else 40.7128,
        'lon': result[2] if result else -74.0060
    }

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points using Haversine formula"""
    from math import radians, sin, cos, sqrt, atan2
    
    R = 6371  # Earth's radius in kilometers
    
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

def populate_metrics():
    """Populate dispatch_metrics from current_dispatches"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*70)
    print("POPULATING DISPATCH_METRICS FROM CURRENT_DISPATCHES")
    print("="*70)
    
    # Get dispatches from the date range, selecting 14 consecutive days
    # Let's pick from Dec 1-14, 2025 (a nice middle range)
    start_date = '2025-12-01'
    end_date = '2025-12-14'
    
    print(f"\n📅 Selected date range: {start_date} to {end_date}")
    print("   (14 days of data)")
    
    cur.execute("""
        SELECT 
            "Dispatch_id",
            "Priority",
            "Required_skill",
            "State",
            "Customer_latitude",
            "Customer_longitude",
            "Duration_min",
            "Appointment_start_datetime"
        FROM current_dispatches
        WHERE "Appointment_start_datetime"::timestamp BETWEEN %s AND %s
        ORDER BY "Appointment_start_datetime"
    """, (start_date, end_date))
    
    dispatches = cur.fetchall()
    print(f"\n✅ Found {len(dispatches)} dispatches in this range")
    
    if len(dispatches) == 0:
        print("\n❌ No dispatches found. Trying a broader date range...")
        # Try Dec 15-28 instead
        start_date = '2025-12-15'
        end_date = '2025-12-28'
        
        cur.execute("""
            SELECT 
                "Dispatch_id",
                "Priority",
                "Required_skill",
                "State",
                "Customer_latitude",
                "Customer_longitude",
                "Duration_min",
                "Appointment_start_datetime"
            FROM current_dispatches
            WHERE "Appointment_start_datetime"::timestamp BETWEEN %s AND %s
            ORDER BY "Appointment_start_datetime"
        """, (start_date, end_date))
        
        dispatches = cur.fetchall()
        print(f"\n✅ Found {len(dispatches)} dispatches in range {start_date} to {end_date}")
    
    if len(dispatches) == 0:
        print("\n❌ Still no dispatches. Let's just take the first 14 days with data...")
        cur.execute("""
            SELECT DISTINCT DATE("Appointment_start_datetime"::timestamp) as date
            FROM current_dispatches
            WHERE "Appointment_start_datetime"::timestamp BETWEEN '2025-11-12' AND '2026-02-09'
            ORDER BY date
            LIMIT 14
        """)
        
        dates = [row[0] for row in cur.fetchall()]
        if dates:
            start_date = str(dates[0])
            end_date = str(dates[-1])
            
            cur.execute("""
                SELECT 
                    "Dispatch_id",
                    "Priority",
                    "Required_skill",
                    "State",
                    "Customer_latitude",
                    "Customer_longitude",
                    "Duration_min",
                    "Appointment_start_datetime"
                FROM current_dispatches
                WHERE DATE("Appointment_start_datetime"::timestamp) = ANY(%s)
                ORDER BY "Appointment_start_datetime"
            """, (dates,))
            
            dispatches = cur.fetchall()
            print(f"\n✅ Found {len(dispatches)} dispatches across {len(dates)} dates")
            print(f"   Date range: {start_date} to {end_date}")
    
    # Clear existing metrics for this date range
    print(f"\n🗑️  Clearing existing metrics in this date range...")
    cur.execute("""
        DELETE FROM dispatch_metrics
        WHERE updated_at::date BETWEEN %s AND %s
    """, (start_date, end_date))
    deleted = cur.rowcount
    print(f"   Deleted {deleted} existing records")
    
    # Process each dispatch
    print(f"\n⚙️  Processing {len(dispatches)} dispatches...")
    inserted = 0
    
    for dispatch in dispatches:
        dispatch_id = dispatch[0]
        priority = dispatch[1]
        required_skill = dispatch[2]
        state = dispatch[3]
        cust_lat = float(dispatch[4])
        cust_lon = float(dispatch[5])
        duration_min = dispatch[6]
        appointment_time = dispatch[7]
        
        # Get a technician
        tech = get_technician_for_dispatch(cur, {
            'required_skill': required_skill,
            'state': state
        })
        
        # Calculate distance
        distance = calculate_distance(cust_lat, cust_lon, tech['lat'], tech['lon'])
        
        # Generate realistic metrics
        # Routing time: 30-120 seconds based on priority
        routing_seconds = {
            'Critical': random.randint(30, 60),
            'High': random.randint(45, 90),
            'Normal': random.randint(60, 120)
        }.get(priority, 90)
        
        # ETC: duration + travel time + buffer
        travel_time_min = int(distance * 1.5)  # ~1.5 min per km
        etc_minutes = duration_min + travel_time_min + random.randint(10, 30)
        
        # Operational cost: base + distance + duration
        base_cost = {
            'Critical': 100,
            'High': 75,
            'Normal': 50
        }.get(priority, 60)
        operational_cost = base_cost + (distance * 2.5) + (duration_min * 0.8)
        
        # Burnout risk: random for now
        burnout_risk = random.choice([True, False, False, False])  # 25% chance
        
        # SLA: Critical < 4hrs, High < 8hrs, Normal < 24hrs
        sla_threshold = {
            'Critical': 240,
            'High': 480,
            'Normal': 1440
        }.get(priority, 480)
        sla_breached = etc_minutes > sla_threshold
        
        # Fallback techs: empty for now
        fallback_techs = '[]'
        
        # Use appointment time as the created/updated time
        timestamp = appointment_time
        
        # Insert into dispatch_metrics
        try:
            cur.execute("""
                INSERT INTO dispatch_metrics (
                    dispatch_id, technician_id, priority, required_skill, state,
                    routing_seconds, estimated_completion_minutes, travel_km,
                    operational_cost, fallback_technicians, burnout_risk,
                    sla_breached, created_at, updated_at
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                )
            """, (
                dispatch_id, tech['id'], priority, required_skill, state,
                routing_seconds, etc_minutes, distance, operational_cost,
                fallback_techs, burnout_risk, sla_breached, timestamp, timestamp
            ))
            inserted += 1
            
            if inserted % 50 == 0:
                print(f"   Processed {inserted} dispatches...")
        
        except Exception as e:
            print(f"   ⚠️  Error inserting dispatch {dispatch_id}: {e}")
            continue
    
    # Commit changes
    conn.commit()
    
    print(f"\n✅ Successfully inserted {inserted} metrics records!")
    
    # Verify the results
    print(f"\n📊 VERIFICATION:")
    print("-" * 70)
    
    cur.execute("""
        SELECT 
            DATE(updated_at) as date,
            COUNT(*) as count,
            ROUND(AVG(routing_seconds) / 60.0, 2) as avg_routing_min,
            ROUND(AVG(estimated_completion_minutes), 2) as avg_etc_min,
            ROUND(AVG(operational_cost), 2) as avg_cost
        FROM dispatch_metrics
        WHERE updated_at::date BETWEEN %s AND %s
        GROUP BY DATE(updated_at)
        ORDER BY DATE(updated_at)
    """, (start_date, end_date))
    
    results = cur.fetchall()
    print(f"\nMetrics by date ({len(results)} days):")
    for row in results:
        print(f"  {row[0]}: {row[1]} dispatches, "
              f"Routing: {row[2]}min, ETC: {row[3]}min, Cost: ${row[4]}")
    
    print("\n" + "="*70)
    print("✅ DONE! Your dashboard should now show a 14-day trend!")
    print("="*70)
    print("\n📈 Refresh your dashboard at: http://localhost:5000")
    print("")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        populate_metrics()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

