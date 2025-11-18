"""
Test the dispatch metrics API to see what data is being returned
"""

import requests
import json

print("="*60)
print("TESTING DISPATCH METRICS API")
print("="*60)

try:
    response = requests.get('http://localhost:5000/api/dispatch-metrics')
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ API Response successful\n")
        print(f"Success: {data.get('success')}")
        print(f"\nSummary:")
        print(json.dumps(data.get('summary', {}), indent=2))
        print(f"\nTrend data points: {len(data.get('trend', []))}")
        if data.get('trend'):
            print("\nTrend data (first 3 entries):")
            for item in data['trend'][:3]:
                print(f"  - {item}")
        else:
            print("\n⚠️ Trend data is EMPTY!")
            print("This is why the chart isn't showing.")
        
        print(f"\nRecent assignments: {len(data.get('recent', []))}")
        
    else:
        print(f"\n❌ API returned status code: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure technician_dashboard.py is running!")

print("="*60)

