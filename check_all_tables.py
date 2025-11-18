#!/usr/bin/env python3
"""
Check the structure of all tables
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

def check_tables():
    """Check all table structures"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*70)
    print("TABLE STRUCTURES IN team_core_flux SCHEMA")
    print("="*70)
    
    tables = ['technicians', 'current_dispatches', 'dispatch_history', 'technician_calendar', 'dispatch_metrics']
    
    for table in tables:
        print(f"\n📋 {table.upper()}")
        print("-" * 70)
        
        # Check if table exists
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'team_core_flux'
                AND table_name = %s
            )
        """, (table,))
        
        exists = cur.fetchone()[0]
        
        if not exists:
            print(f"  ❌ Table does not exist")
            continue
        
        # Get columns
        cur.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'team_core_flux'
            AND table_name = %s
            ORDER BY ordinal_position
        """, (table,))
        
        columns = cur.fetchall()
        print(f"  Columns ({len(columns)}):")
        for col in columns:
            print(f"    - {col[0]} ({col[1]})")
        
        # Get row count
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"  Total rows: {count}")
        
        # Get a sample row to see data
        if count > 0:
            cur.execute(f"SELECT * FROM {table} LIMIT 1")
            sample = cur.fetchone()
            col_names = [desc[0] for desc in cur.description]
            
            print(f"\n  Sample row:")
            for col_name, val in zip(col_names, sample):
                # Truncate long values
                val_str = str(val)
                if len(val_str) > 50:
                    val_str = val_str[:47] + "..."
                print(f"    {col_name}: {val_str}")
    
    print("\n" + "="*70)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    try:
        check_tables()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

