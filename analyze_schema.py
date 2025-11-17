"""
Analyze the schema to understand the data structure for dispatch agent.
"""

import psycopg2

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

def analyze_schema():
    connection = psycopg2.connect(**DB_CONFIG)
    cursor = connection.cursor()
    
    print("=" * 80)
    print("SCHEMA ANALYSIS FOR SMART DISPATCH AGENT")
    print("=" * 80)
    
    # Analyze each table
    tables = ['technicians', 'current_dispatches', 'dispatch_history', 'technician_calendar']
    
    for table in tables:
        print(f"\n{'='*80}")
        print(f"TABLE: {table}")
        print(f"{'='*80}")
        
        # Get columns
        cursor.execute(f"""
            SELECT 
                column_name,
                data_type,
                is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'team_core_flux'
            AND table_name = %s
            ORDER BY ordinal_position;
        """, (table,))
        
        columns = cursor.fetchall()
        print("\nColumns:")
        for col in columns:
            print(f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        # Get sample data
        cursor.execute(f'SELECT * FROM "team_core_flux"."{table}" LIMIT 3;')
        samples = cursor.fetchall()
        if samples:
            print(f"\nSample Data (first 3 rows):")
            col_names = [desc[0] for desc in cursor.description]
            for i, row in enumerate(samples, 1):
                print(f"\n  Row {i}:")
                for j, val in enumerate(row):
                    print(f"    {col_names[j]}: {val}")
    
    cursor.close()
    connection.close()

if __name__ == "__main__":
    analyze_schema()

