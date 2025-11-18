"""
Analyze Dispatch Assignments - Understand Current Patterns
Shows how technicians are assigned based on priority, status, and skills.
"""

import psycopg2
from collections import defaultdict
import json

DB_CONFIG = {
    'host': '212.2.245.85',
    'port': 6432,
    'user': 'postgres',
    'password': 'Tea_IWMZ5wuUta97gupb',
    'database': 'postgres'
}

SCHEMA_NAME = 'team_core_flux'


def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)


def analyze_by_priority():
    """Analyze assignments by priority level"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            d."Priority",
            d."Optimization_status",
            COUNT(*) as count,
            COUNT(DISTINCT d."Optimized_technician_id") as unique_technicians,
            COUNT(DISTINCT d."Required_skill") as unique_skills
        FROM "team_core_flux"."current_dispatches" d
        WHERE d."Priority" IS NOT NULL
        GROUP BY d."Priority", d."Optimization_status"
        ORDER BY 
            CASE d."Priority"
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Normal' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END,
            d."Optimization_status";
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("ASSIGNMENT ANALYSIS BY PRIORITY")
    print("="*80)
    print(f"{'Priority':<12} {'Status':<12} {'Count':<10} {'Unique Techs':<15} {'Unique Skills':<15}")
    print("-"*80)
    
    priority_stats = defaultdict(lambda: {'completed': 0, 'pending': 0, 'techs': set(), 'skills': set()})
    
    for row in results:
        priority, status, count, techs, skills = row
        print(f"{priority or 'N/A':<12} {status or 'N/A':<12} {count:<10} {techs:<15} {skills:<15}")
        
        if status == 'completed':
            priority_stats[priority]['completed'] = count
        elif status == 'pending':
            priority_stats[priority]['pending'] = count
    
    cursor.close()
    conn.close()
    
    return priority_stats


def analyze_by_skill():
    """Analyze assignments by required skill"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            d."Required_skill",
            d."Optimization_status",
            COUNT(*) as count,
            COUNT(DISTINCT d."Optimized_technician_id") as unique_technicians,
            STRING_AGG(DISTINCT d."Priority", ', ') as priorities
        FROM "team_core_flux"."current_dispatches" d
        WHERE d."Required_skill" IS NOT NULL
        GROUP BY d."Required_skill", d."Optimization_status"
        ORDER BY d."Required_skill", d."Optimization_status";
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("ASSIGNMENT ANALYSIS BY SKILL")
    print("="*80)
    print(f"{'Skill':<40} {'Status':<12} {'Count':<10} {'Unique Techs':<15} {'Priorities':<20}")
    print("-"*80)
    
    skill_stats = {}
    
    for row in results:
        skill, status, count, techs, priorities = row
        skill_display = (skill[:37] + '...') if skill and len(skill) > 40 else (skill or 'N/A')
        print(f"{skill_display:<40} {status or 'N/A':<12} {count:<10} {techs:<15} {priorities or 'N/A':<20}")
        
        if skill not in skill_stats:
            skill_stats[skill] = {'completed': 0, 'pending': 0, 'techs': set()}
        
        if status == 'completed':
            skill_stats[skill]['completed'] = count
        elif status == 'pending':
            skill_stats[skill]['pending'] = count
    
    cursor.close()
    conn.close()
    
    return skill_stats


