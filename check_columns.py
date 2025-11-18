#!/usr/bin/env python3
"""
Check the actual columns in dispatch_metrics table
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

def check_columns():
    """Check columns in dispatch_metrics"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    print("\n" + "="*60)
    print("DISPATCH_METRICS TABLE STRUCTURE")
    print("="*60)
    
    cur.execute("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = 'team_core_flux'
        AND table_name = 'dispatch_metrics'
        ORDER BY ordinal_position
    """)
    
    print("\nColumns:")
    for row in cur.fetchall():
        print(f"  - {row[0]} ({row[1]}) {'NULL' if row[2] == 'YES' else 'NOT NULL'}")
    
    # Get a sample row
    print("\nSample row:")
    cur.execute("SELECT * FROM dispatch_metrics LIMIT 1")
    cols = [desc[0] for desc in cur.description]
    row = cur.fetchone()
    
    for col, val in zip(cols, row):
        print(f"  {col}: {val}")
    
    print("="*60)
    
    cur.close()
    conn.close()

if __name__ == '__main__':
    check_columns()

