# Smart Dispatch Scheduler & Alerting Setup Guide

## 🎯 Overview

The automated scheduler provides:
- **Automated Dispatch Processing**: Runs dispatch agent periodically to assign technicians
- **Real-time Alert Monitoring**: Checks metrics every 5 minutes and triggers alerts
- **Automated Reporting**: Daily and weekly summary reports
- **Multi-channel Notifications**: Console, file logs, email, and webhooks (Slack/Teams)

## 📋 Prerequisites

1. **Install Required Packages**:
```bash
pip install -r requirements_dispatch.txt
```

The scheduler requires:
- `APScheduler` - Task scheduling
- `requests` - Webhook notifications
- `psycopg2-binary` - Database connection

## ⚙️ Configuration

### 1. Alert Thresholds

Edit `alert_config.py` to customize alert thresholds:

```python
ALERT_THRESHOLDS = {
    'sla_compliance_critical': 70,      # Alert if SLA < 70%
    'routing_speed_critical': 300,      # Alert if routing > 5 minutes
    'etc_critical': 8,                  # Alert if ETC > 8 hours
    'operational_cost_critical': 500,   # Alert if cost > $500
    'burnout_high_count_critical': 5,   # Alert if 5+ techs burned out
    # ... more thresholds
}
```

### 2. Notification Channels

Enable/disable notification channels in `alert_config.py`:

```python
NOTIFICATION_CHANNELS = {
    'console': True,     # Print to console (always keep enabled)
    'file': True,        # Write to alerts.log (recommended)
    'email': False,      # Email notifications (configure SMTP)
    'webhook': False,    # Slack/Teams webhooks (configure URLs)
}
```

### 3. Email Configuration (Optional)

If you want email alerts, configure in `alert_config.py`:

```python
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',  # Gmail app password
    'recipient_emails': [
        'manager@company.com',
        'dispatcher@company.com'
    ]
}
```

**Gmail App Password Setup**:
1. Go to Google Account → Security
2. Enable 2-Step Verification
3. Go to App Passwords
4. Generate password for "Mail"
5. Use this password in `sender_password`

### 4. Webhook Configuration (Optional)

For Slack or Microsoft Teams alerts:

**Slack**:
1. Go to https://api.slack.com/apps
2. Create new app → Incoming Webhooks
3. Activate webhooks and add to workspace
4. Copy webhook URL to `alert_config.py`:

```python
WEBHOOK_CONFIG = {
    'slack_webhook_url': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
}
```

**Microsoft Teams**:
1. Open Teams channel → Connectors
2. Add "Incoming Webhook"
3. Copy webhook URL to `alert_config.py`:

```python
WEBHOOK_CONFIG = {
    'teams_webhook_url': 'https://outlook.office.com/webhook/YOUR/WEBHOOK/URL'
}
```

### 5. Schedule Configuration

Adjust scheduling intervals in `alert_config.py`:

```python
SCHEDULE_CONFIG = {
    'alert_check_interval': 5,          # Check alerts every 5 minutes
    'dispatch_run_interval': 10,        # Run dispatch every 10 minutes
    'report_generation_interval': 24,   # Reports every 24 hours
    'daily_summary_time': '08:00',      # Daily report at 8 AM
    'weekly_report_day': 0,             # Monday (0=Mon, 6=Sun)
    'weekly_report_time': '09:00',      # Weekly report at 9 AM Monday
}
```

## 🚀 Usage

### Running the Scheduler

**Option 1: Start Scheduler (Recommended for Production)**
```bash
python scheduler.py
```

This will:
- ✅ Run dispatch agent every 10 minutes
- ✅ Check alerts every 5 minutes
- ✅ Send daily summary at 8:00 AM
- ✅ Send weekly summary on Mondays at 9:00 AM

**Press Ctrl+C to stop**

### Running Individual Components

**Run Alert Check Manually**:
```bash
python alert_monitor.py
```

**Run Dispatch Agent Manually**:
```bash
python enhanced_dispatch_agent.py
```

## 📊 What Gets Monitored

### 1. SLA Compliance
- **CRITICAL**: < 70% compliance
- **WARNING**: < 85% compliance
- Checks last 24 hours of dispatch completions