def analyze_technician_assignments():
    """Analyze how technicians are assigned"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            t."Technician_id",
            t."Name",
            t."Primary_skill",
            COUNT(d."Dispatch_id") as total_assignments,
            COUNT(CASE WHEN d."Priority" = 'Critical' THEN 1 END) as critical_count,
            COUNT(CASE WHEN d."Priority" = 'High' THEN 1 END) as high_count,
            COUNT(CASE WHEN d."Priority" = 'Normal' THEN 1 END) as normal_count,
            COUNT(CASE WHEN d."Priority" = 'Low' THEN 1 END) as low_count,
            COUNT(DISTINCT d."Required_skill") as unique_skills_assigned,
            AVG(CAST(d."Optimization_confidence" AS FLOAT)) as avg_confidence
        FROM "team_core_flux"."technicians" t
        LEFT JOIN "team_core_flux"."current_dispatches" d
            ON t."Technician_id" = d."Optimized_technician_id"
            AND d."Optimization_status" = 'completed'
        GROUP BY t."Technician_id", t."Name", t."Primary_skill"
        HAVING COUNT(d."Dispatch_id") > 0
        ORDER BY total_assignments DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("TECHNICIAN ASSIGNMENT ANALYSIS")
    print("="*80)
    print(f"{'Tech ID':<12} {'Name':<25} {'Primary Skill':<30} {'Total':<8} {'Critical':<10} {'High':<8} {'Normal':<8} {'Low':<8} {'Skills':<8} {'Avg Conf':<10}")
    print("-"*80)
    
    tech_stats = []
    
    for row in results:
        tech_id, name, skill, total, critical, high, normal, low, unique_skills, avg_conf = row
        name_display = (name[:23] + '..') if name and len(name) > 25 else (name or 'N/A')
        skill_display = (skill[:28] + '..') if skill and len(skill) > 30 else (skill or 'N/A')
        
        print(f"{tech_id or 'N/A':<12} {name_display:<25} {skill_display:<30} {total or 0:<8} {critical or 0:<10} {high or 0:<8} {normal or 0:<8} {low or 0:<8} {unique_skills or 0:<8} {(avg_conf or 0):.2f}")
        
        tech_stats.append({
            'tech_id': tech_id,
            'name': name,
            'primary_skill': skill,
            'total': total,
            'critical': critical,
            'high': high,
            'normal': normal,
            'low': low,
            'unique_skills': unique_skills,
            'avg_confidence': avg_conf
        })
    
    cursor.close()
    conn.close()
    
    return tech_stats


def analyze_skill_matching():
    """Analyze how well skills are matched"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            d."Required_skill",
            t."Primary_skill",
            COUNT(*) as count,
            AVG(CAST(d."Optimization_confidence" AS FLOAT)) as avg_confidence
        FROM "team_core_flux"."current_dispatches" d
        JOIN "team_core_flux"."technicians" t
            ON d."Optimized_technician_id" = t."Technician_id"
        WHERE d."Optimization_status" = 'completed'
            AND d."Required_skill" IS NOT NULL
            AND t."Primary_skill" IS NOT NULL
        GROUP BY d."Required_skill", t."Primary_skill"
        ORDER BY count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("SKILL MATCHING ANALYSIS")
    print("="*80)
    print(f"{'Required Skill':<35} {'Tech Skill':<35} {'Count':<10} {'Avg Confidence':<15}")
    print("-"*80)
    
    exact_matches = 0
    total_assignments = 0
    
    for row in results:
        req_skill, tech_skill, count, avg_conf = row
        req_display = (req_skill[:33] + '..') if req_skill and len(req_skill) > 35 else (req_skill or 'N/A')
        tech_display = (tech_skill[:33] + '..') if tech_skill and len(tech_skill) > 35 else (tech_skill or 'N/A')
        
        match_indicator = "✅" if req_skill and tech_skill and req_skill.lower() == tech_skill.lower() else "⚠️"
        
        print(f"{req_display:<35} {tech_display:<35} {count or 0:<10} {(avg_conf or 0):.2f} {match_indicator}")
        
        total_assignments += (count or 0)
        if req_skill and tech_skill and req_skill.lower() == tech_skill.lower():
            exact_matches += (count or 0)
    
    if total_assignments > 0:
        match_rate = (exact_matches / total_assignments) * 100
        print(f"\n📊 Exact Skill Match Rate: {match_rate:.1f}% ({exact_matches}/{total_assignments})")
    
    cursor.close()
    conn.close()


def analyze_pending_dispatches():
    """Analyze pending dispatches and why they might not be assigned"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT 
            d."Priority",
            d."Required_skill",
            d."State",
            COUNT(*) as count
        FROM "team_core_flux"."current_dispatches" d
        WHERE d."Optimization_status" = 'pending'
        GROUP BY d."Priority", d."Required_skill", d."State"
        ORDER BY 
            CASE d."Priority"
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Normal' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END,
            count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("PENDING DISPATCHES ANALYSIS")
    print("="*80)
    print(f"{'Priority':<12} {'Required Skill':<35} {'State':<10} {'Count':<10}")
    print("-"*80)
    
    for row in results:
        priority, skill, state, count = row
        skill_display = (skill[:33] + '..') if skill and len(skill) > 35 else (skill or 'N/A')
        print(f"{priority or 'N/A':<12} {skill_display:<35} {state or 'N/A':<10} {count or 0:<10}")
    
    cursor.close()
    conn.close()


def check_available_technicians_for_pending():
    """Check if there are available technicians for pending dispatches"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
        SELECT DISTINCT
            d."Required_skill",
            d."State",
            COUNT(DISTINCT d."Dispatch_id") as pending_count,
            COUNT(DISTINCT t."Technician_id") as available_techs
        FROM "team_core_flux"."current_dispatches" d
        LEFT JOIN "team_core_flux"."technicians" t
            ON t."State" = d."State"
            AND t."Current_assignments" < t."Workload_capacity"
        WHERE d."Optimization_status" = 'pending'
            AND d."Required_skill" IS NOT NULL
            AND d."State" IS NOT NULL
        GROUP BY d."Required_skill", d."State"
        ORDER BY pending_count DESC;
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("\n" + "="*80)
    print("AVAILABILITY CHECK FOR PENDING DISPATCHES")
    print("="*80)
    print(f"{'Required Skill':<35} {'State':<10} {'Pending':<10} {'Available Techs':<20}")
    print("-"*80)
    
    for row in results:
        skill, state, pending, available = row
        skill_display = (skill[:33] + '..') if skill and len(skill) > 35 else (skill or 'N/A')
        status = "✅" if available > 0 else "❌"
        print(f"{skill_display:<35} {state or 'N/A':<10} {pending or 0:<10} {available or 0:<20} {status}")
    
    cursor.close()
    conn.close()

