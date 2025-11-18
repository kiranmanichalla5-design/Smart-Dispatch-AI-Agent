"""
Quick Start Script for Smart Dispatch Scheduler
Sets up and starts the scheduler with guided configuration
"""

import os
import sys
from datetime import datetime


def print_header(title):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def check_dependencies():
    """Check if required packages are installed"""
    print_header("Checking Dependencies")
    
    required_packages = [
        ('psycopg2', 'Database connectivity'),
        ('apscheduler', 'Task scheduling'),
        ('requests', 'Webhook notifications'),
    ]
    
    missing = []
    for package, description in required_packages:
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - {description} (MISSING)")
            missing.append(package)
    
    if missing:
        print("\n⚠️ Missing packages detected!")
        print("Run: pip install -r requirements_dispatch.txt")
        return False
    
    print("\n✅ All dependencies installed")
    return True


def check_database_connection():
    """Test database connection"""
    print_header("Testing Database Connection")
    
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host='212.2.245.85',
            port=6432,
            database='postgres',
            user='postgres',
            password='Tea_IWMZ5wuUta97gupb',
            options='-c search_path=team_core_flux'
        )
        conn.close()
        
        print("✅ Database connection successful")
        return True
    
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def check_required_tables():
    """Check if required database tables exist"""
    print_header("Checking Database Tables")
    
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        conn = psycopg2.connect(
            host='212.2.245.85',
            port=6432,
            database='postgres',
            user='postgres',
            password='Tea_IWMZ5wuUta97gupb',
            options='-c search_path=team_core_flux'
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        required_tables = [
            'technicians',
            'current_dispatches',
            'dispatch_history',
            'dispatch_metrics'
        ]
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'team_core_flux'
        """)
        
        existing_tables = [row['table_name'] for row in cursor.fetchall()]
        
        all_exist = True
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ {table}")
            else:
                print(f"❌ {table} (MISSING)")
                all_exist = False
        
        cursor.close()
        conn.close()
        
        if not all_exist:
            print("\n⚠️ Some required tables are missing!")
            print("Run: python enhanced_dispatch_agent.py (to create dispatch_metrics)")
            return False
        
        print("\n✅ All required tables exist")
        return True
    
    except Exception as e:
        print(f"❌ Table check failed: {e}")
        return False


def check_configuration():
    """Check if configuration files exist"""
    print_header("Checking Configuration")
    
    config_files = [
        ('alert_config.py', 'Alert thresholds and settings'),
        ('notification_handler.py', 'Notification channels'),
        ('alert_monitor.py', 'Alert monitoring logic'),
        ('scheduler.py', 'Task scheduler'),
    ]
    
    all_exist = True
    for filename, description in config_files:
        if os.path.exists(filename):
            print(f"✅ {filename:25} - {description}")
        else:
            print(f"❌ {filename:25} - {description} (MISSING)")
            all_exist = False
    
    if not all_exist:
        print("\n⚠️ Some configuration files are missing!")
        return False
    
    print("\n✅ All configuration files present")
    return True


def show_configuration_summary():
    """Show current configuration"""
    print_header("Current Configuration")
    
    try:
        from alert_config import SCHEDULE_CONFIG, NOTIFICATION_CHANNELS, ALERT_THRESHOLDS
        
        print("\n📅 SCHEDULE:")
        print(f"   Alert checks: Every {SCHEDULE_CONFIG['alert_check_interval']} minutes")
        print(f"   Dispatch runs: Every {SCHEDULE_CONFIG['dispatch_run_interval']} minutes")
        print(f"   Daily summary: {SCHEDULE_CONFIG['daily_summary_time']}")
        print(f"   Weekly summary: {SCHEDULE_CONFIG['weekly_report_time']} on Monday")
        
        print("\n📢 NOTIFICATION CHANNELS:")
        for channel, enabled in NOTIFICATION_CHANNELS.items():
            status = "✅ Enabled" if enabled else "⚪ Disabled"
            print(f"   {channel:10} {status}")
        
        print("\n⚠️ KEY ALERT THRESHOLDS:")
        print(f"   SLA Compliance: < {ALERT_THRESHOLDS['sla_compliance_critical']}% (critical)")
        print(f"   Routing Speed: > {ALERT_THRESHOLDS['routing_speed_critical']}s (critical)")
        print(f"   ETC: > {ALERT_THRESHOLDS['etc_critical']}h (critical)")
        print(f"   Operational Cost: > ${ALERT_THRESHOLDS['operational_cost_critical']} (critical)")
        
        print("\n💡 To customize: Edit alert_config.py")
        return True
    
    except Exception as e:
        print(f"❌ Could not load configuration: {e}")
        return False


def run_initial_alert_check():
    """Run initial alert check to test system"""
    print_header("Running Initial Alert Check")
    
    try:
        from alert_monitor import run_alert_check
        
        print("Testing alert monitoring system...\n")
        run_alert_check()
        
        print("\n✅ Alert check completed successfully")
        print("📁 Check alerts.log for any alerts generated")
        return True
    
    except Exception as e:
        print(f"❌ Alert check failed: {e}")
        return False


def start_scheduler():
    """Start the scheduler"""
    print_header("Starting Scheduler")
    
    print("\n🚀 The scheduler will now start with the following tasks:")
    print("   • Alert monitoring (every 5 minutes)")
    print("   • Dispatch processing (every 10 minutes)")
    print("   • Daily summary reports (8:00 AM)")
    print("   • Weekly summary reports (Monday 9:00 AM)")
    print("\n📝 All alerts will be logged to: alerts.log")
    print("📊 Alert history saved to: alert_history.json")
    print("\n🛑 Press Ctrl+C to stop the scheduler")
    print("\nStarting in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        from scheduler import main
        main()
    
    except KeyboardInterrupt:
        print("\n\n✅ Scheduler stopped by user")
    
    except Exception as e:
        print(f"\n\n❌ Scheduler error: {e}")


def main():
    """Main setup and start routine"""
    print("\n" + "="*60)
    print("  🤖 SMART DISPATCH SCHEDULER - QUICK START")
    print("="*60)
    print(f"  {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed: Install missing dependencies first")
        print("Run: pip install -r requirements_dispatch.txt")
        sys.exit(1)
    
    # Step 2: Check database connection
    if not check_database_connection():
        print("\n❌ Setup failed: Cannot connect to database")
        sys.exit(1)
    
    # Step 3: Check required tables
    if not check_required_tables():
        print("\n❌ Setup failed: Required tables missing")
        sys.exit(1)
    
    # Step 4: Check configuration files
    if not check_configuration():
        print("\n❌ Setup failed: Configuration files missing")
        sys.exit(1)
    
    # Step 5: Show configuration summary
    if not show_configuration_summary():
        print("\n⚠️ Warning: Could not load configuration")
    
    # Step 6: Run initial alert check
    if not run_initial_alert_check():
        print("\n⚠️ Warning: Initial alert check failed")
        response = input("\nContinue anyway? (y/n): ")
        if response.lower() != 'y':
            sys.exit(1)
    
    # Step 7: Confirm start
    print_header("Ready to Start")
    print("\n✅ All pre-flight checks passed!")
    print("\nThe scheduler will run continuously and:")
    print("  • Monitor metrics and send alerts")
    print("  • Automatically process pending dispatches")
    print("  • Generate daily and weekly reports")
    
    response = input("\n🚀 Start the scheduler now? (y/n): ")
    
    if response.lower() == 'y':
        start_scheduler()
    else:
        print("\n📋 To start manually later, run: python scheduler.py")
        print("📖 For full documentation, see: SCHEDULER_SETUP_GUIDE.md")


if __name__ == "__main__":
    main()


