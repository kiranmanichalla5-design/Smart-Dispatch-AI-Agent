"""
Automated Scheduler for Smart Dispatch System
Runs periodic tasks: dispatch agent, alert monitoring, reporting
"""

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import subprocess
import sys
import psycopg2
from psycopg2.extras import RealDictCursor
from alert_config import SCHEDULE_CONFIG
from alert_monitor import run_alert_check
from notification_handler import send_alert, send_summary


# Database connection parameters
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'options': '-c search_path=team_core_flux'
}


class DispatchScheduler:
    """Manages automated scheduling for dispatch system"""
    
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.setup_jobs()
    
    def setup_jobs(self):
        """Set up all scheduled jobs"""
        
        # Alert monitoring (every X minutes)
        alert_interval = SCHEDULE_CONFIG['alert_check_interval']
        self.scheduler.add_job(
            self.run_alert_checks,
            'interval',
            minutes=alert_interval,
            id='alert_monitor',
            name='Alert Monitoring',
            next_run_time=datetime.now()  # Run immediately on start
        )
        
        # Dispatch agent (every X minutes)
        dispatch_interval = SCHEDULE_CONFIG['dispatch_run_interval']
        self.scheduler.add_job(
            self.run_dispatch_agent,
            'interval',
            minutes=dispatch_interval,
            id='dispatch_agent',
            name='Dispatch Agent'
        )
        
        # Daily summary report
        daily_time = SCHEDULE_CONFIG['daily_summary_time']
        hour, minute = map(int, daily_time.split(':'))
        self.scheduler.add_job(
            self.generate_daily_summary,
            CronTrigger(hour=hour, minute=minute),
            id='daily_summary',
            name='Daily Summary Report'
        )
        
        # Weekly summary report
        weekly_day = SCHEDULE_CONFIG['weekly_report_day']
        weekly_time = SCHEDULE_CONFIG['weekly_report_time']
        w_hour, w_minute = map(int, weekly_time.split(':'))
        self.scheduler.add_job(
            self.generate_weekly_summary,
            CronTrigger(day_of_week=weekly_day, hour=w_hour, minute=w_minute),
            id='weekly_summary',
            name='Weekly Summary Report'
        )
        
        print("\n" + "="*60)
        print("📅 SMART DISPATCH SCHEDULER CONFIGURED")
        print("="*60)
        print(f"✅ Alert monitoring: Every {alert_interval} minutes")
        print(f"✅ Dispatch agent: Every {dispatch_interval} minutes")
        print(f"✅ Daily summary: {daily_time} every day")
        print(f"✅ Weekly summary: {weekly_time} every {'Monday' if weekly_day==0 else 'Sunday'}")
        print("="*60 + "\n")
    
    def run_alert_checks(self):
        """Run alert monitoring checks"""
        try:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Running scheduled alert checks...")
            run_alert_check()
        except Exception as e:
            print(f"❌ Alert check failed: {e}")
            send_alert(
                'WARNING',
                'System Error',
                'Alert monitoring job failed',
                str(e)
            )
    
    def run_dispatch_agent(self):
        """Run the dispatch agent to process pending dispatches"""
        try:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Running dispatch agent...")
            
            # Run the enhanced dispatch agent
            result = subprocess.run(
                [sys.executable, 'enhanced_dispatch_agent.py'],
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                print("✅ Dispatch agent completed successfully")
                
                # Check if any dispatches were processed
                if "Assigned" in result.stdout:
                    send_alert(
                        'SUCCESS',
                        'Dispatch Agent',
                        'Automated dispatch run completed',
                        'Pending dispatches have been processed'
                    )
            else:
                print(f"⚠️ Dispatch agent returned error: {result.stderr}")
                send_alert(
                    'WARNING',
                    'Dispatch Agent',
                    'Dispatch agent encountered issues',
                    result.stderr[:200]
                )
        
        except subprocess.TimeoutExpired:
            print("❌ Dispatch agent timed out")
            send_alert(
                'CRITICAL',
                'System Error',
                'Dispatch agent timed out',
                'Process took longer than 5 minutes'
            )
        
        except Exception as e:
            print(f"❌ Dispatch agent failed: {e}")
            send_alert(
                'CRITICAL',
                'System Error',
                'Dispatch agent failed to run',
                str(e)
            )
    
    def generate_daily_summary(self):
        """Generate and send daily summary report"""
        try:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Generating daily summary...")
            
            summary_data = self.get_summary_data('24 hours')
            summary_data['period'] = 'Last 24 hours'
            
            send_summary(summary_data)
            print("✅ Daily summary sent")
        
        except Exception as e:
            print(f"❌ Daily summary failed: {e}")
            send_alert(
                'WARNING',
                'System Error',
                'Daily summary generation failed',
                str(e)
            )
    
    def generate_weekly_summary(self):
        """Generate and send weekly summary report"""
        try:
            print(f"\n⏰ [{datetime.now().strftime('%H:%M:%S')}] Generating weekly summary...")
            
            summary_data = self.get_summary_data('7 days')
            summary_data['period'] = 'Last 7 days'
            
            send_summary(summary_data)
            print("✅ Weekly summary sent")
        
        except Exception as e:
            print(f"❌ Weekly summary failed: {e}")
            send_alert(
                'WARNING',
                'System Error',
                'Weekly summary generation failed',
                str(e)
            )
    
    def get_summary_data(self, period):
        """Get summary data for reporting"""
        conn = None
        try:
            conn = psycopg2.connect(**DB_CONFIG)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Overall dispatch stats
            cursor.execute(f"""
                SELECT 
                    COUNT(*) as total_dispatches,
                    SUM(CASE WHEN status = 'Pending' THEN 1 ELSE 0 END) as pending,
                    SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) as completed
                FROM current_dispatches
                WHERE created_at >= NOW() - INTERVAL '{period}'
            """)
            dispatch_stats = cursor.fetchone()
            
            # Metrics
            cursor.execute(f"""
                SELECT 
                    AVG(routing_speed_seconds) as avg_routing_time,
                    AVG(estimated_completion_hours) as avg_etc,
                    AVG(operational_cost) as avg_cost,
                    ROUND(
                        (SUM(CASE WHEN sla_met = true THEN 1 ELSE 0 END)::float / 
                        NULLIF(COUNT(*), 0) * 100)::numeric,
                        1
                    ) as sla_compliance,
                    SUM(CASE WHEN burnout_alert = true THEN 1 ELSE 0 END) as burnout_alerts
                FROM dispatch_metrics
                WHERE created_at >= NOW() - INTERVAL '{period}'
            """)
            metrics = cursor.fetchone()
            
            # Technician stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_techs,
                    SUM(CASE WHEN availability_status = 'Available' THEN 1 ELSE 0 END) as techs_available,
                    SUM(CASE WHEN availability_status = 'Busy' THEN 1 ELSE 0 END) as techs_busy,
                    AVG(utilization_percentage) as avg_utilization
                FROM technicians
            """)
            tech_stats = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            return {
                'total_dispatches': int(dispatch_stats['total_dispatches'] or 0),
                'pending': int(dispatch_stats['pending'] or 0),
                'completed': int(dispatch_stats['completed'] or 0),
                'avg_routing_time': float(metrics['avg_routing_time'] or 0),
                'avg_etc': float(metrics['avg_etc'] or 0),
                'avg_cost': float(metrics['avg_cost'] or 0),
                'sla_compliance': float(metrics['sla_compliance'] or 0),
                'burnout_alerts': int(metrics['burnout_alerts'] or 0),
                'total_techs': int(tech_stats['total_techs'] or 0),
                'techs_available': int(tech_stats['techs_available'] or 0),
                'techs_busy': int(tech_stats['techs_busy'] or 0),
                'avg_utilization': float(tech_stats['avg_utilization'] or 0),
            }
        
        except Exception as e:
            print(f"❌ Failed to get summary data: {e}")
            return {}
        
        finally:
            if conn:
                conn.close()
    
    def start(self):
        """Start the scheduler"""
        print("\n" + "="*60)
        print("🚀 STARTING SMART DISPATCH SCHEDULER")
        print("="*60)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        send_alert(
            'INFO',
            'System Status',
            'Smart Dispatch Scheduler started',
            f"Automated monitoring and dispatch processing is now active"
        )
        
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            print("\n" + "="*60)
            print("🛑 SCHEDULER STOPPED")
            print("="*60)
            print(f"Stopped at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            print("="*60 + "\n")
            
            send_alert(
                'INFO',
                'System Status',
                'Smart Dispatch Scheduler stopped',
                'Automated monitoring has been terminated'
            )


def main():
    """Main entry point"""
    scheduler = DispatchScheduler()
    scheduler.start()


if __name__ == "__main__":
    main()


