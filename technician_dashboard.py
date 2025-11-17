"""
Technician Dashboard - Web UI
Shows all technicians with their status, assignments, and priority dispatches.
"""

from flask import Flask, render_template, jsonify
import psycopg2
from datetime import datetime
import json

app = Flask(__name__)

# Database configuration
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

SCHEMA_NAME = 'team_core_flux'


def get_db_connection():
    """Create database connection"""
    return psycopg2.connect(**DB_CONFIG)


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('technician_dashboard.html')


@app.route('/api/technicians')
def get_technicians():
    """Get all technicians with their status and assignments"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                t."Technician_id",
                t."Name",
                t."Primary_skill",
                t."City",
                t."County",
                t."State",
                t."Latitude",
                t."Longitude",
                t."Workload_capacity",
                t."Current_assignments",
                CASE 
                    WHEN t."Workload_capacity" = 0 THEN 'No Capacity'
                    WHEN t."Current_assignments" >= t."Workload_capacity" THEN 'Fully Booked'
                    WHEN t."Current_assignments" >= (t."Workload_capacity" * 0.8) THEN 'Nearly Full'
                    ELSE 'Available'
                END as Availability_Status,
                ROUND(
                    CASE 
                        WHEN t."Workload_capacity" > 0 
                        THEN (t."Current_assignments"::FLOAT / t."Workload_capacity") * 100
                        ELSE 0 
                    END, 
                    2
                ) as Utilization_Percentage,
                COUNT(d."Dispatch_id") as Assigned_Dispatches,
                COUNT(CASE WHEN d."Priority" = 'Critical' THEN 1 END) as Critical_Count,
                COUNT(CASE WHEN d."Priority" = 'High' THEN 1 END) as High_Count,
                COUNT(CASE WHEN d."Priority" = 'Normal' THEN 1 END) as Normal_Count,
                COUNT(CASE WHEN d."Priority" = 'Low' THEN 1 END) as Low_Count,
                AVG(CAST(d."Optimization_confidence" AS FLOAT)) as Avg_Confidence
            FROM "team_core_flux"."technicians" t
            LEFT JOIN "team_core_flux"."current_dispatches" d
                ON t."Technician_id" = d."Optimized_technician_id"
                AND d."Optimization_status" = 'completed'
            GROUP BY 
                t."Technician_id",
                t."Name",
                t."Primary_skill",
                t."City",
                t."County",
                t."State",
                t."Latitude",
                t."Longitude",
                t."Workload_capacity",
                t."Current_assignments"
            ORDER BY t."Name";
        """
        
        cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        technicians = []
        for row in rows:
            tech = dict(zip(columns, row))
            
            # Determine status color
            if tech['Availability_Status'] == 'Available':
                tech['status_color'] = 'green'
                tech['status_badge'] = 'success'
            elif tech['Availability_Status'] == 'Nearly Full':
                tech['status_color'] = 'orange'
                tech['status_badge'] = 'warning'
            elif tech['Availability_Status'] == 'Fully Booked':
                tech['status_color'] = 'red'
                tech['status_badge'] = 'danger'
            else:
                tech['status_color'] = 'gray'
                tech['status_badge'] = 'secondary'
            
            # Calculate priority level
            total_priority = (tech['Critical_Count'] or 0) * 4 + \
                           (tech['High_Count'] or 0) * 3 + \
                           (tech['Normal_Count'] or 0) * 2 + \
                           (tech['Low_Count'] or 0) * 1
            
            if total_priority >= 10:
                tech['priority_level'] = 'Critical'
                tech['priority_color'] = 'red'
            elif total_priority >= 5:
                tech['priority_level'] = 'High'
                tech['priority_color'] = 'orange'
            elif total_priority > 0:
                tech['priority_level'] = 'Normal'
                tech['priority_color'] = 'blue'
            else:
                tech['priority_level'] = 'None'
                tech['priority_color'] = 'gray'
            
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


@app.route('/api/technician/<technician_id>/dispatches')
def get_technician_dispatches(technician_id):
    """Get all dispatches assigned to a specific technician"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT 
                "Dispatch_id",
                "Ticket_type",
                "Order_type",
                "Priority",
                "Required_skill",
                "Status",
                "City",
                "State",
                "Customer_latitude",
                "Customer_longitude",
                "Appointment_start_datetime",
                "Appointment_end_datetime",
                "Duration_min",
                "Optimization_confidence",
                "Optimization_status"
            FROM "team_core_flux"."current_dispatches"
            WHERE "Optimized_technician_id" = %s
            ORDER BY 
                CASE "Priority"
                    WHEN 'Critical' THEN 1
                    WHEN 'High' THEN 2
                    WHEN 'Normal' THEN 3
                    WHEN 'Low' THEN 4
                    ELSE 5
                END,
                "Appointment_start_datetime";
        """
        
        cursor.execute(query, (technician_id,))
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        
        dispatches = []
        for row in rows:
            dispatch = dict(zip(columns, row))
            
            # Priority color
            priority = dispatch.get('Priority', 'Normal')
            if priority == 'Critical':
                dispatch['priority_color'] = 'red'
                dispatch['priority_badge'] = 'danger'
            elif priority == 'High':
                dispatch['priority_color'] = 'orange'
                dispatch['priority_badge'] = 'warning'
            elif priority == 'Normal':
                dispatch['priority_color'] = 'blue'
                dispatch['priority_badge'] = 'info'
            else:
                dispatch['priority_color'] = 'gray'
                dispatch['priority_badge'] = 'secondary'
            
            dispatches.append(dispatch)
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'dispatches': dispatches,
            'count': len(dispatches)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Total technicians
        cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."technicians";')
        total_technicians = cursor.fetchone()[0]
        
        # Available technicians
        cursor.execute("""
            SELECT COUNT(*) 
            FROM "team_core_flux"."technicians"
            WHERE "Current_assignments" < "Workload_capacity";
        """)
        available_technicians = cursor.fetchone()[0]
        
        # Total dispatches
        cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."current_dispatches";')
        total_dispatches = cursor.fetchone()[0]
        
        # Optimized dispatches
        cursor.execute("""
            SELECT COUNT(*) 
            FROM "team_core_flux"."current_dispatches"
            WHERE "Optimization_status" = 'completed';
        """)
        optimized_dispatches = cursor.fetchone()[0]
        
        # Pending dispatches
        cursor.execute("""
            SELECT COUNT(*) 
            FROM "team_core_flux"."current_dispatches"
            WHERE "Optimization_status" = 'pending';
        """)
        pending_dispatches = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        return jsonify({
            'success': True,
            'stats': {
                'total_technicians': total_technicians,
                'available_technicians': available_technicians,
                'total_dispatches': total_dispatches,
                'optimized_dispatches': optimized_dispatches,
                'pending_dispatches': pending_dispatches
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Technician Dashboard Server Starting...")
    print("=" * 60)
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

