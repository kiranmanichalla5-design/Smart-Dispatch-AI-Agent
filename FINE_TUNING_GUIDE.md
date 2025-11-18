# Fine-Tuning Guide - Dispatch Agent

## 📊 Analysis Results

Based on the analysis, here's what we found:

### Current Status:
- **Total Dispatches:** 600
- **Completed:** 20 (3.3%)
- **Pending:** 580 (96.7%)
- **Assigned Technicians:** 5
- **Skill Match Rate:** 95% (excellent!)

### Key Findings:

1. **Priority Distribution:**
   - Critical: 200 dispatches (20 completed, 180 pending)
   - Normal: 300 dispatches (all pending)
   - Low: 100 dispatches (all pending)

2. **Skill Distribution:**
   - Line repair: 100 dispatches (10 completed, 90 pending)
   - Network troubleshooting: 100 dispatches (10 completed, 90 pending)
   - Installation skills: 300 dispatches (all pending)
   - Network support: 100 dispatches (all pending)

3. **Technician Assignments:**
   - Only 5 technicians have assignments
   - Most technicians are available
   - Good skill matching (95% exact match)

---

## 🔧 Enhanced Features

### 1. **Enhanced Matching Algorithm** (`enhanced_dispatch_agent.py`)

**New Features:**
- ✅ **Priority Balance Scoring** - Prevents overloading technicians with only critical dispatches
- ✅ **Skill Diversity Scoring** - Distributes different skills across technicians
- ✅ **Improved Skill Matching** - Better keyword and related skill detection
- ✅ **Workload Tracking** - Tracks assignments in real-time
- ✅ **Routing SLA Tracking** - Measures time from request to assignment and flags breaches
- ✅ **Estimated Time of Completion (ETC)** - Uses historical skill averages when duration missing
- ✅ **Operational Cost Modeling** - Combines travel distance + labor time for each dispatch
- ✅ **Fallback Technician Capture** - Stores next-best options when first choice is unavailable
- ✅ **Burnout Risk Detection** - Flags technicians above utilization thresholds

**Scoring Weights:**
- Skill Match: 40%
- Distance: 25%
- Availability: 15%
- Priority Balance: 10% (NEW)
- Skill Diversity: 5% (NEW)
- Historical Performance: 5%

### Dispatch Metrics Table (`dispatch_metrics`)

- `routing_seconds` & `sla_breached` captured for every assignment
- `estimated_completion_minutes` derived from duration & history
- `operational_cost` = travel cost + labor cost
- `fallback_technicians` stored as JSON for auditing reroutes
- `burnout_risk` flagged when utilization exceeds 85%

### 2. **Assignment Analytics Dashboard** (`assignment_analytics_dashboard.py`)

**Visualizations:**
- Status distribution (Completed vs Pending)
- Priority distribution charts
- Skill distribution charts
- Technician assignment summary table
- Priority by status breakdown
- Routing vs completion trend
- Operational cost by priority
- SLA compliance & burnout alert summaries

**Access:** http://127.0.0.1:5004

---

## 🚀 How to Use

### Step 1: Run Analysis
```bash
python analyze_assignments.py
```

This shows:
- Assignment patterns by priority
- Assignment patterns by skill
- Technician workload distribution
- Skill matching rates
- Pending dispatch analysis

### Step 2: Use Enhanced Agent
```bash
python enhanced_dispatch_agent.py
```

**Improvements:**
- Better workload balancing
- Priority-aware assignment
- Skill diversity consideration
- More consistent assignments

### Step 3: View Analytics Dashboard
```bash
python assignment_analytics_dashboard.py
```

Then open: http://127.0.0.1:5004

**Shows:**
- Real-time statistics
- Interactive charts
- Technician assignment details
- Priority and skill breakdowns
- Routing vs completion trends
- Operational cost, SLA compliance, burnout alerts

---

## 📈 Fine-Tuning Recommendations

### 1. **Process More Dispatches**
Currently only 3.3% are completed. Run the enhanced agent to process more:
```bash
python enhanced_dispatch_agent.py
```

### 2. **Balance Priority Distribution**
The enhanced agent now considers:
- Not overloading technicians with only critical dispatches
- Distributing priorities more evenly
- Better workload balance

### 3. **Improve Skill Matching**
Current match rate is 95% - excellent! But you can:
- Add more related skill mappings
- Improve keyword matching
- Consider technician secondary skills

### 4. **Monitor Assignment Patterns**
Use the analytics dashboard to:
- Track which technicians get which priorities
- Monitor skill distribution
- Identify bottlenecks

---

## 🎯 Key Improvements in Enhanced Agent

### Priority Balance
```python
# Prevents one technician from getting all critical dispatches
priority_balance_score = self.priority_balance_score(technician, dispatch)
```

### Skill Diversity
```python
# Ensures technicians get variety of skills
skill_diversity_score = self.skill_diversity_score(technician, dispatch)
```

### Better Skill Matching
```python
# Improved matching with keyword and related skills
skill_score = self.skill_match_score(technician.primary_skill, dispatch.required_skill)
```

---

## 📊 Understanding the Analytics

### Priority Distribution
- Shows how many dispatches of each priority
- Completed vs Pending breakdown
- Helps identify if critical dispatches are being prioritized

### Skill Distribution
- Shows which skills are most needed
- Completed vs Pending by skill
- Helps identify skill gaps

### Technician Assignments
- Shows workload per technician
- Priority breakdown per technician
- Average confidence scores
- Helps identify over/under-utilized technicians

---

## 🤖 Automated Scheduling & Alerting