### 2. Routing Speed
- **CRITICAL**: > 5 minutes average
- **WARNING**: > 3 minutes average
- Checks last hour of routing times

### 3. Estimated Time to Complete (ETC)
- **CRITICAL**: > 8 hours average
- **WARNING**: > 6 hours average
- Checks last 4 hours of assignments

### 4. Operational Cost
- **CRITICAL**: > $500 per dispatch
- **WARNING**: > $350 per dispatch
- Checks last 24 hours of costs

### 5. Technician Burnout
- **CRITICAL**: 5+ technicians at high risk
- **WARNING**: 3+ technicians showing signs
- Real-time monitoring

### 6. First-Time Fix Rate
- **WARNING**: Technicians with < 60% fix rate
- Tracks completed jobs over last 7 days

### 7. Pending Dispatches
- **CRITICAL**: 20+ pending dispatches
- **WARNING**: 10+ pending dispatches
- Real-time queue monitoring

### 8. Technician Utilization
- **CRITICAL**: < 40% or > 95% utilization
- **WARNING**: < 50% or > 85% utilization
- Tracks workload balance

## 📁 Output Files

### alerts.log
Contains all alerts with timestamps:
```
============================================================
🚨 CRITICAL ALERT - SLA Compliance
============================================================
Time: 2025-11-18 14:30:45
Message: SLA compliance critically low at 68.5%
Metric Value: 68.5%
Details: Only 137 out of 200 dispatches met SLA in last 24 hours
============================================================
```

### alert_history.json
JSON log of all alerts for analysis:
```json
[
  {
    "priority": "CRITICAL",
    "category": "SLA Compliance",
    "message": "SLA compliance critically low at 68.5%",
    "metric_value": "68.5%",
    "timestamp": "2025-11-18T14:30:45.123456"
  }
]
```

## 🔧 Customization

### Add Custom Alert Rule

1. **Add Threshold** in `alert_config.py`:
```python
ALERT_THRESHOLDS = {
    'my_custom_metric_critical': 100,
}
```

2. **Add Check Method** in `alert_monitor.py`:
```python
def check_my_custom_metric(self):
    """Check my custom metric"""
    cursor = self.conn.cursor(cursor_factory=RealDictCursor)
    
    cursor.execute("""
        SELECT AVG(my_metric) as avg_value
        FROM my_table
        WHERE created_at >= NOW() - INTERVAL '1 hour'
    """)
    
    result = cursor.fetchone()
    cursor.close()
    
    if result and result['avg_value']:
        value = float(result['avg_value'])
        
        if value > ALERT_THRESHOLDS['my_custom_metric_critical']:
            send_alert(
                'CRITICAL',
                'My Custom Metric',
                f'Metric exceeded threshold: {value}',
                'Additional context here',
                f"{value}"
            )
```

3. **Call in check_all_alerts**:
```python
def check_all_alerts(self):
    # ... existing checks ...
    self.check_my_custom_metric()
```

### Adjust Quiet Hours

Prevent alerts during specific hours (except CRITICAL):

```python
ALERT_SUPPRESSION = {
    'quiet_hours_enabled': True,
    'quiet_hours_start': '22:00',  # 10 PM
    'quiet_hours_end': '07:00',    # 7 AM
}
```

### Suppress Duplicate Alerts

Prevent alert fatigue by suppressing duplicate alerts:

```python
ALERT_SUPPRESSION = {
    'duplicate_suppression_minutes': 30,  # Don't resend same alert within 30 min
}
```

## 🖥️ Running as Background Service

### Windows (Task Scheduler)

1. Open Task Scheduler
2. Create Basic Task → "Smart Dispatch Scheduler"
3. Trigger: "When computer starts"
4. Action: "Start a program"
   - Program: `python`
   - Arguments: `scheduler.py`
   - Start in: `C:\Users\ftrhack93\Downloads\Test_Folder`
5. Settings → Run whether user is logged in or not

### Linux (systemd)

Create `/etc/systemd/system/dispatch-scheduler.service`:

```ini
[Unit]
Description=Smart Dispatch Scheduler
After=network.target postgresql.service

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/Test_Folder
ExecStart=/usr/bin/python3 scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable dispatch-scheduler
sudo systemctl start dispatch-scheduler
sudo systemctl status dispatch-scheduler
```

