"""
Test Dashboard API endpoints to identify issues
"""

import psycopg2
import json

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres',
    'options': '-c search_path=team_core_flux'
}

def test_connection():
    """Test basic connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Database connection successful")
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_technicians_query():
    """Test the technicians query"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        query = """
            SELECT 
                t."Technician_id",
                t."Name",
                t."Primary_skill",
                t."Workload_capacity",
                t."Current_assignments",
                CASE 
                    WHEN t."Workload_capacity" = 0 THEN 'No Capacity'
                    WHEN t."Current_assignments" >= t."Workload_capacity" THEN 'Fully Booked'
                    WHEN t."Current_assignments" >= (t."Workload_capacity" * 0.8) THEN 'Nearly Full'
                    ELSE 'Available'
                END as Availability_Status
            FROM "team_core_flux"."technicians" t
            LIMIT 5;
        """
        
        cursor.execute(query)
        rows = cursor.fetchall()
        print(f"\n✅ Technicians query successful - Found {cursor.rowcount} rows")
        print(f"   Column names: {[desc[0] for desc in cursor.description]}")
        if rows:
            print(f"   Sample row: {rows[0]}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n❌ Technicians query failed: {e}")
        return False

def test_dispatch_metrics_table():
    """Test if dispatch_metrics table exists"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'team_core_flux' 
                AND table_name = 'dispatch_metrics'
            );
        """)
        exists = cursor.fetchone()[0]
        
        if exists:
            cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."dispatch_metrics";')
            count = cursor.fetchone()[0]
            print(f"\n✅ dispatch_metrics table exists with {count} rows")
        else:
            print(f"\n⚠️  dispatch_metrics table does NOT exist")
            print("   This table is created by enhanced_dispatch_agent.py")
            print("   Run: python enhanced_dispatch_agent.py")
        
        cursor.close()
        conn.close()
        return exists
    except Exception as e:
        print(f"\n❌ dispatch_metrics check failed: {e}")
        return False

def test_stats_query():
    """Test the stats query"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Total technicians
        cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."technicians";')
        total_technicians = cursor.fetchone()[0]
        
        # Total dispatches
        cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."current_dispatches";')
        total_dispatches = cursor.fetchone()[0]
        
        print(f"\n✅ Stats query successful")
        print(f"   Total technicians: {total_technicians}")
        print(f"   Total dispatches: {total_dispatches}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"\n❌ Stats query failed: {e}")
        return False

def main():
    print("="*60)
    print("DASHBOARD API TEST")
    print("="*60)
    
    # Run tests
    test_connection()
    test_technicians_query()
    test_stats_query()
    metrics_exists = test_dispatch_metrics_table()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    if not metrics_exists:
        print("\n⚠️  ISSUE FOUND: dispatch_metrics table is missing")
        print("\n📋 TO FIX:")
        print("   1. Run: python enhanced_dispatch_agent.py")
        print("   2. This will create the dispatch_metrics table")
        print("   3. Then refresh the dashboard")
        print("\n   OR use a simpler dashboard without metrics:")
        print("   - The dashboard will work but some metrics will be empty")
    else:
        print("\n✅ All checks passed! Dashboard should work.")
    
    print("="*60)

if __name__ == "__main__":
    main()

