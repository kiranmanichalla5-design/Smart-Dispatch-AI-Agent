"""
Simplified Technician Dashboard - No templates needed
Works directly in browser
"""

from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    """Simple HTML page embedded in Python"""
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Technician Dashboard</title>
        <style>
            body { font-family: Arial; margin: 20px; background: #f5f5f5; }
            .header { background: #667eea; color: white; padding: 20px; border-radius: 10px; }
            .card { background: white; padding: 15px; margin: 10px 0; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .status { padding: 5px 10px; border-radius: 5px; color: white; font-weight: bold; }
            .available { background: #28a745; }
            .nearly-full { background: #ffc107; color: #000; }
            .fully-booked { background: #dc3545; }
            .loading { text-align: center; padding: 20px; }
            button { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; }
            button:hover { background: #5568d3; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔧 Technician Dashboard</h1>
            <p>Smart Dispatch Agent - Real-time Status</p>
            <button onclick="loadData()">🔄 Refresh Data</button>
        </div>
        
        <div id="stats" class="card">
            <h3>Statistics</h3>
            <div id="statsContent" class="loading">Loading...</div>
        </div>
        
        <div id="technicians" class="card">
            <h3>Technicians</h3>
            <div id="techContent" class="loading">Loading technicians...</div>
        </div>
        
        <script>
            function loadData() {
                document.getElementById('techContent').innerHTML = '<div class="loading">Loading...</div>';
                
                fetch('/api/technicians')
                    .then(r => r.json())
                    .then(data => {
                        if (data.success) {
                            let html = '<table border="1" cellpadding="10" style="width:100%; border-collapse: collapse;">';
                            html += '<tr style="background:#f0f0f0;"><th>Name</th><th>ID</th><th>Skill</th><th>Location</th><th>Status</th><th>Workload</th><th>Dispatches</th></tr>';
                            
                            data.technicians.forEach(tech => {
                                const statusClass = tech.Availability_Status === 'Available' ? 'available' : 
                                                   tech.Availability_Status === 'Nearly Full' ? 'nearly-full' : 'fully-booked';
                                
                                html += '<tr>';
                                html += '<td><strong>' + (tech.Name || 'N/A') + '</strong></td>';
                                html += '<td>' + tech.Technician_id + '</td>';
                                html += '<td>' + (tech.Primary_skill || 'N/A') + '</td>';
                                html += '<td>' + (tech.City || 'N/A') + ', ' + (tech.State || 'N/A') + '</td>';
                                html += '<td><span class="status ' + statusClass + '">' + tech.Availability_Status + '</span></td>';
                                html += '<td>' + (tech.Current_assignments || 0) + ' / ' + (tech.Workload_capacity || 0) + '</td>';
                                html += '<td>' + (tech.Assigned_Dispatches || 0) + '</td>';
                                html += '</tr>';
                            });
                            
                            html += '</table>';
                            document.getElementById('techContent').innerHTML = html;
                            
                            // Update stats
                            document.getElementById('statsContent').innerHTML = 
                                '<p><strong>Total Technicians:</strong> ' + data.total + '</p>' +
                                '<p><strong>Available:</strong> ' + data.technicians.filter(t => t.Availability_Status === 'Available').length + '</p>';
                        } else {
                            document.getElementById('techContent').innerHTML = '<p style="color:red;">Error: ' + data.error + '</p>';
                        }
                    })
                    .catch(err => {
                        document.getElementById('techContent').innerHTML = '<p style="color:red;">Error loading data: ' + err + '</p>';
                    });
            }
            
            // Load on page load
            window.onload = loadData;
        </script>
    </body>
    </html>
    '''

@app.route('/api/technicians')
def get_technicians():
    """Get all technicians"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                t."Technician_id",
                t."Name",
                t."Primary_skill",
                t."City",
                t."State",
                t."Workload_capacity",
                t."Current_assignments",
                CASE 
                    WHEN t."Workload_capacity" = 0 THEN 'No Capacity'
                    WHEN t."Current_assignments" >= t."Workload_capacity" THEN 'Fully Booked'
                    WHEN t."Current_assignments" >= (t."Workload_capacity" * 0.8) THEN 'Nearly Full'
                    ELSE 'Available'
                END as Availability_Status,
                COUNT(d."Dispatch_id") as Assigned_Dispatches
            FROM "team_core_flux"."technicians" t
            LEFT JOIN "team_core_flux"."current_dispatches" d
                ON t."Technician_id" = d."Optimized_technician_id"
                AND d."Optimization_status" = 'completed'
            GROUP BY 
                t."Technician_id", t."Name", t."Primary_skill", 
                t."City", t."State", t."Workload_capacity", t."Current_assignments"
            ORDER BY t."Name";
        """
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        technicians = []
        for row in rows:
            tech = dict(zip(columns, row))
            technicians.append(tech)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'technicians': technicians,
            'total': len(technicians)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("=" * 60)
    print("SIMPLIFIED TECHNICIAN DASHBOARD")
    print("=" * 60)
    print("✅ No templates needed - everything embedded")
    print("✅ Open in browser: http://127.0.0.1:5003")
    print("✅ Press Ctrl+C to stop")
    print("=" * 60)
    try:
        app.run(debug=True, host='127.0.0.1', port=5003)
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

