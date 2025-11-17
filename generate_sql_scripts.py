"""
Generate SQL scripts for all tables in team_core_flux schema.
This script creates SQL CREATE TABLE statements that can be run in any SQL editor.
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


def get_table_create_statement(connection, schema_name, table_name):
    """Generate CREATE TABLE statement for a table."""
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
            return None
        
        # Build CREATE TABLE statement
        col_defs = []
        for col in columns:
            col_name, data_type, max_length, num_precision, num_scale, is_nullable, default = col
            
            # Handle different data types
            if data_type in ['integer', 'bigint', 'smallint', 'real', 'double precision']:
                type_def = data_type
            elif max_length:
                type_def = f"{data_type}({max_length})"
            elif num_precision and num_scale:
                type_def = f"{data_type}({num_precision},{num_scale})"
            elif num_precision:
                if data_type in ['numeric', 'decimal']:
                    type_def = f"{data_type}({num_precision})"
                else:
                    type_def = data_type
            else:
                type_def = data_type
            
            # Add NOT NULL if applicable
            null_def = "" if is_nullable == 'YES' else " NOT NULL"
            
            # Add default if applicable
            default_def = ""
            if default:
                default_clean = default.replace(f'"{schema_name}".', '')
                default_def = f" DEFAULT {default_clean}"
            
            col_defs.append(f'    "{col_name}" {type_def}{null_def}{default_def}')
        
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
        
        create_stmt = f'CREATE TABLE "{schema_name}"."{table_name}" (\n' + \
                     ',\n'.join(col_defs) + pk_def + '\n);'
        
        cursor.close()
        return create_stmt
        
    except psycopg2.Error as e:
        print(f"Error getting table structure for {table_name}: {e}")
        return None


def list_tables_in_schema(connection, schema_name):
    """List all tables in the specified schema."""
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
        print(f"Error listing tables: {e}")
        return []


def generate_sql_scripts():
    """Generate SQL scripts for all tables."""
    print("Connecting to database...")
    connection = connect_to_database()
    if not connection:
        print("Failed to connect to database.")
        return
    
    try:
        # List all tables
        print(f"Finding tables in '{SCHEMA_NAME}' schema...")
        tables = list_tables_in_schema(connection, SCHEMA_NAME)
        
        if not tables:
            print(f"No tables found in '{SCHEMA_NAME}' schema.")
            return
        
        print(f"Found {len(tables)} table(s).\n")
        
        # Generate SQL for each table
        sql_output = []
        sql_output.append(f"-- SQL Scripts for tables in '{SCHEMA_NAME}' schema")
        sql_output.append(f"-- Generated automatically")
        sql_output.append(f"-- Schema: {SCHEMA_NAME}\n")
        sql_output.append(f"-- Ensure the schema exists")
        sql_output.append(f"CREATE SCHEMA IF NOT EXISTS \"{SCHEMA_NAME}\";\n")
        sql_output.append("=" * 80 + "\n")
        
        for i, table_name in enumerate(tables, 1):
            print(f"[{i}/{len(tables)}] Generating SQL for: {table_name}")
            
            sql_output.append(f"\n-- Table: {table_name}")
            sql_output.append(f"-- {'=' * 76}\n")
            
            # Get CREATE TABLE statement
            create_stmt = get_table_create_statement(connection, SCHEMA_NAME, table_name)
            
            if create_stmt:
                sql_output.append(create_stmt)
                sql_output.append("\n")
            else:
                sql_output.append(f"-- Error: Could not generate CREATE TABLE for {table_name}\n")
        
        # Write to file
        output_file = f"team_core_flux_schema.sql"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sql_output))
        
        print(f"\n✓ SQL scripts generated successfully!")
        print(f"✓ Output file: {output_file}")
        print(f"\nYou can now copy the SQL from '{output_file}' and run it in your SQL editor.")
        
    finally:
        connection.close()
        print("\nConnection closed.")


if __name__ == "__main__":
    generate_sql_scripts()

