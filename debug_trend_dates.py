#!/usr/bin/env python3
"""
Debug script to see what dates the trend query is returning
"""

import psycopg2
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

def check_trend_dates():
    """Check what dates are in the trend data"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*60)
    print("TREND DATA DEBUG")
    print("="*60)
    
    # Check raw timestamps
    print("\nRaw timestamps (latest 10):")
    cur.execute("""
        SELECT 
            dispatch_id,
            updated_at,
            updated_at::date as date_only,
            TO_CHAR(updated_at, 'YYYY-MM-DD HH24:MI:SS TZ') as formatted
        FROM dispatch_metrics
        ORDER BY updated_at DESC
        LIMIT 10
    """)
    
    for row in cur.fetchall():
        print(f"  ID: {row[0]}, Updated: {row[1]}, Date: {row[2]}, Formatted: {row[3]}")
    
    # Check the actual trend query
    print("\nTrend query (last 14 days grouped):")
    cur.execute("""
        SELECT 
            DATE(updated_at) as trend_date,
            COUNT(*) as count,
            AVG(ABS(routing_seconds)) / 60.0 as avg_routing_min,
            AVG(estimated_completion_minutes) as avg_etc
        FROM dispatch_metrics
        WHERE updated_at >= NOW() - INTERVAL '14 days'
        GROUP BY DATE(updated_at)
        ORDER BY DATE(updated_at) ASC
    """)
    
    rows = cur.fetchall()
    print(f"\nFound {len(rows)} date groups:")
    for row in rows:
        print(f"  Date: {row[0]}, Count: {row[1]}, Avg Routing: {float(row[2]):.2f} min, Avg ETC: {float(row[3]):.2f} min")
    
    # Check server timezone
    print("\nDatabase timezone info:")
    cur.execute("SHOW timezone")
    tz = cur.fetchone()[0]
    print(f"  Database timezone: {tz}")
    
    cur.execute("SELECT NOW(), CURRENT_DATE, CURRENT_TIMESTAMP")
    now_info = cur.fetchone()
    print(f"  Database NOW(): {now_info[0]}")
    print(f"  Database CURRENT_DATE: {now_info[1]}")
    print(f"  Database CURRENT_TIMESTAMP: {now_info[2]}")
    
    # Local system time
    print(f"\nLocal system time: {datetime.now()}")
    print(f"Local system date: {datetime.now().date()}")
    
    print("="*60)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        check_trend_dates()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

