# Smart Dispatch System - Complete Architecture

## 🏗️ System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    SMART DISPATCH SYSTEM                        │
│                     (Fully Automated)                           │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐     ┌──────────────┐
│   DISPATCH   │    │   ALERTING   │     │  ANALYTICS   │
│   ENGINE     │    │   SYSTEM     │     │  DASHBOARDS  │
└──────────────┘    └──────────────┘     └──────────────┘
```

---

## 📦 Component Breakdown

### 1️⃣ **Dispatch Engine** (Core Intelligence)

```
┌─────────────────────────────────────────────────┐
│  enhanced_dispatch_agent.py                     │
│  ─────────────────────────────────────────────  │
│  • Skill Matching (40%)                         │
│  • Distance Calculation (25%)                   │
│  • Availability Check (15%)                     │
│  • Priority Balancing (10%)                     │
│  • Skill Diversity (5%)                         │
│  • Historical Performance (5%)                  │
│  ─────────────────────────────────────────────  │
│  Outputs:                                       │
│  ✓ Technician assignments                       │
│  ✓ ETC calculations                             │
│  ✓ Operational costs                            │
│  ✓ Fallback technicians                         │
│  ✓ Burnout risk flags                           │
└─────────────────────────────────────────────────┘
```

**Addresses Business Problems:**
- ✅ #1: Estimated Time of Completion (ETC)
- ✅ #2: Fast routing to proper technician
- ✅ #3: Fallback routing when unavailable
- ✅ #4: Operational cost optimization
- ✅ #7: Burnout detection

### 2️⃣ **Alerting System** (Proactive Monitoring)

```
┌─────────────────────────────────────────────────┐
│  scheduler.py (Orchestrator)                    │
│  ─────────────────────────────────────────────  │
│  Every 5 min:  ➜  alert_monitor.py              │
│  Every 10 min: ➜  enhanced_dispatch_agent.py    │
│  Daily 8am:    ➜  Daily Summary Report          │
│  Monday 9am:   ➜  Weekly Summary Report         │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  alert_monitor.py (Metric Checker)              │
│  ─────────────────────────────────────────────  │
│  Monitors 8 Key Metrics:                        │
│  1. SLA Compliance                              │
│  2. Routing Speed                               │
│  3. Estimated Completion Time                   │
│  4. Operational Costs                           │
│  5. Technician Burnout                          │
│  6. First-Time Fix Rate                         │
│  7. Pending Dispatches Queue                    │
│  8. Technician Utilization                      │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  notification_handler.py (Alert Dispatcher)     │
│  ─────────────────────────────────────────────  │
│  Channels:                                      │
│  • Console (✅ Enabled by default)              │
│  • File Logs (✅ alerts.log)                    │
│  • Email (⚪ Optional - SMTP)                   │
│  • Webhooks (⚪ Optional - Slack/Teams)         │
│  ─────────────────────────────────────────────  │
│  Features:                                      │
│  • Duplicate suppression                        │
│  • Quiet hours                                  │
│  • Priority-based routing                       │
│  • Alert history tracking                       │
└─────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────┐
│  Output Files:                                  │
│  • alerts.log (Human-readable)                  │
│  • alert_history.json (Machine-readable)        │
└─────────────────────────────────────────────────┘
```

**Addresses Business Problems:**
- ✅ All 8 problems through continuous monitoring

### 3️⃣ **Analytics Dashboards** (Visualization)

```
┌─────────────────────────────────────────────────┐
│  technician_dashboard.py                        │
│  ────────────────────────────────────────────── │
│  URL: http://localhost:5000                     │
│  ────────────────────────────────────────────── │
│  Shows:                                         │
│  • Technician status & availability             │
│  • Current assignments by priority              │
│  • Utilization percentages                      │
│  • Burnout risk indicators                      │
│  • Real-time metrics                            │
│  • Routing & ETC trends                         │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  assignment_analytics_dashboard.py              │
│  ────────────────────────────────────────────── │
│  URL: http://localhost:5004                     │
│  ────────────────────────────────────────────── │
│  Shows:                                         │
│  • Status & priority distribution               │
│  • Skill distribution charts                    │
│  • Technician workload summary                  │
│  • Operational cost breakdown                   │
│  • SLA compliance tracking                      │
│  • Recent assignments table                     │
└─────────────────────────────────────────────────┘
```

**Addresses Business Problems:**
- ✅ Visualization for all 8 problems

### 4️⃣ **Analysis Tools** (Deep Insights)

```
┌─────────────────────────────────────────────────┐
│  analyze_assignments.py                         │
│  ────────────────────────────────────────────── │
│  Analyzes:                                      │
│  • Assignment patterns by priority              │
│  • Assignment patterns by skill                 │
│  • Technician workload distribution             │
│  • Skill matching rates                         │
│  • Routing metrics                              │
│  • Operational costs                            │
│  • SLA compliance                               │
│  • Burnout risks                                │
│  ────────────────────────────────────────────── │
│  Generates: Console report + metrics            │
└─────────────────────────────────────────────────┘
```

---

## 🗄️ Database Schema

```sql
┌────────────────────────────────────────────────┐
│  technicians                                   │
│  ─────────────────────────────────────────────│
│  • technician_id (PK)                          │
│  • name                                        │
│  • primary_skill                               │
│  • latitude, longitude                         │
│  • availability_status                         │
│  • utilization_percentage                      │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  current_dispatches                            │
│  ─────────────────────────────────────────────│
│  • dispatch_id (PK)                            │
│  • customer_name                               │
│  • required_skill                              │
│  • priority                                    │
│  • latitude, longitude                         │
│  • status                                      │
│  • technician_id (FK)                          │
│  • created_at                                  │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  dispatch_history                              │
│  ─────────────────────────────────────────────│
│  • history_id (PK)                             │
│  • dispatch_id (FK)                            │
│  • technician_id (FK)                          │
│  • status                                      │
│  • dispatch_date                               │
│  • completion_date                             │
│  • notes                                       │
└────────────────────────────────────────────────┘

