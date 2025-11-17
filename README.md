# PostgreSQL Database Connection Script

This Python script connects to a PostgreSQL database using the same connection parameters as DBeaver.

## Setup Instructions

### 1. Install Python
Make sure you have Python installed on your computer. You can download it from [python.org](https://www.python.org/downloads/).

### 2. Install Required Package
Open a terminal/command prompt in this folder and run:

```bash
pip install -r requirements.txt
```

### 3. Configure Connection (Optional)
The connection parameters are already set in `connect_postgres.py`:
- Host: 212.2.245.85
- Port: 6432
- User: postgres
- Password: Tea_IWMZ5wuUta97gupb
- Database: postgres (default)

If you need to change the schema, edit line 19 in `connect_postgres.py`:
```python
SCHEMA_NAME = 'public'  # Change this to your desired schema name
```

### 4. Run the Script
```bash
python connect_postgres.py
```

## What the Script Does

1. **Connects** to the PostgreSQL database
2. **Lists** all available schemas
3. **Connects** to the specified schema (default: 'public')
4. **Tests** the connection and displays database information
5. **Closes** the connection when done

## Example Usage

After running the script, you can modify it to run your own queries. For example:

```python
cursor = connection.cursor()
cursor.execute("SELECT * FROM your_table LIMIT 10;")
results = cursor.fetchall()
for row in results:
    print(row)
cursor.close()
```

## Troubleshooting

- **Connection Error**: Check if the database server is accessible and your firewall allows the connection
- **Schema Not Found**: Make sure the schema name exists. The script will list all available schemas
- **Module Not Found**: Run `pip install -r requirements.txt` again