### NEW: Continuous Monitoring & Alerts

The system now includes **automated scheduling and intelligent alerting** to proactively monitor your dispatch operations 24/7.

**Features:**
- ✅ **Automated Dispatch Processing** - Runs dispatch agent every 10 minutes
- ✅ **Real-time Alert Monitoring** - Checks metrics every 5 minutes
- ✅ **Multi-channel Notifications** - Console, file logs, email, Slack/Teams
- ✅ **Smart Alert Suppression** - Prevents alert fatigue
- ✅ **Daily/Weekly Summary Reports** - Automated reporting

### What Gets Monitored:

1. **SLA Compliance** - Alerts if below 70% (critical) or 85% (warning)
2. **Routing Speed** - Alerts if > 5 minutes (critical) or 3 minutes (warning)
3. **Estimated Completion Time** - Alerts if > 8 hours (critical)
4. **Operational Costs** - Alerts if > $500 per dispatch (critical)
5. **Technician Burnout** - Alerts if 5+ technicians at high risk
6. **First-Time Fix Rate** - Alerts if technicians below 60%
7. **Pending Dispatch Queue** - Alerts if 20+ pending (critical)
8. **Technician Utilization** - Alerts if < 40% or > 95%

### Quick Start:

**Option 1: Guided Setup**
```bash
python start_scheduler.py
```

This will:
- ✅ Check all dependencies
- ✅ Test database connection
- ✅ Verify required tables
- ✅ Run initial alert check
- ✅ Start the scheduler

**Option 2: Direct Start**
```bash
python scheduler.py
```

**Option 3: Test Alerts Only**
```bash
python alert_monitor.py
```

### Configuration:

Edit `alert_config.py` to customize:
- Alert thresholds
- Notification channels (console, email, webhooks)
- Schedule intervals
- Quiet hours
- Alert suppression rules

**Example:**
```python
ALERT_THRESHOLDS = {
    'sla_compliance_critical': 70,      # Your target
    'routing_speed_critical': 300,      # 5 minutes
    'burnout_high_count_critical': 5,   # Number of techs
}

NOTIFICATION_CHANNELS = {
    'console': True,      # Always enabled
    'file': True,         # Logs to alerts.log
    'email': False,       # Set to True + configure SMTP
    'webhook': False,     # Set to True + add Slack/Teams URL
}
```

### Output Files:

- **`alerts.log`** - All alerts with timestamps and details
- **`alert_history.json`** - JSON log for analysis
- Console output in real-time

### Full Documentation:

See **`SCHEDULER_SETUP_GUIDE.md`** for:
- Email configuration (Gmail, SMTP)
- Webhook setup (Slack, Microsoft Teams)
- Running as background service
- Customizing alert rules
- Troubleshooting

---

## 🔄 Next Steps

1. **Run Enhanced Agent:**
   ```bash
   python enhanced_dispatch_agent.py
   ```

2. **Monitor Results:**
   ```bash
   python analyze_assignments.py
   ```

3. **View Dashboard:**
   ```bash
   python assignment_analytics_dashboard.py
   ```

4. **Start Automated Monitoring:** (NEW)
   ```bash
   python start_scheduler.py
   ```

5. **Adjust Weights:**
   - Edit `enhanced_dispatch_agent.py`
   - Modify scoring weights in `score_technician()` method
   - Edit `alert_config.py` to customize alert thresholds
   - Test and iterate

---

## 💡 Tips

1. **Start with Priority First:**
   - Enhanced agent processes critical dispatches first
   - Ensures urgent issues get attention

2. **Monitor Workload:**
   - Check analytics dashboard regularly
   - Ensure technicians aren't overloaded

3. **Balance Skills:**
   - Don't assign same skill to one technician repeatedly
   - Use skill diversity scoring

4. **Track Performance:**
   - Monitor confidence scores
   - Review assignment patterns
   - Adjust as needed

---

## 📝 Files Created

### Core Dispatch System:
1. **`analyze_assignments.py`** - Comprehensive analysis tool
2. **`enhanced_dispatch_agent.py`** - Improved matching algorithm
3. **`assignment_analytics_dashboard.py`** - Visual analytics dashboard

### Automated Scheduling & Alerting (NEW):
4. **`scheduler.py`** - Task scheduling orchestrator
5. **`alert_monitor.py`** - Metric monitoring and alert checking
6. **`alert_config.py`** - Configuration and thresholds
7. **`notification_handler.py`** - Multi-channel notifications
8. **`start_scheduler.py`** - Quick start with guided setup

### Documentation:
9. **`FINE_TUNING_GUIDE.md`** - This guide
10. **`SCHEDULER_SETUP_GUIDE.md`** - Complete scheduler documentation

---

## ✅ Summary

You now have:
- ✅ Analysis tools to understand patterns
- ✅ Enhanced matching algorithm
- ✅ Analytics dashboard for visualization
- ✅ Better workload balancing
- ✅ Priority-aware assignment
- ✅ Skill diversity consideration
- ✅ **Automated scheduling and alerting** (NEW)
- ✅ **Real-time monitoring for 8 business problems** (NEW)
- ✅ **Multi-channel notifications** (NEW)
- ✅ **Continuous 24/7 operation** (NEW)

**Quick Start:**
1. Run the enhanced agent: `python enhanced_dispatch_agent.py`
2. Start automated monitoring: `python start_scheduler.py`
3. View dashboards at http://localhost:5000 (technician) and http://localhost:5004 (analytics)

**Your dispatch system now operates autonomously with intelligent monitoring!** 🚀

