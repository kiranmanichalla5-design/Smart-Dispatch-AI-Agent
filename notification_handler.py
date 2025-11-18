"""
Notification Handler for Smart Dispatch Alerts
Handles multiple notification channels: console, file, email, webhook
"""

import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
import requests
from alert_config import (
    NOTIFICATION_CHANNELS, EMAIL_CONFIG, WEBHOOK_CONFIG,
    ALERT_LOG_FILE, ALERT_HISTORY_FILE, ALERT_PRIORITY,
    ALERT_SUPPRESSION
)


class NotificationHandler:
    """Handles sending notifications through multiple channels"""
    
    def __init__(self):
        self.alert_history = self._load_alert_history()
    
    def _load_alert_history(self):
        """Load alert history from file"""
        if os.path.exists(ALERT_HISTORY_FILE):
            try:
                with open(ALERT_HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_alert_history(self):
        """Save alert history to file"""
        with open(ALERT_HISTORY_FILE, 'w') as f:
            json.dump(self.alert_history, f, indent=2)
    
    def _should_suppress_alert(self, alert):
        """Check if alert should be suppressed to avoid alert fatigue"""
        if not ALERT_SUPPRESSION['duplicate_suppression_minutes']:
            return False
        
        # Check if same alert was sent recently
        alert_key = f"{alert['category']}_{alert['message']}"
        current_time = datetime.now()
        
        for hist_alert in self.alert_history:
            if hist_alert.get('key') == alert_key:
                last_time = datetime.fromisoformat(hist_alert['timestamp'])
                time_diff = (current_time - last_time).total_seconds() / 60
                
                if time_diff < ALERT_SUPPRESSION['duplicate_suppression_minutes']:
                    return True
        
        return False
    
    def _is_quiet_hours(self):
        """Check if current time is within quiet hours"""
        if not ALERT_SUPPRESSION['quiet_hours_enabled']:
            return False
        
        now = datetime.now()
        current_time = now.strftime('%H:%M')
        
        start = ALERT_SUPPRESSION['quiet_hours_start']
        end = ALERT_SUPPRESSION['quiet_hours_end']
        
        if start < end:
            return start <= current_time <= end
        else:  # Quiet hours cross midnight
            return current_time >= start or current_time <= end
    
    def send_alert(self, alert):
        """
        Send alert through configured channels
        
        Args:
            alert (dict): Alert information with keys:
                - priority: 'CRITICAL', 'WARNING', 'INFO', 'SUCCESS'
                - category: Alert category (e.g., 'SLA', 'Burnout')
                - message: Alert message
                - details: Additional details (optional)
                - metric_value: The metric value that triggered alert (optional)
        """
        # Check quiet hours (but always send CRITICAL alerts)
        if self._is_quiet_hours() and alert['priority'] != 'CRITICAL':
            return
        
        # Check if alert should be suppressed
        if self._should_suppress_alert(alert):
            return
        
        # Add timestamp and format alert
        alert['timestamp'] = datetime.now().isoformat()
        alert['key'] = f"{alert['category']}_{alert['message']}"
        
        # Get alert priority info
        priority_info = ALERT_PRIORITY.get(alert['priority'], ALERT_PRIORITY['INFO'])
        icon = priority_info['icon']
        
        # Format full message
        full_message = self._format_alert_message(alert, icon)
        
        # Send through enabled channels
        if NOTIFICATION_CHANNELS['console']:
            self._send_console(full_message, alert['priority'])
        
        if NOTIFICATION_CHANNELS['file']:
            self._send_file(full_message)
        
        if NOTIFICATION_CHANNELS['email']:
            self._send_email(alert, full_message)
        
        if NOTIFICATION_CHANNELS['webhook']:
            self._send_webhook(alert, full_message)
        
        # Save to history
        self.alert_history.append(alert)
        self._save_alert_history()
    
    def _format_alert_message(self, alert, icon):
        """Format alert message for display"""
        lines = [
            "=" * 60,
            f"{icon} {alert['priority']} ALERT - {alert['category']}",
            "=" * 60,
            f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Message: {alert['message']}",
        ]
        
        if alert.get('metric_value'):
            lines.append(f"Metric Value: {alert['metric_value']}")
        
        if alert.get('details'):
            lines.append(f"Details: {alert['details']}")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def _send_console(self, message, priority):
        """Print alert to console with color"""
        # ANSI color codes
        colors = {
            'CRITICAL': '\033[91m',  # Red
            'WARNING': '\033[93m',   # Yellow
            'INFO': '\033[94m',      # Blue
            'SUCCESS': '\033[92m',   # Green
        }
        reset = '\033[0m'
        
        color = colors.get(priority, '')
        print(f"{color}{message}{reset}\n")
    
    def _send_file(self, message):
        """Write alert to log file"""
        with open(ALERT_LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(message + "\n\n")
    
    def _send_email(self, alert, message):
        """Send alert via email"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = EMAIL_CONFIG['sender_email']
            msg['To'] = ', '.join(EMAIL_CONFIG['recipient_emails'])
            msg['Subject'] = f"[{alert['priority']}] Smart Dispatch Alert - {alert['category']}"
            
            if EMAIL_CONFIG['cc_emails']:
                msg['Cc'] = ', '.join(EMAIL_CONFIG['cc_emails'])
            
            # Add body
            body = message
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port']) as server:
                server.starttls()
                server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
                
                recipients = EMAIL_CONFIG['recipient_emails'] + EMAIL_CONFIG['cc_emails']
                server.send_message(msg, to_addrs=recipients)
            
            print(f"✉️ Email alert sent to {len(recipients)} recipient(s)")
        
        except Exception as e:
            print(f"❌ Failed to send email alert: {e}")
    
    def _send_webhook(self, alert, message):
        """Send alert to webhook (Slack, Teams, etc.)"""
        try:
            # Slack webhook
            if WEBHOOK_CONFIG.get('slack_webhook_url'):
                slack_payload = {
                    "text": f"*{alert['priority']} Alert*",
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f"*{alert['category']}*\n{alert['message']}"
                            }
                        }
                    ]
                }
                response = requests.post(
                    WEBHOOK_CONFIG['slack_webhook_url'],
                    json=slack_payload,
                    timeout=10
                )
                if response.status_code == 200:
                    print("📱 Slack alert sent")
            
            # Teams webhook
            if WEBHOOK_CONFIG.get('teams_webhook_url'):
                teams_payload = {
                    "title": f"{alert['priority']} Alert - {alert['category']}",
                    "text": alert['message'],
                    "themeColor": ALERT_PRIORITY[alert['priority']]['color']
                }
                response = requests.post(
                    WEBHOOK_CONFIG['teams_webhook_url'],
                    json=teams_payload,
                    timeout=10
                )
                if response.status_code == 200:
                    print("📱 Teams alert sent")
        
        except Exception as e:
            print(f"❌ Failed to send webhook alert: {e}")
    
    def send_summary(self, summary_data):
        """Send daily/weekly summary report"""
        message = self._format_summary(summary_data)
        
        summary_alert = {
            'priority': 'INFO',
            'category': 'Summary Report',
            'message': 'Periodic dispatch system summary',
            'details': message
        }
        
        # Temporarily disable suppression for summaries
        original_suppression = ALERT_SUPPRESSION['duplicate_suppression_minutes']
        ALERT_SUPPRESSION['duplicate_suppression_minutes'] = 0
        
        self.send_alert(summary_alert)
        
        ALERT_SUPPRESSION['duplicate_suppression_minutes'] = original_suppression
    
    def _format_summary(self, data):
        """Format summary report"""
        lines = [
            "\n📊 DISPATCH SYSTEM SUMMARY",
            f"Period: {data.get('period', 'Last 24 hours')}",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "Key Metrics:",
            f"  • Total Dispatches: {data.get('total_dispatches', 0)}",
            f"  • Pending: {data.get('pending', 0)}",
            f"  • Completed: {data.get('completed', 0)}",
            f"  • Avg Routing Time: {data.get('avg_routing_time', 0):.1f}s",
            f"  • Avg ETC: {data.get('avg_etc', 0):.1f} hours",
            f"  • SLA Compliance: {data.get('sla_compliance', 0):.1f}%",
            f"  • Avg Cost: ${data.get('avg_cost', 0):.2f}",
            f"  • Burnout Alerts: {data.get('burnout_alerts', 0)}",
            "",
            "Technician Status:",
            f"  • Available: {data.get('techs_available', 0)}",
            f"  • Busy: {data.get('techs_busy', 0)}",
            f"  • Avg Utilization: {data.get('avg_utilization', 0):.1f}%",
        ]
        
        return "\n".join(lines)


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

_handler = None

def get_notification_handler():
    """Get singleton notification handler instance"""
    global _handler
    if _handler is None:
        _handler = NotificationHandler()
    return _handler


def send_alert(priority, category, message, details=None, metric_value=None):
    """
    Convenience function to send an alert
    
    Args:
        priority: 'CRITICAL', 'WARNING', 'INFO', 'SUCCESS'
        category: Alert category
        message: Alert message
        details: Additional details (optional)
        metric_value: Metric value that triggered alert (optional)
    """
    handler = get_notification_handler()
    alert = {
        'priority': priority,
        'category': category,
        'message': message,
        'details': details,
        'metric_value': metric_value
    }
    handler.send_alert(alert)


def send_summary(summary_data):
    """Send summary report"""
    handler = get_notification_handler()
    handler.send_summary(summary_data)


