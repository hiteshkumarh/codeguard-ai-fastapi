from typing import List, Dict
from app.schemas.request_response import Issue
from app.config import settings

def calculate_score(issues: List[Issue]) -> float:
    score = 100.0
    rule_counts: Dict[str, int] = {}
    
    infra_errors = {"LLM Error", "Execution Error", "Environment Error"}
    
    for issue in issues:
        if issue.type in infra_errors:
            continue
            
        rule_counts[issue.type] = rule_counts.get(issue.type, 0) + 1
        
        # Cap penalty to maximum 2 occurrences per rule
        if rule_counts[issue.type] > 2:
            continue
            
        sev = issue.severity.lower()
        if sev == "critical":
            score -= settings.WEIGHT_CRITICAL
        elif sev == "high":
            score -= settings.WEIGHT_HIGH
        elif sev == "medium":
            score -= settings.WEIGHT_MEDIUM
        elif sev == "low":
            score -= settings.WEIGHT_LOW
            
    # Clamp between 0 and 100
    return max(0.0, min(100.0, score))

def calculate_severity_breakdown(issues: List[Issue]) -> Dict[str, int]:
    breakdown = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }
    
    for issue in issues:
        sev = issue.severity.lower()
        if sev in breakdown:
            breakdown[sev] += 1
            
    return breakdown
