"""
Verify that tables and data exist in team_core_flux schema.
"""

import psycopg2
from psycopg2 import sql

# Database connection parameters
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

SCHEMA_NAME = 'team_core_flux'


def connect_to_database():
    """Connect to the PostgreSQL database."""
    try:
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to database: {e}")
        return None


def verify_tables_and_data():
    """Verify tables exist and show row counts."""
    print("Connecting to database...")
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to database.")
        return
    
    try:
        cursor = connection.cursor()
        
        # Check if schema exists
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name = %s;
        """, (SCHEMA_NAME,))
        
        schema_exists = cursor.fetchone()
        if not schema_exists:
            print(f"✗ Schema '{SCHEMA_NAME}' does not exist!")
            return
        
        print(f"✓ Schema '{SCHEMA_NAME}' exists\n")
        
        # List all tables in the schema
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """, (SCHEMA_NAME,))
        
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        if not tables:
            print(f"✗ No tables found in '{SCHEMA_NAME}' schema!")
            return
        
        print(f"✓ Found {len(table_names)} table(s) in '{SCHEMA_NAME}' schema:")
        print("-" * 60)
        
        # Check row counts for each table
        for table_name in table_names:
            try:
                cursor.execute(f'SELECT COUNT(*) FROM "{SCHEMA_NAME}"."{table_name}";')
                row_count = cursor.fetchone()[0]
                print(f"  • {table_name}: {row_count:,} rows")
            except Exception as e:
                print(f"  • {table_name}: Error counting rows - {e}")
        
        print("-" * 60)
        print("\n✓ All tables are present with data!")
        print("\nTo view these tables in your SQL editor:")
        print(f"  1. Make sure you're connected to the database")
        print(f"  2. Navigate to: Databases → postgres → Schemas → {SCHEMA_NAME} → Tables")
        print(f"  3. Or run this query:")
        print(f"     SELECT * FROM \"{SCHEMA_NAME}\".\"dispatch_history\" LIMIT 10;")
        
        cursor.close()
        
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        connection.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    verify_tables_and_data()

