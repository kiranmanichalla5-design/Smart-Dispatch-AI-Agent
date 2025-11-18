#!/usr/bin/env python3
"""
Search for existing data in the database within specified date range
"""

import psycopg2
from datetime import datetime

# Database connection
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres',
    'options': '-c search_path=team_core_flux'
}

def search_date_range():
    """Search for data in the specified date range"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*70)
    print("SEARCHING FOR DATA IN DATE RANGE: Nov 12, 2025 - Feb 9, 2026")
    print("="*70)
    
    # Define date range
    start_date = '2025-11-12'
    end_date = '2026-02-09'
    
    # Check dispatch_history table
    print("\n📋 DISPATCH_HISTORY Table:")
    print("-" * 70)
    cur.execute("""
        SELECT 
            MIN("Appointment_start_time"::timestamp) as earliest,
            MAX("Appointment_start_time"::timestamp) as latest,
            COUNT(*) as total_records,
            COUNT(DISTINCT DATE("Appointment_start_time"::timestamp)) as unique_dates
        FROM dispatch_history
        WHERE "Appointment_start_time"::timestamp BETWEEN %s AND %s
    """, (start_date, end_date))
    
    row = cur.fetchone()
    if row[0]:
        print(f"  ✅ Found {row[2]} records")
        print(f"  Date range: {row[0]} to {row[1]}")
        print(f"  Unique dates: {row[3]}")
        
        # Get daily breakdown
        cur.execute("""
            SELECT 
                DATE("Appointment_start_time"::timestamp) as dispatch_date,
                COUNT(*) as count,
                COUNT(DISTINCT "Assigned_technician_id") as unique_techs
            FROM dispatch_history
            WHERE "Appointment_start_time"::timestamp BETWEEN %s AND %s
            GROUP BY DATE("Appointment_start_time"::timestamp)
            ORDER BY DATE("Appointment_start_time"::timestamp) DESC
            LIMIT 20
        """, (start_date, end_date))
        
        print("\n  Daily breakdown (latest 20 days):")
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]} dispatches, {row[2]} technicians")
    else:
        print("  ❌ No records found in this date range")
    
    # Check current_dispatches table
    print("\n📋 CURRENT_DISPATCHES Table:")
    print("-" * 70)
    cur.execute("""
        SELECT 
            MIN("Appointment_start_datetime"::timestamp) as earliest,
            MAX("Appointment_start_datetime"::timestamp) as latest,
            COUNT(*) as total_records,
            COUNT(DISTINCT DATE("Appointment_start_datetime"::timestamp)) as unique_dates
        FROM current_dispatches
        WHERE "Appointment_start_datetime"::timestamp BETWEEN %s AND %s
    """, (start_date, end_date))
    
    row = cur.fetchone()
    if row[0]:
        print(f"  ✅ Found {row[2]} records")
        print(f"  Date range: {row[0]} to {row[1]}")
        print(f"  Unique dates: {row[3]}")
        
        # Get daily breakdown
        cur.execute("""
            SELECT 
                DATE("Appointment_start_datetime"::timestamp) as dispatch_date,
                COUNT(*) as count,
                "Status"
            FROM current_dispatches
            WHERE "Appointment_start_datetime"::timestamp BETWEEN %s AND %s
            GROUP BY DATE("Appointment_start_datetime"::timestamp), "Status"
            ORDER BY DATE("Appointment_start_datetime"::timestamp) DESC
            LIMIT 20
        """, (start_date, end_date))
        
        print("\n  Daily breakdown by status (latest 20 days):")
        for row in cur.fetchall():
            print(f"    {row[0]}: {row[1]} dispatches ({row[2]})")
    else:
        print("  ❌ No records found in this date range")
    
    # Check dispatch_metrics table
    print("\n📋 DISPATCH_METRICS Table:")
    print("-" * 70)
    cur.execute("""
        SELECT 
            MIN(updated_at) as earliest,
            MAX(updated_at) as latest,
            COUNT(*) as total_records,
            COUNT(DISTINCT DATE(updated_at)) as unique_dates
        FROM dispatch_metrics
        WHERE updated_at BETWEEN %s AND %s
    """, (start_date, end_date))
    
    row = cur.fetchone()
    if row[0]:
        print(f"  ✅ Found {row[2]} records")
        print(f"  Date range: {row[0]} to {row[1]}")
        print(f"  Unique dates: {row[3]}")
    else:
        print("  ❌ No records found in this date range")
    
    # Check overall data availability
    print("\n📊 OVERALL DATA AVAILABILITY:")
    print("-" * 70)
    
    # dispatch_history
    cur.execute("""
        SELECT 
            MIN("Appointment_start_time"::timestamp) as earliest,
            MAX("Appointment_start_time"::timestamp) as latest,
            COUNT(*) as total
        FROM dispatch_history
    """)
    row = cur.fetchone()
    if row[0]:
        print(f"  dispatch_history:")
        print(f"    Total records: {row[2]}")
        print(f"    Date range: {row[0]} to {row[1]}")
    
    # current_dispatches
    cur.execute("""
        SELECT 
            MIN("Appointment_start_datetime"::timestamp) as earliest,
            MAX("Appointment_start_datetime"::timestamp) as latest,
            COUNT(*) as total
        FROM current_dispatches
    """)
    row = cur.fetchone()
    if row[0]:
        print(f"  current_dispatches:")
        print(f"    Total records: {row[2]}")
        print(f"    Date range: {row[0]} to {row[1]}")
    
    # dispatch_metrics
    cur.execute("""
        SELECT 
            MIN(updated_at) as earliest,
            MAX(updated_at) as latest,
            COUNT(*) as total
        FROM dispatch_metrics
    """)
    row = cur.fetchone()
    if row[0]:
        print(f"  dispatch_metrics:")
        print(f"    Total records: {row[2]}")
        print(f"    Date range: {row[0]} to {row[1]}")
    
    print("\n" + "="*70)
    print("RECOMMENDATION:")
    print("="*70)
    
    # Check if dispatch_history or current_dispatches has data in range
    cur.execute("""
        SELECT COUNT(*) 
        FROM dispatch_history 
        WHERE "Appointment_start_time"::timestamp BETWEEN %s AND %s
    """, (start_date, end_date))
    
    hist_count = cur.fetchone()[0]
    
    cur.execute("""
        SELECT COUNT(*) 
        FROM current_dispatches 
        WHERE "Appointment_start_datetime"::timestamp BETWEEN %s AND %s
    """, (start_date, end_date))
    
    current_count = cur.fetchone()[0]
    
    if hist_count > 0 or current_count > 0:
        print(f"\n✅ Found data in the specified date range!")
        print(f"   dispatch_history: {hist_count} records")
        print(f"   current_dispatches: {current_count} records")
        print("\n   Next step: We'll create dispatch_metrics from this data")
        print("   to populate the trend chart for the dashboard.")
    else:
        print("\n❌ No data found in the specified date range.")
        print("   Please check if:")
        print("   1. The date range is correct")
        print("   2. Data exists in the database")
        print("   3. The tables have been populated with historical data")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        search_date_range()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
