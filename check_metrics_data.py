"""
Check what's actually in the dispatch_metrics table
"""

import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'options': '-c search_path=team_core_flux'
}

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor(cursor_factory=RealDictCursor)

print("="*60)
print("DISPATCH METRICS TABLE ANALYSIS")
print("="*60)

# Check total rows
cursor.execute("SELECT COUNT(*) as total FROM dispatch_metrics;")
print(f"\nTotal rows: {cursor.fetchone()['total']}")

# Check sample data
cursor.execute("""
    SELECT 
        dispatch_id,
        routing_seconds,
        estimated_completion_minutes,
        operational_cost,
        sla_breached,
        burnout_risk,
        created_at,
        updated_at
    FROM dispatch_metrics
    ORDER BY updated_at DESC
    LIMIT 5;
""")

print("\nSample records (latest 5):")
for row in cursor.fetchall():
    print(f"\n  Dispatch ID: {row['dispatch_id']}")
    print(f"  Routing Seconds: {row['routing_seconds']}")
    print(f"  ETC Minutes: {row['estimated_completion_minutes']}")
    print(f"  Cost: ${row['operational_cost']}")
    print(f"  Created: {row['created_at']}")
    print(f"  Updated: {row['updated_at']}")

# Check date range
cursor.execute("""
    SELECT 
        MIN(DATE(updated_at)) as earliest,
        MAX(DATE(updated_at)) as latest,
        COUNT(DISTINCT DATE(updated_at)) as unique_dates
    FROM dispatch_metrics;
""")
dates = cursor.fetchone()
print(f"\nDate range:")
print(f"  Earliest: {dates['earliest']}")
print(f"  Latest: {dates['latest']}")
print(f"  Unique dates: {dates['unique_dates']}")

# Check average routing_seconds
cursor.execute("""
    SELECT 
        AVG(routing_seconds) as avg_routing,
        MIN(routing_seconds) as min_routing,
        MAX(routing_seconds) as max_routing
    FROM dispatch_metrics
    WHERE routing_seconds IS NOT NULL;
""")
stats = cursor.fetchone()
print(f"\nRouting seconds statistics:")
print(f"  Average: {stats['avg_routing']}")
print(f"  Min: {stats['min_routing']}")
print(f"  Max: {stats['max_routing']}")

cursor.close()
conn.close()

print("\n" + "="*60)

