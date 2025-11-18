"""
Alert Monitor for Smart Dispatch System
Monitors metrics and triggers alerts based on thresholds
"""

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta
from notification_handler import send_alert
from alert_config import ALERT_THRESHOLDS


# Database connection parameters
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'options': '-c search_path=team_core_flux'
}


class AlertMonitor:
    """Monitors dispatch metrics and triggers alerts"""
    
    def __init__(self):
        self.conn = None
    
    def connect(self):
        """Connect to database"""
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            return True
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from database"""
        if self.conn:
            self.conn.close()
    
    def check_all_alerts(self):
        """Run all alert checks"""
        if not self.connect():
            return
        
        try:
            print(f"\n🔍 Running alert checks at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            self.check_sla_compliance()
            self.check_routing_speed()
            self.check_etc_times()
            self.check_operational_costs()
            self.check_burnout_risks()
            self.check_first_time_fix()
            self.check_pending_dispatches()
            self.check_technician_utilization()
            
            print("✅ Alert check completed\n")
        
        except Exception as e:
            print(f"❌ Error during alert check: {e}")
        
        finally:
            self.disconnect()
    
    def check_sla_compliance(self):
        """Check SLA compliance percentage"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            # Get SLA compliance for last 24 hours
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN sla_met = true THEN 1 ELSE 0 END) as met_sla,
                    ROUND(
                        (SUM(CASE WHEN sla_met = true THEN 1 ELSE 0 END)::float / 
                        NULLIF(COUNT(*), 0) * 100)::numeric, 
                        1
                    ) as compliance_rate
                FROM dispatch_metrics
                WHERE created_at >= NOW() - INTERVAL '24 hours'
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['total'] > 0:
                compliance = float(result['compliance_rate'] or 0)
                
                if compliance < ALERT_THRESHOLDS['sla_compliance_critical']:
                    send_alert(
                        'CRITICAL',
                        'SLA Compliance',
                        f'SLA compliance critically low at {compliance}%',
                        f"Only {result['met_sla']} out of {result['total']} dispatches met SLA in last 24 hours",
                        f"{compliance}%"
                    )
                elif compliance < ALERT_THRESHOLDS['sla_compliance_warning']:
                    send_alert(
                        'WARNING',
                        'SLA Compliance',
                        f'SLA compliance below target at {compliance}%',
                        f"{result['met_sla']} out of {result['total']} dispatches met SLA",
                        f"{compliance}%"
                    )
        
        except Exception as e:
            print(f"⚠️ SLA check failed: {e}")
    
    def check_routing_speed(self):
        """Check average routing speed"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT AVG(routing_speed_seconds) as avg_speed
                FROM dispatch_metrics
                WHERE created_at >= NOW() - INTERVAL '1 hour'
                AND routing_speed_seconds IS NOT NULL
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['avg_speed']:
                avg_speed = float(result['avg_speed'])
                
                if avg_speed > ALERT_THRESHOLDS['routing_speed_critical']:
                    send_alert(
                        'CRITICAL',
                        'Routing Speed',
                        f'Routing taking too long: {avg_speed:.0f} seconds average',
                        'Dispatches are being routed slower than acceptable',
                        f"{avg_speed:.0f}s"
                    )
                elif avg_speed > ALERT_THRESHOLDS['routing_speed_warning']:
                    send_alert(
                        'WARNING',
                        'Routing Speed',
                        f'Routing speed degraded: {avg_speed:.0f} seconds average',
                        'Consider investigating system performance',
                        f"{avg_speed:.0f}s"
                    )
        
        except Exception as e:
            print(f"⚠️ Routing speed check failed: {e}")
    
    def check_etc_times(self):
        """Check estimated completion times"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT AVG(estimated_completion_hours) as avg_etc
                FROM dispatch_metrics
                WHERE created_at >= NOW() - INTERVAL '4 hours'
                AND estimated_completion_hours IS NOT NULL
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['avg_etc']:
                avg_etc = float(result['avg_etc'])
                
                if avg_etc > ALERT_THRESHOLDS['etc_critical']:
                    send_alert(
                        'CRITICAL',
                        'Completion Time',
                        f'Estimated completion times very high: {avg_etc:.1f} hours',
                        'Customer wait times may be excessive',
                        f"{avg_etc:.1f}h"
                    )
                elif avg_etc > ALERT_THRESHOLDS['etc_warning']:
                    send_alert(
                        'WARNING',
                        'Completion Time',
                        f'Estimated completion times elevated: {avg_etc:.1f} hours',
                        'Monitor technician availability',
                        f"{avg_etc:.1f}h"
                    )
        
        except Exception as e:
            print(f"⚠️ ETC check failed: {e}")
    
    def check_operational_costs(self):
        """Check operational costs"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT AVG(operational_cost) as avg_cost
                FROM dispatch_metrics
                WHERE created_at >= NOW() - INTERVAL '24 hours'
                AND operational_cost IS NOT NULL
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['avg_cost']:
                avg_cost = float(result['avg_cost'])
                
                if avg_cost > ALERT_THRESHOLDS['operational_cost_critical']:
                    send_alert(
                        'CRITICAL',
                        'Operational Cost',
                        f'Average dispatch cost critically high: ${avg_cost:.2f}',
                        'Review dispatch assignments and optimize routing',
                        f"${avg_cost:.2f}"
                    )
                elif avg_cost > ALERT_THRESHOLDS['operational_cost_warning']:
                    send_alert(
                        'WARNING',
                        'Operational Cost',
                        f'Average dispatch cost elevated: ${avg_cost:.2f}',
                        'Consider cost optimization strategies',
                        f"${avg_cost:.2f}"
                    )
        
        except Exception as e:
            print(f"⚠️ Cost check failed: {e}")
    
    def check_burnout_risks(self):
        """Check technician burnout risks"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT COUNT(DISTINCT technician_id) as high_burnout_count
                FROM dispatch_metrics
                WHERE created_at >= NOW() - INTERVAL '4 hours'
                AND burnout_alert = true
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result and result['high_burnout_count']:
                count = int(result['high_burnout_count'])
                
                if count >= ALERT_THRESHOLDS['burnout_high_count_critical']:
                    send_alert(
                        'CRITICAL',
                        'Technician Burnout',
                        f'{count} technicians at high burnout risk',
                        'Immediate intervention needed to prevent turnover',
                        f"{count} technicians"
                    )
                elif count >= ALERT_THRESHOLDS['burnout_high_count_warning']:
                    send_alert(
                        'WARNING',
                        'Technician Burnout',
                        f'{count} technicians showing burnout signs',
                        'Consider workload rebalancing',
                        f"{count} technicians"
                    )
        
        except Exception as e:
            print(f"⚠️ Burnout check failed: {e}")
    
    def check_first_time_fix(self):
        """Check first-time fix rates"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT 
                    t.technician_id,
                    t.name,
                    COUNT(*) as total_jobs,
                    SUM(CASE WHEN h.status = 'Completed' AND h.notes NOT LIKE '%callback%' 
                        THEN 1 ELSE 0 END) as first_time_fixes,
                    ROUND(
                        (SUM(CASE WHEN h.status = 'Completed' AND h.notes NOT LIKE '%callback%' 
                            THEN 1 ELSE 0 END)::float / NULLIF(COUNT(*), 0) * 100)::numeric,
                        1
                    ) as fix_rate
                FROM dispatch_history h
                JOIN technicians t ON h.technician_id = t.technician_id
                WHERE h.dispatch_date >= NOW() - INTERVAL '7 days'
                AND h.status = 'Completed'
                GROUP BY t.technician_id, t.name
                HAVING COUNT(*) >= 5
            """)
            
            results = cursor.fetchall()
            cursor.close()
            
            low_performers = []
            for row in results:
                fix_rate = float(row['fix_rate'] or 0)
                if fix_rate < ALERT_THRESHOLDS['first_time_fix_critical']:
                    low_performers.append(f"{row['name']} ({fix_rate}%)")
            
            if low_performers:
                send_alert(
                    'WARNING',
                    'First-Time Fix Rate',
                    f'{len(low_performers)} technician(s) with low first-time fix rates',
                    'Technicians need training or support: ' + ', '.join(low_performers[:3]),
                    f"{len(low_performers)} technicians"
                )
        
        except Exception as e:
            print(f"⚠️ First-time fix check failed: {e}")
    
    def check_pending_dispatches(self):
        """Check number of pending dispatches"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT COUNT(*) as pending_count
                FROM current_dispatches
                WHERE status = 'Pending'
            """)
            
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                pending = int(result['pending_count'] or 0)
                
                if pending >= ALERT_THRESHOLDS['pending_dispatches_critical']:
                    send_alert(
                        'CRITICAL',
                        'Pending Dispatches',
                        f'{pending} dispatches waiting for assignment',
                        'High backlog - consider emergency staffing',
                        f"{pending} dispatches"
                    )
                elif pending >= ALERT_THRESHOLDS['pending_dispatches_warning']:
                    send_alert(
                        'WARNING',
                        'Pending Dispatches',
                        f'{pending} dispatches in queue',
                        'Monitor situation and ensure adequate staffing',
                        f"{pending} dispatches"
                    )
        
        except Exception as e:
            print(f"⚠️ Pending dispatch check failed: {e}")
    
    def check_technician_utilization(self):
        """Check technician utilization rates"""
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute("""
                SELECT 
                    technician_id,
                    name,
                    utilization_percentage
                FROM technicians
                WHERE availability_status = 'Available'
            """)
            
            results = cursor.fetchall()
            cursor.close()
            
            underutilized = []
            overutilized = []
            
            for row in results:
                util = float(row['utilization_percentage'] or 0)
                
                if util < ALERT_THRESHOLDS['utilization_critical_low']:
                    underutilized.append(f"{row['name']} ({util:.0f}%)")
                elif util > ALERT_THRESHOLDS['utilization_critical_high']:
                    overutilized.append(f"{row['name']} ({util:.0f}%)")
            
            if overutilized:
                send_alert(
                    'CRITICAL',
                    'Resource Utilization',
                    f'{len(overutilized)} technician(s) critically overutilized',
                    'Risk of burnout and quality issues: ' + ', '.join(overutilized[:3]),
                    f"{len(overutilized)} technicians"
                )
            
            if underutilized and len(underutilized) >= 3:
                send_alert(
                    'WARNING',
                    'Resource Utilization',
                    f'{len(underutilized)} technician(s) underutilized',
                    'Inefficient resource allocation: ' + ', '.join(underutilized[:3]),
                    f"{len(underutilized)} technicians"
                )
        
        except Exception as e:
            print(f"⚠️ Utilization check failed: {e}")


def run_alert_check():
    """Convenience function to run alert checks"""
    monitor = AlertMonitor()
    monitor.check_all_alerts()


if __name__ == "__main__":
    # Run alert check
    run_alert_check()


