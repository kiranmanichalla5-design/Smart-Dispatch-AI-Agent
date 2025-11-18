#!/bin/bash
# Quick script to push today's changes to GitHub

echo "=========================================="
echo "Pushing Today's Changes to GitHub"
echo "=========================================="
echo ""

echo "Step 1: Checking Git status..."
git status
echo ""

echo "Step 2: Adding all changes..."
git add .
echo ""

echo "Step 3: Committing changes..."
git commit -m "Fix: Populated 13-day trend data from existing dispatches (Dec 1-13, 2025)

- Added 8 new scripts for data search, population, and testing
- Fixed dashboard API bugs (Decimal conversions, case-sensitivity, JSON parsing)
- Improved trend chart with Chart.js integration
- Cleaned up old metrics data outside target date range
- Enhanced error handling and empty state displays
- Updated enhanced_dispatch_agent.py to fix Created_at column issue

New files:
- search_existing_data.py
- check_all_tables.py
- check_columns.py
- check_metrics_data.py
- debug_trend_dates.py
- populate_metrics_from_dispatches.py
- cleanup_old_metrics.py
- test_trend_api.py
- TODAY_CHANGES_SUMMARY.md

Modified files:
- technician_dashboard.py
- templates/technician_dashboard.html
- enhanced_dispatch_agent.py"

echo ""
echo "Step 4: Pushing to GitHub..."
git push origin main

echo ""
echo "=========================================="
echo "✅ Done! Check your GitHub repository:"
echo "https://github.com/kiranmanichalla5-design/Smart-Dispatch-AI-Agent"
echo "=========================================="

