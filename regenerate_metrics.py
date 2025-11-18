"""
Clear old metrics and regenerate with fixed routing calculation
"""

import psycopg2

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'options': '-c search_path=team_core_flux'
}

print("="*60)
print("REGENERATING DISPATCH METRICS")
print("="*60)

conn = psycopg2.connect(**DB_CONFIG)
cursor = conn.cursor()

# Check current metrics count
cursor.execute("SELECT COUNT(*) FROM dispatch_metrics;")
old_count = cursor.fetchone()[0]
print(f"\n📊 Current metrics records: {old_count}")

# Clear old metrics
print("\n🗑️  Deleting old metrics...")
cursor.execute("DELETE FROM dispatch_metrics;")
conn.commit()
print(f"✅ Deleted {old_count} old records")

# Reset dispatches to pending so they can be reprocessed
print("\n🔄 Resetting dispatch status to pending...")
cursor.execute("""
    UPDATE current_dispatches
    SET "Optimization_status" = 'pending',
        "Optimized_technician_id" = NULL,
        "Optimization_confidence" = NULL
    WHERE "Optimization_status" = 'completed';
""")
affected = cursor.rowcount
conn.commit()
print(f"✅ Reset {affected} dispatches to pending")

cursor.close()
conn.close()

print("\n" + "="*60)
print("✅ Ready to regenerate metrics!")
print("="*60)
print("\nNext step: Run the enhanced dispatch agent:")
print("  python enhanced_dispatch_agent.py")
print("\nThis will generate new metrics with corrected routing times.")
print("="*60)

