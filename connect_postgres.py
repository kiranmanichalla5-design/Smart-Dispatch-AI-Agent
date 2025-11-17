"""
PostgreSQL Database Connection Script
This script connects to a PostgreSQL database using the same parameters as DBeaver.
"""

import psycopg2
from psycopg2 import sql
import sys

# Database connection parameters (from DBeaver)
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'  # Default database, change if needed
}

# Schema name (change this to your desired schema)
SCHEMA_NAME = 'team_core_flux'  # Default schema is 'public', change as needed


def connect_to_database():
    """
    Connect to the PostgreSQL database.
    Returns the connection object if successful, None otherwise.
    """
    try:
        print("Attempting to connect to PostgreSQL database...")
        print(f"Host: {DB_CONFIG['host']}")
        print(f"Port: {DB_CONFIG['port']}")
        print(f"Database: {DB_CONFIG['database']}")
        print(f"User: {DB_CONFIG['user']}")
        
        # Create connection
        connection = psycopg2.connect(
            host=DB_CONFIG['host'],
            port=DB_CONFIG['port'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database']
        )
        
        print("✓ Successfully connected to the database!")
        return connection
        
    except psycopg2.Error as e:
        print(f"✗ Error connecting to database: {e}")
        return None


def set_schema(connection, schema_name):
    """
    Set the search path to the specified schema.
    This makes the schema the default for queries.
    """
    try:
        cursor = connection.cursor()
        
        # Set the search path to the specified schema
        cursor.execute(sql.SQL("SET search_path TO {}").format(
            sql.Identifier(schema_name)
        ))
        
        connection.commit()
        print(f"✓ Successfully connected to schema: {schema_name}")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Error setting schema: {e}")
        return False


def list_schemas(connection):
    """
    List all available schemas in the database.
    """
    try:
        cursor = connection.cursor()
        
        # Query to get all schemas
        cursor.execute("""
            SELECT schema_name 
            FROM information_schema.schemata 
            WHERE schema_name NOT IN ('pg_catalog', 'information_schema', 'pg_toast')
            ORDER BY schema_name;
        """)
        
        schemas = cursor.fetchall()
        
        print("\nAvailable schemas in the database:")
        print("-" * 40)
        for schema in schemas:
            print(f"  - {schema[0]}")
        print("-" * 40)
        
        cursor.close()
        return [schema[0] for schema in schemas]
        
    except psycopg2.Error as e:
        print(f"✗ Error listing schemas: {e}")
        return []


def test_connection(connection):
    """
    Test the connection by running a simple query.
    """
    try:
        cursor = connection.cursor()
        
        # Get current database and schema
        cursor.execute("SELECT current_database(), current_schema();")
        result = cursor.fetchone()
        
        print(f"\nCurrent Database: {result[0]}")
        print(f"Current Schema: {result[1]}")
        
        # Get PostgreSQL version
        cursor.execute("SELECT version();")
        version = cursor.fetchone()[0]
        print(f"PostgreSQL Version: {version.split(',')[0]}")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Error testing connection: {e}")
        return False


def find_table_schema(connection, table_name):
    """
    Find which schema contains the specified table.
    """
    try:
        cursor = connection.cursor()
        
        # Search for the table across all schemas
        cursor.execute("""
            SELECT table_schema 
            FROM information_schema.tables 
            WHERE table_name = %s
            ORDER BY table_schema;
        """, (table_name,))
        
        schemas = cursor.fetchall()
        
        result = []
        if schemas:
            print(f"\nFound '{table_name}' table in the following schema(s):")
            for schema in schemas:
                print(f"  - {schema[0]}")
            result = [schema[0] for schema in schemas]
        else:
            print(f"\n✗ Table '{table_name}' not found in any schema.")
        
        cursor.close()
        return result
        
    except psycopg2.Error as e:
        print(f"✗ Error searching for table: {e}")
        return []


def count_dispatch_history(connection, schema_name=None):
    """
    Count the number of records in the dispatch_history table.
    If schema_name is provided, it will query that specific schema.
    """
    try:
        cursor = connection.cursor()
        
        # Build the query with or without schema specification
        if schema_name:
            query = f'SELECT COUNT(*) FROM "{schema_name}"."dispatch_history";'
            print(f"\nQuerying 'dispatch_history' table in schema: {schema_name}")
        else:
            query = "SELECT COUNT(*) FROM dispatch_history;"
            print(f"\nQuerying 'dispatch_history' table in current schema")
        
        # Count records in dispatch_history table
        cursor.execute(query)
        count = cursor.fetchone()[0]
        
        print(f"📊 Record Count in 'dispatch_history' table: {count:,}")
        
        cursor.close()
        return count
        
    except psycopg2.Error as e:
        print(f"✗ Error querying dispatch_history table: {e}")
        return None


def list_tables_in_schema(connection, schema_name):
    """
    List all tables in the specified schema.
    """
    try:
        cursor = connection.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = %s
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """, (schema_name,))
        
        tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        
        cursor.close()
        return table_names
        
    except psycopg2.Error as e:
        print(f"✗ Error listing tables: {e}")
        return []


def get_table_create_statement(connection, schema_name, table_name):
    """
    Get the CREATE TABLE statement for a table by building it from metadata.
    """
    try:
        cursor = connection.cursor()
        
        # Get column information
        cursor.execute("""
            SELECT 
                column_name,
                data_type,
                character_maximum_length,
                numeric_precision,
                numeric_scale,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            ORDER BY ordinal_position;
        """, (schema_name, table_name))
        
        columns = cursor.fetchall()
        
        if not columns:
            print(f"  ✗ No columns found for table {table_name}")
            cursor.close()
            return None
        
        # Build CREATE TABLE statement
        col_defs = []
        for col in columns:
            col_name, data_type, max_length, num_precision, num_scale, is_nullable, default = col
            
            # Handle different data types
            # PostgreSQL integer types don't take size parameters
            if data_type in ['integer', 'bigint', 'smallint', 'real', 'double precision']:
                type_def = data_type
            elif max_length:
                type_def = f"{data_type}({max_length})"
            elif num_precision and num_scale:
                type_def = f"{data_type}({num_precision},{num_scale})"
            elif num_precision:
                # Only use precision for numeric/decimal types
                if data_type in ['numeric', 'decimal']:
                    type_def = f"{data_type}({num_precision})"
                else:
                    type_def = data_type
            else:
                type_def = data_type
            
            # Add NOT NULL if applicable
            null_def = "" if is_nullable == 'YES' else " NOT NULL"
            
            # Add default if applicable (handle properly)
            default_def = ""
            if default:
                # Remove any schema prefixes from default values
                default_clean = default.replace(f'"{schema_name}".', '')
                default_def = f" DEFAULT {default_clean}"
            
            col_defs.append(f'"{col_name}" {type_def}{null_def}{default_def}')
        
        # Get primary key constraints
        cursor.execute("""
            SELECT a.attname
            FROM pg_index i
            JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY(i.indkey)
            WHERE i.indrelid = %s::regclass
            AND i.indisprimary
            ORDER BY array_position(i.indkey, a.attnum);
        """, (f'"{schema_name}"."{table_name}"',))
        
        pk_cols = [row[0] for row in cursor.fetchall()]
        pk_def = ""
        if pk_cols:
            pk_cols_quoted = ', '.join([f'"{col}"' for col in pk_cols])
            pk_def = f',\n    PRIMARY KEY ({pk_cols_quoted})'
        
        create_stmt = f'CREATE TABLE "{schema_name}"."{table_name}" (\n    ' + \
                     ',\n    '.join(col_defs) + pk_def + '\n);'
        
        cursor.close()
        return create_stmt
        
    except psycopg2.Error as e:
        print(f"  ✗ Error getting table structure: {e}")
        return None


def copy_table_structure(connection, source_schema, dest_schema, table_name):
    """
    Copy table structure from source schema to destination schema.
    """
    try:
        cursor = connection.cursor()
        
        # Get the CREATE TABLE statement
        create_stmt = get_table_create_statement(connection, source_schema, table_name)
        
        if not create_stmt:
            print(f"  ✗ Could not get table structure for {table_name}")
            return False
        
        # Modify the CREATE statement to use destination schema
        create_stmt = create_stmt.replace(f'"{source_schema}"."{table_name}"', 
                                         f'"{dest_schema}"."{table_name}"')
        
        # Execute the CREATE TABLE statement
        cursor.execute(create_stmt)
        connection.commit()
        
        print(f"  ✓ Created table structure: {table_name}")
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        # Check if table already exists
        if "already exists" in str(e):
            print(f"  ⚠ Table {table_name} already exists in destination schema, skipping structure creation")
            return True
        else:
            print(f"  ✗ Error copying table structure for {table_name}: {e}")
            connection.rollback()
            return False


def copy_table_data(connection, source_schema, dest_schema, table_name):
    """
    Copy all data from source table to destination table.
    """
    try:
        cursor = connection.cursor()
        
        # First, check if table exists in destination
        cursor.execute("""
            SELECT COUNT(*) 
            FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = %s;
        """, (dest_schema, table_name))
        
        if cursor.fetchone()[0] == 0:
            print(f"  ✗ Table {table_name} does not exist in destination schema")
            cursor.close()
            return False
        
        # Get row count from source
        cursor.execute(f'SELECT COUNT(*) FROM "{source_schema}"."{table_name}";')
        source_count = cursor.fetchone()[0]
        
        if source_count == 0:
            print(f"  ℹ No data to copy from {table_name} (0 rows)")
            cursor.close()
            return True
        
        # Copy data using INSERT INTO ... SELECT
        copy_query = f'INSERT INTO "{dest_schema}"."{table_name}" SELECT * FROM "{source_schema}"."{table_name}";'
        cursor.execute(copy_query)
        connection.commit()
        
        # Verify the copy
        cursor.execute(f'SELECT COUNT(*) FROM "{dest_schema}"."{table_name}";')
        dest_count = cursor.fetchone()[0]
        
        print(f"  ✓ Copied {dest_count:,} rows to {table_name}")
        
        cursor.close()
        return True
        
    except psycopg2.Error as e:
        print(f"  ✗ Error copying data for {table_name}: {e}")
        connection.rollback()
        return False


def copy_schema_tables_and_data(connection, source_schema, dest_schema):
    """
    Copy all tables and their data from source schema to destination schema.
    """
    print(f"\n{'=' * 60}")
    print(f"Copying tables from '{source_schema}' to '{dest_schema}'")
    print(f"{'=' * 60}\n")
    
    # Ensure destination schema exists
    try:
        cursor = connection.cursor()
        cursor.execute(sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(
            sql.Identifier(dest_schema)
        ))
        connection.commit()
        cursor.close()
        print(f"✓ Destination schema '{dest_schema}' is ready\n")
    except psycopg2.Error as e:
        print(f"✗ Error creating destination schema: {e}")
        return False
    
    # List all tables in source schema
    print(f"📋 Finding tables in '{source_schema}' schema...")
    tables = list_tables_in_schema(connection, source_schema)
    
    if not tables:
        print(f"✗ No tables found in '{source_schema}' schema")
        return False
    
    print(f"✓ Found {len(tables)} table(s): {', '.join(tables)}\n")
    
    # Copy each table
    success_count = 0
    failed_tables = []
    
    for i, table_name in enumerate(tables, 1):
        print(f"[{i}/{len(tables)}] Processing table: {table_name}")
        
        # Step 1: Copy table structure
        if copy_table_structure(connection, source_schema, dest_schema, table_name):
            # Step 2: Copy table data
            if copy_table_data(connection, source_schema, dest_schema, table_name):
                success_count += 1
                print(f"  ✓ Successfully copied {table_name}\n")
            else:
                failed_tables.append(table_name)
                print(f"  ✗ Failed to copy data for {table_name}\n")
        else:
            failed_tables.append(table_name)
            print(f"  ✗ Failed to copy structure for {table_name}\n")
    
    # Summary
    print(f"\n{'=' * 60}")
    print("COPY SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total tables: {len(tables)}")
    print(f"Successfully copied: {success_count}")
    if failed_tables:
        print(f"Failed: {len(failed_tables)}")
        print(f"Failed tables: {', '.join(failed_tables)}")
    print(f"{'=' * 60}\n")
    
    return success_count == len(tables)


def main():
    """
    Main function to connect to database and copy schema.
    """
    print("=" * 60)
    print("PostgreSQL Schema Copy Script")
    print("=" * 60)
    print()
    
    # Step 1: Connect to database
    connection = connect_to_database()
    if not connection:
        print("\nFailed to connect. Please check your connection parameters.")
        sys.exit(1)
    
    try:
        # Step 2: Copy tables and data from SmartDispatchAgentDataset to team_core_flux
        source_schema = 'SmartDispatchAgentDataset'
        dest_schema = 'team_core_flux'
        
        success = copy_schema_tables_and_data(connection, source_schema, dest_schema)
        
        if success:
            print("✓ All tables and data copied successfully!")
        else:
            print("⚠ Some tables may have failed to copy. Check the summary above.")
        
    finally:
        # Close connection when done
        print("\nClosing database connection...")
        connection.close()
        print("✓ Connection closed.")


if __name__ == "__main__":
    main()
