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


@app.route('/api/test')
def test_api():
    """Test API endpoint"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM "team_core_flux"."technicians";')
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'message': f'API working! Found {count} technicians',
            'technician_count': count
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


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
                CAST(
                    ROUND(
                        CAST(
                            (CASE 
                                WHEN t."Workload_capacity" > 0 
                                THEN (t."Current_assignments"::FLOAT / t."Workload_capacity") * 100
                                ELSE 0 
                            END) AS numeric
                        ), 
                        2
                    ) AS numeric
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
            tech_dict = dict(zip(columns, row))
            
            # Normalize all keys to match expected format (handle case sensitivity)
            tech = {}
            for key, value in tech_dict.items():
                # Convert to title case for consistency
                normalized_key = key.replace('_', ' ').title().replace(' ', '_')
                tech[normalized_key] = value
                tech[key] = value  # Keep original too
            
            # Get values with case-insensitive key access
            availability_status = (tech.get('Availability_Status') or 
                                 tech.get('availability_status') or 
                                 tech_dict.get('availability_status', 'Unknown'))
            critical_count = (tech.get('Critical_Count') or 
                            tech.get('critical_count') or 
                            tech_dict.get('critical_count') or 0)
            high_count = (tech.get('High_Count') or 
                        tech.get('high_count') or 
                        tech_dict.get('high_count') or 0)
            normal_count = (tech.get('Normal_Count') or 
                          tech.get('normal_count') or 
                          tech_dict.get('normal_count') or 0)
            low_count = (tech.get('Low_Count') or 
                       tech.get('low_count') or 
                       tech_dict.get('low_count') or 0)
            
            # Determine status color
            if availability_status == 'Available':
                tech['status_color'] = 'green'
                tech['status_badge'] = 'success'
            elif availability_status == 'Nearly Full':
                tech['status_color'] = 'orange'
                tech['status_badge'] = 'warning'
            elif availability_status == 'Fully Booked':
                tech['status_color'] = 'red'
                tech['status_badge'] = 'danger'
            else:
                tech['status_color'] = 'gray'
                tech['status_badge'] = 'secondary'
            
            # Calculate priority level
            total_priority = critical_count * 4 + \
                           high_count * 3 + \
                           normal_count * 2 + \
                           low_count * 1
            
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


@app.route('/api/dispatch-metrics')
def get_dispatch_metrics():
    """Return advanced metrics for routing, ETC, cost, and SLA"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if dispatch_metrics table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'team_core_flux' 
                AND table_name = 'dispatch_metrics'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            # Return empty metrics if table doesn't exist
            cursor.close()
            conn.close()
            return jsonify({
                'success': True,
                'summary': {
                    'avg_routing_minutes': 0,
                    'avg_etc_minutes': 0,
                    'avg_cost': 0,
                    'sla_compliance_pct': 0,
                    'burnout_alerts': 0,
                    'first_time_fix_rate': 0,
                    'ftf_by_priority': {}
                },
                'trend': [],
                'recent': [],
                'note': 'Run enhanced_dispatch_agent.py to populate metrics'
            })

        cursor.execute("""
            SELECT 
                COALESCE(AVG(ABS(routing_seconds)), 0) as avg_routing,
                COALESCE(AVG(estimated_completion_minutes), 0) as avg_etc,
                COALESCE(AVG(operational_cost), 0) as avg_cost,
                COALESCE(SUM(CASE WHEN sla_breached THEN 1 ELSE 0 END), 0) as sla_breaches,
                COUNT(*) as total_records,
                COALESCE(SUM(CASE WHEN burnout_risk THEN 1 ELSE 0 END), 0) as burnout_alerts
            FROM "team_core_flux"."dispatch_metrics";
        """)
        avg_row = cursor.fetchone()

        cursor.execute("""
            SELECT 
                DATE(updated_at) as day,
                COALESCE(AVG(ABS(routing_seconds)) / 60.0, 0) as avg_routing_minutes,
                COALESCE(AVG(estimated_completion_minutes), 0) as avg_etc_minutes
            FROM "team_core_flux"."dispatch_metrics"
            GROUP BY DATE(updated_at)
            ORDER BY DATE(updated_at) ASC
            LIMIT 14;
        """)
        trend_rows = cursor.fetchall()
        trend = [
            {
                'day': row[0].isoformat(),
                'avg_routing_minutes': round(float(row[1] or 0), 2),
                'avg_etc_minutes': round(float(row[2] or 0), 2)
            }
            for row in trend_rows
        ]

        cursor.execute("""
            SELECT 
                dh."Priority",
                AVG(CASE WHEN dh."First_time_fix" = 1 THEN 1 ELSE 0 END) as ftf_rate
            FROM "team_core_flux"."dispatch_history" dh
            WHERE dh."Status" = 'Completed'
            GROUP BY dh."Priority";
        """)
        ftf_rows = cursor.fetchall()
        ftf_map = {row[0] or 'Unknown': round((row[1] or 0) * 100, 1) for row in ftf_rows}
        overall_ftf = round((sum((row[1] or 0) for row in ftf_rows) / len(ftf_rows)) * 100, 1) if ftf_rows else 0.0

        cursor.execute("""
            SELECT 
                dm.dispatch_id,
                dm.routing_seconds,
                dm.estimated_completion_minutes,
                dm.operational_cost,
                dm.sla_breached,
                dm.fallback_technicians,
                dm.burnout_risk,
                d."Priority",
                d."Required_skill",
                d."City",
                d."State",
                d."Optimized_technician_id"
            FROM "team_core_flux"."dispatch_metrics" dm
            JOIN "team_core_flux"."current_dispatches" d
                ON dm.dispatch_id = d."Dispatch_id"
            ORDER BY dm.updated_at DESC
            LIMIT 25;
        """)
        recent = []
        for row in cursor.fetchall():
            fallback = []
            try:
                # Handle fallback_technicians - it might be a string, list, or None
                if row[5]:
                    if isinstance(row[5], str):
                        fallback = json.loads(row[5])
                    elif isinstance(row[5], list):
                        fallback = row[5]
                    else:
                        fallback = []
            except (json.JSONDecodeError, TypeError):
                fallback = []
            
            recent.append({
                'dispatch_id': row[0],
                'routing_seconds': row[1] or 0,
                'etc_minutes': row[2] or 0,
                'operational_cost': float(row[3] or 0),
                'sla_breached': bool(row[4]),
                'fallback': fallback,
                'burnout_risk': bool(row[6]),
                'priority': row[7] or 'N/A',
                'required_skill': row[8] or 'N/A',
                'city': row[9] or 'N/A',
                'state': row[10] or 'N/A',
                'technician_id': row[11] or 'N/A'
            })

        cursor.close()
        conn.close()

        total_records = int(avg_row[4] or 0)
        sla_compliance = 0.0
        if total_records > 0:
            sla_compliance = round(100 - ((float(avg_row[3] or 0) / total_records) * 100), 1)

        return jsonify({
            'success': True,
            'summary': {
                'avg_routing_minutes': round(float(avg_row[0] or 0) / 60.0, 2),
                'avg_etc_minutes': round(float(avg_row[1] or 0), 2),
                'avg_cost': round(float(avg_row[2] or 0), 2),
                'sla_compliance_pct': sla_compliance,
                'burnout_alerts': int(avg_row[5] or 0),
                'first_time_fix_rate': overall_ftf,
                'ftf_by_priority': ftf_map
            },
            'trend': trend,
            'recent': recent
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Technician Dashboard Server Starting...")
    print("=" * 60)
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)

