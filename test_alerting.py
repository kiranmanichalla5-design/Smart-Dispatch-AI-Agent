"""
Test Script for Alerting System
Demonstrates all alert types and notification channels
"""

from notification_handler import send_alert
from datetime import datetime
import time


def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)


def test_alert_priorities():
    """Test different alert priorities"""
    print_section("Testing Alert Priorities")
    
    # CRITICAL alert
    print("\n1. Testing CRITICAL alert...")
    send_alert(
        'CRITICAL',
        'SLA Compliance',
        'SLA compliance critically low at 65.2%',
        'Only 130 out of 200 dispatches met SLA in last 24 hours',
        '65.2%'
    )
    time.sleep(1)
    
    # WARNING alert
    print("\n2. Testing WARNING alert...")
    send_alert(
        'WARNING',
        'Routing Speed',
        'Routing speed degraded: 195 seconds average',
        'Consider investigating system performance',
        '195s'
    )
    time.sleep(1)
    
    # INFO alert
    print("\n3. Testing INFO alert...")
    send_alert(
        'INFO',
        'System Status',
        'Automated monitoring initialized',
        'All systems operational'
    )
    time.sleep(1)
    
    # SUCCESS alert
    print("\n4. Testing SUCCESS alert...")
    send_alert(
        'SUCCESS',
        'Dispatch Processing',
        'All pending dispatches processed successfully',
        '50 dispatches assigned in the last run'
    )
    time.sleep(1)


def test_business_problem_alerts():
    """Test alerts for the 8 business problems"""
    print_section("Testing Business Problem Alerts")
    
    # Problem 1: Estimated Time of Completion
    print("\n1. Testing ETC Alert...")
    send_alert(
        'CRITICAL',
        'Completion Time',
        'Estimated completion times very high: 9.5 hours',
        'Customer wait times may be excessive',
        '9.5h'
    )
    time.sleep(1)
    
    # Problem 2: Routing Speed
    print("\n2. Testing Routing Speed Alert...")
    send_alert(
        'CRITICAL',
        'Routing Speed',
        'Routing taking too long: 320 seconds average',
        'Dispatches are being routed slower than acceptable',
        '320s'
    )
    time.sleep(1)
    
    # Problem 3: Technician Availability (Fallback)
    print("\n3. Testing Fallback Routing Alert...")
    send_alert(
        'WARNING',
        'Technician Availability',
        'Primary technician unavailable, routed to fallback',
        'Dispatch #12345 assigned to second-choice technician'
    )
    time.sleep(1)
    
    # Problem 4: Operational Costs
    print("\n4. Testing Operational Cost Alert...")
    send_alert(
        'CRITICAL',
        'Operational Cost',
        'Average dispatch cost critically high: $525.00',
        'Review dispatch assignments and optimize routing',
        '$525.00'
    )
    time.sleep(1)
    
    # Problem 5: Customer Wait Times
    print("\n5. Testing Customer Wait Time Alert...")
    send_alert(
        'WARNING',
        'Pending Dispatches',
        '15 dispatches in queue',
        'Monitor situation and ensure adequate staffing',
        '15 dispatches'
    )
    time.sleep(1)
    
    # Problem 6: First-Time Fix Rates
    print("\n6. Testing First-Time Fix Alert...")
    send_alert(
        'WARNING',
        'First-Time Fix Rate',
        '3 technician(s) with low first-time fix rates',
        'Technicians need training: John Smith (58%), Jane Doe (55%)',
        '3 technicians'
    )
    time.sleep(1)
    
    # Problem 7: Technician Burnout
    print("\n7. Testing Burnout Alert...")
    send_alert(
        'CRITICAL',
        'Technician Burnout',
        '6 technicians at high burnout risk',
        'Immediate intervention needed to prevent turnover',
        '6 technicians'
    )
    time.sleep(1)
    
    # Problem 8: Resource Utilization
    print("\n8. Testing Utilization Alert...")
    send_alert(
        'CRITICAL',
        'Resource Utilization',
        '4 technician(s) critically overutilized',
        'Risk of burnout: Mike Johnson (96%), Sarah Williams (98%)',
        '4 technicians'
    )
    time.sleep(1)


def test_summary_report():
    """Test summary report"""
    print_section("Testing Summary Report")
    
    from notification_handler import send_summary
    
    summary_data = {
        'period': 'Test Period - Last 24 hours',
        'total_dispatches': 150,
        'pending': 25,
        'completed': 125,
        'avg_routing_time': 145.5,
        'avg_etc': 5.2,
        'sla_compliance': 87.5,
        'avg_cost': 285.50,
        'burnout_alerts': 3,
        'techs_available': 12,
        'techs_busy': 8,
        'avg_utilization': 72.5
    }
    
    print("\nSending summary report...")
    send_summary(summary_data)


def show_alert_files():
    """Show where to find alerts"""
    print_section("Where to Find Alerts")
    
    import os
    
    print("\n📁 Alert Files:")
    
    if os.path.exists('alerts.log'):
        size = os.path.getsize('alerts.log')
        print(f"  ✅ alerts.log ({size} bytes)")
    else:
        print("  ⚪ alerts.log (not created yet)")
    
    if os.path.exists('alert_history.json'):
        size = os.path.getsize('alert_history.json')
        print(f"  ✅ alert_history.json ({size} bytes)")
    else:
        print("  ⚪ alert_history.json (not created yet)")
    
    print("\n📖 How to View:")
    print("  • Open alerts.log in any text editor")
    print("  • Tail alerts.log for real-time: tail -f alerts.log")
    print("  • View JSON: python -c \"import json; print(json.dumps(json.load(open('alert_history.json')), indent=2))\"")


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🧪 ALERT SYSTEM TEST")
    print("="*60)
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    print("\nThis test will demonstrate:")
    print("  1. Different alert priorities (CRITICAL, WARNING, INFO, SUCCESS)")
    print("  2. Alerts for all 8 business problems")
    print("  3. Summary report generation")
    print("  4. Where to find alert logs")
    
    input("\nPress Enter to start the test...")
    
    # Run tests
    test_alert_priorities()
    time.sleep(2)
    
    test_business_problem_alerts()
    time.sleep(2)
    
    test_summary_report()
    time.sleep(1)
    
    show_alert_files()
    
    # Final summary
    print_section("Test Complete")
    print("\n✅ All alert types have been demonstrated!")
    print("\n📋 Next Steps:")
    print("  1. Check alerts.log to see all alerts")
    print("  2. Check alert_history.json for JSON format")
    print("  3. Review alert_config.py to customize thresholds")
    print("  4. Enable email/webhook notifications in alert_config.py")
    print("  5. Run: python scheduler.py to start automated monitoring")
    
    print("\n" + "="*60)
    print("  For full documentation, see:")
    print("  • QUICK_START_SCHEDULER.md")
    print("  • SCHEDULER_SETUP_GUIDE.md")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()