┌────────────────────────────────────────────────┐
│  dispatch_metrics (NEW)                        │
│  ─────────────────────────────────────────────│
│  • metric_id (PK)                              │
│  • dispatch_id (FK)                            │
│  • technician_id (FK)                          │
│  • routing_speed_seconds                       │
│  • estimated_completion_hours                  │
│  • operational_cost                            │
│  • sla_met (boolean)                           │
│  • burnout_alert (boolean)                     │
│  • fallback_technicians (JSON)                 │
│  • created_at                                  │
└────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

```
1. DISPATCH CREATION
   ↓
   current_dispatches table (status='Pending')
   
2. SCHEDULER TRIGGERS (every 10 minutes)
   ↓
   enhanced_dispatch_agent.py runs
   
3. INTELLIGENT MATCHING
   ↓
   • Calculate skill match scores
   • Calculate distance
   • Check availability
   • Consider priority balance
   • Consider skill diversity
   • Review historical performance
   
4. TECHNICIAN ASSIGNMENT
   ↓
   • Update current_dispatches (technician_id, status='Assigned')
   • Calculate ETC
   • Calculate operational cost
   • Determine fallback technicians
   • Check burnout risk
   
5. METRICS RECORDING
   ↓
   dispatch_metrics table
   • routing_speed_seconds
   • estimated_completion_hours
   • operational_cost
   • sla_met
   • burnout_alert
   
6. ALERT CHECKING (every 5 minutes)
   ↓
   alert_monitor.py runs
   • Query dispatch_metrics
   • Compare against thresholds
   • Generate alerts if needed
   
7. NOTIFICATION DISPATCH
   ↓
   notification_handler.py
   • Console output (colored)
   • alerts.log (persistent)
   • alert_history.json (structured)
   • Email (if enabled)
   • Webhook (if enabled)
   
8. COMPLETION
   ↓
   • dispatch_history table
   • Status changed to 'Completed'
   • Technician freed up
```

---

## ⚙️ Configuration Files

| File | Purpose | Key Settings |
|------|---------|--------------|
| `alert_config.py` | Alert thresholds & channels | SLA targets, cost limits, schedule times |
| `enhanced_dispatch_agent.py` | Scoring weights | Skill:40%, Distance:25%, Availability:15% |
| `scheduler.py` | Task scheduling | DB credentials, scheduling logic |
| `alert_monitor.py` | Metric checks | DB credentials, query logic |
| `notification_handler.py` | Notification routing | Email/webhook integration |

---

## 🚀 Startup Sequence

```
Option 1: Manual Components
─────────────────────────────
Terminal 1: python enhanced_dispatch_agent.py  (Run once or manually)
Terminal 2: python technician_dashboard.py     (Dashboard at :5000)
Terminal 3: python assignment_analytics_dashboard.py  (Dashboard at :5004)
Terminal 4: python alert_monitor.py            (Run once to check)

Option 2: Automated (RECOMMENDED)
──────────────────────────────────
Terminal 1: python scheduler.py                (Runs dispatch + alerts automatically)
Terminal 2: python technician_dashboard.py     (Dashboard at :5000)
Terminal 3: python assignment_analytics_dashboard.py  (Dashboard at :5004)

Option 3: Quick Start with Checks
───────────────────────────────────
python start_scheduler.py                      (Guided setup + auto-start)
```

