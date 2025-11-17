"""
Simple test script to verify database connection works.
Run this first before running the main agent.
"""

import psycopg2

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

print("=" * 60)
print("TESTING DATABASE CONNECTION")
print("=" * 60)
print()

try:
    print("Attempting to connect...")
    connection = psycopg2.connect(**DB_CONFIG)
    print("✅ SUCCESS! Connected to database!")
    print()
    
    # Test a simple query
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."technicians";')
    count = cursor.fetchone()[0]
    print(f"✅ Found {count} technicians in database")
    
    cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."current_dispatches" WHERE "Optimization_status" = \'pending\';')
    pending = cursor.fetchone()[0]
    print(f"✅ Found {pending} pending dispatches")
    
    cursor.close()
    connection.close()
    print()
    print("=" * 60)
    print("✅ ALL TESTS PASSED! Ready to run smart_dispatch_agent.py")
    print("=" * 60)
    
except Exception as e:
    print()
    print("=" * 60)
    print("❌ ERROR: Connection failed!")
    print("=" * 60)
    print(f"Error message: {e}")
    print()
    print("Troubleshooting:")
    print("1. Check your internet connection")
    print("2. Verify database credentials are correct")
    print("3. Make sure database server is accessible")
    print("=" * 60)

