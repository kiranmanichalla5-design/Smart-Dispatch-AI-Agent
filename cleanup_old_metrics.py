#!/usr/bin/env python3
"""
Clean up old dispatch_metrics and keep only the data from the specified range
"""

import psycopg2

# Database connection
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres',
    'options': '-c search_path=team_core_flux'
}

def cleanup_metrics():
    """Remove old metrics outside the desired date range"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*70)
    print("CLEANING UP OLD DISPATCH_METRICS")
    print("="*70)
    
    # Check current state
    cur.execute("SELECT COUNT(*), MIN(updated_at), MAX(updated_at) FROM dispatch_metrics")
    row = cur.fetchone()
    print(f"\n📊 Current state:")
    print(f"   Total records: {row[0]}")
    print(f"   Date range: {row[1]} to {row[2]}")
    
    # Show breakdown by date range
    print(f"\n📅 Breakdown:")
    cur.execute("""
        SELECT 
            CASE 
                WHEN updated_at::date < '2025-11-12' THEN 'Before Nov 12, 2025'
                WHEN updated_at::date BETWEEN '2025-11-12' AND '2026-02-09' THEN 'Target Range (Nov 12 - Feb 9)'
                ELSE 'After Feb 9, 2026'
            END as range_group,
            COUNT(*) as count,
            MIN(updated_at::date) as earliest,
            MAX(updated_at::date) as latest
        FROM dispatch_metrics
        GROUP BY range_group
        ORDER BY MIN(updated_at::date)
    """)
    
    for row in cur.fetchall():
        print(f"   {row[0]}: {row[1]} records ({row[2]} to {row[3]})")
    
    # Delete records outside Nov 12, 2025 - Feb 9, 2026
    print(f"\n🗑️  Deleting records outside the target range...")
    cur.execute("""
        DELETE FROM dispatch_metrics
        WHERE updated_at::date < '2025-11-12' 
        OR updated_at::date > '2026-02-09'
    """)
    
    deleted = cur.rowcount
    conn.commit()
    
    print(f"   ✅ Deleted {deleted} records")
    
    # Show final state
    cur.execute("SELECT COUNT(*), MIN(updated_at), MAX(updated_at) FROM dispatch_metrics")
    row = cur.fetchone()
    print(f"\n📊 Final state:")
    print(f"   Total records: {row[0]}")
    print(f"   Date range: {row[1]} to {row[2]}")
    
    # Show daily breakdown
    print(f"\n📈 Daily breakdown:")
    cur.execute("""
        SELECT 
            DATE(updated_at) as date,
            COUNT(*) as count,
            ROUND(AVG(routing_seconds) / 60.0, 2) as avg_routing_min,
            ROUND(AVG(estimated_completion_minutes), 2) as avg_etc_min
        FROM dispatch_metrics
        GROUP BY DATE(updated_at)
        ORDER BY DATE(updated_at)
    """)
    
    rows = cur.fetchall()
    print(f"   {len(rows)} days with data:")
    for row in rows:
        print(f"     {row[0]}: {row[1]} dispatches (Routing: {row[2]}min, ETC: {row[3]}min)")
    
    print("\n" + "="*70)
    print("✅ CLEANUP COMPLETE!")
    print("="*70)
    print("\n📈 Refresh your dashboard to see the updated trend chart!")
    print("   URL: http://localhost:5000")
    print("")
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        cleanup_metrics()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