def analyze_dispatch_metrics():
    """Analyze routing speed, cost, and SLA compliance"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS "team_core_flux"."dispatch_metrics" (
                dispatch_id BIGINT PRIMARY KEY,
                technician_id TEXT,
                priority TEXT,
                required_skill TEXT,
                state TEXT,
                routing_seconds INTEGER,
                estimated_completion_minutes INTEGER,
                travel_km NUMERIC,
                operational_cost NUMERIC,
                fallback_technicians JSONB,
                burnout_risk BOOLEAN,
                sla_breached BOOLEAN,
                created_at TIMESTAMP DEFAULT NOW(),
                updated_at TIMESTAMP DEFAULT NOW()
            );
        """)
        conn.commit()

        cursor.execute("""
            SELECT 
                COALESCE(AVG(routing_seconds) / 60.0, 0) as avg_routing_minutes,
                COALESCE(AVG(estimated_completion_minutes), 0) as avg_etc_minutes,
                COALESCE(AVG(operational_cost), 0) as avg_cost,
                COALESCE(SUM(CASE WHEN sla_breached THEN 1 ELSE 0 END), 0) as sla_breaches,
                COUNT(*) as total_records,
                COALESCE(SUM(CASE WHEN burnout_risk THEN 1 ELSE 0 END), 0) as burnout_alerts
            FROM "team_core_flux"."dispatch_metrics";
        """)
        summary = cursor.fetchone()
        total_records = summary[4] or 0
        sla_breaches = summary[3] or 0
        sla_compliance = 0.0
        if total_records > 0:
            sla_compliance = 100 - (sla_breaches / total_records) * 100

        print("\n" + "="*80)
        print("DISPATCH METRICS (Routing & Cost)")
        print("="*80)
        print(f"Average Routing Time: {(summary[0] or 0):.2f} minutes")
        print(f"Average Completion Time: {(summary[1] or 0):.2f} minutes")
        print(f"Average Operational Cost: ${(summary[2] or 0):.2f}")
        print(f"SLA Compliance: {sla_compliance:.1f}%")
        print(f"Burnout Alerts Logged: {int(summary[5] or 0)}")

        cursor.execute("""
            SELECT 
                d."Priority",
                COALESCE(AVG(dm.operational_cost), 0) as avg_cost,
                COUNT(*) as count
            FROM "team_core_flux"."dispatch_metrics" dm
            JOIN "team_core_flux"."current_dispatches" d
                ON dm.dispatch_id = d."Dispatch_id"
            GROUP BY d."Priority"
            ORDER BY avg_cost DESC;
        """)
        rows = cursor.fetchall()

        print("\nOperational Cost by Priority:")
        print(f"{'Priority':<12} {'Avg Cost':<12} {'Count':<10}")
        print("-"*80)
        for row in rows:
            print(f"{row[0] or 'N/A':<12} ${float(row[1] or 0):<12.2f} {row[2] or 0:<10}")
    except psycopg2.Error as e:
        print(f"Warning: Unable to analyze dispatch metrics: {e}")
    finally:
        cursor.close()
        conn.close()

def generate_summary_report():
    """Generate a comprehensive summary report"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Overall stats
    cursor.execute("""
        SELECT 
            COUNT(*) as total_dispatches,
            COUNT(CASE WHEN "Optimization_status" = 'completed' THEN 1 END) as completed,
            COUNT(CASE WHEN "Optimization_status" = 'pending' THEN 1 END) as pending,
            COUNT(DISTINCT "Optimized_technician_id") as unique_technicians_assigned
        FROM "team_core_flux"."current_dispatches";
    """)
    
    total, completed, pending, unique_techs = cursor.fetchone()
    
    print("\n" + "="*80)
    print("SUMMARY REPORT")
    print("="*80)
    print(f"Total Dispatches: {total or 0}")
    print(f"Completed Assignments: {completed or 0} ({(completed/total*100) if total > 0 else 0:.1f}%)")
    print(f"Pending Assignments: {pending or 0} ({(pending/total*100) if total > 0 else 0:.1f}%)")
    print(f"Unique Technicians Assigned: {unique_techs or 0}")
    
    cursor.close()
    conn.close()


def main():
    print("="*80)
    print("DISPATCH ASSIGNMENT ANALYSIS")
    print("="*80)
    
    # Run all analyses
    generate_summary_report()
    analyze_by_priority()
    analyze_by_skill()
    analyze_technician_assignments()
    analyze_skill_matching()
    analyze_pending_dispatches()
    check_available_technicians_for_pending()
    analyze_dispatch_metrics()
    
    print("\n" + "="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print("\n💡 Recommendations:")
    print("1. Review skill matching rates - improve matching algorithm if needed")
    print("2. Check pending dispatches - ensure technicians are available")
    print("3. Balance workload - distribute assignments evenly")
    print("4. Prioritize critical dispatches - ensure they get best matches")
    print("5. Investigate SLA breaches and routing delays")
    print("6. Address burnout alerts before they impact turnover")
    print("="*80)


if __name__ == "__main__":
    main()

