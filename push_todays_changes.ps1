# Quick PowerShell script to push today's changes to GitHub

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Pushing Today's Changes to GitHub" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Step 1: Checking Git status..." -ForegroundColor Yellow
git status
Write-Host ""

Write-Host "Step 2: Adding all changes..." -ForegroundColor Yellow
git add .
Write-Host ""

Write-Host "Step 3: Committing changes..." -ForegroundColor Yellow
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

Write-Host ""
Write-Host "Step 4: Pushing to GitHub..." -ForegroundColor Yellow
git push origin main

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "✅ Done! Check your GitHub repository:" -ForegroundColor Green
Write-Host "https://github.com/kiranmanichalla5-design/Smart-Dispatch-AI-Agent" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Green

