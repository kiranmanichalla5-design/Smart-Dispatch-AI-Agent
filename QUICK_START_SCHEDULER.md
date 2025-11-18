# Quick Start: Automated Scheduler & Alerting

## 🚀 1-Minute Setup

### Install Dependencies
```bash
pip install -r requirements_dispatch.txt
```

### Start Scheduler (Guided)
```bash
python start_scheduler.py
```

This will check everything and start the scheduler.

### Start Scheduler (Direct)
```bash
python scheduler.py
```

Press `Ctrl+C` to stop.

---

## 📋 What It Does

### Automated Tasks:
- ✅ **Every 5 minutes**: Check metrics and send alerts
- ✅ **Every 10 minutes**: Run dispatch agent to assign technicians
- ✅ **Daily at 8:00 AM**: Send summary report
- ✅ **Monday at 9:00 AM**: Send weekly summary report

### Alerts You'll Get:

| Alert | Critical Threshold | Warning Threshold |
|-------|-------------------|-------------------|
| SLA Compliance | < 70% | < 85% |
| Routing Speed | > 5 minutes | > 3 minutes |
| Completion Time (ETC) | > 8 hours | > 6 hours |
| Operational Cost | > $500/dispatch | > $350/dispatch |
| Technician Burnout | 5+ techs at risk | 3+ techs showing signs |
| First-Time Fix Rate | < 60% | < 75% |
| Pending Dispatches | 20+ pending | 10+ pending |
| Utilization | < 40% or > 95% | < 50% or > 85% |

---

## 📂 Where to Find Alerts

### Console
All alerts print in real-time with color coding:
- 🚨 Red = CRITICAL
- ⚠️ Yellow = WARNING
- ℹ️ Blue = INFO
- ✅ Green = SUCCESS

### alerts.log
All alerts with full details and timestamps

### alert_history.json
JSON format for analysis and reporting

---

## ⚙️ Quick Configuration

### Edit `alert_config.py`

**Change Thresholds:**
```python
ALERT_THRESHOLDS = {
    'sla_compliance_critical': 70,  # Change to your target
    'routing_speed_critical': 300,  # In seconds
}
```

**Enable Email Alerts:**
```python
NOTIFICATION_CHANNELS = {
    'email': True,  # Change from False
}

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'sender_email': 'your-email@gmail.com',
    'sender_password': 'your-app-password',
    'recipient_emails': ['manager@company.com']
}
```

**Enable Slack Alerts:**
```python
NOTIFICATION_CHANNELS = {
    'webhook': True,  # Change from False
}

WEBHOOK_CONFIG = {
    'slack_webhook_url': 'https://hooks.slack.com/services/YOUR/WEBHOOK'
}
```

**Change Schedule:**
```python
SCHEDULE_CONFIG = {
    'alert_check_interval': 5,      # Minutes
    'dispatch_run_interval': 10,    # Minutes
    'daily_summary_time': '08:00',  # Time for daily report
}
```

---

## 🧪 Test Before Production

### 1. Test Alert System
```bash
python alert_monitor.py
```

### 2. Check Alerts Log
```bash
# Windows PowerShell
Get-Content alerts.log -Tail 20

# Linux/Mac
tail -20 alerts.log
```

### 3. Send Test Alert
```python
from notification_handler import send_alert

send_alert(
    'INFO',
    'Test',
    'This is a test alert',
    'Testing the notification system'
)
```

---

## 🔧 Common Commands

### View Running Scheduler
```bash
# Windows
tasklist | findstr python

# Linux/Mac
ps aux | grep scheduler
```

### Stop Scheduler
Press `Ctrl+C` in the terminal running scheduler

### View Real-time Alerts
```bash
# Windows PowerShell
Get-Content -Path "alerts.log" -Wait

# Linux/Mac
tail -f alerts.log
```

### Check Last 10 Alerts
```bash
python -c "import json; alerts = json.load(open('alert_history.json')); [print(f\"{a['timestamp']}: {a['priority']} - {a['message']}\") for a in alerts[-10:]]"
```

---

## 📚 Documentation

- **Full Setup Guide**: `SCHEDULER_SETUP_GUIDE.md`
- **Fine-Tuning Guide**: `FINE_TUNING_GUIDE.md`
- **Configuration**: `alert_config.py`

---

## 🎯 Typical Workflow

### Morning (8:00 AM):
- Receive daily summary report
- Review alerts from overnight

### Throughout Day:
- System automatically processes dispatches every 10 minutes
- Alerts sent immediately when thresholds breached
- Monitor `alerts.log` or dashboard

### End of Day:
- Review alert history
- Adjust thresholds if needed

### Monday Morning (9:00 AM):
- Receive weekly summary report
- Review trends and patterns
- Plan improvements

---

## 💡 Pro Tips

1. **Start Conservative**: Begin with default thresholds, adjust based on your data
2. **Use Console First**: Monitor console output for a day before enabling email
3. **Check Logs Daily**: Review `alerts.log` to understand patterns
4. **Tune Thresholds**: Adjust based on `alert_history.json` analysis
5. **Prevent Fatigue**: Use duplicate suppression and quiet hours
6. **Background Service**: Run in tmux/screen for continuous operation

---

## 🆘 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Scheduler won't start | Check dependencies: `pip install -r requirements_dispatch.txt` |
| No alerts appearing | Check thresholds in `alert_config.py` - may be too high |
| Email not sending | Verify SMTP settings and use app-specific password |
| Database connection error | Check database is running and credentials correct |
| Scheduler keeps stopping | Run in tmux/screen or as system service |

---

## ✅ Success Checklist

- [ ] Installed dependencies
- [ ] Ran `python start_scheduler.py` successfully
- [ ] Saw initial alert check complete
- [ ] Found `alerts.log` file created
- [ ] Reviewed configuration in `alert_config.py`
- [ ] Tested for 1 hour minimum
- [ ] Adjusted thresholds based on your data
- [ ] Set up to run continuously (tmux/service)

**Once complete, your dispatch system runs autonomously with intelligent monitoring!** 🎉


