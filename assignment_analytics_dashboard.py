"""
Assignment Analytics Dashboard
Shows assignment patterns: priority distribution, skill matching, technician workload
"""

from flask import Flask, jsonify, render_template_string
import psycopg2
from collections import defaultdict

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
    """Analytics dashboard"""
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <title>Assignment Analytics Dashboard</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { font-family: Arial; margin: 20px; background: #f5f5f5; }
        .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
        .card { background: white; padding: 20px; margin: 20px 0; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }
        .stat-box { background: white; padding: 15px; border-radius: 8px; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .stat-number { font-size: 2em; font-weight: bold; color: #667eea; }
        .stat-label { color: #666; font-size: 0.9em; }
        button { padding: 10px 20px; background: #667eea; color: white; border: none; border-radius: 5px; cursor: pointer; margin: 10px 5px; }
        button:hover { background: #5568d3; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #667eea; color: white; }
        tr:hover { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="header">
        <h1>📊 Assignment Analytics Dashboard</h1>
        <p>Smart Dispatch Agent - Assignment Patterns & Statistics</p>
        <button onclick="loadData()">🔄 Refresh Data</button>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-number" id="totalDispatches">-</div>
            <div class="stat-label">Total Dispatches</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="completedDispatches">-</div>
            <div class="stat-label">Completed</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="pendingDispatches">-</div>
            <div class="stat-label">Pending</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="uniqueTechnicians">-</div>
            <div class="stat-label">Assigned Technicians</div>
        </div>
    </div>

    <div class="stats-grid">
        <div class="stat-box">
            <div class="stat-number" id="avgRoutingMinutes">-</div>
            <div class="stat-label">Avg Routing (min)</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="avgEtcMinutes">-</div>
            <div class="stat-label">Avg Completion (min)</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="avgOperationalCost">-</div>
            <div class="stat-label">Avg Cost ($)</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="slaCompliance">-</div>
            <div class="stat-label">SLA Compliance (%)</div>
        </div>
        <div class="stat-box">
            <div class="stat-number" id="firstTimeFix">-</div>
            <div class="stat-label">First Time Fix (%)</div>
        </div>
    </div>

    <div class="card">
        <h2>📈 Status Distribution</h2>
        <canvas id="statusChart"></canvas>
    </div>

    <div class="card">
        <h2>🎯 Priority Distribution</h2>
        <canvas id="priorityChart"></canvas>
    </div>

    <div class="card">
        <h2>🔧 Skill Distribution</h2>
        <canvas id="skillChart"></canvas>
    </div>

    <div class="card">
        <h2>⚡ Routing vs Completion Trend</h2>
        <canvas id="routingTrendChart"></canvas>
    </div>

    <div class="card">
        <h2>💰 Operational Cost by Priority</h2>
        <canvas id="costChart"></canvas>
    </div>

    <div class="card">
        <h2>👥 Technician Assignment Summary</h2>
        <div id="technicianTable"></div>
    </div>

    <div class="card">
        <h2>📋 Priority by Status</h2>
        <div id="priorityStatusTable"></div>
    </div>

    <script>
        let statusChart, priorityChart, skillChart, routingTrendChart, costChart;

        async function loadData() {
            try {
                const [summary, priority, skill, technicians, priorityStatus, metrics] = await Promise.all([
                    fetch('/api/summary').then(r => r.json()),
                    fetch('/api/priority').then(r => r.json()),
                    fetch('/api/skill').then(r => r.json()),
                    fetch('/api/technicians').then(r => r.json()),
                    fetch('/api/priority-status').then(r => r.json()),
                    fetch('/api/metrics').then(r => r.json())
                ]);

                // Update stats
                document.getElementById('totalDispatches').textContent = summary.total || 0;
                document.getElementById('completedDispatches').textContent = summary.completed || 0;
                document.getElementById('pendingDispatches').textContent = summary.pending || 0;
                document.getElementById('uniqueTechnicians').textContent = summary.unique_technicians || 0;

                if (metrics.summary) {
                    document.getElementById('avgRoutingMinutes').textContent = metrics.summary.avg_routing_minutes.toFixed(1);
                    document.getElementById('avgEtcMinutes').textContent = metrics.summary.avg_etc_minutes.toFixed(1);
                    document.getElementById('avgOperationalCost').textContent = metrics.summary.avg_cost.toFixed(2);
                    document.getElementById('slaCompliance').textContent = metrics.summary.sla_compliance_pct.toFixed(1);
                    document.getElementById('firstTimeFix').textContent = metrics.summary.first_time_fix_rate.toFixed(1);
                }

                // Status Chart
                if (statusChart) statusChart.destroy();
                statusChart = new Chart(document.getElementById('statusChart'), {
                    type: 'doughnut',
                    data: {
                        labels: ['Completed', 'Pending'],
                        datasets: [{
                            data: [summary.completed || 0, summary.pending || 0],
                            backgroundColor: ['#28a745', '#ffc107']
                        }]
                    }
                });

                // Priority Chart
                if (priorityChart) priorityChart.destroy();
                const priorityData = priority.reduce((acc, p) => {
                    acc.labels.push(p.priority || 'Unknown');
                    acc.completed.push(p.completed || 0);
                    acc.pending.push(p.pending || 0);
                    return acc;
                }, {labels: [], completed: [], pending: []});

                priorityChart = new Chart(document.getElementById('priorityChart'), {
                    type: 'bar',
                    data: {
                        labels: priorityData.labels,
                        datasets: [
                            {
                                label: 'Completed',
                                data: priorityData.completed,
                                backgroundColor: '#28a745'
                            },
                            {
                                label: 'Pending',
                                data: priorityData.pending,
                                backgroundColor: '#ffc107'
                            }
                        ]
                    },
                    options: {
                        scales: { y: { beginAtZero: true } }
                    }
                });

                // Skill Chart
                if (skillChart) skillChart.destroy();
                const skillData = skill.slice(0, 10).reduce((acc, s) => {
                    acc.labels.push((s.skill || 'Unknown').substring(0, 30));
                    acc.completed.push(s.completed || 0);
                    acc.pending.push(s.pending || 0);
                    return acc;
                }, {labels: [], completed: [], pending: []});

                skillChart = new Chart(document.getElementById('skillChart'), {
                    type: 'bar',
                    data: {
                        labels: skillData.labels,
                        datasets: [
                            {
                                label: 'Completed',
                                data: skillData.completed,
                                backgroundColor: '#17a2b8'
                            },
                            {
                                label: 'Pending',
                                data: skillData.pending,
                                backgroundColor: '#ffc107'
                            }
                        ]
                    },
                    options: {
                        scales: { y: { beginAtZero: true } }
                    }
                });

                // Technician Table
                let techHtml = '<table><tr><th>Technician ID</th><th>Name</th><th>Primary Skill</th><th>Total</th><th>Critical</th><th>High</th><th>Normal</th><th>Low</th><th>Avg Confidence</th></tr>';
                technicians.forEach(t => {
                    techHtml += `<tr>
                        <td>${t.technician_id || 'N/A'}</td>
                        <td>${t.name || 'N/A'}</td>
                        <td>${t.primary_skill || 'N/A'}</td>
                        <td>${t.total || 0}</td>
                        <td>${t.critical || 0}</td>
                        <td>${t.high || 0}</td>
                        <td>${t.normal || 0}</td>
                        <td>${t.low || 0}</td>
                        <td>${(t.avg_confidence || 0).toFixed(2)}</td>
                    </tr>`;
                });
                techHtml += '</table>';
                document.getElementById('technicianTable').innerHTML = techHtml;

                // Priority Status Table
                let psHtml = '<table><tr><th>Priority</th><th>Status</th><th>Count</th><th>Unique Technicians</th><th>Unique Skills</th></tr>';
                priorityStatus.forEach(p => {
                    psHtml += `<tr>
                        <td>${p.priority || 'N/A'}</td>
                        <td>${p.status || 'N/A'}</td>
                        <td>${p.count || 0}</td>
                        <td>${p.unique_technicians || 0}</td>
                        <td>${p.unique_skills || 0}</td>
                    </tr>`;
                });
                psHtml += '</table>';
                document.getElementById('priorityStatusTable').innerHTML = psHtml;

                // Routing Trend Chart
                if (routingTrendChart) routingTrendChart.destroy();
                const trendLabels = metrics.trend.map(t => t.day);
                const routingData = metrics.trend.map(t => t.avg_routing_minutes);
                const etcData = metrics.trend.map(t => t.avg_etc_minutes);
                routingTrendChart = new Chart(document.getElementById('routingTrendChart'), {
                    type: 'line',
                    data: {
                        labels: trendLabels,
                        datasets: [
                            {
                                label: 'Avg Routing (min)',
                                data: routingData,
                                borderColor: '#ff6384',
                                tension: 0.3
                            },
                            {
                                label: 'Avg Completion (min)',
                                data: etcData,
                                borderColor: '#36a2eb',
                                tension: 0.3
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        scales: { y: { beginAtZero: true } }
                    }
                });

                // Cost Chart
                if (costChart) costChart.destroy();
                const costLabels = metrics.cost_by_priority.map(c => c.priority);
                const costValues = metrics.cost_by_priority.map(c => c.avg_cost);
                costChart = new Chart(document.getElementById('costChart'), {
                    type: 'bar',
                    data: {
                        labels: costLabels,
                        datasets: [{
                            label: 'Avg Cost ($)',
                            data: costValues,
                            backgroundColor: '#ffa600'
                        }]
                    },
                    options: {
                        scales: { y: { beginAtZero: true } }
                    }
                });

            } catch (error) {
                console.error('Error loading data:', error);
                alert('Error loading data: ' + error.message);
            }
        }

        window.onload = loadData;
    </script>
</body>
</html>
    ''')

@app.route('/api/summary')
def get_summary():
    """Get overall summary statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            COUNT(*) as total,
            COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END) as completed,
            COUNT(CASE WHEN "Optimization_status" = 'pending' THEN 1 END) as pending,
            COUNT(DISTINCT "Optimized_technician_id") as unique_technicians
        FROM "team_core_flux"."current_dispatches";
    """)
    
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    
    return jsonify({
        'total': row[0],
        'completed': row[1],
        'pending': row[2],
        'unique_technicians': row[3]
    })

@app.route('/api/priority')
def get_priority_stats():
    """Get statistics by priority"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            "Priority",
            COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END) as completed,
            COUNT(CASE WHEN "Optimization_status" = 'pending' THEN 1 END) as pending
        FROM "team_core_flux"."current_dispatches"
        WHERE "Priority" IS NOT NULL
        GROUP BY "Priority"
        ORDER BY 
            CASE "Priority"
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Normal' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END;
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'priority': row[0],
            'completed': row[1],
            'pending': row[2]
        })
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/skill')
def get_skill_stats():
    """Get statistics by skill"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            "Required_skill" as skill,
            COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END) as completed,
            COUNT(CASE WHEN "Optimization_status" = 'pending' THEN 1 END) as pending
        FROM "team_core_flux"."current_dispatches"
        WHERE "Required_skill" IS NOT NULL
        GROUP BY "Required_skill"
        ORDER BY completed DESC, pending DESC;
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'skill': row[0],
            'completed': row[1],
            'pending': row[2]
        })
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/technicians')
def get_technician_stats():
    """Get technician assignment statistics"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            t."Technician_id",
            t."Name",
            t."Primary_skill",
            COUNT(d."Dispatch_id") as total,
            COUNT(CASE WHEN d."Priority" = 'Critical' THEN 1 END) as critical,
            COUNT(CASE WHEN d."Priority" = 'High' THEN 1 END) as high,
            COUNT(CASE WHEN d."Priority" = 'Normal' THEN 1 END) as normal,
            COUNT(CASE WHEN d."Priority" = 'Low' THEN 1 END) as low,
            AVG(CAST(d."Optimization_confidence" AS FLOAT)) as avg_confidence
        FROM "team_core_flux"."technicians" t
        LEFT JOIN "team_core_flux"."current_dispatches" d
            ON t."Technician_id" = d."Optimized_technician_id"
            AND d."Optimization_status" = 'completed'
        GROUP BY t."Technician_id", t."Name", t."Primary_skill"
        HAVING COUNT(d."Dispatch_id") > 0
        ORDER BY total DESC;
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'technician_id': row[0],
            'name': row[1],
            'primary_skill': row[2],
            'total': row[3],
            'critical': row[4],
            'high': row[5],
            'normal': row[6],
            'low': row[7],
            'avg_confidence': float(row[8]) if row[8] else 0.0
        })
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/priority-status')
def get_priority_status():
    """Get priority by status breakdown"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT 
            "Priority",
            "Optimization_status" as status,
            COUNT(*) as count,
            COUNT(DISTINCT "Optimized_technician_id") as unique_technicians,
            COUNT(DISTINCT "Required_skill") as unique_skills
        FROM "team_core_flux"."current_dispatches"
        WHERE "Priority" IS NOT NULL
        GROUP BY "Priority", "Optimization_status"
        ORDER BY 
            CASE "Priority"
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Normal' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END,
            "Optimization_status";
    """)
    
    results = []
    for row in cursor.fetchall():
        results.append({
            'priority': row[0],
            'status': row[1],
            'count': row[2],
            'unique_technicians': row[3],
            'unique_skills': row[4]
        })
    
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/api/metrics')
def get_metrics():
    """Return advanced metrics such as routing trend and costs"""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            COALESCE(AVG(routing_seconds) / 60.0, 0) as avg_routing_minutes,
            COALESCE(AVG(estimated_completion_minutes), 0) as avg_etc_minutes,
            COALESCE(AVG(operational_cost), 0) as avg_cost,
            COALESCE(SUM(CASE WHEN sla_breached THEN 1 ELSE 0 END), 0) as sla_breaches,
            COUNT(*) as total_records
        FROM "team_core_flux"."dispatch_metrics";
    """)
    summary_row = cursor.fetchone()
    total_records = summary_row[4] or 0
    sla_breaches = summary_row[3] or 0
    sla_compliance = 0.0
    if total_records > 0:
        sla_compliance = round(100 - (sla_breaches / total_records) * 100, 1)

    cursor.execute("""
        SELECT 
            DATE(updated_at) as day,
            COALESCE(AVG(routing_seconds) / 60.0, 0) as avg_routing_minutes,
            COALESCE(AVG(estimated_completion_minutes), 0) as avg_etc_minutes
        FROM "team_core_flux"."dispatch_metrics"
        GROUP BY DATE(updated_at)
        ORDER BY DATE(updated_at)
        LIMIT 30;
    """)
    trend = [
        {
            'day': row[0].isoformat(),
            'avg_routing_minutes': round(row[1], 2),
            'avg_etc_minutes': round(row[2], 2)
        }
        for row in cursor.fetchall()
    ]

    cursor.execute("""
        SELECT 
            d."Priority",
            COALESCE(AVG(dm.operational_cost), 0) as avg_cost,
            COUNT(*) as count
        FROM "team_core_flux"."dispatch_metrics" dm
        JOIN "team_core_flux"."current_dispatches" d
            ON dm.dispatch_id = d."Dispatch_id"
        GROUP BY d."Priority"
        ORDER BY avg_cost DESC;
    """)
    cost_by_priority = [
        {
            'priority': row[0] or 'Unknown',
            'avg_cost': float(row[1] or 0),
            'count': row[2] or 0
        }
        for row in cursor.fetchall()
    ]

    cursor.execute("""
        SELECT 
            AVG(CASE WHEN "First_time_fix" = 1 THEN 1 ELSE 0 END) as ftf_rate
        FROM "team_core_flux"."dispatch_history"
        WHERE "Status" = 'Completed';
    """)
    ftf = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()

    return jsonify({
        'summary': {
            'avg_routing_minutes': round(summary_row[0], 2),
            'avg_etc_minutes': round(summary_row[1], 2),
            'avg_cost': round(summary_row[2], 2),
            'sla_compliance_pct': sla_compliance,
            'first_time_fix_rate': round(ftf * 100, 1)
        },
        'trend': trend,
        'cost_by_priority': cost_by_priority
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Assignment Analytics Dashboard")
    print("=" * 60)
    print("Open: http://127.0.0.1:5004")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5004)