---

## 📊 Monitoring Points

### Real-time Monitoring:
- **Console**: Live alert output with color coding
- **alerts.log**: Continuous alert logging
- **Dashboard :5000**: Technician status and assignments
- **Dashboard :5004**: Analytics and trends

### Historical Analysis:
- **alert_history.json**: All alerts for trend analysis
- **dispatch_metrics table**: All assignment metrics
- **Reports**: Daily (8am) and Weekly (Monday 9am)

---

## 🎯 Business Problem Mapping

| Problem | Solution Component | Monitoring | Alert |
|---------|-------------------|------------|-------|
| #1 ETC | `calculate_etc()` | dispatch_metrics.estimated_completion_hours | > 8 hours |
| #2 Routing Speed | `record_metrics()` | dispatch_metrics.routing_speed_seconds | > 300s |
| #3 Fallback Routing | `find_best_match()` with fallback | dispatch_metrics.fallback_technicians | When used |
| #4 Operational Cost | `calculate_operational_cost()` | dispatch_metrics.operational_cost | > $500 |
| #5 Customer Wait Time | Queue monitoring | current_dispatches WHERE status='Pending' | > 20 pending |
| #6 First-Time Fix | Historical analysis | dispatch_history + completion | < 60% |
| #7 Technician Burnout | `get_technician_burnout_risk()` | dispatch_metrics.burnout_alert | 5+ techs |
| #8 Resource Utilization | `utilization_percentage` | technicians.utilization_percentage | < 40% or > 95% |

---

## 🔒 Production Considerations

### Security:
- ✅ Database credentials in config (consider env vars)
- ✅ SMTP passwords should use app-specific passwords
- ✅ Webhook URLs should be kept private
- ⚠️ Consider adding authentication to dashboards

### Reliability:
- ✅ Run scheduler as system service (systemd/Task Scheduler)
- ✅ Database connection retry logic implemented
- ✅ Alert suppression prevents alert storms
- ⚠️ Consider adding dead-letter queue for failed dispatches

### Scalability:
- ✅ Efficient SQL queries with indexes
- ✅ Configurable check intervals
- ⚠️ Consider horizontal scaling for high volume
- ⚠️ Monitor database connection pooling

### Monitoring:
- ✅ Multiple alert channels for redundancy
- ✅ Comprehensive logging
- ✅ Historical data retention
- ⚠️ Consider adding health check endpoint

---

## 📚 File Reference

### Core System:
- `enhanced_dispatch_agent.py` - Main dispatch logic
- `scheduler.py` - Automated orchestration
- `alert_monitor.py` - Metric monitoring
- `alert_config.py` - Configuration
- `notification_handler.py` - Alert delivery

### Dashboards:
- `technician_dashboard.py` - Technician view (:5000)
- `assignment_analytics_dashboard.py` - Analytics (:5004)

### Analysis:
- `analyze_assignments.py` - Deep analysis tool
- `test_alerting.py` - Alert system test

### Documentation:
- `SYSTEM_ARCHITECTURE.md` - This file
- `SCHEDULER_SETUP_GUIDE.md` - Complete setup guide
- `QUICK_START_SCHEDULER.md` - Quick reference
- `FINE_TUNING_GUIDE.md` - Optimization guide

### Startup Helpers:
- `start_scheduler.py` - Guided startup
- `test_connection.py` - Database test

---

## 💡 Best Practices

1. **Development**: Start with manual components, test thoroughly
2. **Testing**: Use `test_alerting.py` to verify alert system
3. **Staging**: Run scheduler for 24 hours, monitor alerts.log
4. **Production**: Run as background service, enable email/webhooks
5. **Maintenance**: Review alert_history.json weekly, adjust thresholds

---

## 🎓 Learning Path

1. **Understand Data**: Run `analyze_assignments.py`
2. **Test Manually**: Run `enhanced_dispatch_agent.py` once
3. **View Results**: Open dashboards (:5000, :5004)
4. **Test Alerts**: Run `test_alerting.py`
5. **Start Automation**: Run `start_scheduler.py`
6. **Monitor**: Watch console and alerts.log
7. **Tune**: Adjust thresholds in `alert_config.py`
8. **Production**: Enable email/webhooks, run as service

---

**Your dispatch system is now fully autonomous with intelligent monitoring!** 🚀


