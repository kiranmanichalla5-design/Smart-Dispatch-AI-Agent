"""
Simple test to verify Flask and database connection work
"""

from flask import Flask
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

@app.route('/')
def test():
    return '''
    <h1>✅ Flask is Working!</h1>
    <p>If you see this, Flask is running correctly.</p>
    <p><a href="/test-db">Test Database Connection</a></p>
    '''

@app.route('/test-db')
def test_db():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."technicians";')
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return f'''
        <h1>✅ Database Connection Works!</h1>
        <p>Found {count} technicians in database.</p>
        <p><a href="/">Back to Home</a></p>
        '''
    except Exception as e:
        return f'''
        <h1>❌ Database Error</h1>
        <p>Error: {str(e)}</p>
        <p><a href="/">Back to Home</a></p>
        '''

if __name__ == '__main__':
    print("=" * 60)
    print("SIMPLE TEST SERVER")
    print("=" * 60)
    print("Open: http://localhost:5001")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5001)

