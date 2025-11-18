"""
Alert Configuration for Smart Dispatch System
Defines thresholds and rules for automated alerting
"""

# ============================================================
# ALERT THRESHOLDS
# ============================================================

ALERT_THRESHOLDS = {
    # SLA Compliance (percentage)
    'sla_compliance_critical': 70,  # Alert if below 70%
    'sla_compliance_warning': 85,   # Warning if below 85%
    
    # Routing Speed (seconds)
    'routing_speed_critical': 300,  # Alert if > 5 minutes
    'routing_speed_warning': 180,   # Warning if > 3 minutes
    
    # ETC - Estimated Time to Complete (hours)
    'etc_critical': 8,              # Alert if > 8 hours
    'etc_warning': 6,               # Warning if > 6 hours
    
    # Operational Cost (dollars per dispatch)
    'operational_cost_critical': 500,  # Alert if > $500
    'operational_cost_warning': 350,   # Warning if > $350
    
    # Burnout Risk
    'burnout_high_count_critical': 5,  # Alert if 5+ techs at high burnout
    'burnout_high_count_warning': 3,   # Warning if 3+ techs
    
    # First-Time Fix Rate (percentage)
    'first_time_fix_critical': 60,  # Alert if below 60%
    'first_time_fix_warning': 75,   # Warning if below 75%
    
    # Pending Dispatches
    'pending_dispatches_critical': 20,  # Alert if 20+ pending
    'pending_dispatches_warning': 10,   # Warning if 10+ pending
    
    # Technician Utilization
    'utilization_critical_low': 40,   # Alert if below 40%
    'utilization_critical_high': 95,  # Alert if above 95%
    'utilization_warning_low': 50,    # Warning if below 50%
    'utilization_warning_high': 85,   # Warning if above 85%
}

# ============================================================
# ALERT PRIORITIES
# ============================================================

ALERT_PRIORITY = {
    'CRITICAL': {
        'color': 'red',
        'icon': '🚨',
        'requires_immediate_action': True
    },
    'WARNING': {
        'color': 'yellow',
        'icon': '⚠️',
        'requires_immediate_action': False
    },
    'INFO': {
        'color': 'blue',
        'icon': 'ℹ️',
        'requires_immediate_action': False
    },
    'SUCCESS': {
        'color': 'green',
        'icon': '✅',
        'requires_immediate_action': False
    }
}

# ============================================================
# NOTIFICATION CHANNELS
# ============================================================

NOTIFICATION_CHANNELS = {
    'console': True,      # Print to console
    'file': True,         # Write to alert log file
    'email': False,       # Send email (requires SMTP config)
    'webhook': False,     # Send to webhook (for Slack, Teams, etc.)
}

# ============================================================
# EMAIL CONFIGURATION (if email notifications enabled)
# ============================================================

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',  # Use app-specific password
    'recipient_emails': [
        'manager@company.com',
        'dispatcher@company.com'
    ],
    'cc_emails': []
}

# ============================================================
# WEBHOOK CONFIGURATION (for Slack, Teams, etc.)
# ============================================================

WEBHOOK_CONFIG = {
    'slack_webhook_url': '',  # Add your Slack webhook URL
    'teams_webhook_url': '',  # Add your Teams webhook URL
}

# ============================================================
# ALERT LOG FILE
# ============================================================

ALERT_LOG_FILE = 'alerts.log'
ALERT_HISTORY_FILE = 'alert_history.json'

# ============================================================
# SCHEDULING CONFIGURATION
# ============================================================

SCHEDULE_CONFIG = {
    # How often to check for alerts (in minutes)
    'alert_check_interval': 5,
    
    # How often to run dispatch agent (in minutes)
    'dispatch_run_interval': 10,
    
    # How often to generate summary reports (in hours)
    'report_generation_interval': 24,
    
    # Time to send daily summary report (24-hour format)
    'daily_summary_time': '08:00',
    
    # Days to send weekly report (0=Monday, 6=Sunday)
    'weekly_report_day': 0,
    'weekly_report_time': '09:00',
}

# ============================================================
# ALERT SUPPRESSION (to avoid alert fatigue)
# ============================================================

ALERT_SUPPRESSION = {
    # Don't send same alert again within X minutes
    'duplicate_suppression_minutes': 30,
    
    # Group similar alerts together
    'group_similar_alerts': True,
    
    # Quiet hours (no alerts during this time unless CRITICAL)
    'quiet_hours_enabled': False,
    'quiet_hours_start': '22:00',
    'quiet_hours_end': '07:00',
}


