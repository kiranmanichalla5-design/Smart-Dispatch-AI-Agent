# Smart Dispatch Agent - Implementation Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements_dispatch.txt
```

### 2. Run the Basic Agent

```bash
python smart_dispatch_agent.py
```

This will:
- Connect to your PostgreSQL database
- Find pending dispatches
- Match technicians based on skills, location, and availability
- Update the database with optimized assignments

## 📋 How It Works

### Matching Algorithm

The agent scores technicians using:

1. **Skill Matching (40% weight)**
   - Exact match: 1.0
   - Partial match: 0.7
   - Related skills: 0.5
   - No match: 0.0

2. **Distance (30% weight)**
   - Calculates distance using Haversine formula
   - Closer technicians score higher
   - Normalized to 100km range

3. **Availability (20% weight)**
   - Based on current workload vs capacity
   - Checks technician calendar
   - Less utilized technicians score higher

4. **Historical Performance (10% weight)**
   - First-time-fix rate
   - Productive dispatch rate
   - Based on past assignments with same skill

5. **Priority Adjustment**
   - Critical: +20%
   - High: +10%
   - Normal: 0%
   - Low: -10%

### Example Output

```
🔍 Finding best match for Dispatch ID: 200000495
   Required Skill: Line repair
   Priority: Critical
   Location: Dallas, TX
   Found 5 available technician(s)

📊 Top Candidates:
--------------------------------------------------------------------------------

1. John Smith (T900045)
   Total Score: 0.856
   - Skill Match: 1.00
   - Distance: 12.34 km (score: 0.88)
   - Availability: 0.80
   - Performance: 0.75
   - Current Assignments: 2/10

2. Jane Doe (T900123)
   Total Score: 0.742
   ...
```

## 🔧 Next Steps: Adding LLM Intelligence

### Option 1: Add Ollama (Local, Free)

```python
# Install Ollama: https://ollama.ai
# Then: ollama pull llama3

from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate

llm = Ollama(model="llama3")

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a dispatch optimization expert."),
    ("human", "Given these technician candidates: {candidates}, which is best for dispatch {dispatch_id}? Consider skill match, distance, and availability.")
])

chain = prompt | llm
response = chain.invoke({"candidates": candidates, "dispatch_id": dispatch_id})
```

### Option 2: Add Claude API (Production)

```python
from langchain_anthropic import ChatAnthropic
import os

os.environ["ANTHROPIC_API_KEY"] = "your-api-key"

llm = ChatAnthropic(model="claude-sonnet-4-20250514")

# Use in your scoring logic
reasoning = llm.invoke(f"Analyze technician {tech_id} for dispatch {dispatch_id}")
```

### Option 3: Add LangGraph (Complex Workflows)

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict

class DispatchState(TypedDict):
    dispatch_id: int
    candidates: List[Dict]
    selected_technician: Optional[str]
    reasoning: str

def find_candidates(state: DispatchState):
    # Your existing logic
    return {"candidates": candidates}

def llm_reasoning(state: DispatchState):
    # LLM analyzes candidates
    return {"reasoning": llm_response}

def assign_technician(state: DispatchState):
    # Update database
    return {"selected_technician": best_match}

workflow = StateGraph(DispatchState)
workflow.add_node("find_candidates", find_candidates)
workflow.add_node("llm_reasoning", llm_reasoning)
workflow.add_node("assign", assign_technician)
workflow.set_entry_point("find_candidates")
workflow.add_edge("find_candidates", "llm_reasoning")
workflow.add_edge("llm_reasoning", "assign")
workflow.add_edge("assign", END)
```

## 🔄 Integration with n8n

### Webhook Trigger

1. Create n8n workflow
2. Add webhook node
3. Configure to trigger on new dispatch
4. Call your Python API:

```python
# dispatch_api.py
from flask import Flask, request
from smart_dispatch_agent import SmartDispatchAgent

app = Flask(__name__)
agent = SmartDispatchAgent()

@app.route('/dispatch/assign', methods=['POST'])
def assign_dispatch():
    data = request.json
    dispatch_id = data['dispatch_id']
    result = agent.process_dispatch(dispatch_id)
    return result

if __name__ == '__main__':
    app.run(port=5000)
```

## 📊 Power BI Integration

### Direct PostgreSQL Connection

1. Open Power BI
2. Get Data → PostgreSQL
3. Connect to your database
4. Import tables:
   - `current_dispatches`
   - `technicians`
   - `dispatch_history`

### Key Metrics to Track

- **Optimization Rate**: % of dispatches with optimized assignments
- **Average Confidence Score**: Quality of matches
- **Distance Efficiency**: Average distance per dispatch
- **First-Time-Fix Rate**: By technician and skill
- **Response Time**: Time to assign technician

### Sample Query

```sql
SELECT 
    DATE("Optimization_timestamp") as date,
    COUNT(*) as total_dispatches,
    AVG(CAST("Optimization_confidence" AS FLOAT)) as avg_confidence,
    AVG("Distance_km") as avg_distance
FROM "team_core_flux"."current_dispatches"
WHERE "Optimization_status" = 'completed'
GROUP BY DATE("Optimization_timestamp")
ORDER BY date DESC;
```

## 🎯 Technology Integration Summary

### Current Implementation (MVP)
- ✅ Python (core logic)
- ✅ PostgreSQL (data)
- ✅ Basic matching algorithm

### Phase 2: Add LLM
- Add Ollama or Claude API
- Use LangChain for integration
- Enhance reasoning capabilities

### Phase 3: Add Orchestration
- LangGraph for complex workflows
- n8n for automation triggers
- API endpoints for integration

### Phase 4: Add Analytics
- Databricks for ML models
- Power BI for dashboards
- Advanced performance tracking

## 🐛 Troubleshooting

### Database Connection Issues
```python
# Test connection
python -c "import psycopg2; conn = psycopg2.connect(host='212.2.245.85', port=6432, user='postgres', password='Tea_IWMZ5wuUta97gupb', database='postgres'); print('Connected!')"
```

### No Technicians Found
- Check state matching
- Verify availability (workload < capacity)
- Check calendar entries

### Low Scores
- Verify skill names match exactly
- Check distance calculations
- Review historical data

## 📚 Next Steps

1. **Test the basic agent**: Run `python smart_dispatch_agent.py`
2. **Review results**: Check `current_dispatches` table for `Optimized_technician_id`
3. **Add LLM**: Choose Ollama (free) or Claude (production)
4. **Enhance matching**: Add more factors (time windows, equipment, etc.)
5. **Build API**: Create REST endpoint for integration
6. **Add monitoring**: Track performance metrics

