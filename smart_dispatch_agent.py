"""
Smart Dispatch Agent - MVP Implementation
Matches technicians to dispatch requests based on skills, location, and availability.
"""

import psycopg2
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime
import math

# Database configuration
DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

SCHEMA_NAME = 'team_core_flux'


@dataclass
class Technician:
    """Technician data structure"""
    technician_id: str
    name: str
    primary_skill: str
    city: str
    state: str
    latitude: float
    longitude: float
    workload_capacity: int
    current_assignments: int
    available: bool = True


@dataclass
class Dispatch:
    """Dispatch request data structure"""
    dispatch_id: int
    ticket_type: str
    priority: str
    required_skill: str
    city: str
    state: str
    customer_latitude: float
    customer_longitude: float
    appointment_start_datetime: str
    appointment_end_datetime: str
    duration_min: int


class SmartDispatchAgent:
    """
    Smart Dispatch Agent that matches technicians to dispatch requests.
    """
    
    def __init__(self):
        self.connection = None
        self.connect_to_database()
    
    def connect_to_database(self):
        """Connect to PostgreSQL database"""
        try:
            self.connection = psycopg2.connect(**DB_CONFIG)
            print("✓ Connected to database")
        except psycopg2.Error as e:
            print(f"✗ Database connection error: {e}")
            raise
    
    def calculate_distance(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate distance between two coordinates using Haversine formula.
        Returns distance in kilometers.
        """
        R = 6371  # Earth radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon / 2) ** 2)
        
        c = 2 * math.asin(math.sqrt(a))
        distance = R * c
        
        return distance
    
    def skill_match_score(self, technician_skill: str, required_skill: str) -> float:
        """
        Calculate skill matching score (0-1).
        Exact match = 1.0, partial match = 0.5, no match = 0.0
        """
        tech_skill_lower = technician_skill.lower()
        req_skill_lower = required_skill.lower()
        
        if tech_skill_lower == req_skill_lower:
            return 1.0
        
        # Partial matching (e.g., "Service restoration" matches "restoration")
        if req_skill_lower in tech_skill_lower or tech_skill_lower in req_skill_lower:
            return 0.7
        
        # Check for related skills (simple keyword matching)
        related_skills = {
            'installation': ['install', 'setup', 'deploy'],
            'repair': ['restoration', 'fix', 'maintenance'],
            'diagnosis': ['diagnostic', 'troubleshoot', 'test']
        }
        
        for category, keywords in related_skills.items():
            if category in req_skill_lower:
                if any(kw in tech_skill_lower for kw in keywords):
                    return 0.5
        
        return 0.0
    
    def availability_score(self, technician: Technician) -> float:
        """
        Calculate availability score based on current workload.
        Returns 1.0 if fully available, decreases as workload increases.
        """
        if technician.workload_capacity == 0:
            return 0.0
        
        utilization = technician.current_assignments / technician.workload_capacity
        return max(0.0, 1.0 - utilization)
    
    def get_available_technicians(self, required_skill: str, state: str, 
                                  appointment_date: str) -> List[Technician]:
        """
        Query database for available technicians matching criteria.
        """
        cursor = self.connection.cursor()
        
        try:
            # Query technicians with matching skill and state
            query = """
                SELECT 
                    t."Technician_id",
                    t."Name",
                    t."Primary_skill",
                    t."City",
                    t."State",
                    t."Latitude",
                    t."Longitude",
                    t."Workload_capacity",
                    t."Current_assignments"
                FROM "team_core_flux"."technicians" t
                WHERE t."State" = %s
                AND t."Current_assignments" < t."Workload_capacity"
                ORDER BY t."Current_assignments" ASC;
            """
            
            cursor.execute(query, (state,))
            rows = cursor.fetchall()
            
            technicians = []
            for row in rows:
                tech = Technician(
                    technician_id=row[0],
                    name=row[1],
                    primary_skill=row[2] or "",
                    city=row[3] or "",
                    state=row[4] or "",
                    latitude=float(row[5]) if row[5] else 0.0,
                    longitude=float(row[6]) if row[6] else 0.0,
                    workload_capacity=int(row[7]) if row[7] else 0,
                    current_assignments=int(row[8]) if row[8] else 0
                )
                
                # Check calendar availability (simplified - can be enhanced)
                tech.available = self.check_calendar_availability(
                    tech.technician_id, appointment_date
                )
                
                if tech.available:
                    technicians.append(tech)
            
            return technicians
            
        except psycopg2.Error as e:
            print(f"Error querying technicians: {e}")
            return []
        finally:
            cursor.close()
    
    def check_calendar_availability(self, technician_id: str, date: str) -> bool:
        """
        Check if technician is available on the given date.
        Simplified version - can be enhanced with time slot checking.
        """
        cursor = self.connection.cursor()
        
        try:
            query = """
                SELECT "Available", "Max_assignments"
                FROM "team_core_flux"."technician_calendar"
                WHERE "Technician_id" = %s
                AND "Date" = %s
                LIMIT 1;
            """
            
            cursor.execute(query, (technician_id, date.split()[0]))  # Extract date part
            result = cursor.fetchone()
            
            if result:
                available = result[0] == 1
                max_assignments = result[1] or 0
                return available and max_assignments > 0
            
            return True  # Default to available if no calendar entry
            
        except psycopg2.Error as e:
            print(f"Error checking calendar: {e}")
            return True
        finally:
            cursor.close()
    
    def get_historical_performance(self, technician_id: str, required_skill: str) -> Dict:
        """
        Get historical performance metrics for a technician.
        """
        cursor = self.connection.cursor()
        
        try:
            query = """
                SELECT 
                    COUNT(*) as total_dispatches,
                    AVG("Productive_dispatch") as avg_productive,
                    AVG("First_time_fix") as avg_first_time_fix,
                    AVG("Distance_km") as avg_distance
                FROM "team_core_flux"."dispatch_history"
                WHERE "Assigned_technician_id" = %s
                AND "Required_skill" = %s
                AND "Status" = 'Completed';
            """
            
            cursor.execute(query, (technician_id, required_skill))
            result = cursor.fetchone()
            
            if result and result[0] > 0:
                return {
                    'total_dispatches': result[0] or 0,
                    'avg_productive': float(result[1]) if result[1] else 0.0,
                    'avg_first_time_fix': float(result[2]) if result[2] else 0.0,
                    'avg_distance': float(result[3]) if result[3] else 0.0
                }
            
            return {
                'total_dispatches': 0,
                'avg_productive': 0.5,  # Default neutral score
                'avg_first_time_fix': 0.5,
                'avg_distance': 0.0
            }
            
        except psycopg2.Error as e:
            print(f"Error getting historical performance: {e}")
            return {'total_dispatches': 0, 'avg_productive': 0.5, 
                   'avg_first_time_fix': 0.5, 'avg_distance': 0.0}
        finally:
            cursor.close()
    
    def score_technician(self, technician: Technician, dispatch: Dispatch) -> Dict:
        """
        Calculate overall score for a technician-dispatch match.
        Returns score and details.
        """
        # Skill matching (weight: 40%)
        skill_score = self.skill_match_score(technician.primary_skill, dispatch.required_skill)
        
        # Distance (weight: 30%) - closer is better
        distance_km = self.calculate_distance(
            technician.latitude, technician.longitude,
            dispatch.customer_latitude, dispatch.customer_longitude
        )
        distance_score = max(0.0, 1.0 - (distance_km / 100.0))  # Normalize to 100km
        
        # Availability (weight: 20%)
        availability_score = self.availability_score(technician)
        
        # Historical performance (weight: 10%)
        history = self.get_historical_performance(technician.technician_id, dispatch.required_skill)
        performance_score = (history['avg_productive'] + history['avg_first_time_fix']) / 2.0
        
        # Priority adjustment
        priority_multiplier = {
            'Critical': 1.2,
            'High': 1.1,
            'Normal': 1.0,
            'Low': 0.9
        }.get(dispatch.priority, 1.0)
        
        # Weighted total score
        total_score = (
            skill_score * 0.4 +
            distance_score * 0.3 +
            availability_score * 0.2 +
            performance_score * 0.1
        ) * priority_multiplier
        
        return {
            'technician': technician,
            'total_score': total_score,
            'skill_score': skill_score,
            'distance_km': distance_km,
            'distance_score': distance_score,
            'availability_score': availability_score,
            'performance_score': performance_score,
            'history': history
        }
    
    def find_best_match(self, dispatch: Dispatch, top_n: int = 5) -> List[Dict]:
        """
        Find the best matching technicians for a dispatch request.
        Returns top N candidates with scores.
        """
        print(f"\n🔍 Finding best match for Dispatch ID: {dispatch.dispatch_id}")
        print(f"   Required Skill: {dispatch.required_skill}")
        print(f"   Priority: {dispatch.priority}")
        print(f"   Location: {dispatch.city}, {dispatch.state}")
        
        # Get available technicians
        technicians = self.get_available_technicians(
            dispatch.required_skill,
            dispatch.state,
            dispatch.appointment_start_datetime
        )
        
        if not technicians:
            print("   ⚠ No available technicians found")
            return []
        
        print(f"   Found {len(technicians)} available technician(s)")
        
        # Score each technician
        scored_candidates = []
        for tech in technicians:
            score_data = self.score_technician(tech, dispatch)
            scored_candidates.append(score_data)
        
        # Sort by total score (descending)
        scored_candidates.sort(key=lambda x: x['total_score'], reverse=True)
        
        # Return top N
        return scored_candidates[:top_n]
    
    def assign_technician(self, dispatch_id: int, technician_id: str, 
                         confidence_score: float) -> bool:
        """
        Update the dispatch with the assigned technician.
        """
        cursor = self.connection.cursor()
        
        try:
            update_query = """
                UPDATE "team_core_flux"."current_dispatches"
                SET 
                    "Optimized_technician_id" = %s,
                    "Optimization_status" = 'completed',
                    "Optimization_timestamp" = %s,
                    "Optimization_confidence" = %s
                WHERE "Dispatch_id" = %s;
            """
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(update_query, (
                technician_id,
                timestamp,
                str(round(confidence_score, 2)),
                dispatch_id
            ))
            
            self.connection.commit()
            print(f"✓ Assigned technician {technician_id} to dispatch {dispatch_id}")
            return True
            
        except psycopg2.Error as e:
            print(f"✗ Error assigning technician: {e}")
            self.connection.rollback()
            return False
        finally:
            cursor.close()
    
    def process_dispatch(self, dispatch_id: int) -> Optional[Dict]:
        """
        Process a single dispatch request and assign best technician.
        """
        cursor = self.connection.cursor()
        
        try:
            # Fetch dispatch details
            query = """
                SELECT 
                    "Dispatch_id",
                    "Ticket_type",
                    "Priority",
                    "Required_skill",
                    "City",
                    "State",
                    "Customer_latitude",
                    "Customer_longitude",
                    "Appointment_start_datetime",
                    "Appointment_end_datetime",
                    "Duration_min"
                FROM "team_core_flux"."current_dispatches"
                WHERE "Dispatch_id" = %s
                AND "Optimization_status" = 'pending';
            """
            
            cursor.execute(query, (dispatch_id,))
            row = cursor.fetchone()
            
            if not row:
                print(f"✗ Dispatch {dispatch_id} not found or already processed")
                return None
            
            # Create Dispatch object
            dispatch = Dispatch(
                dispatch_id=row[0],
                ticket_type=row[1] or "",
                priority=row[2] or "Normal",
                required_skill=row[3] or "",
                city=row[4] or "",
                state=row[5] or "",
                customer_latitude=float(row[6]) if row[6] else 0.0,
                customer_longitude=float(row[7]) if row[7] else 0.0,
                appointment_start_datetime=row[8] or "",
                appointment_end_datetime=row[9] or "",
                duration_min=int(row[10]) if row[10] else 0
            )
            
            # Find best matches
            candidates = self.find_best_match(dispatch, top_n=3)
            
            if not candidates:
                return None
            
            # Display results
            print(f"\n📊 Top Candidates:")
            print("-" * 80)
            for i, candidate in enumerate(candidates, 1):
                tech = candidate['technician']
                print(f"\n{i}. {tech.name} ({tech.technician_id})")
                print(f"   Total Score: {candidate['total_score']:.3f}")
                print(f"   - Skill Match: {candidate['skill_score']:.2f}")
                print(f"   - Distance: {candidate['distance_km']:.2f} km (score: {candidate['distance_score']:.2f})")
                print(f"   - Availability: {candidate['availability_score']:.2f}")
                print(f"   - Performance: {candidate['performance_score']:.2f}")
                print(f"   - Current Assignments: {tech.current_assignments}/{tech.workload_capacity}")
            
            # Assign best match
            best_match = candidates[0]
            success = self.assign_technician(
                dispatch_id,
                best_match['technician'].technician_id,
                best_match['total_score']
            )
            
            if success:
                return {
                    'dispatch_id': dispatch_id,
                    'assigned_technician': best_match['technician'].technician_id,
                    'confidence': best_match['total_score'],
                    'alternatives': [
                        {
                            'technician_id': c['technician'].technician_id,
                            'score': c['total_score']
                        }
                        for c in candidates[1:]
                    ]
                }
            
            return None
            
        except psycopg2.Error as e:
            print(f"✗ Error processing dispatch: {e}")
            return None
        finally:
            cursor.close()
    
    def process_pending_dispatches(self, limit: int = 10) -> List[Dict]:
        """
        Process multiple pending dispatches.
        """
        cursor = self.connection.cursor()
        
        try:
            query = """
                SELECT "Dispatch_id"
                FROM "team_core_flux"."current_dispatches"
                WHERE "Optimization_status" = 'pending'
                ORDER BY 
                    CASE "Priority"
                        WHEN 'Critical' THEN 1
                        WHEN 'High' THEN 2
                        WHEN 'Normal' THEN 3
                        WHEN 'Low' THEN 4
                        ELSE 5
                    END,
                    "Dispatch_id"
                LIMIT %s;
            """
            
            cursor.execute(query, (limit,))
            dispatch_ids = [row[0] for row in cursor.fetchall()]
            
            results = []
            for dispatch_id in dispatch_ids:
                result = self.process_dispatch(dispatch_id)
                if result:
                    results.append(result)
            
            return results
            
        except psycopg2.Error as e:
            print(f"✗ Error fetching pending dispatches: {e}")
            return []
        finally:
            cursor.close()
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            print("✓ Database connection closed")


def main():
    """Main function to run the dispatch agent"""
    print("=" * 80)
    print("SMART DISPATCH AGENT - MVP")
    print("=" * 80)
    
    agent = SmartDispatchAgent()
    
    try:
        # Process pending dispatches
        print("\n🚀 Processing pending dispatches...")
        results = agent.process_pending_dispatches(limit=5)
        
        print(f"\n✅ Processed {len(results)} dispatch(es)")
        
        # Example: Process a specific dispatch
        # result = agent.process_dispatch(200000495)
        
    finally:
        agent.close()


if __name__ == "__main__":
    main()