### Running in tmux/screen (Simple Alternative)

**Using tmux**:
```bash
tmux new -s dispatch-scheduler
python scheduler.py

# Detach: Ctrl+B, then D
# Reattach: tmux attach -t dispatch-scheduler
```

**Using screen**:
```bash
screen -S dispatch-scheduler
python scheduler.py

# Detach: Ctrl+A, then D
# Reattach: screen -r dispatch-scheduler
```

## 📈 Monitoring the Scheduler

### Check if Running
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep scheduler.py
```

### View Real-time Alerts
```bash
# Windows PowerShell
Get-Content -Path "alerts.log" -Wait -Tail 20

# Linux/Mac
tail -f alerts.log
```

### View Alert History
```bash
# View last 10 alerts
python -c "import json; alerts = json.load(open('alert_history.json')); print('\n'.join([f\"{a['timestamp']}: {a['priority']} - {a['message']}\" for a in alerts[-10:]]))"
```

## 🎯 Best Practices

1. **Start with Console + File Notifications**
   - Monitor for a few days
   - Adjust thresholds based on your data
   - Then enable email/webhooks

2. **Customize Thresholds**
   - Default thresholds are starting points
   - Tune based on your business requirements
   - Review `alert_history.json` weekly

3. **Test Notifications**
   - Before deploying, test each notification channel
   - Verify emails arrive and webhooks work
   - Check alert suppression is working

4. **Monitor the Scheduler**
   - Check `alerts.log` regularly
   - Ensure scheduler is running continuously
   - Review daily/weekly summaries

5. **Alert Fatigue Prevention**
   - Use quiet hours for non-critical alerts
   - Enable duplicate suppression
   - Adjust thresholds if too many false positives

## 🐛 Troubleshooting

### Scheduler Not Running

**Check**:
```bash
python scheduler.py
```

**Common Issues**:
- Database connection failed → Check `DB_CONFIG` in `scheduler.py`
- Import errors → Run `pip install -r requirements_dispatch.txt`
- Port conflicts → No ports needed for scheduler

### No Alerts Triggering

**Test Alert Monitor**:
```bash
python alert_monitor.py
```

**Possible Causes**:
- No data in metrics tables → Run dispatch agent first
- Thresholds too high → Adjust in `alert_config.py`
- Quiet hours enabled → Check time or disable

### Email Not Sending

**Test Email Config**:
```python
from notification_handler import send_alert
send_alert('INFO', 'Test', 'This is a test email')
```

**Common Issues**:
- Wrong SMTP settings → Verify server/port
- Authentication failed → Use app-specific password for Gmail
- Firewall blocking → Check port 587 is open

### Webhook Not Working

**Test Webhook**:
```python
import requests
response = requests.post('YOUR_WEBHOOK_URL', json={'text': 'Test'})
print(response.status_code)  # Should be 200
```

**Common Issues**:
- Invalid webhook URL → Regenerate webhook
- Payload format wrong → Check Slack/Teams documentation
- Webhook expired → Create new one

## 📚 Related Files

- `alert_config.py` - Configuration and thresholds
- `alert_monitor.py` - Metric monitoring and alert checking
- `notification_handler.py` - Multi-channel notifications
- `scheduler.py` - Task scheduling orchestrator
- `enhanced_dispatch_agent.py` - Dispatch processing
- `alerts.log` - Alert log file
- `alert_history.json` - Alert history JSON

## 🎓 Next Steps

1. **Run the scheduler**:
   ```bash
   python scheduler.py
   ```

2. **Monitor for a day** - Watch console output and `alerts.log`

3. **Tune thresholds** - Adjust based on your business needs

4. **Enable additional channels** - Set up email or webhooks

5. **Deploy as service** - Run continuously in background

## 💡 Tips

- Start conservative with thresholds, then tighten
- Review alert history weekly to spot trends
- Use quiet hours to prevent overnight noise
- Set up different notification channels for different alert levels (e.g., email only for CRITICAL)
- Monitor scheduler health with process monitoring tools

---

**Need Help?** Check the logs in `alerts.log` and `alert_history.json` for diagnostic information.


